from editor import (
    open_image,
    save_image,
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_temperature,
)

# 读取测试图片
img = open_image("images/test.jpg")

# 分别测试不同图像编辑效果
bright_img = adjust_brightness(img, 1.3)
dark_img = adjust_brightness(img, 0.7)
high_contrast_img = adjust_contrast(img, 1.5)
low_saturation_img = adjust_saturation(img, 0.5)
warm_img = adjust_temperature(img, 30)
cool_img = adjust_temperature(img, -30)

# 保存结果
save_image(bright_img, "results/brightness_1_3.jpg")
save_image(dark_img, "results/brightness_0_7.jpg")
save_image(high_contrast_img, "results/contrast_1_5.jpg")
save_image(low_saturation_img, "results/saturation_0_5.jpg")
save_image(warm_img, "results/warm_30.jpg")
save_image(cool_img, "results/cool_30.jpg")

print("Done! editor.py 测试完成，结果已保存到 results/ 文件夹。")