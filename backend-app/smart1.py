import cv2
import numpy as np
from keras.applications.resnet_v2 import preprocess_input
from keras.utils import img_to_array
from PIL import Image
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import cv2
from keras.applications.resnet_v2 import preprocess_input
from keras.utils import img_to_array
from sklearn.model_selection import train_test_split
from keras.applications.resnet_v2 import ResNet50V2
from keras.models import Model
from keras.layers import Dense, Flatten, GlobalAveragePooling2D
import pathlib
from keras.models import load_model
import matplotlib.pyplot as plt



class_names=[]
def training_model4():
    # from google.colab import drive
    # drive.mount('/content/drive')
    # !unzip -q '/content/drive/MyDrive/signDatabasePublicFramesOnly.zip'
    root_dir="dataset/lisa-dataset/"
    total_dataset=pd.read_csv("dataset/lisa-dataset/allAnnotations.csv",sep=";")

    X_dataset=total_dataset[["Filename","Upper left corner X","Upper left corner Y","Lower right corner X","Lower right corner Y"]]
    Y_dataset=total_dataset[["Annotation tag"]]

    le = LabelEncoder()
    Y_dataset['Annotation_encoded']= le.fit_transform(Y_dataset['Annotation tag'])
    class_names=list(le.classes_)
    np.save('classes.npy', le.classes_)

    # if not os.path.exists('cropped_images'):
    #     os.makedirs('cropped_images')

    for index, row in X_dataset.iterrows():
        # img = Image.open(root_dir+row['Filename'])
        # left = row["Upper left corner X"]
        # top = row["Upper left corner Y"]
        # right = row["Lower right corner X"]
        # bottom = row["Lower right corner Y"]
        # cropped_img = img.crop((left, top, right, bottom))
        # cropped_img=cropped_img.resize((50,50))
        cropped_filename = f'cropped_images/cropped_{index}.jpg'
        #cropped_img
        # cropped_img.save(cropped_filename)
        # Add the path of the cropped image to the DataFrame
        X_dataset.loc[index, 'cropped_filename'] = cropped_filename


    X_required=X_dataset[["cropped_filename"]]
    Y_required=Y_dataset[["Annotation_encoded"]]

    X_train,X_test,Y_train,Y_test=train_test_split(X_required,Y_required,test_size=0.2,random_state=42)
    X_train,X_val,Y_train,Y_val=train_test_split(X_train,Y_train,test_size=0.2,random_state=42)

    IMG_SIZE = (50,50)

    X_train_images = []
    for p in X_train.cropped_filename:
        img = cv2.imread(p)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
        img = cv2.resize(img, IMG_SIZE)  # resize to a fixed size
        img = img_to_array(img)  # convert to numpy array
        img = preprocess_input(img)  # preprocess with ResNet preprocessing function
        X_train_images.append(img)

    X_train_images = np.array(X_train_images)

    X_val_images = []
    for p in X_val.cropped_filename:
        img = cv2.imread(p)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
        img = cv2.resize(img, IMG_SIZE)  # resize to a fixed size
        img = img_to_array(img)  # convert to numpy array
        img = preprocess_input(img)  # preprocess with ResNet preprocessing function
        X_val_images.append(img)

    X_val_images = np.array(X_val_images)

    # Load pre-trained ResNet50V2 model
    resnet = ResNet50V2(include_top=False, weights='imagenet', input_shape=(50,50,3))

    # Freeze all layers in the base model
    for layer in resnet.layers:
        layer.trainable = False

    # Add custom output layers on top of the base model
    x = resnet.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(64, activation='relu')(x)
    predictions = Dense(1, activation='linear')(x)

    # Create a new model with the custom output layers
    model = Model(inputs=resnet.input, outputs=predictions)

    model.compile(loss='mean_squared_error',
                optimizer='adam',metrics=['accuracy'])

    model.summary()
    history=model.fit(X_train_images,Y_train,epochs=10,batch_size=32,verbose=1,validation_data=(X_val_images,Y_val))
    import h5py

    model.save("model_prediction_images.h5")
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(10)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()
    return model;

def load_model4():
   
    model = load_model("model_prediction_images.h5");
    
  
    

def testing_model4(model):
    # Load the image you want to predict
    encoder=LabelEncoder()
    encoder.classes_=np.load("classes.npy", allow_pickle=True)
    class_names=encoder.classes_
    test_dir="../public/test"
    data_dir = pathlib.Path(test_dir).with_suffix('');
    # print(data_dir);
    test_paths = list(data_dir.glob('*.png'))
    # print(test_paths);
    result_list = [];

    for test_sign_path in test_paths:
        str_test_sign_path = str(test_sign_path)
        img = cv2.imread(str_test_sign_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (50,50)) # Resize the image to 50x50 pixels
        img = img_to_array(img)  # convert to numpy array
        img = np.expand_dims(img, axis=0) # Add an extra dimension for the batch size
        img = preprocess_input(img) # Add an extra dimension for the batch size
        print(img.shape)
        # Make the prediction
        prediction_score = model.predict(img)
        print(prediction_score)
        out_signal=class_names[int(prediction_score)]
        print(out_signal)
        result = {"img_path":str_test_sign_path[9:len(str_test_sign_path)], "prediction": str(out_signal), "score":str(prediction_score)};
        result_list.append(result);
    return result_list;

# training_model4();