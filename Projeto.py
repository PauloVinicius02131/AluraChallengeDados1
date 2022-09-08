from BIBLIOTECA import funcoes as fc 

from sklearn.linear_model import LogisticRegression

select = 'select * from analise_risco.dados_modelo_ml'

csv = 'teste.csv'

# fc.leitura_banco(select)

fc.leitura_csv(csv)

fc.modelando_dados()

fc.info_dados()

fc.treinando_modelo(LogisticRegression(max_iter=23683))

