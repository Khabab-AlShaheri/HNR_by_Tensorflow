# استخدام صورة أساسية مع Python
FROM python:3.8-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات المطلوبة
COPY requirements.txt .
COPY train_model.ipynb .
COPY model/ ./model/

# تثبيت التبعيات
RUN pip install --no-cache-dir -r requirements.txt

# أمر تشغيل التدريب عند بدء الحاوية
CMD ["python", "train.py"]