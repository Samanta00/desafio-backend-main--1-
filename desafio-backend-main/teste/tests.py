import git
import pytest
from flask import Flask, jsonify
import api  # Certifique-se de que o módulo 'api' esteja no mesmo diretório ou no PYTHONPATH
from unittest.mock import patch

@pytest.fixture
def flask_app():
    app = Flask(__name__)
    return app

def test_git_analysis(flask_app):
    # Simulando a análise de um repositório válido
    with flask_app.test_request_context(
        '/?usuario=gitpython-developers&repositorio=gitdb'
    ):
        result = api.git_analysis()
        # A resposta de result é um objeto Response, precisamos pegar o JSON
        json_data = result.get_json()
        assert 'Sebastian Thiel realizou 268 commits com uma média de 2.95 commits por dia.' in json_data['resultados']

    # Testando a busca das médias de commit
    with flask_app.test_request_context(
            '/?autor1=Sebastian'
    ):
        result = api.buscar_medias_de_commit()
        # A resposta de result é um HTML, precisamos verificar se contém o esperado
        assert 'Sebastian Thiel possui uma média de 2.95 commits por dia.' in result

def test_git_analysis_no_repo(flask_app):
    # Usando patch para simular o comportamento do git.Repo.clone_from
    with patch('git.Repo.clone_from') as mock_clone:
        mock_clone.side_effect = git.exc.GitCommandError('Clone failed', 128)
        
        with flask_app.test_request_context(
            '/?usuario=nonexistent-user&repositorio=nonexistent-repo'
        ):
            with pytest.raises(git.exc.GitCommandError):
                # Certifique-se de que a função que chama clone_from é a que está sendo testada
                api.git_analysis()

