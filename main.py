#Arquivo que sobe o serviço de API e Funcoes de Dados.

# uvicorn FastApi:app --reload
# uvicorn main:app --reload --host 0.0.0.0

import pandas as pd
import numpy as np
import pickle as pk

from fastapi import FastAPI


from BIBLIOTECA.funcoes import criar_faixa_idade, criar_faixa_valor

#-----------------#

app = FastAPI()

with open('MODELO/one_hot_enc.pkl', 'rb') as f:
    one_hot_enc = pk.load(f)
    
with open('MODELO/scaler.pkl', 'rb') as f:
    scaler = pk.load(f)
    
with open('MODELO/modelo.pkl', 'rb') as f:
    modelo = pk.load(f)

@app.get("/")
def hello_root():
    return {"Root": "Você está na raiz da API"}


#127.0.0.1:8000/requisicao/idade=30&salario=5000&propriedade=Alugada&ano_trabalhado=5&motivo_emprestimo=Melhoria do Lar&pontuacao=G&vl_total=10000&juros=8.8&hst_inadimplencia=0&hst_primeiro_credito=2
@app.get('/requisicao/idade={var_pessoa_idade}&salario={var_salario_ano}&propriedade={var_propriedade_sit}&ano_trabalhado={var_ano_trabalhado}&motivo_emprestimo={var_motivo_emprestimo}&pontuacao={var_pontuacao_emprestimos}&vl_total={var_vl_total}&juros={var_tx_juros}&hst_inadimplencia={var_hst_inadimplencia}&hst_primeiro_credito={var_hst_primeiro_credito}')
def montar_requisicao(var_pessoa_idade: int,
                      var_salario_ano: int,
                      var_propriedade_sit: str,
                      var_ano_trabalhado: int,
                      var_motivo_emprestimo: str,
                      var_pontuacao_emprestimos: str,
                      var_vl_total: int,
                      var_tx_juros: float,
                      var_hst_inadimplencia: int,
                      var_hst_primeiro_credito: int):
    global variaveis, dados

    variaveis = {"pessoa_idade": [var_pessoa_idade],
                 "salario_ano": [var_salario_ano],
                 "propriedade_sit": [var_propriedade_sit],
                 "ano_trabalhado": [var_ano_trabalhado],
                 "motivo_emprestimo": [var_motivo_emprestimo],
                 "pontuacao_emprestimos": [var_pontuacao_emprestimos],
                 "vl_total": [var_vl_total],
                 "tx_juros": [var_tx_juros],
                 "hst_inadimplencia": [var_hst_inadimplencia],
                 "hst_primeiro_credito": [var_hst_primeiro_credito]}
    
    dados = pd.DataFrame(variaveis, index=[0])
    
    print(dados)
    return variaveis


@app.get("/previsao")
def previsao():
    global x
    
    criar_faixa_idade(dados)
    criar_faixa_valor(dados)

    df_predicao = one_hot_enc.transform(dados)
    df_predicao = pd.DataFrame(df_predicao, columns=one_hot_enc.get_feature_names_out())

    x = scaler.transform(df_predicao)
    
    print(x)
    previsao = modelo.predict(x)
    
    return  {"previsao": previsao[0],
             'probability_0': modelo.predict_proba(x).tolist()[0][0],
             'probability_1': modelo.predict_proba(x).tolist()[0][1]}


@app.get("/testeimg")
def teste_retorno():
    teste = modelo.decision_function(x)
    print(teste)
    return {'ok'}
