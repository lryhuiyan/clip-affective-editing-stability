import csv

import matplotlib.pyplot as plt


emotion = "lonely"

csv_path = f"results/{emotion}_clip_scores.csv"
output_path = f"results/{emotion}_clip_improvements.png"

edit_names = []
improvements = []

with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        edit_name = row["edit_name"]
        improvement = float(row["improvement"])

        edit_names.append(edit_name)
        improvements.append(improvement)

plt.figure(figsize=(10, 5))

plt.bar(edit_names, improvements)

plt.axhline(y=0, linestyle="--", linewidth=1)

plt.xlabel("Edit Type")
plt.ylabel("CLIP Score Improvement")
plt.title(f"CLIP Score Improvements for '{emotion}'")

plt.xticks(rotation=30, ha="right")

plt.tight_layout()

plt.savefig(output_path, dpi=200)

print(f"Figure saved to: {output_path}")