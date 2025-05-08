import pandas as pd
from pathlib import Path

# Define the category mapping
category_map = {
    1: "StandingBalance",
    2: "SuryaNamaskar",
    3: "Rest",
    4: "FloorHips",
    5: "Viras",
    6: "FloorTwist",
    7: "FloorForward",
    8: "Standing",
    9: "Utkas",
    10: "Balance",
    11: "Inversions",
    12: "Preps",
    13: "Backbends",
    14: "Core"
}

def process_row(row):
    # Create the style part
    styles = []
    if pd.notna(row['Ashtanga']) and str(row['Ashtanga']).strip() != '':
        styles.append("Ashtanga")
    if pd.notna(row['Yin']) and str(row['Yin']).strip() != '':
        styles.append("Yin")
    if pd.notna(row['Baptiste']) and str(row['Baptiste']).strip() != '':
        styles.append("Power")
    
    # Create the categories part
    categories = []
    if pd.notna(row['Categories']):
        # Split categories by comma and convert to integers
        try:
            cat_numbers = [int(x.strip()) for x in str(row['Categories']).split(',') if x.strip().isdigit()]
            for num in cat_numbers:
                if num in category_map:
                    categories.append(category_map[num])
        except:
            pass
    
    # Combine all parts
    tags_parts = []
    
    # Add YogaSeries if present
    if pd.notna(row['YogaSeries']) and str(row['YogaSeries']).strip() != '':
        tags_parts.append(str(row['YogaSeries']).strip())
    
    # Add styles
    tags_parts.extend(styles)
    
    # Add SeriesHot if present
    if pd.notna(row['SeriesHot']) and str(row['SeriesHot']).strip() != '':
        tags_parts.append(str(row['SeriesHot']).strip())
    
    # Add categories
    tags_parts.extend(categories)
    
    # Join all parts with commas
    return ','.join(tags_parts)

def main():
    # Read the CSV file using raw string for Windows path
    input_path = r'C:\Users\mica_\Documents\crypta\.obsidian\code\anki_asana_list.csv'
    output_path = r'C:\Users\mica_\Documents\crypta\.obsidian\code\anki_asana_list_processed.csv'
    
    try:
        df = pd.read_csv(input_path)
        
        # Add the new style column
        df['Style'] = df.apply(lambda row: 
            'Ashtanga' if pd.notna(row['Ashtanga']) and str(row['Ashtanga']).strip() != '' else
            'Yin' if pd.notna(row['Yin']) and str(row['Yin']).strip() != '' else
            'Power' if pd.notna(row['Baptiste']) and str(row['Baptiste']).strip() != '' else
            '', axis=1)

        # Add the tags column
        df['Tags'] = df.apply(process_row, axis=1)

        # Save the modified DataFrame to a new CSV file
        df.to_csv(output_path, index=False)
        
        print(f"Processing complete. Output saved to {output_path}")
        print(f"Added {len(df)} records with new 'Style' and 'Tags' columns.")
        
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()