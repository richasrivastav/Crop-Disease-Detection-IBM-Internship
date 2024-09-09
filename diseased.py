import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import tensorflow as tf
import cv2

def app():
    # Custom CSS for styling
    st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #f7f7f7;
                padding: 20px;
            }
            .stFileUploader label {
                color: #28a745; /* Green color for label */
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 20px;
                text-align: center;
            }
            .stImage img {
                width: 100%; /* Make the uploaded image width match the file uploader width */
            }
            .stButton>button {
                background-color: #95BF44; 
                color: white;
                border-radius: 25px;
                font-size: 18px;
                padding: 12px;
                width: 100%;
                border: none;
                margin: 10px;
                transition: background-color 0.3s ease, transform 0.2s ease;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #4B5A31; /* Darker green on hover */
                transform: scale(1.05);
            }
            .stButton>button:active {
                background-color: #1e7e34; /* Even darker green on click */
                transform: scale(0.95);
            }
        </style>
    """, unsafe_allow_html=True)

    # Upload Image section
    st.header("Upload Image for Disease Detection")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load and display the uploaded image
        uploaded_image = Image.open(uploaded_file)

        # Initialize session state variables if not already present
        if 'original_image' not in st.session_state:
            st.session_state.original_image = uploaded_image
            st.session_state.current_image = uploaded_image
            st.session_state.show_enhanced = False
            st.session_state.show_segmented = False
            st.session_state.enhanced_image = None
            st.session_state.segmented_image = None

        # Display images based on the current state
        if st.session_state.show_enhanced and st.session_state.enhanced_image is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.original_image, caption="Original Image", use_column_width=True)
            with col2:
                st.image(st.session_state.enhanced_image, caption="Enhanced Image", use_column_width=True)
        elif st.session_state.show_segmented and st.session_state.segmented_image is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.original_image, caption="Original Image", use_column_width=True)
            with col2:
                st.image(st.session_state.segmented_image, caption="Segmented Image", use_column_width=True)
                st.write(f"Diseased Area: {st.session_state.diseased_area_cm2:.2f} cm²")
                st.write(f"Disease Percentage: {st.session_state.disease_percentage:.2f}%")
        else:
            st.image(st.session_state.current_image, caption="Current Image", use_column_width=True)

        # Automatically show disease detection after upload
        result_index = show_about_disease(uploaded_file)
        class_name = [
            'Bacterial Leaf Blight',
            'Brown Spot',
            'Healthy Rice Leaf',
            'Leaf Blast',
        ]

        # Display disease detection results
        st.markdown(f"### Detected Disease: {class_name[result_index]}")
        show_recommendations_and_treatment(result_index)

        # Display remaining buttons horizontally with spacing
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Enhance Image"):
                st.session_state.enhanced_image = enhance_image(st.session_state.original_image)
                st.session_state.show_enhanced = True
                st.session_state.current_image = st.session_state.enhanced_image
                st.session_state.show_segmented = False

        with col2:
            if st.button("Segment Image"):
                (st.session_state.segmented_image,
                 st.session_state.disease_percentage,
                 st.session_state.diseased_area_cm2) = segment_image(st.session_state.current_image)
                st.session_state.show_segmented = True
                st.session_state.show_enhanced = False

        with col3:
            if st.button("Reset"):
                reset_state()

        with col4:
            if st.button("Exit"):
                st.write("Exiting disease detection mode.")
                st.stop()

def show_about_disease(test_image):
    model = tf.keras.models.load_model('trained_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=[128, 128])
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

def show_recommendations_and_treatment(disease_index):
    recommendations = {
        0: ("Bacterial Leaf Blight", 
            "### Bacterial Leaf Blight\n\n"
            "#### Symptoms:\n"
            "- Grayish-green streaks on leaves\n"
            "- Yellowing and wilting of leaves\n"
            "- Mily ooze drops from leaves\n\n"
            "#### Recommended Treatment:\n"
            "- Apply copper-based fungicides\n"
            "- Manage water levels\n"
            "- Remove infected plant debris\n\n"
            "#### Action Based on Infection Percentage:\n"
            f"- **If infection is around 20%:** Monitor closely and continue with fungicide application. Improve field drainage and avoid overhead irrigation.\n"
            f"- **If infection is around 50%:** Increase fungicide application frequency. Consider using bactericides if the situation worsens. Improve crop rotation and field sanitation.\n"
            f"- **If infection exceeds 70%:** Immediate intervention is required. Remove heavily infected plants and apply a stronger treatment. Seek advice from an agricultural expert and consider replanting if necessary.\n\n"
            "This disease can severely impact yield if not managed effectively. Regular monitoring and prompt action are key."
        ),
        1: ("Brown Spot", 
            "### Brown Spot\n\n"
            "#### Symptoms:\n"
            "- Dark brown, round spots with yellow halos\n"
            "- Small, dark lesions on the leaves\n\n"
            "#### Recommended Treatment:\n"
            "- Ensure adequate soil nutrients\n"
            "- Apply appropriate fungicides\n"
            "- Rotate crops and avoid excess nitrogen\n\n"
            "#### Action Based on Infection Percentage:\n"
            f"- **If infection is around 20%:** Continue with routine fungicide application. Ensure proper nutrient management and avoid excess watering.\n"
            f"- **If infection is around 50%:** Increase fungicide frequency and consider using a combination of treatments. Improve soil management and crop rotation practices.\n"
            f"- **If infection exceeds 70%:** Extensive control measures are needed. Remove infected plants and apply stronger fungicides. Reassess soil and nutrient management practices.\n\n"
            "Managing Brown Spot effectively requires proactive measures and regular monitoring to prevent extensive damage."
        ),
        2: ("Healthy Rice Leaf", 
            "### Healthy Rice Leaf\n\n"
            "#### Status:\n"
            "- No treatment required\n\n"
            "#### Observations:\n"
            "- The leaf appears healthy and free of disease.\n\n"
            "#### Recommendations:\n"
            "- Continue regular monitoring of the crop.\n"
            "- Maintain good field hygiene and proper agronomic practices to prevent future infections.\n\n"
            "Keeping your crop healthy through preventive measures will help avoid potential disease outbreaks."
        ),
        3: ("Leaf Blast", 
            "### Leaf Blast\n\n"
            "#### Symptoms:\n"
            "- Water-soaked lesions on leaves\n"
            "- Lesions with gray centers and dark brown margins\n\n"
            "#### Recommended Treatment:\n"
            "- Apply systemic fungicides\n"
            "- Ensure good field hygiene\n"
            "- Avoid high nitrogen fertilization\n\n"
            "#### Action Based on Infection Percentage:\n"
            f"- **If infection is around 20%:** Monitor closely and apply fungicides as a preventive measure. Improve field sanitation and manage water levels.\n"
            f"- **If infection is around 50%:** Increase fungicide application frequency and consider additional treatments. Enhance field hygiene practices and adjust fertilization strategies.\n"
            f"- **If infection exceeds 70%:** Take immediate action. Remove severely infected plants and apply stronger fungicides. Consult with experts for advanced treatment options and consider replanting if necessary.\n\n"
            "Leaf Blast can cause significant damage if not addressed promptly. Effective management involves both preventive and reactive measures."
        ),
    }
    
    
    if disease_index in recommendations:
        disease_name, treatment = recommendations[disease_index]
        st.write(f"### Recommended Treatment for {disease_name}:")
        st.write(treatment)
    else:
        st.write("### No specific treatment is required for this condition.")

def enhance_image(image):
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(src=image_cv, ddepth=-1, kernel=kernel)
    
    pil_image = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    
    contrast_enhancer = ImageEnhance.Contrast(pil_image)
    enhanced_image = contrast_enhancer.enhance(1.5)  
    brightness_enhancer = ImageEnhance.Brightness(enhanced_image)
    final_image = brightness_enhancer.enhance(1.2)  
    
    return final_image

def segment_image(uploaded_image):
    # Convert the uploaded image from RGB to BGR and resize
    original_img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    # original_img = cv2.resize(original_img, (400, 400))
    
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_img = cv2.filter2D(src=original_img, ddepth=-1, kernel=kernel)
    
    pil_img = Image.fromarray(cv2.cvtColor(sharpened_img, cv2.COLOR_BGR2RGB))
    contrast_enhancer = ImageEnhance.Contrast(pil_img)
    enhanced_img = contrast_enhancer.enhance(1.5)
    brightness_enhancer = ImageEnhance.Brightness(enhanced_img)
    final_pil_img = brightness_enhancer.enhance(1.2)
    final_img = cv2.cvtColor(np.array(final_pil_img), cv2.COLOR_RGB2BGR)
    
    hsv_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 0])
    upper_bound = np.array([25, 255, 255])
    mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
    result = cv2.bitwise_and(final_img, final_img, mask=mask)
    
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    gray_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
    _, leaf_mask = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY_INV)
    

    disease_mask = cv2.bitwise_and(mask, mask, mask=leaf_mask)
    
    leaf_area_pixels = cv2.countNonZero(leaf_mask)
    diseased_area_pixels = cv2.countNonZero(disease_mask)
    
    disease_percentage = (diseased_area_pixels / leaf_area_pixels) * 100 if leaf_area_pixels != 0 else 0
    
    diseased_area_cm2 = diseased_area_pixels * 0.01




    
    
    return Image.fromarray(result_rgb), disease_percentage, diseased_area_cm2

def reset_state():
    st.session_state.clear()
    st.session_state.show_enhanced = False
    st.session_state.show_segmented = False
    st.session_state.enhanced_image = None
    st.session_state.segmented_image = None
    

if __name__ == "__main__":
    app()
