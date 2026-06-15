from editor import (
    open_image,
    save_image,
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_temperature,
)

from emotion_mapper import get_emotion_params


def apply_emotion_edit(image, emotion):
    """
    根据情绪词对图片进行编辑。

    参数:
        image: PIL Image 图片对象
        emotion: 情绪词，例如 "lonely"

    返回:
        edited_image: 编辑后的图片
        params: 当前情绪对应的编辑参数
    """
    params = get_emotion_params(emotion)

    edited_image = image

    edited_image = adjust_brightness(
        edited_image,
        params["brightness"]
    )

    edited_image = adjust_contrast(
        edited_image,
        params["contrast"]
    )

    edited_image = adjust_saturation(
        edited_image,
        params["saturation"]
    )

    edited_image = adjust_temperature(
        edited_image,
        params["temperature"]
    )

    return edited_image, params


def edit_image_by_emotion(input_path, emotion, output_path):
    """
    从文件路径读取图片，根据情绪词编辑图片，并保存结果。

    参数:
        input_path: 输入图片路径
        emotion: 情绪词
        output_path: 输出图片路径

    返回:
        params: 当前情绪对应的编辑参数
    """
    image = open_image(input_path)

    edited_image, params = apply_emotion_edit(image, emotion)

    save_image(edited_image, output_path)

    return params