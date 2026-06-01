import sqlite3, datetime
from fastapi import FastAPI, HTTPException
from app.schemas import PenguinInput, PredictionOutput, AnalysisOutput
from app.service import PredictionService, MistralService

app = FastAPI(title='Penguin Classifier', description='API ML — APIE638', version='1.0')
svc = PredictionService()
mistral = MistralService()

def init_db():
    con = sqlite3.connect('predictions.db')
    con.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, species TEXT, confidence REAL,
        bill_length REAL, bill_depth REAL, flipper REAL, mass REAL
    )''')
    con.commit(); con.close()

init_db()


@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'RandomForest v1.0'}

@app.post('/predict', response_model=PredictionOutput)
def predict(penguin: PenguinInput):
    """Prédit l'espèce d'un pingouin à partir de ses 4 mensurations."""
    try:
        result = svc.predict(penguin)
        con = sqlite3.connect('predictions.db')
        con.execute('INSERT INTO predictions VALUES (NULL,?,?,?,?,?,?,?)',
            (datetime.datetime.now().isoformat(), result.species, result.confidence,
            penguin.bill_length_mm, penguin.bill_depth_mm,
            penguin.flipper_length_mm, penguin.body_mass_g))
        con.commit(); con.close()
        return result
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

