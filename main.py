from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
import openpyxl
from datetime import datetime
import os

# ---------------- COLORS (MODERN THEME) ----------------
BG_MAIN = "#F3F4F6"
CARD_BG = "#FFFFFF"
PRIMARY = "#6366F1"
PRIMARY_HOVER = "#4F46E5"
TEXT_DARK = "#1F2937"
TEXT_LIGHT = "#6B7280"
BORDER = "#E5E7EB"

# ---------------- SYMPTOM MAPPING ----------------
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

# ------------- ORIGINAL DATA -------------
l1 = [
'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria',
'family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances',
'receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding',
'distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum',
'prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads',
'scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails',
'blister','red_sore_around_nose','yellow_crust_ooze'
]

disease = list(mapping.keys())
l2 = [0] * len(l1)

# -------- LOAD DATA ----------
df = pd.read_csv(r"C:\Users\harsh\Downloads\Disease_Detection-main\Training.csv")
df.replace({'prognosis': mapping}, inplace=True)

X = df[l1]
y = df[["prognosis"]]

# ----------------------------------------------------
# ------------- SAVE TO EXCEL FUNCTION ---------------
def save_to_excel(name, symptoms, result):
    filename = "prediction_log.xlsx"

    if not os.path.exists(filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Predictions"
        ws.append(["Timestamp", "Patient Name", "Symptom 1", "Symptom 2", "Symptom 3",
                   "Symptom 4", "Symptom 5", "Predicted Disease"])
        wb.save(filename)

    wb = openpyxl.load_workbook(filename)
    ws = wb.active

    ws.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        *symptoms,
        result
    ])

    wb.save(filename)

# ----------- ML FUNCTION --------------
def randomforest():
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier()
    clf.fit(X, np.ravel(y))

    psymptoms = [Symptom1.get(), Symptom2.get(), Symptom3.get(),
                 Symptom4.get(), Symptom5.get()]
    name = Name.get()

    global l2
    l2 = [1 if s in psymptoms else 0 for s in l1]

    prediction = clf.predict([l2])[0]
    result = disease[prediction]

    result_box.config(state=NORMAL)
    result_box.delete("1.0", END)
    result_box.insert(END, result)
    result_box.config(state=DISABLED)

    save_to_excel(name, psymptoms, result)

# ----------------------------------------------------
# ------------------- UI START -----------------------
root = Tk()
root.title("AI Doctor - Disease Predictor")
root.geometry("850x700")
root.configure(bg=BG_MAIN)

# ---------------- STYLING ----------------
style = ttk.Style()
style.configure("TLabel", background=CARD_BG, foreground=TEXT_DARK, font=("Segoe UI", 11))
style.configure("Header.TLabel", background=BG_MAIN, foreground=PRIMARY, font=("Segoe UI", 32, "bold"))
style.configure("SubHeader.TLabel", background=BG_MAIN, foreground=TEXT_LIGHT, font=("Segoe UI", 14))
style.configure("Card.TFrame", background=CARD_BG, relief="flat", padding=30)
style.configure("TEntry", padding=8, relief="flat")
style.map("TButton",
          background=[("active", PRIMARY_HOVER)],
          relief=[("pressed", "flat")])

# ---------------- HEADER ----------------
header = ttk.Label(root, text="AI Doctor", style="Header.TLabel")
header.pack(pady=(30, 5))

subtitle = ttk.Label(root,
                     text="Select symptoms to detect possible disease",
                     style="SubHeader.TLabel")
subtitle.pack(pady=(0, 20))

# ---------------- MAIN CARD ----------------
main_frame = ttk.Frame(root, style="Card.TFrame")
main_frame.pack(pady=20, padx=40, fill="both")

form_frame = ttk.Frame(main_frame, style="Card.TFrame")
form_frame.pack()

OPTIONS = sorted(l1)

# -------- Input Variables --------
Name = StringVar()
Symptom1 = StringVar()
Symptom2 = StringVar()
Symptom3 = StringVar()
Symptom4 = StringVar()
Symptom5 = StringVar()

# -------- Name Entry --------
ttk.Label(form_frame, text="Patient Name").grid(row=0, column=0, pady=10, sticky="w")
name_entry = ttk.Entry(form_frame, textvariable=Name, width=30)
name_entry.grid(row=0, column=1, pady=10, padx=10)

# -------- Dropdown Creator --------
def create_dropdown(label, variable, row):
    ttk.Label(form_frame, text=label).grid(row=row, column=0, pady=10, sticky="w")
    cb = ttk.Combobox(form_frame, textvariable=variable, values=OPTIONS, width=27)
    cb.set("Select symptom")
    cb.grid(row=row, column=1, pady=10, padx=10)

create_dropdown("Symptom 1", Symptom1, 1)
create_dropdown("Symptom 2", Symptom2, 2)
create_dropdown("Symptom 3", Symptom3, 3)
create_dropdown("Symptom 4", Symptom4, 4)
create_dropdown("Symptom 5", Symptom5, 5)

# ---------------- PREDICT BUTTON ----------------
predict_btn = ttk.Button(main_frame,
                         text="Predict Disease",
                         command=randomforest)
predict_btn.pack(pady=20, ipadx=14, ipady=6)

# ---------------- RESULT DISPLAY ----------------
result_label = ttk.Label(main_frame, text="Prediction Result",
                         foreground=PRIMARY, background=CARD_BG,
                         font=("Segoe UI", 16, "bold"))
result_label.pack(pady=(0, 10))

result_box = Text(main_frame,
                  height=2,
                  width=50,
                  bg="#F9FAFB",
                  fg=TEXT_DARK,
                  font=("Segoe UI", 13),
                  relief="flat",
                  padx=10,
                  pady=10)
result_box.pack()
result_box.config(state=DISABLED)

root.mainloop()
