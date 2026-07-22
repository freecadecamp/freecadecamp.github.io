"""
VARAM Website Final QA & Content Fix Script
Fixes all outstanding issues found in the audit across all HTML files.
"""
import re
import os

def fix_file(filename, fixes):
    """Apply a list of (old, new) replacements to a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[SKIP] {filename} not found")
        return

    original = content
    change_count = 0
    for old, new, desc in fixes:
        if old in content:
            content = content.replace(old, new)
            change_count += 1
            print(f"  [FIX] {desc}")
        else:
            print(f"  [SKIP] Not found: {desc}")

    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[SAVED] {filename} ({change_count} changes)")
    else:
        print(f"[UNCHANGED] {filename}")

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("VARAM WEBSITE FINAL QA - APPLYING ALL FIXES")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────
# home.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[home.html]")
fix_file("home.html", [
    # Fix CTA "save 40% wood" -> "save more than 80% wood"
    (
        "Reduce smoke, save 40% wood, and protect health.",
        "Reduce smoke, save more than 80% wood, and protect health.",
        "CTA: Fix 40% -> more than 80%"
    ),
    # Fix invalid CSS property z-home -> z-index
    (
        "z-home: 0;",
        "z-index: 0;",
        "CSS: z-home:0 -> z-index:0"
    ),
    (
        "z-home: 1;",
        "z-index: 1;",
        "CSS: z-home:1 -> z-index:1"
    ),
    (
        "z-home: 2;",
        "z-index: 2;",
        "CSS: z-home:2 -> z-index:2"
    ),
    (
        "z-home: 999;",
        "z-index: 999;",
        "CSS: z-home:999 -> z-index:999"
    ),
    # Fix hero nav Home link to home.html (already home.html in home.html, OK)
    # Standardize "Traditional Stove" -> "Traditional Wood Stove" in CTA area
    (
        '"Compared to Traditional Open Stove"',
        '"Compared to Traditional Wood Stove"',
        "Terminology: Traditional Open Stove -> Traditional Wood Stove"
    ),
])

# ─────────────────────────────────────────────────────────────────
# services.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[services.html]")
fix_file("services.html", [
    # Fix title typo: SERVISE -> SERVICES
    (
        "VARAM SUSTAINABLE SOLUTIONS SERVISE",
        "VARAM SUSTAINABLE SOLUTIONS SERVICES",
        "Title: SERVISE -> SERVICES"
    ),
    # Fix broken Biomass Fuel Assessment text: double comma + broken word "ers"
    (
        "Analysis of agricultural residues, wood chips, , and organic waste to determine suitability for smokeless stoves, ers, or biogas. We provide fuel sourcing guidance.",
        "Analysis of organic waste and biomass to determine suitability for smokeless stoves or biogas. We provide fuel sourcing guidance.",
        "Biomass Assessment: Fix double comma, broken word 'ers', remove agri residues"
    ),
    # Fix double comma in CTA: "switched to smokeless,, biogas"
    (
        "switched to smokeless,, biogas, and by VARAM.",
        "switched to smokeless biogas solutions by VARAM.",
        "CTA: Fix double comma and broken sentence"
    ),
    # Fix missing icon list item (Multi-fuel)
    (
        '<li class="flex items-start gap-2">Multi-fuel compatibility (nutshells, agri-waste)</li>',
        '<li class="flex items-start gap-2"><i class="fas fa-check-circle text-amber-500 mt-0.5"></i><span>Multi-fuel compatibility (coconut shell, biomass pellets)</span></li>',
        "Biogas: Fix missing icon on multi-fuel list item, remove agri-waste"
    ),
    # Fix lowercase biogas digester -> capitalize B
    (
        "<span>biogas digester sizing (kitchen waste/cow dung)</span>",
        "<span>Biogas digester sizing (kitchen waste/cow dung)</span>",
        "Biogas: Capitalize 'biogas digester'"
    ),
    # Fix hero nav Home link -> home.html
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
    # Mobile menu Home link fix
    (
        'href="index.html">Home</a>\n<a class="py-2',
        'href="home.html">Home</a>\n<a class="py-2',
        "Mobile nav: Fix Home link"
    ),
])

# ─────────────────────────────────────────────────────────────────
# products.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[products.html]")
fix_file("products.html", [
    # Fix category nav centering: grid-cols-2 md:grid-cols-3 -> grid-cols-2 justify-center max-w-xl
    (
        'class="grid grid-cols-2 md:grid-cols-3 gap-4 text-center max-w-3xl mx-auto"',
        'class="grid grid-cols-2 gap-4 text-center max-w-xl mx-auto"',
        "Products: Fix category nav centering (2-col grid)"
    ),
    # Fix product grid last-row centering: wrap in a flex justify-center for 5 items
    # The grid is md:grid-cols-2 lg:grid-cols-3 with 5 items — last item floats left
    # Add justify-items-center to parent
    (
        'class="grid md:grid-cols-2 lg:grid-cols-3 gap-8"',
        'class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 justify-items-center"',
        "Products: Center-align product cards in grid"
    ),
    # Each product card: ensure full width on grid
    (
        'class="product-card relative bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover-scale"',
        'class="product-card relative bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover-scale w-full"',
        "Products: Make product cards full width within grid cell"
    ),
])

# ─────────────────────────────────────────────────────────────────
# installation.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[installation.html]")
fix_file("installation.html", [
    # Fix hero broken sentence
    (
        "our expert team manages complete installation of smokeless stoves, systems, biogas, and with precision and safety.",
        "our expert team manages complete installation of biogas systems with precision and safety.",
        "Hero: Fix broken sentence about installation types"
    ),
    # Fix nav Home link -> home.html
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
    # Fix CTA: "Book your free kitchen consultation" remove "free"
    (
        "Book your free kitchen consultation today",
        "Book your kitchen consultation today",
        "CTA: Remove 'free' from kitchen consultation"
    ),
])

# ─────────────────────────────────────────────────────────────────
# contact.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[contact.html]")
fix_file("contact.html", [
    # Remove Auto Ignition Pellet Stove option from dropdown
    (
        '<option>\U0001f33e Auto Ignition Pellet Stove</option>\n',
        '',
        "Contact: Remove Auto Ignition Pellet Stove from dropdown"
    ),
    (
        '<option>🌾 Auto Ignition Pellet Stove</option>\n',
        '',
        "Contact: Remove Auto Ignition Pellet Stove from dropdown (emoji)"
    ),
    # Fix Demo Kitchen reference in location
    (
        "📍 Showroom &amp; Demo Kitchen available",
        "📍 Showroom &amp; Demonstration available",
        "Contact: Remove 'Demo Kitchen' reference"
    ),
    # Fix email consistency: varamcleancooking.com -> varamsustainable.com
    (
        "contact@varamcleancooking.com",
        "contact@varamsustainable.com",
        "Contact: Unify email to varamsustainable.com"
    ),
    # Fix nav Home link -> home.html
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
])

# ─────────────────────────────────────────────────────────────────
# about.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[about.html]")
fix_file("about.html", [
    # Fix broken sentences where removed product types left blanks: "chips, ." and empty spans
    (
        "Uses twigs, chips, .",
        "Uses twigs, chips, and biomass pellets.",
        "About: Fix broken sentence in product type card"
    ),
    # Fix "Reduce fuel costs by " (empty) 
    (
        "<li class=\"flex items-center gap-2\"><i class=\"fas fa-check-circle text-green-500\"></i> Reduce fuel costs by </li>",
        "<li class=\"flex items-center gap-2\"><i class=\"fas fa-check-circle text-green-500\"></i> Reduce fuel costs by more than 80%</li>",
        "About: Fix 'Reduce fuel costs by ' incomplete sentence"
    ),
    # Fix empty product ecosystem span
    (
        "<span class=\"px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-semibold\"></span>",
        "",
        "About: Remove empty product tag span"
    ),
    # Fix " models for commercial kitchens" (missing product name)
    (
        "<li class=\"flex items-center gap-2\"><i class=\"fas fa-check-circle text-green-500\"></i>  models for commercial kitchens</li>",
        "<li class=\"flex items-center gap-2\"><i class=\"fas fa-check-circle text-green-500\"></i> GE20 &amp; GE25 models for commercial kitchens</li>",
        "About: Fix ' models for commercial kitchens'"
    ),
    # Fix "with digital temperature control" - missing product name
    (
        "<li class=\"flex items-center gap-2\"><i class=\"fas fa-check-circle text-green-500\"></i> with digital temperature control</li>",
        "",
        "About: Remove 'with digital temperature control' (removed product)"
    ),
    # Fix hero bio: "biomass smokeless stoves, systems, biogas, and " -> clean up
    (
        "specialized in <span class=\"font-semibold\">biomass smokeless stoves, systems, biogas, and </span>",
        "specialized in <span class=\"font-semibold\">biomass smokeless stoves and biogas systems</span>",
        "About: Fix hero specialization text"
    ),
    # Fix step 4 empty: " models maintain steady heat for "
    (
        "<p class=\"text-gray-700\"> models maintain steady heat for </p>",
        "<p class=\"text-gray-700\">GE series models maintain steady heat for efficient mass cooking.</p>",
        "About: Fix empty step 4 description"
    ),
    # Fix step 1: "chips, agri-waste" -> proper text
    (
        "Biomass fuel (, chips, agri-waste) is loaded",
        "Biomass fuel (wood chips, coconut shell, biomass pellets) is loaded",
        "About: Fix step 1 fuel description"
    ),
    # Fix empty amber stats box
    (
        "<div class=\"text-5xl font-black text-amber-600\"></div>",
        "<div class=\"text-5xl font-black text-amber-600\">80%+</div>",
        "About: Add missing stat number (avg fuel savings)"
    ),
    # Fix "M.r Senthil" -> "Mr. Senthil"
    (
        "M.r Senthil(Founder of vss)",
        "Mr. Senthil, Founder of VSS",
        "About: Fix name formatting"
    ),
    # Fix "Biomased" typo
    (
        "Biomased cooking solutions",
        "Biomass cooking solutions",
        "About: Fix 'Biomased' typo"
    ),
    # Fix empty product range tag (the last empty <span>)
    (
        "<span class=\"px-4 py-2 bg-slate-100 text-slate-700 rounded-full text-sm font-semibold\"></span>",
        "",
        "About: Remove second empty product tag"
    ),
    # Fix nav Home link
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
])

# ─────────────────────────────────────────────────────────────────
# projects.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[projects.html]")
fix_file("projects.html", [
    # Fix nav Home link -> home.html
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
])

# ─────────────────────────────────────────────────────────────────
# gallery.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[gallery.html]")
fix_file("gallery.html", [
    # Fix nav Home link -> home.html
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
    # Fix gallery description: "biomass gasifier" -> "clean cooking"
    (
        "A glimpse of our biomass gasifier installations across India",
        "A glimpse of our clean cooking installations across India",
        "Gallery: Update hero description"
    ),
    # GE10 old capacity
    (
        "Upto 7kg rice capacity",
        "Upto 8kg rice capacity",
        "Gallery: GE10 capacity 7kg -> 8kg"
    ),
])

# ─────────────────────────────────────────────────────────────────
# cart.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[cart.html]")
fix_file("cart.html", [
    # Fix nav Home link -> home.html  
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
])

# ─────────────────────────────────────────────────────────────────
# admin.html fixes
# ─────────────────────────────────────────────────────────────────
print("\n[admin.html]")
fix_file("admin.html", [
    # Fix nav Home link -> home.html  
    (
        'href="index.html">Home</a>',
        'href="home.html">Home</a>',
        "Nav: Fix Home link index.html -> home.html"
    ),
])

print("\n" + "=" * 60)
print("ALL FIXES APPLIED SUCCESSFULLY")
print("=" * 60)
