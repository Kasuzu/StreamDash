
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Función para cargar los datos
@st.cache_data  # Actualizado según la nueva política de caché de Streamlit
def cargar_datos():
    datos = pd.read_csv('Datos_Nar.csv')
    return datos

# Carga los datos
datos = cargar_datos()

# Configuración del título y descripción del aplicativo
st.title('Aplicativo Interactivo de Visualización de Datos de la Gobernación de Nariño')
st.write('Este aplicativo muestra estadísticas globales, permite seleccionar una dependencia para explorar sus interacciones específicas y generar gráficas personalizadas.')

# Dividir la pantalla en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader('Estadísticas Generales')
    resumen_municipios = datos.groupby('Municipios').Genero.value_counts().unstack().fillna(0).astype(int)
    resumen_municipios['Total'] = resumen_municipios.sum(axis=1).astype(int)
    st.table(resumen_municipios)

with col2:
    st.subheader('Exploración por Dependencia')
    dependencia_seleccionada = st.selectbox('Selecciona una Dependencia:', datos['Dependencias'].unique())
    total_beneficiados = datos[datos['Dependencias'] == dependencia_seleccionada].shape[0]
    st.markdown(f'**La {dependencia_seleccionada} ha beneficiado a {total_beneficiados} personas.**')

    datos_por_dependencia = datos[datos['Dependencias'] == dependencia_seleccionada]
    municipios_alcanzados = datos_por_dependencia['Municipios'].unique()
    municipios_no_alcanzados = set(datos['Municipios'].unique()) - set(municipios_alcanzados)
    st.write(f'Municipios alcanzados: {len(municipios_alcanzados)}')
    with st.expander("Ver detalles de municipios alcanzados"):
        st.table(pd.DataFrame(municipios_alcanzados, columns=['Municipios Alcanzados']))
    st.write(f'Municipios no alcanzados: {len(municipios_no_alcanzados)}')
    with st.expander("Ver detalles de municipios no alcanzados"):
        st.table(pd.DataFrame(sorted(municipios_no_alcanzados), columns=['Municipios No Alcanzados']))

    st.subheader('Genera tu Gráfica')
    tipo_grafica = st.selectbox('Selecciona el tipo de gráfica:', ['Barras', 'Histograma', 'Líneas'])
    columna_datos = st.selectbox('Selecciona el dato para graficar:', datos.columns)
    boton_generar = st.button('Generar Gráfica')

    if boton_generar:
        fig, ax = plt.subplots()
        if tipo_grafica == 'Barras':
            sns.countplot(x=columna_datos, data=datos, palette='pastel', ax=ax)
        elif tipo_grafica == 'Histograma':
            sns.histplot(datos[columna_datos], kde=True, bins=20, color='skyblue', ax=ax)
        elif tipo_grafica == 'Líneas':
            sns.lineplot(data=datos, x=datos.index, y=columna_datos, ax=ax)
        st.pyplot(fig)
