import tkinter as tk
from tkinter import ttk
import base64
import threading
import time
import os
from datetime import datetime

# ======================================================
#  PART 1 — CORE APP + SIDEBAR + NAVIGATION + GLASS UI
# ======================================================

# ------------------ GLOBAL COLORS ---------------------
MODERN_THEME = {
    "light": {
        "bg": "#F8FAFC",
        "sidebar": "#FFFFFF",
        "glass": "#FFFFFF",
        "text": "#0F172A",
        "subtext": "#64748B",
        "accent": "#6366F1",
        "accent_hover": "#4F46E5",
        "accent_light": "#EEF2FF",
        "border": "#E2E8F0",
        "shadow": "#00000010"
    },
    "dark": {
        "bg": "#020617",
        "sidebar": "#0F172A",
        "glass": "#1E293B",
        "text": "#F8FAFC",
        "subtext": "#94A3B8",
        "accent": "#818CF8",
        "accent_hover": "#A5B4FC",
        "accent_light": "#312E81",
        "border": "#334155",
        "shadow": "#00000040"
    }
}

CURRENT_THEME = MODERN_THEME["light"]


THEME = CURRENT_THEME


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
    def __init__(self, parent, padding=25, radius=20, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            bg=THEME["glass"],
            highlightthickness=1,
            highlightbackground=THEME["border"],
            padx=2,
            pady=2
        )

        # Inner container with padding
        self.inner = tk.Frame(self, bg=THEME["glass"])
        self.inner.pack(expand=True, fill="both", padx=padding, pady=padding)

        # Subtle shadow effect using a border
        self.shadow = tk.Frame(self, bg=THEME["border"], height=1)
        self.shadow.pack(side="bottom", fill="x")



# ======================================================
#  SIDEBAR BUTTON WITH ICON + LABEL
# ======================================================
class SidebarButton(tk.Frame):
    def __init__(self, parent, text, icon, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.active = False

        self["bg"] = THEME["sidebar"]

        self.btn = tk.Frame(self, bg=THEME["sidebar"], cursor="hand2")
        self.btn.pack(fill="x", pady=2, padx=10)

        # Indicator bar
        self.indicator = tk.Frame(self.btn, bg=THEME["sidebar"], width=4)
        self.indicator.pack(side="left", fill="y", pady=8)

        # -------- ICON LABEL --------
        icon_img = load_icon(icon)
        if icon_img:
            self.icon_label = tk.Label(self.btn, image=icon_img, bg=THEME["sidebar"])
            self.icon_label.image = icon_img
        else:
            self.icon_label = tk.Label(self.btn, text="•", font=("Segoe UI", 14),
                                      bg=THEME["sidebar"], fg=THEME["subtext"])

        self.icon_label.pack(side="left", padx=(12, 8))

        # -------- TEXT LABEL --------
        self.text_label = tk.Label(
            self.btn, text=text, font=("Segoe UI", 11),
            bg=THEME["sidebar"], fg=THEME["text"]
        )
        self.text_label.pack(side="left", padx=5, pady=12)

        # -------- HOVER EVENTS --------
        for widget in (self.btn, self.icon_label, self.text_label):
            widget.bind("<Enter>", lambda e: self.highlight())
            widget.bind("<Leave>", lambda e: self.unhighlight())
            widget.bind("<Button-1>", lambda e: self.on_click())

    def highlight(self):
        if not self.active:
            self.btn.config(bg=THEME["accent_light"])
            self.text_label.config(bg=THEME["accent_light"], fg=THEME["accent"])
            self.icon_label.config(bg=THEME["accent_light"], fg=THEME["accent"])
            self.indicator.config(bg=THEME["accent_light"])

    def unhighlight(self):
        if not self.active:
            self.btn.config(bg=THEME["sidebar"])
            self.text_label.config(bg=THEME["sidebar"], fg=THEME["text"])
            self.icon_label.config(bg=THEME["sidebar"], fg=THEME["subtext"])
            self.indicator.config(bg=THEME["sidebar"])

    def set_active(self, active=True):
        self.active = active
        if active:
            self.btn.config(bg=THEME["accent_light"])
            self.text_label.config(bg=THEME["accent_light"], fg=THEME["accent"], font=("Segoe UI", 11, "bold"))
            self.icon_label.config(bg=THEME["accent_light"], fg=THEME["accent"])
            self.indicator.config(bg=THEME["accent"])
        else:
            self.unhighlight()

    def on_click(self):
        self.command()



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
        # Sidebar container
        self.sidebar = tk.Frame(self.root, bg=THEME["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar Header (App Name/Logo)
        header_sidebar = tk.Frame(self.sidebar, bg=THEME["sidebar"], pady=30)
        header_sidebar.pack(fill="x")
        tk.Label(
            header_sidebar, text="AI DOCTOR",
            font=("Segoe UI", 18, "bold"),
            bg=THEME["sidebar"], fg=THEME["accent"]
        ).pack()

        # Content area
        self.content = tk.Frame(self.root, bg=THEME["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        # Top Header Bar
        self.header_bar = tk.Frame(self.content, bg=THEME["bg"], height=80)
        self.header_bar.pack(fill="x", padx=40, pady=(20, 0))
        self.header_bar.pack_propagate(False)

        self.page_title = tk.Label(
            self.header_bar, text="Home",
            font=("Segoe UI", 24, "bold"),
            bg=THEME["bg"], fg=THEME["text"]
        )
        self.page_title.pack(side="left")

        # ---- Floating AI Button (Restyled) ----
        self.ai_button = tk.Button(
            self.header_bar,
            text="✨ AI Assistant",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["accent"],
            fg="white",
            activebackground=THEME["accent_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.open_ai_assistant
        )
        self.ai_button.pack(side="right")

        self.sidebar_buttons = []
        self.add_sidebar_buttons()
        self.show_home()


    # ======================================================
    #  AI ASSISTANT POPUP WINDOW
    # ======================================================
    def open_ai_assistant(self):
        win = tk.Toplevel(self.root)
        win.title("AI Health Assistant")
        win.geometry("450x650")
        win.configure(bg=THEME["bg"])
        win.transient(self.root)  # Keep on top of parent

        # Header
        head = tk.Frame(win, bg=THEME["accent"], pady=15)
        head.pack(fill="x")
        tk.Label(
            head, text="✨ Health Assistant",
            font=("Segoe UI", 14, "bold"),
            bg=THEME["accent"], fg="white"
        ).pack()

        # ----- Chat Display -----
        display_frame = tk.Frame(win, bg=THEME["bg"])
        display_frame.pack(fill="both", expand=True, padx=15, pady=15)

        canvas = tk.Canvas(display_frame, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=canvas.yview)
        
        # Chat container inside canvas
        self.chat_frame = tk.Frame(canvas, bg=THEME["bg"])
        self.chat_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.chat_frame, anchor="nw", width=400) # Fixed width for wrapping
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ----- User Input -----
        input_container = tk.Frame(win, bg=THEME["sidebar"], pady=15, padx=15)
        input_container.pack(fill="x")
        
        input_frame = tk.Frame(input_container, bg=THEME["bg"], highlightthickness=1, highlightbackground=THEME["border"])
        input_frame.pack(fill="x")

        self.ai_entry = tk.Entry(
            input_frame, font=("Segoe UI", 11),
            bg=THEME["bg"], fg=THEME["text"],
            relief="flat", insertbackground=THEME["text"]
        )
        self.ai_entry.pack(side="left", fill="x", expand=True, padx=12, pady=10)
        self.ai_entry.bind("<Return>", lambda e: self.process_ai_message())

        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["accent"],
            fg="white",
            relief="flat",
            activebackground=THEME["accent_hover"],
            activeforeground="white",
            padx=15,
            command=self.process_ai_message
        )
        send_btn.pack(side="right", padx=5, pady=5)
        
        self.add_chat_bubble("Hello! I'm your AI health assistant. How can I help you today?", "ai")

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
        bubble_bg = THEME["accent"] if sender == "ai" else THEME["accent_light"]
        text_fg = "white" if sender == "ai" else THEME["text"]
        align = "e" if sender == "user" else "w"
        
        wrapper = tk.Frame(self.chat_frame, bg=THEME["bg"])
        wrapper.pack(fill="x", pady=5)

        bubble = tk.Frame(
            wrapper,
            bg=bubble_bg,
            padx=12,
            pady=8
        )
        bubble.pack(anchor=align, padx=10)

        lbl = tk.Label(
            bubble,
            text=text,
            font=("Segoe UI", 11),
            bg=bubble_bg,
            fg=text_fg,
            wraplength=300,
            justify="left"
        )
        lbl.pack()
        
        # Auto-scroll to bottom
        self.chat_frame.update_idletasks()


    # ======================================================
    #  OFFLINE AI RESPONSE GENERATION (NLP + Knowledge Base)
    # ======================================================
    def generate_ai_response(self, msg):
        msg = msg.lower().strip()
        
        # Greetings
        if any(word in msg for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm your AI health assistant. I can help you understand symptoms, provide information about diseases, and offer general health advice. How can I assist you today?"

        # Symptom-based help
        if "symptom" in msg or "feel" in msg or "pain" in msg:
            return "I can help identify potential causes for your symptoms. Please use the 'Diagnosis' tab for a comprehensive analysis using our machine learning model, or tell me more about what you're feeling."

        # Disease name detection (Enhanced)
        matched_disease = None
        for disease in disease_info.keys():
            # Check for exact or close match
            d_lower = disease.lower().replace(" ", "")
            m_lower = msg.replace(" ", "")
            if d_lower in m_lower or m_lower in d_lower:
                matched_disease = disease
                break
        
        if matched_disease:
            info = disease_info[matched_disease]
            return (
                f"🩺 **{matched_disease}**\n\n"
                f"📝 **What it is:** {info['explanation']}\n\n"
                f"❓ **Common Causes:** {info['causes']}\n\n"
                f"⚠️ **Symptoms:** {info['symptoms']}\n\n"
                f"🛡️ **Prevention:** {info['prevention']}\n\n"
                f"🏠 **Home Care:** {info['homecare']}\n\n"
                f"👨‍⚕️ **When to see a doctor:** {info['doctor']}"
            )

        # General advice categories
        advice_map = {
            "fever": "Fever is often a sign of infection. Stay hydrated, rest, and monitor your temperature. If it exceeds 103°F (39.4°C) or lasts more than 3 days, see a doctor.",
            "headache": "Headaches can be caused by stress, dehydration, or eye strain. Try resting in a dark room and drinking water. Seek immediate care if it's sudden and severe.",
            "stomach": "Stomach pain may be due to indigestion, infection, or more serious issues. Stick to a bland diet (BRAT: Bananas, Rice, Applesauce, Toast) and stay hydrated.",
            "cough": "Coughs can be viral or bacterial. Honey and warm liquids can soothe a sore throat. If you have difficulty breathing, seek help immediately.",
            "diet": "A balanced diet rich in fruits, vegetables, lean proteins, and whole grains is essential for long-term health.",
            "exercise": "Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week."
        }

        for key, advice in advice_map.items():
            if key in msg:
                return f"💡 **Advice on {key.capitalize()}:**\n\n{advice}"

        return (
            "I'm not quite sure about that. I can provide detailed information on over 40 diseases, explain symptoms, or give general health tips.\n\n"
            "Try asking about a specific condition like 'Tell me about Dengue' or 'What are the symptoms of Diabetes?'"
        )

    # ---------------- Sidebar Buttons ----------------
    # ---------------- Sidebar Buttons ----------------
    def add_sidebar_buttons(self):
        self.btn_home = SidebarButton(
            self.sidebar, "Home", ICONS["home"],
            command=self.show_home
        )
        self.btn_home.pack(fill="x")

        self.btn_diag = SidebarButton(
            self.sidebar, "Diagnosis", ICONS["diagnosis"],
            command=self.show_diagnosis
        )
        self.btn_diag.pack(fill="x")

        self.btn_hist = SidebarButton(
            self.sidebar, "History", ICONS["history"],
            command=self.show_history
        )
        self.btn_hist.pack(fill="x")

        self.btn_sett = SidebarButton(
            self.sidebar, "Settings", ICONS["settings"],
            command=self.show_settings
        )
        self.btn_sett.pack(fill="x")
        
        self.sidebar_buttons = [self.btn_home, self.btn_diag, self.btn_hist, self.btn_sett]

    # ==================================================
    #  PAGE SWITCHER
    # ==================================================
    def switch_page(self, frame_builder, title, active_btn):
        if self.active_page:
            self.active_page.destroy()

        self.page_title.config(text=title)
        
        # Update sidebar active states
        for btn in self.sidebar_buttons:
            btn.set_active(False)
        active_btn.set_active(True)

        self.active_page = frame_builder()
        self.active_page.pack(fill="both", expand=True, padx=40, pady=(0, 40))

    # ----------------- Pages -----------------

    def show_home(self):
        def build():
            frame = GlassFrame(self.content)
            
            # Welcome Illustration / Icon Placeholder
            tk.Label(
                frame.inner,
                text="👋",
                font=("Segoe UI", 48),
                bg=frame.inner["bg"]
            ).pack(pady=(20, 10))

            tk.Label(
                frame.inner,
                text="Welcome to AI Doctor",
                font=("Segoe UI", 28, "bold"),
                bg=frame.inner["bg"],
                fg=THEME["text"],
            ).pack(pady=10)

            tk.Label(
                frame.inner,
                text="Your intelligent health companion powered by machine learning.",
                font=("Segoe UI", 14),
                bg=frame.inner["bg"],
                fg=THEME["subtext"],
            ).pack(pady=10)
            
            # Quick Stats or Info Cards
            stats_frame = tk.Frame(frame.inner, bg=frame.inner["bg"])
            stats_frame.pack(pady=30, fill="x")
            
            def create_card(parent, title, desc):
                card = tk.Frame(parent, bg=THEME["accent_light"], padx=20, pady=20)
                card.pack(side="left", expand=True, fill="both", padx=10)
                tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=THEME["accent_light"], fg=THEME["accent"]).pack(anchor="w")
                tk.Label(card, text=desc, font=("Segoe UI", 10), bg=THEME["accent_light"], fg=THEME["subtext"], justify="left", wraplength=150).pack(anchor="w", pady=(5, 0))

            create_card(stats_frame, "Precision", "Our ensemble model uses 5+ algorithms for high accuracy.")
            create_card(stats_frame, "Speed", "Get instant predictions based on your symptoms.")
            create_card(stats_frame, "History", "Keep track of all your previous health checks.")

            return frame

        self.switch_page(build, "Home", self.btn_home)

    def show_diagnosis(self):
        # This will be overridden by the injected method later
        pass

    def show_history(self):
        # This will be overridden by the injected method later
        pass

    def show_settings(self):
        # This will be overridden by the injected method later
        pass


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
TRAIN_CSV_PATH = r"Training.csv"

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

# Silence downcasting warning
pd.set_option('future.no_silent_downcasting', True)
df = df.replace({'prognosis': mapping})

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
# TRAIN_CSV_PATH = r"Training.csv"
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
            frame = GlassFrame(self.content, padding=30)

            # ------------------ Form Layout ------------------
            form_frame = tk.Frame(frame.inner, bg=frame.inner["bg"])
            form_frame.pack(fill="both", expand=True)

            left_side = tk.Frame(form_frame, bg=frame.inner["bg"])
            left_side.pack(side="left", fill="both", expand=True, padx=(0, 20))

            right_side = tk.Frame(form_frame, bg=frame.inner["bg"])
            right_side.pack(side="right", fill="both", expand=True)

            # --- Left Side: Input ---
            tk.Label(
                left_side, text="Patient Information",
                font=("Segoe UI", 14, "bold"),
                bg=left_side["bg"], fg=THEME["text"]
            ).pack(anchor="w", pady=(0, 15))

            tk.Label(
                left_side, text="Patient Name",
                font=("Segoe UI", 10),
                bg=left_side["bg"], fg=THEME["subtext"]
            ).pack(anchor="w")

            name_entry = ttk.Entry(left_side, width=40)
            name_entry.pack(anchor="w", pady=(5, 20))

            tk.Label(
                left_side, text="Select Symptoms",
                font=("Segoe UI", 10),
                bg=left_side["bg"], fg=THEME["subtext"]
            ).pack(anchor="w", pady=(0, 5))

            choices = sorted(symptom_list)
            symptom_vars = []

            for i in range(5):
                var = tk.StringVar()
                box = ttk.Combobox(left_side, textvariable=var, values=choices, width=45)
                box.set(f"Symptom {i+1}")
                box.pack(anchor="w", pady=5)
                symptom_vars.append(var)

            # --- Right Side: Results ---
            tk.Label(
                right_side, text="Diagnosis Results",
                font=("Segoe UI", 14, "bold"),
                bg=right_side["bg"], fg=THEME["text"]
            ).pack(anchor="w", pady=(0, 15))

            result_box = tk.Frame(right_side, bg=THEME["accent_light"], padx=20, pady=20)
            result_box.pack(fill="both", expand=True)

            result_label = tk.Label(
                result_box,
                text="Enter details and click predict to see results.",
                font=("Segoe UI", 11),
                bg=THEME["accent_light"],
                fg=THEME["subtext"],
                wraplength=350,
                justify="left"
            )
            result_label.pack(fill="both", expand=True)

            # ------------------ Prediction Logic ------------------
            import time

            def predict():
                name = name_entry.get().strip()
                selected = [v.get() for v in symptom_vars if v.get() not in ["", "Symptom 1", "Symptom 2", "Symptom 3", "Symptom 4", "Symptom 5"]]

                if name == "":
                    result_label.config(text="⚠ Please enter patient name.", fg="#EF4444")
                    return

                if len(selected) == 0:
                    result_label.config(text="⚠ Select at least one symptom.", fg="#EF4444")
                    return

                # Build input vector
                vector = [1 if s in selected else 0 for s in symptom_list]

                # Start loading
                result_label.config(text="🔄 Analyzing symptoms... please wait.", fg=THEME["accent"])
                
                def run_prediction():
                    time.sleep(1.5)  # Simulated processing delay

                    try:
                        vector_scaled = scaler.transform([vector])
                        probs = best_model.predict_proba(vector_scaled)[0]
                        top3 = probs.argsort()[-3:][::-1]
                        main_disease = disease_list[top3[0]]

                        # Log to excel
                        save_to_excel_log(name, selected + [""]*(5 - len(selected)), main_disease)

                        info = disease_info.get(main_disease, {})
                        
                        res_str = f"🎯 PROBABLE DIAGNOSIS: {main_disease.upper()}\n"
                        res_str += f"Confidence: {probs[top3[0]]*100:.1f}%\n\n"
                        res_str += f"Other possibilities:\n"
                        res_str += f"• {disease_list[top3[1]]} ({probs[top3[1]]*100:.1f}%)\n"
                        res_str += f"• {disease_list[top3[2]]} ({probs[top3[2]]*100:.1f}%)\n\n"
                        res_str += f"💡 EXPLANATION:\n{info.get('explanation', 'N/A')}\n\n"
                        res_str += f"🏥 ADVICE:\n{info.get('homecare', 'Consult a professional.')}"

                        result_label.config(text=res_str, fg=THEME["text"], justify="left")
                    except Exception as e:
                        result_label.config(text=f"Error: {str(e)}", fg="#EF4444")

                threading.Thread(target=run_prediction).start()

            # ------------------ Predict Button ------------------
            predict_btn = tk.Button(
                left_side,
                text="Run Diagnosis",
                font=("Segoe UI", 12, "bold"),
                bg=THEME["accent"],
                fg="white",
                activebackground=THEME["accent_hover"],
                activeforeground="white",
                cursor="hand2",
                relief="flat",
                padx=30,
                pady=12,
                command=predict
            )
            predict_btn.pack(anchor="w", pady=20)

            return frame

        self.switch_page(build, "Diagnosis", self.btn_diag)

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
            frame = GlassFrame(self.content, padding=25)

            file = "prediction_log.xlsx"
            if not os.path.exists(file):
                tk.Label(
                    frame.inner,
                    text="No history found yet. Start by running a diagnosis!",
                    font=("Segoe UI", 12),
                    bg=frame.inner["bg"],
                    fg=THEME["subtext"]
                ).pack(pady=50)
                return frame

            # Load Excel
            try:
                df_log = pd.read_excel(file)
                df_log = df_log.sort_index(ascending=False) # Recent first
            except Exception as e:
                tk.Label(frame.inner, text=f"Error loading history: {e}", bg=frame.inner["bg"], fg="red").pack()
                return frame

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
            cols_to_show = ["Timestamp", "Patient Name", "Result"]
            for col, column_name in enumerate(cols_to_show):
                tk.Label(
                    table_frame,
                    text=column_name,
                    font=("Segoe UI", 11, "bold"),
                    bg=THEME["accent_light"],
                    fg=THEME["accent"],
                    padx=15,
                    pady=10,
                    width=20 if column_name != "Timestamp" else 25
                ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

            # ---------------- ROWS ----------------
            for r, row_data in enumerate(df_log[cols_to_show].values, start=1):
                for c, cell in enumerate(row_data):
                    tk.Label(
                        table_frame,
                        text=str(cell),
                        font=("Segoe UI", 10),
                        bg=frame.inner["bg"],
                        fg=THEME["text"],
                        padx=15,
                        pady=8,
                        anchor="w"
                    ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

            return frame

        self.switch_page(build, "Prediction History", self.btn_hist)

    AIDoctorApp.show_history = history_page

add_history_page_to_app()

# ======================================================
#  SETTINGS PAGE (Dark Mode Toggle)
# ======================================================

def add_settings_page_to_app():

    def settings_page(self):
        def build():
            frame = GlassFrame(self.content, padding=30)

            # ------------------ Appearance ------------------
            tk.Label(
                frame.inner, text="Appearance",
                font=("Segoe UI", 14, "bold"),
                bg=frame.inner["bg"], fg=THEME["text"]
            ).pack(anchor="w", pady=(0, 20))

            def toggle_theme():
                global CURRENT_THEME, THEME
                CURRENT_THEME = MODERN_THEME["dark"] if theme_var.get() == 1 else MODERN_THEME["light"]
                THEME = CURRENT_THEME
                self.rebuild_ui()

            theme_var = tk.IntVar(value=1 if CURRENT_THEME == MODERN_THEME["dark"] else 0)

            # Modern-style toggle (simplified for Tkinter)
            toggle_container = tk.Frame(frame.inner, bg=frame.inner["bg"])
            toggle_container.pack(fill="x", pady=10)
            
            tk.Checkbutton(
                toggle_container,
                text=" Enable Dark Mode",
                font=("Segoe UI", 11),
                variable=theme_var,
                bg=frame.inner["bg"],
                fg=THEME["text"],
                activebackground=frame.inner["bg"],
                activeforeground=THEME["text"],
                command=toggle_theme,
                selectcolor=frame.inner["bg"] if CURRENT_THEME == MODERN_THEME["light"] else THEME["sidebar"]
            ).pack(side="left")

            # ------------------ Info ------------------
            tk.Frame(frame.inner, bg=THEME["border"], height=1).pack(fill="x", pady=40)
            
            tk.Label(
                frame.inner, text="About AI Doctor",
                font=("Segoe UI", 14, "bold"),
                bg=frame.inner["bg"], fg=THEME["text"]
            ).pack(anchor="w", pady=(0, 10))

            about_text = (
                "Version: 2.0.0 (Modern Edition)\n"
                "Engine: Ensemble ML (RF, XGB, SVM, LR, GB)\n"
                "UI: Custom Glassmorphism System\n\n"
                "This application is designed for educational purposes and provides preliminary disease "
                "predictions based on reported symptoms. Always consult a medical professional."
            )
            
            tk.Label(
                frame.inner, text=about_text,
                font=("Segoe UI", 10),
                bg=frame.inner["bg"], fg=THEME["subtext"],
                justify="left"
            ).pack(anchor="w")

            return frame

        self.switch_page(build, "Settings", self.btn_sett)

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
