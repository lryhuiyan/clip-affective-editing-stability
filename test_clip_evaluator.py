from clip_evaluator import load_clip_model, compute_image_text_similarity

model, preprocess, tokenizer, device = load_clip_model()

image_path = "results/counterfactual_lonely_original.jpg"
text = "a lonely image"

score = compute_image_text_similarity(
    image_path=image_path,
    text=text,
    model=model,
    preprocess=preprocess,
    tokenizer=tokenizer,
    device=device,
)

print(f"Image: {image_path}")
print(f"Text: {text}")
print(f"CLIP similarity score: {score:.4f}")