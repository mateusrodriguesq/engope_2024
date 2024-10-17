# Importações necessárias
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import os
import pickle
from sklearn.tree import export_graphviz

# Importa a classe com os dados
from import_databases import import_db

# Função principal da página de classificação
def page_classifier():
    st.title('Análise de Classificação e Modelagem com Busca de Hiperparâmetros')

    # Explicação no sidebar de como funciona esta aba
    st.sidebar.write("Nesta aba, vamos treinar e avaliar modelos de classificação para prever a degradação da pastagem.")
    st.sidebar.write("Os modelos serão treinados com diferentes tamanhos de conjunto de teste e hiperparâmetros.")
    st.sidebar.write("O melhor modelo será salvo e exibido com suas métricas de avaliação.")

    # Botão para rodar o processo de modelagem
    st.sidebar.error("Este processo pode demorar diversos minutos e a página performar lentamente por um tempo, como o projeto já vem com o modelo pré-definido não é recomendado executar o comando.")
    if st.sidebar.button("Clique para rodar a Análise de Classificação e Modelagem com Busca de Hiperparâmetros"):
        st.warning("Aguarde, o processo pode demorar alguns minutos...")
        models_start()

# Função que executa o processo de avaliação de modelos
def models_start():
    # Carregar os dados
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


    # Divisão dos dados
    X = dados[['Altura', 'EstDesenv', 'Invasoras', 'Cupins', 'CobertSolo', 'DispForr', 'DispFolhVerd', 'CondAtual', 'PotProd', 'Degrad', 'Manejo']]
    y = dados['CLASS_DED_ENCODED']  # Variável alvo codificada

    # Test sizes que vamos variar
    test_sizes = [0.2, 0.25, 0.3, 0.35]

    # Hiperparâmetros do Gradient Boosting a serem testados
    param_grid_gradient_boosting = {
        'n_estimators': [50, 100, 200, 500],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 10],
        'verbose': [0, 1]
    }

    # Função para avaliar o modelo e salvar os resultados
    def avaliar_modelo_grid(modelo, nome_modelo, param_grid, X_train, y_train, X_test, y_test):
        grid = GridSearchCV(modelo, param_grid, cv=5, n_jobs=-1, verbose=1)
        grid.fit(X_train, y_train)
        y_pred = grid.best_estimator_.predict(X_test)

        # Avaliação com métricas de classificação
        accuracy = accuracy_score(y_test, y_pred)
        f1 = classification_report(y_test, y_pred, output_dict=True)['weighted avg']['f1-score']
        precision = classification_report(y_test, y_pred, output_dict=True)['weighted avg']['precision']
        recall = classification_report(y_test, y_pred, output_dict=True)['weighted avg']['recall']

        st.write(f"**{nome_modelo}** com melhores hiperparâmetros: {grid.best_params_}")
        st.write(f"Acurácia: {accuracy:.2f}")
        st.write(f"F1-Score: {f1:.2f}")
        st.write(f"Precisão: {precision:.2f}")
        st.write(f"Recall: {recall:.2f}")

        # Relatório detalhado (precision, recall, f1-score)
        st.write("**Relatório de Classificação Completo**")
        st.text(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

        # Matriz de confusão
        fig, ax = plt.subplots()
        ax.set_title(f"Matriz de Confusão - {nome_modelo}\nAcurácia: {accuracy:.2f}")
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap="YlGnBu", ax=ax,
                    xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        ax.set_xlabel("Predito")
        ax.set_ylabel("Verdadeiro")
        st.pyplot(fig)

        # Criar uma string simplificada para os hiperparâmetros no nome do arquivo
        formatted_params = "_".join([f"{key}-{value}" for key, value in grid.best_params_.items()])

        # Nome do arquivo sem caracteres especiais
        filename = f"models_graph/confusion_matrix_{nome_modelo}_acc-{accuracy:.2f}_params-{formatted_params}.png"

        # Salvar a imagem da matriz de confusão
        os.makedirs('models_graph', exist_ok=True)
        fig.savefig(filename)
        st.success(f"Matriz de Confusão salva: {filename}")

        # Salvar o melhor modelo com pickle
        model_filename = f'models/{nome_modelo}_best_model.pkl'
        os.makedirs('models', exist_ok=True)
        with open(model_filename, 'wb') as file:
            pickle.dump(grid.best_estimator_, file)
        st.success(f"Melhor modelo salvo como: {model_filename}")



        return {
            'nome_modelo': nome_modelo,
            'accuracy': accuracy,
            'f1_score': f1,
            'precision': precision,
            'recall': recall,
            'params': grid.best_params_
        }

    # Rodar o processo de avaliação dos modelos e selecionar o melhor
    best_model = None
    best_score = 0

    for test_size in test_sizes:
        st.write(f"### Testando com test_size = {test_size}")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        # Gradient Boosting
        grad_boost = GradientBoostingClassifier()
        result = avaliar_modelo_grid(grad_boost, "Gradient Boosting", param_grid_gradient_boosting, X_train, y_train, X_test, y_test)

        # Comparar para selecionar o melhor modelo
        if result['accuracy'] > best_score:
            best_score = result['accuracy']
            best_model = result

    # Exibir o melhor modelo
    st.write("### Melhor Modelo")
    st.write(f"**{best_model['nome_modelo']}** com acurácia de {best_model['accuracy']:.2f}")
    st.write(f"**F1-Score:** {best_model['f1_score']:.2f}")
    st.write(f"**Precisão:** {best_model['precision']:.2f}")
    st.write(f"**Recall:** {best_model['recall']:.2f}")
    st.write(f"**Melhores Hiperparâmetros:** {best_model['params']}")

    # Salve todas as informações do modelo em um dataframe e salve em xlsx
    df = pd.DataFrame([best_model])
    df.to_excel('models/best_model.xlsx', index=False)

    # Exibir a matriz de confusão do melhor modelo
    st.image(f"models_graph/confusion_matrix_{best_model['nome_modelo']}_acc-{best_model['accuracy']:.2f}_params-{'_'.join([f'{key}-{value}' for key, value in best_model['params'].items()])}.png")


