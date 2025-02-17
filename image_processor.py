from PIL import Image, ImageDraw
import os

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.image_path = image_path
        self.mask = None

    def load_image(self):
        return self.image

    def create_mask(self, box):
        # 创建一个与图像大小相同的透明掩码
        self.mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(self.mask)
        # 在掩码上绘制一个白色矩形，用于抠图
        draw.rectangle(box, fill=255)

    def change_background(self, color):
        # 将背景颜色替换为指定颜色
        new_image = self.image.copy()
        new_image.putalpha(255)
        background = Image.new('RGBA', new_image.size, color)
        new_image = Image.alpha_composite(background, new_image)
        self.image = new_image.convert('RGB')

    def composite_image(self, background_color):
        if self.mask is None:
            raise ValueError("Mask not created. Please create a mask first.")
        background = Image.new('RGB', self.image.size, background_color)
        composite = Image.composite(self.image, background, self.mask)
        self.image = composite

    def save_image(self, output_path):
        self.image.save(output_path)
        print(f"Image saved to {output_path}")

def main():
    image_path = 'input.jpg'  # 输入图片路径
    output_path = 'output.jpg'  # 输出图片路径
    background_color = (255, 255, 255)  # 背景颜色 (R, G, B)

    processor = ImageProcessor(image_path)
    processor.load_image()
    processor.create_mask((100, 100, 300, 300))  # 抠图区域 (left, top, right, bottom)
    processor.change_background((0, 0, 0))  # 更改背景颜色为黑色
    processor.composite_image(background_color)
    processor.save_image(output_path)

if __name__ == "__main__":
    main()