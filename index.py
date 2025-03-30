import tkinter as tk
from tkinter import ttk
import subprocess
import os

class VectorCalculusLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Lanzador de Aplicaciones Vectoriales")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=10)
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame, 
            text="🚀 Lanzador de Aplicaciones de Cálculo Vectorial",
            style='Title.TLabel'
        ).pack(pady=(0, 30))
        
        # Botones de aplicaciones
        apps = [
            ("📦 Volumen de Paralelepípedo", "parallelepiped_volume.py"),
            ("➡️ Proyección Ortogonal", "orthogonal_projection.py"),
            ("🔍 Independencia Lineal", "linear_independence.py")
        ]
        
        for app_name, app_file in apps:
            ttk.Button(
                main_frame,
                text=app_name,
                command=lambda f=app_file: self.launch_app(f),
                style='TButton'
            ).pack(fill=tk.X, pady=10)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Label(
            footer_frame,
            text="Desarrollado por Urafael | v2.1",
            font=('Segoe UI', 8),
            foreground='#7f8c8d'
        ).pack(side=tk.RIGHT)
    
    def launch_app(self, app_file):
        try:
            if not os.path.exists(app_file):
                raise FileNotFoundError(f"Archivo {app_file} no encontrado")
            
            # Usar el intérprete de Python actual
            python_exec = "python" if os.name == 'nt' else "python3"
            subprocess.Popen([python_exec, app_file])
            
        except Exception as e:
            tk.messagebox.showerror(
                "Error",
                f"No se pudo iniciar la aplicación:\n{str(e)}\n\n"
                f"Asegúrate que {app_file} está en el mismo directorio"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorCalculusLauncher(root)
    root.mainloop()
