import csv
import os
from pathlib import Path

from clip_evaluator import load_clip_model
from run_experiment import run_single_emotion_experiment


EMOTIONS = [
    "happy",
    "lonely",
    "scary",
    "peaceful",
    "romantic",
    "hopeful",
]


def find_image_files(image_dir):
    image_dir_path = Path(image_dir)

    image_files = []

    for suffix in ["*.jpg", "*.jpeg", "*.png"]:
        image_files.extend(image_dir_path.glob(suffix))

    image_files = sorted(image_files)

    return image_files


def run_multi_image_experiments():
    image_dir = "images/multi"
    output_dir = "results_multi"

    os.makedirs(output_dir, exist_ok=True)

    image_files = find_image_files(image_dir)

    if len(image_files) == 0:
        print("No images found.")
        return

    summary_rows = []

    print("=" * 60)
    print("Running multi-image experiments")
    print(f"Number of images: {len(image_files)}")
    print("=" * 60)

    print("Loading CLIP model once...")
    model, preprocess, tokenizer, device = load_clip_model()
    print("CLIP model loaded.")

    for image_path in image_files:
        image_name = image_path.stem

        print("=" * 60)
        print(f"Processing image: {image_name}")
        print("=" * 60)

        image_output_dir = f"{output_dir}/{image_name}"
        os.makedirs(image_output_dir, exist_ok=True)

        for emotion in EMOTIONS:
            result = run_single_emotion_experiment(
                input_path=str(image_path),
                emotion=emotion,
                output_dir=image_output_dir,
                model=model,
                preprocess=preprocess,
                tokenizer=tokenizer,
                device=device,
                keep_generated_images=False,
            )

            scores = result["scores"]
            original_score = scores["original"]
            best_edit = result["best_edit"]
            best_score = scores[best_edit]
            best_improvement = best_score - original_score

            summary_rows.append(
                {
                    "image_name": image_name,
                    "emotion": emotion,
                    "best_edit": best_edit,
                    "original_score": original_score,
                    "best_score": best_score,
                    "best_improvement": best_improvement,
                    "csv_path": result["csv_path"],
                    "plot_path": result["plot_path"],
                }
            )

            print(
                f"{image_name} | {emotion} | "
                f"best_edit={best_edit} | "
                f"improvement={best_improvement:+.4f}"
            )

    summary_csv_path = f"{output_dir}/all_images_all_emotions_summary.csv"

    with open(summary_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "image_name",
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

    print("=" * 60)
    print("All experiments finished.")
    print(f"Summary saved to: {summary_csv_path}")
    print("=" * 60)


if __name__ == "__main__":
    run_multi_image_experiments()