import csv

import matplotlib.pyplot as plt


summary_csv_path = "results/all_emotions_summary.csv"
output_path = "results/all_emotions_best_improvements.png"

emotions = []
best_edits = []
best_improvements = []

with open(summary_csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        emotion = row["emotion"]
        best_edit = row["best_edit"]
        best_improvement = float(row["best_improvement"])

        emotions.append(emotion)
        best_edits.append(best_edit)
        best_improvements.append(best_improvement)

x_labels = []

for emotion, best_edit in zip(emotions, best_edits):
    label = f"{emotion}\n({best_edit})"
    x_labels.append(label)

plt.figure(figsize=(11, 5))

plt.bar(x_labels, best_improvements)

plt.axhline(y=0, linestyle="--", linewidth=1)

plt.xlabel("Emotion and Best Edit")
plt.ylabel("Best CLIP Score Improvement")
plt.title("Best CLIP Score Improvement Across Emotions")

plt.xticks(rotation=20, ha="right")

plt.tight_layout()

plt.savefig(output_path, dpi=200)
plt.close()

print(f"Summary plot saved to: {output_path}")