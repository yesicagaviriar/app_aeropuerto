import pandas as pd
import streamlit as st
import plotly.express as px

ruta ='https://github.com/juliandariogiraldoocampo/ia_taltech/raw/refs/heads/main/aeropuerto/data_sint_oper_pred_clas.csv'

df = pd.read_csv(ruta)

#****Analisis y procesamiento de datos****

df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
estadisticos = df_tipo_vuelo['count'].describe()
maximo = estadisticos['max']
minimo = estadisticos['min']
media = estadisticos['mean']

# TOP 5 AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
df_top5_ops_aeropuerto = df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_ops_aeropuerto.columns = ['AEROPUERTO_OPERACION', 'count']

# TOP 10 RUTAS CON MAYOR NÚMERO DE OPERACIONES
df['RUTA'] = df['ORIGEN'] + ' ▶ ' + df['DESTINO']
df_top10_rutas = df['RUTA'].value_counts().reset_index().head(10)
df_top10_rutas.columns = ['RUTA', 'count']



#****Configuración de la pagina***

st.set_page_config(
    page_title='Operaciones Acumuladas',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# # Ajuste del ancho máximo del contenedor principal a 1200 píxeles
st.markdown(
    '''
    <style>
        .block-container {
            max-width: 1200px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

paleta_barra = px.colors.qualitative.Antique

#****Visualización de datos****
st.image('encabezado.png')
st.title('Datos operaciones')

col1, col2, col3 = st.columns(3)

with col3:
    st.metric('Máximo', f'{maximo:.0f}', border=True)
with col1:
    st.metric('Mínimo', f'{minimo:.0f}', border=True)
with col2:
    st.metric('Media', f'{media:.0f}', border=True)


with st.expander('Ver Matriz de Datos'):
    st.dataframe(df)

with st.expander('Top 5 Aeropuertos con Mayor Número de Operaciones'):
    st.dataframe(df_top5_ops_aeropuerto)

with st.expander('Top 10 Rutas con Mayor Número de Operaciones'):
    st.dataframe(df_top10_rutas)

# DISEÑO DE 2 COLUMNAS PARA LAS GRÁFICAS DE BARRAS
col4, col5 = st.columns(2)

# ANÁLISIS DE LOS AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES

with col4:
    fig_barras = px.bar(
        df_top5_ops_aeropuerto,
        x='AEROPUERTO_OPERACION',
        y='count',
        title='Top 5 Aeropuertos con Mayor Número de Operaciones',
        labels={
            'AEROPUERTO_OPERACION': 'Aeropuerto',
             'count': 'Número de Operaciones'
            },
        color='AEROPUERTO_OPERACION',
        color_discrete_sequence=paleta_barra
        )
    fig_barras.update_layout(showlegend=False)

    #** mostrar la grafica de barras
    st.plotly_chart(fig_barras, use_container_width=True)

with col5:
# # ANÁLISIS DE RUTAS
    fig_rutas = px.bar(
        df_top10_rutas.sort_values('count', ascending=True),
        x='count',
        y='RUTA',
        orientation='h',
        title='TOP 10 RUTAS',
        labels={'count': 'Cantidad de Operaciones', 'RUTA': 'Rutas'},
        color='count',
        color_continuous_scale='tealgrn'
    )
    fig_rutas.update_layout(showlegend=False)
    st.plotly_chart(fig_rutas, use_container_width=True)