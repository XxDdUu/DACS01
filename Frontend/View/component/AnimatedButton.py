from PyQt6.QtWidgets import QPushButton, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class AnimatedButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.setMouseTracking(True)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(0.6)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().leaveEvent(event)