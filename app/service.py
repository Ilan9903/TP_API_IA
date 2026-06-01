import os, requests
import joblib, numpy as np
from pathlib import Path
from app.schemas import PenguinInput, PredictionOutput
from dotenv import load_dotenv

load_dotenv() 

MODELS_DIR = Path(__file__).parent.parent / 'models'

class PredictionService:
    def __init__(self):
        self.model = joblib.load(MODELS_DIR / 'model.pkl')
        self.encoder = joblib.load(MODELS_DIR / 'encoder.pkl')
        print('■ Modèle chargé')
    
    def predict(self, data: PenguinInput) -> PredictionOutput:
        x = np.array([[data.bill_length_mm, data.bill_depth_mm, data.flipper_length_mm, data.body_mass_g]])

        idx = self.model.predict(x)[0]
        confidence = float(self.model.predict_proba(x)[0][idx])
        species = self.encoder.inverse_transform([idx])[0]

        return PredictionOutput(
            species = species,
            confidence = round(confidence, 3),
            message = f'{species} - confiance {confidence:.1%}'
        )

class MistralService:
    API_URL = 'https://api.mistral.ai/v1/chat/completions'

    def __init__(self):
        self.key = os.getenv('MISTRAL_API_KEY')
        if not self.key:
            raise ValueError('MISTRAL_API_KEY is not set in environment variables')
        
    def describe(self, species: str, confidence: float) -> str:
        prompt = (
            f'En 2-3 phrases simples, décris le pingouin {species} '
            f'(Pygoscelis) de façon pédagogique. '
            f'Mentionne ses caractéristiques physiques distinctives.'
        )
        body = {
            'model' : 'mistral-small-latest',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150
        }
        headers = {'Authorization': f'Bearer {self.key}', 'Content-Type': 'application/json'}
        resp = requests.post(self.API_URL, json=body, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()['choices'][0]['message']['content']