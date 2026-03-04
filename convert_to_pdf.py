#!/usr/bin/env python3
"""Script pour convertir RAPPORT_PROJET.txt en PDF"""

from fpdf import FPDF
import sys

class PDF(FPDF):
    def header(self):
        pass
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Courier', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Créer le PDF
pdf = PDF(format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(left=10, top=10, right=10)

# Utiliser Courier qui est toujours disponible
font_name = 'Courier'
has_unicode = False

# Lire le fichier texte
try:
    with open('RAPPORT_PROJET.txt', 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Ajouter les pages
pdf.add_page()
pdf.set_font(font_name, '', 8)

# Nettoyer le contenu en ne gardant que les caractères ASCII imprimables et espaces
cleaned_lines = []
for line in content.split('\n'):
    cleaned_line = ''
    for char in line:
        # Garder ASCII imprimable (32-126), tab (9), et newline (10)
        if 32 <= ord(char) <= 126 or char in '\t':
            cleaned_line += char
        else:
            # Remplacer les caractères non-ASCII par des équivalents
            replacements = {
                # Box drawing
                '╔': '+', '╗': '+', '╚': '+', '╝': '+', '═': '=', '║': '|',
                '│': '|', '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
                '─': '-', '└': '+', '┘': '+', '┌': '+', '┐': '+',
                # Bullets and symbols
                '•': '*', '●': '*', '○': 'o', '◦': '-',
                '✓': 'v', '✔': 'v', '✗': 'x', '✘': 'x',
                '✅': '[OK]', '❌': '[X]', '⚠': '[!]', '⚠️': '[!]',
                # Arrows
                '→': '->', '←': '<-', '↑': '^', '↓': 'v', '↔': '<->',
                '⇒': '=>', '⇐': '<=', '⇔': '<=>',
                # Emojis (colored circles)
                '🔵': '[1]', '🟢': '[2]', '🟣': '[3]', '🔴': '[!]',
                # Other emojis
                '🎯': '[*]', '📋': '[i]', '👥': '[Eq]', '🏗️': '[Ar]',
                '💻': '[PC]', '📊': '[St]', '🚀': '[>>]', '🔮': '[?]',
                '🎓': '[Ed]', '📚': '[Doc]', '🎨': '[#]', '📄': '[F]',
                '📁': '[D]', '🪟': '[W]', '🐧': '[L]', '💾': '[DB]',
                '🌐': '[Net]', '🔧': '[!]', '🔒': '[Sec]', '▼': 'v',
                # Quotes
                ''': "'", ''': "'", '"': '"', '"': '"', '„': '"',
                '‚': "'", '‹': '<', '›': '>', '«': '<<', '»': '>>',
                # Dashes and spaces
                '–': '-', '—': '--', '…': '...', ' ': ' ',
                # Accented characters
                'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
                'à': 'a', 'â': 'a', 'ä': 'a', 'å': 'a',
                'ù': 'u', 'û': 'u', 'ü': 'u',
                'ô': 'o', 'ö': 'o', 'œ': 'oe',
                'î': 'i', 'ï': 'i', 'ç': 'c',
                'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
                'À': 'A', 'Â': 'A', 'Ä': 'A', 'Å': 'A',
                'Ù': 'U', 'Û': 'U', 'Ü': 'U',
                'Ô': 'O', 'Ö': 'O', 'Œ': 'OE',
                'Î': 'I', 'Ï': 'I', 'Ç': 'C',
            }
            cleaned_line += replacements.get(char, '?')
    cleaned_lines.append(cleaned_line)

content = '\n'.join(cleaned_lines)

# Ajouter le contenu ligne par ligne
lines = content.split('\n')
max_width = 105  # Largeur maximale en caractères

for line in lines:
    # Tronquer les lignes trop longues
    if len(line) > max_width:
        # Découper en morceaux de max_width caractères
        while len(line) > max_width:
            pdf.cell(0, 4, line[:max_width], ln=True)
            line = line[max_width:]
        if line:
            pdf.cell(0, 4, line, ln=True)
    else:
        pdf.cell(0, 4, line, ln=True)

# Sauvegarder le PDF
try:
    pdf.output('RAPPORT_PROJET.pdf')
    print("✓ PDF créé avec succès: RAPPORT_PROJET.pdf")
except Exception as e:
    print(f"Erreur lors de la création du PDF: {e}")
    sys.exit(1)
