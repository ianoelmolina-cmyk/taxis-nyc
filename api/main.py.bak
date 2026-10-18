from datetime import date
import numpy as np
import pandas as pd
import xgboost as xgb
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Taxis NYC API")

VARIABLES = ["lag_24", "lag_48", "lag_167", "lag_168", "lag_169", "media_dia_ant", "hora_dia","dia_semana", "feriado", "zona"]
CUANTILES = ["p10", "p20", "p30", "p40", "p50", "p60", "p70", "p80", "p90"]
#0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9

# Se cargan UNA vez, al arrancar
modelo = xgb.XGBRegressor()
modelo.load_model("modelo_pronostico.ubj")
demanda = pd.read_parquet("demanda.parquet")
zonas = pd.read_csv("zonas.csv")

CATEGORIAS = np.array(sorted(zonas["LocationID"]), dtype="int64")
demanda["zona"] = pd.Categorical(demanda["PULocationID"], categories=CATEGORIAS)


@app.get("/")
def raiz():
    return {
        "estado": "ok",
        "mensaje": "API de pronóstico de demanda de taxis amarillos en NYC",
    }


@app.get("/info")
def info():

    lista_zonas = (
        zonas[["LocationID","Zone", "Borough"]].rename(columns={"LocationID": "id" , "Zone": "nombre", "Borough": "distrito"}).to_dict("records")
    )

    return {
        "zonas": lista_zonas,      # una lista de {"id", "nombre", "distrito"} desde 'zonas'
        "fechas": demanda["hora"].dt.date.unique().astype(str).tolist(),     # las fechas distintas de demanda["hora"], como texto
        "cuantiles": CUANTILES,
    }


@app.get("/pronostico")
def pronostico(zona_id: int, fecha: date):
    filas = demanda[ (demanda["PULocationID"]==zona_id) & (demanda["hora"].dt.date == fecha) ]
    if filas.empty:
        raise HTTPException(status_code=404, detail="No se encontraron registros para mostrar")

    pred = np.sort(modelo.predict(filas[VARIABLES]), axis=1)

    zona_fila = zonas[ zonas["LocationID"] == zona_id ].iloc[0]

    horas = []
    for i, (_, fila) in enumerate(filas.iterrows()):
        horas.append({
            "hora": int(fila["hora_dia"]),
            "real": None if pd.isna(fila["viajes"]) else int(fila["viajes"]),   #fila["real"],
            "hace_una_semana": float(fila["lag_168"]),
            "cuantiles": {c: float(pred[i, j]) for j, c in enumerate(CUANTILES) },
        })
    return {"zona": {"id": zona_id, "nombre":zona_fila["Zone"] , "distrito":zona_fila["Borough"]}, 
            "fecha": str(fecha), 
            "horas": horas}