import numpy as np

def calcular_proyeccion(a, b):
    """Calcula la proyección ortogonal de a sobre b"""
    producto_punto = np.dot(a, b)
    norma_b_cuadrado = np.dot(b, b)
    
    if norma_b_cuadrado == 0:
        raise ValueError("El vector b no puede ser el vector cero")
    
    factor_escalar = producto_punto / norma_b_cuadrado
    proyeccion = factor_escalar * b
    
    return proyeccion, producto_punto, norma_b_cuadrado, factor_escalar

def mostrar_explicacion(a, b, proyeccion, producto_punto, norma_b_cuadrado, factor_escalar):
    """Muestra una explicación detallada del cálculo"""
    print("\n=== Explicación del cálculo ===")
    print("Fórmula: proj_b a = (a·b / b·b) * b")
    print("\n1. Producto punto (a·b):")
    print(f"   {a} · {b} = {producto_punto:.6f}")
    print("\n2. Norma al cuadrado de b (b·b):")
    print(f"   {b} · {b} = {norma_b_cuadrado:.6f}")
    print("\n3. Factor escalar (a·b / b·b):")
    print(f"   {producto_punto:.6f} / {norma_b_cuadrado:.6f} = {factor_escalar:.6f}")
    print("\n4. Proyección resultante:")
    print(f"   {factor_escalar:.6f} * {b} = {proyeccion}")
    print("\n📝 Interpretación geométrica:")
    print("La proyección ortogonal representa la componente de a en la dirección de b.")
    if np.allclose(proyeccion, a):
        print("¡Los vectores son paralelos (proyección = a)!")
    elif np.allclose(proyeccion, np.zeros_like(proyeccion)):
        print("¡Los vectores son ortogonales (proyección = vector cero)!")

def ingresar_vector(nombre):
    """Solicita al usuario ingresar un vector"""
    while True:
        entrada = input(f"Ingrese el vector {nombre} (componentes separadas por comas): ").strip()
        try:
            componentes = [float(x.strip()) for x in entrada.split(",")]
            if len(componentes) < 1:
                raise ValueError("El vector debe tener al menos una componente")
            return np.array(componentes)
        except ValueError as e:
            print(f"Error: {e}. Intente nuevamente. Ejemplo: 1, 2.5, -3")

def main():
    print("=== Calculadora de Proyección Ortogonal ===")
    print("Instrucciones:")
    print("1. Ingrese dos vectores en ℝⁿ (mismo número de componentes)")
    print("2. Cada vector debe ingresarse como componentes separadas por comas (ejemplo: 1, 2, 3)")
    print("3. El programa calculará la proyección de a sobre b usando la fórmula: proj_b a = (a·b / b·b) * b\n")
    
    # Ingreso de vectores
    a = ingresar_vector("a")
    b = ingresar_vector("b")
    
    # Verificar que tengan la misma dimensión
    if len(a) != len(b):
        print("\nError: Los vectores deben tener la misma dimensión")
        print(f"Dimensión de a: {len(a)}, Dimensión de b: {len(b)}")
        return
    
    try:
        # Cálculo de la proyección
        proyeccion, producto_punto, norma_b_cuadrado, factor_escalar = calcular_proyeccion(a, b)
        
        # Resultados
        print("\n=== Resultados ===")
        print(f"Vector a: {a}")
        print(f"Vector b: {b}")
        print(f"\n➡️ Proyección de a sobre b: {proyeccion}")
        
        # Explicación detallada
        mostrar_explicacion(a, b, proyeccion, producto_punto, norma_b_cuadrado, factor_escalar)
        
    except ValueError as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()