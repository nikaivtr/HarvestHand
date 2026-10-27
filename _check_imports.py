import ast, importlib

# Parse main_menu.py to find popup imports
tree = ast.parse(open(r'scenes\main_menu.py', encoding='utf-8').read())

# Find import statements
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom):
        if node.module and 'popups' in node.module:
            print(f"Import from: {node.module}")
            for alias in node.names:
                print(f"  - {alias.name}")

# Also check for direct usage of scan_popup
print("\nChecking for scan_popup references in main_menu...")
s = open(r'scenes\main_menu.py', encoding='utf-8').read()
if 'scan_popup' in s:
    print("  scan_popup IS referenced in main_menu")
else:
    print("  scan_popup is NOT referenced in main_menu")

# Check what popups are actually imported
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom) and node.module and 'popups' in node.module:
        for alias in node.names:
            print(f"  Imported name: {alias.name}")