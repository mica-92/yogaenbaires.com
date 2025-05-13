import requests
import json
import time
from datetime import datetime

# Config
API_KEY = "AIzaSyDyoGPqU8Azdkio3V34bmazwhGFnpVa6qA"  # Replace with your actual key

import requests
import csv
import time
from math import radians, sin, cos, sqrt, atan2

LOCATIONS = {
    "Centro": {"coords": (-34.61349161568787, -58.38532160667667), "radius": 2600},
    
    "Coghlan": {"coords": (-34.5599888337661, -58.46331862080038), "radius": 3000},
    "Palermo": {"coords": (-34.5837996891416, -58.42026701394255), "radius": 2200},
    "Caballito": {"coords": (-34.6188, -58.44616), "radius": 3000},
    "ViLO": {"coords": (-34.525778230272905, -58.488243670392734), "radius": 2000},
    "San Isidro": {"coords": (-34.49189058564024, -58.50981957911854), "radius": 2500},
    "Banfield": {"coords": (-34.757585031869375, -58.40209308764139), "radius": 3000}
}


import requests
import csv
import time
from math import radians, sin, cos
from datetime import datetime

MAX_RESULTS_PER_ZONE = 1000  # Máximo deseado por zona
RESULTS_PER_API_CALL = 60  # Límite de Google por solicitud
BASE_RADIUS = 3000  # Radio inicial en metros (3km)
QUERY = "yoga studio"  # Término de búsqueda
LANGUAGE = "es"  # Idioma para los resultados
MIN_DELAY = 2  # Delay mínimo entre solicitudes (requerido por Google)
EXTRA_DELAY = 1  # Delay adicional para seguridad

# Configuración específica para Caballito
CABALLITO_CONFIG = {
    "name": "centro",
    "coords": (-34.61349161568787, -58.38532160667667),
    "radius": BASE_RADIUS
}

zone = "centro2"

def calculate_delay():
    """Calcula el delay necesario entre solicitudes considerando la hora actual"""
    now = datetime.now().time()
    # Durante horas pico (10-12 y 16-19), aumentar el delay
    if (10 <= now.hour < 12) or (16 <= now.hour < 19):
        return MIN_DELAY + 2
    return MIN_DELAY

def get_sub_areas(lat, lng, main_radius, num_sub_areas=6):
    """Divide un área circular en sub-áreas para búsquedas más focalizadas"""
    sub_areas = []
    for i in range(num_sub_areas):
        angle = radians(i * (360 / num_sub_areas))
        dx = main_radius * 0.7 * cos(angle) / 111320  # Conversión metros a grados
        dy = main_radius * 0.7 * sin(angle) / (111320 * cos(radians(lat)))
        sub_areas.append({
            "coords": (lat + dy, lng + dx),
            "radius": int(main_radius * 0.6)  # Radio reducido para sub-áreas
        })
    return sub_areas

def make_api_request(url, params, max_retries=3):
    """Realiza una solicitud a la API con manejo de errores y reintentos"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") in ["OK", "ZERO_RESULTS"]:
                    return data
                elif data.get("status") == "OVER_QUERY_LIMIT":
                    wait_time = (2 ** attempt) * 5  # Backoff exponencial
                    print(f"Límite de consultas excedido. Esperando {wait_time} segundos...")
                    time.sleep(wait_time)
                    continue
            else:
                print(f"Error HTTP {response.status_code}. Reintentando...")
        except Exception as e:
            print(f"Error en la solicitud: {e}. Reintentando...")
        
        if attempt < max_retries - 1:
            time.sleep(calculate_delay() + EXTRA_DELAY)
    
    return {"status": "REQUEST_FAILED"}

def get_places(api_key, location, radius, query, max_results):
    """Obtiene lugares con paginación y manejo adecuado de delays"""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places = []
    params = {
        "key": api_key,
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "keyword": query,
        "language": LANGUAGE
    }
    
    while len(places) < max_results:
        current_delay = calculate_delay()
        time.sleep(current_delay)
        
        data = make_api_request(url, params)
        
        if data["status"] != "OK":
            break
        
        new_places = [{
            "name": p["name"],
            "address": p.get("vicinity", "N/A"),
            "lat": p["geometry"]["location"]["lat"],
            "lng": p["geometry"]["location"]["lng"],
            "zone": zone
        } for p in data["results"]]
        
        places.extend(new_places)
        
        if "next_page_token" not in data or len(places) >= max_results:
            break
            
        params["pagetoken"] = data["next_page_token"]
        time.sleep(EXTRA_DELAY)  # Delay extra para tokens de página
    
    return places[:max_results]

def process_zone(zone_config):
    """Procesa una zona completa con posibles subdivisiones"""
    name, coords, radius = zone_config["name"], zone_config["coords"], zone_config["radius"]
    all_places = []
    
    # Búsqueda inicial en el área principal
    base_places = get_places(API_KEY, coords, radius, QUERY, RESULTS_PER_API_CALL)
    all_places.extend(base_places)
    print(f"{name}: Búsqueda inicial encontró {len(base_places)} lugares")
    
    # Si necesitamos más resultados, dividimos la zona
    if len(base_places) >= RESULTS_PER_API_CALL and len(all_places) < MAX_RESULTS_PER_ZONE:
        sub_areas = get_sub_areas(coords[0], coords[1], radius)
        for i, area in enumerate(sub_areas, 1):
            if len(all_places) >= MAX_RESULTS_PER_ZONE:
                break
                
            sub_places = get_places(
                API_KEY, 
                area["coords"], 
                area["radius"], 
                QUERY, 
                min(RESULTS_PER_API_CALL, MAX_RESULTS_PER_ZONE - len(all_places))
            )
            all_places.extend(sub_places)
            print(f"{name}: Sub-área {i} agregó {len(sub_places)} lugares (Total: {len(all_places)})")
            time.sleep(EXTRA_DELAY)
    
    # Eliminar duplicados
    unique_places = []
    seen = set()
    for place in all_places:
        key = (place["name"], round(place["lat"], 6), round(place["lng"], 6))
        if key not in seen:
            seen.add(key)
            unique_places.append(place)
            if len(unique_places) >= MAX_RESULTS_PER_ZONE:
                break
    
    return unique_places

def export_to_csv(places, filename):
    """Exporta los resultados a un archivo CSV"""
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "address", "lat", "lng", "zone"])
        writer.writeheader()
        writer.writerows(places)
    print(f"Datos exportados a {filename}")

# Ejecución principal
if __name__ == "__main__":
    start_time = time.time()
    print(f"Iniciando búsqueda en {CABALLITO_CONFIG['name']}...")
    
    caballito_places = process_zone(CABALLITO_CONFIG)
    
    print(f"\nResumen:")
    print(f"- Zona procesada: {CABALLITO_CONFIG['name']}")
    print(f"- Radio inicial: {CABALLITO_CONFIG['radius']} metros")
    print(f"- Lugares encontrados: {len(caballito_places)}")
    print(f"- Tiempo total: {time.time() - start_time:.2f} segundos")
    
    # Exportar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"yoga_studios_{zone}_{timestamp}.csv"
    export_to_csv(caballito_places, filename)