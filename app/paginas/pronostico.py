import requests
import streamlit as st

@st.cache_data(ttl=3600)
def llamar_api(ruta, **params):
    r = requests.get(f"{st.secrets['API_URL']}{ruta}", params=params, timeout=90)
    r.raise_for_status()
    return r.json()


st.title("Pronóstico de demanda")

try:
    with st.status("Conectando con la API...") as estado:
        info = llamar_api("/info")
        estado.update(label="API conectada", state="complete")
except requests.RequestException as e:
    st.error("Lo lamentamos! No hemos podido ejecutar tu consulta")       # tu mensaje para la gerente
    st.caption(f"Detalle: {e}")
    st.stop()

