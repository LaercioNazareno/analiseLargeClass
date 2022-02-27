import os
import sys
import requests
import csv
from json import dump
from json import loads
from unicodedata import name

## Variaveis globais 
apiUrlBase = 'https://api.github.com/graphql'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer f4fb4aa95200cc25e360cd9d1a195a36460e1a67',
}
## Verificar a ordem das estrelas
query = """
    query {
        search(query:"stars:>100 language:java" , type:REPOSITORY, first:100) {
            edges {
                node{
                    ... on Repository {
                      nameWithOwner
                      url
                      createdAt
                      updatedAt
                      name
                       stargazers {
                          totalCount
                        }
                    }
                }
            }
        }
    }
"""
json = {
    "query": query, "variables": {}
}
def getDataList():
    response = requests.post(apiUrlBase, headers=headers, json=json)
    data = response.json()['data']['search']['edges']
    return data

def dataProcessing(data): 
    link = ''
    nameProject = ''
    numProject = 0
    for node in data:
        numProject = numProject + 1
        repository = node['node']
        nameProject = repository['name']
        link = repository['url']
        command = "CloneProjects.bat "+ link + " " + nameProject +" "+ str(numProject)
        os.system(command)

def saveData(data):
    file = open("../results/evaluatedProjects.csv", 'w')
    writer = openFileWriterAndWriteHeader(file)
    numProject = 1
    for node in data:
        repository = node['node']
        nameProject = repository['name']
        link = repository['url']
        createdAt = repository['createdAt']
        updatedAt = repository['updatedAt']
        qtdEstrelas = repository['stargazers']['totalCount']
        writer.writerow({"Nome": nameProject,
                         "url":link,
                         "Data Criacao": createdAt,
                         "Data de Atualizacao": updatedAt,
                         "Qtd estrelas": qtdEstrelas
                        })
#adicionar o numero de estrelas 
def openFileWriterAndWriteHeader(file):
    fieldnames = ["Nome","url","Data Criacao","Data de Atualizacao", "Qtd estrelas"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    return writer

data = getDataList()
saveData(data)
dataProcessing(data)

# Decore 96 * 5
# PMD ok
# Jdeodorant
# Jspiriti não ok
# Multiview
