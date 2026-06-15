import csv
from collections import defaultdict, Counter


input_csv_path = "results_multi/all_images_all_emotions_summary.csv"

best_edit_counts_path = "results_multi/emotion_best_edit_counts.csv"
average_improvements_path = "results_multi/emotion_average_improvements.csv"
stability_analysis_path = "results_multi/emotion_stability_analysis.csv"


def read_summary_rows(csv_path):
    rows = []

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["original_score"] = float(row["original_score"])
            row["best_score"] = float(row["best_score"])
            row["best_improvement"] = float(row["best_improvement"])
            rows.append(row)

    return rows


def analyze_best_edit_counts(rows):
    emotion_to_best_edits = defaultdict(list)

    for row in rows:
        emotion = row["emotion"]
        best_edit = row["best_edit"]

        emotion_to_best_edits[emotion].append(best_edit)

    count_rows = []

    for emotion, best_edits in emotion_to_best_edits.items():
        counter = Counter(best_edits)

        for best_edit, count in counter.items():
            count_rows.append(
                {
                    "emotion": emotion,
                    "best_edit": best_edit,
                    "count": count,
                }
            )

    return count_rows


def analyze_average_improvements(rows):
    emotion_to_improvements = defaultdict(list)

    for row in rows:
        emotion = row["emotion"]
        best_improvement = row["best_improvement"]

        emotion_to_improvements[emotion].append(best_improvement)

    average_rows = []

    for emotion, improvements in emotion_to_improvements.items():
        average_improvement = sum(improvements) / len(improvements)

        average_rows.append(
            {
                "emotion": emotion,
                "num_images": len(improvements),
                "average_best_improvement": average_improvement,
                "max_best_improvement": max(improvements),
                "min_best_improvement": min(improvements),
            }
        )

    return average_rows


def analyze_stability(rows):
    emotion_to_best_edits = defaultdict(list)

    for row in rows:
        emotion = row["emotion"]
        best_edit = row["best_edit"]

        emotion_to_best_edits[emotion].append(best_edit)

    stability_rows = []

    for emotion, best_edits in emotion_to_best_edits.items():
        counter = Counter(best_edits)

        dominant_best_edit, dominant_count = counter.most_common(1)[0]
        num_images = len(best_edits)
        dominant_edit_ratio = dominant_count / num_images

        stability_rows.append(
            {
                "emotion": emotion,
                "dominant_best_edit": dominant_best_edit,
                "dominant_count": dominant_count,
                "num_images": num_images,
                "dominant_edit_ratio": dominant_edit_ratio,
            }
        )

    return stability_rows


def save_csv(rows, output_path, fieldnames):
    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_summary_rows(input_csv_path)

    best_edit_count_rows = analyze_best_edit_counts(rows)
    average_improvement_rows = analyze_average_improvements(rows)
    stability_rows = analyze_stability(rows)

    save_csv(
        best_edit_count_rows,
        best_edit_counts_path,
        ["emotion", "best_edit", "count"],
    )

    save_csv(
        average_improvement_rows,
        average_improvements_path,
        [
            "emotion",
            "num_images",
            "average_best_improvement",
            "max_best_improvement",
            "min_best_improvement",
        ],
    )

    save_csv(
        stability_rows,
        stability_analysis_path,
        [
            "emotion",
            "dominant_best_edit",
            "dominant_count",
            "num_images",
            "dominant_edit_ratio",
        ],
    )

    print("Analysis finished.")
    print(f"Best edit counts saved to: {best_edit_counts_path}")
    print(f"Average improvements saved to: {average_improvements_path}")
    print(f"Stability analysis saved to: {stability_analysis_path}")


if __name__ == "__main__":
    main()