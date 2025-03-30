import numpy as np

def check_linear_independence(vectors):
    """Determina si los vectores son linealmente independientes"""
    # Convertir a matriz numpy (cada vector como columna)
    matrix = np.array(vectors).T
    
    # Verificar si la matriz es cuadrada (para usar determinante)
    if matrix.shape[0] == matrix.shape[1]:
        det = np.linalg.det(matrix)
        if not np.isclose(det, 0, atol=1e-10):
            return True, f"El determinante es {det:.6f} (≠ 0)"
        else:
            return False, f"El determinante es {det:.6f} (= 0)"
    else:
        # Para matrices no cuadradas, usar rango
        rank = np.linalg.matrix_rank(matrix)
        if rank == len(vectors):
            return True, f"El rango de la matriz es {rank} (máximo posible)"
        else:
            return False, f"El rango de la matriz es {rank} (no máximo)"

def main():
    print("=== Análisis de Independencia Lineal de Vectores ===")
    print("Instrucciones:")
    print("1. Ingrese cada vector separando sus componentes por comas")
    print("2. Ejemplo: Para el vector (1, 2, 3), escriba: 1, 2, 3")
    print("3. Presione Enter después de cada vector")
    print("4. Escriba 'fin' para terminar la entrada\n")
    
    vectors = []
    while True:
        entrada = input(f"Ingrese el vector {len(vectors)+1} (o 'fin' para terminar): ").strip()
        
        if entrada.lower() == 'fin':
            break
            
        try:
            componentes = [float(x.strip()) for x in entrada.split(",")]
            vectors.append(componentes)
            print(f"Vector {len(vectors)} añadido: {componentes}")
        except ValueError:
            print("Error: Ingrese números válidos separados por comas. Ejemplo: 1, 2, 3")
    
    if not vectors:
        print("\nNo se ingresaron vectores. Saliendo...")
        return
    
    print("\n=== Vectores ingresados ===")
    for i, vec in enumerate(vectors, 1):
        print(f"Vector {i}: {vec}")
    
    print("\n=== Resultado del análisis ===")
    es_independiente, explicacion = check_linear_independence(vectors)
    
    if es_independiente:
        print("✅ Los vectores son LINEALMENTE INDEPENDIENTES")
    else:
        print("❌ Los vectores son LINEALMENTE DEPENDIENTES")
    
    print(f"\n🔍 Explicación: {explicacion}")
    
    # Mostrar matriz formada por los vectores
    print("\nMatriz formada por los vectores (como columnas):")
    print(np.array(vectors).T)

if __name__ == "__main__":
    main()