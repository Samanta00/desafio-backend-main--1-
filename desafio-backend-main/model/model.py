from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GitAnalysisResult(Base):
    __tablename__ = 'git_analysis_results'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    analyze_date = Column(DateTime)
    average_commits = Column(Float)
    repository_url = Column(String)
    repository_name = Column(String)

# Configuração do banco de dados
engine = create_engine('sqlite:///git_analysis_results.db')
Session = sessionmaker(bind=engine)

# Cria todas as tabelas caso não exista
Base.metadata.create_all(engine)
