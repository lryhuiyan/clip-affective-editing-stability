EMOTION_PRESETS = {
    "happy": {
        "brightness": 1.15,
        "contrast": 1.05,
        "saturation": 1.25,
        "temperature": 20,
    },
    "lonely": {
        "brightness": 0.85,
        "contrast": 0.90,
        "saturation": 0.60,
        "temperature": -30,
    },
    "scary": {
        "brightness": 0.65,
        "contrast": 1.45,
        "saturation": 0.75,
        "temperature": -20,
    },
    "peaceful": {
        "brightness": 1.05,
        "contrast": 0.85,
        "saturation": 0.90,
        "temperature": -10,
    },
    "romantic": {
        "brightness": 1.08,
        "contrast": 0.90,
        "saturation": 1.20,
        "temperature": 25,
    },
    "hopeful": {
        "brightness": 1.20,
        "contrast": 1.05,
        "saturation": 1.15,
        "temperature": 15,
    },
}


def get_emotion_params(emotion):
    """
    根据情绪词返回对应的图像编辑参数。

    参数:
        emotion: 字符串，例如 "lonely"

    返回:
        一个字典，例如:
        {
            "brightness": 0.85,
            "contrast": 0.90,
            "saturation": 0.60,
            "temperature": -30
        }
    """
    emotion = emotion.lower().strip()

    if emotion not in EMOTION_PRESETS:
        raise ValueError(
            f"Unsupported emotion: {emotion}. "
            f"Supported emotions are: {list(EMOTION_PRESETS.keys())}"
        )

    return EMOTION_PRESETS[emotion]


def list_supported_emotions():
    """
    返回当前支持的所有情绪词。
    """
    return list(EMOTION_PRESETS.keys())