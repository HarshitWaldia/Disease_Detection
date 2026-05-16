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

        self.add_sidebar_buttons()

        # Start at home page
        self.show_home()

    # ---------------- Sidebar Buttons ----------------
    def add_sidebar_buttons(self):
        SidebarButton(
            self.sidebar, "Home", ICONS["home"],
            command=self.show_home
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "Diagnosis", ICONS["diagnosis"],
            command=self.show_diagnosis
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "History", ICONS["history"],
            command=self.show_history
        ).pack(fill="x")

        SidebarButton(
            self.sidebar, "Settings", ICONS["settings"],
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
#  PART 2 — ML MODEL + DIAGNOSIS PAGE + LOADING ANIMATION
# ======================================================

import pandas as pd
import numpy as np
import openpyxl
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

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

# Train the model ONCE
clf = RandomForestClassifier()
clf.fit(X, np.ravel(y))


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
                    time.sleep(1)  # Simulate processing delay
                    prediction = clf.predict([vector])[0]
                    result = disease_list[prediction]

                    save_to_excel_log(name, selected + [""]*(5-len(selected)), result)

                    self.loading = False
                    loading_label.config(text="")
                    result_label.config(text=f"Predicted Disease: {result}", fg=THEME["text"])

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
