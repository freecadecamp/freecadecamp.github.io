import os
import re
from bs4 import BeautifulSoup

def process_html_files():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        print(f"Processing: {file}")
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # -------------------------------------------------------------
        # 1. CLEAN UP PRODUCT RANGE GRIDS (replaces gasifier types)
        # Keep only "Biomass Smokeless Stove" and "Biogas" (decomposing cards 2 and 4)
        # -------------------------------------------------------------
        for grid in soup.find_all('div', class_='grid md:grid-cols-2 lg:grid-cols-4 gap-6'):
            cards = grid.find_all('div', recursive=False)
            if len(cards) == 4:
                card_texts = [c.get_text().lower() for c in cards]
                if 'biomass smokeless' in card_texts[0] and 'biogas' in card_texts[2]:
                    print(f"  -> Cleaning product range grid in {file}")
                    # Decompose Card 2 (Stove) and Card 4 (Automated/Continuous)
                    cards[1].decompose()
                    cards[3].decompose()
                    # Center the remaining 2 cards beautifully
                    grid['class'] = [c for c in grid['class'] if c != 'lg:grid-cols-4']
                    grid['class'].extend(['lg:grid-cols-2', 'max-w-3xl', 'mx-auto'])

        # -------------------------------------------------------------
        # 2. ABOUT.HTML STORY AND COMMITMENT UPDATES
        # -------------------------------------------------------------
        if file == 'about.html':
            # Remove "annual maintenance" from Commitment text
            for p in soup.find_all('p', class_='text-gray-600'):
                if 'accessible to every Indian kitchen' in p.get_text():
                    print("  -> Updating commitment text in about.html")
                    p.string = "We are dedicated to making clean cooking accessible to every Indian kitchen. Our stoves and biogas are designed for durability, ease of use, and maximum fuel efficiency. We provide end-to-end support — from needs assessment to installation and training."

        # -------------------------------------------------------------
        # 3. SERVICES.HTML DETAILED CLEANUPS
        # -------------------------------------------------------------
        if file == 'services.html':
            # A. Specialized Services grid (grid md:grid-cols-3 gap-8)
            # Remove "Stoves" (Card 2) and clean up Card 3 (Biogas)
            for grid in soup.find_all('div', class_='grid md:grid-cols-3 gap-8'):
                cards = grid.find_all('div', recursive=False)
                if len(cards) == 3:
                    card_texts = [c.find('h3').get_text().strip().lower() if c.find('h3') else '' for c in cards]
                    if 'biomass smokeless' in card_texts[0] and 'stoves' in card_texts[1] and 'biogas' in card_texts[2]:
                        print("  -> Cleaning specialized services in services.html")
                        cards[1].decompose()
                        # Center remaining 2 cards
                        grid['class'] = [c for c in grid['class'] if c not in ['grid', 'md:grid-cols-3']]
                        grid['class'].extend(['grid', 'md:grid-cols-2', 'max-w-4xl', 'mx-auto'])
                        
                        # Clean up Biogas heading
                        h3_biogas = cards[2].find('h3')
                        if h3_biogas:
                            h3_biogas.string = "Biogas"
                        # Clean up multi-fuel compatibility list item (remove leading comma)
                        for li in cards[2].find_all('li'):
                            if '(,' in li.get_text():
                                li.string = "Multi-fuel compatibility (nutshells, agri-waste)"

            # B. Deployment & Advisory Services (grid md:grid-cols-2 gap-8)
            # Remove "User Training" and "Logistics & Lifetime Support" cards
            for grid in soup.find_all('div', class_='grid md:grid-cols-2 gap-8'):
                cards = grid.find_all('div', recursive=False)
                if len(cards) == 4:
                    card_texts = [c.find('h3').get_text().strip().lower() if c.find('h3') else '' for c in cards]
                    if 'needs assessment' in card_texts[0] and 'user training' in card_texts[1] and 'savings' in card_texts[2] and 'logistics' in card_texts[3]:
                        print("  -> Cleaning deployment & advisory services in services.html")
                        cards[1].decompose()
                        cards[3].decompose()
                        
                        # Update Needs Assessment card text to remove truncated text
                        for p in cards[0].find_all('p'):
                            if 'ideal solution' in p.get_text().lower():
                                p.string = "Understanding your cooking volume, fuel access, budget, and smoke elimination goals to recommend the ideal solution: Biomass Smokeless Stove or Biogas."

        # -------------------------------------------------------------
        # 4. INSTALLATION.HTML STEP & CHECKLIST UPDATES
        # -------------------------------------------------------------
        if file == 'installation.html':
            # A. Step 1: Change Free kitchen energy audit to Telephonic guidance
            for step in soup.find_all('div', class_='step-card'):
                h3 = step.find('h3')
                if h3 and 'kitchen assessment' in h3.get_text().lower():
                    print("  -> Updating Step 1 in installation.html")
                    for d in step.find_all('div', class_='text-green-600'):
                        if 'audit' in d.get_text().lower():
                            d.string = ""
                            icon = soup.new_tag('i', attrs={"class": "fas fa-phone mr-1"})
                            d.append(icon)
                            d.append(" Telephonic fuel efficiency guidance will be given")

            # B. Pre-installation Checklist items (exhaust, chimney, auto-feed, hopper)
            print("  -> Updating pre-installation checklist in installation.html")
            for li in soup.find_all('li'):
                text = li.get_text().lower()
                if 'stove/hopper/digester' in text:
                    li.string = ""
                    icon = soup.new_tag('i', attrs={"class": "fas fa-check-circle text-green-600 mr-2"})
                    li.append(icon)
                    span = soup.new_tag('span', attrs={"class": "text-gray-700"})
                    span.string = "Adequate space for biogas digester placement"
                    li.append(span)
                elif 'exhaust/' in text or 'exhaust/ chimney' in text:
                    li.decompose()
                elif 'electrical outlet' in text:
                    li.decompose()
                elif 'for biogas: organic' in text:
                    li.string = ""
                    icon = soup.new_tag('i', attrs={"class": "fas fa-check-circle text-green-600 mr-2"})
                    li.append(icon)
                    span = soup.new_tag('span', attrs={"class": "text-gray-700"})
                    span.string = "Organic waste supply & water source"
                    li.append(span)

            # C. Installation by Product Type (remove Stove, keep only Biogas)
            for grid in soup.find_all('div', class_='grid md:grid-cols-2 lg:grid-cols-4 gap-6'):
                cards = grid.find_all('div', recursive=False)
                if len(cards) >= 3:
                    card_texts = [c.find('h3').get_text().strip().lower() if c.find('h3') else '' for c in cards]
                    if 'stove' in card_texts[0] and 'biogas' in card_texts[1] and 'electrical connection' in card_texts[2]:
                        print("  -> Cleaning installation by product grid in installation.html")
                        cards[0].decompose()
                        cards[2].decompose()
                        
                        biogas_card = cards[1]
                        h3 = biogas_card.find('h3')
                        if h3:
                            h3.string = "Biogas Plant"
                        p = biogas_card.find('p')
                        if p:
                            p.string = "Digester installation, inlet/outlet piping, gas storage, and Pressure Pump setup. Site excavation may be required. Installation completed in 4–5 Hours."
                        
                        # Center the card
                        grid['class'] = [c for c in grid['class'] if c not in ['grid', 'md:grid-cols-2', 'lg:grid-cols-4']]
                        grid['class'].extend(['flex', 'justify-center', 'max-w-md', 'mx-auto'])

        # -------------------------------------------------------------
        # 5. CONTACT.HTML BENEFITS & CTA UPDATES
        # -------------------------------------------------------------
        if file == 'contact.html':
            # Replace Free kitchen energy audit with Telephonic Guidance
            for li in soup.find_all('li'):
                text = li.get_text().lower()
                if 'energy audit' in text:
                    print("  -> Updating audit checklist item in contact.html")
                    li.string = ""
                    icon = soup.new_tag('i', attrs={"class": "fas fa-check-circle text-green-600"})
                    li.append(icon)
                    li.append(" Telephonic Fuel Efficiency Guidance Will Be Given")

        # -------------------------------------------------------------
        # 6. GLOBAL FOOTER TEXT AND CLEANUPS
        # -------------------------------------------------------------
        for p in soup.find_all('p', class_='text-sm text-gray-400 leading-relaxed'):
            text = p.get_text()
            if '40% wood saving' in text or 'compared to traditional' in text:
                print(f"  -> Cleaning global footer in {file}")
                p.string = "Next gen clean cooking biomass smokeless stove and biogas, VSS delivers efficient ecofriendly stoves for homes, hotels and industries to cook with cleaner and safe fuels | More Than 80% Fuel Saving vs Traditional Stove."

        # Write back HTML
        new_content = str(soup)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # -----------------------------------------------------------------
    # GLOBAL REGEX REPLACEMENTS (TEXT AND ATTRIBUTES CLEANUPS)
    # -----------------------------------------------------------------
    print("\nRunning global regex replacements...")
    
    replacements = [
        # Fuel cost savings and wood savings updates
        (r'40% wood saving\b', 'More Than 80% Fuel Saving vs Traditional Stove'),
        (r'40% wood savings\b', 'More Than 80% Fuel Saving vs Traditional Stove'),
        (r'40% firewood reduction\b', 'More Than 80% Fuel Saving vs Traditional Stove'),
        (r'40% less firewood\b', 'More Than 80% Fuel Saving vs Traditional Stove'),
        (r'70% average fuel cost reduction\b', 'More Than 80% Fuel Cost Reduction'),
        (r'70% average fuel reduction\b', 'More Than 80% Fuel Cost Reduction'),
        (r'70% fuel savings\b', 'More Than 80% Fuel Cost Reduction'),
        (r'save up to 70% on fuel\b', 'achieve More Than 80% Fuel Cost Reduction'),
        (r'70% LPG offset\b', 'More Than 80% LPG offset'),
        (r'15\+ states\b', 'Pan India Delivery Options Available'),
        (r'15\+ States\b', 'Pan India Delivery Options Available'),
        
        # Access capitalization
        (r'lack access to Smokeless stove\b', 'lack access to Smokeless Stove'),
        
        # Free demo / warranty / AMC removals
        (r' · 1 year warranty\b', ''),
        (r' · 1 Year Warranty\b', ''),
        (r'1 Year Warranty \+ Extended Warranty Option\b', ''),
        (r'1 Year Warranty\b', ''),
        (r'Lifetime Support, 1 Year Warranty, Free Demo Available\b', ''),
        (r'Request a Free Demo\b', ''),
        (r'Free Demo Available\b', ''),
        (r'Visit our office or schedule a product demo\b', 'Visit our office or get in touch'),
        (r'Showroom & Demo Kitchen available\b', 'Showroom available'),
        (r'annual maintenance contracts\b', 'lifetime support'),
        (r'annual maintenance contract\b', 'lifetime support'),
        
        # Clean up empty tags and leading commas left behind
        (r'<li><i class="fas fa-check-circle text-green-500 mr-2"></i>\s*</li>', ''),
        (r'<h3>\s*Stove\s*</h3>', ''),
        (r'<h3 class="[^"]*">\s*Stove\s*</h3>', ''),
    ]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Fix specific double references or spacing
        content = re.sub(r'vs traditional woodstove vs traditional woodstove', 'vs traditional woodstove', content, flags=re.IGNORECASE)
        content = re.sub(r'Traditional Stove vs traditional woodstove', 'Traditional Stove', content, flags=re.IGNORECASE)
        content = re.sub(r'Traditional Stove compared to traditional woodstoves', 'Traditional Stove', content, flags=re.IGNORECASE)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

    print("All revisions and regex cleanup completed successfully!")

if __name__ == '__main__':
    process_html_files()
