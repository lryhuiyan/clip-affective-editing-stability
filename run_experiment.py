import argparse
import csv
import os

import matplotlib.pyplot as plt

from counterfactual import save_counterfactual_edits
from clip_evaluator import load_clip_model, compute_image_text_similarity


def run_single_emotion_experiment(
    input_path: str,
    emotion: str,
    output_dir: str = "results",
    text_prompt: str | None = None,
    model=None,
    preprocess=None,
    tokenizer=None,
    device=None,
    keep_generated_images: bool = True,
):
    """
    对一张图片和一个目标情绪运行完整反事实实验。

    流程:
    1. 生成反事实编辑图片
    2. 使用 CLIP 计算每张图片与目标文本的相似度
    3. 保存 CSV 结果
    4. 绘制分数提升柱状图
    5. 如果 keep_generated_images=False，则删除中间生成的反事实图片
    """
    if text_prompt is None:
        text_prompt = f"a {emotion} image"

    print("=" * 60)
    print(f"Running experiment for emotion: {emotion}")
    print(f"Input image: {input_path}")
    print(f"Text prompt: {text_prompt}")
    print("=" * 60)

    # Step 1: 生成反事实编辑图片
    params, saved_paths = save_counterfactual_edits(
        input_path=input_path,
        emotion=emotion,
        output_dir=output_dir,
    )

    print("Counterfactual images generated.")
    print(f"Emotion params: {params}")
    print("-" * 60)

    # Step 2: 加载 CLIP 模型
    # 如果外部没有传入模型，就在这里加载；
    # 如果外部已经传入模型，就直接复用，避免批量实验时反复加载。
    if model is None or preprocess is None or tokenizer is None or device is None:
        model, preprocess, tokenizer, device = load_clip_model()

    scores = {}

    for edit_name, image_path in saved_paths.items():
        score = compute_image_text_similarity(
            image_path=image_path,
            text=text_prompt,
            model=model,
            preprocess=preprocess,
            tokenizer=tokenizer,
            device=device,
        )

        scores[edit_name] = score

    # Step 3: 打印结果并准备 CSV 行
    original_score = scores["original"]

    rows = []

    print(f"CLIP text prompt: {text_prompt}")
    print("-" * 60)

    for edit_name, score in scores.items():
        improvement = score - original_score

        print(
            f"{edit_name}: score={score:.4f}, "
            f"improvement={improvement:+.4f}"
        )

        rows.append(
            {
                "edit_name": edit_name,
                "score": score,
                "improvement": improvement,
            }
        )

    best_edit = max(scores, key=scores.get)
    best_score = scores[best_edit]

    print("-" * 60)
    print(f"Best edit: {best_edit}")
    print(f"Best score: {best_score:.4f}")

    # Step 4: 保存 CSV
    safe_prompt_name = text_prompt.replace(" ", "_").replace("/", "_")
    csv_path = f"{output_dir}/{emotion}_{safe_prompt_name}_clip_scores.csv"

    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["edit_name", "score", "improvement"],
        )

        writer.writeheader()
        writer.writerows(rows)

    print("-" * 60)
    print(f"CSV saved to: {csv_path}")

    # Step 5: 绘制柱状图
    plot_path = f"{output_dir}/{emotion}_{safe_prompt_name}_clip_improvements.png"

    edit_names = [row["edit_name"] for row in rows]
    improvements = [row["improvement"] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.bar(edit_names, improvements)
    plt.axhline(y=0, linestyle="--", linewidth=1)

    plt.xlabel("Edit Type")
    plt.ylabel("CLIP Score Improvement")
    plt.title(f"CLIP Score Improvements\nPrompt: '{text_prompt}'")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(plot_path, dpi=200)
    plt.close()

    print(f"Plot saved to: {plot_path}")

    # Step 6: 如果是批量正式实验，可以删除中间生成的反事实图片
    # 注意：这里只删除 output_dir 里的临时结果图，不会删除 images/multi 里的原始输入图片。
    if not keep_generated_images:
        for edit_name, image_path in saved_paths.items():
            if os.path.exists(image_path):
                os.remove(image_path)

        print("Generated counterfactual images removed.")

    return {
        "emotion": emotion,
        "text_prompt": text_prompt,
        "params": params,
        "scores": scores,
        "best_edit": best_edit,
        "csv_path": csv_path,
        "plot_path": plot_path,
    }


def parse_args():
    """
    解析命令行参数。
    """
    parser = argparse.ArgumentParser(
        description="Run a CLIP-guided counterfactual affective image editing experiment."
    )

    parser.add_argument(
        "--input",
        type=str,
        default="images/test.jpg",
        help="Path to the input image.",
    )

    parser.add_argument(
        "--emotion",
        type=str,
        default="lonely",
        help="Target emotion used for image editing, such as lonely, scary, peaceful.",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Optional free-form text prompt for CLIP evaluation.",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="results",
        help="Directory for saving output images, CSV files, and plots.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    result = run_single_emotion_experiment(
        input_path=args.input,
        emotion=args.emotion,
        output_dir=args.output_dir,
        text_prompt=args.prompt,
    )

    print("=" * 60)
    print("Experiment finished.")
    print(f"Emotion: {result['emotion']}")
    print(f"Text prompt: {result['text_prompt']}")
    print(f"Best edit: {result['best_edit']}")
    print(f"CSV: {result['csv_path']}")
    print(f"Plot: {result['plot_path']}")