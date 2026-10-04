# EcoPredict AI Frontend

Streamlit dashboard for the deployed EcoPredict AI FastAPI backend.

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app uses `https://ecopredit-ai.onrender.com` by default.

To use another backend:

```bash
API_URL=https://your-api-url.onrender.com streamlit run streamlit_app.py
```

## Cloud deployment

Deploy this folder as a Render Web Service:

- Root Directory: `frontend`
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT`
- Environment Variable: `API_URL=https://ecopredit-ai.onrender.com`
