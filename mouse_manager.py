from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class MouseManager:
    def __init__(self, parent):
        self.parent = parent

    def mouse_press(self, event):
        if self.parent.drawing_mode:
            self.parent.rectangle_manager.mouse_press(event)
        else:
            self.parent.scroll_area.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            self.parent.last_mouse_pos = event.position()
            event.accept()

    def mouse_move(self, event):
        if self.parent.drawing_mode:
            self.parent.rectangle_manager.mouse_move(event)
        else:
            if event.buttons() & Qt.MouseButton.LeftButton:
                self.parent.scroll_area.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
                if self.parent.last_mouse_pos:
                    delta = event.position() - self.parent.last_mouse_pos
                    self.parent.scroll_area.horizontalScrollBar().setValue(self.parent.scroll_area.horizontalScrollBar().value() - int(delta.x()))
                    self.parent.scroll_area.verticalScrollBar().setValue(self.parent.scroll_area.verticalScrollBar().value() - int(delta.y()))
                    self.parent.last_mouse_pos = event.position()
                event.accept()
            else:
                self.parent.scroll_area.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouse_release(self, event):
        if self.parent.drawing_mode:
            self.parent.rectangle_manager.mouse_release(event)
        else:
            self.parent.scroll_area.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.parent.last_mouse_pos = None
            event.accept()
