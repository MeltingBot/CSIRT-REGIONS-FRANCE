from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfgen import canvas
import json
import os

def get_safe_value(data, key, default="N/A"):
    """Récupère une valeur en toute sécurité avec une valeur par défaut"""
    return data.get(key, default)

def create_csirt_card(csirt_data, output_path):
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Fond noir pour l'en-tête
    c.setFillColor(black)
    c.rect(0, height-50*mm, width, 50*mm, fill=1)
    
    # Nom du CSIRT en blanc
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    title = csirt_data['name'].upper()
    c.drawCentredString(width/2, height-25*mm, title)
    
    # Région en dessous
    c.setFont("Helvetica-Bold", 24)
    region = get_safe_value(csirt_data, 'region')
    c.drawCentredString(width/2, height-40*mm, region)
    
    # Rectangle blanc pour le numéro de téléphone
    c.setFillColor(white)
    phone_box_width = 400
    phone_box_height = 50
    phone_box_x = (width - phone_box_width) / 2
    phone_box_y = height - 80*mm
    c.rect(phone_box_x, phone_box_y, phone_box_width, phone_box_height, stroke=1, fill=1)
    
    # Numéro de téléphone
    phone_data = get_safe_value(csirt_data, 'phone', {})
    phone_number = get_safe_value(phone_data, 'number', "N/A")
    phone_type = get_safe_value(phone_data, 'type', "")
    
    phone_color = HexColor('#00ff7f') if phone_type == 'toll_free' else HexColor('#666666')
    c.setFillColor(phone_color)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, phone_box_y + 15, phone_number)
    
    # Zone si présente
    zone = get_safe_value(csirt_data, 'zone', "")
    if zone:
        c.setFillColor(black)
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, phone_box_y - 20, zone)
    
    # Définition des symboles simples
    symbols = {
        'clock': "⧖",     
        'web': "◉",       
        'email': "✉",    
        'doc': "◰"        
    }
    
    # Informations de contact
    start_y = height - 110*mm
    text_start_x = width/2-170  # Position x du début du texte
    symbol_x = width/2-200      # Position x des symboles
    link_height = 16            # Hauteur du texte pour les liens
    
    # Horaires
    c.setFillColor(black)
    availability = get_safe_value(csirt_data, 'availability', {})
    hours_text = get_safe_value(availability, 'raw', "N/A")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(symbol_x, start_y, symbols['clock'])
    c.setFont("Helvetica", 16)
    c.drawString(text_start_x, start_y, hours_text)
    
    # Site web avec lien
    start_y -= 30
    website = get_safe_value(csirt_data, 'website', "N/A")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(symbol_x, start_y, symbols['web'])
    c.setFont("Helvetica", 16)
    
    if website != "N/A":
        web_display = website.replace('https://', '').upper()
        c.setFillColor(HexColor('#0000FF'))  # Bleu pour les liens
        c.drawString(text_start_x, start_y, web_display)
        # Ajouter le lien cliquable
        rect = (text_start_x, start_y, text_start_x + c.stringWidth(web_display, "Helvetica", 16), start_y + link_height)
        c.linkURL(website, rect)
    else:
        c.setFillColor(black)
        c.drawString(text_start_x, start_y, website)
    
    # Email avec lien mailto
    start_y -= 30
    email = get_safe_value(csirt_data, 'email', "N/A")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(symbol_x, start_y, symbols['email'])
    c.setFont("Helvetica", 16)
    
    if email != "N/A":
        email_display = email.upper()
        c.setFillColor(HexColor('#0000FF'))  # Bleu pour les liens
        c.drawString(text_start_x, start_y, email_display)
        # Ajouter le lien mailto
        rect = (text_start_x, start_y, text_start_x + c.stringWidth(email_display, "Helvetica", 16), start_y + link_height)
        c.linkURL('mailto:' + email, rect)
    else:
        c.setFillColor(black)
        c.drawString(text_start_x, start_y, email)
    
    # RFC 2350 avec lien
    rfc_data = get_safe_value(csirt_data, 'rfc_2350', {})
    rfc_url = get_safe_value(rfc_data, 'document_url')
    if rfc_url:
        start_y -= 30
        c.setFont("Helvetica-Bold", 16)
        c.drawString(symbol_x, start_y, symbols['doc'])
        c.setFillColor(HexColor('#0000FF'))  # Bleu pour les liens
        c.setFont("Helvetica", 16)
        rfc_text = "RFC2350"
        c.drawString(text_start_x, start_y, rfc_text)
        # Ajouter le lien cliquable
        rect = (text_start_x, start_y, text_start_x + c.stringWidth(rfc_text, "Helvetica", 16), start_y + link_height)
        c.linkURL(rfc_url, rect)
    
    # TLP en bas de page
    tlp_level = get_safe_value(rfc_data, 'tlp_level', "N/A")
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#ff0000'))
    c.drawString(10, 10, f"TLP:{tlp_level}")
    
    c.save()

def generate_all_csirt_pdfs(json_data, output_dir="fiches_csirt"):
    os.makedirs(output_dir, exist_ok=True)
    successful = 0
    failed = 0
    
    for csirt in json_data['csirt_centers']:
        output_path = os.path.join(
            output_dir,
            f"fiche_{csirt['name'].lower().replace(' ', '_')}.pdf"
        )
        
        try:
            create_csirt_card(csirt, output_path)
            successful += 1
            print(f"✅ Fiche générée avec succès pour {csirt['name']}")
        except Exception as e:
            failed += 1
            print(f"❌ Échec de génération pour {csirt['name']}: {str(e)}")
    
    print(f"\nRésumé de la génération:")
    print(f"- Fiches générées avec succès: {successful}")
    print(f"- Échecs: {failed}")
    print(f"- Total: {successful + failed}")

if __name__ == "__main__":
    try:
        with open('csirt_france.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        generate_all_csirt_pdfs(data)
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {str(e)}")