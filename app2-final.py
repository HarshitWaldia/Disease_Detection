import tkinter as tk
from tkinter import ttk
import base64
import threading

# ======================================================
#  PART 1 — CORE APP + SIDEBAR + NAVIGATION + GLASS UI
# ======================================================

# ------------------ GLOBAL COLORS ---------------------
LIGHT_THEME = {
    "bg": "#F2F3F7",
    "sidebar": "#FFFFFF",
    "glass": "#FFFFFFAA",
    "text": "#1F2937",
    "subtext": "#6B7280",
    "accent": "#6366F1",
    "accent_hover": "#4F46E5",
    "border": "#E5E7EB"
}

DARK_THEME = {
    "bg": "#0F1115",
    "sidebar": "#1A1C22",
    "glass": "#1F2129CC",
    "text": "#F3F4F6",
    "subtext": "#9CA3AF",
    "accent": "#818CF8",
    "accent_hover": "#A5B4FC",
    "border": "#2D2F36"
}

THEME = LIGHT_THEME  # starts with light mode


# -------------- BASE64 ICONS (PLACEHOLDERS) -----------
# You can replace these later with real icons or SVG.
ICONS = {
    "home": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAK...",  # placeholder
    "diagnosis": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAK...",
    "history": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAK...",
    "settings": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAK..."
}


def load_icon(b64):
    """Convert base64 → Tkinter PhotoImage."""
    try:
        return tk.PhotoImage(data=b64)
    except Exception:
        return None


# ======================================================
#  GLASS FRAME (Fake glass using translucent white layer)
# ======================================================
class GlassFrame(tk.Frame):
    def __init__(self, parent, padding=20, radius=20, **kwargs):
        super().__init__(parent, **kwargs)

        # Fake glass: just soft white
        glass_color = "#FFFFFF"

        self.radius = radius
        self.padding = padding

        self["bg"] = glass_color
        self["highlightthickness"] = 1
        self["highlightbackground"] = THEME["border"]

        self.inner = tk.Frame(self, bg=glass_color)
        self.inner.pack(expand=True, fill="both", padx=padding, pady=padding)



# ======================================================
#  SIDEBAR BUTTON WITH ICON + LABEL
# ======================================================
class SidebarButton(tk.Frame):
    def __init__(self, parent, text, icon, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command

        self["bg"] = THEME["sidebar"]

        self.btn = tk.Frame(self, bg=THEME["sidebar"])
        self.btn.pack(fill="x", pady=3)

        # -------- ICON LABEL (always created) --------
        icon_img = load_icon(icon)
        if icon_img:
            self.icon_label = tk.Label(self.btn, image=icon_img, bg=THEME["sidebar"])
            self.icon_label.image = icon_img
        else:
            # fallback so icon_label ALWAYS exists
            self.icon_label = tk.Label(self.btn, text="•", font=("Segoe UI", 12),
                                      bg=THEME["sidebar"], fg=THEME["text"])

        self.icon_label.pack(side="left", padx=12)

        # -------- TEXT LABEL --------
        self.text_label = tk.Label(
            self.btn, text=text, font=("Segoe UI", 12),
            bg=THEME["sidebar"], fg=THEME["text"]
        )
        self.text_label.pack(side="left", padx=10)

        # -------- HOVER EVENTS --------
        for widget in (self.btn, self.icon_label, self.text_label):
            widget.bind("<Enter>", lambda e: self.highlight())
            widget.bind("<Leave>", lambda e: self.unhighlight())
            widget.bind("<Button-1>", lambda e: self.command())

    def highlight(self):
        self.btn.config(bg=THEME["accent"])
        self.text_label.config(bg=THEME["accent"], fg="#FFFFFF")
        self.icon_label.config(bg=THEME["accent"])

    def unhighlight(self):
        self.btn.config(bg=THEME["sidebar"])
        self.text_label.config(bg=THEME["sidebar"], fg=THEME["text"])
        self.icon_label.config(bg=THEME["sidebar"])



# ======================================================
#  MAIN APPLICATION CLASS
# ======================================================
class AIDoctorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Doctor - Modern Glass UI")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.root.configure(bg=THEME["bg"])

        self.active_page = None

        self.build_layout()

    # ---------------- Build Main Layout ----------------
    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=THEME["sidebar"], width=240)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg=THEME["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        # ---- Floating AI Button ----
        self.ai_button = tk.Button(
            self.content,
            text="🧠  AI Assistant",
            font=("Segoe UI", 12, "bold"),
            bg=THEME["accent"],
            fg="white",
            activebackground=THEME["accent_hover"],
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            padx=10,
            pady=10,
            command=self.open_ai_assistant
        )
        self.ai_button.place(relx=0.97, rely=0.06, anchor="ne")

        self.add_sidebar_buttons()
        self.show_home()


    # ======================================================
    #  AI ASSISTANT POPUP WINDOW
    # ======================================================
    def open_ai_assistant(self):
        win = tk.Toplevel(self.root)
        win.title("AI Health Assistant")
        win.geometry("500x600")
        win.configure(bg=THEME["bg"])

        # ----- Chat Display -----
        display_frame = tk.Frame(win, bg=THEME["bg"])
        display_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(display_frame, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=canvas.yview)
        self.chat_frame = tk.Frame(canvas, bg=THEME["bg"])

        self.chat_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ----- User Input -----
        input_frame = tk.Frame(win, bg=THEME["bg"])
        input_frame.pack(fill="x")

        self.ai_entry = tk.Entry(input_frame, font=("Segoe UI", 12))
        self.ai_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg=THEME["accent"],
            fg="white",
            relief="flat",
            command=self.process_ai_message
        )
        send_btn.pack(side="right", padx=10, pady=10)

    # ======================================================
    #  PROCESS AI MESSAGE
    # ======================================================
    def process_ai_message(self):
        msg = self.ai_entry.get().strip()
        if msg == "":
            return
        
        self.add_chat_bubble(msg, "user")
        self.ai_entry.delete(0, tk.END)

        response = self.generate_ai_response(msg)
        self.add_chat_bubble(response, "ai")


    # ======================================================
    #  CHAT BUBBLE DISPLAY
    # ======================================================
    def add_chat_bubble(self, text, sender="user"):
        bubble = tk.Frame(
            self.chat_frame,
            bg=THEME["accent"] if sender == "ai" else "#E5E7EB",
            padx=10,
            pady=6
        )
        bubble.pack(anchor="e" if sender == "ai" else "w", pady=4, padx=10)

        lbl = tk.Label(
            bubble,
            text=text,
            font=("Segoe UI", 11),
            bg=bubble["bg"],
            fg="white" if sender == "ai" else "#111"
        )
        lbl.pack()


    # ======================================================
    #  OFFLINE AI RESPONSE GENERATION (NLP + Knowledge Base)
    # ======================================================
    def generate_ai_response(self, msg):
        msg = msg.lower()

        # Simple NLP:
        keywords = msg.split()

        # Disease name detection
        for disease in disease_info.keys():
            if disease.lower().replace(" ", "") in msg.replace(" ", ""):
                info = disease_info[disease]
                return (
                    f"🩺 *{disease}*\n\n"
                    f"• What it is: {info['explanation']}\n\n"
                    f"• Causes: {info['causes']}\n\n"
                    f"• Symptoms: {info['symptoms']}\n\n"
                    f"• Prevention: {info['prevention']}\n\n"
                    f"• Home Care: {info['homecare']}\n\n"
                    f"• When to see doctor: {info['doctor']}"
                )

        # General health questions
        if "fever" in msg:
            return (
                "Fever can result from infections, dehydration, or inflammation.\n\n"
                "Try:\n• Rest\n• Hydration\n• Lukewarm compress\n\n"
                "Seek care if fever > 3 days or very high."
            )

        if "headache" in msg or "migraine" in msg:
            return (
                "Headaches may be caused by stress, dehydration, or sleep issues.\n"
                "If migraine: rest in a dark room and stay hydrated.\n"
                "Seek help if headaches are severe or frequent."
            )

        return (
            "I'm here to help! Try asking:\n"
            "• What is dengue?\n"
            "• Symptoms of diabetes?\n"
            "• How to reduce fever?\n"
            "• Causes of migraine?"
        )

    # ---------------- Sidebar Buttons ----------------
    def add_sidebar_buttons(self):
        SidebarButton(
            self.sidebar, "🏠 Home", ICONS["home"],
            command=self.show_home
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "🩺 Diagnosis", ICONS["diagnosis"],
            command=self.show_diagnosis
        ).pack(fill="x")

        SidebarButton(
            self.sidebar,
            "🤖 AI Assistant",
            ICONS["settings"],   # or use another icon if you have one
            command=self.open_ai_assistant
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "📜 History", ICONS["history"],
            command=self.show_history
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "⚙️ Settings", ICONS["settings"],
            command=self.show_settings
        ).pack(fill="x")

    # ==================================================
    #  PAGE SWITCHER
    # ==================================================
    def switch_page(self, frame_builder):
        if self.active_page:
            self.active_page.destroy()

        self.active_page = frame_builder()
        self.active_page.pack(fill="both", expand=True, padx=20, pady=20)

    # ----------------- Pages -----------------

    def show_home(self):
        def build():
            frame = GlassFrame(self.content)
            tk.Label(
                frame.inner,
                text="Welcome to AI Doctor",
                font=("Segoe UI", 28, "bold"),
                bg=frame.inner["bg"],
                fg=THEME["text"],
            ).pack(pady=20)

            tk.Label(
                frame.inner,
                text="Use the sidebar to navigate.\nThis app uses machine learning to predict diseases based on symptoms.",
                font=("Segoe UI", 14),
                bg=frame.inner["bg"],
                fg=THEME["subtext"],
            ).pack(pady=10)

            return frame

        self.switch_page(build)

    def show_diagnosis(self):
        # Placeholder — actual UI in PART 2
        def build():
            frame = GlassFrame(self.content)
            tk.Label(
                frame.inner,
                text="Diagnosis Page (loading...)",
                font=("Segoe UI", 24),
                bg=frame.inner["bg"],
                fg=THEME["text"]
            ).pack(pady=40)
            return frame

        self.switch_page(build)

    def show_history(self):
        # Placeholder — real table added in PART 3
        def build():
            frame = GlassFrame(self.content)
            tk.Label(
                frame.inner,
                text="History Page (loading...)",
                font=("Segoe UI", 24),
                bg=frame.inner["bg"],
                fg=THEME["text"]
            ).pack(pady=40)
            return frame

        self.switch_page(build)

    def show_settings(self):
        # Placeholder — real settings added in PART 3
        def build():
            frame = GlassFrame(self.content)
            tk.Label(
                frame.inner,
                text="Settings Page (loading...)",
                font=("Segoe UI", 24),
                bg=frame.inner["bg"],
                fg=THEME["text"]
            ).pack(pady=40)
            return frame

        self.switch_page(build)


# ======================================================
#  FULL DISEASE KNOWLEDGE BASE (EXPLANATION + ADVICE)
# ======================================================

disease_info = {

    "Fungal infection": {
        "explanation": "A fungal infection occurs when fungi grow excessively on the skin or inside the body.",
        "causes": "Warm, moist environments, poor hygiene, weak immunity.",
        "symptoms": "Itching, redness, flaky skin, rash, white patches.",
        "prevention": "Keep skin dry, avoid sharing personal items, wear breathable clothing.",
        "homecare": "Wash area daily, keep dry, apply mild antifungal cream if advised.",
        "doctor": "If spreading, painful, or not improving in 7–10 days."
    },

    "Allergy": {
        "explanation": "An allergy occurs when the immune system reacts to harmless substances.",
        "causes": "Pollen, dust, food, pet dander, chemicals.",
        "symptoms": "Sneezing, itching, rash, watery eyes, swelling.",
        "prevention": "Avoid triggers, keep home clean, use masks during pollen season.",
        "homecare": "Cold compress, hydration, mild antihistamines (if safe).",
        "doctor": "If breathing difficulty or facial swelling occurs."
    },

    "GERD": {
        "explanation": "GERD occurs when stomach acid flows back into the esophagus.",
        "causes": "Spicy food, late meals, obesity, alcohol, caffeine.",
        "symptoms": "Heartburn, chest burning, sour taste, cough.",
        "prevention": "Avoid heavy meals, reduce caffeine and spicy foods.",
        "homecare": "Eat small meals, stay upright after eating.",
        "doctor": "If chest pain or persistent reflux occurs."
    },

    "Chronic cholestasis": {
        "explanation": "Long-term blockage of bile flow from the liver.",
        "causes": "Liver disease, bile duct obstruction, infections.",
        "symptoms": "Jaundice, itching, fatigue, dark urine.",
        "prevention": "Avoid alcohol, maintain liver health.",
        "homecare": "Hydration, low-fat diet.",
        "doctor": "Required for long-term monitoring."
    },

    "Drug Reaction": {
        "explanation": "Unexpected reaction to medication.",
        "causes": "Side effects, allergy, incorrect use.",
        "symptoms": "Rash, itching, swelling, fever.",
        "prevention": "Check medication allergies, follow dosage instructions.",
        "homecare": "Stop suspected drug (if told by doctor).",
        "doctor": "Immediately if breathing difficulty occurs."
    },

    "Peptic ulcer diseae": {
        "explanation": "Sores in the stomach or intestine lining.",
        "causes": "H. pylori bacteria, stress, spicy food.",
        "symptoms": "Burning stomach pain, nausea, bloating.",
        "prevention": "Avoid smoking, alcohol, spicy foods.",
        "homecare": "Small bland meals, avoid late meals.",
        "doctor": "If vomiting blood or severe pain."
    },

    "AIDS": {
        "explanation": "Severe immune deficiency caused by HIV.",
        "causes": "HIV infection through fluids.",
        "symptoms": "Weight loss, fever, weakness, recurrent infections.",
        "prevention": "Safe practices, avoid shared needles.",
        "homecare": "Good nutrition, hygiene, avoid infections.",
        "doctor": "Regular long-term care required."
    },

    "Diabetes ": {
        "explanation": "A chronic condition with high blood sugar levels.",
        "causes": "Genetics, poor diet, obesity.",
        "symptoms": "Thirst, frequent urination, fatigue.",
        "prevention": "Healthy weight, exercise, low sugar diet.",
        "homecare": "Monitor sugar, avoid sugary foods.",
        "doctor": "Regular monitoring needed."
    },

    "Gastroenteritis": {
        "explanation": "Infection causing stomach and intestine inflammation.",
        "causes": "Virus, bacteria, contaminated food.",
        "symptoms": "Vomiting, diarrhea, cramps, fever.",
        "prevention": "Wash hands, avoid unsafe food.",
        "homecare": "ORS, hydration, rest.",
        "doctor": "If dehydration signs appear."
    },

    "Bronchial Asthma": {
        "explanation": "Chronic inflammation of airways.",
        "causes": "Allergens, smoke, cold air, exercise.",
        "symptoms": "Wheezing, breathlessness, cough.",
        "prevention": "Avoid triggers, use inhalers as prescribed.",
        "homecare": "Steam inhalation, calm breathing.",
        "doctor": "If severe or frequent attacks occur."
    },

    "Hypertension ": {
        "explanation": "High blood pressure.",
        "causes": "Stress, high salt, genetics.",
        "symptoms": "Headache, dizziness, sometimes none.",
        "prevention": "Low salt diet, exercise.",
        "homecare": "Relaxation, reduce salt.",
        "doctor": "Regular checkups required."
    },

    "Migraine": {
        "explanation": "Neurological disorder causing intense headaches.",
        "causes": "Stress, hormones, bright lights.",
        "symptoms": "Throbbing headache, nausea, light sensitivity.",
        "prevention": "Avoid triggers, maintain sleep schedule.",
        "homecare": "Dark room rest, hydration.",
        "doctor": "If frequent or severe."
    },

    "Cervical spondylosis": {
        "explanation": "Wear and tear of neck spine.",
        "causes": "Aging, poor posture.",
        "symptoms": "Neck stiffness, pain, headache.",
        "prevention": "Good posture, ergonomic workplace.",
        "homecare": "Warm compress, stretching.",
        "doctor": "If pain radiates to arms."
    },

    "Paralysis (brain hemorrhage)": {
        "explanation": "Loss of muscle movement due to brain bleeding.",
        "causes": "Stroke, trauma.",
        "symptoms": "Weakness, slurred speech, paralysis.",
        "prevention": "Control BP, avoid smoking.",
        "homecare": "Requires medical care + rehab.",
        "doctor": "Emergency condition."
    },

    "Jaundice": {
        "explanation": "Yellow skin due to excess bilirubin.",
        "causes": "Liver disease, infection.",
        "symptoms": "Yellow eyes, dark urine.",
        "prevention": "Avoid alcohol, clean food.",
        "homecare": "Hydration, rest.",
        "doctor": "If worsening or lasting long."
    },

    "Malaria": {
        "explanation": "Mosquito-borne infection.",
        "causes": "Plasmodium parasite via mosquitoes.",
        "symptoms": "Fever, chills, body pain.",
        "prevention": "Mosquito nets, avoid stagnant water.",
        "homecare": "Stay hydrated, rest.",
        "doctor": "If vomiting or severe weakness."
    },

    "Chicken pox": {
        "explanation": "Viral infection with itchy blisters.",
        "causes": "Varicella virus.",
        "symptoms": "Rash, fever, blisters.",
        "prevention": "Vaccination, avoid infected people.",
        "homecare": "Calamine lotion, avoid scratching.",
        "doctor": "If blisters spread to eyes."
    },

    "Dengue": {
        "explanation": "Mosquito-borne viral fever.",
        "causes": "Aedes mosquitoes.",
        "symptoms": "High fever, joint pain, weakness.",
        "prevention": "Avoid mosquito bites.",
        "homecare": "Hydration, paracetamol (avoid ibuprofen).",
        "doctor": "If bleeding, vomiting, or severe pain."
    },

    "Typhoid": {
        "explanation": "Bacterial infection through contaminated food/water.",
        "causes": "Salmonella typhi bacteria.",
        "symptoms": "High fever, abdominal pain, weakness.",
        "prevention": "Safe water, clean food.",
        "homecare": "Soft diet, ORS.",
        "doctor": "Medical evaluation needed."
    },

    "hepatitis A": {
        "explanation": "Viral infection affecting liver.",
        "causes": "Contaminated food/water.",
        "symptoms": "Fatigue, nausea, jaundice.",
        "prevention": "Hygiene, clean water.",
        "homecare": "Rest, hydration.",
        "doctor": "If symptoms worsen."
    },

    "Hepatitis B": {
        "explanation": "Liver infection spread by fluids.",
        "causes": "Contact with infected blood or fluids.",
        "symptoms": "Fatigue, jaundice, abdominal pain.",
        "prevention": "Vaccination, safe practices.",
        "homecare": "Avoid alcohol.",
        "doctor": "Regular monitoring required."
    },

    "Hepatitis C": {
        "explanation": "Chronic liver infection.",
        "causes": "Exposure to infected blood.",
        "symptoms": "Fatigue, jaundice, weight loss.",
        "prevention": "Avoid shared needles.",
        "homecare": "Healthy diet.",
        "doctor": "Medical treatment required."
    },

    "Hepatitis D": {
        "explanation": "Liver infection requiring hepatitis B co-infection.",
        "causes": "Hepatitis D virus.",
        "symptoms": "Jaundice, fatigue.",
        "prevention": "Avoid hepatitis B infection.",
        "homecare": "Rest, avoid alcohol.",
        "doctor": "Medical care mandatory."
    },

    "Hepatitis E": {
        "explanation": "Viral infection from contaminated water.",
        "causes": "Infected water supply.",
        "symptoms": "Fever, jaundice, fatigue.",
        "prevention": "Safe drinking water.",
        "homecare": "Hydration, rest.",
        "doctor": "If symptoms worsen."
    },

    "Alcoholic hepatitis": {
        "explanation": "Liver inflammation due to alcohol.",
        "causes": "Heavy drinking.",
        "symptoms": "Jaundice, stomach pain.",
        "prevention": "Avoid alcohol.",
        "homecare": "Hydration, healthy diet.",
        "doctor": "Urgent treatment for severe cases."
    },

    "Tuberculosis": {
        "explanation": "Serious bacterial infection affecting lungs.",
        "causes": "Mycobacterium tuberculosis.",
        "symptoms": "Cough, weight loss, night sweats.",
        "prevention": "Avoid infected people, good ventilation.",
        "homecare": "Healthy diet, rest.",
        "doctor": "Requires full medical treatment."
    },

    "Common Cold": {
        "explanation": "Viral infection affecting the nose and throat.",
        "causes": "Rhinovirus.",
        "symptoms": "Cough, sneezing, runny nose.",
        "prevention": "Handwashing, avoid sick contacts.",
        "homecare": "Steam inhalation, warm drinks.",
        "doctor": "If lasting more than 10 days."
    },

    "Pneumonia": {
        "explanation": "Lung infection with swelling of air sacs.",
        "causes": "Bacteria, virus, fungi.",
        "symptoms": "Cough, fever, breathing difficulty.",
        "prevention": "Vaccination, hygiene.",
        "homecare": "Warm liquids, rest.",
        "doctor": "Urgent care recommended."
    },

    "Dimorphic hemmorhoids(piles)": {
        "explanation": "Swollen veins in rectal area.",
        "causes": "Straining, constipation.",
        "symptoms": "Pain, bleeding during bowel movement.",
        "prevention": "High fibre diet, hydration.",
        "homecare": "Warm sitz bath.",
        "doctor": "If bleeding is heavy or persistent."
    },

    "Heart attack": {
        "explanation": "Blocked blood flow to heart muscle.",
        "causes": "Cholesterol, smoking, hypertension.",
        "symptoms": "Chest pain, sweating, nausea.",
        "prevention": "Healthy diet, exercise.",
        "homecare": "Emergency — seek immediate care.",
        "doctor": "Emergency treatment required."
    },

    "Varicose veins": {
        "explanation": "Enlarged twisted veins, usually in legs.",
        "causes": "Weak vein valves, long standing.",
        "symptoms": "Visible veins, leg pain.",
        "prevention": "Avoid long standing.",
        "homecare": "Leg elevation, walking.",
        "doctor": "If ulcers or severe pain."
    },

    "Hypothyroidism": {
        "explanation": "Underactive thyroid gland.",
        "causes": "Autoimmune issues, iodine deficiency.",
        "symptoms": "Fatigue, weight gain, cold intolerance.",
        "prevention": "Iodine balanced diet.",
        "homecare": "Healthy diet, exercise.",
        "doctor": "Needs thyroid level monitoring."
    },

    "Hyperthyroidism": {
        "explanation": "Overactive thyroid gland.",
        "causes": "Autoimmune conditions.",
        "symptoms": "Weight loss, anxiety, fast heartbeat.",
        "prevention": "Limit caffeine.",
        "homecare": "Stress reduction.",
        "doctor": "Evaluation and treatment needed."
    },

    "Hypoglycemia": {
        "explanation": "Low blood sugar level.",
        "causes": "Irregular meals, medications.",
        "symptoms": "Shakiness, sweating, confusion.",
        "prevention": "Regular meals, avoid skipping food.",
        "homecare": "Take a quick sugar source.",
        "doctor": "If unconscious or recurring episodes."
    },

    "Osteoarthristis": {
        "explanation": "Joint cartilage wear and tear.",
        "causes": "Age, injury.",
        "symptoms": "Joint pain, stiffness.",
        "prevention": "Maintain weight, avoid joint stress.",
        "homecare": "Warm compress, gentle exercise.",
        "doctor": "If mobility decreases."
    },

    "Arthritis": {
        "explanation": "Inflammation of joints.",
        "causes": "Autoimmune, infection, injury.",
        "symptoms": "Swelling, stiffness, pain.",
        "prevention": "Healthy lifestyle.",
        "homecare": "Warm baths.",
        "doctor": "If persistent or worsening."
    },

    "(vertigo) Paroymsal  Positional Vertigo": {
        "explanation": "Brief dizziness triggered by head movement.",
        "causes": "Inner ear crystals.",
        "symptoms": "Spinning sensation, imbalance.",
        "prevention": "Avoid sudden movements.",
        "homecare": "Sit down during episodes.",
        "doctor": "If persistent or severe."
    },

    "Acne": {
        "explanation": "Inflammatory skin condition with pimples.",
        "causes": "Hormones, oil glands.",
        "symptoms": "Pimples, blackheads.",
        "prevention": "Clean face regularly, avoid oily cosmetics.",
        "homecare": "Gentle cleansing.",
        "doctor": "If cystic or severe."
    },

    "Urinary tract infection": {
        "explanation": "Bacterial infection in urinary tract.",
        "causes": "Bacteria entering urethra.",
        "symptoms": "Burning urination, frequent urge.",
        "prevention": "Hydration, hygiene.",
        "homecare": "Drink plenty of water.",
        "doctor": "If fever or back pain occurs."
    },

    "Psoriasis": {
        "explanation": "Chronic autoimmune skin disease.",
        "causes": "Immune overactivity.",
        "symptoms": "Scaly patches, itching.",
        "prevention": "Reduce stress, avoid triggers.",
        "homecare": "Moisturize skin.",
        "doctor": "If spreading rapidly."
    },

    "Impetigo": {
        "explanation": "Bacterial skin infection with crusty sores.",
        "causes": "Bacteria entering broken skin.",
        "symptoms": "Red sores, yellow crusts.",
        "prevention": "Good hygiene.",
        "homecare": "Keep area clean.",
        "doctor": "If spreading or near eyes."
    }

}

# ======================================================
#  PART 2 — ML MODEL + DIAGNOSIS PAGE + LOADING ANIMATION
# ======================================================

import pandas as pd
import numpy as np
import openpyxl
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.metrics import accuracy_score

# -------------------- LOAD ML DATA --------------------

# Update paths to your Training.csv file:
TRAIN_CSV_PATH = r"C:\Users\harsh\Downloads\Disease_Detection-main\Training.csv"

df = pd.read_csv(TRAIN_CSV_PATH)

# Mapping from original project
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

symptom_list = list(df.columns[:-1])
disease_list = list(mapping.keys())

X = df[symptom_list]
y = df["prognosis"]

# # ======================================================
# #  SUPER ENSEMBLE MODEL (RF + XGB + SVM + LR + GB)
# # ======================================================

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
# from sklearn.svm import SVC
# from sklearn.linear_model import LogisticRegression
# import xgboost as xgb
# from sklearn.metrics import accuracy_score

# # Load training data
# TRAIN_CSV_PATH = r"C:\Users\harsh\Downloads\Disease_Detection-main\Training.csv"
# df = pd.read_csv(TRAIN_CSV_PATH)
# df.replace({'prognosis': mapping}, inplace=True)

# X = df.iloc[:, :-1]
# y = df["prognosis"]

# # Train-test split
# X_train, X_val, y_train, y_val = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# # ========= SCALING (For SVM & Logistic Regression) =========
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_val_scaled = scaler.transform(X_val)

# # ========= DEFINE MODELS =========
# model_rf = RandomForestClassifier(n_estimators=300, max_depth=20, class_weight="balanced")

# model_xgb = xgb.XGBClassifier(
#     n_estimators=300, learning_rate=0.05, max_depth=6,
#     subsample=0.9, colsample_bytree=0.9, eval_metric='mlogloss'
# )

# model_svm = SVC(probability=True, kernel='rbf', C=2, gamma='scale')

# model_lr = LogisticRegression(max_iter=2000)

# model_gb = GradientBoostingClassifier(n_estimators=300, learning_rate=0.05, max_depth=4)

# # ========= ENSEMBLE (soft voting) =========
# ensemble = VotingClassifier(
#     estimators=[
#         ("rf", model_rf),
#         ("xgb", model_xgb),
#         ("svm", model_svm),
#         ("lr", model_lr),
#         ("gb", model_gb)
#     ],
#     voting='soft'
# )

# # Train ensemble
# ensemble.fit(X_train_scaled, y_train)

# # Validation accuracy
# pred_val = ensemble.predict(X_val_scaled)
# print("\nEnsemble Accuracy:", accuracy_score(y_val, pred_val))

import pickle

# Load pre-trained models
best_model = pickle.load(open("ensemble_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ======================================================
#  SAVE TO EXCEL (LOGGING)
# ======================================================
def save_to_excel_log(name, symptoms, result):
    filename = "prediction_log.xlsx"

    if not os.path.exists(filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Predictions"
        ws.append([
            "Timestamp", "Patient Name",
            "Symptom 1", "Symptom 2", "Symptom 3",
            "Symptom 4", "Symptom 5", "Result"
        ])
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


# ======================================================
#  EXTEND THE AIDoctorApp CLASS (add diagnosis page)
# ======================================================

def add_diagnosis_page_to_app():

    def diagnosis_page(self):
        """Builds the full diagnosis UI inside a glass card."""

        def build():
            frame = GlassFrame(self.content, padding=25)

            # ------------------ Title ------------------
            tk.Label(
                frame.inner,
                text="Disease Prediction",
                font=("Segoe UI", 22, "bold"),
                fg=THEME["text"],
                bg=frame.inner["bg"]
            ).pack(anchor="w", pady=(0, 10))

            # ------------------ Patient Name ------------------
            tk.Label(
                frame.inner, text="Patient Name:",
                font=("Segoe UI", 12),
                bg=frame.inner["bg"], fg=THEME["text"]
            ).pack(anchor="w")

            name_entry = ttk.Entry(frame.inner, width=40)
            name_entry.pack(anchor="w", pady=(0, 15))

            # ------------------ Symptoms Dropdowns ------------------
            tk.Label(
                frame.inner, text="Select up to 5 symptoms:",
                font=("Segoe UI", 12),
                bg=frame.inner["bg"], fg=THEME["text"]
            ).pack(anchor="w", pady=(10, 5))

            choices = sorted(symptom_list)
            symptom_vars = []

            for i in range(5):
                var = tk.StringVar()
                box = ttk.Combobox(frame.inner, textvariable=var, values=choices, width=50)
                box.set("Select a symptom")
                box.pack(anchor="w", pady=5)
                symptom_vars.append(var)

            # ------------------ Result Label ------------------
            result_label = tk.Label(
                frame.inner,
                text="Result will appear here...",
                font=("Segoe UI", 14),
                bg=frame.inner["bg"],
                fg=THEME["subtext"]
            )
            result_label.pack(pady=20)

            # ------------------ Loading Animation ------------------
            loading_label = tk.Label(
                frame.inner,
                text="",
                font=("Segoe UI", 12),
                bg=frame.inner["bg"],
                fg=THEME["accent"]
            )
            loading_label.pack()

            def animate_loading():
                dots = ["", ".", "..", "..."]
                i = 0
                while self.loading:
                    loading_label.config(text="Predicting" + dots[i % 4])
                    i += 1
                    loading_label.update()
                    time.sleep(0.3)

            # ------------------ Prediction Logic ------------------
            import time

            def predict():
                name = name_entry.get().strip()
                selected = [v.get() for v in symptom_vars if v.get() != "Select a symptom"]

                if name == "":
                    result_label.config(text="⚠ Please enter patient name.", fg="red")
                    return

                if len(selected) == 0:
                    result_label.config(text="⚠ Select at least one symptom.", fg="red")
                    return

                # Build input vector
                vector = [1 if s in selected else 0 for s in symptom_list]

                # Start loading animation
                self.loading = True
                thread_anim = threading.Thread(target=animate_loading)
                thread_anim.start()

                def run_prediction():
                    time.sleep(1)  # Simulated processing delay

                    # -------- BUILD INPUT VECTOR --------
                    vector = [1 if s in selected else 0 for s in symptom_list]

                    # -------- SCALE INPUT --------
                    vector_scaled = scaler.transform([vector])

                    # -------- PREDICT PROBABILITIES --------
                    probs = best_model.predict_proba(vector_scaled)[0]

                    # -------- TOP 3 DISEASES --------
                    top3 = probs.argsort()[-3:][::-1]

                    main_disease = disease_list[top3[0]]

                    # -------- LOG TO EXCEL --------
                    save_to_excel_log(name, selected + [""]*(5 - len(selected)), main_disease)

                    # -------- EXPLANATION + SAFE ADVICE --------
                    info = disease_info.get(main_disease, {})
                    explanation = info.get("explanation", "No explanation available.")
                    advice = info.get("advice", "No advice available.")

                    result_text = (
                        f"🔍 Top Predictions:\n"
                        f"1. {disease_list[top3[0]]} ({probs[top3[0]]*100:.2f}%)\n"
                        f"2. {disease_list[top3[1]]} ({probs[top3[1]]*100:.2f}%)\n"
                        f"3. {disease_list[top3[2]]} ({probs[top3[2]]*100:.2f}%)\n\n"
                        f"🧠 Explanation:\n{explanation}\n\n"
                        f"💊 Recommendations:\n{advice}"
                    )

                    # -------- UPDATE UI --------
                    self.loading = False
                    loading_label.config(text="")
                    result_label.config(text=result_text, fg=THEME["text"])


                threading.Thread(target=run_prediction).start()

            # ------------------ Predict Button ------------------
            predict_btn = tk.Button(
                frame.inner,
                text="Predict Disease",
                font=("Segoe UI", 13, "bold"),
                bg=THEME["accent"],
                fg="white",
                activebackground=THEME["accent_hover"],
                cursor="hand2",
                relief="flat",
                padx=20,
                pady=10,
                command=predict
            )
            predict_btn.pack(pady=10)

            return frame

        self.switch_page(build)

    # Inject this method into AIDoctorApp
    AIDoctorApp.show_diagnosis = diagnosis_page


# activate injection
add_diagnosis_page_to_app()

# ======================================================
#  PART 3 — HISTORY PAGE + SETTINGS PAGE + THEME ENGINE
# ======================================================

# --------------- History Page (Excel Log Reader) ---------------
def add_history_page_to_app():

    def history_page(self):

        def build():
            frame = GlassFrame(self.content, padding=20)

            title = tk.Label(
                frame.inner,
                text="Prediction History",
                font=("Segoe UI", 20, "bold"),
                bg=frame.inner["bg"],
                fg=THEME["text"]
            )
            title.pack(anchor="w", pady=(0, 10))

            file = "prediction_log.xlsx"
            if not os.path.exists(file):
                tk.Label(
                    frame.inner,
                    text="No history found.",
                    font=("Segoe UI", 14),
                    bg=frame.inner["bg"],
                    fg=THEME["subtext"]
                ).pack(pady=20)
                return frame

            # Load Excel
            df = pd.read_excel(file)

            # =============== SCROLLABLE TABLE ===============
            container = tk.Frame(frame.inner, bg=frame.inner["bg"])
            container.pack(fill="both", expand=True)

            canvas = tk.Canvas(container, bg=frame.inner["bg"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            table_frame = tk.Frame(canvas, bg=frame.inner["bg"])
            canvas.create_window((0, 0), window=table_frame, anchor="nw")

            def update_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            table_frame.bind("<Configure>", update_scroll)

            # ---------------- HEADER ----------------
            for col, column_name in enumerate(df.columns):
                tk.Label(
                    table_frame,
                    text=column_name,
                    font=("Segoe UI", 11, "bold"),
                    bg=frame.inner["bg"],
                    fg=THEME["text"],
                    borderwidth=1,
                    relief="solid",
                    padx=8,
                    pady=4
                ).grid(row=0, column=col, sticky="nsew")

            # ---------------- ROWS ----------------
            for r, row_data in enumerate(df.values, start=1):
                for c, cell in enumerate(row_data):
                    tk.Label(
                        table_frame,
                        text=str(cell),
                        font=("Segoe UI", 10),
                        bg=frame.inner["bg"],
                        fg=THEME["subtext"],
                        borderwidth=1,
                        relief="solid",
                        padx=8,
                        pady=4
                    ).grid(row=r, column=c, sticky="nsew")

            # Expand columns equally
            for col in range(len(df.columns)):
                table_frame.grid_columnconfigure(col, weight=1)

            return frame

        self.switch_page(build)

    AIDoctorApp.show_history = history_page

add_history_page_to_app()

# ======================================================
#  SETTINGS PAGE (Dark Mode Toggle)
# ======================================================

def add_settings_page_to_app():

    def settings_page(self):

        def build():
            frame = GlassFrame(self.content, padding=25)

            tk.Label(
                frame.inner,
                text="Settings",
                font=("Segoe UI", 22, "bold"),
                bg=frame.inner["bg"],
                fg=THEME["text"]
            ).pack(anchor="w", pady=(0, 20))

            # ------------------ Theme Toggle ------------------
            def toggle_theme():
                global THEME
                THEME = DARK_THEME if theme_var.get() == 1 else LIGHT_THEME
                self.rebuild_ui()

            theme_var = tk.IntVar(value=1 if THEME == DARK_THEME else 0)

            tk.Checkbutton(
                frame.inner,
                text=" Dark Mode",
                font=("Segoe UI", 14),
                variable=theme_var,
                bg=frame.inner["bg"],
                fg=THEME["text"],
                activebackground=frame.inner["bg"],
                command=toggle_theme,
                selectcolor=frame.inner["bg"]
            ).pack(anchor="w", pady=5)

            # ------------------ About Section ------------------
            tk.Label(
                frame.inner,
                text="\nAI Doctor v1.0\nModern Glass UI\nPowered by Machine Learning",
                font=("Segoe UI", 12),
                bg=frame.inner["bg"],
                fg=THEME["subtext"],
                justify="left"
            ).pack(anchor="w", pady=30)

            return frame

        self.switch_page(build)

    AIDoctorApp.show_settings = settings_page


add_settings_page_to_app()


# ======================================================
#  THEME REBUILDING (Applies Dark/Light Mode)
# ======================================================
def add_rebuild_ui_to_app():

    def rebuild_ui(self):
        """Rebuild the entire UI after theme change."""
        self.root.configure(bg=THEME["bg"])

        self.sidebar.destroy()
        self.content.destroy()

        self.build_layout()

    AIDoctorApp.rebuild_ui = rebuild_ui


add_rebuild_ui_to_app()


# ======================================================
#  🎉 FULL APPLICATION IS COMPLETE AFTER PART 3
# ======================================================
print("AI Doctor App Loaded Successfully — All Parts (1–3) Installed.")

# ======================================================
#  APP STARTER
# ======================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AIDoctorApp(root)

    root.mainloop()
