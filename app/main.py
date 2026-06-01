from fastapi import FastAPI, HTTPException
from app.schemas import PenguinInput, PredictionOutput, AnalysisOutput
from app.service import PredictionService, MistralService

app = FastAPI(title='Penguin Classifier', description='API ML — APIE638', version='1.0')
svc = PredictionService()
mistral = MistralService()

@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'RandomForest v1.0'}

@app.post('/predict', response_model=PredictionOutput)
def predict(penguin: PenguinInput):
    """Prédit l'espèce d'un pingouin à partir de ses 4 mensurations."""
    try:
        return svc.predict(penguin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/analyze', response_model=AnalysisOutput)
def analyze(penguin: PenguinInput):
    """Prédit l'espèce et génère une description via Mistral."""
    pred = svc.predict(penguin)
    description = mistral.describe(pred.species, pred.confidence)
    return AnalysisOutput(
        species = pred.species,
        confidence = pred.confidence,
        description = description
    )

