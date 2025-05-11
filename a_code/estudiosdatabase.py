import os
import json
import csv
from datetime import datetime
import yaml  # pip install pyyaml

# Initialize the database
database = {}

# Fields to include in CSV export
CSV_FIELDS = [
    'id',
    'title',
    'date',
    'estilo',
    'duracion',
    'intensidad',
    'niveles',
    'barrio',
    'direccion:texto',
    'direccion:maps',
    'instagram',
    'salones',
    'capacidad'
]

# Fields to include in Markdown export
MD_FIELDS = [
    'title',
    'date',
    'id',
    'estilo',
    'duracion',
    'intensidad',
    'niveles',
    'barrio',
    'otros',
    'direccion',
    'instagram',
    'highlight',
    'draft',
    'descripcion',
    'salones',
    'capacidad',
    'reservas',
    'instagrampost',
    'instagramreview',
    'website',
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo',
    'comments'
]

def generate_id():
    """Generate a new sequential ID"""
    if not database:
        return "001"
    last_id = max(database.keys())
    new_num = int(last_id) + 1
    return f"{new_num:03d}"

def input_nested_field(field_name, parent_field=None):
    """Handle input for nested fields"""
    if field_name == 'direccion':
        return {
            'texto': input("Dirección (texto): "),
            'maps': input("Google Maps URL: ")
        }
    elif field_name == 'comments':
        comments = []
        while True:
            text = input("Comment text (or 'done' to finish): ")
            if text.lower() == 'done':
                break
            author = input("Author: ")
            cardcolor = input("Card color: ")
            comments.append({
                'text': text,
                'author': author,
                'cardcolor': cardcolor
            })
        return comments
    elif isinstance(field_name, list):
        values = []
        print(f"Enter {parent_field} (one per line, empty to finish):")
        while True:
            value = input().strip()
            if not value:
                break
            values.append(value)
        return values
    else:
        return input(f"{field_name}: ")

def create_studio():
    """Create a new yoga studio entry"""
    studio_id = generate_id()
    print(f"\nCreating new studio with ID: {studio_id}")
    
    studio = {
        'id': studio_id,
        'title': input("Title: "),
        'date': datetime.now().strftime("%Y-%m-%d"),
        'estilo': input_nested_field('estilo', 'estilo'),
        'duracion': input_nested_field('duracion', 'duracion'),
        'intensidad': input_nested_field('intensidad', 'intensidad'),
        'niveles': input_nested_field('niveles', 'niveles'),
        'barrio': input_nested_field('barrio', 'barrio'),
        'otros': input_nested_field('otros', 'otros'),
        'direccion': input_nested_field('direccion'),
        'instagram': input("Instagram URL: "),
        'highlight': False,
        'draft': False,
        'descripcion': input("Description: "),
        'salones': input("Number of rooms: "),
        'capacidad': input("Capacity: "),
        'reservas': input("Reservation info: "),
        'instagrampost': input("Instagram post URL (optional): "),
        'instagramreview': input("Instagram review URL (optional): "),
        'website': input("Website URL (optional): "),
        'lunes': input_nested_field('lunes', 'Monday schedule'),
        'martes': input_nested_field('martes', 'Tuesday schedule'),
        'miercoles': input_nested_field('miercoles', 'Wednesday schedule'),
        'jueves': input_nested_field('jueves', 'Thursday schedule'),
        'viernes': input_nested_field('viernes', 'Friday schedule'),
        'sabado': input_nested_field('sabado', 'Saturday schedule'),
        'domingo': input_nested_field('domingo', 'Sunday schedule'),
        'comments': input_nested_field('comments')
    }
    
    # Additional content
    studio['Content'] = input("\nLong description content:\n")
    
    database[studio_id] = studio
    print(f"\nStudio {studio_id} created successfully!")

def modify_studio():
    """Modify an existing yoga studio entry"""
    if not database:
        print("No studios in database.")
        return
    
    print("\nAvailable studios:")
    for studio_id, studio in database.items():
        print(f"{studio_id}: {studio['title']}")
    
    studio_id = input("\nEnter studio ID to modify: ")
    if studio_id not in database:
        print("Invalid ID.")
        return
    
    studio = database[studio_id]
    print(f"\nModifying studio {studio_id}: {studio['title']}")
    
    # Show current values and allow modification
    for key, value in studio.items():
        if key in ['id', 'date']:
            continue  # Don't modify these
        
        print(f"\nCurrent {key}: {value}")
        change = input(f"Change {key}? (y/n): ").lower()
        if change == 'y':
            if key in ['direccion', 'comments']:
                studio[key] = input_nested_field(key)
            elif isinstance(value, list):
                studio[key] = input_nested_field(key, key)
            else:
                studio[key] = input(f"New {key}: ")
    
    print(f"\nStudio {studio_id} updated successfully!")

def delete_studio():
    """Delete a yoga studio entry"""
    if not database:
        print("No studios in database.")
        return
    
    print("\nAvailable studios:")
    for studio_id, studio in database.items():
        print(f"{studio_id}: {studio['title']}")
    
    studio_id = input("\nEnter studio ID to delete: ")
    if studio_id not in database:
        print("Invalid ID.")
        return
    
    confirm = input(f"Are you sure you want to delete studio {studio_id}? (y/n): ").lower()
    if confirm == 'y':
        del database[studio_id]
        print(f"Studio {studio_id} deleted.")
    else:
        print("Deletion canceled.")

def export_json():
    """Export database to JSON file"""
    filename = "estudios.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    print(f"Database exported to {filename}")

def export_csv():
    """Export selected fields to CSV file"""
    filename = "estudios.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(CSV_FIELDS)
        
        # Write data rows
        for studio_id, studio in database.items():
            row = []
            for field in CSV_FIELDS:
                if ':' in field:  # Nested field
                    parent, child = field.split(':')
                    if parent in studio and child in studio[parent]:
                        row.append(studio[parent][child])
                    else:
                        row.append('')
                else:
                    if field in studio:
                        if isinstance(studio[field], list):
                            row.append(', '.join(studio[field]))
                        else:
                            row.append(studio[field])
                    else:
                        row.append('')
            writer.writerow(row)
    
    print(f"Selected fields exported to {filename}")

def export_markdown():
    """Export each studio to a separate Markdown file"""
    for studio_id, studio in database.items():
        # Create directory
        dir_name = f"{studio_id} {studio['title']}"
        os.makedirs(dir_name, exist_ok=True)
        
        # Prepare content for Markdown
        md_content = {}
        for field in MD_FIELDS:
            if field in studio:
                md_content[field] = studio[field]
        
        # Add YAML front matter
        yaml_content = yaml.dump(md_content, allow_unicode=True, sort_keys=False)
        full_content = f"---\n{yaml_content}---\n\n{studio.get('Content', '')}"
        
        # Write to file
        with open(os.path.join(dir_name, "index.md"), 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"Exported {dir_name}/index.md")

def swipe_clean():
    """Clear the database (for testing)"""
    global database
    confirm = input("Are you sure you want to clear the database? (y/n): ").lower()
    if confirm == 'y':
        database = {}
        print("Database cleared.")
    else:
        print("Operation canceled.")

def load_database():
    """Load database from JSON file if exists"""
    global database
    try:
        with open("estudios.json", 'r', encoding='utf-8') as f:
            database = json.load(f)
        print("Database loaded from estudios.json")
    except FileNotFoundError:
        print("No existing database found. Starting with empty database.")

def main_menu():
    """Display main menu and handle user input"""
    load_database()
    
    while True:
        print("\nYoga En Baires Database")
        print("---")
        print("1. Nuevo Estudio")
        print("2. Modificar Estudio")
        print("3. Eliminar Estudio")
        print("4. Crear/Update .json, .csv, .md")
        print("5. Swipe Clean")
        print("6. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            create_studio()
        elif choice == '2':
            modify_studio()
        elif choice == '3':
            delete_studio()
        elif choice == '4':
            export_json()
            export_csv()
            export_markdown()
        elif choice == '5':
            swipe_clean()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
    