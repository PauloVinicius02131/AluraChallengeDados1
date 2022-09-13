import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import seaborn as sns
import sqlalchemy as sql

from sqlalchemy import create_engine

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler

from datetime import date, datetime
from datetime import timedelta
import time

import os
import sys

from collections import Counter
from sklearn.datasets import make_classification

from imblearn.under_sampling import ClusterCentroids, RandomUnderSampler, NearMiss

# Obtendo dados.
# Analise_RISCO
string_connection = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
                    user='root',
                    password='125478',
                    server='127.0.0.1',
                    database='analise_risco')

cnx = sql.create_engine(string_connection)


def leitura_banco(select):
    global dados
    dados = pd.read_sql(select, cnx)
    return dados


def leitura_csv(csv):
    global dados
    dados = pd.read_csv(csv)
    return dados


def leitura_csv_predicao(csv_predicao):
    global base_predicao
    # base_predicao = pd.read_csv(csv_predicao)
    # base_predicao = base_predicao.drop(
    #     columns=['pessoa_id', 'pessoa_idade', 'salario_ano', 'vl_total','inadimplencia'])
    return base_predicao


def modelando_dados():
    global base_dados
    base_dados = dados.drop(
        columns=['pessoa_id', 'pessoa_idade', 'salario_ano', 'vl_total'])
    return base_dados


def info_dados():
    linhas = base_dados.shape[0]
    colunas = base_dados.shape[1]
    print('\nO numero de linhas é %s linhas e %s colunas\n' % (linhas, colunas))
    print('Cabeçalho dos Dados:')
    print(base_dados.info())
    print('-'*100)
    print('\n Descrição dos dados:')
    print(base_dados.describe())
    print('-'*100)
    nulos = base_dados.isnull().sum()
    print('Dados nulos:')
    print(base_dados)
    print('-'*100)


def treinando_modelo(classificador):

    # Separando a Base  e variavel resposta.

    y = base_dados['inadimplencia']
    x = base_dados.drop(columns=['inadimplencia'])
    # --------------------------------------------------------------------

    # Balanceamento das Variaveis alvo.

    # cc = ClusterCentroids(random_state=0)
    # rus = RandomUnderSampler(random_state=0)

    nm = NearMiss(version=1, n_neighbors_ver3=3)
    x_resampled, y_resampled = nm.fit_resample(x, y)

    print(sorted(Counter(y_resampled).items()))
    # --------------------------------------------------------------------

    # Separando a base de treino e teste.

    SEED = 80
    # Treino Teste Split
    raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(
        x_resampled, y_resampled, test_size=0.30, random_state=SEED)
    # --------------------------------------------------------------------

    # Normalizando os dados.

    scaler = StandardScaler()
    scaler.fit(raw_treino_x)
    treino_x = scaler.transform(raw_treino_x)
    teste_x = scaler.transform(raw_teste_x)
    # --------------------------------------------------------------------

    # Plotagem Treino e Teste.

    base_treino = treino_x.shape[0]
    base_teste = teste_x.shape[0]
    print('A base de treino tem %s elementos e a base de teste tem %s elementos.' % (
        base_treino, base_teste))
    print(100*'-')
    # --------------------------------------------------------------------

    # Fit do Modelo.

    modelo = classificador
    modelo.fit(treino_x, treino_y)

    # --------------------------------------------------------------------

    # Matriz de Confusão.

    matriz_confusao = ConfusionMatrixDisplay.from_estimator(
        modelo, teste_x, teste_y, cmap='Blues')
    plt.title('Matriz de Confusao')
    matriz = matriz_confusao.figure_
    # plt.show
    # --------------------------------------------------------------------

    # Classification Report.

    previsoes = modelo.predict(teste_x)

    print('\nClassification Report:')
    print(classification_report(teste_y, previsoes))
    print(100*'-')
    # --------------------------------------------------------------------

    # Curva ROC e AUC.

    prob_previsao = modelo.predict_proba(teste_x)[:, 1]

    tfp, tvp, limite = roc_curve(teste_y, prob_previsao)
    print('roc_auc:', roc_auc_score(teste_y, prob_previsao))

    fig1 = plt.figure()
    plt.plot(tfp, tvp)
    plt.plot([0, 1], ls="--", c='red')
    plt.plot([0, 0], [1, 0], ls="--",
             c='green'), plt.plot([1, 1], ls="--", c='green')
    plt.ylabel('Sensibilidade')
    plt.xlabel('Especificidade')
    plt.show()

    pdf = matplotlib.backends.backend_pdf

    pdf = pdf.PdfFile(
        "output_" + datetime.now().strftime("%d_%m_%H_%M_%S") + ".pdf")

    report = classification_report(teste_y, previsoes, output_dict=True)
    report_map = sns.heatmap(pd.DataFrame(report).iloc[:-1, :].T, annot=True)
    report_fig = report_map.figure

    pdf.savefig(report_fig)
    pdf.savefig(matriz)
    pdf.savefig(fig1)
    pdf.close()
    # --------------------------------------------------------------------
    # previsao = modelo.predict(base_predicao)

    return modelo, matriz_confusao
