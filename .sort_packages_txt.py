from collections import defaultdict
with open(".packages.txt") as pf:
    content = pf.read().strip()

lines = content.splitlines()
packages = defaultdict(list)

section_name = None
for line in lines:
    if len(line) == 0: continue
    if line.startswith("#"):
        section_name = line.split("#")[1].strip()
    else:
        packages[section_name].append(line)

for section_name in sorted(packages.keys()):
    print(f"# {section_name}")
    for package in sorted(packages[section_name]):
        print(package)
    print()