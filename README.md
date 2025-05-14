# Image Enhancement Toolkit

A streamlit-based web application that provides various image processing functionalities using OpenCV and PIL.

## Features

- **Image Upload**: Support for JPG, JPEG, and PNG formats
- **Processing Operations**:
  - Grayscale conversion
  - Gaussian blur with adjustable kernel size
  - Edge detection with customizable thresholds
  - Binary thresholding with adjustable values
  - Brightness and contrast adjustment
  - Background removal
  - Image cropping with adjustable coordinates
- **Download**: Processed images can be downloaded in PNG format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ramez-Asaad/PixelPerfect.git
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- Python ≥ 3.12
- streamlit ≥ 1.44.1
- numpy ≥ 2.2.5
- matplotlib ≥ 3.10.1
- opencv-python ≥ 4.11.0
- pillow ≥ 11.2.1

## Usage

1. Start the Streamlit server:
   ```bash
   streamlit run v0.1/app.py
   ```

2. Open your web browser and go to the displayed URL (typically http://localhost:8501)

3. Upload an image using the file uploader in the sidebar

4. Select a processing operation and adjust parameters as needed

5. Download the processed image using the download button

## Project Structure

```
PIXELPERFECT/
├── .streamlit/
│   └── config.toml                # Streamlit configuration file
│
├── static/                        # Static assets
│   ├── ggg.jpg                    # Example/test image
│   ├── style.css                  # Custom styling
│   └── Transformation.ipynb      # Notebook for image transformations
│
├── v0.1/                          # Main application code
│   ├── app.py                     # Streamlit app entry point
│   ├── sections/                  # Functional modules
│   │   ├── __init__.py
│   │   ├── crop.py                # Image cropping functionality
│   │   ├── edit.py                # General image editing
│   │   └── remove_bg.py           # Background removal
│   │
│   └── utils/                     # Helper functions
│       ├── image_processing.py   # Image manipulation logic
│       └── utils.py              # Common utility functions
│
├── LICENSE                        # License information
├── packages.txt                   # Optional: manually listed packages
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

