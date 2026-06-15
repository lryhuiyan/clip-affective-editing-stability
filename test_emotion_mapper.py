from emotion_mapper import get_emotion_params, list_supported_emotions

print("Supported emotions:")
print(list_supported_emotions())

print("\nParams for lonely:")
print(get_emotion_params("lonely"))

print("\nParams for Scary with uppercase input:")
print(get_emotion_params("Scary"))