import os
import shutil
from datetime import datetime
from flask import request
import git
from models import GitAnalysisResult, Session

def git_analysis():
    usuario = request.args.get('usuario')
    repositorio = request.args.get('repositorio')

    repo_url = f'https://github.com/{usuario}/{repositorio}.git'
    repo_dir = 'diretorio_local_repositorio'

    # Remove o repositório se já existir
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

    # Clona o repositório
    repo = git.Repo.clone_from(repo_url, repo_dir)

    # Inicializa dicionário para armazenar os commits por desenvolvedor
    commits_por_desenvolvedor = {}
    dias_por_desenvolvedor = {}

    # Itera pelo histórico de commits
    for commit in repo.iter_commits():
        autor = commit.author.name
        commits_por_desenvolvedor[autor] = commits_por_desenvolvedor.get(autor, 0) + 1

        data_commit = commit.committed_datetime.date()
        if autor not in dias_por_desenvolvedor:
            dias_por_desenvolvedor[autor] = {data_commit}
        else:
            dias_por_desenvolvedor[autor].add(data_commit)

    response = ''
    session = Session()

    # Retorna o total de commits e a média de commits por dia por desenvolvedor
    for autor, commits in commits_por_desenvolvedor.items():
        dias = len(dias_por_desenvolvedor[autor])
        media_commits_por_dia = commits / dias
        response += f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.<br>'

        result = GitAnalysisResult(
            author=autor,
            analyze_date=datetime.now(),
            average_commits=media_commits_por_dia,
            repository_url=repo_url,
            repository_name=repositorio
        )
        session.add(result)

    session.commit()
    session.close()

    return response


def buscar_medias_de_commit():
    autor1 = request.args.get('autor1')
    autor2 = request.args.get('autor2')
    autor3 = request.args.get('autor3')
    autores = [autor1, autor2, autor3]

    session = Session()
    resultados = []

    for autor in autores:
        registros = session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f"%{autor}%")).all()
        for registro in registros:
            resultados.append(f'{registro.author} possui uma média de {registro.average_commits:.2f} commits por dia.')

    session.close()
    resultados_nao_duplicados = set(resultados)
    return "<br>".join(resultados_nao_duplicados)
