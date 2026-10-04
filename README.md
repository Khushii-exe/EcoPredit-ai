# EcoPredict AI ⚡

Cloud-ready ML API for household appliance energy-consumption prediction.

## Stack
Python • Pandas • NumPy • Scikit-learn Random Forest • FastAPI • Pytest • Docker • GitHub Actions • Render

## Architecture
Client → FastAPI → Pydantic validation → feature ordering → Random Forest → prediction + category + recommendation

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Test
```bash
pytest -q
```
The automated suite has 4 tests and uses FastAPI TestClient; no running server is required.

For manual API integration testing, start the server and run:
```bash
python prediction_check.py
```

## Docker
```bash
docker build -t ecopredict-ai .
docker run -p 8000:8000 ecopredict-ai
```

## Render deployment
The repository includes `Dockerfile` and `render.yaml`.

1. Push this repository to GitHub.
2. Create a new Render Blueprint/Web Service from the repository.
3. Deploy the Docker service.
4. Verify `/health` and `/docs` on the deployed URL.

## CI/CD
GitHub Actions runs `pytest -q` on pushes and pull requests to `main`.

For the requirement to block failing code from reaching `main`, enable a GitHub branch rule/ruleset requiring the `CI / test` status check before merging.

## Model
`model/energy_model.pkl` contains the trained Random Forest and the exact feature order used during training, preventing feature-order mismatches at inference time.

## Dataset
`data/energydata_complete.csv` is included for reproducibility. The notebook contains the data analysis, chronological split, baseline, Random Forest training/evaluation, feature importance, and model export workflow.
