import csv

from run_experiment import run_single_emotion_experiment


EMOTIONS = [
    "happy",
    "lonely",
    "scary",
    "peaceful",
    "romantic",
    "hopeful",
]


def run_all_emotions(
    input_path: str = "images/test.jpg",
    output_dir: str = "results",
):
    """
    对同一张图片批量运行多个情绪的反事实实验，
    并生成多情绪汇总表。
    """
    all_results = []
    summary_rows = []

    print("=" * 60)
    print("Running experiments for all emotions")
    print(f"Input image: {input_path}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)

    for emotion in EMOTIONS:
        result = run_single_emotion_experiment(
            input_path=input_path,
            emotion=emotion,
            output_dir=output_dir,
        )

        all_results.append(result)

        scores = result["scores"]
        original_score = scores["original"]
        best_edit = result["best_edit"]
        best_score = scores[best_edit]
        best_improvement = best_score - original_score

        summary_rows.append(
            {
                "emotion": emotion,
                "best_edit": best_edit,
                "original_score": original_score,
                "best_score": best_score,
                "best_improvement": best_improvement,
                "csv_path": result["csv_path"],
                "plot_path": result["plot_path"],
            }
        )

        print("=" * 60)
        print(f"Finished emotion: {emotion}")
        print(f"Best edit: {best_edit}")
        print("=" * 60)

    summary_csv_path = f"{output_dir}/all_emotions_summary.csv"

    with open(summary_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "emotion",
                "best_edit",
                "original_score",
                "best_score",
                "best_improvement",
                "csv_path",
                "plot_path",
            ],
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print("All emotion experiments finished.")
    print("-" * 60)

    for row in summary_rows:
        print(
            f"{row['emotion']}: "
            f"best_edit={row['best_edit']}, "
            f"best_improvement={row['best_improvement']:+.4f}"
        )

    print("-" * 60)
    print(f"Summary CSV saved to: {summary_csv_path}")

    return all_results, summary_csv_path


if __name__ == "__main__":
    run_all_emotions()