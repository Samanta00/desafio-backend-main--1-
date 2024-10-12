# Desafio técnico




## Autora: Ellen Samanta

## Para rodar o projeto, entre na pasta desafio-backend-main e digite no terminal:  python3 api.py
## Para executar o arquivo docker, entre na pasta docker e digite : docker-compose -f docker-compose.yaml up -d

## ao executar a rota[GET] Pelo insominia/Postman, você pode escrever tanto maiusculo quanto minusculo no campo de nomes, exemplo
## ('http://127.0.0.1:5000/analisador-git/buscar?autor1=OCTOCAT&autor2=johnneylee&autor3=cameronmcefee')

## Você terá um retorno: 
### Johnneylee Jack Rollins possui uma média de 1.00 commits por dia.
### cameronmcefee possui uma média de 1.00 commits por dia.
### The Octocat possui uma média de 1.00 commits por dia.


## ao executar a rota[GET]('http://127.0.0.1:5000/analisador-git/buscar?autor1=octocat&autor2=Johnneylee&autor3=cameronmcefee')
## você terá um retorno: 

{
    "resultados": [
        "The Octocat realizou 1 commits com uma média de 1.00 commits por dia.",
        "Johnneylee Jack Rollins realizou 1 commits com uma média de 1.00 commits por dia.",
        "cameronmcefee realizou 1 commits com uma média de 1.00 commits por dia."
    ]
}
