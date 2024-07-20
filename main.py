import sys
from PyQt6.QtWidgets import QApplication
from image_cropper import ImageCropper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec())
 
