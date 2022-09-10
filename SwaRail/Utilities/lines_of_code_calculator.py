import os

total_lines = 0
considered_files = []

for path, folders, files in os.walk("../../SwaRail"):
    if path.endswith("__"):
        continue

    for file in files:
        if not file.endswith(".py"):
            continue

        complete_path = path + "\\" + file
        
        with open(complete_path, 'r') as f:
            total_lines += len(f.read().split('\n'))

        considered_files.append(complete_path)



print("Considered Files =", considered_files)
print("\n\nTotal Lines =", total_lines)