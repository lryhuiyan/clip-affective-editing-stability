from PIL import Image
import torch
import open_clip


def load_clip_model(
    model_name: str = "ViT-B-32",
    pretrained: str = "openai",
    device: str = "cpu",
):
    """
    加载 CLIP 模型、图像预处理函数和文本 tokenizer。

    参数:
        model_name: CLIP 模型结构名称
        pretrained: 预训练权重来源
        device: 运行设备，当前使用 "cpu"

    返回:
        model: CLIP 模型
        preprocess: 图像预处理函数
        tokenizer: 文本 tokenizer
        device: 实际使用的设备
    """
    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name,
        pretrained=pretrained,
    )

    tokenizer = open_clip.get_tokenizer(model_name)

    model = model.to(device)
    model.eval()

    return model, preprocess, tokenizer, device


def compute_image_text_similarity(
    image_path: str,
    text: str,
    model,
    preprocess,
    tokenizer,
    device: str = "cpu",
) -> float:
    """
    计算一张图片和一句文本之间的 CLIP 相似度。

    参数:
        image_path: 图片路径
        text: 文本描述，例如 "a lonely image"
        model: CLIP 模型
        preprocess: 图像预处理函数
        tokenizer: 文本 tokenizer
        device: 运行设备

    返回:
        similarity: 图片和文本的余弦相似度分数
    """
    image = Image.open(image_path).convert("RGB")

    image_input = preprocess(image).unsqueeze(0).to(device)
    text_input = tokenizer([text]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_input)

        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_features.T).item()

    return similarity