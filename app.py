import streamlit as st
import zipfile
import io
import pandas as pd

st.title("Relatório de Vendas Diárias 💵")
st.set_page_config(layout='wide', page_icon='💵', page_title='Relatório Eddi')

# Upload do arquivo ZIP
uploaded_file = st.file_uploader("Faça o upload de um arquivo .zip", type=["zip"])

if uploaded_file is not None:
    # Lendo o arquivo ZIP na memória
    with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), "r") as zip_ref:
        file_names = zip_ref.namelist()  # Lista de arquivos dentro do ZIP

        # Filtrar apenas arquivos Excel
        excel_files = [file for file in file_names if file.endswith('.xls') or file.endswith('.xlsx')]

        if not excel_files:
            st.error("Nenhum arquivo Excel encontrado no ZIP.")
        else:
            st.write("Arquivos Excel encontrados:")
            # for file in excel_files:
            #     st.write(file)

            lista_df = []

            for file in excel_files:
                with zip_ref.open(file) as excel_file:
                    # Extração de informações do nome do arquivo
                    partes_nome = file.split(" - ")
                    nome_mktplace = partes_nome[0]
                    data_do_arquivo = partes_nome[-1].replace('.', '/').replace('/xls', '').replace('/xlsx', '')

                    if len(partes_nome) == 3:
                        nome_empresa = partes_nome[1]
                    else:
                        nome_empresa = "NÃO DEFINIDO"

                    # Leitura do arquivo Excel
                    df = pd.read_excel(excel_file)
                    df["mktplace"] = nome_mktplace
                    df["Empresa"] = nome_empresa
                    df["Data"] = data_do_arquivo
                    lista_df.append(df)

            # Concatenar todos os dataframes
            df = pd.concat(lista_df, ignore_index=True)

            # Tratamento da coluna 'Quantidade'
            df["Quantidade"] = df["Quantidade"].astype(str).str.replace(",", ".").astype(float).astype(int)

            # Cálculo do total de vendas
            total_vendas = df["Quantidade"].sum()
            st.success(f"--- Quantidade total de vendas: {total_vendas} ---")

            # Vendas por canais de vendas
            vendas_canais = df.groupby("mktplace")["Quantidade"].sum()
            st.subheader("- Vendas por Canais de Vendas -")
            for mktplace, quantidade in vendas_canais.items():
                st.write(f"**{mktplace.title()}**: {quantidade}")

            # Vendas por empresa
            vendas_empresas = df.groupby("Empresa")["Quantidade"].sum().sort_values(ascending=False)
            st.subheader("- Vendas por Empresas -")
            for empresa, quantidade in vendas_empresas.items():
                st.write(f"**{empresa.title()}**: {quantidade}")

            # Criar botão para baixar o relatório em CSV
            csv = df.to_csv(index=False, encoding="utf-8-sig", sep=";")
            st.download_button(label="Baixar Relatório CSV", data=csv, file_name="relatorio_vendas.csv", mime="text/csv")
