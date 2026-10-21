import streamlit as st

st.set_page_config(page_title="Taxis NYC", layout="wide")

pagina_pronostico = st.Page("paginas/pronostico.py", title="Pronóstico", icon=":material/insights:")
pagina_segmentacion = st.Page("paginas/segmentacion.py", title="Segmentación zonas", icon=":material/scatter_plot:")
pagina_decision = st.Page("paginas/decision.py", title="Decisión", icon=":material/hub:")
pagina_ficha = st.Page("paginas/ficha.py", title="Ficha", icon=":material/description:")

pg = st.navigation({"Planificar": [pagina_pronostico, pagina_decision],
                    "Entender": [pagina_segmentacion, pagina_ficha]
                    })

with st.sidebar:
    st.title("Taxis NYC")



pg.run()