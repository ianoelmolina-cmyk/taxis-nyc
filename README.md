# Planificacion de taxis nyc
- Estudiante: 'Noel Amilcar Molina Campos'
- Descripción: 'el modelo pronostica los viajes por hora en cada zona, con un rango de incertidumbre. La app agrupa las zonas por tipo de uso, y calcula cuántos taxis enviar según los costos que fije el usuario.'
- Entrenamiento: 'El entrenamiento fue realizado con datos historicos de operaciones registradas en los días 1-24 de Enero de 2024 en la ciudad NYC'
- Prueba del modelo se realizó con los datos restantes del mes de Enero de 2024, es decir los datos de los días 25-31.

## Despliegue

### Carpetas
- /api en esta carpeta se encuentra la api, el modelo y los requirements de la api.
- /app en esta carpeta se encuentra la estructura de la app, la app y sus requirements.
- /app/paginas esta carpeta contiene las páginas visibles de la app.

### Versión publicada
- **API (Render):** <https://taxis-nyc-api.onrender.com/docs>. Si estaba inactiva, puede tardar cerca de un minuto en responder.
- **App (Streamlit):** <https://taxis-nyc-seppcspqfvxszqbtulds8m.streamlit.app>
- **Repositorio (github):** <https://github.com/ianoelmolina-cmyk/taxis-nyc/tree/main/api>

### Correr el proyecto en local
1. Clonar el repositorio: git clone https://github.com/ianoelmolina-cmyk/taxis-nyc.git
2. Crear y activar un entorno virtual: python -m venv .venv y activarlo:
    - Windows (PowerShell): .venv\Scripts\Activate.ps1
    - Mac/Linux: source .venv/bin/activate
3. Instalar las librerías de la API y de la app: pip install -r api/requirements.txt y pip install -r app/requirements.txt
4. Levantar la API (desde la carpeta api): cd api y luego python -m uvicorn main:app --reload
   (queda en http://localhost:8000/docs)
5. Crear app/.streamlit/secrets.toml con API_URL = "http://localhost:8000"
6. Levantar la app, en **otra terminal** con el entorno activado: cd app y luego streamlit run streamlit_app.py