from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import os

class MainWindowView(QMainWindow):
    """View for working with main_window"""
    
    def __init__(self):
        super().__init__()
        loadUi("main_window.ui",self)
        self.__status_widget = None
        self.scrollArea.setWidgetResizable(True)
        self.__image = None
        self.__fileName = None
        
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.display_image(self.__image)
        

    def select_image_file(self)->str:
        '''Returns the path to selected by user image'''
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg)")
        self.__fileName = os.path.basename(file_path)
        return file_path

    def save_image_file(self)->str:
        '''Returns the path where the user wants to save the image'''
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image File", self.__fileName, "Image Files (*.png *.jpg *.jpeg)")
        return file_path

    def display_error(self, message:str)->None:
        """Shows the message box with error"""
        QMessageBox.critical(self, "Error", message)

    def display_image(self, image):
        """Shows image on screen"""
        if image is None:
            return
        self.__image = image
        height, width, channels_number = image.shape if len(image.shape) == 3 else (*image.shape, 1)
        bytes_per_line = channels_number * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888 \
                         if channels_number == 3 else QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.scrollArea.width() - 30,self.scrollArea.height() - 30,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.imageLbl.setPixmap(pixmap)

    def get_channel_id(self)->int:
        """Returns selected channel id"""
        return [self.originalRB.isChecked(),self.greyscaleRB.isChecked(),
                self.redRB.isChecked(),self.greenRB.isChecked(),
                self.blueRB.isChecked()].index(True)

    def get_margin_size(self):
        """Returns margin size: up, right, left, bottom"""
        return (self.upSB.value(),self.rightSB.value(),self.bottomSB.value(),self.leftSB.value())

    def get_line_params(self):
        """Returns coordinates (x1, y1, x2, y2) of the segment ends and brush thickness"""
        try:
            params = (int(self.x1LE.text()),int(self.y1LE.text()),int(self.x2LE.text()),int(self.y2LE.text()))
            for param in params:
                if param < 0:
                    raise ValueError
            return (*params,self.thicknessSB.value())
        except ValueError:
            self.display_error("Invalid line parameters")
            return None

    def add_line_to_list(self, x1, y1, x2, y2, thickness):
        """Adds line to linesLst with specified params: x1, y1, x2, y2, thickness"""
        item = QListWidgetItem(f"Line: (x1: {x1}, y1: {y1}, "
                               f"x2: {x2}, y2: {y2}, thickness: {thickness})")
        self.linesLst.addItem(item)

    def remove_selected_line_from_list(self):
        """Removes selected line from linesLst"""
        selected_items = self.linesLst.selectedItems()

        for item in selected_items:
            row = self.linesLst.row(item)
            self.linesLst.takeItem(row)
            return row
        return None

    def set_status(self,status:str):
        """Sets text to statusBar"""
        if self.__status_widget is not None:
            self.statusBar.removeWidget(self.__status_widget)
        self.__status_widget = QLabel(status)
        self.statusBar.addWidget(self.__status_widget)
        
    def set_default(self):
        """Returns everything to the way it was"""
        self.originalRB.setChecked(True)
        
        self.upSB.setValue(0)
        self.rightSB.setValue(0)
        self.bottomSB.setValue(0)
        self.leftSB.setValue(0)
        
        self.x1LE.setText("")
        self.y1LE.setText("")
        self.x2LE.setText("")
        self.y2LE.setText("")
        self.thicknessSB.setValue(1)
        
        self.statusBar.removeWidget(self.__status_widget)
        self.__status_widget = None
        self.linesLst.clear()
