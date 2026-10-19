import streamlit as st

st.set_page_config(page_title="Taxis NYC", layout="wide")

pagina_pronostico = st.Page("paginas/pronostico.py", title="Pronóstico", icon=":material/insights:")

pg = st.navigation({"Planificar": [pagina_pronostico]})

with st.sidebar:
    st.title("Taxis NYC")

pg.run()