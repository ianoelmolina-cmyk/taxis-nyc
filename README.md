# Planificacion de taxis nyc
- Estudiante: 'Noel Amilcar Molina Campos'
- Descripcion: 'El modelo pronostica viajes por hora en cada zona con rango de incertidumbre, y la app agrupa las zonas por tipo de uso. El modelo sirve para ayudar con la gestion y planificacion de operaciones de los taxis amarillos en la ciudad de Nueva York, siendo capaz de determinar cuantos taxis deberán operar por esos tipo de zona y horario'
- Entrenamiento: 'El entrenamiento fue realizado con datos historicos de operaciones anteriores en la ciudad NYC'

## Despliegue

### Versión publicada
- **API (Render):** <https://taxis-nyc-api.onrender.com/docs>. Si estaba inactiva, puede tardar cerca de un minuto en responder.
- **App (Streamlit):** <https://taxis-nyc-seppcspqfvxszqbtulds8m.streamlit.app>

### Correr el proyecto en local
1. Clonar el repositorio: `git clone https://github.com/ianoelmolina-cmyk/taxis-nyc.git`
2. Crear y activar un entorno virtual: `python -m venv .venv` y activarlo:
    - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
    - Mac/Linux: `source .venv/bin/activate`
3. Instalar las librerías de la API y de la app: `pip install -r api/requirements.txt` y `pip install -r app/requirements.txt`
4. Levantar la API (desde la carpeta `api`): `cd api` y luego `python -m uvicorn main:app --reload`
   (queda en `http://localhost:8000/docs`)
5. Crear `app/.streamlit/secrets.toml` con `API_URL = "http://localhost:8000"`
6. Levantar la app, en **otra terminal** con el entorno activado: `cd app` y luego `streamlit run streamlit_app.py`