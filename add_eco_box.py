import os
from bs4 import BeautifulSoup

def add_eco_box():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    
    eco_box_html = """
    <!-- ECO-FRIENDLY & SUSTAINABLE ENERGY BOX -->
    <section class="py-12 bg-gradient-to-br from-green-50 to-emerald-100 border-t border-green-200">
        <div class="max-w-5xl mx-auto px-6 text-center">
            <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-green-100 transform hover:scale-[1.01] transition-transform">
                <span class="inline-block px-4 py-1.5 bg-green-100 text-green-800 rounded-full text-sm font-bold tracking-wider mb-4 uppercase">Eco-Friendly & Sustainable Energy</span>
                <h2 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-6 tracking-tight">Smokeless Biomass Stove</h2>
                <div class="w-24 h-1 bg-gradient-to-r from-green-500 to-emerald-600 mx-auto rounded-full mb-6"></div>
                <p class="text-lg md:text-xl text-gray-700 leading-relaxed max-w-3xl mx-auto font-medium">
                    Next gen clean cooking biomass smokeless stove and biogas. VSS delivers efficient, ecofriendly stoves for homes, hotels, and industries to cook with cleaner and safe fuels.
                </p>
                <div class="mt-8 flex justify-center">
                    <div class="inline-flex items-center gap-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white px-6 py-3 rounded-2xl shadow-md font-bold text-lg">
                        <i class="fas fa-fire-alt text-2xl"></i>
                        <span>40% wood saving vs traditional open stove</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # First, remove any existing eco-box if it was added previously (to avoid duplicates during script re-runs)
        for section in soup.find_all('section', class_=lambda c: c and 'from-green-50 to-emerald-100' in c):
            section.decompose()
            
        new_box = BeautifulSoup(eco_box_html, 'html.parser')
        
        # Inject just before the footer
        footer = soup.find('footer')
        if footer:
            footer.insert_before(new_box)
        else:
            if soup.body:
                soup.body.append(new_box)
                
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("Eco-friendly box successfully injected into all auxiliary pages.")

if __name__ == '__main__':
    add_eco_box()
