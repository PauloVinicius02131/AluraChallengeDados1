from BIBLIOTECA import funcoes as fc

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier


select = 'select * from analise_risco.dados_modelo_ml'

csv = 'Data/Dados.csv'

csv_predicao = 'Data/Predicao.csv'

fc.leitura_csv(csv)

# fc.leitura_csv_predicao(csv_predicao)

fc.modelando_dados()

fc.info_dados()

# LogisticRegression(max_iter=20300) output_08_09_20_04_55
# RandomForestClassifier(n_estimators=50, max_depth=10, random_state=0) output_08_09_20_13_35
# AdaBoostClassifier(random_state=0)


fc.treinando_modelo(RandomForestClassifier(
    n_estimators=50, max_depth=10, random_state=0))

