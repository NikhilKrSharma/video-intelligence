import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QHBoxLayout, 
    QVBoxLayout, 
    QFileDialog, 
    QSlider, 
    QLabel, 
    QMessageBox, 
    QLineEdit
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dual Video Player')
        self.setGeometry(100, 100, 1200, 600)

        # Create layouts
        main_layout = QVBoxLayout()
        video_layout = QHBoxLayout()
        control_layout = QHBoxLayout()
        speed_layout = QHBoxLayout()

        # Create video labels
        self.video_label1 = QLabel(self)
        self.video_label2 = QLabel(self)
        self.video_label1.setMinimumSize(400, 300)
        self.video_label2.setMinimumSize(400, 300)
        video_layout.addWidget(self.video_label1)
        video_layout.addWidget(self.video_label2)

        # Create buttons
        self.select_button1 = QPushButton('Select Video 1', self)
        self.select_button2 = QPushButton('Select Video 2', self)
        self.play_pause_button = QPushButton('Play', self)

        # Create speed control
        self.speed_input = QLineEdit(self)
        self.speed_input.setPlaceholderText("Enter speed (e.g. 1.5)")
        self.set_speed_button = QPushButton('Set Speed', self)
        speed_layout.addWidget(self.speed_input)
        speed_layout.addWidget(self.set_speed_button)

        # Create slider
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 1000)

        # Add widgets to control layout
        control_layout.addWidget(self.select_button1)
        control_layout.addWidget(self.select_button2)
        control_layout.addWidget(self.play_pause_button)
        control_layout.addLayout(speed_layout)

        # Add layouts to main layout
        main_layout.addLayout(video_layout)
        main_layout.addWidget(self.seek_slider)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

        # Connect buttons to functions
        self.select_button1.clicked.connect(lambda: self.select_video(1))
        self.select_button2.clicked.connect(lambda: self.select_video(2))
        self.play_pause_button.clicked.connect(self.play_pause)
        self.set_speed_button.clicked.connect(self.set_speed)
        self.seek_slider.sliderMoved.connect(self.seek)

        # Initialize variables
        self.video1 = None
        self.video2 = None
        self.is_playing = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.current_speed = 1.0

        # Disable buttons initially
        self.play_pause_button.setEnabled(False)
        self.set_speed_button.setEnabled(False)
        self.seek_slider.setEnabled(False)

    def select_video(self, video_number):
        filename, _ = QFileDialog.getOpenFileName(self, f"Select Video {video_number}", "", "Video Files (*.mp4 *.avi)")
        if filename:
            if video_number == 1:
                self.video1 = cv2.VideoCapture(filename)
                if not self.video1.isOpened():
                    QMessageBox.critical(self, "Error", f"Could not open video 1: {filename}")
                    return
            else:
                self.video2 = cv2.VideoCapture(filename)
                if not self.video2.isOpened():
                    QMessageBox.critical(self, "Error", f"Could not open video 2: {filename}")
                    return

            if self.video1 and self.video2:
                self.seek_slider.setValue(0)
                self.play_pause_button.setEnabled(True)
                self.set_speed_button.setEnabled(True)
                self.seek_slider.setEnabled(True)
                QMessageBox.information(self, "Success", f"Video {video_number} loaded successfully")

    def play_pause(self):
        if self.video1 and self.video2:
            if self.is_playing:
                self.timer.stop()
                self.play_pause_button.setText('Play')
            else:
                self.timer.start(int(33 / self.current_speed))  # Adjust for current speed
                self.play_pause_button.setText('Pause')
            self.is_playing = not self.is_playing
        else:
            QMessageBox.warning(self, "Warning", "Please select both videos before playing")

    def update_frame(self):
        if not self.video1 or not self.video2:
            QMessageBox.critical(self, "Error", "Video objects are not initialized")
            return

        ret1, frame1 = self.video1.read()
        ret2, frame2 = self.video2.read()

        if ret1 and ret2:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

            h1, w1, ch1 = frame1.shape
            h2, w2, ch2 = frame2.shape

            bytes_per_line1 = ch1 * w1
            bytes_per_line2 = ch2 * w2

            q_image1 = QImage(frame1.data, w1, h1, bytes_per_line1, QImage.Format_RGB888)
            q_image2 = QImage(frame2.data, w2, h2, bytes_per_line2, QImage.Format_RGB888)

            self.video_label1.setPixmap(QPixmap.fromImage(q_image1).scaled(self.video_label1.size(), Qt.KeepAspectRatio))
            self.video_label2.setPixmap(QPixmap.fromImage(q_image2).scaled(self.video_label2.size(), Qt.KeepAspectRatio))

            # Update slider position
            total_frames = min(self.video1.get(cv2.CAP_PROP_FRAME_COUNT), self.video2.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = self.video1.get(cv2.CAP_PROP_POS_FRAMES)
            self.seek_slider.setValue(int((current_frame / total_frames) * 1000))
        else:
            QMessageBox.warning(self, "Warning", "End of video reached")
            self.play_pause()

    def seek(self):
        if self.video1 and self.video2:
            total_frames = min(self.video1.get(cv2.CAP_PROP_FRAME_COUNT), self.video2.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_to_seek = int((self.seek_slider.value() / 1000) * total_frames)

            self.video1.set(cv2.CAP_PROP_POS_FRAMES, frame_to_seek)
            self.video2.set(cv2.CAP_PROP_POS_FRAMES, frame_to_seek)

            self.update_frame()

    def set_speed(self):
        try:
            new_speed = float(self.speed_input.text())
            if new_speed <= 0:
                raise ValueError("Speed must be positive")
            self.current_speed = new_speed
            if self.is_playing:
                self.timer.setInterval(int(33 / self.current_speed))
            QMessageBox.information(self, "Success", f"Playback speed set to {new_speed}x")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())