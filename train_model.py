import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import xgboost as xgb

# Load Data
df = pd.read_csv(r"C:\Users\harsh\Downloads\Disease_Detection-main\Training.csv")

mapping = {
    'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,'Paralysis (brain hemorrhage)':13,'Jaundice':14,
    'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,'Hepatitis B':20,
    'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,
    'Varicose veins':30,'Hypothyroidism':31,'Hyperthyroidism':32,'Hypoglycemia':33,
    'Osteoarthristis':34,'Arthritis':35,'(vertigo) Paroymsal  Positional Vertigo':36,
    'Acne':37,'Urinary tract infection':38,'Psoriasis':39,'Impetigo':40
}

df.replace({'prognosis': mapping}, inplace=True)

X = df.iloc[:, :-1]
y = df["prognosis"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Build ensemble
model_rf = RandomForestClassifier(n_estimators=300, max_depth=20, class_weight="balanced")
model_xgb = xgb.XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=6, eval_metric='mlogloss')
model_svm = SVC(probability=True, kernel='rbf', C=2)
model_lr = LogisticRegression(max_iter=2000)
model_gb = GradientBoostingClassifier(n_estimators=300)

ensemble = VotingClassifier(
    estimators=[
        ("rf", model_rf),
        ("xgb", model_xgb),
        ("svm", model_svm),
        ("lr", model_lr),
        ("gb", model_gb)
    ],
    voting="soft"
)

# Train ensemble model (slow but ONE TIME ONLY)
ensemble.fit(X_scaled, y)

# Save model + scaler
pickle.dump(ensemble, open("ensemble_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("Model + Scaler saved successfully!")
