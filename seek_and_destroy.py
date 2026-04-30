import os
import re
from bs4 import BeautifulSoup

def process_html_files():
    about_text = "VSS has been operating robustly since 2020, dedicated to carbon‑free, environment‑friendly, energy‑saving, and economically viable products. We manufacture high‑efficiency smokeless biomass stoves that empower households, hotels, and industries to cook clean, safe, and sustainably. As per NFHS-5 (2019-21): 41% of India still rely on biomass for cooking — emitting 340 million tonnes of CO₂ annually. Globally 2.4 billion people lack access to clean cooking solutions, causing significant damage to economy, public health and environment. Indoor air pollution from wood-based cooking causes about 3 million premature deaths annually worldwide, with 0.6 million in India (PTI report Jan 29, 2024)."

    html_files = [f for f in os.listdir('.') if f.endswith('.html')]

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # REMOVALS:
        # We need to forcefully remove the entire product cards for "ContinFeed" or empty "Stove" cards
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. Remove Product Cards that contain "ContinFeed", "Stove" (if empty prefix like <h3> Stove</h3>), or "Pellet"
        for card in soup.find_all('div', class_='product-card'):
            text = card.get_text().lower()
            if 'continfeed' in text or 'continuous' in text or 'pellet' in text:
                card.decompose()
                continue
            
            # Check for exactly " Stove" or "Stove" with missing prefix
            h3 = card.find('h3')
            if h3 and h3.get_text().strip() == 'Stove':
                card.decompose()
                continue
                
        # 2. Add the About text to all pages
        # If it's about.html, it's already in the main body. For index.html, we should replace the existing split About text.
        # For all other pages, we can inject a nice About section right above the Eco-Friendly box.
        
        # Find if we already injected the About section (to avoid duplicates)
        for section in soup.find_all('section', id='global-about-us'):
            section.decompose()

        about_html = f"""
        <section id="global-about-us" class="py-16 bg-white border-t border-gray-100">
            <div class="max-w-6xl mx-auto px-6 lg:px-8 text-center md:text-left">
                <div class="flex flex-col md:flex-row items-center gap-10">
                    <div class="md:w-1/3 flex justify-center">
                        <div class="w-32 h-32 bg-green-50 rounded-full flex items-center justify-center border-4 border-green-100 shadow-inner">
                            <i class="fas fa-leaf text-6xl text-green-600 drop-shadow-sm"></i>
                        </div>
                    </div>
                    <div class="md:w-2/3">
                        <span class="text-orange-500 font-bold tracking-wider uppercase text-sm mb-2 block">Our Mission</span>
                        <h2 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">About VSS</h2>
                        <div class="w-20 h-1 bg-gradient-to-r from-green-500 to-orange-500 rounded-full mb-6 mx-auto md:mx-0"></div>
                        <p class="text-gray-700 text-lg leading-relaxed text-justify md:text-left">
                            {about_text}
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
        
        if file == 'index.html':
            # Remove the existing ABOUT US sections in index.html to avoid duplication
            # There is a section with <!-- ABOUT US -->
            for h2 in soup.find_all('h2'):
                if 'ABOUT US' in h2.get_text().upper():
                    # decompose its parent section
                    parent_section = h2.find_parent('section')
                    if parent_section:
                        parent_section.decompose()
            # Also remove the info circle text
            for div in soup.find_all('div', class_='text-white/90 text-sm max-w-3xl border-t border-white/20 pt-6'):
                div.decompose()
                
        # Inject the new About Us section
        if file != 'about.html': # about.html already has this text seamlessly integrated in its layout
            eco_box = None
            for section in soup.find_all('section'):
                if 'Eco-Friendly & Sustainable Energy' in section.get_text() or 'Eco-Friendly Sustainable Energy' in section.get_text():
                    eco_box = section
                    break
            
            new_about = BeautifulSoup(about_html, 'html.parser')
            if eco_box:
                eco_box.insert_before(new_about)
            else:
                footer = soup.find('footer')
                if footer:
                    footer.insert_before(new_about)
                else:
                    if soup.body:
                        soup.body.append(new_about)

        # Write back
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    # Run a final regex cleanup for lingering words
    removals = [
        r'ContinFeed Industrial',
        r'ContinFeed',
        r'12\+ hours uninterrupted cooking\.',
        r'⏱️ Auto-feed hopper'
    ]
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for p in removals:
            content = re.sub(p, '', content, flags=re.IGNORECASE)
            
        # Clean up empty h3 tags that might have been left behind
        content = re.sub(r'<h3>\s*</h3>', '', content)
        content = re.sub(r'<h3 class="[^"]*">\s*</h3>', '', content)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

    print("All removals verified. Global About Us section injected.")

if __name__ == '__main__':
    process_html_files()
