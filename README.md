# AluraChallengeDados1 - Alura Cash 
  Neste projeto a Alura nos desafia a encontrar a probabilidade de inadimplência quando um determinado cliente solicitar um empréstimo. Para isso, utilizamos o dataset da Alura Cash que ja vem com algumas variáveis pré-processadas e com a variável alvo "inadimplente" que indica se o cliente pagou ou não o empréstimo.

  
  São 3 etapas propostas separadas por semanas com graus de dificuldade crescentes em que cada uma respectivamente corresponde aos seguintes objetivos: 
    
    1- Restaurar BD Alura Cash.
    
    2- Construção  e validação do Modelo de Aprendizado de Maquina.
    
    3- Hospedar Modelo em API. Criar requisição para API e apresentar resultado na ferramenta PowerBI.


# Etapa 1
  Nesta etapa, foi necessário realizar a importação do arquivo DUMP para o banco de dados MySQL.
    
  Após a importação, foi necessário realizar o tratamento dos dados, realizando tradução no nome das colunas e variaveis assim como modelar uma tabela única para ser lida pelo modelo.

   Na pasta DATA/DUMP_BD_MySQL, encontra-se o arquivo DUMP do banco de dados e  também o script BD.sql que foi utilizado para os tratamentos dos dados.
   
      * Alteração do tipo de dados nas colunas para melhor desempenho.
      * Tradução de nome de colunas
      * Tradução de linhas
      * Inclusão de chaves primarias e estrangeiras.
      * Criação de tabela única para leitura do modelo.
      
# Etapa 2

  Nesta etapa, foi necessário realizar a construção do modelo de aprendizado de maquina, o modelo escolhido foi o GradientBoostingClassifier, que é um modelo de aprendizado de maquina supervisionado que utiliza o algoritmo de boosting para melhorar a performance do modelo.
  
  Para isso, foi necessário realizar a leitura do banco de dados, realizar a limpeza dos dados, realizar a transformação dos dados e por fim, realizar a construção do modelo.
  
  No arquivo Projeto_V1.ipynb, encontra-se o código utilizado para a construção do modelo assim como o tratamento do dado.

  No processo de validação do modelo consta descrito no arquivo ValidarModelos.ipynb, foram testados outros 3 modelos com métodos de Over e Under Sampling e a utilização de GridSearchCV para encontrar os melhores parâmetros para o modelo escolhido.

  Ao final de cada processo foi utilizada a biblioteca Pickle para exportar o modelo serializado para o arquivo modelo.pkl que será utilizado na API. ( Assim como os transformadores de dados.)

# Etapa 3
      
      Em construção.

  
#alurachallengedados1