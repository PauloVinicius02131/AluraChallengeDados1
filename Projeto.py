from BIBLIOTECA import funcoes as fc

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

select = 'select * from analise_risco.dados_modelo_ml'

csv = 'Data/Dados.csv'

csv_predicao = 'Data/Predicao.csv'

fc.leitura_csv(csv)

fc.modelando_dados()

fc.info_dados()

# (LogisticRegression(max_iter=20300))
# (RandomForestClassifier(n_estimators=50, max_depth=10, random_state=0))
# (AdaBoostClassifier(random_state=0))
# (DecisionTreeClassifier())
# (GradientBoostingClassifier(n_estimators = 50, learning_rate = 1.0, max_depth = 5, random_state = 0))

fc.treinando_modelo(GradientBoostingClassifier(n_estimators = 60, learning_rate = 1.0, max_depth = 13, random_state = 0))