import csv

from clip_evaluator import load_clip_model, compute_image_text_similarity

# 目标情绪
emotion = "lonely"
text_prompt = f"a {emotion} image"

# 需要评估的反事实图片
image_paths = {
    "original": "results/counterfactual_lonely_original.jpg",
    "brightness_only": "results/counterfactual_lonely_brightness_only.jpg",
    "contrast_only": "results/counterfactual_lonely_contrast_only.jpg",
    "saturation_only": "results/counterfactual_lonely_saturation_only.jpg",
    "temperature_only": "results/counterfactual_lonely_temperature_only.jpg",
    "all_attributes": "results/counterfactual_lonely_all_attributes.jpg",
}

# 加载 CLIP 模型
model, preprocess, tokenizer, device = load_clip_model()

# 保存每种编辑方式的 CLIP 分数
scores = {}

for edit_name, image_path in image_paths.items():
    score = compute_image_text_similarity(
        image_path=image_path,
        text=text_prompt,
        model=model,
        preprocess=preprocess,
        tokenizer=tokenizer,
        device=device,
    )

    scores[edit_name] = score

# 输出所有分数
print(f"Text prompt: {text_prompt}")
print("-" * 50)

for edit_name, score in scores.items():
    print(f"{edit_name}: {score:.4f}")

# 找出分数最高的编辑方式
best_edit = max(scores, key=scores.get)
best_score = scores[best_edit]

print("-" * 50)
print(f"Best edit: {best_edit}")
print(f"Best score: {best_score:.4f}")

# 计算相对原图的提升
original_score = scores["original"]

print("-" * 50)
print("Score improvements compared with original:")

rows = []

for edit_name, score in scores.items():
    improvement = score - original_score
    print(f"{edit_name}: {improvement:+.4f}")

    rows.append(
        {
            "edit_name": edit_name,
            "score": score,
            "improvement": improvement,
        }
    )

# 保存 CSV 文件
csv_path = f"results/{emotion}_clip_scores.csv"

with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["edit_name", "score", "improvement"],
    )

    writer.writeheader()
    writer.writerows(rows)

print("-" * 50)
print(f"CSV saved to: {csv_path}")