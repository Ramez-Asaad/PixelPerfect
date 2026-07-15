import os
import glob
from removebg import RemoveBg

def batch_remove_background(input_folder, output_folder, api_key):
    """
    Removes the background from all images in the input_folder and 
    saves them to the output_folder using the removebg library.
    """
    # Initialize the RemoveBg API client
    rmbg = RemoveBg(api_key, "error.log")
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # Supported image extensions
    extensions = ('*.jpg', '*.jpeg', '*.png')
    image_paths = []
    
    # Gather all images in the input folder
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))
        # Also check uppercase extensions
        image_paths.extend(glob.glob(os.path.join(input_folder, ext.upper())))
        
    if not image_paths:
        print(f"No images found in {input_folder}")
        return

    print(f"Found {len(image_paths)} images. Starting background removal...")
    
    for img_path in image_paths:
        filename = os.path.basename(img_path)
        print(f"Processing: {filename}")
        
        try:
            # removebg saves the file in the same directory by default with _no_bg.png postfix
            # We will move it to the output folder
            rmbg.remove_background_from_img_file(img_path)
            
            # Find the newly created file (removebg adds "_no_bg.png" to the original filename without extension)
            base_name = os.path.splitext(filename)[0]
            new_file_name = f"{base_name}_no_bg.png"
            source_new_file = os.path.join(input_folder, new_file_name)
            target_new_file = os.path.join(output_folder, new_file_name)
            
            if os.path.exists(source_new_file):
                # Move to the output folder
                os.replace(source_new_file, target_new_file)
                print(f"Successfully saved to: {target_new_file}")
            else:
                print(f"Failed to find processed file for: {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print("Batch processing complete!")

if __name__ == "__main__":
    # Setup your environment here
    API_KEY = "YOUR_REMOVE_BG_API_KEY" # Replace with your actual remove.bg API key
    INPUT_DIR = "input_images"         # Folder containing your original images
    OUTPUT_DIR = "output_images"       # Folder where processed images will be saved
    
    # Create input folder for convenience if it doesn't exist
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Created {INPUT_DIR} folder. Please put your images there and run the script again.")
    elif API_KEY == "YOUR_REMOVE_BG_API_KEY":
        print("Please edit the script and set your API_KEY first!")
    else:
        batch_remove_background(INPUT_DIR, OUTPUT_DIR, API_KEY)
