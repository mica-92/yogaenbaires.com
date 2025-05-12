import json
import os
from datetime import datetime

# TODO: Implementar navegación con Ctrl+C (x1: reintentar, x2: campo anterior, x3: salir)


# Constantes
ARCHIVO_DATOS = "estudios_database.json"
ARCHIVO_ID = "last_id.txt"


def cargar_base_datos():
    """Carga la base de datos desde archivo JSON o crea una nueva si no existe."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r') as f:
            return json.load(f)
    return {}

def cargar_ultimo_id():
    """Carga el último ID usado desde archivo o comienza desde 0."""
    if os.path.exists(ARCHIVO_ID):
        with open(ARCHIVO_ID, 'r') as f:
            return int(f.read().strip())
    return 0

def guardar_base_datos():
    """Guarda la base de datos actual en archivo JSON."""
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(base_estudios, f, indent=4)

def guardar_ultimo_id():
    """Guarda el último ID usado en archivo."""
    with open(ARCHIVO_ID, 'w') as f:
        f.write(str(ultimo_id))

base_estudios = cargar_base_datos()
ultimo_id = cargar_ultimo_id()

def generar_id():
    """Genera un ID secuencial en formato 001, 002, etc."""
    global ultimo_id
    ultimo_id += 1
    guardar_ultimo_id()
    return f"{ultimo_id:03d}"

def obtener_date_actual():
    """Devuelve la date actual en formato AAAA-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")

def resetear_base_datos():
    """Resetea completamente la base de datos y el último ID."""
    global base_estudios, last_id
    
    # Resetear variables globales
    base_estudios = {}
    last_id = 0
    
    # Guardar los cambios en los archivos
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(base_estudios, f)
    
    with open(ARCHIVO_ID, 'w') as f:
        f.write(str(last_id))

# ------------------------------ #

def imprimir_estudio(estudio_id, datos):
    """Imprime la información de un estudio en formato consistente."""
    print(f"\n=== Estudio {estudio_id} - {datos['title']} ===\n")
    print(f"- Fecha: {datos['date']}")
    print(f"- Highlight: {datos.get('highlight', False)} - Weight: {datos.get('weight', 10)}")
    print(f"- Draft: {datos.get('draft', True)}")
    
    print("\nTaxonomías")
    print(f"- Estilos: {', '.join(datos['estilos'])}")
    print(f"- Duración: {', '.join(datos['duracion'])}")
    print(f"- Intensidad: {', '.join(datos['intensidad'])}")
    print(f"- Barrio: {datos.get('barrio', 'No especificado')}")

    print("\nEstudio")
    print(f"- Dirección: {datos.get('direccion', 'No especificada')}")
    print(f"- Salón: {datos.get('salon', 'No especificado')}")
    print(f"- Capacidad: {datos.get('capacidad', 'No especificada')}")
    print(f"- Modalidad de reserva: {datos.get('reserva', 'No especificada')}")
    print(f"- Descripción: {datos.get('descripcion', 'No disponible')}")

    print("\nRedes Sociales")
    print(f"- Instagram: {datos.get('instagram', 'No especificado')}")
    print(f"- Post Destacado: {datos.get('instagram_post', 'No especificado')}")
    print(f"- Reseña YEB: {datos.get('instagram_review', 'No especificado')}")
    print(f"- Website: {datos.get('website', 'No especificado')}")
    
    if datos.get('comments'):
        print("\nComentarios:")
        for i, comentario in enumerate(datos['comments'], 1):
            autor = comentario.get('author', 'Anónimo')
            print(f"  {i}. {comentario['text']} ({autor})")
            print(f"     [Estilo: {comentario.get('cardcolor', 'style-quote')}, Peso: {comentario.get('weight', 10)}]")

# ------------------------------ #

def ver_todos():
    """Muestra todos los estudios en la base de datos."""
    print("\n--- Todos los Estudios ---\n")
    if not base_estudios:
        print("La base de datos está vacía")
        return
    
    ids_ordenados = sorted(base_estudios.keys(), key=lambda x: int(x))
    print("Total de estudios:", len(base_estudios), "\n")
    for estudio_id in ids_ordenados:
        datos = base_estudios[estudio_id]
        print(f"{estudio_id} - {datos['title']}")

def eliminar_estudio():
    """Elimina un estudio y ajusta el último ID si es necesario."""
    global ultimo_id
    
    print("\n--- Eliminar Estudio ---\n")
    estudio_id = input("ID del Estudio a Eliminar: ").strip()

    try:
        estudio_id_normalizado = f"{int(estudio_id):03d}"
    except ValueError:
        print("\nError: El ID debe ser un número")
        return
    
    if estudio_id_normalizado in base_estudios:
        # Mostrar detalles del estudio para confirmación
        datos = base_estudios[estudio_id_normalizado]
        print("\nSeleccionaste para eliminar:")
        print(f"ID {estudio_id_normalizado} - {datos['title']}")

        # Pedir confirmación
        confirmacion = input("\nConfirmar (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Verificar si es el último ID
            if int(estudio_id_normalizado) == ultimo_id:
                ultimo_id -= 1
                guardar_ultimo_id()
                print(f"Último ID ajustado a {ultimo_id:03d}")
            
            del base_estudios[estudio_id_normalizado]
            guardar_base_datos()
            print("\n¡Estudio eliminado con éxito!")
        else:
            print("\nEliminación cancelada")
    else:
        print("\nError: Estudio no encontrado")

def buscar_estudio():
    """Busca un estudio por su ID o título."""
    print("\n--- Buscar Estudio ---\n")
    print("1. Buscar por ID")
    print("2. Buscar por título")
    opcion = input("\nElija el tipo de búsqueda (1-2): ").strip()
    
    if opcion == '1':
        # Búsqueda por ID
        estudio_id = input("ID del Estudio: ").strip()
        try:
            estudio_id_normalizado = f"{int(estudio_id):03d}"
        except ValueError:
            print("\nError: El ID debe ser un número")
            return
            
        if estudio_id_normalizado in base_estudios:
            datos = base_estudios[estudio_id_normalizado]
            print("\nEstudio encontrado:")
            imprimir_estudio(estudio_id_normalizado, base_estudios[estudio_id_normalizado])

        else:
            print("\nError: Estudio no encontrado")
            
    elif opcion == '2':
        # Búsqueda por título
        titulo_buscar = input("Ingrese el título a buscar: ").strip().lower()
        encontrados = []
        
        for estudio_id, datos in base_estudios.items():
            if titulo_buscar in datos['titulo'].lower():
                encontrados.append((estudio_id, datos))
        
        if encontrados:
            print(f"\nSe encontraron {len(encontrados)} estudios:")
            for estudio_id, datos in encontrados:
                imprimir_estudio(estudio_id_normalizado, base_estudios[estudio_id_normalizado])

        else:
            print("\nNo se encontraron estudios con ese título")
            
    else:
        print("\nOpción inválida. Por favor ingrese 1 o 2")

# ------------------------------ #

def seleccionar_estilos():
    """Función auxiliar para seleccionar múltiples estilos."""
    print("\nEstilos Disponibles:")
    print("1 = Hatha [default]")
    print("2 = Vinyasa")
    print("3 = Ashtanga")
    print("4 = Yin")
    print("5 = Otros")
    print("Para seleccionar múltiples estilos separa con comas (ej: 2,3)")
    
    while True:
        estilo_choices = input("\n- Estilos [1]: ").strip()
        if not estilo_choices:
            return ["Hatha"]
        
        selected = [c.strip() for c in estilo_choices.split(',')]
        
        if all(c in ['1', '2', '3', '4', '5'] for c in selected):
            break
        print("Opción inválida. Por favor ingrese números del 1 al 5, separados por comas")
    
    # Mapear números a nombres de estilos
    estilos_map = {
        '1': 'Hatha',
        '2': 'Vinyasa',
        '3': 'Ashtanga',
        '4': 'Yin',
        '5': 'Otros'
    }
    return [estilos_map[c] for c in selected]

def seleccionar_duracion():
    """Función auxiliar para seleccionar múltiples duraciones de clase."""
    print("\nSeleccionar Duraciones:")
    print("1 = 45 min")
    print("2 = 60 min [default]")
    print("3 = 90 min")
    print("4 = 90+ min")
    print("5 = Otros")
    print("Para seleccionar múltiples estilos separa con comas (ej: 2,3)")

    
    while True:
        duracion_input = input("\n- Tiempo de clase [2]: ").strip()
        
        if not duracion_input:
            return ["60 min"]
        
        selecciones = [s.strip() for s in duracion_input.split(',')]
        
        if all(s in ['1', '2', '3', '4', '5'] for s in selecciones):
            break
        print("Opción inválida. Por favor ingrese números del 1 al 5, separados por comas")
    
    # Mapear números a duraciones
    duraciones_map = {
        '1': '45 min',
        '2': '60 min',
        '3': '90 min',
        '4': '90+ min',
        '5': 'Otros'
    }
    
    # Eliminar duplicados y mantener orden
    selecciones_unicas = []
    [selecciones_unicas.append(s) for s in selecciones if s not in selecciones_unicas]
    
    return [duraciones_map[s] for s in selecciones_unicas]

def seleccionar_intensidad():
    """Función auxiliar para seleccionar múltiples intensidades."""
    print("\nSeleccionar Intensidades (separar con comas para múltiples):")
    print("1 = Suave")
    print("2 = Moderada [default]")
    print("3 = Intensa")
    print("4 = Variable")
    print("5 = Personalizada")
    print("Para seleccionar múltiples intesidades separa con comas (ej: 2,3)")

    
    while True:
        intensidad_input = input("\n- Niveles de intensidad [2]: ").strip()
        
        # Si no se ingresa nada, usar valor por defecto (Moderada)
        if not intensidad_input:
            return ["Moderada"]
        
        # Procesar múltiples selecciones
        selecciones = [s.strip() for s in intensidad_input.split(',')]
        
        # Validar todas las opciones
        if all(s in ['1', '2', '3', '4', '5'] for s in selecciones):
            break
        print("Opción inválida. Por favor ingrese números del 1 al 5, separados por comas")
    
    # Mapear números a intensidades
    intensidad_map = {
        '1': 'Suave',
        '2': 'Moderada',
        '3': 'Intensa',
        '4': 'Variable',
        '5': 'Personalizada'
    }
    
    # Eliminar duplicados y mantener orden
    selecciones_unicas = []
    [selecciones_unicas.append(s) for s in selecciones if s not in selecciones_unicas]
    
    return [intensidad_map[s] for s in selecciones_unicas]

# Variable global para mantener los barrios registrados
barrios_registrados = []

def cargar_barrios():
    """Carga los barrios ya utilizados de la base de datos existente."""
    global barrios_registrados
    barrios_registrados = []
    for estudio in base_estudios.values():
        if 'barrio' in estudio and estudio['barrio'] not in barrios_registrados:
            barrios_registrados.append(estudio['barrio'])

def seleccionar_barrio():
    """Función auxiliar para seleccionar barrios con opción de agregar nuevos."""
    global barrios_registrados
    
    # Cargar barrios existentes de los estudios previos
    cargar_barrios()
    
    print("\nSeleccionar Barrio:")
    
    # Mostrar barrios registrados con números
    for i, barrio in enumerate(barrios_registrados, 1):
        print(f"{i} = {barrio}")
    
    print("O ingrese un nuevo barrio")
    
    while True:
        barrio_input = input("\n- Barrio (número o nombre): ").strip()
        
        if not barrio_input:
            print("Debe ingresar un barrio")
            continue
            
        # Si es un número de los mostrados
        if barrio_input.isdigit():
            index = int(barrio_input) - 1
            if 0 <= index < len(barrios_registrados):
                return barrios_registrados[index]
            print(f"Número inválido. Ingrese 1-{len(barrios_registrados)} o un nuevo barrio")
        else:
            # Es un nuevo barrio
            nuevo_barrio = barrio_input.title()  # Formato de título
            if nuevo_barrio not in barrios_registrados:
                barrios_registrados.append(nuevo_barrio)
            return nuevo_barrio

import urllib.parse

def extraer_datos_maps(input_maps):
    """
    Extrae la URL de Google Maps y las coordenadas (latitud, longitud) del código embed.
    Retorna un diccionario con: {'url': str, 'lat': str, 'lng': str} o None si no es válido.
    """
    resultado = {
        'url': None,
        'lat': None,
        'lng': None
    }
    
    # Extraer URL
    if input_maps.startswith('https://www.google.com/maps/embed?'):
        resultado['url'] = input_maps
    elif 'src="https://www.google.com/maps/embed?' in input_maps:
        start = input_maps.find('src="') + 5
        end = input_maps.find('"', start)
        resultado['url'] = input_maps[start:end]
    else:
        if 'https://www.google.com/maps/' in input_maps:
            print("\n⚠️  Por favor use el código 'embed', no la URL normal de Google Maps")
            print("Para obtener el código embed:")
            print("1. En Google Maps, haga clic en 'Compartir'")
            print("2. Seleccione 'Insertar un mapa'")
            print("3. Copie el código iframe completo")
        return None
    
    # Extraer coordenadas de la URL (si existe)
    if resultado['url']:
        try:
            parsed = urllib.parse.urlparse(resultado['url'])
            params = urllib.parse.parse_qs(parsed.query)
            if 'pb' in params:
                pb_parts = params['pb'][0].split('!')
                for part in pb_parts:
                    if part.startswith('3d'):  # Latitud
                        resultado['lat'] = part[2:]
                    elif part.startswith('2d'):  # Longitud
                        resultado['lng'] = part[2:]
        except Exception as e:
            print(f"⚠️  No se pudieron extraer coordenadas: {e}")
    
    return resultado if resultado['url'] else None

def seleccionar_maps():
    """Función auxiliar para ingresar el mapa de Google y extraer datos."""
    print("\nIngrese el código embed de Google Maps (iframe completo o URL)")
    
    while True:
        user_input = input("\n- Pegue el código o URL: ").strip()
        
        if not user_input:
            return None
            
        datos_maps = extraer_datos_maps(user_input)
        
        if datos_maps:
            if datos_maps['lat'] and datos_maps['lng']:
                print(f"\nCoordenadas detectadas: Lat {datos_maps['lat']}, Lng {datos_maps['lng']}")
            return datos_maps
        
        print("Formato no reconocido. Por favor:")
        print("1. Use el código embed completo (iframe) O")
        print("2. Solo la URL embed (que comience con https://www.google.com/maps/embed?)")


def ingresar_descripcion():
    """Solicita la descripción del estudio (opcional, máx. 500 caracteres)."""
    print("\nDescripción del estudio (opcional, máx. 500 caracteres):")
    
    while True:
        descripcion = input("- Descripción Corta: ").strip()
        caracteres = len(descripcion)
        
        # Si está vacía, retorna cadena vacía
        if not descripcion:
            return ""
            
        # Valida longitud máxima
        if caracteres > 500:
            print(f"\n¡ADVERTENCIA! La descripción tiene {caracteres} caracteres (máx. 500).")
            print("Fragmento:", descripcion[:100] + "...")  # Muestra preview
            print("Opciones: r=recorte automatico; v=volver a ingresar; s=usar igual")
            
            confirmacion = input("¿Qué desea hacer? : ").lower()
            if confirmacion == 'r':
                return descripcion[:500]  # Recorta
            elif confirmacion == 'v':
                continue  # Vuelve a pedir
            elif confirmacion == 's':
                return descripcion  # Acepta el texto largo
            else:
                print("Opción no válida. Se usará texto completo.")
                return descripcion
        else:
            print(f"\n✓ Longitud aceptable ({caracteres}/500 caracteres)")
            return descripcion
        
# Variable global para mantener los tipos de reserva registrados
reservas_registradas = ["No hace falta reserva previa"]  # Valor inicial

def seleccionar_reserva():
    """Función para seleccionar o crear tipo de reserva."""
    global reservas_registradas
    
    # Cargar reservas existentes de estudios previos
    reservas_utilizadas = set()
    for estudio in base_estudios.values():
        if 'reserva' in estudio and estudio['reserva'] not in reservas_registradas:
            reservas_registradas.append(estudio['reserva'])
    
    print("\nOpciones de Reserva:")
    for i, reserva in enumerate(reservas_registradas, 1):
        print(f"{i} = {reserva}")
    print("O ingrese un nuevo tipo de reserva")
    
    while True:
        reserva_input = input("\n- Seleccione número o ingrese modalidad de reserva [1]: ").strip()
        
        if not reserva_input:
            return reservas_registradas[0]  # Valor por defecto ("No hace falta reserva previa")
            
        # Si es un número de los mostrados
        if reserva_input.isdigit():
            index = int(reserva_input) - 1
            if 0 <= index < len(reservas_registradas):
                return reservas_registradas[index]
            print(f"Número inválido. Ingrese 1-{len(reservas_registradas)} o un nuevo tipo")
        else:
            # Es un nuevo tipo de reserva
            nueva_reserva = reserva_input
            if nueva_reserva not in reservas_registradas:
                reservas_registradas.append(nueva_reserva)
            return nueva_reserva


def normalizar_instagram(perfil):
    """Convierte cualquier formato de entrada a URL completa de Instagram sin / final"""
    perfil = perfil.strip()
    if not perfil:
        return ""
    
    # Si ya es una URL completa
    if perfil.startswith("https://www.instagram.com/"):
        return perfil.rstrip('/')  # Elimina / final si existe
    
    # Eliminar @ si está presente
    perfil = perfil.lstrip('@')
    
    return f"https://www.instagram.com/{perfil}"  # Sin / al final

def ingresar_instagram():
    print("\nPerfil de Instagram (opcional):")
    print("Acepta @perfil, perfil o URL completa")
    
    while True:
        entrada = input("- Instagram: ").strip()
        url = normalizar_instagram(entrada)
        
        if not entrada:
            confirm = input("¿Instagram? (s/n): ").strip().lower()
            if confirm == 'n':
                return ""
            continue
            
        print(f"URL que se guardará: {url}")
        confirm = input("¿Es correcto? (s/n): ").strip().lower()
        if confirm == 's':
            return url

def ingresar_instagram_post(instagram_default):
    print("\nPost/Reel de Instagram (opcional):")
    print(f"Dejar vacío para usar el perfil: {instagram_default}")
    
    entrada = input("- URL del post/reel: ").strip()
    if not entrada:
        return instagram_default
    
    # Validar formato básico y eliminar / final
    if "instagram.com/p/" in entrada or "instagram.com/reel/" in entrada:
        return entrada.rstrip('/')
    else:
        print("¡Formato no reconocido! Debe ser un post o reel de Instagram")
        return ingresar_instagram_post(instagram_default)

def ingresar_website():
    """Solicita URL de website (opcional)"""
    print("\nSitio web (opcional):")
    entrada = input("- URL: ").strip()
    
    if not entrada:
        return ""
    
    # Asegurar que comienza con http:// o https://
    if not entrada.startswith(('http://', 'https://')):
        entrada = f"https://{entrada}"
    
    return entrada.rstrip('/')

def agregar_comentarios():
    """Permite agregar múltiples comentarios con estilos y peso"""
    comentarios = []
    
    # Opciones de estilo
    estilos = {
        '1': {'nombre': 'Marrón-Montaña', 'clase': 'style-mountain'},
        '2': {'nombre': 'Verde-Lotus', 'clase': 'style-spa'},
        '3': {'nombre': 'Violeta-Docente', 'clase': 'style-person'},
        '4': {'nombre': 'Amarillo-Info', 'clase': 'style-info'},
        '5': {'nombre': 'Gris-Luna', 'clase': 'style-moon'},
        '6': {'nombre': 'Azul-Reseña', 'clase': 'style-quote'}
    }
    
    print("\n--- Agregar Comentarios ---")
    print("Ingrese los comentarios (deje vacío el texto para terminar):")
    
    while True:
        # Texto del comentario (obligatorio)
        texto = input("\nTexto del comentario: ").strip()
        if not texto:
            break
            
        # Autor (opcional)
        autor = input("Autor (opcional): ").strip() or None
        
        # Selección de estilo
        print("\nEstilos disponibles:")
        for num, estilo in estilos.items():
            print(f"{num}. {estilo['nombre']} ({estilo['clase']})")
        
        while True:
            opcion = input("\nSeleccione estilo [6]: ").strip() or '6'
            if opcion in estilos:
                cardcolor = estilos[opcion]['clase']
                break
            print("Opción inválida. Intente nuevamente.")
        
        # Peso (default 10)
        peso = input("Weight [10]: ").strip()
        weight = int(peso) if peso.isdigit() and 1 <= int(peso) <= 10 else 10
        
        # Crear comentario
        comentario = {
            'text': texto,
            'author': autor,
            'cardcolor': cardcolor,
            'weight': weight
        }
        
        comentarios.append(comentario)
        print(f"\n✔ Comentario agregado")
    
    return comentarios

# Variable global para mantener los otros registrados
otros_registrados = [
    "Meditación",
    "Prenatal",
    "Para Mayores",
    "Integral",
    "Restaurativo",
    "Kundalini",
    "Bikram",
    "Retiro",
    "Hot",
    "Online"
]

def seleccionar_otros():
    """Función para seleccionar múltiples opciones de 'Otros' con posibilidad de agregar nuevos."""
    global otros_registrados
    
    print("\nSeleccionar Otros (puede elegir múltiples separados por comas):")
    
    # Mostrar opciones registradas con números
    for i, otro in enumerate(otros_registrados, 1):
        print(f"{i} = {otro}")
    
    print("O ingrese nuevos valores separados por comas")
    
    while True:
        seleccion = input("\n- Otros (números o nombres separados por comas): ").strip()
        
        if not seleccion:
            return []
            
        seleccionados = []
        nuevos_valores = []
        
        # Procesar cada elemento separado por comas
        for item in seleccion.split(','):
            item = item.strip()
            
            # Si es un número de los mostrados
            if item.isdigit():
                index = int(item) - 1
                if 0 <= index < len(otros_registrados):
                    seleccionados.append(otros_registrados[index])
                else:
                    print(f"⚠️ Número {item} fuera de rango. Ignorando.")
            else:
                # Es un nuevo valor
                nuevo_valor = item.title()  # Formato de título
                if nuevo_valor not in otros_registrados:
                    otros_registrados.append(nuevo_valor)
                    nuevos_valores.append(nuevo_valor)
                seleccionados.append(nuevo_valor)
        
        # Mostrar confirmación
        if seleccionados:
            print("\nSeleccionados:")
            for sel in seleccionados:
                print(f"  • {sel}")
            
            if nuevos_valores:
                print("\nNuevos valores agregados:")
                for nuevo in nuevos_valores:
                    print(f"  • {nuevo}")
            
            confirmar = input("\n¿Confirmar selección? (s/n) [s]: ").strip().lower()
            if confirmar != 'n':
                return seleccionados
        else:
            print("⚠️ No se seleccionaron valores válidos. Intente nuevamente.")

# ------------------------------ #

def agregar_estudio():
    """Agrega un nuevo estudio a la base de datos."""
    print("\n--- Agregar Nuevo Estudio ---\n")
    
    # Get title (keeping in English as requested)
    title = input("- Nombre del Estudio: ").strip()
    
    date_input = input("- Fecha (YYYY-MM-DD) [si está vacio es hoy]: ").strip()
    date = date_input if date_input else obtener_date_actual()
    estilos = seleccionar_estilos()
    duracion = seleccionar_duracion()
    intensidad = seleccionar_intensidad()
    otros = seleccionar_otros()
    barrio = seleccionar_barrio()
    direccion = input("\n- Dirección: ").strip()
    datos_maps = seleccionar_maps()
    salon = input("\n- Número de salón [1]: ").strip() or "1"
    capacidad = input("\n- Capacidad [10]: ").strip() or "10"
    reserva = seleccionar_reserva()
    instagram = ingresar_instagram()
    instagram_post = ingresar_instagram_post(instagram) if instagram else ""
    instagram_review = ingresar_instagram_post("https://www.instagram.com/p/DJdIytrItm1/")  # Default
    website = ingresar_website()
    comentarios = agregar_comentarios()

    

    # Highlight & Draft
    estado = {
        'highlight': False,
        'draft': True,
        'weight': 10  # Valor por defecto
    }
    
    highlight_input = input("\n¿Destacar? (s/n) [n]: ").strip().lower()
    estado['highlight'] = highlight_input == 's'
    
    if estado['highlight']:
        # Mostrar estudios destacados existentes
        estudios_destacados = [
            f"ID: {id} - {data['title']} (Weight: {data.get('weight', 10)})"
            for id, data in base_estudios.items()
            if data.get('highlight', False)
        ]
        
        if estudios_destacados:
            print("\nEstudios destacados actuales:")
            for estudio in estudios_destacados:
                print(f"  • {estudio}")
        else:
            print("\nNo hay estudios destacados actualmente.")
        
        # Solicitar weight con validación - Agregar deafult de 10
        while True:
            try:
                weight = int(input("\nWeight [10]: ").strip() or "10")
                if 1 <= weight <= 100:
                    estado['weight'] = weight
                    break
                else:
                    print("Error: El weight debe estar entre 1 y 100")
            except ValueError:
                print("Error: Debe ingresar un número válido")
    
    # Configurar draft
    draft_input = input("\n¿Borrador? (s/n) [s]: ").strip().lower()
    estado['draft'] = draft_input != 'n'  # True para cualquier cosa que no sea 'n'

    descripcion = ingresar_descripcion()

    # Add to database
    estudio_id = generar_id()
    base_estudios[estudio_id] = {
        'title': title,
        'date': date,
        'estilos': estilos,
        'duracion': duracion,
        'intensidad': intensidad,
        'barrio': barrio,
        'direccion': direccion,
        'google_maps': {
            'url': datos_maps['url'],
            'coordenadas': {
                'lat': datos_maps['lat'],
                'lng': datos_maps['lng']}
                },
        'highlight': estado['highlight'],
        'weight': estado['weight'],
        'draft': estado['draft'],
        'descripcion': descripcion,
        'salon': salon,
        'capacidad': capacidad,
        'reserva': reserva,
        'instagram': instagram,
        'instagram_post': instagram_post,
        'instagram_review': instagram_review,
        'website': website,
        'comments': comentarios,
        'otros': otros,
       
    
    }

    guardar_base_datos()
    
    # Confirmation message
    print(f"\n¡Estudio agregado con éxito!\n")
    print(f"\n{estudio_id} - {title}")
    print(f"- Fecha: {date}")
    print(f"- Highlight: {estado['highlight']} - Weight: {estado['weight']}")
    print(f"- Draft: {estado['draft']}")
    
    print("\nTaxonomias")
    print(f"- Estilos: {', '.join(estilos)}")
    print(f"- Duración: {', '.join(duracion)}")
    print(f"- Intensidad: {', '.join(intensidad)}")
    print(f"- Barrio: {barrio}")
    print("Otros:", ", ".join(otros) if otros else " ")


    print("\nEstudio")
    print(f"- Direccion: {direccion}")
    print(f"- Salón: {salon}")
    print(f"- Capacidad: {capacidad}")
    print(f"- Modalidad de reserva: {reserva}")
    print(f"- Descripción corta: {descripcion}")

    print("\nInstagram & Website")
    print(f"- Instagram Perfil: {instagram}"),
    print(f"- Instagram Post Destacado: {instagram_post}"),
    print(f"- Instagram Reseña YEB: {instagram_review}"),
    print(f"- Website: {website}"),
    
    # En la sección de mensaje de confirmación, cambia:
    if base_estudios[estudio_id].get('comments'):
        print("\nComentarios:")
        for comentario in base_estudios[estudio_id]['comments']:
            autor = comentario.get('author', 'Anónimo')
            print(f"  • {comentario['text']} ({autor})")
            print(f"    [Estilo: {comentario['cardcolor']}, Peso: {comentario['weight']}]")



    print("\n¡Gracias por usar Śālāgṛham!")



def modificar_estudio():
    """Modifica un estudio existente."""
    print("\n--- Modificar Estudio ---")
    estudio_id = input("Ingrese el ID del estudio a modificar (ej. 001): ").strip()
    
    if estudio_id in base_estudios:
        print("\nDatos actuales:")
        print(f"Título: {base_estudios[estudio_id]['title']}")
        print(f"date: {base_estudios[estudio_id]['date']}")
        
        print("\nIngrese nuevos valores (deje vacío para mantener el actual):")
        nuevo_title = input(f"Nuevo título [{base_estudios[estudio_id]['title']}]: ").strip()
        nueva_date_input = input(f"Nueva date [{base_estudios[estudio_id]['date']}]: ").strip()
        
        if nuevo_title:
            base_estudios[estudio_id]['title'] = nuevo_title
        if nueva_date_input:
            base_estudios[estudio_id]['date'] = nueva_date_input
        elif not nueva_date_input and not nuevo_title:
            print("\nNo se realizaron cambios.")
            return
        
        guardar_base_datos()
        print("\n¡Estudio actualizado con éxito!")
    else:
        print("\nError: Estudio no encontrado")



def menu():
    """Muestra el menú principal y maneja la interacción con el usuario."""
    while True:
        try:    
            print("\n=== Menú Principal ===")
            print("1. Agregar nuevo estudio")
            print("2. Ver todos los estudios")
            print("3. Buscar estudio por ID")
            print("4. Modificar estudio")
            print("5. Eliminar estudio")
            print("6. Salir")
            print("7. Imprimir base de datos")
            print("8. Resetear base de datos")
            
            opcion = input("\nIngrese su opción (1-8): ").strip()
            
            if opcion == '1':
                agregar_estudio()
            elif opcion == '2':
                ver_todos()
            elif opcion == '3':
                buscar_estudio()
            elif opcion == '4':
                modificar_estudio()
            elif opcion == '5':
                eliminar_estudio()
            elif opcion == '6':
                input("\nPresione Enter para salir...")
                print("Que tengas un hermoso día! :)")
                print(" \n")
                break
            elif opcion == '7':
                print("\n--- Base de Datos ---\n")
                print(json.dumps(base_estudios, indent=4))
            elif opcion == '8':
                confirmacion = input("\n ⚠️ ¿ESTÁ SEGURO que desea resetear la base de datos? (s/n): ").strip().lower()
                if confirmacion == 's':
                    resetear_base_datos()
                    print("\n¡Base de datos reseteada correctamente!")
                else:
                    print("\nOperación cancelada.")
            else:
                print("\nOpción inválida. Por favor ingrese un número entre 1 y 8.")

        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            print("Volviendo al menú principal...")
            continue

if __name__ == "__main__":
    print("\nHola Mica :) Bienvenida a Śālāgṛham")
    print("Sistema de Gestión de Estudios de Yoga En Baires")
    print("En qué te puedo ayudar hoy?")

    menu()