from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

class LoadingScreen(QWidget):
    def __init__(self, gif_path):
        super().__init__()

        # Load the gif and get its size
        movie = QMovie(gif_path)
        movie.jumpToFrame(0)
        movie.start()
        size = movie.currentPixmap().size()

        # Set the window size based on the gif size
        self.setFixedSize(size.width(), size.height())
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove spacing

        label_animation = QLabel()
        label_animation.setMovie(movie)
        layout.addWidget(label_animation, alignment=Qt.AlignCenter)

        self.movie = movie  # Save reference to the movie object

    def closeEvent(self, event):
        event.ignore()  # Ignore the close event to prevent closing the loading screen

    def closeLoadingScreen(self):
        self.close()  # Close the loading screen manually

    def stopAnimation(self):
        self.movie.stop()  # Stop the animation manually
