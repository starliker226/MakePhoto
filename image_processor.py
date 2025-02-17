from PIL import Image, ImageDraw, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import numpy as np
from rembg import remove  # 使用rembg库进行人物抠图

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
        # 加载图像
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
        # 将抠图与背景颜色合成
        if self.mask is None:
            raise ValueError("Mask not created. Please create a mask first.")
        background = Image.new('RGB', self.image.size, background_color)
        composite = Image.composite(self.image, background, self.mask)
        self.image = composite

    def save_image(self, output_path):
        # 保存处理后的图像
        self.image.save(output_path)
        print(f"Image saved to {output_path}")

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("证件照生成器")
        self.root.geometry("680x500")  # 设置固定窗口大小为680x500
        self.root.configure(bg="#f0f0f0")
        
        # 计算窗口在屏幕中央的位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 680) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"+{x}+{y}")  # 设置窗口在屏幕中央
        
        self.image_path = None
        self.background_color = (255, 255, 255)  # 默认背景颜色为白色
        self.one_inch_size = (295, 413)  # 一寸照片的尺寸
        self.two_inch_size = (413, 579)  # 二寸照片的尺寸
        
        # 使用Grid布局来放置图片标签
        self.original_image_label = tk.Label(self.root, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.original_image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.composite_image_label = tk.Label(self.root, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.composite_image_label.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.image_info_label = tk.Label(self.root, bg="#f0f0f0", font=("Arial", 10))
        self.image_info_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.color_info_label = tk.Label(self.root, bg="#f0f0f0", font=("Arial", 10))
        self.color_info_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 将按钮放置在图片下方
        self.create_widgets()

    def create_widgets(self):
        # 创建一个框架来容纳按钮
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20), sticky="s")  # 将按钮框架移动到第3行，并设置底部填充为20像素
        
        # 选择图片按钮
        self.select_image_button = tk.Button(button_frame, text="选择图片", command=self.select_image, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.select_image_button.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 选择背景颜色按钮
        self.select_color_button = tk.Button(button_frame, text="选择背景颜色", command=self.select_background_color, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.select_color_button.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 新增导出合成图片按钮
        self.export_composite_button = tk.Button(button_frame, text="导出二寸图片", command=self.export_composite_image, bg="#FF5722", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.export_composite_button.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 导出一寸照片按钮
        self.export_one_inch_button = tk.Button(button_frame, text="导出一寸照片", command=self.export_one_inch_image, bg="#9C27B0", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.export_one_inch_button.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 关闭程序按钮
        self.close_button = tk.Button(button_frame, text="关闭程序", command=self.close_program, bg="#F44336", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.close_button.pack(side=tk.LEFT, padx=10, expand=True)
        
        # 调整按钮框架居中对齐
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)  # 增加一列权重配置

    def close_program(self):
        # 关闭程序
        self.root.destroy()

    def select_image(self):
        # 选择图片文件
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.image_info_label.config(text=f"已选择图片: {self.image_path}")
            self.display_image(self.original_image_label, self.image_path)

    def display_image(self, label, image_path):
        # 显示图片
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # 修改缩放图片大小为300x300
        photo = ImageTk.PhotoImage(image)
        label.image = photo  # 保持对PhotoImage对象的引用
        label.config(image=photo)

    def select_background_color(self):
        # 选择背景颜色
        color_code = colorchooser.askcolor(title="选择背景颜色")[0]
        if color_code:
            self.background_color = tuple(int(c) for c in color_code)
            self.color_info_label.config(text=f"已选择背景颜色: {self.background_color}")
            self.update_composite_image()

    def update_composite_image(self):
        # 更新合成图片
        if self.image_path:
            processor = ImageProcessor(self.image_path)
            processor.load_image()
            processor.create_mask()
            processor.change_background((0, 0, 0))  # 更改背景颜色为黑色
            processor.composite_image(self.background_color)
            temp_output_path = "temp_composite.jpg"
            processor.save_image(temp_output_path)
            self.display_image(self.composite_image_label, temp_output_path)
            os.remove(temp_output_path)  # 删除临时文件

    def export_composite_image(self):
        # 导出合成的二寸图片
        if not self.image_path:
            messagebox.showerror("错误", "请先选择图片")
            return
        
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp")])
        if output_path:
            processor = ImageProcessor(self.image_path)
            processor.load_image()
            processor.create_mask()
            processor.change_background(self.background_color)  # 使用选择的背景颜色
            processor.composite_image(self.background_color)
            processor.image = processor.image.resize(self.two_inch_size)  # 调整图片大小为二寸
            processor.save_image(output_path)
            messagebox.showinfo("提示", f"合成图片已保存到: {output_path}")
            self.display_image(self.composite_image_label, output_path)

    def export_one_inch_image(self):
        # 导出一寸照片
        if not self.image_path:
            messagebox.showerror("错误", "请先选择图片")
            return
        
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp")])
        if output_path:
            processor = ImageProcessor(self.image_path)
            processor.load_image()
            processor.create_mask()
            processor.change_background((0, 0, 0))  # 更改背景颜色为黑色
            processor.composite_image(self.background_color)
            processor.image = processor.image.resize(self.one_inch_size)  # 调整图片大小为一寸
            processor.save_image(output_path)
            messagebox.showinfo("提示", f"一寸照片已保存到: {output_path}")
            self.display_image(self.composite_image_label, output_path)

def main():
    # 主函数
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()