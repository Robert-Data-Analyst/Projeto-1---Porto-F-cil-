import pandas as pd
from datetime import datetime, timedelta

# Carregar os dados
df = pd.read_csv('movimentacao.csv')

''' Converter datas'''
# aqui os valores da coluna data_chegada serão transformadas em um objeto datetime
# os valores que não puderem ser transformados recebem o valor NaT
df['data_chegada'] = pd.to_datetime(df['data_chegada'], errors='coerce')

''' Definir data limite (últimos 90 dias a partir de 07/10/2025)'''
# datetime define que a data será contada a partir de 07/10/2025
# e timedelta define o intervalo de tempo
# subtraindo as duas datas temos como resultado 09/07/2025
# esse valor será atribuído a data_limite
data_limite = datetime(2025, 10, 7) - timedelta(days=90)

''' Filtrar dados dos últimos 90 dias'''
# criado um novo dataframe com as datas filtradas
# ou seja, fizemos a conversão e agora nessa comparação todos as linhas onde, na coluna data_chegada,
# tiver valores NaT serão excluídos uma vez que retornarão 'false"
# importante dizer que todas as demais colunas serão copiadas para o novo dataframe
df_filtrado = df[df['data_chegada'] >= data_limite].copy()

''' Remover registros com dados ausentes relevantes'''
# aqui, através da função .dropna(subset=""), definimos as tabelas onde ao ser localizado valores NaN, NaT e None
# terão as linhas excluídas de todas as colunas do dataframe
df_filtrado = df_filtrado.dropna(subset=['tipo_carga', 'volume_carga', 'berco'])

# Agrupar por berço e tipo de carga e somar volume
agrupado = df_filtrado.groupby(['berco', 'tipo_carga'])['volume_carga'].sum().reset_index()

# Calcular volume total por berço
volume_total_berco = agrupado.groupby('berco')['volume_carga'].sum().reset_index()
volume_total_berco.rename(columns={'volume_carga': 'volume_berco'}, inplace=True)

# Mesclar para calcular porcentagem
relatorio = pd.merge(agrupado, volume_total_berco, on='berco')
relatorio['percentual'] = (relatorio['volume_carga'] / relatorio['volume_berco']) * 100

# Ordenar por berço e volume decrescente
relatorio = relatorio.sort_values(by=['berco', 'volume_carga'], ascending=[True, False])

# Selecionar os 5 principais tipos de carga por berço
relatorio_top5 = relatorio.groupby('berco').head(5)

# Exibir relatório final
print(relatorio_top5[['berco', 'tipo_carga', 'volume_carga', 'percentual']])
