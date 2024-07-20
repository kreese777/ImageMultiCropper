import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QToolButton, QStatusBar, QApplication, QPushButton
from PyQt6.QtGui import QPixmap, QImage, QCursor
from PyQt6.QtCore import Qt, QPoint
from Managers.rectangle_list import RectangleList
from Managers.rectangle_manager import RectangleManager
from Managers.menu_manager import MenuManager
from Managers.mouse_manager import MouseManager

class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Multi Cropper")
        self.setGeometry(100, 100, 1200, 800)  # Set larger initial size

        # State variables
        self.image = None
        self.pixmap = None
        self.image_path = None
        self.rects = []  # List to store (QRect, name) tuples
        self.selected_rect_index = None
        self.drawing_mode = False  # Initial state for drawing mode
        self.last_mouse_pos = None  # To track the last mouse position for panning

        # Create RectangleManager
        self.rectangle_manager = RectangleManager(self)

        # Create menu
        self.menu_manager = MenuManager(self)

        # Create MouseManager
        self.mouse_manager = MouseManager(self)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Left layout for image and buttons
        self.left_layout = QVBoxLayout()

        # Image panel label
        self.image_panel_label = QLabel("Image Panel")
        self.left_layout.addWidget(self.image_panel_label)

        # Scroll area for image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.left_layout.addWidget(self.scroll_area)

        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label)

        # Button layout
        self.button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.menu_manager.load_image)
        self.button_layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Crops")
        self.save_button.clicked.connect(self.menu_manager.save_crops)
        self.button_layout.addWidget(self.save_button)

        self.save_json_button = QPushButton("Save JSON Annotation")
        self.save_json_button.clicked.connect(self.menu_manager.save_annotations_json)
        self.button_layout.addWidget(self.save_json_button)

        self.save_xml_button = QPushButton("Save XML Annotation")
        self.save_xml_button.clicked.connect(self.menu_manager.save_annotations_xml)
        self.button_layout.addWidget(self.save_xml_button)

        self.left_layout.addLayout(self.button_layout)

        # Toggle button for drawing mode
        self.draw_button = QToolButton()
        self.draw_button.setText("Toggle Draw Mode")
        self.draw_button.setCheckable(True)
        self.draw_button.clicked.connect(self.toggle_draw_mode)
        self.button_layout.addWidget(self.draw_button)

        # Add left layout to the main layout
        self.main_layout.addLayout(self.left_layout, 4)  # Give more weight to the image panel

        # Right layout for the list and delete button
        self.right_layout = QVBoxLayout()

        # Rectangle list panel label
        self.rect_list_label = QLabel("Rectangle List")
        self.right_layout.addWidget(self.rect_list_label)

        self.rect_list = RectangleList(self)
        self.right_layout.addWidget(self.rect_list)

        self.delete_button = QPushButton("Delete Rectangle")
        self.delete_button.clicked.connect(self.rect_list.delete_rectangle)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet(self.rect_list.get_delete_button_stylesheet(False))
        self.rect_list.set_delete_button(self.delete_button)
        self.right_layout.addWidget(self.delete_button)

        # Add right layout to the main layout
        self.main_layout.addLayout(self.right_layout, 1)  # Give less weight to the list panel

        # Connect mouse events
        self.image_label.mousePressEvent = self.mouse_manager.mouse_press
        self.image_label.mouseMoveEvent = self.mouse_manager.mouse_move
        self.image_label.mouseReleaseEvent = self.mouse_manager.mouse_release

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def update_image(self):
        if self.pixmap:
            temp_pixmap = self.pixmap.copy()
            self.rectangle_manager.draw_rectangles(temp_pixmap)
            self.image_label.setPixmap(temp_pixmap)

    def select_rectangle(self, index):
        self.selected_rect_index = index
        self.update_image()

    def toggle_draw_mode(self):
        self.drawing_mode = not self.drawing_mode
        if self.drawing_mode:
            self.scroll_area.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        else:
            self.scroll_area.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
