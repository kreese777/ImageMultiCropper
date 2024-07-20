from PyQt6.QtWidgets import QMenuBar, QApplication, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QDialogButtonBox, QScrollArea, QTextBrowser
from PyQt6.QtGui import QAction, QImage, QPixmap
from PyQt6.QtCore import Qt
import os
import datetime
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

class MenuManager:
    def __init__(self, parent):
        self.parent = parent
        self.menubar = QMenuBar(parent)
        self.create_menu()

    def create_menu(self):
        # File menu
        file_menu = self.menubar.addMenu('File')

        load_action = QAction('Load Image', self.parent)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        save_action = QAction('Save Crops', self.parent)
        save_action.triggered.connect(self.save_crops)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction('Quit', self.parent)
        quit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(quit_action)

        # Annotate menu
        annotate_menu = self.menubar.addMenu('Annotate')

        save_annotations_action = QAction('Save JSON Annotations', self.parent)
        save_annotations_action.triggered.connect(self.save_annotations_json)
        annotate_menu.addAction(save_annotations_action)

        save_annotations_xml_action = QAction('Save XML Annotations', self.parent)
        save_annotations_xml_action.triggered.connect(self.save_annotations_xml)
        annotate_menu.addAction(save_annotations_xml_action)

        # Help menu
        help_menu = self.menubar.addMenu('Help')

        user_guide_action = QAction('User Guide', self.parent)
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)

        about_action = QAction('About', self.parent)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.parent.setMenuBar(self.menubar)

    def show_about(self):
        current_year = datetime.datetime.now().year
        years = "2024" if current_year == 2024 else f"2024-{current_year}"
        
        about_dialog = QDialog(self.parent)
        about_dialog.setWindowTitle("About Image Multi Cropper")
        
        layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_pixmap = self.resize_pixmap(logo_pixmap, 240)
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label)
        
        # Text
        text_layout = QVBoxLayout()
        
        app_info = QLabel(f"<b>Image Multi Cropper</b> v1.0<br>Copyright {years} Kristopher Reese")
        text_layout.addWidget(app_info)
        
        license_info = QLabel('<a href="https://www.gnu.org/licenses/gpl-3.0.html">GPLv3 License</a>')
        license_info.setOpenExternalLinks(True)
        text_layout.addWidget(license_info)
        
        layout.addLayout(text_layout)
        
        about_dialog.setLayout(layout)
        about_dialog.exec()

    def show_user_guide(self):
        user_guide_dialog = QDialog(self.parent)
        user_guide_dialog.setWindowTitle("Image Multi Cropper User Guide")
        user_guide_dialog.resize(800, 600)  # Set initial size of the dialog
        
        layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        text_browser = QTextBrowser()
        text_browser.setHtml(open("user_guide.html").read())
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_browser)
        
        layout.addWidget(scroll_area)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(user_guide_dialog.accept)
        layout.addWidget(button_box)
        
        user_guide_dialog.setLayout(layout)
        user_guide_dialog.exec()

    def resize_pixmap(self, pixmap, width):
        aspect_ratio = width / pixmap.width()
        height = int(pixmap.height() * aspect_ratio)
        return pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.parent.image = QImage(file_name)
            self.parent.pixmap = QPixmap.fromImage(self.parent.image)
            self.parent.image_label.setPixmap(self.parent.pixmap)
            self.parent.rects = []  # Reset the list of rectangles
            self.parent.rect_list.clear()
            self.parent.selected_rect_index = None
            self.parent.image_path = file_name  # Store the image path
            self.parent.update_image()
            self.parent.status_bar.showMessage("Image loaded successfully", 5000)  # Show message for 5 seconds

    def save_crops(self):
        if not self.parent.rects or self.parent.image is None:
            return

        output_dir = os.path.join(os.getcwd(), "cropped_images")
        os.makedirs(output_dir, exist_ok=True)

        for rect, name in self.parent.rects:
            cropped_image = self.parent.image.copy(rect)
            file_path = os.path.join(output_dir, f"{name}.png")
            cropped_image.save(file_path)
        self.parent.status_bar.showMessage(f"All crops saved to {output_dir}", 5000)  # Show message for 5 seconds

    def save_annotations_json(self):
        if not self.parent.rects or self.parent.image is None:
            return

        annotations = {
            'image_path': self.parent.image_path,
            'rectangles': [
                {'name': name, 'x': rect.x(), 'y': rect.y(), 'width': rect.width(), 'height': rect.height()}
                for rect, name in self.parent.rects
            ]
        }

        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Annotations", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(annotations, f, indent=4)
            self.parent.status_bar.showMessage(f"Annotations saved to {file_name}", 5000)  # Show message for 5 seconds

    def save_annotations_xml(self):
        if not self.parent.rects or self.parent.image is None:
            return

        annotations = ET.Element('annotations')
        image_path = ET.SubElement(annotations, 'image_path')
        image_path.text = self.parent.image_path

        rectangles = ET.SubElement(annotations, 'rectangles')
        for rect, name in self.parent.rects:
            rect_elem = ET.SubElement(rectangles, 'rectangle')
            ET.SubElement(rect_elem, 'name').text = name
            ET.SubElement(rect_elem, 'x').text = str(rect.x())
            ET.SubElement(rect_elem, 'y').text = str(rect.y())
            ET.SubElement(rect_elem, 'width').text = str(rect.width())
            ET.SubElement(rect_elem, 'height').text = str(rect.height())

        tree = ET.ElementTree(annotations)
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Annotations", "", "XML Files (*.xml)")
        if file_name:
            # Pretty-print the XML
            xml_str = ET.tostring(annotations, encoding='utf-8')
            parsed_xml = minidom.parseString(xml_str)
            pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

            with open(file_name, 'w') as f:
                f.write(pretty_xml_str)
            self.parent.status_bar.showMessage(f"Annotations saved to {file_name}", 5000)  # Show message for 5 seconds
