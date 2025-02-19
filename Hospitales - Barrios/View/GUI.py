import tkinter as tk
from tkinter import ttk, messagebox
from config import CELL_SIZE
from utils.input_validator import InputValidator

class HospitalDistributionView:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Distribución de Hospitales")
        # **CAMBIOS DE DISEÑO**: Fondo base y configuración de estilos
        self.root.configure(bg='#f8f8f8')
        self.configure_styles()
        self.create_main_container()
        self.create_input_frame()
        
        # Área de simulación
        self.simulation_frame = ttk.LabelFrame(self.main_frame, text="Simulación", padding=10, relief="groove")
        self.simulation_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.simulation_container = None
        self.canvas = None
        self.assignments_frame = None

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Puedes usar 'default', 'clam', 'alt', etc.
        
        # Fuente y color de fondo
        style.configure('.', font=('Helvetica', 10), background='#f8f8f8')
        
        # Estilo para LabelFrames
        style.configure('TLabelframe', background='#f8f8f8', bordercolor='#cccccc')
        style.configure('TLabelframe.Label', font=('Helvetica', 10, 'bold'), foreground='#333333')
        
        # Estilo para Labels
        style.configure('TLabel', foreground='#333333')
        
        # Estilo para Buttons
        style.configure('TButton', foreground='#333333', background='#e6e6e6')
        
        # Estilo para la barra de progreso
        style.configure('Horizontal.TProgressbar', troughcolor='#e6e6e6', background='#4da6ff')

    def create_main_container(self):
        self.main_container = tk.Canvas(self.root, bg='#f8f8f8')
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_container.yview)
        self.main_container.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.main_container.pack(side="left", fill="both", expand=True)
        
        self.main_frame = ttk.Frame(self.main_container, padding=10)
        self.main_container.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Actualizar región de scroll
        self.main_frame.bind("<Configure>", lambda e: self.main_container.configure(scrollregion=self.main_container.bbox("all")))
    
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="Configuración", padding=10, relief="groove")
        input_frame.pack(fill="x", padx=10, pady=5)
        for i in range(2):
            input_frame.grid_columnconfigure(i, weight=1)
        
        title_label = ttk.Label(input_frame, text="Parámetros de la Simulación", style='TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(input_frame, text="Tamaño de la cuadrícula:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.grid_size_var = tk.StringVar(value="")
        self.grid_size_entry = ttk.Entry(input_frame, textvariable=self.grid_size_var, width=15)
        self.grid_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(input_frame, text="Número de barrios:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.neighborhoods_var = tk.StringVar(value="")
        self.neighborhoods_entry = ttk.Entry(input_frame, textvariable=self.neighborhoods_var, width=15)
        self.neighborhoods_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(input_frame, text="Número de hospitales:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.hospitals_var = tk.StringVar(value="")
        self.hospitals_entry = ttk.Entry(input_frame, textvariable=self.hospitals_var, width=15)
        self.hospitals_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        self.start_button = ttk.Button(input_frame, text="Iniciar Simulación")
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.reset_button = ttk.Button(input_frame, text="Reiniciar")
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(input_frame, orient='horizontal', length=200, mode='determinate', style='Horizontal.TProgressbar')
        self.progress_bar.grid(row=6, column=0, columnspan=2, pady=5)
        self.progress_bar['maximum'] = 100
    
    def get_input_values(self):
        return (self.grid_size_var.get(), self.neighborhoods_var.get(), self.hospitals_var.get())
    
    def display_error(self, message):
        messagebox.showerror("Error", message)
    
    def setup_simulation_area(self, n):
        if self.simulation_container:
            self.simulation_container.destroy()
        self.simulation_container = ttk.Frame(self.simulation_frame, padding=5)
        self.simulation_container.pack(fill="both", expand=True)
        
        canvas_width = n * CELL_SIZE
        canvas_height = n * CELL_SIZE
        self.canvas = tk.Canvas(self.simulation_container, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack(side="left", padx=10, pady=10)
        
        self.assignments_frame = ttk.LabelFrame(self.simulation_container, text="Asignaciones", padding=10, relief="groove")
        self.assignments_frame.pack(side="right", fill="y", padx=10, pady=10)
    
    def update_assignments(self, assignments):
        for widget in self.assignments_frame.winfo_children():
            widget.destroy()
        if assignments:
            for barrio, hospital in sorted(assignments.items()):
                label_text = f"Barrio {barrio} -> Hospital {hospital}"
                lbl = ttk.Label(self.assignments_frame, text=label_text)
                lbl.pack(anchor='w', pady=2)
        else:
            ttk.Label(self.assignments_frame, text="No se asignaron barrios.").pack()
    
    def set_progress(self, value):
        """Actualiza el valor de la barra de progreso."""
        self.progress_bar['value'] = value
        self.progress_bar.update_idletasks()
    
    def reset(self):
        """
        Reinicia la simulación:
          - Destruye todos los widgets dentro de simulation_frame.
          - Reinicia los valores de entrada a los predeterminados.
        """
        for widget in self.simulation_frame.winfo_children():
            widget.destroy()
        self.simulation_container = None
        self.canvas = None
        self.assignments_frame = None
        
        # Reiniciar los campos de entrada
        self.grid_size_var.set("")
        self.neighborhoods_var.set("")
        self.hospitals_var.set("")
        
        # Reiniciar la barra de progreso
        self.set_progress(0)