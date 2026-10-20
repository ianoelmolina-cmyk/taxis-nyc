import requests
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data(ttl=3600)
def llamar_api(ruta, **params):
    r = requests.get(f"{st.secrets['API_URL']}{ruta}", params=params, timeout=90)
    r.raise_for_status()
    return r.json()


st.title("Decisión: ¿Cuántos taxis enviar?")

try:
    with st.status("Conectando con la API...") as estado:
        info = llamar_api("/info")
        estado.update(label="API conectada", state="complete")
except requests.RequestException as e:
    st.error("Lo lamentamos! No hemos podido ejecutar tu consulta")       # tu mensaje para la gerente
    st.caption(f"Detalle: {e}")
    st.stop()

@st.fragment
def decision():
    
    # 1. Selectores de zona y fecha. Selectores, armados con lo que devolvió /info

    zonas = {z["id"]: f'{z["nombre"]} ({z["distrito"]})' for z in info["zonas"]}
    zona_id = st.selectbox("Zona", options=list(zonas.keys()), format_func=lambda i: zonas[i])
    fecha = st.segmented_control("Fecha", info["fechas"], default=info["fechas"][0])

    if not fecha:
        st.stop()

    # 2. Los dos costos
    c_ocioso = st.slider("Costo de un taxi sin pasajero durante una hora (USD)", 1, 100, 10)
    c_perdido = st.slider("Costo de un pasajero que no encontró taxi (USD)", 1, 200, 40)

    # 3. Cuantil óptimo
    q = c_perdido / (c_ocioso + c_perdido)
    nivel = min(max(round(q, 1), 0.1), 0.9)      # el más cercano de los que da la API
    col = f"p{int(nivel * 100)}"

    st.info(
        f"Perder un pasajero cuesta {c_perdido / c_ocioso:.1f} veces lo que cuesta un taxi ocioso, "
        f"así que conviene cubrir el {nivel:.0%} de la demanda posible y enviar el pronóstico {col}."
    )
    # 4. Pedir /pronostico y armar la tabla (igual que en Pronóstico, sacando la columna `col`)

    
    try:
        datos = llamar_api("/pronostico", zona_id=zona_id, fecha=fecha)
    except requests.RequestException as e:
        st.error("No pudimos obtener el pronóstico para esa zona y fecha. Prueba con otra combinación.")
        st.caption(f"Detalle: {e}")
        st.stop()

    #De la respuesta a una tabla
    df = pd.DataFrame(datos["horas"])
    df[col] = df["cuantiles"].apply(lambda cuantiles: cuantiles[col])
    df["p50"] = df["cuantiles"].apply(lambda cuantiles: cuantiles["p50"])

    st.bar_chart(df.set_index("hora")[[col, "p50"]])

    # 5. Costo de cada regla, solo si hay datos reales
    def costo(enviados, real):
        return (np.maximum(enviados - real, 0) * c_ocioso + np.maximum(real - enviados, 0) * c_perdido).sum()

    if df["real"].notna().all():
        costo_recomend = costo(df[col], df["real"])
        costo_p50 = costo(df["p50"], df["real"])
        costo_semanal = costo(df["hace_una_semana"], df["real"])
        base = max(costo_recomend, 1)

        # 6. Tres st.metric (recomendación, p50 y "hace una semana"), con delta_color="inverse"
        st.subheader("Si este día se decide así, el costo podría ser:")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Recomendación ({col})", f"${costo_recomend:,.0f}", border=True)
        c2.metric("Enviar el pronóstico central (p50)", f"${costo_p50:,.0f}", delta=f"{costo_p50/base -1:+.0%} vs la recomendación", 
                  delta_color="inverse", border=True)
        c3.metric("Enviar lo de hace una semana", f"${costo_semanal:,.0f}", delta=f"{costo_semanal/base -1:+.0%} vs la recomendación",
                  delta_color="inverse", border=True)
    else:
        st.info("Esto es un pronóstico dado para el día futuro y no tiene datos reales, así que no se puede comparar el costo,")


    # 7. st.download_button con el plan en CSV

    plan = pd.DataFrame({"hora": df["hora"], "taxis_recomendados": df[col].round().astype(int)})
    st.download_button("Dercargar el plan de taxis por hora", plan.to_csv(index=False),
                       file_name=f"plan_taxis_{zona_id}_{fecha}.csv", mime="text/csv")

decision()