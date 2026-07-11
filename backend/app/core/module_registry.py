"""
Registo central de módulos do Back Office SEC4DATA.

Para acrescentar um novo módulo/funcionalidade ao Back Office:
  1. Criar o modelo em app/models/<nome>.py
  2. Criar os schemas em app/schemas/<nome>.py
  3. Criar o router em app/modules/<nome>/router.py
     (usar um módulo existente, ex. services, como referência)
  4. Importar o router abaixo e acrescentar uma linha a MODULES

Ou, mais simples: correr scripts/new_module.py, que gera os três
ficheiros acima automaticamente a partir de uma lista de campos.

Não é preciso tocar em mais nenhum ficheiro do backend — o main.py
regista todos os routers automaticamente a partir desta lista.
"""
from dataclasses import dataclass
from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.blog.router import router as blog_router
from app.modules.leads.router import router as leads_router
from app.modules.services.router import router as services_router
from app.modules.products.router import router as products_router
from app.modules.team.router import router as team_router
from app.modules.testimonials.router import router as testimonials_router
from app.modules.settings.router import router as settings_router
from app.modules.public.router import router as public_router


@dataclass
class ModuleDefinition:
    key: str
    label: str
    prefix: str
    router: APIRouter


MODULES: list[ModuleDefinition] = [
    ModuleDefinition("auth", "Autenticação", "/api/auth", auth_router),
    ModuleDefinition("users", "Utilizadores", "/api/users", users_router),
    ModuleDefinition("blog", "Blog", "/api/blog", blog_router),
    ModuleDefinition("leads", "Contactos/Leads", "/api/leads", leads_router),
    ModuleDefinition("services", "Serviços", "/api/services", services_router),
    ModuleDefinition("products", "Produtos", "/api/products", products_router),
    ModuleDefinition("team", "Equipa", "/api/team", team_router),
    ModuleDefinition("testimonials", "Testemunhos", "/api/testimonials", testimonials_router),
    ModuleDefinition("settings", "Definições", "/api/settings", settings_router),
    ModuleDefinition("public", "Público (site)", "/api/public", public_router),
]
