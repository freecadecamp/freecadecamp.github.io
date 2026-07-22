"""
Fix logo paths across all HTML files.
Changes src="logo.png" to src="/logo.png" (root-relative)
so it always resolves correctly regardless of page location.
Also fixes logo.jpg references.
"""
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace relative logo.png with root-relative /logo.png
    # Only match src="logo.png" or src='logo.png' (not already absolute or root-relative)
    content = re.sub(r'src=["\']logo\.png["\']', 'src="/logo.png"', content)
    content = re.sub(r'src=["\']logo\.jpg["\']', 'src="/logo.jpg"', content)

    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count replacements
        count = original.count('src="logo.png"') + original.count("src='logo.png'") + \
                original.count('src="logo.jpg"') + original.count("src='logo.jpg'")
        print(f"[FIXED] Fixed {count} logo reference(s) in {filename}")
    else:
        print(f"[OK] No changes needed in {filename}")

print("\nDone! All logo paths updated to root-relative /logo.png")
