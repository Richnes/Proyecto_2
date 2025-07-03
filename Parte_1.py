import random
import json
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
def exportar_info_pdf(jugador_id, datos):
    nombre_archivo = f"{jugador_id}_info.pdf"
    c = canvas.Canvas(nombre_archivo,pagesize=letter)
    c.setFont("Helvetica",12)
    
    c.drawString(100, 750, "INFORMACIÓN DEL JUGADOR")
    c.drawString(100, 720, F"ID: {jugador_id}")
    c.drawString(100, 700, f"Nombre: {datos['nombre']}")
    c.drawString(100, 680, f"Correo: {datos['correo']}")
    c.drawString(100, 660, f"Fecha: {datos['fecha']}")
    c.drawString(100,640, f"Puntaje: {datos.get('puntaje', 0)}")

    movimiento = datos.get("movimientos", [])
    c.drawString(100, 620, "Movimientos:")
    
    #Mostrar los movimientos divididos en líneas si son muchos
    linea = 600 
    linea_max = 100
    linea_texto = ""
    for i, mov in enumerate(movimiento):
        linea_texto += mov + " "
        if (i+1) % 20 == 0 or i == len(movimiento) - 1:
            c.drawString(120, linea, linea_texto.strip())
            linea_texto = ""
            linea -= 20
            if linea < linea_max:
                break #evitar que pase de página 
    c.save()
    print(f"PDF generado: {nombre_archivo}")
    
    
#mostramos los ganadores por orden asecendente de mes/año
def ganadores_del_mes():
    jugadores = cargar_jugadores()
    ganadores = {}
    
#inicamos un dic de ganadores vacía para agregarlos ahí
    for jugador_id, datos in jugadores.items():
        fecha = datos.get("fecha")
        puntaje = datos.get("puntaje")
        nombre = datos.get("nombre")
#si en la fecha no hay ganadores o el puntaje es mayor que 0 se agrega un ganador 
        if fecha not in ganadores or puntaje > ganadores[fecha][1]:
            ganadores[fecha] = (nombre,puntaje)

    print("\n## GANADORES DEL MES ##\n")
    print("{:<10} {:<15} {:<10}".format("Mes","jugador","Puntaje"))
    print("-"*40)  
    #ordenamos los meses

    meses_ordenados = sorted(ganadores.keys(), key=lambda x: (int(x.split("/")[1]), int(x.split("/")[0])))
        
    for mes in meses_ordenados:
        nombre, puntaje = ganadores[mes]
        print("{:<10} {:<15} {:<10}".format(mes, nombre, puntaje))

    
def mostrar_rankings():
    jugadores = cargar_jugadores()
    
    print("\n## LISTA DE GANADORES ##\n")
    print("{:<6} {:15} {:<10}".format("ID","Nombre","Puntaje"))
    print("-"*35)
    
    ranking = sorted(jugadores.items(), key=lambda x: x[1].get("puntaje"),reverse=True)
    
    for jugador_id, datos in ranking:
        nombre = datos.get("nombre","")
        puntaje = datos.get("puntaje",0)
        print("{:<6} {:<15} {:<10}".format(jugador_id,nombre,puntaje))
        
def info_jugadores():
    jugadores = cargar_jugadores()
    jugador_id = input("Ingrese el ID del jugador: ").strip()
    
    if jugador_id not in jugadores:
        print("ID no encontrado.")
        return 
    
    jugador = jugadores[jugador_id]
    print("\n### INFO DEL JUGADOR ###")
    print(f"ID: {jugador_id}")
    print(f"Nombre: {jugador['nombre']}")
    print(f"Correo: {jugador['correo']}")
    print(f"Fecha: {jugador['fecha']}")
    print(f"Puntaje: {jugador.get('puntaje', 0)}")
    movimientos = jugador.get("movimientos", [])
    print(f"Movimientos: {' '.join(movimientos) if movimientos else 'Sin movimientos' }")
    
    opcion = input("¿Desea exportar esta información en PDF? (s/n): ").lower()
    if opcion == "s":
        exportar_info_pdf(jugador_id, jugador)
        
def guardar_resultado_partida():
    jugadores = cargar_jugadores()
    jugador_id = estado_juego["jugador_id"]

    if jugador_id in jugadores:
        jugadores[jugador_id]["puntaje"] = estado_juego["puntaje"]
        jugadores[jugador_id]["movimientos"] = estado_juego["movimientos_totales"]
    
    guardar_jugadores(jugadores)
    
def cargar_jugadores():
    if os.path.exists("jugadores.json"):
        with open("jugadores.json","r") as archivo:
            return json.load(archivo)
    else:
        return {}
    
def guardar_jugadores(jugadores):
    with open("jugadores.json","w") as archivo:
        json.dump(jugadores,archivo,indent=4)

def registrar_jugador():
    jugadores = cargar_jugadores()
    print("## INICIO DE JUEGO ##")
    nombre = input("Ingrese su nombre de usuario: ").strip()
    correo = input("Ingrese su correo: ").strip()
    fecha = input("la fecha papu->(mes y año): ") #12/2025
    
    Arrobas = ["@gmail.com","@hotmail.com","@utec.edu.pe"]
    
    while not any(dominio in correo for dominio in Arrobas):
        correo = input("Ingrese su correo: ")
    
    while True:
        try:
            mes, año = map(int,fecha.split("/"))
            if 1 <= mes <= 12:
                break
            else:
                fecha = input("la fecha papu->(mes y año): ") #12/2025
        except:
            fecha = input("la fecha papu->(mes y año): ") #12/2025

    for jugador_id, data in jugadores.items():
        if data["nombre"] == nombre and data["correo"] == correo:
            print(f"Bienvenido nuevamente, {nombre}!")
            estado_juego["nombre_jugador"] = nombre
            estado_juego["jugador_id"] = jugador_id
            return jugadores
    nuevo_id = f"u{len(jugadores)+1:02}"
    jugadores[nuevo_id] = {
        "nombre": nombre,
        "correo": correo,
        "fecha": fecha,
        "movimientos": []
    }
    guardar_jugadores(jugadores)
    print(f"¡Nuevo jugador registrado con ID: {nuevo_id}!")
    estado_juego["nombre_jugador"] = nombre
    estado_juego["jugador_id"] = nuevo_id
    return jugadores

# Crear matriz vacía
def crear_matriz():
    filas = 10
    columnas = 20
    return [["." for _ in range(columnas)] for _ in range(filas)]

# Actualizar matriz con serpiente y manzana
def actualizar_matriz():
    matriz = crear_matriz()
    # Dibuja el cuerpo de la serpiente
    for (i, j) in estado_juego["serpiente"][:-1]:
        matriz[i][j] = "-"
    # Dibuja la cabeza de la serpiente
    i, j = estado_juego["serpiente"][-1]
    matriz[i][j] = ">" # Puedes ajustar esto para que la cabeza apunte en la dirección correcta si lo deseas
    # Dibuja la manzana
    mi, mj = estado_juego["manzana"]
    matriz[mi][mj] = "@"
    estado_juego["matriz"] = matriz

# Mostrar matriz
def imprimir_matriz(matriz):
    print(f"\n## SNAKE ##\nJugador: {estado_juego['nombre_jugador']}\nPuntaje: {estado_juego['puntaje']}\n")
    for fila in matriz:
        print("".join(fila))

# Colocar manzana aleatoria
def generar_manzana():
    posiciones_ocupadas = set(estado_juego["serpiente"]) # Coordenadas ocupadas por la serpiente
    while True:
        fila = random.randint(0, 9)
        col = random.randint(0, 19)
        if (fila, col) not in posiciones_ocupadas:
            estado_juego["manzana"] = (fila, col)
            estado_juego["movimientos_manzana"] = 0 # Reinicia el contador de movimientos de la manzana
            break

# Movimiento de serpiente
def movimiento_del_gusano(di, dj):
    global estado_juego

    cabeza = estado_juego["serpiente"][-1]
    nueva_cabeza = (cabeza[0] + di, cabeza[1] + dj)

    # Colisión con límites (manejo de "teletransporte" a través de los bordes)
    nueva_fila, new_col = nueva_cabeza # Desempaqueta la tupla para poder trabajar con los valores

    if nueva_fila >= 10: # abajo
        nueva_fila = 0
    elif nueva_fila < 0: # arriba
        nueva_fila = 9

    if new_col >= 20: # por la derecha
        new_col = 0
    elif new_col < 0: # por la izquierda
        new_col = 19

    nueva_cabeza = (nueva_fila, new_col) 

    # Colisión con sí misma
    # Se verifica si la nueva cabeza colisiona con cualquier parte del cuerpo de la serpiente,
    # excepto la cola si la serpiente no va a crecer (es decir, si no comió una manzana).
    # Esto evita que la serpiente colisione consigo misma al moverse a la posición que acaba de dejar su cola.
    if nueva_cabeza in estado_juego["serpiente"][:-1]: # Excluye la última parte (cola) para evitar falsos positivos
        print("¡La serpiente se chocó consigo misma!")
        finalizar_partida()
        return # Termina la ejecución de esta llamada

    comio_manzana = nueva_cabeza == estado_juego["manzana"]
    estado_juego["serpiente"].append(nueva_cabeza)

    if not comio_manzana:
        estado_juego["serpiente"].pop(0) # Elimina la cola si no comió manzana
        estado_juego["movimientos_manzana"] += 1
    else:
        estado_juego["puntaje"] += 1
        generar_manzana() # Genera una nueva manzana

    # Si la manzana no fue comida en 20 movimientos
    if estado_juego["movimientos_manzana"] >= 20:
        print("¡La manzana no fue comida en 20 movimientos!")
        finalizar_partida()
        return # Termina la ejecución de esta llamada


    actualizar_matriz()
    imprimir_matriz(estado_juego["matriz"])
    # Continúa el ciclo pidiendo el siguiente movimiento
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
        estado_juego["movimientos_totales"].append("w") 
        movimiento_del_gusano(-1, 0)
    elif movimiento == "s":
        estado_juego["movimientos_totales"].append("s") 
        movimiento_del_gusano(1, 0)
        
    elif movimiento == "a":
        estado_juego["movimientos_totales"].append("a") 
        movimiento_del_gusano(0, -1)
    elif movimiento == "d":
        estado_juego["movimientos_totales"].append("d") 
        movimiento_del_gusano(0, 1)

# Ingresar datos del jugador
def ingresar_nombre():
    jugadores = registrar_jugador()
    print("####################")
    return estado_juego["nombre_jugador"]
# Iniciar el juego
def juego():
    global estado_juego
    # Reiniciar el estado del juego para una nueva partida
    estado_juego["serpiente"] = [(0, 1), (0, 2), (0, 3)]
    estado_juego["puntaje"] = 0
    estado_juego["movimientos_manzana"] = 0
    estado_juego["movimientos_totales"] = []

    generar_manzana()
    actualizar_matriz()
    imprimir_matriz(estado_juego["matriz"])
    Impresion_De_menu()

# Mostrar récords
def records():
    print("## RECORD ##".center(80))
    print("1. Rankings".center(80))
    print("2. Ganadores del mes".center(80))
    
    opciones = ["1","2","s"]
    op = input("Presione 's' para regresar al menú principal: ")
    while op.lower() not in opciones:
        op = input("Introduzca una opción válida: ")
    if op == "1":
        mostrar_rankings()
    elif op == "2":
        ganadores_del_mes()
    elif op.lower() == "s":
        main_menu()


# Finalizar partida y regresar al menú principal
def finalizar_partida():
    guardar_resultado_partida()
    print("###################################")
    print(f"\nFin del juego. Puntaje final: {estado_juego['puntaje']}\n")
    print("Regresando al menú principal... Espere 3 segundos")
    print("###################################\n")
    time.sleep(3)
    main_menu() # Vuelve al menú principal

# Salir del juego
def salir():
    print("Hasta luego!!!!!")
    exit()

# Menú principal
def main_menu():
    print("########################## MENU DE INICIO ##########################".center(80))
    print("1. Empezar el juego".center(80))
    print("2. Récords".center(80))
    print("3. Info de Jugadores".center(80))
    print("4. Salir".center(80))

    print()

    opciones_De_inicio = ["1", "2", "3","4"]
    opcion = input("Escoger opción: ")

    while opcion not in opciones_De_inicio:
        opcion = input("Opción inválida, escoja otra opción del menú: ")

    if opcion == "1":
        nombre_usuario = ingresar_nombre()
        print(f"Bienvenido, {nombre_usuario}!")
        juego()
    elif opcion == "2":
        records()
    elif opcion == "3":
        info_jugadores()
    elif opcion == "4":
        salir()

# Iniciar programa
if __name__ == "__main__":
    main_menu()

