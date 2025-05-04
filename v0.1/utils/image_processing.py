import cv2
import numpy as np
import streamlit as st

def process_image(img_array, operation_type, params=None):
        if operation_type == "grayscale":
            return cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        elif operation_type == "blur":
            kernel_size = params.get("kernel_size", 5)
            return cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)
        elif operation_type == "edges":
            threshold1 = params.get("threshold1", 100)
            threshold2 = params.get("threshold2", 200)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            return cv2.Canny(gray, threshold1, threshold2)
        elif operation_type == "threshold":
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            thresh_value = params.get("thresh_value", 127)
            _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
            return binary
        elif operation_type == "color_adjust":
            brightness = params.get("brightness", 0)
            contrast = params.get("contrast", 1)
            return cv2.convertScaleAbs(img_array, alpha=contrast, beta=brightness)
        elif operation_type == "log_transform":
            
            c = 255 / np.log(1 + np.max(img_array))
            img_array = c * (np.log(img_array + 1))
            img_array = np.array(np.clip(img_array, 0, 255), dtype=np.uint8)
            return img_array
        elif operation_type == "negative":
            return 255 - img_array
        elif operation_type == "piecewise":
            # Default piecewise mapping: identity (no change)
            r_vals = np.array(params.get("r_vals", [0, 70, 150, 255]), dtype=np.uint8)
            s_vals = np.array(params.get("s_vals", [0, 50, 200, 255]), dtype=np.uint8)

            # Ensure correct shape and clipping
            r_vals = np.clip(r_vals, 0, 255)
            s_vals = np.clip(s_vals, 0, 255)

            # Apply interpolation separately for grayscale or each channel
            if len(img_array.shape) == 2:  # Grayscale
                flat = img_array.flatten()
                mapped = np.interp(flat, r_vals, s_vals)
                result = mapped.reshape(img_array.shape).astype(np.uint8)
            else:  # Color image: apply to each channel
                result = np.zeros_like(img_array)
                for c in range(img_array.shape[2]):
                    flat = img_array[:, :, c].flatten()
                    mapped = np.interp(flat, r_vals, s_vals)
                    result[:, :, c] = mapped.reshape(img_array.shape[:2]).astype(np.uint8)

            return result
        elif operation_type == "power_law":
            gamma = params.get("gamma", 1.0)
            normalized_img = img_array / 255.0
            img_array = np.power(normalized_img, gamma)
            img_array = (img_array * 255).astype(np.uint8)
            return img_array
        elif operation_type == "graylevel_slicing":
            """Apply gray-level slicing to an image."""
            low_threshold = params.get("low_threshold", 100)
            high_threshold = params.get("high_threshold", 200)
            img_array = np.where((img_array >= low_threshold) & (img_array <= high_threshold), 255, 0).astype(np.uint8)
            return img_array
        elif operation_type == "log_transform":
            """Apply logarithmic transformation to an image."""
            c = 255 / np.log(1 + np.max(img_array))
            img_array = c * (np.log(img_array + 1))
            img_array = np.array(np.clip(img_array, 0, 255), dtype=np.uint8)
            return img_array
        elif operation_type=="watershed_segmentation":
            """Apply watershed segmentation to an image."""
            # Convert to grayscale and blur
            kernel_size = params.get("kernel_size", 5)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
            
            # Apply Otsu's thresholding
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Noise removal with morphological operations
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # Sure background area
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            
            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            sure_fg = np.uint8(sure_fg)
            
            # Finding unknown region
            unknown = cv2.subtract(sure_bg, sure_fg)
            
            # Marker labelling
            _, markers = cv2.connectedComponents(sure_fg)
            markers += 1  # Add one to all labels so that background is 1, not 0
            markers[unknown == 255] = 0  # Mark the unknown region with 0
            
            # Apply watershed
            markers = cv2.watershed(img_array.copy(), markers)
            
            # Create a color visualization of the markers
            result = img_array.copy()
            result[markers == -1] = [0, 0, 255]  # Mark boundaries in red
            
            return result
        elif operation_type == "adaptive_threshold": 
            """Apply adaptive thresholding to an image."""
            block_size = params.get("block_size", 11)
            c_value = params.get("c_value", 2)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, block_size, c_value
            )
            return cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2RGB)      
        return img_array
    