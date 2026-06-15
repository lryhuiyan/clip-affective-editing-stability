from PIL import Image

from editor import (
    open_image,
    save_image,
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_temperature,
)

from emotion_mapper import get_emotion_params
from emotion_editor import apply_emotion_edit


def generate_counterfactual_edits(
    image: Image.Image,
    emotion: str
) -> tuple[dict[str, Image.Image], dict[str, float | int]]:
    """
    为一张图片和一个目标情绪生成反事实编辑结果。

    参数:
        image: PIL 图片对象
        emotion: 情绪词，例如 "lonely"

    返回:
        edited_results:
            一个字典，key 是编辑类型，value 是编辑后的图片对象。
        params:
            一个字典，保存当前情绪对应的图像编辑参数。
    """
    params = get_emotion_params(emotion)

    edited_results = {}

    edited_results["original"] = image

    edited_results["brightness_only"] = adjust_brightness(
        image,
        params["brightness"]
    )

    edited_results["contrast_only"] = adjust_contrast(
        image,
        params["contrast"]
    )

    edited_results["saturation_only"] = adjust_saturation(
        image,
        params["saturation"]
    )

    edited_results["temperature_only"] = adjust_temperature(
        image,
        params["temperature"]
    )

    all_edited_image, _ = apply_emotion_edit(image, emotion)
    edited_results["all_attributes"] = all_edited_image

    return edited_results, params


def save_counterfactual_edits(
    input_path: str,
    emotion: str,
    output_dir: str = "results"
) -> tuple[dict[str, float | int], dict[str, str]]:
    """
    从路径读取图片，生成某个情绪的反事实编辑结果，并保存到文件夹。

    参数:
        input_path: 输入图片路径，例如 "images/test.jpg"
        emotion: 目标情绪，例如 "lonely"
        output_dir: 输出文件夹，默认是 "results"

    返回:
        params:
            当前情绪对应的参数字典。
        saved_paths:
            一个字典，key 是编辑类型，value 是保存后的图片路径。
    """
    image = open_image(input_path)

    edited_results, params = generate_counterfactual_edits(image, emotion)

    saved_paths = {}

    for edit_name, edited_image in edited_results.items():
        save_path = f"{output_dir}/counterfactual_{emotion}_{edit_name}.jpg"
        save_image(edited_image, save_path)
        saved_paths[edit_name] = save_path

    return params, saved_paths