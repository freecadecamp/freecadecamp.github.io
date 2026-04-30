import os
import re

def clean_text():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    
    # Global removals
    removals = [
        r'pellets?',
        r'continuous feeding stoves?',
        r'continuous feeding',
        r'continuous operation',
        r'12\+ hours continuous',
        r'12\+ hours without reloading',
        r'biogasifier',
        r'premium pellet\s*stove',
        r'varam clean cooking services',
        r'solar',
        r'65\s*%\s*fuel savings?',
        r'60-70\s*%\s*vs\s*LPG',
        r'60\s*%\s*Avg\.\s*Fuel\s*Savings',
        r'60\s*%',
        r'12\+\s*hrs\s*continuous\s*feeding'
    ]
    
    footer_target = r'Manufacturing high-efficiency smokeless biomass[\s\n]*stoves and biogas systems since 2020\. Carbon‑free, environment‑friendly, energy‑saving economic[\s\n]*products for a cleaner India\.'
    footer_replacement = "Next gen clean cooking biomass smokeless stove and biogas, VSS delivers efficient ecofriendly stoves for homes, hotels and industries to cook with cleaner and safe fuels | 40% wood saving compared to traditional open stoves."

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for p in removals:
            content = re.sub(p, '', content, flags=re.IGNORECASE)
            
        # Update Footer
        content = re.sub(footer_target, footer_replacement, content, flags=re.IGNORECASE)
        
        # If it's about.html, replace the company story
        if file == 'about.html':
            # Target the paragraphs in the 'Founded to End Smoke & Energy Poverty' section
            story_pattern = r'Founded in 2012.*?through decentralized biomass utilization\.'
            new_story = "VSS has been operating robustly since 2020, dedicated to carbon‑free, environment‑friendly, energy‑saving, and economically viable products. We manufacture high‑efficiency smokeless biomass stoves that empower households, hotels, and industries to cook clean, safe, and sustainably. As per NFHS-5 (2019-21): 41% of India still rely on biomass for cooking — emitting 340 million tonnes of CO₂ annually. Globally 2.4 billion people lack access to clean cooking solutions, causing significant damage to economy, public health and environment. Indoor air pollution from wood-based cooking causes about 3 million premature deaths annually worldwide, with 0.6 million in India (PTI report Jan 29, 2024)."
            content = re.sub(story_pattern, new_story, content, flags=re.IGNORECASE | re.DOTALL)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Global text updates complete.")

if __name__ == '__main__':
    clean_text()
