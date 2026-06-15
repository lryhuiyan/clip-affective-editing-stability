import csv
from pathlib import Path


summary_csv = Path("results_multi/all_images_all_emotions_summary.csv")
output_csv = Path("case_studies/case_study_summary.csv")


selected_cases = [
    ("test_027", "lonely"),
    ("test_023", "lonely"),
    ("test_023", "scary"),
    ("test_054", "scary"),
    ("test_085", "romantic"),
    ("test_041", "hopeful"),
    ("test_029", "hopeful"),
]


def main():
    selected_set = set(selected_cases)

    rows = []

    with open(summary_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            key = (row["image_name"], row["emotion"])

            if key in selected_set:
                rows.append(row)

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

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved case study summary to: {output_csv}")
    print(f"Number of cases: {len(rows)}")


if __name__ == "__main__":
    main()