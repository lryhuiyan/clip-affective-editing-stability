import csv
from collections import defaultdict


input_csv_path = "results_multi/all_images_all_emotions_summary.csv"

top_examples_path = "results_multi/top_examples_by_emotion.csv"
bottom_examples_path = "results_multi/bottom_examples_by_emotion.csv"
original_best_path = "results_multi/original_best_cases.csv"


def read_rows(csv_path):
    rows = []

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["best_improvement"] = float(row["best_improvement"])
            rows.append(row)

    return rows


def group_by_emotion(rows):
    emotion_to_rows = defaultdict(list)

    for row in rows:
        emotion = row["emotion"]
        emotion_to_rows[emotion].append(row)

    return emotion_to_rows


def save_rows(rows, output_path, fieldnames):
    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_rows(input_csv_path)
    emotion_to_rows = group_by_emotion(rows)

    top_rows = []
    bottom_rows = []

    for emotion, emotion_rows in emotion_to_rows.items():
        sorted_rows = sorted(
            emotion_rows,
            key=lambda row: row["best_improvement"],
            reverse=True,
        )

        top_rows.extend(sorted_rows[:5])
        bottom_rows.extend(sorted_rows[-5:])

    original_best_rows = [
        row for row in rows
        if row["best_edit"] == "original"
    ]

    fieldnames = [
        "image_name",
        "emotion",
        "best_edit",
        "original_score",
        "best_score",
        "best_improvement",
        "csv_path",
        "plot_path",
    ]

    save_rows(top_rows, top_examples_path, fieldnames)
    save_rows(bottom_rows, bottom_examples_path, fieldnames)
    save_rows(original_best_rows, original_best_path, fieldnames)

    print("Example inspection finished.")
    print(f"Top examples saved to: {top_examples_path}")
    print(f"Bottom examples saved to: {bottom_examples_path}")
    print(f"Original-best cases saved to: {original_best_path}")
    print(f"Number of original-best cases: {len(original_best_rows)}")


if __name__ == "__main__":
    main()