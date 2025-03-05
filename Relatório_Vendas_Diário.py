# %%
import pandas as pd
import shutil 
from pathlib import Path
import requests

lista_df = []
pasta = input('Digite o endereço: ').replace('"', '')
caminho_pasta = Path(pasta)
for arquivo in caminho_pasta.iterdir():
    if str(arquivo.name).endswith('xls'):
        nome_mktplace = arquivo.name.split(' - ')[0] 
        data_do_arquivo = arquivo.name.split(' - ')[-1].replace('.', '/').replace('/xls', '')
        if len(str(arquivo.name).split(' - ')) == 3:
            nome_empresa = str(arquivo.name).split(' - ')[1]
        else:
            nome_empresa = 'NÃO DEFINIDO'                    
        df = pd.read_excel(arquivo)
        df['mktplace'] = nome_mktplace
        df['Empresa'] = nome_empresa
        df['Data'] = data_do_arquivo
        lista_df.append(df)
df = pd.concat(lista_df, ignore_index=True)
total_vendas = df['Quantidade'].str.replace(',', '.').astype(float).astype(int).sum()
print(f'--- Quantidade de vendas dia {data_do_arquivo}: {total_vendas} ---')
mensagem1 = f'Quantidade de vendas dia {data_do_arquivo}: {total_vendas} '
df['Quantidade'] = df['Quantidade'].str.replace(',', '.').astype(float).astype(int)
vendas_canais = df.groupby('mktplace')['Quantidade'].sum()
print('\n- Vendas Canais de Vendas -')
for mktplace, quantidade in vendas_canais.items():
    print(f'{mktplace.title()}: {quantidade}')
vendas_empresas = df.groupby('Empresa')['Quantidade'].sum().sort_values(ascending=False)
print('\n- Vendas Empresas -')
for Empresa, quantidade in vendas_empresas.items():
    print(f'{Empresa.title()}: {quantidade}')    
vendas_canais_empresas = df.groupby(['Empresa', 'mktplace'])['Quantidade'].sum() 
# df.to_csv('Relatorio sumarizado.csv', index=False, encoding='utf-8-sig', sep=';')         
print(' ')
mensagem = [mensagem1, vendas_canais, vendas_empresas]
# %%
for c in mensagem:
    url = f'https://api.callmebot.com/whatsapp.php?phone=+5516981610385&text={c}&apikey=4901827'
    requests.get(url)

# %%
vendas_canais_empresas