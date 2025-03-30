import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class ParallelepipedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Volumen de Paralelepípedo")
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
        self.vector_c = tk.StringVar()
        
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
            text="📦 Volumen de Paralelepípedo en ℝ³",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        # Panel de entrada
        input_panel = ttk.LabelFrame(main_frame, text=" Ingreso de Vectores ", padding=15)
        input_panel.pack(fill=tk.X, pady=5)
        
        # Entrada de vectores
        ttk.Label(input_panel, text="Vector a (x,y,z):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_panel, textvariable=self.vector_a, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(input_panel, text="Vector b (x,y,z):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_panel, textvariable=self.vector_b, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(input_panel, text="Vector c (x,y,z):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_panel, textvariable=self.vector_c, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Frame para botones
        button_frame = ttk.Frame(input_panel)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botón de cálculo
        ttk.Button(
            button_frame,
            text="📊 Calcular Volumen",
            command=self.calculate_volume,
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
        notebook.add(result_tab, text="📋 Resultado")
        
        self.volume_label = ttk.Label(
            result_tab, 
            text="Volumen: ", 
            font=('Segoe UI', 11, 'bold'),
            foreground='#2c3e50'
        )
        self.volume_label.pack(anchor=tk.W, pady=5)
        
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
        self.explanation_text.insert(tk.END, "Ingrese tres vectores en ℝ³ para calcular el volumen...")
        self.explanation_text.config(state=tk.DISABLED)
        
        # Gráfico 3D
        graph_tab = ttk.Frame(notebook)
        notebook.add(graph_tab, text="📐 Gráfico 3D")
        
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_empty_plot()
        
        # Footer con créditos
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(
            footer_frame,
            text="Desarrollado por Javier Barros | v1.1 | Cálculo Vectorial",
            style='Footer.TLabel'
        ).pack(side=tk.RIGHT)
    
    def draw_empty_plot(self):
        self.ax.clear()
        self.ax.set_title("Esperando datos...", pad=20)
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_zlabel('Eje Z')
        self.ax.text(0, 0, 0, "Ingrese 3 vectores\npara visualizar", 
                    ha='center', va='center', fontsize=10, color='gray')
        self.canvas.draw()
    
    def draw_parallelepiped(self, a, b, c):
        self.ax.clear()
        
        # Vértices del paralelepípedo
        vertices = [
            [0, 0, 0],
            a,
            [a[0]+b[0], a[1]+b[1], a[2]+b[2]],
            b,
            [a[0]+c[0], a[1]+c[1], a[2]+c[2]],
            [a[0]+b[0]+c[0], a[1]+b[1]+c[1], a[2]+b[2]+c[2]],
            [b[0]+c[0], b[1]+c[1], b[2]+c[2]],
            c
        ]
        
        # Definir las 6 caras del paralelepípedo
        faces = [
            [vertices[0], vertices[1], vertices[4], vertices[3]],
            [vertices[1], vertices[2], vertices[5], vertices[4]],
            [vertices[2], vertices[6], vertices[7], vertices[5]],
            [vertices[3], vertices[4], vertices[7], vertices[6]],
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[7], vertices[6]]
        ]
        
        # Dibujar las caras
        face_collection = Poly3DCollection(faces, alpha=0.25, linewidths=1, edgecolor='k')
        face_collection.set_facecolor('cyan')
        self.ax.add_collection3d(face_collection)
        
        # Dibujar los vectores
        origin = [0, 0, 0]
        self.ax.quiver(*origin, *a, color='r', arrow_length_ratio=0.1, label=f'a = {a}')
        self.ax.quiver(*origin, *b, color='g', arrow_length_ratio=0.1, label=f'b = {b}')
        self.ax.quiver(*origin, *c, color='b', arrow_length_ratio=0.1, label=f'c = {c}')
        
        # Configurar el gráfico
        max_val = max(max(abs(val) for val in vector) for vector in [a, b, c]) * 1.5
        self.ax.set_xlim([-max_val, max_val])
        self.ax.set_ylim([-max_val, max_val])
        self.ax.set_zlim([-max_val, max_val])
        self.ax.set_title("Paralelepípedo formado por los vectores", pad=20)
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_zlabel('Eje Z')
        self.ax.legend()
        
        self.canvas.draw()
    
    def calculate_volume(self):
        try:
            # Obtener y validar vectores
            a = np.array([float(x) for x in self.vector_a.get().split(",")])
            b = np.array([float(x) for x in self.vector_b.get().split(",")])
            c = np.array([float(x) for x in self.vector_c.get().split(",")])
            
            if a.shape != (3,) or b.shape != (3,) or c.shape != (3,):
                raise ValueError("Cada vector debe tener exactamente 3 componentes")
            
            # Calcular producto triple (a · (b × c))
            cross_product = np.cross(b, c)
            scalar_triple = np.dot(a, cross_product)
            volume = abs(scalar_triple)
            
            # Mostrar resultados
            self.volume_label.config(text=f"Volumen: {volume:.6f} unidades cúbicas", foreground='#27ae60')
            
            # Explicación matemática
            explanation = self.generate_explanation(a, b, c, cross_product, scalar_triple, volume)
            self.explanation_text.config(state=tk.NORMAL)
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.insert(tk.END, explanation)
            self.explanation_text.config(state=tk.DISABLED)
            
            # Dibujar paralelepípedo
            self.draw_parallelepiped(a, b, c)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}\n\nFormato correcto: 1.0, 2.5, -3.2")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
            self.draw_empty_plot()
    
    def generate_explanation(self, a, b, c, cross_product, scalar_triple, volume):
        explanation = "📐 EXPLICACIÓN MATEMÁTICA DEL VOLUMEN\n\n"
        explanation += "Fórmula del volumen: V = |a · (b × c)|\n\n"
        
        explanation += "1️⃣ Producto vectorial (b × c):\n"
        explanation += f"   b × c = {b} × {c} = {cross_product}\n\n"
        
        explanation += "2️⃣ Producto escalar (a · (b × c)):\n"
        explanation += f"   a · (b × c) = {a} · {cross_product} = {scalar_triple:.6f}\n\n"
        
        explanation += "3️⃣ Volumen absoluto:\n"
        explanation += f"   V = |{scalar_triple:.6f}| = {volume:.6f}\n\n"
        
        explanation += "🔍 Interpretación geométrica:\n"
        explanation += "El valor absoluto del producto triple escalar representa el volumen del paralelepípedo formado por los tres vectores.\n"
        explanation += "Si el volumen es cero, los vectores son coplanares (linealmente dependientes)."
        
        return explanation
    
    def clear_fields(self):
        # Limpiar los campos de entrada
        self.vector_a.set("")
        self.vector_b.set("")
        self.vector_c.set("")
        
        # Restablecer los resultados
        self.volume_label.config(text="Volumen: ", foreground='#2c3e50')
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, "Ingrese tres vectores en ℝ³ para calcular el volumen...")
        self.explanation_text.config(state=tk.DISABLED)
        
        # Restablecer el gráfico
        self.draw_empty_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParallelepipedApp(root)
    root.mainloop()