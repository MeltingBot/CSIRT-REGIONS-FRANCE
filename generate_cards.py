import json
from datetime import datetime

def generate_marp_presentation(csirt_data):
    # Initialize the presentation content
    presentation = []
    
    # Add header with Marp directives
    presentation.append("""---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

<!-- _class: lead -->
# CSIRTs en France
## État des lieux des centres de réponse aux incidents cyber régionaux
### {}

- {} CSIRTs régionaux en France métropolitaine et outre-mer
- Tous les CSIRTs couvrent : entreprises, collectivités, associations
""".format(datetime.now().strftime("%d/%m/%Y"), len(csirt_data)))

    # Add slides for each CSIRT
    for csirt in csirt_data:
        # Format phone number
        phone_type = {
            'toll_free': '(gratuit)',
            'fixed_rate': '(prix d\'un appel local)',
            'local_rate': '(prix d\'un appel local)'
        }.get(csirt['phone']['type'], '')
        
        # Format hours
        hours = csirt['availability']['raw']

        presentation.append(f"""
---
# {csirt['name']}

- 🏠 **Zone**: {csirt['Zone']}
- 📞 **Téléphone**: {csirt['phone']['number']} {phone_type}
- 🌐 **Site web**: {csirt['website']}
{f"- ✉️  **Email**: {csirt['email']}" if 'email' in csirt else ''}
- 🕐 **Disponibilité**: {hours}
""")

    # Write to file
    with open('csirt_presentation.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(presentation))

# Parse and process the JSON data
def main():
    try:
        with open('csirt_france.json', 'r', encoding='utf-8') as f:
            csirt_centers = json.load(f)
        generate_marp_presentation(csirt_centers['csirt_centers'])
        print("Présentation générée avec succès dans 'csirt_presentation.md'")
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")

if __name__ == "__main__":
    main()