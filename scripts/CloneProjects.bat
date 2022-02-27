@echo off
set URL_PROJECT=%1
set NAME_PROJECT=%2
set INDEX_PROJECT=%3

set RESULT=../results
set REPOSITORY=../repositories/%NAME_PROJECT%

set LOG_FILE=%RESULT%/%NAME_PROJECT%/logProject%NAME_PROJECT%

mkdir %RESULT%/%NAME_PROJECT%/

echo 'ANALISE E CLONAGEM DO PROJETO '%NAME_PROJECT% ' INDEX ' %INDEX_PROJECT%
git clone %URL_PROJECT% ../repositories/%NAME_PROJECT%

call java17
echo 'verificando o build maven do ' %NAME_PROJECT%
call mvn -f %REPOSITORY% verify > %LOG_FILE%

echo 'coletando as metricas ' %NAME_PROJECT%
call java -jar -Xms1g -Xmx20g ../tools/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar %REPOSITORY% false 0 False %RESULT%/%NAME_PROJECT%/


echo 'coletando o code-smell ' %NAME_PROJECT%
cd ../tools
call java -jar -Xms1g -Xmx20g ../tools/codesmells/Designite/DesigniteJava.jar -i %REPOSITORY% -o %RESULT%/%NAME_PROJECT%
cls
call java8
call java -jar -Xms1g -Xmx20g  C:/Users/Administrator/Downloads/tcc/TCC_Laercio/organic/eclipse/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar org.eclipse.core.launcher.Main -application organic.Organic -sf %RESULT%/%NAME_PROJECT%/organicResult.json -src %REPOSITORY%

call pmd -d %REPOSITORY% -f text  -R category/java/design.xml/GodClass -language java > %RESULT%/%NAME_PROJECT%/pmdResultGodClass.txt

