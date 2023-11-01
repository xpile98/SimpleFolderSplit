"""
import splitfolders

dataset_path = 'D:\\(temp)Remover_Panel\\_images\\TestImages_20230516(test)'
output_path = dataset_path + '_splitted'
splitfolders.ratio(dataset_path, output=output_path, seed=1337, ratio=(0.7, 0.3))       # Train / Valid
"""
import sys
import os
import splitfolders
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSlider, QMessageBox

class ImageSplitter(QWidget):
    def __init__(self):
        super().__init__()

        self.dataset_path = None
        self.output_path = None
        self.train_ratio = 0.7

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.select_folder_button = QPushButton('Select Folder')
        self.select_folder_button.clicked.connect(self.selectFolder)
        layout.addWidget(self.select_folder_button)

        self.folder_label = QLabel('')
        layout.addWidget(self.folder_label)

        self.train_ratio_label = QLabel('Train Ratio (0.0 - 1.0): 0.70')
        layout.addWidget(self.train_ratio_label)

        self.train_ratio_slider = QSlider()
        self.train_ratio_slider.setOrientation(1)  # Vertical orientation
        self.train_ratio_slider.setMinimum(0)
        self.train_ratio_slider.setMaximum(100)
        self.train_ratio_slider.setValue(int(self.train_ratio * 100))
        self.train_ratio_slider.valueChanged.connect(self.updateTrainRatio)
        layout.addWidget(self.train_ratio_slider)

        self.valid_ratio_label = QLabel('Valid Ratio (Automatically Calculated): 0.30')
        layout.addWidget(self.valid_ratio_label)

        self.split_button = QPushButton('Split Images')
        self.split_button.clicked.connect(self.splitImages)
        layout.addWidget(self.split_button)

        self.setLayout(layout)
        self.setWindowTitle('SimpleFolderSplit')

    def selectFolder(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        folder_dialog.setDirectory(os.path.expanduser('~'))  # Start in user's home directory
        if folder_dialog.exec_():
            self.dataset_path = folder_dialog.selectedFiles()[0]
            self.folder_label.setText(self.dataset_path)

    def updateTrainRatio(self):
        self.train_ratio = self.train_ratio_slider.value() / 100.0
        self.valid_ratio_label.setText(f'Valid Ratio (Automatically Calculated): {1 - self.train_ratio:.2f}')
        self.train_ratio_label.setText(f'Train Ratio (0.0 - 1.0): {self.train_ratio:.2f}')

    def splitImages(self):
        if self.dataset_path is None:
            return

        self.output_path = self.dataset_path + '_splitted'
        splitfolders.ratio(self.dataset_path, output=self.output_path, seed=1337, ratio=(self.train_ratio, 1 - self.train_ratio))
        QMessageBox.information(self, 'Information', f'Images split and saved in {self.output_path}')

        # self.folder_label.setText(f'Images split and saved in {self.output_path}')

        # Open the folder in the default file explorer
        if os.path.exists(self.output_path):
            if sys.platform == 'win32':
                os.system(f'explorer.exe /e,"{os.path.abspath(self.output_path)}"')
            elif sys.platform == 'darwin':
                os.system(f'open -R "{self.output_path}"')
            elif sys.platform == 'linux':
                os.system(f'xdg-open "{self.output_path}"')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splitter = ImageSplitter()
    splitter.show()
    sys.exit(app.exec_())
