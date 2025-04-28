**Handwritten Numbers Recognition Project**

**نضره عامه :**

بناء شبكة عصبية للتعرف على الأرقام المكتوبة بخط اليد باستخدام مكتبة TensorFlow

**المتطلبات :**

**هذه هي إصدارات الحزمة التي تم تطوير الكود واختبارها عليها ، وقد تعمل مع الإصدارات السابقة.**


      python \>= 3.12.5
      
      pillow \>= 10.4.0
      
      tensorflow \>= 2.19.0
      
      numpy \>= 2.0.2



**وصف المشروع:**

بناء نموذج عصبي باستخدام TensorFlow، وتدريبه على مجموعة بيانات MNIST الشهيرة، ثم تطبيقه في واجهة مستخدم تفاعلية تسمح للمستخدمين برسم الأرقام والحصول على تنبؤات فورية.

**البيانات :**

تم تحميل البيانات مباشرة من MINIST

**الهدف :**

يتم استخدام الكود الموجود في هذا الريبو لإنشاء وتدريب نموذج من TensorFlow وتصدير النتيجة بتنسيق يمكن تقديمه باستخدام TensorFlow.

**تعليمات الاستخدام :**

  **1.فتح موجهة الاوامر و إنشاء مجلد جديد**

         mkdir namefolder
         cd namefolder

   **2.تنزيل المشروع :**
    
    
         git clone https://github.com/Khabab-AlShaheri/HNR_by_Tensorflow.git
   **3.الدخول الى مجلد المشروع**
         
         cd HNR_by_Tensorflow
      

  **4.إعداد البيئة الافتراضية (اختياري ولكن موصى به)**


         python -m venv name_venv
         name_venv/Scripts/activate.bat على نظام تشغيل الويندوز \#
         source name_venv/bin/activate على نظام تشغيل لينكس او ماك \#
  

   **5. تثبيت المتطلبات**

   سيتم تثبيت جميع الحزم اللازمة لتشغيل المشروع  .​

     pip install -r requirements.txt

   **6. تدريب النموذج**

  لتدريب النموذج، يمكنك استخدام Jupyter Notebook أو تشغيل السكربت مباشرة.

 ثم افتح الملف  train_model.ipynb  وابدا في التنفيذ .

 تشغيل السكربت مباشرة

       python train_model.py

   **7. استخدام النموذج المدرب**

      cd app
      python recognizer_app.py

**هيكل المشروع :**

    :.

    │ .gitignore     \#Git لتحديد الملفات التي يتم تجاهلها من قبل

    │ Dockerfile    \# Docker container ملف إعداد لتشغيل المشروع داخل

    │ recognizer.py    \# سكربت لتشغيل النموذج على صور جديدة تم استبداله 

    │ requirements.txt   \# قائمة بالحزم المطلوبة للمشروع 

    │ train_model.ipynb    \#ملف تدريب النموذج \#

    │

    ├───app

    │       recognizer_app.py   \# سكربت لتشغيل النموذج على صور جديدة 

    │

    └───model     \# يحتوي على ملفات النماذج المدربة أو ملفات الحفظ

          best_model.h5
      
          final_model.h5
      
          mnist_model.h5
