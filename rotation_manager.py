from PyQt6.QtGui import QTransform, QPixmap
from PyQt6.QtCore import Qt

class RotationManager:
    def __init__(self, parent):
        self.parent = parent
        self.current_angle = 0
        self.rotated_pixmap = None  # Store the rotated pixmap

    def rotate_image(self, angle):
        self.current_angle = angle
        self.apply_rotation()

    def apply_rotation(self):
        if self.parent.pixmap:
            transform = QTransform().rotate(self.current_angle)
            self.rotated_pixmap = self.parent.pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.parent.image_label.setPixmap(self.rotated_pixmap)
            self.parent.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.parent.image_label.repaint()  # Force repaint
