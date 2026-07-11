from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.module_registry import MODULES

# Garante que todos os modelos são conhecidos do SQLAlchemy antes do create_all
from app.models import user, blog, lead, service, product, team, testimonial, setting  # noqa: F401,E501

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in MODULES:
    app.include_router(module.router, prefix=module.prefix, tags=[module.label])


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "modulos_ativos": [m.key for m in MODULES]}
