import tkinter as tk
from tkinter import ttk, messagebox
import clips
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Tuple, Set

class PlantExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto de Diagnóstico de Plantas")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f0")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Expert System
        self.expert_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.expert_tab, text="Sistema Experto")
        
        # Tab 2: Fuzzy Logic System
        self.fuzzy_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fuzzy_tab, text="Recomendación de Plantas")
        
        # Initialize expert system tab
        self.init_expert_system_tab()
        
        # Initialize fuzzy logic tab
        self.init_fuzzy_logic_tab()
        
        # Create the fuzzy logic system
        self.create_fuzzy_system()
    
    def init_expert_system_tab(self):
        # Symptom categories and options
        self.symptom_categories = {
            "Color de hojas": ["verde pálido", "amarillo uniforme", "púrpura o rojizo", "bordes secos o quemados"],
            "Condición de hojas": ["marchitas", "crecimiento atrofiado"],
            "Condición de tallo": ["débil o quebradizo", "engrosado"],
            "Crecimiento y desarrollo": ["maduración tardía", "floración ausente"]
        }
        
        # Selected symptoms
        self.selected_symptoms = {}
        
        # Create the CLIPS environment
        self.env = self.create_expert_system()
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.expert_tab, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="Sistema Experto de Diagnóstico de Plantas",
            font=("Helvetica", 16, "bold"),
            foreground="#2e7d32"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="Identifique deficiencias de nutrientes en sus plantas basado en síntomas observables",
            font=("Helvetica", 10),
            foreground="#555555"
        )
        subtitle_label.pack()
        
        # Create content frame with two columns
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Symptom selection
        self.left_frame = ttk.LabelFrame(content_frame, text="Selección de Síntomas", padding=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create symptom selection widgets
        self.create_symptom_selection()
        
        # Right column - Results
        self.right_frame = ttk.LabelFrame(content_frame, text="Resultados del Diagnóstico", padding=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create results display
        self.results_text = tk.Text(self.right_frame, wrap=tk.WORD, height=20, width=40)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame, padding=(0, 20, 0, 0))
        buttons_frame.pack(fill=tk.X)
        
        # Reset button
        reset_button = ttk.Button(
            buttons_frame, 
            text="Reiniciar", 
            command=self.reset_form
        )
        reset_button.pack(side=tk.LEFT)
        
        # Diagnose button
        diagnose_button = ttk.Button(
            buttons_frame, 
            text="Diagnosticar", 
            command=self.run_diagnosis
        )
        diagnose_button.pack(side=tk.RIGHT)
        
        # Create custom style for the accent button
        style = ttk.Style()
        style.configure("Accent.TButton", background="#2e7d32", foreground="white")
        
        # Footer
        footer_frame = ttk.Frame(self.main_frame, padding=(0, 20, 0, 0))
        footer_frame.pack(fill=tk.X)
        
        footer_text = ttk.Label(
            footer_frame,
            text="Este sistema experto diagnostica deficiencias de nitrógeno, potasio y fósforo basado en síntomas observables.\n"
                 "Para diagnósticos más precisos, considere consultar con un agrónomo o especialista en plantas.",
            font=("Helvetica", 8),
            foreground="#777777",
            justify=tk.CENTER
        )
        footer_text.pack()
    
    def init_fuzzy_logic_tab(self):
        # Create main frame for fuzzy logic tab
        self.fuzzy_main_frame = ttk.Frame(self.fuzzy_tab, padding=20)
        self.fuzzy_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_frame = ttk.Frame(self.fuzzy_main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="Sistema de Recomendación de Plantas",
            font=("Helvetica", 16, "bold"),
            foreground="#2e7d32"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="Reciba recomendaciones de plantas basadas en el pH del suelo y la frecuencia de riego",
            font=("Helvetica", 10),
            foreground="#555555"
        )
        subtitle_label.pack()
        
        # Create content frame with two columns
        content_frame = ttk.Frame(self.fuzzy_main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Input parameters
        self.fuzzy_left_frame = ttk.LabelFrame(content_frame, text="Parámetros de Entrada", padding=10)
        self.fuzzy_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # pH input
        ph_frame = ttk.Frame(self.fuzzy_left_frame, padding=(0, 5))
        ph_frame.pack(fill=tk.X, pady=10)
        
        ph_label = ttk.Label(
            ph_frame, 
            text="Nivel de pH del suelo (0-14):",
            font=("Helvetica", 10, "bold")
        )
        ph_label.pack(anchor=tk.W)
        
        self.ph_var = tk.StringVar(value="7.0")
        ph_entry = ttk.Entry(
            ph_frame,
            textvariable=self.ph_var,
            width=10
        )
        ph_entry.pack(fill=tk.X, pady=(5, 0))
        
        # pH scale
        ph_scale_frame = ttk.Frame(self.fuzzy_left_frame)
        ph_scale_frame.pack(fill=tk.X, pady=5)
        
        ph_scale_label1 = ttk.Label(ph_scale_frame, text="Ácido")
        ph_scale_label1.pack(side=tk.LEFT)
        
        ph_scale = ttk.Scale(
            ph_scale_frame,
            from_=0,
            to=14,
            orient=tk.HORIZONTAL,
            variable=self.ph_var,
            command=lambda v: self.ph_var.set(f"{float(v):.1f}")
        )
        ph_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ph_scale_label2 = ttk.Label(ph_scale_frame, text="Alcalino")
        ph_scale_label2.pack(side=tk.RIGHT)
        
        # Separator
        ttk.Separator(self.fuzzy_left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Riego input
        riego_frame = ttk.Frame(self.fuzzy_left_frame, padding=(0, 5))
        riego_frame.pack(fill=tk.X, pady=10)
        
        riego_label = ttk.Label(
            riego_frame, 
            text="Frecuencia de riego (0-10):",
            font=("Helvetica", 10, "bold")
        )
        riego_label.pack(anchor=tk.W)
        
        self.riego_var = tk.StringVar(value="5.0")
        riego_entry = ttk.Entry(
            riego_frame,
            textvariable=self.riego_var,
            width=10
        )
        riego_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Riego scale
        riego_scale_frame = ttk.Frame(self.fuzzy_left_frame)
        riego_scale_frame.pack(fill=tk.X, pady=5)
        
        riego_scale_label1 = ttk.Label(riego_scale_frame, text="Bajo")
        riego_scale_label1.pack(side=tk.LEFT)
        
        riego_scale = ttk.Scale(
            riego_scale_frame,
            from_=0,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.riego_var,
            command=lambda v: self.riego_var.set(f"{float(v):.1f}")
        )
        riego_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        riego_scale_label2 = ttk.Label(riego_scale_frame, text="Alto")
        riego_scale_label2.pack(side=tk.RIGHT)
        
        # Buttons
        buttons_frame = ttk.Frame(self.fuzzy_left_frame, padding=(0, 20, 0, 0))
        buttons_frame.pack(fill=tk.X)
        
        # Calculate button
        calculate_button = ttk.Button(
            buttons_frame, 
            text="Calcular Recomendación", 
            command=self.calculate_recommendation
        )
        calculate_button.pack(side=tk.RIGHT)
        
        # Right column - Results and graph
        self.fuzzy_right_frame = ttk.LabelFrame(content_frame, text="Resultados y Gráfico", padding=10)
        self.fuzzy_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Results frame
        results_frame = ttk.Frame(self.fuzzy_right_frame)
        results_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.recommendation_var = tk.StringVar(value="")
        recommendation_label = ttk.Label(
            results_frame,
            textvariable=self.recommendation_var,
            font=("Helvetica", 12),
            foreground="#2e7d32",
            wraplength=400
        )
        recommendation_label.pack(fill=tk.X)
        
        # Graph frame
        self.graph_frame = ttk.Frame(self.fuzzy_right_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer_frame = ttk.Frame(self.fuzzy_main_frame, padding=(0, 20, 0, 0))
        footer_frame.pack(fill=tk.X)
        
        footer_text = ttk.Label(
            footer_frame,
            text="Este sistema utiliza lógica difusa para recomendar tipos de plantas basado en el pH del suelo y la frecuencia de riego.\n"
                 "Las recomendaciones incluyen cactus, rosales y helechos según las condiciones ambientales.",
            font=("Helvetica", 8),
            foreground="#777777",
            justify=tk.CENTER
        )
        footer_text.pack()
    
    def create_symptom_selection(self):
        """Create the symptom selection widgets"""
        for i, (category, symptoms) in enumerate(self.symptom_categories.items()):
            # Create frame for this category
            category_frame = ttk.Frame(self.left_frame, padding=(0, 5))
            category_frame.pack(fill=tk.X, pady=5)
            
            # Category label
            category_label = ttk.Label(
                category_frame, 
                text=f"{category}:",
                font=("Helvetica", 10, "bold")
            )
            category_label.pack(anchor=tk.W)
            
            # Combobox for symptom selection
            symptom_var = tk.StringVar()
            symptom_combobox = ttk.Combobox(
                category_frame, 
                textvariable=symptom_var,
                values=[""] + symptoms,
                width=40,
                state="readonly"
            )
            symptom_combobox.pack(fill=tk.X, pady=(5, 0))
            symptom_combobox.current(0)
            
            # Store the variable for later access
            self.selected_symptoms[category] = symptom_var
            
            # Add a separator except for the last item
            if i < len(self.symptom_categories) - 1:
                ttk.Separator(self.left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
    
    def create_expert_system(self):
        """Create the CLIPS expert system environment"""
        env = clips.Environment()
        env.clear()

        # Define templates
        env.build("""
            (deftemplate diagnostico (slot deficiencia (type STRING)))
        """)
        env.build("""
            (deftemplate sintoma (slot categoria (type STRING)) (slot caracteristica (type STRING)))
        """)
        env.build("""
            (deftemplate tratamiento (slot recomendacion (type STRING)))
        """)

        # Rules for nutrient deficiencies
        env.build("""
            (defrule nitrogeno-deficiencia
                (or (sintoma (categoria "Color de hojas") (caracteristica "verde pálido"))
                    (sintoma (categoria "Condición de hojas") (caracteristica "crecimiento atrofiado")))
                =>
                (assert (diagnostico (deficiencia "nitrogeno"))))
        """)
        env.build("""
            (defrule potasio-deficiencia
                (or (sintoma (categoria "Color de hojas") (caracteristica "bordes secos o quemados"))
                    (sintoma (categoria "Condición de tallo") (caracteristica "débil o quebradizo")))
                =>
                (assert (diagnostico (deficiencia "potasio"))))
        """)
        env.build("""
            (defrule fosforo-deficiencia
                (or (sintoma (categoria "Color de hojas") (caracteristica "púrpura o rojizo"))
                    (sintoma (categoria "Crecimiento y desarrollo") (caracteristica "maduración tardía")))
                =>
                (assert (diagnostico (deficiencia "fosforo"))))
        """)

        # Treatment rules
        env.build("""
            (defrule nitrogeno-tratamiento
                (diagnostico (deficiencia "nitrogeno"))
                =>
                (assert (tratamiento (recomendacion "Aplicar fertilizante con urea o nitrato de amonio"))))
        """)
        env.build("""
            (defrule potasio-tratamiento
                (diagnostico (deficiencia "potasio"))
                =>
                (assert (tratamiento (recomendacion "Añadir fertilizante rico en potasio, como ceniza de madera o sulfato de potasio"))))
        """)
        env.build("""
            (defrule fosforo-tratamiento
                (diagnostico (deficiencia "fosforo"))
                =>
                (assert (tratamiento (recomendacion "Incorporar fertilizantes con fosfato, como superfosfato de calcio"))))
        """)
        
        return env
    
    def create_fuzzy_system(self):
        """Create the fuzzy logic system for plant recommendation"""
        # Definición de los antecedentes (entradas)
        self.acidez = ctrl.Antecedent(np.arange(0, 14, 0.1), 'acidez')  # pH del suelo
        self.riego = ctrl.Antecedent(np.arange(0, 10, 0.1), 'riego')  # Frecuencia de riego

        # Definición del consecuente (salida)
        self.planta = ctrl.Consequent(np.arange(0, 5, 0.1), 'planta')  # Tipo de planta

        # Definir conjuntos difusos
        self.acidez['ácido'] = fuzz.trapmf(self.acidez.universe, [0, 0, 4.5, 6.5])
        self.acidez['neutro'] = fuzz.trapmf(self.acidez.universe, [4.5, 6.5, 8, 10])
        self.acidez['alcalino'] = fuzz.trapmf(self.acidez.universe, [8, 10, 14, 14])

        self.riego['bajo'] = fuzz.trapmf(self.riego.universe, [0, 0, 3, 4.5])
        self.riego['medio'] = fuzz.trapmf(self.riego.universe, [3, 4.5, 6, 7])
        self.riego['alto'] = fuzz.trapmf(self.riego.universe, [6, 7, 10, 10])

        self.planta['cactus'] = fuzz.trapmf(self.planta.universe, [0, 0, 0.7, 1.5])
        self.planta['rosal'] = fuzz.trapmf(self.planta.universe, [1, 1.5, 2.2, 3.3])
        self.planta['helecho'] = fuzz.trapmf(self.planta.universe, [2.5, 3.3, 4, 4.5])

        # # Definir reglas difusas
        # rule1 = ctrl.Rule(self.acidez['ácido'] & self.riego['alto'], self.planta['helecho'])
        # rule2 = ctrl.Rule(self.acidez['neutro'] & self.riego['medio'], self.planta['rosal'])
        # rule3 = ctrl.Rule(self.acidez['alcalino'] & self.riego['bajo'], self.planta['cactus'])

        # # Crear el sistema de control
        # self.planta_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
        # self.sistema = ctrl.ControlSystemSimulation(self.planta_ctrl)

        # Definir reglas
        rules = [
            ctrl.Rule(self.acidez['ácido'] & self.riego['alto'], self.planta['helecho']),
            ctrl.Rule(self.acidez['ácido'] & self.riego['medio'], self.planta['helecho']),
            ctrl.Rule(self.acidez['ácido'] & self.riego['bajo'], self.planta['rosal']),
            ctrl.Rule(self.acidez['neutro'] & self.riego['alto'], self.planta['helecho']),
            ctrl.Rule(self.acidez['neutro'] & self.riego['medio'], self.planta['rosal']),
            ctrl.Rule(self.acidez['neutro'] & self.riego['bajo'], self.planta['rosal']),
            ctrl.Rule(self.acidez['alcalino'] & self.riego['alto'], self.planta['helecho']),
            ctrl.Rule(self.acidez['alcalino'] & self.riego['medio'], self.planta['rosal']),
            ctrl.Rule(self.acidez['alcalino'] & self.riego['bajo'], self.planta['cactus'])
        ]

        # Crear sistema de control
        self.planta_ctrl = ctrl.ControlSystem(rules)
        self.sistema = ctrl.ControlSystemSimulation(self.planta_ctrl)
    
    def calculate_recommendation(self):
        """Calculate plant recommendation based on pH and watering frequency"""
        try:
            # Get input values
            ph_value = float(self.ph_var.get())
            riego_value = float(self.riego_var.get())
            
            # Validate input ranges
            if not (0 <= ph_value <= 14):
                messagebox.showerror("Error", "El valor de pH debe estar entre 0 y 14.")
                return
            
            if not (0 <= riego_value <= 10):
                messagebox.showerror("Error", "La frecuencia de riego debe estar entre 0 y 10.")
                return

            # if ( ph_value < 6.5 and riego_value > 3 or ph_value < 6.5 and riego_value < 3 ):
            #     messagebox.showerror("Error", "El valor de pH debe estar entre 0 y 14 y la frecuencia de riego entre 0 y 10.")
            #     return
            
            # if ( ph_value < 10 and riego_value > 3 ):
            #     messagebox.showerror("Error", "El valor de pH debe estar entre 0 y 14 y la frecuencia de riego entre 0 y 10.")
            #     return
            
            # Set input values to the fuzzy system
            self.sistema.input['acidez'] = ph_value
            self.sistema.input['riego'] = riego_value
            
            # Compute the result
            self.sistema.compute()
            
            # Get the result
            resultado = self.sistema.output['planta']
            
            # Determine the plant type based on the result
            if resultado < 1.5:
                planta_recomendada = "Cactus"
                descripcion = "Los cactus son ideales para suelos alcalinos con baja frecuencia de riego."
            elif resultado < 3:
                planta_recomendada = "Rosal"
                descripcion = "Los rosales prefieren suelos neutros con frecuencia de riego media."
            else:
                planta_recomendada = "Helecho"
                descripcion = "Los helechos prosperan en suelos ácidos con alta frecuencia de riego."
            
            # Update the recommendation label
            self.recommendation_var.set(f"Planta recomendada: {planta_recomendada}\n\n{descripcion}\n\nValor numérico: {resultado:.2f}")
            
            # Update the graph
            self.update_graph(resultado)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
    
    def update_graph(self, resultado):
        """Update the fuzzy logic graph with the current result"""
        # Clear the graph frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Create a new figure
        fig, ax = plt.subplots(figsize=(6, 4)) 
        
        # Plot the membership functions
        self.planta.view(sim=self.sistema, ax=ax)
        
        # Add a vertical line at the result value
        ax.axvline(x=resultado, color='black', linestyle='-', linewidth=2)
        
        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
    
    def run_diagnosis(self):
        """Run the expert system diagnosis based on selected symptoms"""
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Reset the CLIPS environment
        self.env.reset()
        
        # Get selected symptoms
        selected = []
        for category, var in self.selected_symptoms.items():
            symptom = var.get()
            if symptom:
                selected.append((category, symptom))
                
        if not selected:
            messagebox.showinfo("Información", "Por favor seleccione al menos un síntoma para realizar el diagnóstico.")
            self.results_text.config(state=tk.DISABLED)
            return
        
        # Add selected symptoms to results
        self.results_text.insert(tk.END, "Síntomas seleccionados:\n")
        for category, symptom in selected:
            self.results_text.insert(tk.END, f"• {category}: {symptom}\n")
            # Assert the symptom in the CLIPS environment
            self.env.assert_string(f'(sintoma (categoria "{category}") (caracteristica "{symptom}"))')
        
        self.results_text.insert(tk.END, "\n")
        
        # Run the expert system
        self.env.run()
        
        # Get diagnoses and treatments
        deficiencies = {fact['deficiencia'] for fact in self.env.facts() if fact.template.name == 'diagnostico'}
        treatments = {fact['recomendacion'] for fact in self.env.facts() if fact.template.name == 'tratamiento'}
        
        # Display results
        if deficiencies:
            self.results_text.insert(tk.END, "Deficiencias detectadas:\n")
            for deficiency in deficiencies:
                self.results_text.insert(tk.END, f"• {deficiency.capitalize()}\n")
            
            self.results_text.insert(tk.END, "\nTratamientos recomendados:\n")
            for treatment in treatments:
                self.results_text.insert(tk.END, f"• {treatment}\n")
        else:
            self.results_text.insert(
                tk.END, 
                "No se detectaron deficiencias con los síntomas proporcionados.\n\n"
                "Considere seleccionar síntomas adicionales o consultar con un especialista."
            )
        
        self.results_text.config(state=tk.DISABLED)
    
    def reset_form(self):
        """Reset the form and clear results"""
        # Clear symptom selections
        for var in self.selected_symptoms.values():
            var.set("")
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        # Reset the CLIPS environment
        self.env.reset()


def main():
    root = tk.Tk()
    app = PlantExpertSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()