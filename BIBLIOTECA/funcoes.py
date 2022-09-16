import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy as sql
import pickle 
from sqlalchemy import create_engine

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

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder

SEED = 80
np.random.seed(SEED)


def criar_faixas(df_predicao):
    global df_faixas
    faixa_etaria = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    faixa_etaria_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    df_predicao['faixa_idade'] = pd.cut(
        x=df_predicao['pessoa_idade'], bins=faixa_etaria, labels=faixa_etaria_labels)

    faixa_salario = [4000, 28872, 35004, 42016, 49000,
                     55004, 63096, 73004, 85757, 110004, 150004]
    faixa_salario_labes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    df_predicao['Faixa_Salarial'] = pd.cut(
        x=df_predicao['salario_ano'], bins=faixa_salario, labels=faixa_salario_labes)

    faixa_emprestimo = [1475, 2450, 3450, 4425, 5425, 6400, 7400, 8375, 9350, 10325, 11325, 12325, 13300, 14300, 15275, 16250, 17250,
                        18225, 19200, 20200, 21200, 22100, 23100, 24150, 25000, 26000, 27050, 28000, 29000, 30000, 31050, 32000, 33000, 34000, 35000]

    faixa_emprestimo_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                               16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]

    df_predicao['Faixa_Emprestimo'] = pd.cut(
        x=df_predicao['vl_total'], bins=faixa_emprestimo, labels=faixa_emprestimo_labels)

    df_faixas = df_predicao.copy()

    return df_predicao, df_faixas
