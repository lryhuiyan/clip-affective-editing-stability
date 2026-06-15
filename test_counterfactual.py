from counterfactual import save_counterfactual_edits

emotion = "lonely"

params, saved_paths = save_counterfactual_edits(
    input_path="images/test.jpg",
    emotion=emotion,
    output_dir="results",
)

print(f"Target emotion: {emotion}")
print(f"Params: {params}")
print("Saved counterfactual images:")

for edit_name, save_path in saved_paths.items():
    print(f"{edit_name}: {save_path}")

print("Done! 反事实编辑结果已经保存到 results/ 文件夹。")