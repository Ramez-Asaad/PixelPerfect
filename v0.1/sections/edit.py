import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
from utils.image_processing import process_image
from utils.utils import pil_to_bytes, bytes_to_pil
from sections.crop import crop_page
from sections.remove_bg import remove_bg_page

lottie_animation = "https://lottiefiles.com/animation/ai-image-tool-12999495"  # Placeholder for Lottie animation

def edit_page():
    st.title("🖼️ Image Editor")

    # Add a "Clear Image" button to reset the uploaded image
    if st.button("🗑️ Clear Image", key='clear-edit'):
        st.session_state.image_bytes = None
        st.session_state.refresh = True

    if st.session_state.image_bytes is None:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.session_state.image_bytes = pil_to_bytes(image)
            # Instead of st.experimental_rerun(), rely on Streamlit's reactivity
            st.session_state.refresh = True
    else:
        image = bytes_to_pil(st.session_state.image_bytes)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✂️ Go to Cropping"):
            st.session_state.current_page = "crop"
    with col2:
        if st.button("🧹 Remove Background"):
            st.session_state.current_page = "remove_bg"
    with col3:
        if st.button("🔄 Reset Edits"):
            st.session_state.image_bytes = pil_to_bytes(image)
            st.experimental_set_query_params(refresh="true")
            
    if st.session_state.current_page == "crop":
        with st.spinner("Loading cropping page..."):
            crop_page()
            st.success("Page loaded!")
            st.stop()
    elif st.session_state.current_page == "remove_bg":
        with st.spinner("loading background removal page..."):
            remove_bg_page()
            st.stop()
    

    # File uploader at the top
    if st.session_state.image_bytes is not None:
        img_array = np.array(image)
    
        # Operation selection
        operation = st.selectbox(
        "Select Operation", 
        ["Grayscale", "Blur", "Edge Detection", "Threshold", "Color Adjustment", "Log Transform", "Negative", "Piecewise", "Power Law"],
        help="Choose an operation to apply to the image",
        index=0
        )
    
        # Parameters in expandable section
        with st.expander("Adjustment Parameters", expanded=True):
            params = {}
            if operation == "Blur":
                params["kernel_size"] = st.slider(
                    "Blur Amount", 1, 31, 5, step=2,
                    help="Higher values create more blur"
                )
            elif operation == "Edge Detection":
                col1, col2 = st.columns(2)
                with col1:
                    params["threshold1"] = st.slider(
                        "Threshold 1", 0, 300, 100,
                        help="First threshold for the hysteresis procedure"
                    )
                with col2:
                    params["threshold2"] = st.slider(
                        "Threshold 2", 0, 300, 200,
                        help="Second threshold for the hysteresis procedure"
                    )
            elif operation == "Threshold":
                params["thresh_value"] = st.slider(
                    "Threshold Value", 0, 255, 127,
                    help="Pixel values above this will be white, below will be black"
                )
            elif operation == "Color Adjustment":
                col1, col2 = st.columns(2)
                with col1:
                    params["brightness"] = st.slider(
                        "Brightness", -100, 100, 0,
                        help="Adjust image brightness"
                    )
                with col2:
                    params["contrast"] = st.slider(
                        "Contrast", 0.0, 3.0, 1.0, 0.1,
                        help="Adjust image contrast"
                    )
            elif operation == "Log Transform":
                params["c"] = st.slider(
                    "Constant (c)", 1.0, 10.0, 2.0, 0.1,
                    help="Constant for log transformation"
                )
            elif operation == "Negative":
                pass
            elif operation == "Piecewise":
                help=("ℹ️Piecewise linear transformation enhances image contrast by applying different linear mappings to pixel intensity ranges.")
                st.markdown("""
                The transformation is divided into three parts:
                - Intensities below **r1** are scaled from 0 to **s1**.
                - Intensities between **r1** and **r2** are stretched from **s1** to **s2**.
                - Intensities above **r2** are scaled from **s2** to 255.
                
                This helps improve details in specific brightness regions of the image.
                """)
                col1, col2 = st.columns(2)
                with col1:
                    r1 = st.slider("r1", min_value=0, max_value=255, value=70, help="**r1, r2**: These are intensity thresholds in the input image. They define regions of interest.")
                    r2 = st.slider("r2", min_value=0, max_value=255, value=150, help="**r1, r2**: These are intensity thresholds in the input image. They define regions of interest.")



                with col2:
                    s1 = st.slider("s1", min_value=0, max_value=255, value=50)
                    s2 = st.slider("s2", min_value=0, max_value=255, value=200)
                params["r_vals"] = [0, r1, r2, 255]
                params["s_vals"] = [0, s1, s2, 255]
            elif operation == "Power Law":
                params["gamma"] = st.slider(
                    "Gamma", 0.1, 5.0, 1.0, 0.1,
                    help="Adjust the gamma value for power law transformation"
                )
        # Process image
        operation_map = {
        "Grayscale": "grayscale",
        "Blur": "blur",
        "Edge Detection": "edges",
        "Threshold": "threshold",
        "Color Adjustment": "color_adjust",
        "Log Transform": "log_transform",
        "Negative": "negative",
        "Piecewise": "piecewise",
        "Power Law": "power_law"
        }
    
        
    
        # Display images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(image)
    
        with col2:
            st.subheader("Processed Image")
            with st.spinner("Processing..."):
                processed_image = process_image(img_array, operation_map[operation], params)
            st.image(processed_image)
            st.success("Processing complete!")

    
        # Download button9
        if isinstance(processed_image, np.ndarray):
            if len(processed_image.shape) == 2:
                pil_img = Image.fromarray(processed_image)
            else:
                pil_img = Image.fromarray(processed_image)
        
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            byte_img = buf.getvalue()
        
            st.download_button(
                label="Download Processed Image",
                data=byte_img,
                file_name=f"processed_{operation.lower().replace(' ', '_')}.png",
                mime="image/png",
            )
    else:
        st.info("Please upload an image to begin editing.")
        

