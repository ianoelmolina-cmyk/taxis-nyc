import streamlit as st

st.set_page_config(page_title="Taxis NYC", layout="wide")

pagina_pronostico = st.Page("paginas/pronostico.py", title="Pronóstico", icon=":material/insights:")
pagina_segmentacion = st.Page("paginas/segmentacion.py", title="Segmentación zonas", icon=":material/scatter_plot:")

pg = st.navigation({"Planificar": [pagina_pronostico],
                    "Entender": [pagina_segmentacion]
                    })

with st.sidebar:
    st.title("Taxis NYC")



pg.run()