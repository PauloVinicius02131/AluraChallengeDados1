import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import Pipeline

from sklearn.model_selection import GroupKFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split


from sklearn.preprocessing import StandardScaler

from imblearn.over_sampling import SMOTE

from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import recall_score

SEED = 80
np.random.seed(SEED)


def leitura_csv(csv):
    global base_dados
    base_dados = pd.read_csv(csv).drop(
        columns=['pessoa_id', 'pessoa_idade', 'salario_ano', 'vl_total'])
    return base_dados

def treinando_modelo(classificador):
    y = base_dados['inadimplencia']
    x = base_dados.drop(columns=['inadimplencia'])

    print('A Basse possui: %s elementos.' % (x.shape[0].__format__(',d')))
    print('-'*100)

    #Normalizando os Dados.
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    # Balanceamento da Base de Dados.
    resampler = SMOTE(random_state=SEED)
    resampler_name = resampler.__getattribute__('__class__').__name__
    x_resampled, y_resampled = resampler.fit_resample(x, y)

    print('A Basse foi balanceada com: %s' % (resampler_name))
    print('*'*36)

    # Separação Treino e Teste.
    treino_x, teste_x, treino_y, teste_y = train_test_split(
        x_resampled, y_resampled, test_size=0.30, random_state=0)
    base_treino = treino_x.shape[0]
    base_teste = teste_x.shape[0]

    print('Separada com: %s elementos de treino e %s elementos para teste.' % (
        base_treino.__format__(',d'), base_teste.__format__(',d')))
    print('-'*100)


    scaler = StandardScaler()
    modelo = GradientBoostingClassifier(loss='log_loss', max_depth=8, max_features='sqrt',
                                        random_state=80, subsample=0.5)

    pipeline = Pipeline([('scaler', scaler), ('estimador', modelo)])

    print('Definição do Pipeline')
    print('-'*100)
    print(pipeline.named_steps['scaler'])
    print('*'*16)
    print(pipeline.named_steps['estimador'])
    print('-'*100)

    pipeline.fit(treino_x, treino_y)

    predicao = pipeline.predict(teste_x)

    print('Classification Report')
    print('.'*53)
    print(classification_report(teste_y, predicao))
    print('.'*53)


    matriz_confusao = ConfusionMatrixDisplay.from_estimator(
        pipeline, teste_x, teste_y, cmap='Blues')
    plt.title('Matriz de Confusao')

    prob_previsao = pipeline.predict_proba(teste_x)[:, 1]


    tfp, tvp, limite = roc_curve(teste_y, prob_previsao)

    plt.figure(figsize=(6, 6))
    plt.plot(tfp, tvp)
    plt.plot([0, 1], ls="--", c='red')
    plt.plot([0, 0], [1, 0], ls="--",
            c='green'), plt.plot([1, 1], ls="--", c='green')
    plt.ylabel('Sensibilidade')
    plt.xlabel('Especificidade')
    plt.show()
    print('roc_auc:', roc_auc_score(teste_y, prob_previsao))

    return modelo, matriz_confusao
