from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image,ImageDraw,ImageOps
import numpy as np
from tensorflow.keras.models import load_model

WIDTH, HEIGHT = 200, 200
DEFAULT_BG = "black"
DEFAULT_COLOR = "white"
BRUSH_SIZE = 10
# تحميل النموذج الجديد
model = load_model('../model/best_model.h5')

def predict_digit(img):
    # إعادة تشكيل الصورة لتكون 32x32 بكسل
    img = img.resize((32, 32))
    # تحويل الصورة إلى تدرج الرمادي
    img = img.convert('L')
    img = np.array(img)
    # إعادة تشكيل الصورة لتناسب إدخال النموذج وتطبيع البيانات
    img = img.reshape(1, 32, 32, 1)
    img = img / 255.0
    # التنبؤ بالرقم
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        self.bg_color = DEFAULT_BG
        self.paint_color = DEFAULT_COLOR
        # إنشاء عناصر الواجهة
        self.canvas = tk.Canvas(self, width=300, height=300, bg="black", cursor="cross")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Recognise", command=self.classify_handwriting)   
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)
       
        # تنظيم العناصر باستخدام الشبكة
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        self.image1 = Image.new("RGB", (WIDTH, HEIGHT), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image1)

        # ربط أحداث الرسم
        self.canvas.bind("<B1-Motion>", self.paint)
        self.last_x, self.last_y = None, None

    def clear_all(self):
        """مسح كل شيء من اللوحة"""
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        """التنبؤ بالرقم المرسوم"""
        HWND = self.canvas.winfo_id()  # الحصول على معرف اللوحة
        rect = win32gui.GetWindowRect(HWND)  # الحصول على إحداثيات اللوحة
        a, b, c, d = rect
        rect = (a + 4, b + 4, c - 4, d - 4)
        im = ImageGrab.grab(rect)

        # التنبؤ بالرقم
        digit, acc = predict_digit(im)
        self.label.configure(text=f"{digit}, {int(acc * 100)}%")

    # def draw_lines(self, event):
    #     """رسم خطوط على اللوحة"""
    #     self.x = event.x
    #     self.y = event.y
    #     r = 8
    #     self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='white')
        
    def paint(self, event):
        x1, y1 = (event.x - BRUSH_SIZE), (event.y - BRUSH_SIZE)
        x2, y2 = (event.x + BRUSH_SIZE), (event.y + BRUSH_SIZE)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.paint_color, outline=self.paint_color)
        self.draw.ellipse([x1, y1, x2, y2], fill=self.paint_color)

        
# تشغيل التطبيق
app = App()
mainloop()