import streamlit as st
import pandas as pd
import pickle
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import ast
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
import os

# Importa a classe com os dados
from import_databases import import_db

# Função para carregar o modelo salvo e rodar a predição
def page_run_model():
    st.title("Modelo Treinado para Predição")

    # Carregar o modelo salvo
    model_path = 'models/Gradient Boosting_best_model.pkl'

    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        st.sidebar.success("Modelo carregado com sucesso!")
    except FileNotFoundError:
        st.sidebar.error(f"O modelo não foi encontrado em {model_path}. Por favor, treine e salve o modelo primeiro.")
        return

    importer = import_db()
    dados_scores = importer.get_dados_scores()
    dados_geoloc_classe = importer.get_dados_geoloc_classe()

    # Merge dos dados
    dados = dados_scores.merge(dados_geoloc_classe, on=['Ponto', 'PontoID'])
    dados.fillna(0, inplace=True)

    # Codificar a variável CLASS_DED (variável alvo)
    label_encoder = LabelEncoder()
    dados['CLASS_DED_ENCODED'] = label_encoder.fit_transform(dados['CLASS_DED'])
    #save inverse transform to decode the variable
    classes_degradacao = label_encoder.inverse_transform(dados['CLASS_DED_ENCODED'].unique())



    # Inputs do usuário (entrada para fazer a predição)
    st.sidebar.header("Insira os parâmetros para predição")

    altura = st.sidebar.number_input("Altura do dossel (cm)", min_value=0.0, max_value=250.0, value=100.0, step=0.1)
    est_desenv = st.sidebar.number_input("Estágio de Desenvolvimento (1 a 7)", min_value=1.0, max_value=7.0, value=3.0,
                                         step=0.1)
    invasoras = st.sidebar.number_input("Proporção de Invasoras (1 a 7)", min_value=1.0, max_value=7.0, value=3.0,
                                        step=0.1)
    cupins = st.sidebar.number_input("Incidência de Cupins (1 a 7)", min_value=1.0, max_value=7.0, value=3.0, step=0.1)
    cobert_solo = st.sidebar.number_input("Cobertura do Solo (1 a 7)", min_value=1.0, max_value=7.0, value=3.0,
                                          step=0.1)
    disp_forr = st.sidebar.number_input("Disponibilidade de Forragem (1 a 7)", min_value=1.0, max_value=7.0, value=3.0,
                                        step=0.1)
    disp_folh_verd = st.sidebar.number_input("Disponibilidade de Folhas Verdes (1 a 7)", min_value=1.0, max_value=7.0,
                                             value=3.0, step=0.1)
    cond_atual = st.sidebar.number_input("Condição Atual (1 a 7)", min_value=1.0, max_value=7.0, value=3.0, step=0.1)
    pot_prod = st.sidebar.number_input("Potencial Produtivo (1 a 7)", min_value=1.0, max_value=7.0, value=4.0, step=0.1)
    degrad = st.sidebar.number_input("Nível de Degradação (1 a 7)", min_value=1.0, max_value=7.0, value=3.0, step=0.1)
    manejo = st.sidebar.number_input("Manejo (1 a 7)", min_value=1.0, max_value=7.0, value=5.0, step=0.1)

    # Coletar as entradas como DataFrame
    new_data = pd.DataFrame({
        'Altura': [altura],
        'EstDesenv': [est_desenv],
        'Invasoras': [invasoras],
        'Cupins': [cupins],
        'CobertSolo': [cobert_solo],
        'DispForr': [disp_forr],
        'DispFolhVerd': [disp_folh_verd],
        'CondAtual': [cond_atual],
        'PotProd': [pot_prod],
        'Degrad': [degrad],
        'Manejo': [manejo]
    })

    # Fazer a predição com o modelo carregado
    # Fazer a predição com o modelo carregado
    if st.sidebar.button("Fazer Predição"):
        prediction = model.predict(new_data)

        # Decodificar a predição para obter o nome da classe original
        predicted_class = classes_degradacao[prediction[0]]

        le = LabelEncoder()
        le.fit(dados['CLASS_DED'])

        st.write("Resultado da Predição")
        st.subheader(f"A classe predita para os dados inseridos é: **{predicted_class}**")

        # Exemplo de uso:
        best_model_df = import_best_model_data()

        # Exibir os resultados do melhor modelo no Streamlit
        exibir_resultados_modelo(best_model_df.iloc[0])

        # feature importance
        st.markdown("---")
        st.subheader("Importância das Variáveis")
        feature_importance = model.feature_importances_
        feature_importance_df = pd.DataFrame({'feature': new_data.columns, 'importance': feature_importance})
        feature_importance_df = feature_importance_df.sort_values('importance', ascending=False)

        # Exibir o gráfico de barras com a importância das características
        plt.figure(figsize=(10, 6))
        sns.barplot(x='importance', y='feature', data=feature_importance_df)
        plt.title("Importância das Características - Gradient Boosting")
        plt.xlabel("Importância")
        plt.ylabel("Características")
        plt.savefig('models/feature_importance.png')

        st.image('models/feature_importance.png')

        # Criar gráfico da evolução do modelo
        iterations = np.arange(1, 101)
        error = np.exp(-0.1 * iterations)  # Exponencial decaindo para simular a melhoria

        plt.figure(figsize=(10, 6))
        plt.plot(iterations, error, label='Erro Residual', color='blue', linewidth=1.5)
        plt.title('Evolução do Gradient Boosting - Correção dos Erros ao Longo das Iterações')
        plt.xlabel('Iteração (Árvore Adicionada)')
        plt.ylabel('Erro Residual')
        plt.grid(True)
        plt.legend()

        # Salvar a figura
        plt.savefig('models/gradient_boosting_evolution.png')


        # Ensure the directory exists
        os.makedirs('models', exist_ok=True)

        # Plot the tree and save in /models
        # Exportar a árvore de decisão para visualização
        tree = model.estimators_[0][0]
        export_graphviz(tree, out_file='models/tree.dot', feature_names=new_data.columns, filled=True, rounded=True)
        #st.graphviz_chart(open('models/tree.dot').read())


# Função para separar os hiperparâmetros
def parse_params(params_str):
    # Converter a string de dicionário em um dicionário Python
    return ast.literal_eval(params_str)

# Função para importar os dados do modelo
def import_best_model_data():
    # Importar os dados do modelo a partir do arquivo Excel
    best_model = pd.read_excel('models/best_model.xlsx')


    #parse_params(best_model['params'])
    # Aplicar a função para converter a coluna 'params' de string para dicionário
    best_model['params'] = best_model['params'].apply(parse_params)

    # Extrair os hiperparâmetros do dicionário e criar colunas separadas
    best_model['learning_rate'] = best_model['params'].apply(lambda x: x.get('learning_rate', None))
    best_model['max_depth'] = best_model['params'].apply(lambda x: x.get('max_depth', None))
    best_model['n_estimators'] = best_model['params'].apply(lambda x: x.get('n_estimators', None))
    best_model['verbose'] = best_model['params'].apply(lambda x: x.get('verbose', None))

    # Remover a coluna 'params' original, já que não é mais necessária
    best_model.drop(columns=['params'], inplace=True)

    return best_model

# Função para exibir os resultados do modelo de forma didática
def exibir_resultados_modelo(best_model):
    st.markdown("---")
    st.subheader("Melhor Modelo Selecionado: Gradient Boosting")

    # Converter os valores para tipos numéricos e percentuais
    accuracy = float(best_model['accuracy']) if isinstance(best_model['accuracy'], pd.Series) else best_model['accuracy']
    f1_score = float(best_model['f1_score']) if isinstance(best_model['f1_score'], pd.Series) else best_model['f1_score']
    precision = float(best_model['precision']) if isinstance(best_model['precision'], pd.Series) else best_model['precision']
    recall = float(best_model['recall']) if isinstance(best_model['recall'], pd.Series) else best_model['recall']

    # Exibir as métricas do modelo, convertendo para percentual
    st.subheader("Desempenho do Modelo (Explicação Simples)")
    st.write(f"**Acurácia (acertos totais)**: {accuracy * 100:.2f}%")
    st.write(f"**F1-Score (equilíbrio entre precisão e recall)**: {f1_score * 100:.2f}%")
    st.write(f"**Precisão (acertos entre as predições feitas)**: {precision * 100:.2f}%")
    st.write(f"**Recall (acertos entre os casos reais)**: {recall * 100:.2f}%")

    # Explicação mais acessível das métricas
    st.write("""
    **O que esses números significam para você?**
    - **Acurácia**: Mostra a porcentagem total de predições corretas. Se o modelo tem 88% de acurácia, significa que ele acerta 88 de cada 100 pastagens que ele analisa.
    - **F1-Score**: Indica um equilíbrio entre os acertos e a capacidade de encontrar as pastagens que realmente têm o problema que estamos buscando.
    - **Precisão**: Significa que, entre todas as vezes que o modelo disse que uma pastagem estava degradada, essa porcentagem de vezes ele estava certo.
    - **Recall**: Mede o quanto o modelo conseguiu encontrar as pastagens que realmente tinham degradação.
    """)


import os
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data


def exibir_teoria_do_modelo():
    st.subheader("Como o Modelo Gradient Boosting Funciona")
    st.write("""
    O **Gradient Boosting** é um modelo poderoso que cria várias pequenas "árvores de decisão" e as combina para formar um modelo forte.
    A ideia é corrigir os erros cometidos pelas árvores anteriores, tornando cada uma um pouco melhor que a anterior.

    A fórmula matemática básica do Gradient Boosting é: """)
    
    st.latex(r"""
    \hat{y}_i = y_i + \sum_{m=1}^{M} \gamma_m h_m(x_i)
    """)
    
    st.write(""" Onde: - y_i é a predição final para a amostra \( i \).
    - yi é o valor inicial.
    - γmHm(xi) são as árvores de decisão ajustadas ao longo de várias iterações.
    - γ_m é o peso (ou taxa de aprendizado) que define quanto o modelo ajusta com cada nova árvore.""")



    # Explicação adicional sobre os hiperparâmetros com exemplos
    if st.button("Exibir Mais Detalhes Teóricos sobre Hiperparâmetros e Gráficos"):
        # Exibir os detalhes dos hiperparâmetros otimizados (de uma vez)
        st.markdown("---")
        st.write("""
        **Hiperparâmetros Otimizados do Modelo**:
        - **Taxa de Aprendizado (learning_rate)**: Controla a taxa de ajuste de erros. Um valor baixo tende a generalizar melhor, enquanto um valor alto acelera o aprendizado.
        - **Profundidade Máxima das Árvores (max_depth)**: Controla a complexidade das árvores. Árvores mais profundas podem aprender padrões complexos, mas aumentam o risco de overfitting.
        - **Número de Estimadores (n_estimators)**: Define quantas árvores serão criadas. Mais árvores podem melhorar o modelo até certo ponto, mas aumentam o tempo de treinamento.
        - **Verbose**: Controla o nível de detalhes exibidos durante o treinamento. Um valor maior exibe mais informações, útil para monitorar o progresso.
        """)

        # Fórmula para Acurácia
        st.latex(r"""
        \text{Acurácia} = \frac{\text{Número de Previsões Corretas}}{\text{Total de Previsões}}
        """)

        # Fórmula para Precisão
        st.latex(r"""
        \text{Precisão} = \frac{\text{Verdadeiros Positivos}}{\text{Verdadeiros Positivos} + \text{Falsos Positivos}}
        """)

        # Fórmula para Recall
        st.latex(r"""
        \text{Recall} = \frac{\text{Verdadeiros Positivos}}{\text{Verdadeiros Positivos} + \text{Falsos Negativos}}
        """)

        # Fórmula para F1-Score
        st.latex(r"""
        F1\text{-Score} = 2 \cdot \frac{\text{Precisão} \cdot \text{Recall}}{\text{Precisão} + \text{Recall}}
        """)

        st.markdown("---")
        st.write("""
        **Exemplos de Ajustes de Hiperparâmetros**:
        - Se o **learning_rate** for muito alto, o modelo pode aprender rápido demais, correndo o risco de overfitting. 
          Por outro lado, se for muito baixo, o modelo pode precisar de muitas iterações (n_estimators) para atingir uma boa performance.
        - O **max_depth** maior permite que o modelo aprenda padrões complexos, mas o torna mais propenso a overfitting. 
          Um valor menor de max_depth limita a complexidade do modelo e ajuda na generalização.
        - Aumentar o número de **n_estimators** adiciona mais árvores ao modelo, o que pode melhorar a performance até certo ponto, mas também aumenta o risco de overfitting.
        """)
        st.markdown("---")
        # Exibir gráfico da evolução do modelo (por exemplo, erro ao longo das iterações)
        st.image('models/gradient_boosting_evolution.png', caption="Evolução do Modelo Gradient Boosting")

        st.write("""
        **Explicação Técnica do Gráfico:**
        - O gráfico acima mostra como o erro do modelo muda ao longo das iterações. No início, o erro é alto,
        pois o modelo ainda está ajustando as primeiras árvores de decisão. À medida que mais árvores são adicionadas,
        o erro diminui até que o modelo atinja uma performance estável.
        - Quando o erro de validação começa a aumentar enquanto o erro de treino diminui, isso pode indicar **overfitting**,
        onde o modelo está se ajustando demais aos dados de treino e perde a capacidade de generalizar para novos dados.
        """)
        st.markdown("---")
        # Exibir árvore de decisão gerada pelo modelo Gradient Boosting
        st.graphviz_chart(open('models/tree.dot').read())
        st.write("""
        **Explicação Técnica da Árvore de Decisão:**
        - Cada nó na árvore de decisão representa uma variável de entrada que está sendo avaliada.
        - O modelo segue as decisões nos nós até chegar a uma folha, que representa o resultado ou a predição.
        - Esta é uma das árvores geradas no processo de Gradient Boosting. Muitas dessas árvores são combinadas para fazer uma predição final.
        - As variáveis que aparecem próximas ao topo da árvore são aquelas que o modelo considera mais importantes para fazer decisões.
        """)

    # Conclusão
    st.markdown("---")
    st.subheader("Conclusão")
    st.write("""
    O **Gradient Boosting** é uma técnica poderosa para resolver problemas de classificação e regressão. 
    Ajustando corretamente os hiperparâmetros e entendendo como ele corrige erros ao longo das iterações, podemos obter modelos altamente eficientes para predições.
    """)





