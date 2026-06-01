import os, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

penguins = [
    {'bill_length_mm':39.1,'bill_depth_mm':18.7,'flipper_length_mm':181,'body_mass_g':3750},
    {'bill_length_mm':46.5,'bill_depth_mm':17.9,'flipper_length_mm':192,'body_mass_g':3500},
    {'bill_length_mm':46.1,'bill_depth_mm':13.2,'flipper_length_mm':211,'body_mass_g':4500},
]

for i, p in enumerate(penguins, 1):
    r = requests.post(f'{BASE_URL}/predict', json=p).json()
    print(f'Pingouin {i} → {r["species"]} ({r["confidence"]:.0%})')