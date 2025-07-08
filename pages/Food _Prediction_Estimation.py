import streamlit as st
import os
import sys
import cv2
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.image import img_to_array  # type: ignore
from utils.auth_utils import require_login

@ require_login
def main_app():
    st.sidebar.header("Scan your food!")
    st.sidebar.write("Upload an image and see the predicted food class.")
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    
    model = load_model(os.path.join(os.getcwd(), "models", "food_classification_model.h5"))
    food_classes = ["apple_pie", "donuts", "dumplings", "edamame", "gyoza", "ice_cream", "pancakes", "pizza", "ramen", "sushi", "waffles"]
    if picture:
        # To read image file buffer with OpenCV:
        bytes_data = picture.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # Validate cv2_img
        if cv2_img is None:
            st.error("Failed to decode the image. Please try again.")
        else:
            # Check the type and shape of cv2_img
            #st.write(type(cv2_img))  # Should output: <class 'numpy.ndarray'>
            st.write(f"Original dimension of image {cv2_img.shape}")  # Should output: (height, width, channels)
            
            # Resize the image to match the model's input size
            target_size = (224, 224)  # Example target size
            resized_img = cv2.resize(cv2_img, target_size, interpolation=cv2.INTER_AREA)
            
            # Check the resized image
            st.write(f"After image processing {resized_img.shape}")  # Should output: (224, 224, channels)
            
            # Pass the resized image to the classification function
            predicted_food = real_time_food_classification(model, food_classes, resized_img)



# Preprocess the image to match the model's input requirements
def preprocess_frame(frame, target_size=(224, 224)):
    frame_resized = cv2.resize(frame, target_size)  # Resize frame
    frame_array = img_to_array(frame_resized)  # Convert to array
    frame_array = frame_array / 255.0  # Normalize pixel values
    return np.expand_dims(frame_array, axis=0)  # Add batch dimension

# Real-time food classification using webcam
def real_time_food_classification(model, food_classes, picture):
    cap = cv2.VideoCapture(0)  # Open webcam (0 is the default camera)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # Preprocess the frame
    preprocessed_frame = preprocess_frame(picture)
    
    # Predict the food class
    predictions = model.predict(preprocessed_frame)
    class_idx = np.argmax(predictions)
    predicted_class = food_classes[class_idx]

    # Convert the image from BGR (OpenCV format) to RGB (Streamlit format)
    picture_rgb = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

    # Display the image with the prediction in Streamlit
    st.image(picture_rgb, caption="Real-Time Food Classification", use_container_width=True)

    # Print the predicted class below the image
    st.write(f"**Prediction:** {predicted_class}")
    
    # Show the frame
    cv2.imshow("Real-Time Food Classification", picture)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    
    # clean up the class
    predicted_class = predicted_class.replace("_", " ")
    # add a value of 1 in front of the predicted class
    predicted_class = "1 " + predicted_class
    return predicted_class


main_app()