from PyQt6.QtWidgets import QListWidget, QPushButton

class RectangleList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.delete_button = None  # Reference to the delete button

    def set_delete_button(self, delete_button):
        self.delete_button = delete_button
        self.itemSelectionChanged.connect(self.update_delete_button_state)

    def update_delete_button_state(self):
        if self.currentRow() != -1:
            self.delete_button.setEnabled(True)
            self.delete_button.setStyleSheet(self.get_delete_button_stylesheet(True))
        else:
            self.delete_button.setEnabled(False)
            self.delete_button.setStyleSheet(self.get_delete_button_stylesheet(False))

    def delete_rectangle(self):
        current_row = self.currentRow()
        if current_row != -1:
            self.takeItem(current_row)
            del self.parent.rects[current_row]
            self.clearSelection()  # Clear the selection
            self.parent.selected_rect_index = None
            self.parent.update_image()

    def get_delete_button_stylesheet(self, enabled):
        if enabled:
            return """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #dcdcdc;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #dcdcdc;
                    border: 1px solid #c0c0c0;
                    color: #a0a0a0;
                }
            """
