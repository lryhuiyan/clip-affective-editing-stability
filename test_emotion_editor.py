from emotion_editor import edit_image_by_emotion

emotions = [
    "happy",
    "lonely",
    "scary",
    "peaceful",
    "romantic",
    "hopeful",
]

for emotion in emotions:
    output_path = f"results/test_{emotion}.jpg"

    params = edit_image_by_emotion(
        input_path="images/test.jpg",
        emotion=emotion,
        output_path=output_path,
    )

    print(f"Emotion: {emotion}")
    print(f"Saved to: {output_path}")
    print(f"Params: {params}")
    print("-" * 50)

print("Done! 所有情绪编辑结果已保存到 results/ 文件夹。")