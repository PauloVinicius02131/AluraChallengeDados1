# AluraChallengeDados1 - Alura Cash 
  Neste projeto a Alura nos desafiará a encontrar um indicador de Taxa de Probabilidade de Inadimplencia utilizando de regressão logistica em um bd disponibilizado.
  
  São 3 etapas propostas separadas por semana em que cada uma respectivamente corresponde aos seguintes objetivos: 
    
    1- Obtenção do BD via arquivo DUMP, incluindo estes dados em um banco e realizar tratamentos basicos via sql. 
    
    2- Construção do Modelo de Aprendizado de Maquina. (Regressão logistica com sklearn) 
    
    3- Exibição de resultados via PowerBI.


# Etapa 1
   Este repositório ja se encontra com as interações realizadas no banco, o arquivo que realiza este tratamento esta no diretório raiz nomeado como ETL_BANCO.sql

   Ali você pode encontrar nos comentários basicamente 4 processos:
   
      * Alteração do tipo de dados nas colunas para melhor desempenho.
      * Tradução de nome de colunas
      * Tradução de linhas
      * Inclusão de chaves primarias e estrangeiras.
      
# Etapa 2

   No arquivo Notebook.ipynb estão os tratamentos dos dados nulos e das variaveis sejam categoricas ou numericas, nos markdowns existem comentários sobre tais analises.
   
   Já o arquivo projeto.py é possivel encontrar as funções que capturam o dataset tratado pelo notebook e executa o modelo gerando uma saida pdf na pasta raiz com as métricas de classificação.
   
   Atualmente o projeto se encontra na adptação dos modelos para as avaliações necessárias conforme escopo, seja aumentar clientela ou reduzir risco de inadimplencia.
      
# Observações Gerais sobre o repositório.

  O repositório ja esta com o venv e suas dependencias - faltante arquivo requirements *apenas no final do projeto.
  
  Notebook Jupyter esta para realizar testes e analises nos dados.
  
  
#alurachallengedados1
