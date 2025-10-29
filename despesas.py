import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "despesas.csv"

def load_despesas():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["data", "descricao", "categoria", "valor"])

def save_despesas(df):
    df.to_csv(CSV_FILE, index=False)

def validar_data(data_str):
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def adicionar_despesa(df):
    data = input("Data da despesa (YYYY-MM-DD): ")
    while not validar_data(data):
        print("Data inválida! Use o formato YYYY-MM-DD.")
        data = input("Data da despesa (YYYY-MM-DD): ")
    
    descricao = input("Descrição: ").strip()
    while not descricao:
        print("Descrição não pode estar vazia!")
        descricao = input("Descrição: ").strip()
    
    categoria = input("Categoria: ").strip()
    while not categoria:
        print("Categoria não pode estar vazia!")
        categoria = input("Categoria: ").strip()
    
    while True:
        try:
            valor = float(input("Valor: "))
            if valor <= 0:
                print("O valor deve ser positivo!")
                continue
            break
        except ValueError:
            print("Digite um valor numérico válido.")
    
    # CORREÇÃO: usando concat ao invés de append
    novo_registro = pd.DataFrame([{
        "data": data, 
        "descricao": descricao,
        "categoria": categoria, 
        "valor": valor
    }])
    
    df = pd.concat([df, novo_registro], ignore_index=True)
    save_despesas(df)
    print("Despesa adicionada com sucesso!")
    return df
