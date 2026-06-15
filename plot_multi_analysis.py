import csv
from collections import defaultdict

import matplotlib.pyplot as plt


average_csv_path = "results_multi/emotion_average_improvements.csv"
count_csv_path = "results_multi/emotion_best_edit_counts.csv"
stability_csv_path = "results_multi/emotion_stability_analysis.csv"

average_output_path = "results_multi/emotion_average_improvements.png"
count_output_path = "results_multi/emotion_best_edit_counts.png"
stability_output_path = "results_multi/emotion_stability_analysis.png"


def plot_average_improvements():
    emotions = []
    average_improvements = []

    with open(average_csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            emotions.append(row["emotion"])
            average_improvements.append(float(row["average_best_improvement"]))

    plt.figure(figsize=(9, 5))
    plt.bar(emotions, average_improvements)

    plt.axhline(y=0, linestyle="--", linewidth=1)

    plt.xlabel("Emotion")
    plt.ylabel("Average Best CLIP Score Improvement")
    plt.title("Average Best Improvement Across Images")

    plt.tight_layout()
    plt.savefig(average_output_path, dpi=200)
    plt.close()

    print(f"Average improvement plot saved to: {average_output_path}")


def plot_best_edit_counts():
    emotion_to_counts = defaultdict(dict)
    all_best_edits = set()

    with open(count_csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            emotion = row["emotion"]
            best_edit = row["best_edit"]
            count = int(row["count"])

            emotion_to_counts[emotion][best_edit] = count
            all_best_edits.add(best_edit)

    emotions = list(emotion_to_counts.keys())
    best_edits = sorted(all_best_edits)

    x_positions = list(range(len(emotions)))
    bar_width = 0.12

    plt.figure(figsize=(12, 6))

    for i, best_edit in enumerate(best_edits):
        counts = []

        for emotion in emotions:
            count = emotion_to_counts[emotion].get(best_edit, 0)
            counts.append(count)

        shifted_positions = [
            x + (i - len(best_edits) / 2) * bar_width
            for x in x_positions
        ]

        plt.bar(
            shifted_positions,
            counts,
            width=bar_width,
            label=best_edit,
        )

    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.title("Best Edit Type Counts Across Images")

    plt.xticks(x_positions, emotions)
    plt.legend()

    plt.tight_layout()
    plt.savefig(count_output_path, dpi=200)
    plt.close()

    print(f"Best edit count plot saved to: {count_output_path}")


def plot_stability_analysis():
    emotions = []
    ratios = []
    labels = []

    with open(stability_csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            emotion = row["emotion"]
            dominant_best_edit = row["dominant_best_edit"]
            dominant_edit_ratio = float(row["dominant_edit_ratio"])

            emotions.append(emotion)
            ratios.append(dominant_edit_ratio)
            labels.append(f"{emotion}\n({dominant_best_edit})")

    plt.figure(figsize=(10, 5))

    plt.bar(labels, ratios)

    plt.xlabel("Emotion and Dominant Best Edit")
    plt.ylabel("Dominant Edit Ratio")
    plt.title("Stability of Dominant Best Edit Across Images")

    plt.ylim(0, 1)

    plt.xticks(rotation=20, ha="right")

    plt.tight_layout()
    plt.savefig(stability_output_path, dpi=200)
    plt.close()

    print(f"Stability analysis plot saved to: {stability_output_path}")


def main():
    plot_average_improvements()
    plot_best_edit_counts()
    plot_stability_analysis()


if __name__ == "__main__":
    main()