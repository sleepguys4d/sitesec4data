# SEC4DATA — Site institucional + Back Office

Plataforma completa: site público, API e Back Office de gestão de conteúdo,
desenhada para que **novas funcionalidades e opções possam ser acrescentadas
sem reescrever nada do que já existe**.

## Estrutura do projeto

```
sec4data-platform/
├── site/               Site institucional — 1 ficheiro HTML autocontido
├── backend/            API (FastAPI + SQLAlchemy + JWT + RBAC)
├── admin/               Back Office (React + TypeScript + Vite + Tailwind)
├── nginx/               Configuração de produção (serve site + admin + proxy da API)
├── scripts/
│   └── new_module.py    Gerador de novos módulos do Back Office
└── docker-compose.yml
```

## Arrancar em produção (Docker)

```bash
cp .env.example .env      # ajustar SECRET_KEY
docker compose up --build
```

- Site institucional: `http://localhost/`
- Back Office: `http://localhost/admin/`
- API: `http://localhost/api/`

**Login inicial do Back Office:**
```
email:    admin@sec4data.co.ao
password: MudarEstaPassword!1
```
⚠️ Mudar esta password imediatamente após o primeiro acesso (Back Office → Utilizadores).

## Arrancar em desenvolvimento (sem Docker)

Backend:
```bash
cd backend
pip install -r requirements.txt --break-system-packages
python3 -m app.seed          # cria o utilizador admin e o conteúdo inicial
uvicorn app.main:app --reload
```
Por omissão usa SQLite (`sec4data.db`). Para Postgres, definir `DATABASE_URL` num `.env` dentro de `backend/`.

Back Office:
```bash
cd admin
npm install
npm run dev
```
O Vite já faz proxy de `/api` para `http://localhost:8000` em desenvolvimento.

Site: o ficheiro `site/index.html` pode ser aberto diretamente no browser — funciona
com conteúdo de exemplo mesmo sem o backend ligado, e passa a mostrar dados reais
assim que a API estiver disponível na mesma origem.

## Como o Back Office é "completo e adaptável"

O pedido original era um Back Office **completo** e **adaptável a novas
funcionalidades**. Isso foi resolvido com três mecanismos concretos:

### 1. Registo central de módulos (backend)
`backend/app/core/module_registry.py` é a única lista que o `main.py` lê para
saber que rotas existem. Cada módulo é um trio modelo + schema + router.

### 2. Configuração central de módulos (Back Office)
`admin/src/config/modules.ts` é a única coisa que a interface lê para saber que
módulos mostrar, que colunas tem a tabela, e que campos tem o formulário. Não há
nenhum ecrã escrito à mão por módulo — `ModulePage.tsx` é 100% genérico.

### 3. Gerador automático de módulos
```bash
python3 scripts/new_module.py \
  --name evento \
  --label "Eventos" \
  --fields "titulo:text:true,descricao:textarea,data:text,ativo:boolean"
```
Isto gera automaticamente o modelo, o schema e o router no backend, e imprime
no ecrã as duas linhas exatas a colar em `module_registry.py` e `modules.ts`.
Depois de colar essas linhas e reiniciar o backend, o módulo novo já aparece
no menu do Back Office, com tabela, formulário, permissões e contagem no
Painel — tudo automaticamente. **Este fluxo foi testado e confirmado a funcionar.**

## Módulos incluídos

| Módulo | Descrição |
|---|---|
| Blog | Artigos com estado rascunho/publicado, consumidos pelo site |
| Contactos / Leads | Submissões do formulário de contacto do site |
| Serviços | Os 8 serviços apresentados no site |
| Produtos | HIDEN, Sniffing, SOC Xpert, Fraud Hunter |
| Equipa | Membros da equipa (nome, cargo, foto, bio) |
| Testemunhos | Testemunhos de clientes (só aparecem no site quando existirem) |
| Utilizadores | Gestão de acessos ao Back Office (admin only) |
| Definições | Textos do hero, contacto, redes sociais — chave/valor |

## Papéis (RBAC)

- **admin** — acesso total, incluindo gestão de utilizadores e eliminação de registos
- **editor** — pode criar/editar conteúdo, não pode apagar nem gerir utilizadores
- **viewer** — apenas leitura

## Notas de segurança para produção

- Mudar `SECRET_KEY` no `.env` antes de expor publicamente.
- Mudar a password do utilizador admin inicial.
- `CORS_ORIGINS` está aberto a `http://localhost` por omissão — ajustar para o domínio real.
- O JWT do Back Office é guardado em `localStorage`; para maior robustez em
  produção de alta exigência, considerar migrar para cookies `httpOnly`.
