import pandas as pd


# Projeto - Porto Fácil (Análise de Dados com Pandas)
# Relatório de Eficiência de Atracação

""""
Importar dados fictícios de movimentação portuária (CSV)
Limpar, filtrar, agrupar e gerar estatísticas
Criar relatório consolidado com groupby, merge, sort_values
"""


# Criando os dados fictícios
# gerei um dicionário que irei transformar em dataframe
dados = {
    'navio': [
        'Atlântico Sul', 'Mar Azul', 'Estrela do Mar', 'Vento Norte', 'Sol Nascente',
        'Aurora Boreal', 'Tempestade', 'Luz do Oceano', 'Maré Alta', 'Horizonte',
        'Atlântico Sul', 'Mar Azul', 'Estrela do Mar', 'Vento Norte', 'Sol Nascente',
        'Aurora Boreal', 'Tempestade', 'Luz do Oceano', 'Maré Alta', 'Horizonte',
        'Estrela Polar', 'Brisa do Mar', 'Coral Vivo', 'Nevoeiro', 'Alvorada',
        'Estrela Polar', 'Brisa do Mar', 'Coral Vivo', 'Nevoeiro'
    ],
    'data_chegada': [
        '2025-09-01', '2025-09-02', '2025-09-03', '2025-09-04', '2025-09-05',
        '2025-09-06', '2025-09-07', '2025-09-08', '2025-09-09', '2025-09-10',
        '2025-09-11', '2025-09-12', '2025-09-13', '2025-09-14', '2025-09-15',
        '2025-09-16', '2025-09-17', '2025-09-18', '2025-09-19', '2025-09-20',
        '2025-09-21', '2025-09-22', None, '2025-09-24', '2025-09-25',
        '2025-09-26', '2025-09-27', '2025-09-28', '2025-09-29'
    ],
    'data_saida': [
        '2025-09-03', '2025-09-05', '2025-09-04', '2025-09-06', '2025-09-07',
        '2025-09-08', '2025-09-09', '2025-09-10', '2025-09-11', '2025-09-12',
        '2025-09-13', '2025-09-14', '2025-09-15', '2025-09-16', '2025-09-17',
        '2025-09-18', '2025-09-19', '2025-09-20', '2025-09-21', None,
        '2025-09-23', '2025-09-24', '2025-09-25', '2025-09-26', '2025-09-27',
        None, '2025-09-29', '2025-09-30', '2025-10-01'
    ],
    'tipo_carga': [
        'Contêineres', 'Granel Líquido', 'Contêineres', 'Granel Sólido', 'Veículos',
        'Contêineres', 'Granel Líquido', 'Contêineres', 'Granel Sólido', 'Veículos',
        'Contêineres', 'Granel Líquido', 'Contêineres', 'Granel Sólido', 'Veículos',
        'Contêineres', 'Granel Líquido', 'Contêineres', 'Granel Sólido', None,
        'Contêineres', 'Granel Líquido', 'Contêineres', 'Granel Sólido', 'Veículos',
        'Contêineres', None, 'Granel Sólido', 'Veículos'
    ],
    'volume_carga': [
        1200, 850, 950, 1500, 600,
        1300, 900, 1000, 1600, 700,
        1100, 870, 980, 1400, 650,
        1250, 880, 1020, 1550, None,
        1150, 890, None, 1450, 670,
        1280, 910, 990, 1500
    ],
    'berco': [
        1, 2, 1, 3, 2,
        1, 2, 1, 3, 2,
        1, 2, 1, 3, 2,
        1, 2, 1, 3, None,
        1, 2, 1, 3, 2,
        None, 2, 1, 3
    ]
}

# Criando o DataFrame
df = pd.DataFrame(dados)

# Salvando como CSV
df.to_csv('movimentacao.csv', index=False)


"""
nesse contexto irei fazer alguns desafios emulando solicitações reais
"""

# 1° dasafio - Relatório de eficiência de atracação

"""
O gerente operacional quer saber quais navios estão atracando com maior eficiência, ou seja, menor tempo entre chegada e saída.

"""
"""
Tarefas:

- Limpar dados faltantes ou datas inválidas
- Calcular tempo de permanência (data_saida - data_chegada)
- Agrupar por navio e calcular média de permanência
- Ordenar por menor tempo médio (sort_values)
- Gerar relatório com os 10 navios mais eficientes

"""

# Etapa 1: Limpeza de dados faltantes e datas inválidas
# Remove linhas com data_chegada ou data_saida ausentes
df = df.dropna(subset=['data_chegada', 'data_saida'])

# Converte datas para datetime
df['data_chegada'] = pd.to_datetime(df['data_chegada'], errors='coerce')
df['data_saida'] = pd.to_datetime(df['data_saida'], errors='coerce')

# Remove linhas com datas inválidas após conversão
df = df.dropna(subset=['data_chegada', 'data_saida'])

# Etapa 2: Calcular tempo de permanência
# Garante que data_saida seja posterior à data_chegada
df = df[df['data_saida'] >= df['data_chegada']]
df['tempo_permanencia'] = (df['data_saida'] - df['data_chegada']).dt.days

# Etapa 3: Agrupar por navio e calcular estatísticas
relatorio = df.groupby('navio').agg(
    media_permanencia=('tempo_permanencia', 'mean'),
    total_atracacoes=('navio', 'count'),
    volume_medio=('volume_carga', 'mean')
).reset_index()

# Etapa 4: Ordenar por menor tempo médio de permanência
relatorio = relatorio.sort_values(by='media_permanencia')

# Etapa 5: Selecionar os 10 navios mais eficientes
relatorio_top10 = relatorio.head(10)

# Exibir o relatório final
print(relatorio_top10)
