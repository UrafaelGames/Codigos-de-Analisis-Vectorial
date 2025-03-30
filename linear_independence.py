import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis Avanzado de Vectores")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Disabled.TEntry', foreground='gray')
        self.style.map('TButton', 
                      foreground=[('active', '#ffffff'), ('disabled', '#cccccc')],
                      background=[('active', '#3498db'), ('disabled', '#bdc3c7')])
        
        
        # Variables
        self.vectors = []
        self.dark_mode = False
        
        # Widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título y controles superiores
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="🔍 Análisis Avanzado de Vectores en ℝ³",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        # Botón modo oscuro
        ttk.Button(
            header_frame,
            text="🌙 Modo Oscuro",
            command=self.toggle_dark_mode,
            style='TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # Panel de entrada
        input_panel = ttk.LabelFrame(scrollable_frame, text=" Entrada de Vectores ", padding=15)
        input_panel.pack(fill=tk.X, padx=10, pady=5)
        
        # Contador de vectores
        self.counter_label = ttk.Label(
            input_panel,
            text="Vectores ingresados: 0/3",
            font=('Segoe UI', 10, 'bold'),
            foreground='#2c3e50'
        )
        self.counter_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Entrada de vector
        entry_frame = ttk.Frame(input_panel)
        entry_frame.pack(fill=tk.X)
        
        ttk.Label(entry_frame, text="Vector (x, y, z):").pack(side=tk.LEFT)
        
        self.vector_entry = ttk.Entry(entry_frame, width=30)
        self.vector_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.vector_entry.bind("<Return>", self.add_vector)
        
        # Botones de acción
        button_frame = ttk.Frame(input_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.add_button = ttk.Button(
            button_frame,
            text="➕ Agregar Vector",
            command=self.add_vector,
            style='TButton'
        )
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = ttk.Button(
            button_frame,
            text="🔍 Analizar",
            command=self.analyze_vectors,
            state=tk.DISABLED,
            style='TButton'
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ Limpiar Todo",
            command=self.clear_vectors,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Visualización de vectores
        vector_display_frame = ttk.LabelFrame(scrollable_frame, text=" Vectores Ingresados ", padding=10)
        vector_display_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.vector_display = scrolledtext.ScrolledText(
            vector_display_frame,
            width=60,
            height=5,
            font=('Consolas', 10),
            wrap=tk.NONE,
            bg='white',
            relief=tk.FLAT
        )
        self.vector_display.pack(fill=tk.BOTH, expand=True)
        
        # Panel de resultados
        results_frame = ttk.LabelFrame(scrollable_frame, text=" Resultados del Análisis ", padding=10)
        results_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de resultados
        result_tab = ttk.Frame(notebook)
        notebook.add(result_tab, text="📊 Resultados")
        
        self.result_text = tk.Text(
            result_tab,
            width=60,
            height=8,
            font=('Segoe UI', 10),
            wrap=tk.WORD,
            bg='white',
            padx=5,
            pady=5,
            relief=tk.FLAT
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de explicación
        explanation_tab = ttk.Frame(notebook)
        notebook.add(explanation_tab, text="📚 Explicación")
        
        self.explanation_text = tk.Text(
            explanation_tab,
            width=60,
            height=8,
            font=('Segoe UI', 9),
            wrap=tk.WORD,
            bg='#f9f9f9',
            padx=5,
            pady=5,
            relief=tk.FLAT
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.insert(tk.END, "Ingrese exactamente 3 vectores para analizar...")
        self.explanation_text.config(state=tk.DISABLED)
        
        # Gráfico 3D
        graph_frame = ttk.LabelFrame(scrollable_frame, text=" Visualización 3D ", padding=10)
        graph_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor='#f0f2f5')
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_empty_plot()
    
    def draw_empty_plot(self):
        self.ax.clear()
        self.ax.set_title("Visualización de Vectores 3D", pad=20)
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_zlabel('Eje Z')
        self.ax.text(0, 0, 0, "Ingrese 3 vectores\npara visualizar", 
                    ha='center', va='center', fontsize=10, color='gray')
        self.canvas.draw()
    
    def draw_vectors(self):
        self.ax.clear()
        
        # Configuración de ejes
        self.ax.set_title("Visualización de Vectores 3D", pad=20)
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_zlabel('Eje Z')
        
        # Origen
        origin = [0, 0, 0]
        
        # Dibujar cada vector
        colors = ['r', 'g', 'b']
        labels = ['Vector 1', 'Vector 2', 'Vector 3']
        
        for i, (vector, color, label) in enumerate(zip(self.vectors, colors, labels)):
            self.ax.quiver(*origin, *vector, color=color, arrow_length_ratio=0.1, label=label)
            # Añadir etiqueta al final del vector
            self.ax.text(*vector, f"v{i+1}", color=color)
        
        # Ajustar límites de los ejes
        max_val = max(max(abs(val) for val in vector) for vector in self.vectors) + 1
        self.ax.set_xlim([-max_val, max_val])
        self.ax.set_ylim([-max_val, max_val])
        self.ax.set_zlim([-max_val, max_val])
        
        # Leyenda
        self.ax.legend()
        
        self.canvas.draw()
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Estilo oscuro
            bg_color = '#2c3e50'
            fg_color = '#ecf0f1'
            entry_bg = '#34495e'
            self.style.configure('.', background=bg_color, foreground=fg_color)
            self.style.configure('TFrame', background=bg_color)
            self.style.configure('TLabel', background=bg_color, foreground=fg_color)
            self.style.configure('Title.TLabel', foreground='#3498db')
            self.root.configure(background=bg_color)
            self.vector_display.configure(bg=entry_bg, fg=fg_color)
            self.result_text.configure(bg=entry_bg, fg=fg_color)
            self.explanation_text.configure(bg='#34495e', fg=fg_color)
            self.figure.set_facecolor('#34495e')
            self.ax.set_facecolor('#34495e')
            self.ax.tick_params(colors=fg_color)
            self.ax.xaxis.label.set_color(fg_color)
            self.ax.yaxis.label.set_color(fg_color)
            self.ax.zaxis.label.set_color(fg_color)
            self.ax.title.set_color(fg_color)
        else:
            # Estilo claro
            bg_color = '#f0f2f5'
            fg_color = '#2c3e50'
            entry_bg = 'white'
            self.style.configure('.', background=bg_color, foreground=fg_color)
            self.style.configure('TFrame', background=bg_color)
            self.style.configure('TLabel', background=bg_color, foreground=fg_color)
            self.style.configure('Title.TLabel', foreground='#2c3e50')
            self.root.configure(background=bg_color)
            self.vector_display.configure(bg=entry_bg, fg='black')
            self.result_text.configure(bg=entry_bg, fg='black')
            self.explanation_text.configure(bg='#f9f9f9', fg='black')
            self.figure.set_facecolor('#f0f2f5')
            self.ax.set_facecolor('#f0f2f5')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.zaxis.label.set_color('black')
            self.ax.title.set_color('black')
        
        if len(self.vectors) == 3:
            self.draw_vectors()
        else:
            self.draw_empty_plot()
    
    def add_vector(self, event=None):
        if len(self.vectors) >= 3:
            messagebox.showwarning("Límite alcanzado", "Ya has ingresado 3 vectores (máximo permitido)")
            return
            
        vec_input = self.vector_entry.get().strip()
        if not vec_input:
            return
            
        try:
            # Validar que sean exactamente 3 componentes
            components = [x.strip() for x in vec_input.split(",")]
            if len(components) != 3:
                raise ValueError("Debe ingresar exactamente 3 componentes (x, y, z)")
                
            vector = [float(x) for x in components]
            self.vectors.append(vector)
            self.vector_display.insert(tk.END, f"🔹 Vector {len(self.vectors)}: {vector}\n")
            self.vector_entry.delete(0, tk.END)
            
            # Actualizar contador
            self.counter_label.config(text=f"Vectores ingresados: {len(self.vectors)}/3")
            
            # Habilitar análisis cuando haya 3 vectores
            if len(self.vectors) == 3:
                self.analyze_button.config(state=tk.NORMAL)
                self.vector_entry.config(state=tk.DISABLED, style='Disabled.TEntry')
                self.add_button.config(state=tk.DISABLED)
                self.explanation_text.config(state=tk.NORMAL)
                self.explanation_text.delete(1.0, tk.END)
                self.explanation_text.insert(tk.END, "Presione 'Analizar' para ver los resultados...")
                self.explanation_text.config(state=tk.DISABLED)
                self.draw_vectors()
                
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}\n\nEjemplo correcto: 1.5, 2.0, -3.2")
    
    def analyze_vectors(self):
        if len(self.vectors) != 3:
            messagebox.showwarning("Error", "Debe ingresar exactamente 3 vectores")
            return
            
        try:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.explanation_text.config(state=tk.NORMAL)
            self.explanation_text.delete(1.0, tk.END)
            
            matrix = np.array(self.vectors).T
            
            # Encabezado del resultado
            self.result_text.insert(tk.END, "=== ANÁLISIS DE INDEPENDENCIA LINEAL ===\n\n", 'header')
            self.result_text.insert(tk.END, "🔹 Vectores ingresados:\n", 'subheader')
            for i, vec in enumerate(self.vectors, 1):
                self.result_text.insert(tk.END, f"   Vector {i}: {vec}\n")
            self.result_text.insert(tk.END, "\n")
            
            # Método del determinante (siempre para 3 vectores en ℝ³)
            det = np.linalg.det(matrix)
            self.result_text.insert(tk.END, "🔹 Método utilizado: Determinante\n", 'subheader')
            self.result_text.insert(tk.END, f"   Valor del determinante: {det:.6f}\n\n")
            
            if not np.isclose(det, 0, atol=1e-10):
                self.result_text.insert(tk.END, "✅ CONCLUSIÓN: Los vectores son LINEALMENTE INDEPENDIENTES\n\n", 'success')
                explanation = self.get_determinant_explanation(matrix, det)
            else:
                self.result_text.insert(tk.END, "❌ CONCLUSIÓN: Los vectores son LINEALMENTE DEPENDIENTES\n\n", 'error')
                explanation = self.get_determinant_explanation(matrix, det)
            
            # Mostrar matriz
            self.result_text.insert(tk.END, "🔹 Matriz de vectores (como columnas):\n", 'subheader')
            self.result_text.insert(tk.END, str(matrix) + "\n")
            
            # Configurar estilos de texto
            self.result_text.tag_config('header', font=('Segoe UI', 11, 'bold'))
            self.result_text.tag_config('subheader', font=('Segoe UI', 10, 'bold'))
            self.result_text.tag_config('success', foreground='#27ae60', font=('Segoe UI', 10, 'bold'))
            self.result_text.tag_config('error', foreground='#e74c3c', font=('Segoe UI', 10, 'bold'))
            self.result_text.config(state=tk.DISABLED)
            
            # Mostrar explicación
            self.explanation_text.insert(tk.END, explanation)
            self.explanation_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis:\n{str(e)}")
    
    def get_determinant_explanation(self, matrix, det):
        explanation = "📚 EXPLICACIÓN MATEMÁTICA\n\n"
        explanation += "Para tres vectores en el espacio tridimensional, calculamos el determinante de la matriz 3×3 formada por estos vectores como columnas.\n\n"
        
        explanation += "1️⃣ Construcción de la matriz:\n"
        explanation += "La matriz se forma usando los vectores como columnas:\n"
        explanation += str(matrix) + "\n\n"
        
        explanation += f"2️⃣ Cálculo del determinante: det(A) = {det:.6f}\n\n"
        
        if np.isclose(det, 0, atol=1e-10):
            explanation += "3️⃣ Interpretación (determinante = 0):\n"
            explanation += "   - Los vectores son coplanares (están en el mismo plano)\n"
            explanation += "   - Existe una relación lineal entre ellos\n"
            explanation += "   - El sistema tiene infinitas soluciones\n"
        else:
            explanation += "3️⃣ Interpretación (determinante ≠ 0):\n"
            explanation += "   - Los vectores son linealmente independientes\n"
            explanation += "   - Generan todo el espacio tridimensional\n"
            explanation += "   - Forman una base para ℝ³\n"
        
        explanation += "\n🔍 Interpretación geométrica:\n"
        explanation += "El valor absoluto del determinante representa el volumen del paralelepípedo formado por los tres vectores. "
        explanation += "Si el volumen es cero, los vectores están en el mismo plano."
        
        return explanation
    
    def clear_vectors(self):
        self.vectors = []
        self.vector_display.delete(1.0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, "Ingrese exactamente 3 vectores para analizar...")
        self.explanation_text.config(state=tk.DISABLED)
        self.counter_label.config(text="Vectores ingresados: 0/3")
        self.vector_entry.config(state=tk.NORMAL)
        self.add_button.config(state=tk.NORMAL)
        self.analyze_button.config(state=tk.DISABLED)
        self.vector_entry.delete(0, tk.END)
        self.draw_empty_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorApp(root)
    root.mainloop()