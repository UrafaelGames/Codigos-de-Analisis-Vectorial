import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D

class VectorProjectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyección Ortogonal de Vectores")
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
        self.style.configure('Footer.TLabel', font=('Segoe UI', 8), foreground='#7f8c8d')
        
        # Variables para los vectores
        self.vector_a = tk.StringVar()
        self.vector_b = tk.StringVar()
        
        # Widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame, 
            text="➡️ Proyección Ortogonal de Vectores en ℝⁿ",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        # Panel de entrada
        input_panel = ttk.LabelFrame(main_frame, text=" Entrada de Vectores ", padding=15)
        input_panel.pack(fill=tk.X, pady=5)
        
        # Entrada de vectores
        ttk.Label(input_panel, text="Vector a (x,y,z...):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_panel, textvariable=self.vector_a, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(input_panel, text="Vector b (x,y,z...):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_panel, textvariable=self.vector_b, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Frame para botones
        button_frame = ttk.Frame(input_panel)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botón de cálculo
        ttk.Button(
            button_frame,
            text="📐 Calcular Proyección",
            command=self.calculate_projection,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón de limpiar
        ttk.Button(
            button_frame,
            text="🧹 Limpiar Campos",
            command=self.clear_fields,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        results_frame = ttk.LabelFrame(main_frame, text=" Resultados ", padding=10)
        results_frame.pack(fill=tk.BOTH, pady=5, expand=True)
        
        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de resultados
        result_tab = ttk.Frame(notebook)
        notebook.add(result_tab, text="📊 Resultado")
        
        self.projection_label = ttk.Label(
            result_tab, 
            text="Proyección: ", 
            font=('Segoe UI', 11, 'bold'),
            foreground='#2c3e50'
        )
        self.projection_label.pack(anchor=tk.W, pady=5)
        
        # Explicación matemática
        explanation_tab = ttk.Frame(notebook)
        notebook.add(explanation_tab, text="📚 Explicación")
        
        self.explanation_text = scrolledtext.ScrolledText(
            explanation_tab,
            width=60,
            height=10,
            font=('Segoe UI', 9),
            wrap=tk.WORD,
            bg='#f9f9f9',
            padx=5,
            pady=5,
            relief=tk.FLAT
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.insert(tk.END, "Ingrese dos vectores en ℝⁿ para calcular la proyección...")
        self.explanation_text.config(state=tk.DISABLED)
        
        # Gráfico
        graph_tab = ttk.Frame(notebook)
        notebook.add(graph_tab, text="📈 Gráfico")
        
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_empty_plot()
        
        # Footer con créditos
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(
            footer_frame,
            text="Desarrollado por Javier Barros | v1.2 | Álgebra Lineal",
            style='Footer.TLabel'
        ).pack(side=tk.RIGHT)
    
    def draw_empty_plot(self):
        self.ax.clear()
        self.ax.set_title("Esperando datos de vectores...", pad=20)
        self.ax.text(0.5, 0.5, "Ingrese dos vectores\npara visualizar la proyección", 
                    ha='center', va='center', fontsize=10, color='gray')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def draw_projection(self, a, b, projection):
        self.ax.clear()
        
        # Configuración del gráfico
        self.ax.set_title("Proyección Ortogonal", pad=20)
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        
        # Ajustar límites según los vectores
        max_val = max(max(np.abs(a)), max(np.abs(b)), max(np.abs(projection))) * 1.2
        self.ax.set_xlim([-max_val, max_val])
        self.ax.set_ylim([-max_val, max_val])
        
        # Dibujar los vectores
        origin = [0, 0]
        self.ax.quiver(*origin, *a[:2], color='r', angles='xy', scale_units='xy', scale=1, 
                      width=0.005, label=f'Vector a = {a[:2]}...')
        self.ax.quiver(*origin, *b[:2], color='b', angles='xy', scale_units='xy', scale=1,
                      width=0.005, label=f'Vector b = {b[:2]}...')
        self.ax.quiver(*origin, *projection[:2], color='g', angles='xy', scale_units='xy', scale=1,
                      width=0.005, label=f'Proyección = {projection[:2]}...')
        
        # Dibujar línea punteada para la proyección
        self.ax.plot([a[0], projection[0]], [a[1], projection[1]], 'k--', linewidth=0.5)
        
        # Cuadrícula y leyenda
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend()
        
        # Nota si los vectores tienen más de 2 dimensiones
        if len(a) > 2 or len(b) > 2:
            self.ax.text(0.05, 0.95, "Nota: Mostrando solo las primeras 2 dimensiones", 
                        transform=self.ax.transAxes, fontsize=8, color='gray')
        
        self.canvas.draw()
    
    def calculate_projection(self):
        try:
            # Obtener y validar vectores
            a = np.array([float(x) for x in self.vector_a.get().split(",")])
            b = np.array([float(x) for x in self.vector_b.get().split(",")])
            
            if a.shape != b.shape:
                raise ValueError("Los vectores deben tener la misma dimensión")
            
            # Calcular proyección
            dot_product = np.dot(a, b)
            b_norm_squared = np.dot(b, b)
            
            if b_norm_squared == 0:
                raise ValueError("El vector b no puede ser el vector cero")
            
            projection = (dot_product / b_norm_squared) * b
            
            # Mostrar resultados
            self.projection_label.config(text=f"Proyección: {np.array_str(projection, precision=6)}", foreground='#27ae60')
            
            # Explicación matemática
            explanation = self.generate_explanation(a, b, dot_product, b_norm_squared, projection)
            self.explanation_text.config(state=tk.NORMAL)
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            self.explanation_text.config(state=tk.DISABLED)
            
            # Dibujar proyección (solo mostramos 2D para simplificar)
            self.draw_projection(a, b, projection)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}\n\nFormato correcto: 1.0, 2.5, -3.2")
            self.draw_empty_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
            self.draw_empty_plot()
    
    def generate_explanation(self, a, b, dot_product, b_norm_squared, projection):
        explanation = "📐 EXPLICACIÓN MATEMÁTICA DE LA PROYECCIÓN\n\n"
        explanation += "Fórmula: proj_b a = (a·b / b·b) * b\n\n"
        
        explanation += f"1️⃣ Producto punto (a·b):\n"
        explanation += f"   {a} · {b} = {dot_product:.6f}\n\n"
        
        explanation += f"2️⃣ Norma al cuadrado de b (b·b):\n"
        explanation += f"   {b} · {b} = {b_norm_squared:.6f}\n\n"
        
        explanation += f"3️⃣ Factor escalar (a·b / b·b):\n"
        explanation += f"   {dot_product:.6f} / {b_norm_squared:.6f} = {dot_product/b_norm_squared:.6f}\n\n"
        
        explanation += f"4️⃣ Proyección resultante:\n"
        explanation += f"   {dot_product/b_norm_squared:.6f} * {b} = {np.array_str(projection, precision=6)}\n\n"
        
        explanation += "🔍 Interpretación geométrica:\n"
        explanation += "La proyección ortogonal representa la 'sombra' del vector a sobre el vector b.\n"
        explanation += "- Si los vectores son ortogonales (a·b = 0), la proyección será el vector cero.\n"
        explanation += "- Si los vectores son paralelos, la proyección será el mismo vector a.\n"
        explanation += "- La diferencia a - proj_b a es ortogonal al vector b."
        
        return explanation
    
    def clear_fields(self):
        # Limpiar los campos de entrada
        self.vector_a.set("")
        self.vector_b.set("")
        
        # Restablecer los resultados
        self.projection_label.config(text="Proyección: ", foreground='#2c3e50')
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, "Ingrese dos vectores en ℝⁿ para calcular la proyección...")
        self.explanation_text.config(state=tk.DISABLED)
        
        # Restablecer el gráfico
        self.draw_empty_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorProjectionApp(root)
    root.mainloop()