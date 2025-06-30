import random
import time


# Estado global del juego
estado_juego = {
    "matriz": [],
    "serpiente": [(0, 1), (0, 2), (0, 3)],
    "manzana": (0, 0),
    "puntaje": 0,
    "movimientos_manzana": 0,
    "movimientos_totales": [],
    "nombre_jugador": ""
}

# Crear matriz vacía
def crear_matriz():
    filas = 10
    columnas = 20
    return [["." for _ in range(columnas)] for _ in range(filas)]

# Actualizar matriz con serpiente y manzana
def actualizar_matriz():
    matriz = crear_matriz()
    for (i, j) in estado_juego["serpiente"][:-1]:
        matriz[i][j] = "-"
    i, j = estado_juego["serpiente"][-1]
    matriz[i][j] = ">"
    mi, mj = estado_juego["manzana"]
    #Actualiza la matriz con la serpiente incorporada
    matriz[mi][mj] = "@"
    estado_juego["matriz"] = matriz

# Mostrar matriz
def imprimir_matriz(matriz):
    print(f"\n## SNAKE ##\nJugador: {estado_juego['nombre_jugador']}\nPuntaje: {estado_juego['puntaje']}\n")
    for fila in matriz:
        print("".join(fila))

# Colocar manzana aleatoria
def generar_manzana():
    posiciones_ocupadas = set(estado_juego["serpiente"]) #coordenadas 
    while True:
        fila = random.randint(0, 9)
        col = random.randint(0, 19)
        if (fila, col) not in posiciones_ocupadas:
            estado_juego["manzana"] = (fila, col)
            estado_juego["movimientos_manzana"] = 0
            break

# Movimiento de serpiente
def movimiento_del_gusano(di, dj):
    cabeza = estado_juego["serpiente"][-1]
    nueva_cabeza = (cabeza[0] + di, cabeza[1] + dj) #1,1

    # Colisión con límites
    if not (0 <= nueva_cabeza[0] < 10 and 0 <= nueva_cabeza[1] < 20):
        if nueva_cabeza[0] == 10:
            nueva_cabeza[0] -= 10
        if nueva_cabeza[1] == 20:
            nueva_cabeza[1] -= 20
                    
        return finalizar_partida()

    # Colisión con sí misma
    if nueva_cabeza in estado_juego["serpiente"]:
        print("¡La serpiente se chocó consigo misma!")
        return finalizar_partida()

    comio_manzana = nueva_cabeza == estado_juego["manzana"]
    estado_juego["serpiente"].append(nueva_cabeza)

    if not comio_manzana:
        estado_juego["serpiente"].pop(0)
        estado_juego["movimientos_manzana"] += 1
    else:
        estado_juego["puntaje"] += 1
        generar_manzana()

    if estado_juego["movimientos_manzana"] >= 20:
        print("¡La manzana no fue comida en 20 movimientos!")
        return finalizar_partida()

    estado_juego["movimientos_totales"].append((di, dj))
    actualizar_matriz()
    imprimir_matriz(estado_juego["matriz"])
    Impresion_De_menu()

# Imprimir menú de movimientos
def Impresion_De_menu():
    print("""
             Arriba      (w)
             Abajo       (s)
             Izquierda   (a)
             Derecha     (d)
             Salir       (exit)""")
    movimiento = input("Seleccione un movimiento: ").lower()
    movimientos_validos = ["w", "a", "s", "d", "exit"]

    while movimiento not in movimientos_validos:
        movimiento = input("Movimiento inválido. Intente otra vez: ").lower()

    if movimiento == "exit":
        finalizar_partida()
    elif movimiento == "w":
        movimiento_del_gusano(-1, 0)
    elif movimiento == "s":
        movimiento_del_gusano(1, 0)
    elif movimiento == "a":
        movimiento_del_gusano(0, -1)
    elif movimiento == "d":
        movimiento_del_gusano(0, 1)

# Ingresar datos del jugador
def ingresar_nombre():
    print("## INICIO DE JUEGO ##")
    nombre = input("Ingrese su nombre de usuario: ")
    estado_juego["nombre_jugador"] = nombre
    print("####################")
    return nombre

# Iniciar el juego
def juego():
    estado_juego["serpiente"] = [(0, 1), (0, 2), (0, 3)]
    estado_juego["puntaje"] = 0
    estado_juego["movimientos_totales"] = []
    generar_manzana()
    actualizar_matriz()
    imprimir_matriz(estado_juego["matriz"])
    Impresion_De_menu()

# Mostrar récords
def records():
    print("## RECORD ##")
    reescritura_de_archivo()
    input("Presione 's' para regresar al menú principal: ")
    main_menu()

# Reescritura de Archivo
def reescritura_de_archivo():
    nombre_jugador = estado_juego["nombre_jugador"]
    puntaje_actual = estado_juego["puntaje"]

    records = {}
    try:
        archivo_r = open("records.txt", "r")
        for cadena in archivo_r:
            partes = cadena.strip().split()
            if len(partes) >= 2:
                nombre = " ".join(partes[:-2])
                puntaje = int(partes[-2])
                records[nombre] = puntaje
        archivo_r.close()
    except FileNotFoundError:
        pass

    if puntaje_actual > 0:
        if nombre_jugador in records.keys():
            if puntaje_actual > records[nombre_jugador]:
                records[nombre_jugador] = puntaje_actual
        else:
            records[nombre_jugador] = puntaje_actual


    archivo_w = open("records.txt", "w")
    for nombre, puntaje in records.items():
        archivo_w.write(f"{nombre} {puntaje} puntos\n")
    archivo_w.close()

    archivo_r = open("records.txt", "r")
    for cadena in archivo_r:
        print(cadena.strip())
    archivo_r.close()

# Finalizar partida y regresar
def finalizar_partida():
    print("###################################")
    print(f"\nFin del juego. Puntaje final: {estado_juego['puntaje']}\n")
    print("Regresando al menú principal... Espere 3 segundos")
    print("###################################\n")
    time.sleep(3)
    main_menu()

# Salir del juego
def salir():
    print("Hasta luego!!!!!")
    exit()
    #main_menu()
# Menú principal
def main_menu():
    print("########################## MENU DE INICIO ##########################".center(80))
    print("1. Empezar el juego".center(80))
    print("2. Récords".center(80))
    print("3. Salir".center(80))
    print()

    opciones_De_inicio = ["1", "2", "3"]
    opcion = input("Escoger opción: ")

    while opcion not in opciones_De_inicio:
        opcion = input("Opción inválida, escoga otra opción del menu: ")

    if opcion == "1":
        nombre_usuario = ingresar_nombre()
        print(f"Bienvenido, {nombre_usuario}!")
        juego()
    elif opcion == "2":
        records()
    elif opcion == "3":
        salir()

# Iniciar programa
main_menu()