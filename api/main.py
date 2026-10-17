from fastapi import FastAPI

app = FastAPI(title="Taxis NYC API")


@app.get("/")
def raiz():
    return {
        "estado": "ok",
        "mensaje": "API de pronóstico de demanda de taxis amarillos en NYC",
    }


@app.get("/info")
def info():
    # Datos de prueba: más adelante vendrán de los archivos que guarde el notebook
    return {
        "zonas": [
            {"id": 161, "nombre": "Midtown Center", "distrito": "Manhattan"},
            {"id": 132, "nombre": "JFK Airport", "distrito": "Queens"},
        ],
        "fechas": [
            "2024-01-25", "2024-01-26", "2024-01-27", "2024-01-28",
            "2024-01-29", "2024-01-30", "2024-01-31", "2024-02-01",
        ],
        "cuantiles": ["p10", "p20", "p30", "p40", "p50", "p60", "p70", "p80", "p90"],
    }