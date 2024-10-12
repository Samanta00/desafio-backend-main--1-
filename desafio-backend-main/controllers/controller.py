from flask import request, jsonify
import os
import shutil
from datetime import datetime
import git
from database import get_db
from model.model import GitAnalysisResult

def git_analysis():
    session = None  
    repo_dir = 'diretorio_local_repositorio'  
    try:
        usuario = request.args.get('usuario')
        repositorio = request.args.get('repositorio')

        # Verifica se os parâmetros obrigatórios foram fornecidos
        if not usuario or not repositorio:
            return jsonify({"error": "Parâmetros 'usuario' e 'repositorio' são obrigatórios."}), 400

        repo_url = f'https://github.com/{usuario}/{repositorio}.git'

        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = git.Repo.clone_from(repo_url, repo_dir)

        commits_por_desenvolvedor = {}
        dias_por_desenvolvedor = {}

        for commit in repo.iter_commits():
            autor = commit.author.name
            commits_por_desenvolvedor[autor] = commits_por_desenvolvedor.get(autor, 0) + 1

            data_commit = commit.committed_datetime.date()
            dias_por_desenvolvedor.setdefault(autor, set()).add(data_commit)

        session = next(get_db())

        resultados = []
        for autor, commits in commits_por_desenvolvedor.items():
            dias = len(dias_por_desenvolvedor[autor])
            media_commits_por_dia = commits / dias if dias > 0 else 0
            resultados.append(f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.')

            result = GitAnalysisResult(
                author=autor,
                analyze_date=datetime.now(),
                average_commits=media_commits_por_dia,
                repository_url=repo_url,
                repository_name=repositorio
            )
            session.add(result)

        session.commit()
        
        if not resultados:
            return jsonify({"error": "Nenhum commit encontrado para o repositório."}), 404

    except git.exc.GitCommandError:
        return jsonify({"error": "Não foi possível acessar o repositório. Verifique o usuário e o repositório informados."}), 400
    except Exception as e:
        return jsonify({"error": "Ocorreu um erro inesperado."}), 500
    finally:
        if session:  
            session.close()
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir) 

    return jsonify({"resultados": resultados})



def buscar_medias_de_commit():
    autor1 = request.args.get('autor1')
    autor2 = request.args.get('autor2')
    autor3 = request.args.get('autor3')
    autores = [autor1, autor2, autor3]

    session = next(get_db())

    resultados = []
    for autor in autores:
        registros = session.query(GitAnalysisResult).filter(GitAnalysisResult.author.ilike(f"%{autor}%")).all()
        
        if not registros: 
            resultados.append(f'nenhum registro encontrado para {autor}.'.lower())
        else:
            for registro in registros:
                resultados.append(f'{registro.author.lower()} possui uma média de {registro.average_commits:.2f} commits por dia.'.lower())

    session.close() 
    resultados_nao_duplicados = set(resultados)  
    return "<br>".join(resultados_nao_duplicados)

