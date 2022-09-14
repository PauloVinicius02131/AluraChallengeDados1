
# uvicorn main:app --reload


from fastapi import FastAPI
import pandas as pd
import pickle
from BIBLIOTECA.funcoes import criar_faixas

app = FastAPI()


with open('MODELO/one_hot_enc.pkl', 'rb') as f:
    one_hot_enc = pickle.load(f)
    
with open('MODELO/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
    
with open('MODELO/modelo.pkl', 'rb') as f:
    modelo = pickle.load(f)

@app.get("/")
def hello_root():
    return {"message": "Hello World"}

@app.get("/testedicionario/")
def teste_dicionario(testedic: str, teste2dic: str):
    return testedic , teste2dic

#http://127.0.0.1:8000/testedicionario/?testedic="testestring"&teste2dic="testestring2"


@app.get("/montardicionario/")
def montar_dicionario(teste_pessoa_id: str, 
                      teste_pessoa_idade: int,
                      teste_salario_ano: int,
                      teste_propriedade_sit: str,
                      teste_ano_trabalhado: int,
                      teste_motivo_emprestimo: str,
                      teste_pontuacao_emprestimos: str,
                      teste_vl_total: int,
                      teste_tx_juros: int,
                      teste_hst_inadimplencia: int,
                      teste_hst_primeiro_credito: int):
    global variaveis
    
    variaveis = {"pessoa_id": [teste_pessoa_id],
                       "pessoa_idade": [teste_pessoa_idade],
                       "salario_ano": [teste_salario_ano],
                       "propriedade_sit": [teste_propriedade_sit],
                       "ano_trabalhado": [teste_ano_trabalhado],
                       "motivo_emprestimo": [teste_motivo_emprestimo],
                       "pontuacao_emprestimos": [teste_pontuacao_emprestimos],
                       "vl_total": [teste_vl_total],
                       "tx_juros": [teste_tx_juros],
                       "inadimplencia": [0],
                       "hst_inadimplencia" :[teste_hst_inadimplencia],
                       "hst_primeiro_credito": [teste_hst_primeiro_credito]}
    
    return variaveis

#http://127.0.0.1:8000/testedicionario/?teste_pessoa_id="abc"&teste_pessoa_idade="25"&teste_salario_ano=""&teste_propriedade_sit=""&teste_ano_trabalhado=""&teste_motivo_emprestimo=""&teste_pontuacao_emprestimos=""&teste_vl_total=""&teste_tx_juros=""&teste_hst_inadimplencia=""&teste_hst_primeiro_credito=""

#http://127.0.0.1:8000/montardicionario/?teste_pessoa_id="abc"&teste_pessoa_idade=27&teste_salario_ano=128000&teste_propriedade_sit="Hipotecada"&teste_ano_trabalhado=7&teste_motivo_emprestimo="Pagamento de dÃ©bitos"&teste_pontuacao_emprestimos="A"&teste_vl_total=6000&teste_tx_juros=8&teste_hst_inadimplencia=0&teste_hst_primeiro_credito=4

@app.get("/testeretorno")
def teste_retorno():
    df_predicao = pd.DataFrame(variaveis, index=[0])
    df_predicao = one_hot_enc.transform(df_predicao)
    df_predicao = pd.DataFrame(
        df_predicao, columns=one_hot_enc.get_feature_names())
    criar_faixas(df_predicao=df_predicao)
    data_predicao = df_predicao.drop(
        columns=['pessoa_id', 'pessoa_idade', 'salario_ano', 'vl_total'])
    x = data_predicao.drop(columns=['inadimplencia'])
    x = scaler.transform(x)
    previsao = modelo.predict(x)
    print(previsao)
    return {"previsao": previsao[0]}

