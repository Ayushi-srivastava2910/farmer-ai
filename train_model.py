import tensorflow as tf # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

# 📁 dataset path
data_dir = "dataset"

# 🔄 preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    zoom_range=0.3,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    "dataset",
    target_size=(224,224),
    batch_size=32,
    subset="training"
)
print(train_data.class_indices)

val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

val_data = val_datagen.flow_from_directory(
    "dataset",
    target_size=(224,224),
    batch_size=32,
    subset="validation"
)

# 🧠 model (MobileNet - lightweight & powerful)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224,224,3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(train_data.num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 🚀 training
model.fit(train_data, validation_data=val_data, epochs=5)

# 💾 save model
model.save("model.h5")

print("✅ MODEL TRAINED SUCCESSFULLY")