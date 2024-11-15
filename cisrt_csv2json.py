import csv
import json
from datetime import datetime
import re

def determine_phone_type(phone_number, call_type):
    """Détermine le type de numéro de téléphone basé sur son format et type d'appel"""
    if not phone_number:
        return None
        
    if call_type == "gratuit" or phone_number.startswith("0 800") or phone_number.startswith("0800"):
        return "toll_free"
    elif phone_number.startswith("09"):
        return "fixed_rate"
    elif phone_number.startswith("01") or phone_number.startswith("02") or phone_number.startswith("03") or phone_number.startswith("04") or phone_number.startswith("05"):
        return "local_rate"
    else:
        return "fixed_rate"

def format_time(time_str):
    """Convertit les heures du format 'XXhYY' en format 'HH:MM'"""
    if 'h' not in time_str:
        return time_str
    
    parts = time_str.split('h')
    hours = parts[0].strip()
    minutes = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "00"
    
    # Ajouter un zéro devant si nécessaire
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    
    return f"{hours}:{minutes}"

def parse_availability(availability_str):
    """Parse les horaires d'ouverture en structure standardisée"""
    if not availability_str:
        return None

    availability = {
        "type": "business-hours",
        "timezone": "Europe/Paris",
        "work_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
        "hours": [],
        "exceptions": [],
        "raw": availability_str
    }

    if "24h/24" in availability_str or "24/24" in availability_str:
        availability["type"] = "24-7"
        availability["hours"] = [{"start": "00:00", "end": "23:59"}]
        availability["work_days"].extend(["saturday", "sunday"])
        return availability

    if "astreinte" in availability_str.lower():
        availability["type"] = "business-hours-with-oncall"

    # Parse les heures standards
    time_ranges = re.findall(r'(\d{1,2}h\d{0,2})\s*-\s*(\d{1,2}h\d{0,2})', availability_str)
    for start, end in time_ranges:
        start_formatted = format_time(start)
        end_formatted = format_time(end)
        
        availability["hours"].append({
            "start": start_formatted,
            "end": end_formatted
        })

    if "férié" in availability_str.lower():
        availability["exceptions"].append("public_holidays")

    return availability

def format_phone_data(phone, call_type):
    """Formate les données de téléphone en structure standardisée"""
    if not phone:
        return None
    
    return {
        "number": phone,
        "type": determine_phone_type(phone, call_type)
    }

def convert_csv_to_json(csv_file):
    csirt_centers = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Construction de l'objet CSIRT
            csirt = {
                "name": row["CISRT"],
                "country": "FR",
                "region": row["Region"],
                "zone": row["Zone"] if row["Zone"] else None,
                "phone": format_phone_data(row["Numero de telephone"], row.get("type_appel")),
                "email": row["Mail"] if row["Mail"] else None,
                "website": row["Site Web"] if row["Site Web"] else None,
                
                "scope": {
                    "type": "overseas" if row["Region"] in ["Antilles, Guyane", "La Réunion", "Polynésie Française"] else "regional",
                    "audience": "public",
                    "sector": None,
                    "eligibility": {
                        "geographic": f"All organizations in {row['Region']}",
                        "organization_types": [
                            "companies",
                            "public_institutions",
                            "associations",
                            "local_authorities"
                        ],
                        "restrictions": None
                    }
                },

                "availability": parse_availability(row["Disponibilité"]),

                "rfc_2350": {
                    "document_url": row["RFC 2530"] if row["RFC 2530"] else None,
                    "version": "1.0",
                    "last_updated": datetime.now().strftime("%Y-%m-%d"),
                    "tlp_level": "WHITE",
                    
                    "team_information": {
                        "name": row["CISRT"],
                        "status": "TLP:WHITE",
                        "timezone": "Europe/Paris",
                        "operating_hours": row["Disponibilité"]
                    }
                }
            }
            
            # Nettoyer les valeurs None
            csirt = {k: v for k, v in csirt.items() if v is not None}
            csirt_centers.append(csirt)
    
    return {"csirt_centers": csirt_centers}

def save_json(data, output_file):
    """Sauvegarde les données en JSON avec indentation"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Utilisation du script
    input_csv = "CSIRT_France.csv"
    output_json = "csirt_france.json"
    
    try:
        data = convert_csv_to_json(input_csv)
        save_json(data, output_json)
        print(f"Conversion réussie ! Le fichier {output_json} a été créé.")
    except Exception as e:
        print(f"Erreur lors de la conversion : {str(e)}")