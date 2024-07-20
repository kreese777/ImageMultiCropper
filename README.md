# Image Multi Cropper

Image Multi Cropper was built for my coin collecting hobby, but it was also modified to allow for annotations to be created within an image.  The tool was built with PyQt6 and allows users to crop multiple areas from a single image. Users can select crop areas using the mouse, name each crop, and save all of those cropped areas at once.  I use this functionality to crop multiple coins from an image when taking photos of coin folders.  The application also supports saving annotations in JSON and XML formats.

## Installation

### Prerequisites

- Python 3.6+
- PyQt6

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ImageMultiCropper.git
   cd ImageMultiCropper
   ```
   
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. Simply Run the application with:
   ```bash
   python main.py
   ```

## Feature Usage and Documentation

Information can also be found in the help menu or the user_guide.html file.

1. Use the **Load Image** button to load an image.

2. Toggle the **Draw Mode** button to enable drawing rectangles on the image.

3. Click and drag to draw rectangles on the image.

4. Enter a name for each rectangle when prompted.

5. Use the **Save Crops** button to save all crop areas as separate images.

6. Use the **Save JSON Annotation** and **Save XML Annotation** buttons to save annotations in JSON and XML formats, respectively.

7. Use the **Delete Rectangle** button to remove a selected rectangle from the list.

### About

This is a small application and intended more for personal use (as a coin collector) or to assist with research annotations of images.  

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Some of the code was assisted by ChatGPT.
