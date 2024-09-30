import streamlit as st
import pandas as pd
import plotly.express as px

# Título del tablero
st.title("Dashboard Financiero Interactivo")

# Cargar datos desde GitHub
url = "https://raw.githubusercontent.com/tonahp/dfclean/refs/heads/main/df_clean.csv"
df = pd.read_csv(url)

# Renombrar columnas para que coincidan con lo solicitado
df.rename(columns={
    'Company_ID': 'Compañía', 
    'Total_Revenue': 'Totales', 
    'Short_Term_Debt': 'Deudas a Corto Plazo',
    'Long_Term_Debt': 'Deudas a Largo Plazo',
    'Current_Assets': 'Activos Circulantes',
    'Current_Liabilities': 'Pasivos Circulantes',
    'Equity': 'Patrimonio Neto',
    'Financial_Expenses': 'Gastos Financieros',
    'Current_Ratio': 'Ratio Actual',
    'Debt_to_Equity_Ratio': 'Ratio Deuda Capital',
    'Interest_Coverage_Ratio': 'Ratio Cobertura de Interés',
    'Industry': 'Industria',
    'Country': 'País',
    'Company_Size': 'Tamaño de Compañía'
}, inplace=True)

# Cálculo de los indicadores financieros
df['Ratio de Liquidez'] = df['Activos Circulantes'] / df['Pasivos Circulantes']
df['Deuda Total'] = df['Deudas a Corto Plazo'] + df['Deudas a Largo Plazo']
df['Ratio de Deuda a Patrimonio'] = df['Deuda Total'] / df['Patrimonio Neto']
df['Cobertura de Gastos Financieros'] = df['Totales'] / df['Gastos Financieros']

# Filtros interactivos
st.sidebar.header("Filtrar datos:")
empresa_seleccionada = st.sidebar.multiselect("Seleccionar Compañía", options=df["Compañía"].unique())
industria_seleccionada = st.sidebar.multiselect("Seleccionar Industria", options=df["Industria"].unique())
pais_seleccionado = st.sidebar.multiselect("Seleccionar País", options=df["País"].unique())

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df.copy()

if empresa_seleccionada:
    df_filtrado = df_filtrado[df_filtrado["Compañía"].isin(empresa_seleccionada)]

if industria_seleccionada:
    df_filtrado = df_filtrado[df_filtrado["Industria"].isin(industria_seleccionada)]

if pais_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(pais_seleccionado)]

# Visualización de gráficos
st.subheader("Visualización de Ratios Financieros")

# Gráfico de barras de los ratios financieros
st.write("Comparación de ratios entre las empresas seleccionadas")
fig = px.bar(df_filtrado, x='Compañía', y=['Ratio de Liquidez', 'Ratio de Deuda a Patrimonio', 'Cobertura de Gastos Financieros'],
             barmode='group', title='Ratios Financieros por Compañía')
st.plotly_chart(fig)

# Gráfico circular de la distribución de empresas por industria
st.write("Distribución por Industria")
fig_industria = px.pie(df_filtrado, names='Industria', title="Distribución de Compañías por Industria")
st.plotly_chart(fig_industria)

# Gráfico de líneas de evolución del ratio de liquidez
st.write("Evolución del Ratio de Liquidez")
fig_linea = px.line(df_filtrado, x='Compañía', y='Ratio de Liquidez', title="Evolución del Ratio de Liquidez")
st.plotly_chart(fig_linea)

# Mostrar tabla con los ratios calculados
st.subheader("Tabla de Ratios Financieros")
st.dataframe(df_filtrado[['Compañía', 'Ratio de Liquidez', 'Ratio de Deuda a Patrimonio', 'Cobertura de Gastos Financieros']])

# Integración opcional con ChatGPT
import requests

def chatgpt_query(prompt):
    api_key = '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'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        return answer
    else:
        return "Error en la consulta a ChatGPT."

# Integración en el dashboard
st.header("Preguntas sobre los Ratios Financieros")
user_question = st.text_input("Haz una pregunta sobre los datos:")
if st.button("Enviar"):
    if user_question:
        answer = chatgpt_query(user_question)
        st.write("Respuesta de ChatGPT:")
        st.write(answer)
