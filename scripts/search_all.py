import os
import re
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# List of regex/strings to search for, grouped by section
search_groups = {
    "S1_Commitment": [r"Lifetime Support", r"1 Year Warranty", r"Free Demo Available", r"Request a Free Demo", r"Free Demo"],
    "S2_Services": [r"System Engineering", r"Installation & Commissioning", r"O&M User Training", r"User Training"],
    "S3_Specialized": [r"Fixed Installations", r"Automated Ignition", r"Feed Calibration", r"Efficiency Optimization up to 95%", r"95%"],
    "S4_NeedsAssessment": [r"Free Kitchen Audit", r"Comparative Fuel Cost Analysis", r"Payback Period within 2 Months", r"Customized Solution Blueprint"],
    "S5_Logistics": [r"Reliable Delivery Installation", r"Annual Maintenance Contract", r"Genuine Spare Parts", r"Pan India Delivery & Installation", r"Pan India Dispatch"],
    "S6_SpareParts": [r"Genuine Spare Parts for all Models", r"Smokeless", r"Continuous", r"Biogas"],
    "S7_AMC": [r"Comprehensive AMC with Quarterly Servicing", r"AMC"],
    "S8_Warranty": [r"1 Year Warranty \+ Extended Warranty Option"],
    "S9_AfterSales": [r"After Sales & Lifetime Care", r"After Sales", r"Lifetime Care"],
    "S10_AboutVSS": [r"People lack access to Varam Sustainable Solutions", r"People lack access to Smokeless Stove", r"People lack access"],
    "S11_Products": [
        r"40% Fuel Saving", r"40% Fuel Savings", r"More than 80% Fuel Saving",
        r"7 kg", r"8 kg", r"98% Smoke Elimination", r"Heavy Duty Grate", r"Ash Management",
        r"Payback within 12 Months", r"15\+ Years Lifespan", r"Rugged Stainless Steel Build",
        r"Eliminate up to 98% smoke and achieve 40% wood saving compared to traditional open stove",
        r"GE 5", r"GE 10", r"GE 15", r"GE 20", r"GE 25"
    ],
    "S12_FuelCost": [r"70% Average Fuel Cost Reduction", r"70% Fuel Savings", r"70%"],
    "S13_Delivery": [r"15\+ States", r"15\+ states"],
    "S14_InstallationPage": [
        r"Installation & Integration", r"How We Install Your Clean Cooking System",
        r"Hopper Installation", r"Exhaust Fitting", r"Electrical Connection",
        r"Performance Testing", r"Smoke Emission Check", r"Operator Training", r"Complete Documentation"
    ],
    "S15_WhatsIncluded": [r"Free Delivery", r"24/7 Technical Support"],
    "S16_PreInstallation": [r"Wood Chips", r"Agri Waste"],
    "S17_StoveDuration": [r"Installation in 2–3 Hours", r"2-3 Hours", r"Control Panel Setup", r"4–5 Hours", r"Current Duration"],
    "S18_Projects": [r"Real World Installations of Smokeless Stove", r"Clean Cooking Products Deployed"],
    "S19_CommunityProjects": [r"Isha Foundation", r"Akshaya Patra"],
    "S20_Environmental": [r"Environmental Impact"],
    "S21_Testimonials": [r"Testimonial", r"Awaiting actual institutional"],
    "S22_Contact": [r"80% Reduction in Fuel Cost versus LPG"],
    "S23_BiogasSupport": [r"Installation Training for Biogas Plant", r"Lifetime Support for Biogas Plant"],
    "S24_FAQ": [
        r"Best Stove for Home Cooking", r"What is Continuous Feed Stock\?", r"Are Automatic Stoves Available\?",
        r"How Does a Biogas Plant Work\?", r"What is the Payback Period\?", r"Do You Provide Installation and Support\?"
    ],
    "S25_LeadGen": [r"Want a Free Kitchen Energy Audit\?", r"Energy Audit"]
}

results = {}

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        line_num = idx + 1
        for group, queries in search_groups.items():
            for query in queries:
                if re.search(query, line, re.IGNORECASE):
                    if group not in results:
                        results[group] = []
                    results[group].append({
                        "file": filename,
                        "line": line_num,
                        "query": query,
                        "content": line.strip()
                    })

# Print report sorted by group
for group in sorted(results.keys()):
    print(f"=== {group} ===")
    seen = set()
    for item in results[group]:
        key = (item["file"], item["line"], item["query"])
        if key not in seen:
            seen.add(key)
            print(f"  {item['file']}:{item['line']} ({item['query']}) -> {item['content'][:120]}")
    print()
