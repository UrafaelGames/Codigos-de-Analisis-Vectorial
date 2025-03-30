import numpy as np

def calcular_volumen(a, b, c):
    """Calcula el volumen del paralelepípedo usando el producto triple escalar"""
    producto_vectorial = np.cross(b, c)
    producto_triple = np.dot(a, producto_vectorial)
    volumen = abs(producto_triple)
    return volumen, producto_vectorial, producto_triple

def mostrar_explicacion(a, b, c, p_vectorial, p_triple, volumen):
    """Genera una explicación detallada del cálculo"""
    print("\n=== Explicación del cálculo ===")
    print("Fórmula: V = |a · (b × c)|")
    print("\n1. Producto vectorial (b × c):")
    print(f"   {b} × {c} = {p_vectorial}")
    print("\n2. Producto escalar (a · (b × c)):")
    print(f"   {a} · {p_vectorial} = {p_triple:.6f}")
    print("\n3. Volumen absoluto:")
    print(f"   V = |{p_triple:.6f}| = {volumen:.6f}")
    print("\n📝 Interpretación geométrica:")
    print("El valor absoluto del producto triple escalar representa")
    print("el volumen del paralelepípedo formado por los tres vectores.")
    if np.isclose(volumen, 0):
        print("¡Los vectores son coplanares (volumen cero)!")

def ingresar_vector(nombre):
    """Solicita al usuario ingresar un vector"""
    while True:
        entrada = input(f"Ingrese el vector {nombre} (x,y,z): ").strip()
        try:
            componentes = [float(x.strip()) for x in entrada.split(",")]
            if len(componentes) != 3:
                raise ValueError("Debe tener exactamente 3 componentes")
            return np.array(componentes)
        except ValueError as e:
            print(f"Error: {e}. Intente nuevamente. Ejemplo: 1.5, -2.0, 3.2")

def main():
    print("=== Calculadora de Volumen de Paralelepípedo ===")
    print("Instrucciones:")
    print("1. Ingrese tres vectores en ℝ³ (3 dimensiones)")
    print("2. Cada vector debe ingresarse como x,y,z (ejemplo: 1, 2, 3)")
    print("3. El programa calculará el volumen usando |a · (b × c)|\n")
    
    # Ingreso de vectores
    a = ingresar_vector("a")
    b = ingresar_vector("b")
    c = ingresar_vector("c")
    
    # Cálculo del volumen
    volumen, p_vectorial, p_triple = calcular_volumen(a, b, c)
    
    # Resultados
    print("\n=== Resultados ===")
    print(f"Vector a: {a}")
    print(f"Vector b: {b}")
    print(f"Vector c: {c}")
    print(f"\n📦 Volumen del paralelepípedo: {volumen:.6f}")
    
    # Explicación detallada
    mostrar_explicacion(a, b, c, p_vectorial, p_triple, volumen)

if __name__ == "__main__":
    main()