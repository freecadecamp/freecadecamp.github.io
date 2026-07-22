import os

def fix_logos():
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # 1. Fix about.html logos
    about_path = 'about.html'
    if os.path.exists(about_path):
        with open(about_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Target 1: India's Clean Cooking Revolution top icon
        target1 = '<i class="fas fa-chart-line text-4xl mb-4"></i> <h2 class="text-3xl md:text-4xl font-bold">India\'s Clean Cooking Revolution</h2>'
        replacement1 = '<img src="/logo.png" alt="VSS Logo" class="w-16 h-16 object-contain rounded-xl mx-auto mb-4 bg-white p-2 shadow-md"> <h2 class="text-3xl md:text-4xl font-bold">India\'s Clean Cooking Revolution</h2>'

        # Target 2: Join the Movement top icon
        target2 = '<i class="fas fa-globe-asia text-5xl text-green-700 mb-4"></i> <h3 class="text-2xl font-bold text-gray-800">Join the Movement</h3>'
        replacement2 = '<img src="/logo.png" alt="VSS Logo" class="w-16 h-16 object-contain rounded-xl mx-auto mb-4 bg-white p-2 shadow-sm border border-green-100"> <h3 class="text-2xl font-bold text-gray-800">Join the Movement</h3>'

        if target1 in content:
            content = content.replace(target1, replacement1)
            print("Successfully replaced India's Clean Cooking Revolution icon in about.html")
        else:
            print("Warning: Target 1 not found in about.html")

        if target2 in content:
            content = content.replace(target2, replacement2)
            print("Successfully replaced Join the Movement icon in about.html")
        else:
            print("Warning: Target 2 not found in about.html")

        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 2. Fix products.html logos
    products_path = 'products.html'
    if os.path.exists(products_path):
        with open(products_path, 'r', encoding='utf-8') as f:
            content = f.read()

        target = '<i class="fas fa-leaf text-white text-5xl mb-4 opacity-80"></i>'
        replacement = '<img src="/logo.png" alt="VSS Logo" class="w-16 h-16 object-contain rounded-xl mx-auto mb-4 bg-white p-2 shadow-md">'

        if target in content:
            content = content.replace(target, replacement)
            print("Successfully replaced Switch to GE Series icon in products.html")
        else:
            print("Warning: Target not found in products.html")

        with open(products_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 3. Fix installation.html logos
    installation_path = 'installation.html'
    if os.path.exists(installation_path):
        with open(installation_path, 'r', encoding='utf-8') as f:
            content = f.read()

        target = '<i class="fas fa-lightbulb text-orange-500 text-4xl mb-4"></i>'
        replacement = '<img src="/logo.png" alt="VSS Logo" class="w-12 h-12 object-contain rounded-lg mb-4 bg-orange-50 p-1 border border-orange-100">'

        if target in content:
            content = content.replace(target, replacement)
            print("Successfully replaced Need Help Preparing icon in installation.html")
        else:
            print("Warning: Target not found in installation.html")

        with open(installation_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    fix_logos()
