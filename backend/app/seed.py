"""Popula a base de dados com o utilizador administrador e o conteúdo real do site."""
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.service import Service
from app.models.product import Product
from app.models.setting import Setting
from app.models import blog, lead, team, testimonial  # noqa: F401

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@sec4data.co.ao").first():
            db.add(User(
                nome="Administrador",
                email="admin@sec4data.co.ao",
                password_hash=hash_password("MudarEstaPassword!1"),
                role=UserRole.admin,
            ))

        if db.query(Service).count() == 0:
            servicos = [
                ("SOC Gerido", "Monitorização contínua 24/7 com deteção e resposta orquestradas.", "radar"),
                ("MDR", "Deteção e resposta geridas sobre todo o parque tecnológico do cliente.", "shield"),
                ("Threat Intelligence", "Inteligência de ameaças acionável, adaptada ao contexto angolano.", "eye"),
                ("Penetration Testing", "Testes de intrusão ofensivos alinhados com OWASP e PTES.", "terminal"),
                ("Resposta a Incidentes", "Contenção, erradicação e recuperação após incidentes de segurança.", "alert"),
                ("Forense Digital", "Investigação forense de sistemas comprometidos e recolha de prova.", "search"),
                ("Compliance", "Conformidade com a Lei n.º 22/11 e normas internacionais de segurança.", "check"),
                ("Formação e Academia", "Capacitação técnica através da Academia SEC4DATA.", "book"),
            ]
            for i, (titulo, descricao, icone) in enumerate(servicos):
                db.add(Service(titulo=titulo, descricao=descricao, icone=icone, ordem=i))

        if db.query(Product).count() == 0:
            produtos = [
                ("HIDEN", "Plataforma de Cyber Threat Intelligence", "Inteligência de ameaças centralizada, com múltiplas fontes e RBAC.", ["Feeds de CTI", "Correlação de IOCs", "RBAC"], "database"),
                ("Sniffing", "SIEM / XDR", "Deteção e resposta alargada com correlação de eventos em tempo real.", ["SIEM", "XDR", "Correlação em tempo real"], "activity"),
                ("SOC Xpert", "Gestão de Casos", "Plataforma de gestão de casos e playbooks para operações de SOC.", ["Gestão de casos", "Playbooks", "SDK de conectores"], "layers"),
                ("Fraud Hunter", "Plataforma Antifraude", "Deteção de fraude orientada a padrões comportamentais.", ["Deteção comportamental", "Alertas em tempo real", "Relatórios"], "shield-check"),
            ]
            for i, (nome, tagline, descricao, features, icone) in enumerate(produtos):
                db.add(Product(nome=nome, tagline=tagline, descricao=descricao, features=features, icone=icone, ordem=i))

        if db.query(Setting).count() == 0:
            definicoes = [
                ("hero_titulo", "Segurança que antecipa a ameaça", "geral", "Título principal do site"),
                ("hero_subtitulo", "SOC, MDR e Threat Intelligence para organizações angolanas e africanas.", "geral", "Subtítulo do hero"),
                ("contacto_email", "geral@sec4data.co.ao", "contacto", "Email de contacto público"),
                ("contacto_telefone", "+244 900 000 000", "contacto", "Telefone de contacto público"),
                ("contacto_morada", "Luanda, Angola", "contacto", "Morada apresentada no site"),
                ("linkedin_url", "", "redes_sociais", "URL do LinkedIn"),
            ]
            for chave, valor, grupo, descricao in definicoes:
                db.add(Setting(chave=chave, valor=valor, grupo=grupo, descricao=descricao))

        db.commit()
        print("Seed concluído.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
