import os

import tensorflow as tf

# training crack images
train_crack_dir = '../data/train/crack'

# training no_crack images
train_no_crack_dir = '../data/train/no_crack'

print('total training crack images:', len(os.listdir(train_crack_dir)))
print('total training no_crack images:', len(os.listdir(train_no_crack_dir)))

model = tf.keras.models.Sequential([
 tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
 tf.keras.layers.MaxPool2D((2, 2)),
 tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
 tf.keras.layers.MaxPool2D((2, 2)),
 tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
 tf.keras.layers.MaxPool2D((2, 2)),
 tf.keras.layers.Flatten(),
 tf.keras.layers.Dense(units=512, activation='relu'),
 tf.keras.layers.Dense(units=1, activation='sigmoid'),
])

model.summary()


model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory('../data/train',
                                                    target_size=(150, 150), batch_size=100, class_mode='binary')

validation_generator = train_datagen.flow_from_directory('../data/validation',
                                                         target_size=(150, 150), batch_size=10, class_mode='binary')

history = model.fit_generator(
      train_generator,
      steps_per_epoch=8,
      epochs=20,
      verbose=1,
      validation_data=validation_generator,
      validation_steps=8
)

model.save('crack_detection.h5')