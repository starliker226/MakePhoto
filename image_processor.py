from PIL import Image, ImageDraw, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import numpy as np
from rembg import remove  # 添加rembg库
# 确保安装onnxruntime库，可以通过以下命令安装：
# pip install onnxruntime
# 确保安装numba和pymatting库的最新版本，可以通过以下命令安装：
# pip install --upgrade numba pymatting

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.image_path = image_path
        self.mask = None

    def load_image(self):
        return self.image

    def create_mask(self):
        # 使用rembg库进行人物抠图
        input = self.image
        output = remove(input)
        self.mask = Image.new("L", output.size, 0)
        self.mask.paste(output.split()[-1], (0, 0))
        self.image = output

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

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("二寸证件照生成器")
        self.root.geometry("800x600")  # 增加窗口大小以显示两张图片
        self.root.configure(bg="#f0f0f0")  # 设置背景颜色
        
        self.image_path = None
        self.background_color = (255, 255, 255)  # 默认背景颜色为白色
        
        self.original_image_label = tk.Label(self.root, bg="#f0f0f0", bd=2, relief=tk.SOLID)  # 添加边框
        self.original_image_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.composite_image_label = tk.Label(self.root, bg="#f0f0f0", bd=2, relief=tk.SOLID)  # 添加边框
        self.composite_image_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.image_info_label = tk.Label(self.root, bg="#f0f0f0", font=("Arial", 10))
        self.image_info_label.pack(side=tk.BOTTOM, pady=10)
        
        self.color_info_label = tk.Label(self.root, bg="#f0f0f0", font=("Arial", 10))
        self.color_info_label.pack(side=tk.BOTTOM, pady=10)
        
        self.create_widgets()

    def create_widgets(self):
        # 创建一个框架来容纳按钮
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(side=tk.BOTTOM, pady=20)  # 将框架放置在窗口底部
        
        # 选择图片按钮
        self.select_image_button = tk.Button(button_frame, text="选择图片", command=self.select_image, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.select_image_button.pack(side=tk.LEFT, padx=10)  # 将按钮放置在框架的左侧
        
        # 选择背景颜色按钮
        self.select_color_button = tk.Button(button_frame, text="选择背景颜色", command=self.select_background_color, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.select_color_button.pack(side=tk.LEFT, padx=10)  # 将按钮放置在框架的左侧
        
        # 保存图片按钮
        self.save_image_button = tk.Button(button_frame, text="保存图片", command=self.save_image, bg="#FF5722", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.save_image_button.pack(side=tk.LEFT, padx=10)  # 将按钮放置在框架的左侧

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.image_info_label.config(text=f"已选择图片: {self.image_path}")
            self.display_image(self.original_image_label, self.image_path)

    def display_image(self, label, image_path):
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # 缩放图片以适应Label
        photo = ImageTk.PhotoImage(image)
        label.image = photo  # 保持对PhotoImage对象的引用
        label.config(image=photo)

    def select_background_color(self):
        color_code = colorchooser.askcolor(title="选择背景颜色")[0]
        if color_code:
            self.background_color = tuple(int(c) for c in color_code)
            self.color_info_label.config(text=f"已选择背景颜色: {self.background_color}")

    def save_image(self):
        if not self.image_path:
            messagebox.showerror("错误", "请先选择图片")
            return
        
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if output_path:
            processor = ImageProcessor(self.image_path)
            processor.load_image()
            processor.create_mask()  # 修改为不带参数的create_mask方法
            processor.change_background((0, 0, 0))  # 更改背景颜色为黑色
            processor.composite_image(self.background_color)
            processor.save_image(output_path)
            messagebox.showinfo("提示", f"图片已保存到: {output_path}")
            self.display_image(self.composite_image_label, output_path)

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()