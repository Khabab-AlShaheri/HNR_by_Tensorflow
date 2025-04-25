import tkinter as tk
from tkinter import colorchooser, filedialog
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import tensorflow as tf

model = tf.keras.models.load_model("model/mnist_model.h5")

WIDTH, HEIGHT = 200, 200
DEFAULT_BG = "black"
DEFAULT_COLOR = "white"
BRUSH_SIZE = 10

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("توقع رقم MNIST")
        self.resizable(False, False)

        self.bg_color = DEFAULT_BG
        self.paint_color = DEFAULT_COLOR

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg=self.bg_color, cursor="cross")
        self.canvas.grid(row=0, column=0, columnspan=6, pady=2, padx=2)
        
        self.button_predict = tk.Button(self, text="توقع", width=8, command=self.predict_digit)
        self.button_predict.grid(row=1, column=1)
        
        self.button_clear = tk.Button(self, text="مسح", width=8, command=self.clear_canvas)
        self.button_clear.grid(row=1, column=2)
        
        self.button_save = tk.Button(self, text="حفظ الصورة", width=10, command=self.save_image)
        self.button_save.grid(row=1, column=3)
        
        self.button_color = tk.Button(self, text="لون الفرشاة", width=10, command=self.choose_paint_color)
        self.button_color.grid(row=2, column=1)
        
        self.button_bg_color = tk.Button(self, text="لون الخلفية", width=10, command=self.choose_bg_color)
        self.button_bg_color.grid(row=2, column=2)
        
        self.label_result = tk.Label(self, text="الرسم ثم الضغط على توقع", font=("Arial", 14))
        self.label_result.grid(row=3, column=0, columnspan=6, pady=4)

        self.image1 = Image.new("RGB", (WIDTH, HEIGHT), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image1)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.last_x, self.last_y = None, None

    def paint(self, event):
        x1, y1 = (event.x - BRUSH_SIZE), (event.y - BRUSH_SIZE)
        x2, y2 = (event.x + BRUSH_SIZE), (event.y + BRUSH_SIZE)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.paint_color, outline=self.paint_color)
        self.draw.ellipse([x1, y1, x2, y2], fill=self.paint_color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image1 = Image.new("RGB", (WIDTH, HEIGHT), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image1)
        self.label_result.config(text="الرسم ثم الضغط على توقع")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image1.save(file_path)
            self.label_result.config(text=f"تم حفظ الصورة في:\n{file_path}")

    def choose_paint_color(self):
        color_code = colorchooser.askcolor(title="اختر لون الفرشاة")
        if color_code[1]:
            self.paint_color = color_code[1]

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="اختر لون الخلفية")
        if color_code[1]:
            self.bg_color = color_code[1]
            self.canvas.config(bg=self.bg_color)
            self.clear_canvas()  # أعد رسم الخلفية الجديدة

    def predict_digit(self):
        # معالجة الصورة للرؤية بالأسود والأبيض
        image = self.image1.convert("L")
        # قص الحدود السوداء أو الملونة لاحتواء الرقم
        image = ImageOps.invert(image)
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
        # تغيير الحجم
        image = image.resize((28, 28), Image.LANCZOS)
        # عكس الألوان مرة أخرى لتكون كما في MNIST
        image = ImageOps.invert(image)
        # تحويل إلى مصفوفة numpy وقيم [0,1]
        img_array = np.array(image).astype('float32') / 255.0
        img_array = img_array.reshape(1, 28*28)
        pred = model.predict(img_array)
        digit = np.argmax(pred)
        confidence = np.max(pred)
        self.label_result.config(text=f"الرقم المتوقع: {digit} (ثقة: {confidence:.2f})")

if __name__ == "__main__":
    app = App()
    app.mainloop()