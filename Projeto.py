from BIBLIOTECA import funcoes as fc

from sklearn.ensemble import GradientBoostingClassifier

csv = 'Data/Dados.csv'

csv_predicao = 'Data/Predicao.csv'

fc.leitura_csv(csv)

fc.treinando_modelo(GradientBoostingClassifier(
    n_estimators=60, learning_rate=1.0, max_depth=13, random_state=0))
