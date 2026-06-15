from PIL import Image, ImageEnhance


def open_image(image_path):
    """
    读取图片，并统一转换为 RGB 格式。
    """
    return Image.open(image_path).convert("RGB")


def save_image(image, save_path):
    """
    保存图片。
    """
    image.save(save_path)


def adjust_brightness(image, factor):
    """
    调整亮度。

    factor = 1.0 表示不变
    factor > 1.0 表示变亮
    factor < 1.0 表示变暗
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image, factor):
    """
    调整对比度。

    factor = 1.0 表示不变
    factor > 1.0 表示提高对比度
    factor < 1.0 表示降低对比度
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def adjust_saturation(image, factor):
    """
    调整饱和度。

    factor = 1.0 表示不变
    factor > 1.0 表示颜色更鲜艳
    factor < 1.0 表示颜色更灰、更淡
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def adjust_temperature(image, shift):
    """
    调整色温。

    shift > 0 表示偏暖：增强红色，削弱蓝色
    shift < 0 表示偏冷：增强蓝色，削弱红色

    shift 建议范围：-50 到 50
    """
    r, g, b = image.split()

    if shift > 0:
        r = r.point(lambda i: min(255, i + shift))
        b = b.point(lambda i: max(0, i - shift))
    elif shift < 0:
        shift = abs(shift)
        r = r.point(lambda i: max(0, i - shift))
        b = b.point(lambda i: min(255, i + shift))

    return Image.merge("RGB", (r, g, b))