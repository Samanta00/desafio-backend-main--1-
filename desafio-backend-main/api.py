from flask import Flask
from controllers.controller import git_analysis, buscar_medias_de_commit

app = Flask(__name__)

@app.route('/analisador-git', methods=['GET'])
def analisar_git():
    return git_analysis()

@app.route('/analisador-git/buscar', methods=['GET'])
def buscar_commits():
    return buscar_medias_de_commit()

if __name__ == '__main__':
    app.run(debug=True)
