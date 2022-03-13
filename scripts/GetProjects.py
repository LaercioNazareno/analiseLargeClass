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
    'Authorization': 'bearer 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',
}

query = """
    query {
        search(query:"stars:>100 language:java" , type:REPOSITORY, first:5) {
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
        cloneProject(numProject, nameProject, link)
        createRequiredFiles(nameProject)
        avaliarComPmd(nameProject, numProject)
        os.system("cls")

def createRequiredFiles(nameProject):
   createProjectFile(nameProject)
   createClasspathFile(nameProject)

def createClasspathFile(nameProject):
    file = open("../repositories/"+nameProject+".classpath", 'w')
    file.write("""<?xml version="1.0" encoding="UTF-8"?>
<classpath>
	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.7"/>
	<classpathentry kind="output" path="bin"/>
</classpath>""")
    file.close()

def createProjectFile(nameProject):
    file = open("../repositories/"+nameProject+".project", 'w')
    file.write("""<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>"""+nameProject+"""</name>
	<comment></comment>
	<projects>
	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.jdt.core.javabuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>org.eclipse.jdt.core.javanature</nature>
	</natures>
</projectDescription>""")
    file.close()

def cloneProject(numProject, nameProject, link):
    print("Clonando o projeto: "+ nameProject+" index: "+ str(numProject))
    command = "git clone "+link+" ../repositories/"+nameProject
    os.system(command)

def avaliarComPmd(nameProject, numProject):
    print("Avaliando o projeto "+nameProject+" index: "+ str(numProject))
    diretory = "../results/"+nameProject
    os.makedirs(diretory)
    command = "pmd -d " +"../repositories/"+nameProject +" -f text  -R category/java/design.xml/GodClass -language java > "+ "../results/"+nameProject+"/pmdResultGodClass.txt"
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

def openFileWriterAndWriteHeader(file):
    fieldnames = ["Nome","url","Data Criacao","Data de Atualizacao", "Qtd estrelas"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    return writer

data = getDataList()
saveData(data)
dataProcessing(data)

# Decore não ok
# PMD ok
# Jdeodorant ok
# Jspiriti ok
# Multiview
