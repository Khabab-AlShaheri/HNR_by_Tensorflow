# استخدام صورة أساسية مع Python
FROM python:3.13.3

# تعيين مجلد العمل
# WORKDIR /app

# # نسخ الملفات المطلوبة
# # COPY requirements.txt .
# COPY train_model.ipynb .
# COPY model/ ./model/

# # تثبيت التبعيات
# RUN pip install --no-cache-dir -r requirements.txt

# # أمر تشغيل التدريب عند بدء الحاوية
# CMD ["python", "train.py"]
# FROM python:3.10-slim  # نسخة بديلة لوجود مشكلة في 3.13.3

WORKDIR /app

COPY . .

RUN pip install tensorflow && \
    mkdir -p /app/model

CMD ["python", "train.py"]