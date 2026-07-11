#!/usr/bin/env python3
"""
Gerador de novos módulos para o Back Office SEC4DATA.

Uso:
    python3 scripts/new_module.py --name evento --label "Eventos" \\
        --fields "titulo:text:true,descricao:textarea,data:text,ativo:boolean"

Tipos de campo suportados: text, textarea, boolean, number

Gera:
    backend/app/models/<name>.py
    backend/app/schemas/<name>.py
    backend/app/modules/<name>/router.py
    backend/app/modules/<name>/__init__.py

E imprime no ecrã:
    - a linha a acrescentar em backend/app/core/module_registry.py
    - o objeto a acrescentar no array MODULES em admin/src/config/modules.ts

Depois de gerar, reiniciar o backend (o create_all trata da tabela nova).
"""
import argparse
import os

MODEL_TEMPLATE = '''from sqlalchemy import Column, Integer, String, Text, Boolean

from app.core.database import Base


class {class_name}(Base):
    __tablename__ = "{table_name}"
    id = Column(Integer, primary_key=True, index=True)
{fields}
'''

SCHEMA_TEMPLATE = '''from typing import Optional

from pydantic import BaseModel


class {class_name}Base(BaseModel):
{fields}


class {class_name}Create({class_name}Base):
    pass


class {class_name}Update(BaseModel):
{optional_fields}


class {class_name}Out({class_name}Base):
    id: int

    class Config:
        from_attributes = True
'''

ROUTER_TEMPLATE = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.{name} import {class_name}
from app.schemas.{name} import {class_name}Create, {class_name}Update, {class_name}Out

router = APIRouter()


@router.get("/", response_model=list[{class_name}Out])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query({class_name}).all()


@router.post("/", response_model={class_name}Out)
def criar(payload: {class_name}Create, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = {class_name}(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@router.put("/{{item_id}}", response_model={class_name}Out)
def atualizar(item_id: int, payload: {class_name}Update, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = db.query({class_name}).filter({class_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item


@router.delete("/{{item_id}}")
def apagar(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    item = db.query({class_name}).filter({class_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    db.delete(item); db.commit()
    return {{"ok": True}}
'''

SQL_TYPES = {"text": "String(255)", "textarea": "Text", "boolean": "Boolean", "number": "Integer"}
PY_TYPES = {"text": "str", "textarea": "str", "boolean": "bool", "number": "int"}
ADMIN_TYPES = {"text": "text", "textarea": "textarea", "boolean": "boolean", "number": "number"}


def parse_fields(raw):
    fields = []
    for part in raw.split(","):
        bits = part.split(":")
        name = bits[0].strip()
        ftype = bits[1].strip() if len(bits) > 1 else "text"
        required = len(bits) > 2 and bits[2].strip().lower() == "true"
        fields.append((name, ftype, required))
    return fields


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", required=True, help="nome do módulo em minúsculas, singular, ex: evento")
    parser.add_argument("--label", required=True, help="rótulo a mostrar no Back Office, ex: Eventos")
    parser.add_argument("--fields", required=True, help="nome:tipo:obrigatorio separados por vírgula")
    args = parser.parse_args()

    name = args.name.lower()
    class_name = name[0].upper() + name[1:]
    fields = parse_fields(args.fields)

    model_fields = "\n".join(
        f'    {n} = Column({SQL_TYPES.get(t, "String(255)")}{"" if req else ", nullable=True"})'
        for n, t, req in fields
    )
    schema_fields = "\n".join(
        f'    {n}: {PY_TYPES.get(t, "str")}' if req
        else f'    {n}: Optional[{PY_TYPES.get(t, "str")}] = None'
        for n, t, req in fields
    )
    optional_fields = "\n".join(
        f'    {n}: Optional[{PY_TYPES.get(t, "str")}] = None' for n, t, req in fields
    )

    repo_root = os.path.join(os.path.dirname(__file__), "..")
    backend_app = os.path.join(repo_root, "backend", "app")
    module_dir = os.path.join(backend_app, "modules", name)
    os.makedirs(module_dir, exist_ok=True)

    with open(os.path.join(backend_app, "models", f"{name}.py"), "w", encoding="utf-8") as f:
        f.write(MODEL_TEMPLATE.format(class_name=class_name, table_name=name + "s", fields=model_fields))

    with open(os.path.join(backend_app, "schemas", f"{name}.py"), "w", encoding="utf-8") as f:
        f.write(SCHEMA_TEMPLATE.format(class_name=class_name, fields=schema_fields, optional_fields=optional_fields))

    with open(os.path.join(module_dir, "router.py"), "w", encoding="utf-8") as f:
        f.write(ROUTER_TEMPLATE.format(name=name, class_name=class_name))

    open(os.path.join(module_dir, "__init__.py"), "w").close()

    admin_fields = ",\n".join(
        f'      {{ name: \'{n}\', label: \'{n.capitalize()}\', type: \'{ADMIN_TYPES.get(t, "text")}\'' +
        (", required: true" if req else "") + " }"
        for n, t, req in fields
    )

    print(f"\nMódulo '{name}' gerado com sucesso em backend/app/modules/{name}/\n")
    print("1) Acrescentar em backend/app/core/module_registry.py:\n")
    print(f'   from app.modules.{name}.router import router as {name}_router')
    print(f'   ModuleDefinition("{name}", "{args.label}", "/api/{name}s", {name}_router),\n')
    print("2) Acrescentar em admin/src/config/modules.ts (dentro do array MODULES):\n")
    print(f"""  {{
    key: '{name}',
    label: '{args.label}',
    icon: FileText, // trocar pelo ícone lucide-react desejado
    apiPath: '/{name}s',
    fields: [
{admin_fields},
    ],
  }},""")
    print("\n3) Reiniciar o backend — a tabela é criada automaticamente no arranque.\n")


if __name__ == "__main__":
    main()
