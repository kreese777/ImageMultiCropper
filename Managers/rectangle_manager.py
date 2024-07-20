from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtWidgets import QInputDialog, QMessageBox

class RectangleManager:
    def __init__(self, parent):
        self.parent = parent
        self.start_x = self.start_y = None
        self.current_rect = None
        self.selected_rect = None
        self.resizing = False
        self.resizing_edge = None

    def mouse_press(self, event):
        if self.parent.image is None or not self.is_within_image(event.position()):
            return  # Do nothing if no image is loaded or mouse is outside the image

        pos = event.position()
        for rect, _ in self.parent.rects:
            if self.is_near_edge(pos, rect):
                self.selected_rect = rect
                self.start_x = int(pos.x())
                self.start_y = int(pos.y())
                self.resizing = True
                return

        if event.button() == Qt.MouseButton.LeftButton:
            self.start_x = int(pos.x())
            self.start_y = int(pos.y())
            self.current_rect = QRect(self.start_x, self.start_y, 0, 0)
            self.selected_rect = None

    def mouse_move(self, event):
        if self.parent.image is None:
            return  # Do nothing if no image is loaded

        pos = event.position()
        if self.resizing and self.selected_rect is not None:
            self.resize_rectangle(pos)
            self.parent.update_image()
            return

        if self.current_rect is not None:
            self.current_rect.setWidth(int(pos.x()) - self.start_x)
            self.current_rect.setHeight(int(pos.y()) - self.start_y)
            self.parent.update_image()
            return

    def mouse_release(self, event):
        if self.parent.image is None or not self.is_within_image(event.position()):
            return  # Do nothing if no image is loaded or mouse is outside the image

        if self.resizing and self.selected_rect is not None:
            self.resizing = False
            self.selected_rect = None
            self.parent.update_image()
            return

        if event.button() == Qt.MouseButton.LeftButton and self.current_rect is not None:
            if self.is_valid_rectangle(self.current_rect):
                while True:
                    name, ok = QInputDialog.getText(self.parent, "Input", "Enter name for the crop:")
                    if not ok:
                        self.current_rect = None
                        self.parent.update_image()
                        return
                    if not self.is_duplicate_name(name):
                        break
                    QMessageBox.warning(self.parent, "Invalid Name", "The name is already in use. Please enter a unique name.")
                self.parent.rects.append((self.current_rect, name))
                self.parent.rect_list.addItem(name)
            else:
                self.parent.status_bar.showMessage("Invalid rectangle: overlaps with an existing one", 5000)
                QMessageBox.warning(self.parent, "Invalid Rectangle", "The rectangle overlaps with an existing one. Please draw a valid rectangle.")
            self.current_rect = None
            self.parent.update_image()

    def is_within_image(self, position):
        if self.parent.pixmap is None:
            return False

        image_rect = self.parent.image_label.pixmap().rect()
        return image_rect.contains(int(position.x()), int(position.y()))

    def is_near_edge(self, pos, rect):
        edge_threshold = 5
        near_left = abs(pos.x() - rect.left()) <= edge_threshold
        near_right = abs(pos.x() - rect.right()) <= edge_threshold
        near_top = abs(pos.y() - rect.top()) <= edge_threshold
        near_bottom = abs(pos.y() - rect.bottom()) <= edge_threshold

        if near_left and near_top:
            self.resizing_edge = 'top_left'
        elif near_right and near_top:
            self.resizing_edge = 'top_right'
        elif near_left and near_bottom:
            self.resizing_edge = 'bottom_left'
        elif near_right and near_bottom:
            self.resizing_edge = 'bottom_right'
        elif near_left:
            self.resizing_edge = 'left'
        elif near_right:
            self.resizing_edge = 'right'
        elif near_top:
            self.resizing_edge = 'top'
        elif near_bottom:
            self.resizing_edge = 'bottom'
        else:
            self.resizing_edge = None

        return self.resizing_edge is not None

    def resize_rectangle(self, pos):
        if self.resizing_edge == 'left':
            self.selected_rect.setLeft(int(pos.x()))
        elif self.resizing_edge == 'right':
            self.selected_rect.setRight(int(pos.x()))
        elif self.resizing_edge == 'top':
            self.selected_rect.setTop(int(pos.y()))
        elif self.resizing_edge == 'bottom':
            self.selected_rect.setBottom(int(pos.y()))
        elif self.resizing_edge == 'top_left':
            self.selected_rect.setTopLeft(QPoint(int(pos.x()), int(pos.y())))
        elif self.resizing_edge == 'top_right':
            self.selected_rect.setTopRight(QPoint(int(pos.x()), int(pos.y())))
        elif self.resizing_edge == 'bottom_left':
            self.selected_rect.setBottomLeft(QPoint(int(pos.x()), int(pos.y())))
        elif self.resizing_edge == 'bottom_right':
            self.selected_rect.setBottomRight(QPoint(int(pos.x()), int(pos.y())))

    def draw_rectangles(self, pixmap):
        painter = QPainter(pixmap)
        for index, (rect, name) in enumerate(self.parent.rects):
            if index == self.parent.selected_rect_index:
                pen = QPen(Qt.GlobalColor.blue, 3)
            else:
                pen = QPen(Qt.GlobalColor.red, 1)
            painter.setPen(pen)
            painter.drawRect(rect)
            painter.drawText(rect.topLeft() + QPoint(5, 15), name)  # Adjust the position as needed
        if self.current_rect:
            pen = QPen(Qt.GlobalColor.red, 1)
            painter.setPen(pen)
            painter.drawRect(self.current_rect)
        painter.end()

    def is_valid_rectangle(self, new_rect):
        for rect, _ in self.parent.rects:
            if rect.intersects(new_rect):
                return False
        return True

    def is_duplicate_name(self, name):
        for _, rect_name in self.parent.rects:
            if rect_name == name:
                return True
        return False
