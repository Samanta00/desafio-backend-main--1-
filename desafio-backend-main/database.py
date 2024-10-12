# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:ElS895623!@localhost:3307/git_analysis_results.db"

# Cria a conexão com o banco de dadps
engine = create_engine(DATABASE_URL, echo=True)

# Cria a base declarativa
Base = declarative_base()

# Configura as sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
