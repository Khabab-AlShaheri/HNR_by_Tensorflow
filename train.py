import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
tf.compat.v1.disable_eager_execution()  # إصلاح لمشاكل التوافق
# تحميل البيانات
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# معالجة البيانات
def preprocess_data(images, labels):
    images = images.reshape((-1, 28, 28, 1)).astype("float32") / 255.0
    images = tf.image.resize_with_pad(images, 32, 32)  # زيادة الحجم لتناسب بنية أكثر تعقيدًا
    return images, labels

train_images, train_labels = preprocess_data(train_images, train_labels)
test_images, test_labels = preprocess_data(test_images, test_labels)

# إنشاء مولد البيانات المُعزز
datagen = ImageDataGenerator(
    rotation_range=15,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2
)

# بناء نموذج CNN متقدم
def build_model():
    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,1)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        layers.Conv2D(64, (3,3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        layers.Flatten(),
        layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer,
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model

model = build_model()

# Callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = ModelCheckpoint('model/best_model.h5', save_best_only=True)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)

# التدريب
history = model.fit(
    datagen.flow(train_images, train_labels, batch_size=128, subset='training'),
    validation_data=datagen.flow(train_images, train_labels, batch_size=128, subset='validation'),
    epochs=50,
    callbacks=[early_stop, checkpoint, lr_scheduler]
)

# تقييم النموذج النهائي
model.load_weights('model/best_model.h5')  # تحميل أفضل أوزان
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=0)
print(f'\nالدقة النهائية على بيانات الاختبار: {test_acc:.4f}')

# حفظ النموذج الكامل

model.save('model/final_model.h5')