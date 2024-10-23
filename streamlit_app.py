# Bibliotecas para deploy em Streamlit
# Bibliotecas para manipulação de arquivos e expressões regulares
import os
import re

# Bibliotecas para análise de dados
import pandas as pd
# Bibliotecas para visualização de dados
import plotly.express as px
import streamlit as st

# Importação de funções e classes do projeto
from import_databases import import_db
from models import page_classifier
from run_model import page_run_model, exibir_teoria_do_modelo

# Bibliotecas para modelagem e estatística
# Bibliotecas para modelos de classificação
# Biblioteca para plotagem de mapas

st.set_page_config(layout="wide", page_title="Dashboard - Engope 2024", page_icon=":bar_chart:")


def logo():
    st.sidebar.image('static/logos/logo-ufg.png', width=400)
    #st.sidebar.image('static/logo-ufg.jpg', width=100)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.write('')
    with col2:
        st.write('')
    with col3:
        st.write('')
    with col4:
        st.write('')
    with col5:
        st.write('')
    with col6:
        st.image('static/logos/logo_engope_2024.jpg', width=200)


def intro():

    # Título e cabeçalho principal
    st.title("Plataforma de Monitoramento de Degradação de Pastagens")
    st.header("Classificação e Visualização Temática das Unidades Amostrais")

    st.markdown('---')

    st.markdown("""O grupo **Brachiara LAB** foi criado com o objetivo de desenvolver soluções inovadoras para combater a degradação de pastagens, um problema relevante para a sustentabilidade agropecuária. A participação no **I Datathon**, promovido durante o **VI ENGOPE – Encontro Goiano de Probabilidade e Estatística**, pelo Instituto de Matemática e Estatística **(IME)** da UFG, nos permitiu aplicar conceitos de análise de dados e estatística de maneira prática e colaborativa.""")

    # Descrição inicial
    st.markdown("""
    Esta plataforma tem como objetivo **classificar as unidades amostrais** de pastagens, **identificando níveis de degradação** com base em variáveis ecológicas e de manejo. A partir das análises, é gerada uma **visualização final por meio de um mapa temático**, permitindo uma compreensão espacial intuitiva e facilitando a tomada de decisão para o manejo sustentável das áreas avaliadas.
    """)

    st.markdown('---')    
    # Funcionalidades
    st.subheader("Funcionalidades")
    st.markdown("""
    - **Classificação Automática**: Algoritmos de aprendizado de máquina classificam as áreas com base em níveis de degradação definidos.
    - **Análises Descritivas**: Geração de relatórios com estatísticas das variáveis amostrais, como disponibilidade de folhas verdes, presença de invasoras e estágio de desenvolvimento das plantas.
    - **Visualização em Mapa Temático**: Visualize os resultados das classificações em um **mapa interativo**, facilitando a compreensão dos padrões espaciais de degradação.
    - **Exportação de Relatórios**: Exporte relatórios completos ou personalizados em PDF, contendo os principais insights das análises.
    """)

    st.markdown('---')
    # Sobre o Conjunto de Dados
    st.subheader("Sobre o Conjunto de Dados")
    st.markdown("""
    O monitoramento das **pastagens tropicais brasileiras** é essencial para garantir um manejo sustentável, dada a sua ampla diversidade de espécies e a sua vulnerabilidade à degradação. O conjunto de dados utilizado foi coletado em Goiás, em parceria com o **MapBiomas**, com o objetivo de mapear as áreas de pastagem e avaliar seu nível de degradação, essencial para a preservação ambiental.
    """)

    st.markdown('---')
    # Como Funciona
    st.subheader("Como Funciona")
    st.markdown("""
    1. **Navegue pelo menu** e selecione a página desejada.
    2. **Escolha as variáveis e parâmetros** para realizar a classificação.
    3. **Visualize os resultados** por meio de mapas e relatórios.
    """)

    st.markdown('---')
# Equipe e Contato
    st.subheader("Equipe e Contato")
    st.markdown("""
    Este projeto é desenvolvido para o **1º Datathon** do **6º Encontro Goiano de Probabilidade e Estatística (Engope)** do IME-UFG.

    Colaboradores do projeto:
    Danilo Silva Caravalho de Oliveira  - IME
    José Diogo Ferreira de Melo - IME
    Mateus Rrodrigues Alves de Aquino - IME
    Matheus Henrique de Souza Carvalho  - IME
    Vinícius Ferreira Amorim Santada - IME
    
    Para dúvidas ou mais informações, entre em contato pelo e-mail: **mateusrodriguesq@gmail.com**""")

    st.markdown("---")

    if st.button("Ver mais informações sobre a coleta de campo"):

        st.subheader("Coleta de Campo")
        st.markdown("""A coleta foi realizada dentro de unidades amostrais (UA) de **30 x 30 m (900 m\u00B2)**, cada uma representando um pixel dentro da área mapeada. A localização das UAs foi definida por avaliadores em campo utilizando GPS.
            """)

        st.markdown("---")     
        st.subheader("Variáveis Avaliadas")
        st.markdown("""
    As principais variáveis ecológicas foram analisadas por dois avaliadores em cada UA, que atribuíram notas de 1 a 7 para cada variável. As variáveis avaliadas incluem:
    - **Estágio de Desenvolvimento das Plantas**: Variável que analisa o estágio de crescimento das plantas na pastagem. Notas mais baixas indicam perfilhos jovens, enquanto notas mais altas indicam perfilhos em estágio reprodutivo avançado.
    - **Presença de Plantas Invasoras**: Avalia a proporção de plantas invasoras presentes em relação à vegetação forrageira.
    - **Presença de Cupins**: Considera a presença de cupinzeiros e a degradação que eles causam no solo.
    - **Cobertura Vegetal do Solo**: Relaciona-se com a quantidade de solo coberto por vegetação viva.
    - **Disponibilidade de Forragem e Folhas Verdes**: Avaliação da quantidade de material vegetal disponível, que é fundamental para a alimentação do gado.
    - **Condição Atual da Pastagem**: Avaliação visual geral da pastagem, levando em conta todos os fatores acima.
    - **Potencial Produtivo**: Projeção da capacidade da pastagem para os próximos 12 meses.
    """)

        st.markdown("---")
    # Detalhes das variáveis com tabelas explicativas
    ### Escalas de Avaliação das Variáveis:
        st.markdown("""
    **Estágio de Desenvolvimento das Plantas**:
    1. Ausência de folhas senescentes, elevado crescimento.
    2. Predominância de folhas verdes, colmos finos.
    3. Boa relação folha:colmo, planta em alongamento.
    4. Início do processo de alongamento, senescência de algumas folhas.
    5. Inflorescência se desenvolvendo, folhas senescentes.
    6. Alta quantidade de folhas senescentes, baixa relação folha:colmo.
    7. Pasto seco, predominância de folhas senescentes e mortas.""")

        st.markdown("---")
        st.markdown("""
    **Presença de Plantas Invasoras**:
    1. Nenhuma planta invasora.
    2. Até 10% da área com invasoras.
    3. Entre 10% e 30% da área com invasoras.
    4. Entre 30% e 50% da área com invasoras.
    5. Entre 50% e 70% da área com invasoras.
    6. Entre 70% e 90% da área com invasoras.
    7. Mais de 90% da área com invasoras.""")

        st.markdown("---")
        st.markdown("""
    **Cobertura Vegetal do Solo**:
    1. Menos de 10% de vegetação viva.
    2. Cobertura entre 10% e 30%.
    3. Cobertura entre 30% e 45%.
    4. Cobertura entre 45% e 55%.
    5. Cobertura entre 55% e 65%.
    6. Cobertura entre 65% e 90%.
    7. Mais de 90% de vegetação viva.""")

        st.markdown("---")
        st.markdown("""  
    **Condição Atual da Pastagem**:
    1. Degradação intensa, TL < 0,3 UA/ha.
    2. Severamente degradada, TL entre 0,3 a 0,5 UA/ha.
    3. Baixa qualidade forrageira, TL entre 0,5 a 0,7 UA/ha.
    4. Condição média, TL entre 0,7 a 1,0 UA/ha.
    5. Boa condição, TL entre 1,0 a 2,0 UA/ha.
    6. Próximo ao máximo, TL entre 2,0 a 3,0 UA/ha.
    7. Excelente condição, TL > 3,0 UA/ha.""")



def metric_with_info(label, value, delta, description):
    # Criar o HTML para a label e o ícone de informação
    html_content = f'''
    <div style="display: flex; align-items: center;">
        <span>{label}</span>
        <span style="margin-left: 5px; cursor: pointer;" title="{description}">ℹ️</span>
    </div>
    '''
    # Exibir o HTML da label e ícone de informação
    st.markdown(html_content, unsafe_allow_html=True)
    # Exibir o componente de métrica
    st.metric(label=label, value=value, delta=delta, label_visibility="collapsed")


def page_eda():
    st.title('Análise Exploratória de Dados')
    importer = import_db()
    dados_scores = importer.get_dados_scores()
    dados_geoloc_classe = importer.get_dados_geoloc_classe()
    dicionario_variaveis = importer.get_dicionario_variaveis()

    # Create a dictionary for variable descriptions
    var_desc = dict(zip(dicionario_variaveis['NOME'], dicionario_variaveis['DESCRIÇÃO']))

    # Merge dados_scores and dados_geoloc_classe by Ponto e PontoID
    dados = dados_scores.merge(dados_geoloc_classe, on=['Ponto', 'PontoID'])
    # Fillna 0
    dados.fillna(0, inplace=True)
    # dados['LOCCLASS'] if outside, Fora da área, if inside, Dentro da área
    dados['LOCCLASS'] = dados['LOCCLASS'].apply(lambda x: 'Fora da área' if x == 0 else 'Dentro da área')

    # Ensure Especie01 column is of type string
    dados = dados[dados['Especie01'] != 0]
    dados['Especie01'] = dados['Especie01'].astype(str)


    # Multiselect to choose filters
    #in pontos default the Ponto = 'M1091-E1-P6'
    print(dados['Especie01'].unique())
    especies = st.sidebar.multiselect('Selecione as Espécies', dados['Especie01'].unique())
    avaliadores = st.sidebar.multiselect('Selecione os Avaliadores', dados['Avaliador'].unique())
    pontos = st.sidebar.multiselect('Selecione os Pontos', dados['Ponto'].unique(), default=['M1091-E1-P6'])

    # Filter data based on selections
    if pontos:
        dados = dados[dados['Ponto'].isin(pontos)]
    if avaliadores:
        dados = dados[dados['Avaliador'].isin(avaliadores)]
    if especies:
        dados = dados[dados['Especie01'].isin(especies)]

    # Merge all data_filtered in Avaliador and save in a string
    avaliadores_str = ', '.join(dados['Avaliador'].unique())

    # Format data to DD/MM/YYYY
    if not dados.empty:
        data = dados['Data'].iloc[0].strftime('%d/%m/%Y')
    else:
        data = 'Data not available'

    st.markdown('---')
    st.write(
        '**Estatísticas Descritivas coletados por:** ' + avaliadores_str + ' **no Ponto** ' + '**' + ', '.join(pontos) + '**' + ' em ' + '**' + data + '**.')


    c1, c2, c3 = st.columns(3)
    with c1:
        metric_with_info('Altura Média (cm)', round(dados['Altura'].mean(), 2), round(dados['Altura'].std(), 2), 'ALTURA')
    with c2:
        metric_with_info('Estágio de Desenvolvimento Médio', round(dados['EstDesenv'].mean(), 2), round(dados['EstDesenv'].std(), 2), 'EstDesenv')
    with c3:
        metric_with_info('Presença de Invasoras Média', round(dados['Invasoras'].mean(), 2), round(dados['Invasoras'].std(), 2), 'INVASORAS')

    c4, c5, c6 = st.columns(3)
    with c4:
        metric_with_info('Presença de Cupins Média', round(dados['Cupins'].mean(), 2), round(dados['Cupins'].std(), 2), 'CUPINS')
    with c5:
        metric_with_info('Cobertura do Solo Média', round(dados['CobertSolo'].mean(), 2), round(dados['CobertSolo'].std(), 2), 'CobertSolo')
    with c6:
        metric_with_info('Disponibilidade de Forragem Média', round(dados['DispForr'].mean(), 2), round(dados['DispForr'].std(), 2), 'DispForr')

    c7, c8, c9, c10, c11 = st.columns(5)
    with c7:
        metric_with_info('Disponibilidade de Folhas Verdes Média', round(dados['DispFolhVerd'].mean(), 2), round(dados['DispFolhVerd'].std(), 2), 'DispFolhVerd')
    with c8:
        metric_with_info('Condição Atual Média', round(dados['CondAtual'].mean(), 2), round(dados['CondAtual'].std(), 2), 'CondAtual')
    with c9:
        metric_with_info('Potencial Produtivo Médio', round(dados['PotProd'].mean(), 2), round(dados['PotProd'].std(), 2), 'PotProd')
    with c10:
        metric_with_info('Nível de Degradação Médio', round(dados['Degrad'].mean(), 2), round(dados['Degrad'].std(), 2), 'Degrad')
    with c11:
        metric_with_info('Manejo Médio', round(dados['Manejo'].mean(), 2), round(dados['Manejo'].std(), 2), 'Manejo')

    c13, c14, c15 = st.columns(3)
    with c13:
        metric_with_info('Dentro ou fora da estrada', dados['LOCCLASS'].iloc[0], '', 'LOCCLASS')
    with c14:
        color = ''
        if dados['CLASS_DED'].iloc[0] == 'Não Degradada':
            color = 'green'
        elif dados['CLASS_DED'].iloc[0] == 'Degradada Baixa':
            color = 'yellow'
        elif dados['CLASS_DED'].iloc[0] == 'Degradada Moderada':
            color = 'orange'
        elif dados['CLASS_DED'].iloc[0] == 'Degradada Agrícola Severa':
            color = 'red'
        elif dados['CLASS_DED'].iloc[0] == 'Degradada Biológica Severa':
            color = 'purple'

        st.markdown(
            f"<div style='font-size:25px;'>Classe de Degradação: <span style='color:{color}; font-weight:bold;'>{dados['CLASS_DED'].iloc[0]}</span></div>",
            unsafe_allow_html=True)
    with c15:
        metric_with_info('Espécie', dados['Especie01'].iloc[0], '', 'ESPECIE_01')
    st.markdown('---')



    st.write('**Dados por Avaliador**')
    # Order the data_filtered like [['Avaliador', 'Data', 'Especie01', 'Altura', 'EstDesenv', 'Invasoras', 'Cupins', 'CobertSolo', 'DispForr', 'DispFolhVerd', 'CondAtual', 'PotProd', 'Degrad', 'Manejo', LOCCLASS', 'CLASS_DED']]
    data_filtered_a = dados[['Avaliador', 'Ponto', 'Data', 'Especie01', 'Altura', 'EstDesenv', 'Invasoras', 'Cupins', 'CobertSolo', 'DispForr', 'DispFolhVerd', 'CondAtual', 'PotProd', 'Degrad', 'Manejo', 'LOCCLASS', 'CLASS_DED']]
    st.write(data_filtered_a)

    #if especies is not null, show the distribution of CLASS_DED sum by especies in percentage bar chart not stacked (value counts)
    # if especies is not null, show the distribution of CLASS_DED sum by especies in percentage bar chart not stacked (value counts)
    if especies:
        # st.write('**Distribuição das Classes de Degradação por Espécie**')
        data_filtered_b = data_filtered_a.copy()
        data_filtered_b = data_filtered_b['CLASS_DED'].value_counts(normalize=True).reset_index()
        data_filtered_b.columns = ['CLASS_DED', 'Percentage']
        data_filtered_b['Percentage'] = round(data_filtered_b['Percentage'] * 100, 2).astype(str) + ' %'

        fig = px.bar(data_filtered_b, x='CLASS_DED', y='Percentage', text='Percentage', color='CLASS_DED', labels={'CLASS_DED': 'Classe de Degradação', 'Percentage': 'Porcentagem'}, title='Distribuição das Classes de Degradação por Espécie')
        st.plotly_chart(fig)

    if avaliadores:
        # st.write('**Distribuição das Classes de Degradação por Avaliador**')
        data_filtered_c = data_filtered_a.copy()
        data_filtered_c = data_filtered_c['CLASS_DED'].value_counts(normalize=True).reset_index()
        data_filtered_c.columns = ['CLASS_DED', 'Percentage']
        data_filtered_c['Percentage'] = round(data_filtered_c['Percentage'] * 100, 2).astype(str) + ' %'

        fig = px.bar(data_filtered_c, x='CLASS_DED', y='Percentage', text='Percentage', color='CLASS_DED', labels={'CLASS_DED': 'Classe de Degradação', 'Percentage': 'Porcentagem'}, title='Distribuição das Classes de Degradação por Avaliador')
        st.plotly_chart(fig)

        #count Pontos visitados by Avaliador sum by Ponto
        data_filtered_d = data_filtered_a.copy()
        data_filtered_d = data_filtered_d.groupby(['Avaliador', 'Ponto']).size().reset_index(name='Count')
        st.write('**Pontos Visitados por Avaliador**')
        st.metric(label='Pontos Visitados', value=data_filtered_d['Count'].sum())

    if pontos:
        # st.write('**Distribuição das Classes de Degradação por Ponto**')
        data_filtered_e = data_filtered_a.copy()
        data_filtered_e = data_filtered_e['CLASS_DED'].value_counts(normalize=True).reset_index()
        data_filtered_e.columns = ['CLASS_DED', 'Percentage']
        data_filtered_e['Percentage'] = round(data_filtered_e['Percentage'] * 100, 2).astype(str) + ' %'

        fig = px.bar(data_filtered_e, x='CLASS_DED', y='Percentage', text='Percentage', color='CLASS_DED', labels={'CLASS_DED': 'Classe de Degradação', 'Percentage': 'Porcentagem'}, title='Distribuição das Classes de Degradação por Ponto')
        st.plotly_chart(fig)

        #distribuição de plantas na região
        st.write('**Distribuição de Plantas na Região**')
        data_filtered_f = data_filtered_a.copy()
        data_filtered_f = data_filtered_f['Especie01'].value_counts(normalize=True).reset_index()
        data_filtered_f.columns = ['Especie01', 'Percentage']
        data_filtered_f['Percentage'] = round(data_filtered_f['Percentage'] * 100, 2).astype(str) + ' %'

        fig = px.bar(data_filtered_f, x='Especie01', y='Percentage', text='Percentage', color='Especie01', labels={'Especie01': 'Espécie', 'Percentage': 'Porcentagem'}, title='Distribuição de Plantas na Região')
        st.plotly_chart(fig)




    st.markdown('---')

    mapbox_styles = st.sidebar.selectbox('Escolha um estilo de mapa:', ['open-street-map', 'carto-positron', 'carto-darkmatter'])
    # List of mapbox styles that do not require an API token
    #st.write(mapbox_styles)
    #mapbox_styles = ['open-street-map', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner']

    # Plot map with filtered data for each style

    fig = px.scatter_mapbox(
        dados,
        lat="LAT",
        lon="LON",
        color="CLASS_DED",
        size="Altura",
        hover_name="Ponto",
        hover_data={"Avaliador": True, "Especie01": True, "Altura": True, "CLASS_DED": True},
        color_continuous_scale={
            'Não Degradada': '#FFD700',  # Amarelo
            'Degradada Baixa': '#FF8C00',  # Laranja
            'Degradada Moderada': '#90EE90',  # Verde claro
            'Degradação Agrícola Severa': '#D3D3D3',  # Cinza
            'Degradação Biológica Severa': '#98FB98'  # Verde mais claro
        },
        title=f"Mapa de Degradação de Pastagens - {mapbox_styles}",
        mapbox_style=mapbox_styles,
        zoom=10,
        height=600
    )
    st.plotly_chart(fig)



def page_conhecimento_plantas():
    # Título da página
    st.title('Conhecimento das Plantas')

    plant_descriptions = {
        'Brachiaria brizantha': {
            'descricao': 'Espécie de gramínea forrageira, com alta produtividade e adaptada a solos bem drenados.',
            'estado_solo': 'Melhora a qualidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Não é invasora.',
                'Incidência de cupins': 'Resistência alta.',
                'Cobertura do solo': 'Boa cobertura do solo.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto potencial.',
                'Nível de degradação': 'Resistente à degradação.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Brachiaria brizantha cv Marandu': {
            'descricao': 'Cultivar amplamente utilizada no Brasil, resistente à seca e indicada para solos de média a alta fertilidade.',
            'estado_solo': 'Aumenta a fertilidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,5 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento moderado.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção elevada.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição satisfatória.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo eficiente.'
            }
        },
        'Brachiaria decumbens': {
            'descricao': 'Gramínea rasteira que se adapta bem a solos ácidos e de baixa fertilidade.',
            'estado_solo': 'Pode empobrecer o solo se mal manejada.',
            'invasora': True,
            'variaveis': {
                'Altura do dossel': 'Até 1 metro.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento lento.',
                'Proporção de plantas daninhas': 'Presença moderada.',
                'Incidência de cupins': 'Baixa resistência.',
                'Cobertura do solo': 'Cobertura média.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Baixa oferta.',
                'Condição atual do pasto': 'Condição regular.',
                'Potencial produtivo': 'Médio.',
                'Nível de degradação': 'Moderado.',
                'Manejo adotado': 'Manejo variado.'
            }
        },
        'Paspalum notatum': {
            'descricao': 'Gramínea forrageira resistente a diferentes tipos de solo, ideal para regiões úmidas.',
            'estado_solo': 'Contribui para a retenção de umidade.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1 metro.',
                'Idade fisiológica dos perfilhos': 'Crescimento moderado.',
                'Proporção de plantas daninhas': 'Poucas.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Cobertura boa.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo eficiente.'
            }
        },
        'Andropogon gayanus': {
            'descricao': 'Gramínea alta, resistente à seca e adaptada a solos pobres.',
            'estado_solo': 'Pode melhorar a fertilidade a longo prazo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Cobertura média.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição satisfatória.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Panicum maximum cv Massai': {
            'descricao': 'Cultivar de Panicum com alta produtividade e resistência ao pastejo.',
            'estado_solo': 'Melhora a estrutura do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Não é invasora.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção muito alta.',
                'Oferta de folhas verdes (kg/ha)': 'Excelente oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Muito alto.',
                'Nível de degradação': 'Resistente à degradação.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Cynodon sp': {
            'descricao': 'Grupo de gramíneas que se adaptam bem a diferentes condições climáticas.',
            'estado_solo': 'Bom para solos compactados.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1 metro.',
                'Idade fisiológica dos perfilhos': 'Crescimento moderado.',
                'Proporção de plantas daninhas': 'Poucas.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Moderado.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo eficiente.'
            }
        },
        'Brachiaria humidicola': {
            'descricao': 'Gramínea ideal para áreas alagadas e solo úmido.',
            'estado_solo': 'Contribui para a retenção de água.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,5 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Andropogon sp': {
            'descricao': 'Gramínea que se adapta a várias condições climáticas e de solo.',
            'estado_solo': 'Pode melhorar a qualidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,8 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento moderado.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Cobertura boa.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Moderado.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Panicum maximum': {
            'descricao': 'Espécie forrageira com alta produtividade e boa resistência ao pastejo.',
            'estado_solo': 'Melhora a estrutura do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Baixa.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Brachiaria sp': {
            'descricao': 'Grupo de gramíneas que incluem várias espécies forrageiras.',
            'estado_solo': 'Contribui para a melhoria do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Variável.',
                'Idade fisiológica dos perfilhos': 'Variável.',
                'Proporção de plantas daninhas': 'Baixa.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Boa.',
                'Produção de forragem (kg/ha)': 'Variável.',
                'Oferta de folhas verdes (kg/ha)': 'Boa.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Moderado a alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Panicum maximum cv Mombaça': {
            'descricao': 'Cultivar com alta capacidade de recuperação e resistência ao pastejo.',
            'estado_solo': 'Melhora a qualidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2,5 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Excelente.',
                'Produção de forragem (kg/ha)': 'Produção muito alta.',
                'Oferta de folhas verdes (kg/ha)': 'Excelente.',
                'Condição atual do pasto': 'Condição ótima.',
                'Potencial produtivo': 'Muito alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo eficiente.'
            }
        },
        'Cynodon dactylon cv Tifton 85': {
            'descricao': 'Cultivar de Cynodon altamente produtiva e resistente ao pastejo.',
            'estado_solo': 'Melhora a estrutura do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1 metro.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento moderado.',
                'Proporção de plantas daninhas': 'Baixa.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Hyparrhenia rufa': {
            'descricao': 'Gramínea perene, bem adaptada a solos ácidos e com boa tolerância à seca.',
            'estado_solo': 'Pode melhorar a fertilidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,5 metros.',
                'Idade fisiológica dos perfilhos': 'Crescimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Moderado.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Panicum maximum cv Tanzânia': {
            'descricao': 'Cultivar de Panicum com alta produtividade e resistência ao pastejo.',
            'estado_solo': 'Melhora a qualidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 2,5 metros.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Excelente.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Excelente.',
                'Condição atual do pasto': 'Condição ótima.',
                'Potencial produtivo': 'Muito alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo eficiente.'
            }
        },
        'Brachiaria ruziziensis': {
            'descricao': 'Gramínea de crescimento rápido, ideal para solos ácidos e com alta umidade.',
            'estado_solo': 'Melhora a fertilidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,5 metros.',
                'Idade fisiológica dos perfilhos': 'Crescimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }

        },
        'Cynodon nlemfuensis': {
            'descricao': 'Gramínea forrageira adaptada a climas tropicais e subtropicais.',
            'estado_solo': 'Melhora a qualidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1 metro.',
                'Idade fisiológica dos perfilhos': 'Desenvolvimento moderado.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Moderado.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },
        'Brachiaria brizantha cv Xaraes': {
            'descricao': 'Cultivar resistente a condições de seca, ideal para a Região Centro-Oeste do Brasil.',
            'estado_solo': 'Aumenta a fertilidade do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,2 metros.',
                'Idade fisiológica dos perfilhos': 'Crescimento rápido.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Baixa.',
                'Cobertura do solo': 'Boa cobertura.',
                'Produção de forragem (kg/ha)': 'Produção alta.',
                'Oferta de folhas verdes (kg/ha)': 'Boa oferta.',
                'Condição atual do pasto': 'Condição boa.',
                'Potencial produtivo': 'Alto.',
                'Nível de degradação': 'Baixo.',
                'Manejo adotado': 'Manejo adequado.'
            }
        },

        'Brachiaria arrecta': {
            'descricao': 'Espécie de gramínea forrageira que se adapta bem a solos alagadiços. Usada em áreas úmidas e de várzea.',
            'estado_solo': 'Melhora a drenagem do solo.',
            'invasora': False,
            'variaveis': {
                'Altura do dossel': 'Até 1,5 metros.',
                'Idade fisiológica dos perfilhos': 'Crescimento moderado.',
                'Proporção de plantas daninhas': 'Baixa presença.',
                'Incidência de cupins': 'Moderada.',
                'Cobertura do solo': 'Boa cobertura, especialmente em áreas úmidas.',
                'Produção de forragem (kg/ha)': 'Produção moderada.',
                'Oferta de folhas verdes (kg/ha)': 'Oferta moderada.',
                'Condição atual do pasto': 'Condição boa, dependendo do manejo.',
                'Potencial produtivo': 'Moderado a alto.',
                'Nível de degradação': 'Resistente à degradação em condições úmidas.',
                'Manejo adotado': 'Requer manejo adequado para maximizar produção.'
            }
        }
    }

    # Select box para escolher a planta
    selected_plant = st.sidebar.selectbox('Selecione uma planta:', list(plant_descriptions.keys()))

    image_path = format_filename(selected_plant)


    # Exibe a imagem da planta selecionada
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, caption=selected_plant, width=590)
    else:
        st.warning('Imagem não encontrada para essa planta.')

# Usando a função st.markdown com o parâmetro correto
    st.markdown(f"""<div style="text-align: center;"><h2>{selected_plant}</h2><p>{plant_descriptions[selected_plant]['descricao']}</p></div>""", unsafe_allow_html=True)

    # Adiciona a tabela com informações adicionais
    st.markdown("<h3>Informações Adicionais:</h3>", unsafe_allow_html=True)

    # Criação da tabela de informações adicionais (somente descrição)
    st.dataframe(pd.DataFrame.from_dict(plant_descriptions[selected_plant]['variaveis'], orient='index', columns=['Descrição']))






# Função para gerar o nome do arquivo corretamente
def format_filename(plant_name):
    # Remove caracteres especiais e mantém apenas letras, números e hífens
    formatted_name = re.sub(r'[^a-zA-Z0-9-]+', '-', plant_name).strip('-').lower()
    return f'static/plants/{formatted_name}.jpg'



logo()
page_to_funcs = {
    'Página Inicial': intro,
    'Análise Exploratória': page_eda,
    'Conhecimento das Plantas': page_conhecimento_plantas,
    'Classificação de pastagens (Predição)': page_run_model,
    'Teoria do modelo escolhido': exibir_teoria_do_modelo
}
# criando um sidebar
st.sidebar.title('Menu')

page = st.sidebar.selectbox('Selecione a página', list(page_to_funcs.keys()))
st.sidebar.markdown('---')
page_to_funcs[page]()





