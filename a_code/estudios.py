import json
import os
from datetime import datetime
import urllib.parse
import requests
from config import API_KEY
from tabulate import tabulate
import yaml


# Constantes
ARCHIVO_DATOS = "estudios_database.json"
ARCHIVO_ID = "last_id.txt"
CLASES_JSON_FILE = "clases_guardadas.json"
NOMBRE_ARCHIVO_OTROS = 'otros_registrados.json'

# ------------------------------------------------#
# BASICAS: OTROS ---------------------------------#

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

# ------------------------------------------------#
# BASICAS: IMRPRIMIR,VER,BUSCAR, ELIMINAR --------#

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
    if 'otros' in datos and datos['otros']:
        print(f"- Otros: {', '.join(datos['otros'])}")

    print("\nEstudio")
    print(f"- Dirección: {datos.get('direccion', 'No especificada')}")
    if 'google_maps' in datos:
        print(f"- Google Maps URL: {datos['google_maps'].get('url', 'No especificada')}")
        if 'coordenadas' in datos['google_maps']:
            print(f"- Coordenadas: Lat {datos['google_maps']['coordenadas'].get('lat', 'No especificada')}, "
                  f"Lng {datos['google_maps']['coordenadas'].get('lng', 'No especificada')}")
    print(f"- Salón: {datos.get('salon', 'No especificado')}")
    print(f"- Capacidad: {datos.get('capacidad', 'No especificada')}")
    print(f"- Modalidad de reserva: {datos.get('reserva', 'No especificada')}")
    print(f"- Descripción corta: {datos.get('descripcion', 'No disponible')}")
    if 'content' in datos:
        print(f"- Reseña completa: {datos['content']}")

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

    if datos.get('horarios'):
        print("\nHorarios de Clase:")
        for dia, clases in datos['horarios'].items():
            print(f"\n{dia.capitalize()}:")
            for clase in clases:
                print(f"  • {clase['horario']} - {clase['clase']}")
                print(f"     Descripción: {clase.get('descripcion', 'Sin descripción')}")
                print(f"     Estilo: {clase.get('style', 'Sin estilo definido')}")

    if datos.get('visitas'):
        print("\nVisitas Registradas:")
        for visita_id, visita in datos['visitas'].items():
            print(f"\nVisita #{visita_id}:")
            print(f"- Fecha: {visita.get('Fecha', 'Sin fecha')}")
            print("Notas:")
            print(visita.get('Notas', 'Sin notas registradas'))

def ver_todos():
    """Muestra todos los estudios en la base de datos."""
    print("\n" + " Todos los estudios ".center(50, "-") + "\n")
    if not base_estudios:
        print("La base de datos está vacía")
        return
    
    ids_ordenados = sorted(base_estudios.keys(), key=lambda x: int(x))
    print("Total de estudios:", len(base_estudios), "\n")
    for estudio_id in ids_ordenados:
        datos = base_estudios[estudio_id]
        print(f"- {estudio_id} - {datos['title']}")

def eliminar_estudio():
    """Elimina un estudio y ajusta el último ID si es necesario."""
    global ultimo_id
    
    print("\n" + " Eliminar estudio ".center(50, "-"))
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
    print("\n" + " Buscar Estudios ".center(50, "-"))   
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

# ------------------------------------------------#
# TAXONOMIAS -------------------------------------#

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

NOMBRE_ARCHIVO_OTROS = 'otros_registrados.json'

def cargar_otros():
    """Carga las opciones de 'Otros' desde el archivo JSON."""
    if os.path.exists(NOMBRE_ARCHIVO_OTROS):
        with open(NOMBRE_ARCHIVO_OTROS, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Error al decodificar {NOMBRE_ARCHIVO_OTROS}. Se utilizará una lista vacía.")
                return []
    else:
        return []

def guardar_otros(otros):
    """Guarda la lista de 'Otros' en el archivo JSON."""
    with open(NOMBRE_ARCHIVO_OTROS, 'w') as f:
        json.dump(otros, f, indent=4)

otros_registrados = cargar_otros()

def seleccionar_otros():
    """Función para seleccionar múltiples opciones de 'Otros' con posibilidad de agregar nuevos, leyendo y guardando en JSON."""
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
                    nuevos_valores.append((len(otros_registrados), nuevo_valor))  # Guardamos (ID, valor)
                seleccionados.append(nuevo_valor)

        # Mostrar confirmación
        if seleccionados:
            print("\nSeleccionados:")
            for sel in seleccionados:
                print(f"  • {sel}")

            if nuevos_valores:
                print("\nNuevos valores agregados:")
                for id_valor in nuevos_valores:
                    print(f"  • {id_valor[1]} (ID: {id_valor[0]})")

            confirmar = input("\n¿Confirmar selección? (s/n) [s]: ").strip().lower()
            if confirmar != 'n':
                guardar_otros(otros_registrados)  # Guardar los cambios en el archivo
                return seleccionados
        else:
            print("⚠️ No se seleccionaron valores válidos. Intente nuevamente.")

# ------------------------------------------------#
# BARRIOS ----------------------------------------#

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

# --------------------------------------------- #
# GOOGLE MAPS Y DIRECCION --------------------- #

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

# ------------------------------------------------#
# DESCRIPCION CORTA ------------------------------#

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

# ------------------------------------------------#
# RESERVAS ---------------------------------------# AGREGAR RESERVAS EXTERNO

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


# ------------------------------------------------#
# INSTAGRAM & REDES ------------------------------#

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

# ------------------------------------------------#
# COMENTARIOS ------------------------------------#

def agregar_comentarios():
    """Permite agregar múltiples comentarios con estilos y peso"""
    comentarios = []
    
    # Opciones de estilo
    estilos = {
        '1': {'nombre': 'Marrón - Montaña', 'clase': 'style-mountain'},
        '2': {'nombre': 'Verde - Lotus', 'clase': 'style-spa'},
        '3': {'nombre': 'Violeta - Docente', 'clase': 'style-person'},
        '4': {'nombre': 'Amarillo - Info', 'clase': 'style-info'},
        '5': {'nombre': 'Gris - Luna', 'clase': 'style-moon'},
        '6': {'nombre': 'Azul - Reseña', 'clase': 'style-quote'}
    }
    
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
            print(f"{num}. {estilo['nombre']}")
        
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

# ------------------------------------------------#
# HORARIO DE CLASES ------------------------------#

# Estructuras base para estilos y descripciones
estilos_clases = {
    1: {'nombre': 'Hatha', 'style': 'style-hatha', 'color': 'Azul'},
    2: {'nombre': 'Vinyasa', 'style': 'style-vinyasa', 'color': 'Rojo'},
    3: {'nombre': 'Ashtanga', 'style': 'style-ashtanga', 'color': 'Verde'},
    4: {'nombre': 'Otros', 'style': 'style-otros', 'color': 'Marrón'},
    5: {'nombre': 'Otros', 'style': 'style-otros2', 'color': 'Violeta'}
}

descripciones_predeterminadas = {
    'Yin': 'Esto es una clase de Yin',
    'Vinyasa': 'Esto es una clase de Vinyasa',
    'Ashtanga': 'Esto es una clase de Ashtanga',
    'Hatha': 'Esto es una clase de Hatha'
}

# Variable para almacenar nuevas descripciones
descripciones_personalizadas = {}

dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

def seleccionar_estilo_clase():
    """Permite seleccionar un estilo de clase con sus propiedades."""
    print("\nSeleccionar estilo de clase:")
    for num, datos in estilos_clases.items():
        print(f"{num} = {datos['color']}-{datos['nombre']} ({datos['style']})")
    
    while True:
        opcion = input("\n- Elija número de estilo o escriba nuevo estilo: ").strip()
        
        if opcion.isdigit():
            num = int(opcion)
            if num in estilos_clases:
                return estilos_clases[num]
            print("Número inválido. Intente nuevamente.")
        else:
            # Nuevo estilo (small caps por defecto)
            nuevo_estilo = opcion.title()
            return {
                'nombre': nuevo_estilo,
                'style': f"style-{nuevo_estilo.lower()}",
                'color': 'Personalizado'
            }

def obtener_descripcion_clase(nombre_clase):
    """Obtiene descripción predeterminada o permite crear una nueva."""
    if nombre_clase in descripciones_predeterminadas:
        print(f"\nDescripción predeterminada para {nombre_clase}:")
        print(descripciones_predeterminadas[nombre_clase])
        
        usar_predet = input("¿Usar esta descripción? (s/n) [s]: ").strip().lower()
        if usar_predet != 'n':
            return descripciones_predeterminadas[nombre_clase]
    
    # Crear nueva descripción
    print(f"\nCrear descripción para '{nombre_clase}':")
    nueva_desc = input("Descripción (ej: 'Clase de trabajo muscular pasivo'): ").strip()
    
    # Guardar para futuras referencias
    if nombre_clase not in descripciones_personalizadas:
        desc_id = len(descripciones_personalizadas) + 1
        descripciones_personalizadas[desc_id] = {
            'clase': nombre_clase,
            'descripcion': nueva_desc
        }
        print(f"Nueva descripción guardada con ID: {desc_id}")
    
    return nueva_desc

def formatear_horario(horario_input):
    """Formatea el horario ingresado al formato HH:MM"""
    try:
        # Reemplazar puntos por dos puntos si es necesario
        horario = horario_input.replace('.', ':')
        
        # Si no tiene separador, agregar :00
        if ':' not in horario:
            horario += ':00'
        
        # Dividir horas y minutos
        partes = horario.split(':')
        horas = partes[0].zfill(2)  # Asegurar 2 dígitos para horas
        minutos = partes[1].ljust(2, '0')[:2]  # Tomar solo 2 dígitos para minutos
        
        return f"{horas}:{minutos}"
    except:
        return horario_input  # Si hay error, devolver el original

def mostrar_horario_semanal(horarios):
    """Muestra el horario en formato de lista por días"""

    print("\n" + " Horario Final Ingresado ".center(50, "-"))    
    for dia in dias_semana:
        print(f"\n{dia.upper()}".ljust(50, '-'))
        
        if dia in horarios and horarios[dia]:
            for clase in horarios[dia]:
                print(f"  • {clase['horario']} - {clase['clase']}")
                if clase['descripcion']:
                    print(f"    Descripción: {clase['descripcion']}")
                if clase.get('style'):
                    print(f"    Estilo: {clase['style']}")
                print()  # Espacio entre clases
        else:
            print("  No hay clases programadas")
    
    print("="*50)

def ordenar_horarios(horarios):
    """Ordena las clases por hora en cada día"""
    for dia in horarios:
        horarios[dia].sort(key=lambda x: x['horario'])
    return horarios

def modificar_clase(clases_dia):
    """Permite modificar una clase específica"""
    print("\nClases disponibles:")
    for i, clase in enumerate(clases_dia, 1):
        print(f"{i}. {clase['horario']} - {clase['clase']}")
    
    while True:
        num = input("\nNúmero de clase a modificar (0 para cancelar): ").strip()
        if num == '0':
            return False
        if num.isdigit() and 0 < int(num) <= len(clases_dia):
            clase = clases_dia[int(num)-1]
            break
        print("Número inválido")
    
    print("\n¿Qué deseas modificar?")
    print("1. Día")
    print("2. Horario")
    print("3. Nombre de clase")
    print("4. Descripción")
    print("5. Estilo")
    print("6. Todo correcto")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == '1':
        nuevo_dia = seleccionar_dia()
        return {'clase': clase, 'nuevo_dia': nuevo_dia}
    elif opcion == '2':
        clase['horario'] = input(f"Nuevo horario ({clase['horario']}): ").strip() or clase['horario']
        clase['horario'] = formatear_horario(clase['horario'])
    elif opcion == '3':
        clase['clase'] = input(f"Nuevo nombre ({clase['clase']}): ").strip() or clase['clase']
    elif opcion == '4':
        clase['descripcion'] = input(f"Nueva descripción ({clase['descripcion']}): ").strip() or clase['descripcion']
    elif opcion == '5':
        nuevo_estilo = seleccionar_estilo_clase()
        clase['style'] = nuevo_estilo['style']
    
    return True

def seleccionar_dia():
    """Permite seleccionar un día de la semana"""
    print("\nDías disponibles:")
    for i, dia in enumerate(dias_semana, 1):
        print(f"{i}. {dia.capitalize()}")
    
    while True:
        num = input("\nSeleccione día (1-7): ").strip()
        if num.isdigit() and 1 <= int(num) <= 7:
            return dias_semana[int(num)-1]
        print("Opción inválida")

def formatear_horario(horario_input):
    """Formatea el horario ingresado al formato HH:MM"""
    try:
        # Reemplazar puntos por dos puntos si es necesario
        horario = horario_input.replace('.', ':')
        
        # Si no tiene separador, agregar :00
        if ':' not in horario:
            horario += ':00'
        
        # Dividir horas y minutos
        partes = horario.split(':')
        horas = partes[0].zfill(2)  # Asegurar 2 dígitos para horas
        minutos = partes[1].ljust(2, '0')[:2]  # Tomar solo 2 dígitos para minutos
        
        return f"{horas}:{minutos}"
    except:
        return horario_input  # Si hay error, devolver el original

def ordenar_horarios(horarios):
    """Ordena las clases por hora en cada día"""
    for dia in horarios:
        horarios[dia].sort(key=lambda x: x['horario'])
    return horarios

def modificar_clase(clases_dia, dia_actual):
    """Permite modificar una clase específica"""
    print(f"\nClases programadas para {dia_actual.upper()}:")
    for i, clase in enumerate(clases_dia, 1):
        print(f"{i}. {clase['horario']} - {clase['clase']}")
    
    while True:
        num = input("\nNúmero de clase a modificar (0 para cancelar): ").strip()
        if num == '0':
            return False
        if num.isdigit() and 0 < int(num) <= len(clases_dia):
            clase = clases_dia[int(num)-1]
            break
        print("Número inválido. Intente nuevamente.")
    
    print("\n¿Qué deseas modificar?")
    print("1. Día completo")
    print("2. Horario")
    print("3. Nombre de clase")
    print("4. Descripción")
    print("5. Estilo")
    print("6. Eliminar clase")
    print("7. Todo correcto (no modificar)")
    
    opcion = input("\nOpción [7]: ").strip() or "7"
    
    if opcion == '1':
        nuevo_dia = seleccionar_dia(excluir_actual=dia_actual)
        return {'clase': clase, 'nuevo_dia': nuevo_dia, 'dia_actual': dia_actual}
    elif opcion == '2':
        nuevo_horario = input(f"Nuevo horario (actual: {clase['horario']}): ").strip()
        if nuevo_horario:
            clase['horario'] = formatear_horario(nuevo_horario)
    elif opcion == '3':
        nuevo_nombre = input(f"Nuevo nombre (actual: {clase['clase']}): ").strip()
        if nuevo_nombre:
            clase['clase'] = nuevo_nombre
    elif opcion == '4':
        nueva_desc = input(f"Nueva descripción (actual: {clase['descripcion']}):\n").strip()
        if nueva_desc:
            clase['descripcion'] = nueva_desc
    elif opcion == '5':
        print("\nSeleccionar nuevo estilo:")
        nuevo_estilo = seleccionar_estilo_clase()
        clase['style'] = nuevo_estilo['style']
    elif opcion == '6':
        confirmar = input(f"¿Eliminar clase {clase['clase']}? (s/n): ").strip().lower()
        if confirmar == 's':
            clases_dia.remove(clase)
            return {'eliminada': True}
    
    return {'modificada': True}

def seleccionar_dia(excluir_actual=None):
    """Permite seleccionar un día de la semana, excluyendo opcionalmente uno"""
    print("\nDías disponibles:")
    dias_disponibles = [dia for dia in dias_semana if dia != excluir_actual]
    
    for i, dia in enumerate(dias_disponibles, 1):
        print(f"{i}. {dia.capitalize()}")
    
    while True:
        num = input("\nSeleccione día: ").strip()
        if num.isdigit() and 1 <= int(num) <= len(dias_disponibles):
            return dias_disponibles[int(num)-1]
        print(f"Opción inválida. Ingrese 1-{len(dias_disponibles)}")

# Variable global para clases guardadas (persistente entre llamadas a la función)
clases_guardadas_global = {}

# Nombre del archivo JSON para guardar las clases
CLASES_JSON_FILE = "clases_guardadas.json"

def cargar_clases_guardadas():
    """Carga las clases guardadas desde el archivo JSON."""
    if os.path.exists(CLASES_JSON_FILE):
        try:
            with open(CLASES_JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Advertencia: Error al leer el archivo de clases. Se creará uno nuevo.")
            return {}
    return {}

def guardar_clases_guardadas(clases):
    """Guarda las clases en el archivo JSON."""
    try:
        with open(CLASES_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(clases, f, ensure_ascii=False, indent=2)
    except IOError:
        print("Error: No se pudo guardar las clases en el archivo.")

def agregar_horario_clases():
    """Agrega horarios de clases por día con todas las validaciones."""
    # Cargar clases guardadas al inicio
    clases_guardadas = cargar_clases_guardadas()
    
    horarios = {}
    
    print("\n" + " Horarios de Clase ".center(50, "-"))
    print("-" * 50)  # Línea continua de 50 guiones
    print("Instrucciones:")
    print("- Ingrese horarios en formato 8, 8.30, 8:45, etc.")
    print("- Deje vacío para omitir días")
    print("- Se ordenarán automáticamente por hora\n")


    def mostrar_clases_guardadas():
        if clases_guardadas:
            print("\nClases guardadas:")
            for idx, (nombre, datos) in enumerate(clases_guardadas.items(), 1):
                print(f"{idx}. {nombre} - Descripción: {datos['descripcion']}")
        else:
            print("\nNo hay clases guardadas aún")

    for dia in dias_semana:
        clases_dia = []
        print("\n" + f" DÍA: {dia.upper()} ".center(50, "-"))
        
        # Opción de copiar cualquier día anterior con clases
        dias_con_clases = [d for d in dias_semana[:dias_semana.index(dia)] if d in horarios and horarios[d]]
        
        if dias_con_clases:
            print("\nOpciones para copiar horario:")
            for i, d in enumerate(dias_con_clases, 1):
                print(f"{i}. Copiar horario de {d.upper()}")
            print(f"{len(dias_con_clases)+1}. No copiar (crear nuevo horario)")
            
            while True:
                opcion = input(f"\nSeleccione día a copiar (1-{len(dias_con_clases)+1}) [{len(dias_con_clases)+1}]: ").strip() or str(len(dias_con_clases)+1)
                
                if opcion.isdigit():
                    num = int(opcion)
                    if 1 <= num <= len(dias_con_clases):
                        dia_a_copiar = dias_con_clases[num-1]
                        horarios[dia] = [clase.copy() for clase in horarios[dia_a_copiar]]
                        print(f"\nHorario de {dia_a_copiar.capitalize()} copiado a {dia.capitalize()}")
                        break
                    elif num == len(dias_con_clases)+1:
                        break
                print(f"Opción inválida. Ingrese 1-{len(dias_con_clases)+1}")
            
            if dia in horarios:  # Si se copió un horario, continuar al siguiente día
                continue
        
        while True:
            # Mostrar resumen del día actual
            if clases_dia:
                print(f"\nClases cargadas para {dia.upper()}:")
                for i, clase in enumerate(clases_dia, 1):
                    print(f"  {i}. {clase['horario']} - {clase['clase']}")
            else:
                print("\nNo hay clases programadas para este día")
            
            # Opciones del menú
            print("\nOpciones:")
            print("1. Agregar clase")
            print("2. Modificar/Eliminar clase")
            print("3. Continuar al siguiente día")
            opcion = input("\nSeleccione opción [3]: ").strip() or "3"
            
            if opcion == "3":
                # Confirmación para terminar el día
                if clases_dia:
                    print("\n" + f" Horario Preliminar {dia.upper()} ".center(50, "-"))
                    for clase in clases_dia:
                        print(f"  - {clase['horario']} {clase['clase']}: {clase['descripcion']}")
                
                confirmar = input(f"\n¿Confirmar horario de {dia.upper()}? (s/n) [s]: ").strip().lower() or 's'
                if confirmar == 's':
                    if clases_dia:
                        horarios[dia] = clases_dia
                    break
                else:
                    continue
            
            elif opcion == "1":
                # Agregar nueva clase
                print(f"\nAgregar clase para {dia.upper()}:")
                
                # Obtener horario
                while True:
                    horario_input = input("Horario (ej: 8, 8.30, 8:45): ").strip()
                    if not horario_input:
                        print("Horario no puede estar vacío")
                        continue
                    horario = formatear_horario(horario_input)
                    break
                
                # Mostrar clases guardadas
                mostrar_clases_guardadas()
                
                # Obtener nombre de clase
                nombre_clase = input("\nNombre de la clase (ej: Yin Yoga) o número de clase guardada: ").strip()
                while not nombre_clase:
                    print("Nombre no puede estar vacío")
                    nombre_clase = input("Nombre de la clase: ").strip()
                
                # Verificar si es una clase guardada
                if nombre_clase.isdigit():
                    num = int(nombre_clase)
                    if 1 <= num <= len(clases_guardadas):
                        nombre_clase = list(clases_guardadas.keys())[num-1]
                        clase_existente = clases_guardadas[nombre_clase]
                        
                        nueva_clase = {
                            'horario': horario,
                            'clase': nombre_clase,
                            'descripcion': clase_existente['descripcion'],
                            'style': clase_existente['style']
                        }
                        
                        clases_dia.append(nueva_clase)
                        clases_dia.sort(key=lambda x: x['horario'])
                        continue
                
                # Si no es una clase guardada, crear nueva
                print("\nSeleccionar estilo de clase:")
                print("1 = Hatha (Azul)")
                print("2 = Vinyasa (Rojo)")
                print("3 = Ashtanga (Verde)")
                print("4 = Yin (Naranja)")
                print("5 = Otros (Violeta)")
                print("6 = Otros (Marron)")
                
                while True:
                    estilo_opcion = input("\nElija número de estilo (1-6) [6]: ").strip() or "6"
                    if estilo_opcion in ['1', '2', '3', '4', '5', '6']:
                        break
                    print("Opción inválida. Ingrese 1-5")
                
                estilos = {
                    '1': {'nombre': 'Hatha', 'style': 'style-hatha'},
                    '2': {'nombre': 'Vinyasa', 'style': 'style-vinyasa'},
                    '3': {'nombre': 'Ashtanga', 'style': 'style-ashtanga'},
                    '6': {'nombre': 'Otros', 'style': 'style-otros'},
                    '5': {'nombre': 'Otros', 'style': 'style-otros2'},
                    '4': {'nombre': 'Yin', 'style': 'style-yin'}
                }
                estilo = estilos[estilo_opcion]
                
                                # Obtener descripción
                # Obtener descripción
                desc_existentes = [v for k,v in clases_guardadas.items() if nombre_clase.lower() in k.lower()]
                if desc_existentes:
                    print("\nDescripciones existentes para clases similares:")
                    for i, desc in enumerate(desc_existentes, 1):
                        print(f"{i}. {desc['descripcion']}")
                    
                    opcion_desc = input("\nSeleccione número de descripción o escriba nueva: ").strip()
                    if opcion_desc.isdigit() and 1 <= int(opcion_desc) <= len(desc_existentes):
                        descripcion = desc_existentes[int(opcion_desc)-1]['descripcion']
                    else:
                        # Si el usuario escribió algo que no es un número, usar eso como nueva descripción
                        descripcion = opcion_desc if opcion_desc else input("Descripción: ").strip()
                else:
                    descripcion = input("Descripción: ").strip()

                # Guardar clase (se guardará en el JSON al final)
                if nombre_clase not in clases_guardadas:
                    clases_guardadas[nombre_clase] = {
                        'descripcion': descripcion,
                        'style': estilo['style']
                    }
                
                clases_dia.append({
                    'horario': horario,
                    'clase': nombre_clase,
                    'descripcion': descripcion,
                    'style': estilo['style']
                })
                
                # Ordenar después de agregar
                clases_dia.sort(key=lambda x: x['horario'])
            
            elif opcion == "2" and clases_dia:
                # Modificar/Eliminar clase existente
                resultado = modificar_clase(clases_dia, dia)
                
                if resultado and 'nuevo_dia' in resultado:
                    # Mover clase a otro día
                    clases_dia.remove(resultado['clase'])
                    nuevo_dia = resultado['nuevo_dia']
                    if nuevo_dia not in horarios:
                        horarios[nuevo_dia] = []
                    horarios[nuevo_dia].append(resultado['clase'])
                    horarios[nuevo_dia].sort(key=lambda x: x['horario'])
                
                # Reordenar después de modificar
                clases_dia.sort(key=lambda x: x['horario'])
    
    # Guardar las clases actualizadas en el JSON
    guardar_clases_guardadas(clases_guardadas)
    
    # Procesamiento final
    horarios = ordenar_horarios(horarios)
    
    # Mostrar resumen completo
    mostrar_horario_semanal(horarios)
    
    # Confirmación final con opción de modificación
    while True:
        print("\nOpciones finales:")
        print("1. Confirmar y guardar horario")
        print("2. Modificar horario existente")
        print("3. Descartar todo y comenzar de nuevo")
        opcion = input("\nSeleccione opción [1]: ").strip() or "1"
        
        if opcion == "1":
            return horarios
        elif opcion == "2":
            print("\nSeleccione día a modificar:")
            dia_mod = seleccionar_dia()
            
            if dia_mod in horarios:
                resultado = modificar_clase(horarios[dia_mod], dia_mod)
                
                if resultado:
                    if 'nuevo_dia' in resultado:
                        # Mover clase a otro día
                        horarios[dia_mod].remove(resultado['clase'])
                        nuevo_dia = resultado['nuevo_dia']
                        if nuevo_dia not in horarios:
                            horarios[nuevo_dia] = []
                        horarios[nuevo_dia].append(resultado['clase'])
                    
                    # Reordenar y mostrar cambios
                    horarios = ordenar_horarios(horarios)
                    mostrar_horario_semanal(horarios)
            else:
                print(f"\nNo hay clases programadas para {dia_mod}.upper")
                agregar = input(f"¿Desea agregar clases a {dia_mod}.upper? (s/n): ").strip().lower()
                if agregar == 's':
                    pass
        elif opcion == "3":
            confirmar = input("\n¿Está seguro de descartar todo el horario? (s/n): ").strip().lower()
            if confirmar == 's':
                return agregar_horario_clases()  # Reiniciar proceso

# ----------------------------------------------- #
# YAML ------------------------------------------ #

def generate_yaml(estudio_id):
    """Generate YAML output for a given studio ID"""
    estudio = base_estudios[estudio_id]
    
    # Prepare the YAML structure with clean ID (no leading zeros)
    yaml_data = {
        'title': estudio['title'],
        'date': estudio['date'],
        'id': str(int(estudio_id)),  # Remove leading zeros
        'estilo': estudio['estilos'],
        'duracion': estudio['duracion'],
        'intensidad': estudio['intensidad'],
        'barrio': [estudio['barrio']],
        'direccion': {
            'texto': estudio['direccion'],
            'maps': estudio['google_maps']['url']
        },
        'instagram': estudio['instagram'],
        'highlight': estudio['highlight'],
        'descripcion': estudio['descripcion'],
        'salones': estudio['salon'],
        'capacidad': estudio['capacidad'],
        'reservas': estudio['reserva'],
        'instagrampost': estudio['instagram_post'],
        'instagramreview': estudio['instagram_review'],
        'website': estudio['website']
    }
    
    # Add schedule (horarios)
    if 'horarios' in estudio and estudio['horarios']:
        for dia, clases in estudio['horarios'].items():
            yaml_data[dia] = []
            for clase in clases:
                yaml_data[dia].append({
                    'horario': clase['horario'],
                    'clase': clase['clase'],
                    'descripcion': clase['descripcion'],
                    'style': clase['style'].replace('style-', '')
                })
    
    # Add comments if they exist
    if estudio.get('comments'):
        yaml_data['comments'] = []
        for comentario in estudio['comments']:
            comment_entry = {
                'text': comentario['text'],
                'cardcolor': comentario['cardcolor'].replace('style-', '')
            }
            if 'author' in comentario and comentario['author']:
                comment_entry['author'] = comentario['author']
            yaml_data['comments'].append(comment_entry)
    
    # Generate YAML with custom formatting
    yaml_output = "---\n"
    yaml_output += yaml.dump(yaml_data, allow_unicode=True, sort_keys=False, width=120)
    yaml_output += "---\n\n"
    
    # Add the descriptive text (content)
    if estudio.get('content'):
        yaml_output += estudio['content'] + "\n"
    
    return yaml_output

def save_yaml_to_file(estudio_id, filename=None):
    """Generate and save YAML to a file in a specific folder structure"""
    # Remove leading zeros from ID for folder naming
    clean_id = str(int(estudio_id))
    
    # Get study data
    estudio = base_estudios[estudio_id]
    
    # Create folder name: ID + Title (without special chars)
    folder_name = f"{clean_id} {estudio['title']}"
    
    # Sanitize folder name (remove invalid characters)
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '')
    
    # Create directory if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Set default filename
    if filename is None:
        filename = "index.md"
    
    # Generate YAML content
    yaml_content = generate_yaml(estudio_id)
    
    # Save to file
    file_path = os.path.join(folder_name, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"YAML file saved as {file_path}")

# ----------------------------------------------- #
# AGREGAR VISITAS ------------------------------- #

def agregar_visita(estudio_id):
    """Agrega una visita a un estudio específico."""
    print(f"\n--- Agregar Visita al Estudio ID: {estudio_id} ---")
    
    # Generar ID de visita secuencial
    visitas_existentes = base_estudios[estudio_id].get('visitas', {})
    nuevo_id = len(visitas_existentes) + 1
    
    # Obtener fecha de la visita
    fecha_input = input("- Fecha de la visita (YYYY-MM-DD) [Hoy]: ").strip()
    fecha = fecha_input if fecha_input else obtener_date_actual()
    
    # Obtener notas de la visita
    print("\nNotas de la visita (presione Enter dos veces para finalizar):")
    notas = []
    while True:
        linea = input()
        if not linea and notas:  # Finalizar con doble Enter
            break
        if linea:  # Ignorar líneas vacías intermedias
            notas.append(linea)
    
    # Crear estructura de visita
    visita = {
        'ID': nuevo_id,
        'Fecha': fecha,
        'Notas': '\n'.join(notas) if notas else "Sin notas"
    }
    
    # Agregar visita al estudio
    if 'visitas' not in base_estudios[estudio_id]:
        base_estudios[estudio_id]['visitas'] = {}
    
    base_estudios[estudio_id]['visitas'][nuevo_id] = visita
    guardar_base_datos()
    
    print(f"\n¡Visita #{nuevo_id} agregada con éxito al estudio {estudio_id}!")
    print(f"Fecha: {fecha}")
    print(f"Notas: {visita['Notas']}")

def mostrar_visitas(estudio_id):
    """Muestra todas las visitas de un estudio."""
    visitas = base_estudios[estudio_id].get('visitas', {})
    
    if not visitas:
        print(f"\nEl estudio {estudio_id} no tiene visitas registradas.")
        return
    
    print(f"\n--- Visitas del Estudio {estudio_id} ---")
    for visita_id, visita in visitas.items():
        print(f"\nVisita #{visita_id} - Fecha: {visita['Fecha']}")
        print("Notas:")
        print(visita['Notas'])
    print("--------------------")

def menu_visitas(estudio_id):
    """Menú para gestionar visitas de un estudio."""
    while True:
        print("\n--- Gestión de Visitas ---")
        print("1. Agregar nueva visita")
        print("2. Ver visitas existentes")
        print("3. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            agregar_visita(estudio_id)
        elif opcion == "2":
            mostrar_visitas(estudio_id)
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# ----------------------------------------------- #
# AGREGAR ESTUDIO ------------------------------- #

def agregar_estudio():
    """Agrega un nuevo estudio a la base de datos."""

    print("\n" + "-" * 50) 
    print(" Ingresar Nuevo Estudio ".center(50, " "))
    print("-" * 50 + "\n") 

    # Get title (keeping in English as requested)
    title = input("- Nombre del Estudio: ").strip()
    date_input = input("- Fecha (YYYY-MM-DD) [si está vacio es hoy]: ").strip()
    date = date_input if date_input else obtener_date_actual()
    datos_maps = seleccionar_maps()
    direccion = input("\n- Dirección: ").strip()
    barrio = seleccionar_barrio()
 
    # Highlight & Draft
    estado = {
        'highlight': False,
        'draft': True,
        'weight': 10  # Valor por defecto
    }
    
    highlight_input = input("\n- ¿Destacar? (s/n) [n]: ").strip().lower()
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
    draft_input = input("\n- ¿Borrador? (s/n) [s]: ").strip().lower()
    estado['draft'] = draft_input != 'n'  # True para cualquier cosa que no sea 'n'
    
    print("\n" + " Taxonomias ".center(50, "-"))
    estilos = seleccionar_estilos()
    duracion = seleccionar_duracion()
    intensidad = seleccionar_intensidad()
    otros = seleccionar_otros()

    print("\n" + " Información del Espacio ".center(50, "-"))
    salon = input("\n- Número de salón [1]: ").strip() or "1"
    capacidad = input("\n- Capacidad [10]: ").strip() or "10"
    reserva = seleccionar_reserva()

    print("\n" + " Instagram & Website ".center(50, "-"))
    instagram = ingresar_instagram()
    instagram_post = ingresar_instagram_post(instagram) if instagram else ""
    instagram_review = ingresar_instagram_post("https://www.instagram.com/p/DJdIytrItm1/")  # Default
    website = ingresar_website()


    print("\n" + " Comentarios & Info Cards ".center(50, "-"))
    comentarios = agregar_comentarios()

    horarios = agregar_horario_clases()

    print("\n" + " Descripción Corta y Content ".center(50, "-"))
    descripcion = ingresar_descripcion()
    content = input("\n- Reseña: ").strip()

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
                'lng': datos_maps['lng']},
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
        'horarios': horarios,
        'content': content,
        'visitas': {}  # Inicializamos el diccionario de visitas vacío
    }

    guardar_base_datos()

    agregar_visita_ahora = input("\n¿Desea agregar una visita ahora? (s/n) [n]: ").strip().lower() or 'n'
    if agregar_visita_ahora == 's':
        agregar_visita(estudio_id)

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
    
    if base_estudios[estudio_id].get('comments'):
        print("\nComentarios:")
        for comentario in base_estudios[estudio_id]['comments']:
            autor = comentario.get('author', 'Anónimo')
            print(f"  • {comentario['text']} ({autor})")
            print(f"    [Estilo: {comentario['cardcolor']}, Peso: {comentario['weight']}]")
    
    if base_estudios[estudio_id].get('horarios'):
        print("\nHorarios de Clase")
        for dia, clases in base_estudios[estudio_id]['horarios'].items():
            print(f"\n{dia.capitalize()}:")
            for clase in clases:
                print(f"  • {clase['horario']} - {clase['clase']}")
                print(f"    Descripción: {clase['descripcion']}")
  
    else:
        print("\nHorarios: No se agregaron horarios de clases")

    print("\nDescripciones:")
    print(f"- Descripcion Corta: {descripcion}"),
    print(f"- Descripción Larga: {content}"),  

    print("\n¡Gracias por usar Śālāgṛham!")

def modificar_estudio():
    """Modifica un estudio existente con menú por secciones."""
    print("\n" + "-" * 50)
    print(" MODIFICAR ESTUDIO ".center(50))
    print("-" * 50 + "\n")
    
    # Selección de estudio con normalización de ID
    estudio_id = input("Ingrese el ID del estudio a modificar: ").strip()
    
    try:
        estudio_id_normalizado = f"{int(estudio_id):03d}"
    except ValueError:
        print("\nError: El ID debe ser un número")
        return
        
    if estudio_id_normalizado not in base_estudios:
        print("\n⚠️ Error: Estudio no encontrado")
        return
    
    estudio = base_estudios[estudio_id_normalizado]
    
    while True:
        print("\n" + "-" * 50)
        print(f" Editando: {estudio_id} - {estudio['title']} ".center(50, "·"))
        print("\nSeleccione sección a modificar:")
        print(" 1. Información Básica (nombre, fecha, dirección, barrio)")
        print(" 2. Taxonomías (estilos, duración, intensidad, otros)")
        print(" 3. Información del Espacio (salón, capacidad, reserva)")
        print(" 4. Google Maps (dirección, coordenadas)")
        print(" 5. Redes Sociales (Instagram, website)")
        print(" 6. Comentarios & Info Cards")
        print(" 7. Horarios de Clases")
        print(" 8. Descripción y Contenido")
        print(" 9. Estado (destacado/borrador/weight)")
        print("10. Visitas")
        print("11. Guardar cambios y salir")
        print(" 0. Salir sin guardar")
        
        opcion = input("\nOpción: ").strip()
        
        if opcion == "1":
            print("\n" + " INFORMACIÓN BÁSICA ".center(50, "-"))
            estudio['title'] = input(f"Nombre [{estudio['title']}]: ").strip() or estudio['title']
            estudio['date'] = input(f"Fecha (YYYY-MM-DD) [{estudio['date']}]: ").strip() or estudio['date']
            estudio['direccion'] = input(f"Dirección [{estudio['direccion']}]: ").strip() or estudio['direccion']
            estudio['barrio'] = seleccionar_barrio()
            
        elif opcion == "2":
            print("\n" + " TAXONOMÍAS ".center(50, "-"))
            estudio['estilos'] = seleccionar_estilos()
            estudio['duracion'] = seleccionar_duracion()
            estudio['intensidad'] = seleccionar_intensidad()
            estudio['otros'] = seleccionar_otros()
            
        elif opcion == "3":
            print("\n" + " INFORMACIÓN DEL ESPACIO ".center(50, "-"))
            estudio['salon'] = input(f"Salón [{estudio.get('salon', '1')}]: ").strip() or estudio.get('salon', '1')
            estudio['capacidad'] = input(f"Capacidad [{estudio.get('capacidad', '10')}]: ").strip() or estudio.get('capacidad', '10')
            estudio['reserva'] = seleccionar_reserva()
            
        elif opcion == "4":
            print("\n" + " GOOGLE MAPS ".center(50, "-"))
            print("Configuración actual de Google Maps:")
            if 'google_maps' in estudio:
                print(f"URL: {estudio['google_maps'].get('url', 'No especificada')}")
                print(f"Coordenadas: {estudio['google_maps'].get('coordenadas', {}).get('lat', 'No especificada')}, "
                      f"{estudio['google_maps'].get('coordenadas', {}).get('lng', 'No especificada')}")
            
            if input("\n¿Modificar Google Maps? (s/n): ").strip().lower() == 's':
                datos_maps = seleccionar_maps()
                if datos_maps:
                    estudio['google_maps'] = {
                        'url': datos_maps['url'],
                        'coordenadas': {
                            'lat': datos_maps['lat'],
                            'lng': datos_maps['lng']
                        }
                    }
            
        elif opcion == "5":
            print("\n" + " REDES SOCIALES ".center(50, "-"))
            estudio['instagram'] = ingresar_instagram()
            if estudio['instagram']:
                estudio['instagram_post'] = ingresar_instagram_post(estudio['instagram'])
            estudio['instagram_review'] = ingresar_instagram_post("https://www.instagram.com/p/DJdIytrItm1/")
            estudio['website'] = ingresar_website()
            
        elif opcion == "6":
            print("\n" + " COMENTARIOS & INFO CARDS ".center(50, "-"))
            if estudio.get('comments'):
                print("\nComentarios actuales:")
                for i, comentario in enumerate(estudio['comments'], 1):
                    print(f"{i}. {comentario['text']} ({comentario.get('author', 'Anónimo')})")                
                print("\nOpciones:")
                print("1. Agregar nuevo comentario")
                print("2. Eliminar comentario existente")
                print("3. Reemplazar todos los comentarios")
                print("4. Mantener actuales")
                
                sub_opcion = input("\nElija opción [4]: ").strip() or "4"
                
                if sub_opcion == "1":
                    nuevo_comentario = agregar_comentarios()
                    estudio['comments'].extend(nuevo_comentario)
                elif sub_opcion == "2":
                    num = input("Número de comentario a eliminar: ").strip()
                    if num.isdigit() and 0 < int(num) <= len(estudio['comments']):
                        estudio['comments'].pop(int(num)-1)
                elif sub_opcion == "3":
                    estudio['comments'] = agregar_comentarios()
            else:
                estudio['comments'] = agregar_comentarios()
                
        elif opcion == "7":
            print("\n" + " HORARIOS DE CLASES ".center(50, "-"))
            if input("¿Modificar horarios? (s/n): ").strip().lower() == 's':
                estudio['horarios'] = agregar_horario_clases()
            
        elif opcion == "8":
            print("\n" + " DESCRIPCIÓN Y CONTENIDO ".center(50, "-"))
            estudio['descripcion'] = ingresar_descripcion()
            estudio['content'] = input("\nReseña completa:\n").strip() or estudio.get('content', '')
            
        elif opcion == "9":
            print("\n" + " ESTADO ".center(50, "-"))
            highlight = input(f"¿Destacar? (s/n) [{'s' if estudio.get('highlight', False) else 'n'}]: ").strip().lower() or ('s' if estudio.get('highlight', False) else 'n')
            estudio['highlight'] = highlight == 's'
            
            if estudio['highlight']:
                weight = input(f"Peso (1-100) [{estudio.get('weight', 10)}]: ").strip()
                estudio['weight'] = int(weight) if weight.isdigit() else estudio.get('weight', 10)
            
            draft = input(f"¿Borrador? (s/n) [{'s' if estudio.get('draft', True) else 'n'}]: ").strip().lower() or ('s' if estudio.get('draft', True) else 'n')
            estudio['draft'] = draft == 's'
            
        elif opcion == "10":
            print("\n" + " VISITAS ".center(50, "-"))
            menu_visitas(estudio_id)
            
        elif opcion == "11":
            guardar_base_datos()
            print("\n✅ Cambios guardados exitosamente")
            break
            
        elif opcion == "0":
            confirmar = input("\n⚠️ ¿Está seguro de salir sin guardar? (s/n): ").strip().lower()
            if confirmar == 's':
                print("\nCambios descartados")
                break
        else:
            print("\n⚠️ Opción no válida")

# ------------------------------------------------#
# MENU -------------------------------------#

def menu():
    """Muestra el menú principal y maneja la interacción con el usuario."""
    while True:
        try:    
            print("\n" + "-" * 50) 
            print(" Menu Principal ".center(50, " "))
            print("-" * 50 + "\n") 
            print("1. Agregar nuevo estudio")
            print("2. Ver todos los estudios")
            print("3. Buscar estudio por ID")
            print("4. Modificar estudio")
            print("5. Eliminar estudio")
            print("6. Generar YAML de estudio")
            print("7. Salir")
            print("8. Imprimir base de datos")
            print("9. Resetear base de datos")
            
            opcion = input("\nIngrese su opción (1-9): ").strip()
            
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
                # Nueva opción para generar YAML
                print("\n--- Generar YAML de Estudio ---")
                estudio_id = input("Ingrese el ID del estudio: ").strip()
                try:
                    estudio_id_normalizado = f"{int(estudio_id):03d}"
                    if estudio_id_normalizado in base_estudios:
                        filename = input(f"Nombre del archivo [estudio_{estudio_id_normalizado}.yaml]: ").strip()
                        filename = filename or f"estudio_{estudio_id_normalizado}.yaml"
                        save_yaml_to_file(estudio_id_normalizado, filename)
                    else:
                        print("\nError: Estudio no encontrado")
                except ValueError:
                    print("\nError: El ID debe ser un número")
            elif opcion == '7':
                input("\nPresione Enter para salir...")
                print("Que tengas un hermoso día! :)")
                print(" \n")
                break
            elif opcion == '8':
                print("\n--- Base de Datos ---\n")
                print(json.dumps(base_estudios, indent=4))
            elif opcion == '9':
                confirmacion = input("\n ⚠️ ¿ESTÁ SEGURO que desea resetear la base de datos? (s/n): ").strip().lower()
                if confirmacion == 's':
                    resetear_base_datos()
                    print("\n¡Base de datos reseteada correctamente!")
                else:
                    print("\nOperación cancelada.")
            else:
                print("\nOpción inválida. Por favor ingrese un número entre 1 y 9")

        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            print("Volviendo al menú principal...")
            continue


if __name__ == "__main__":
    print("\n" + "-" * 50) 
    print("\n" + " Hola Mica :) Bienvenida a Śālāgṛham ".center(50, " "))
    print(" Sistema de Gestión de Estudios de Yoga En Baires ".center(50, " "))
    print(" En qué te puedo ayudar hoy? ".center(50, " "))
    menu()