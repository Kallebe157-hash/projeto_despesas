import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "despesas.csv"
COLS = ["data", "descricao", "categoria", "valor"]

def _empty_df():
    return pd.DataFrame(columns=COLS)

def load_despesas():
    """Carrega o CSV, criando se não existir. Garante colunas e tipos."""
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        df = _empty_df()
        df.to_csv(CSV_FILE, index=False)
        return df

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception:
        # Se der erro de leitura, recomeça limpo
        df = _empty_df()

    # Garante colunas esperadas
    for c in COLS:
        if c not in df.columns:
            df[c] = pd.Series(dtype="object")

    # Normaliza tipos
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["descricao"] = df["descricao"].astype("string").fillna("")
    df["categoria"] = df["categoria"].astype("string").fillna("")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0)

    # Ordena colunas
    df = df[COLS]
    return df

def save_despesas(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

def validar_data(data_str: str) -> bool:
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def adicionar_despesa(df: pd.DataFrame) -> pd.DataFrame:
    data = input("Data da despesa (YYYY-MM-DD): ").strip()
    while not validar_data(data):
        print("Data inválida! Use o formato YYYY-MM-DD.")
        data = input("Data da despesa (YYYY-MM-DD): ").strip()

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
            valor = float(input("Valor (use ponto como separador decimal): ").strip())
            if valor <= 0:
                print("O valor deve ser positivo!")
                continue
            break
        except ValueError:
            print("Digite um valor numérico válido (ex: 25.50).")

    novo_registro = pd.DataFrame([{
        "data": data,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor
    }])

    df = pd.concat([df, novo_registro], ignore_index=True)
    save_despesas(df)
    print("✅ Despesa adicionada com sucesso!")
    return df

def listar_despesas(df: pd.DataFrame):
    if df.empty:
        print("Nenhuma despesa registrada ainda.")
        return
    # Exibe com a data formatada
    df_show = df.copy()
    df_show["data"] = df_show["data"].dt.strftime("%Y-%m-%d")
    print("\n=== LISTA DE DESPESAS ===")
    print(df_show.to_string(index=False))
    print()

def resumo_por_categoria(df: pd.DataFrame):
    if df.empty:
        print("Nenhuma despesa para resumir.")
        return
    resumo = df.groupby("categoria", dropna=False)["valor"].sum().sort_values(ascending=False)
    print("\n=== RESUMO POR CATEGORIA ===")
    print(resumo.to_string())
    print(f"\nTotal geral: R$ {df['valor'].sum():.2f}\n")

def grafico_gastos_mensais(df: pd.DataFrame):
    if df.empty:
        print("Nenhuma despesa para gerar gráfico.")
        return
    dfg = df.copy()
    dfg["ano_mes"] = dfg["data"].dt.to_period("M").astype(str)
    mensal = dfg.groupby("ano_mes")["valor"].sum().sort_index()

    if mensal.empty:
        print("Sem dados mensais para plotar.")
        return

    mensal.plot(kind="bar")
    plt.title("Gastos por mês")
    plt.xlabel("Ano-Mês")
    plt.ylabel("Valor (R$)")
    plt.tight_layout()
    plt.show()

def menu():
    df = load_despesas()
    while True:
        print("=== CONTROLE DE DESPESAS ===")
        print("1) Adicionar despesa")
        print("2) Listar despesas")
        print("3) Resumo por categoria")
        print("4) Gráfico mensal")
        print("5) Sair")
        opc = input("Escolha uma opção: ").strip()

        if opc == "1":
            df = adicionar_despesa(df)
        elif opc == "2":
            listar_despesas(df)
        elif opc == "3":
            resumo_por_categoria(df)
        elif opc == "4":
            grafico_gastos_mensais(df)
        elif opc == "5":
            print("Até mais!")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    menu()
