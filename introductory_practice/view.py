from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox,QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

class MainWindowView(QMainWindow):
    """View for working with main_window"""
    
    def __init__(self):
        super().__init__()
        loadUi("main_window.ui",self)

    def select_image_file(self)->str:
        '''Returns the path to selected by user image'''
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg)")
        return file_path

    def save_image_file(self)->str:
        '''Returns the path where the user wants to save the image'''
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Image Files (*.png *.jpg *.jpeg)")
        return file_path

    def display_error(self, message:str)->None:
        """Shows the message box with error"""
        QMessageBox.critical(self, "Error", message)

    def display_image(self, image):
        """Shows image on screen"""
        if image is None:
            return
        height, width, channels_number = image.shape if len(image.shape) == 3 else (*image.shape, 1)
        bytes_per_line = channels_number * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888 \
                         if channels_number == 3 else QImage.Format_Grayscale8)
        self.imageLbl.setPixmap(QPixmap.fromImage(q_image))

    def get_channel_id(self)->int:
        """Returns selected channel id"""
        buttons = self.channelsGB.buttons()
        return [buttons[x].isChecked() for x in range(len(buttons))].index(True)

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

    def add_line_to_list(self, line):
        """Adds line to linesLst with specified params: x1, y1, x2, y2, thickness"""
        item = QListWidgetItem(f"Line: ( x1: {line[0]}, y1: {line[1]},
                               x2: {line[2]}, y2: {line[3]}, thickness: {line[4]})")
        self.linesLst.addItem(item)

    def remove_selected_line_from_list(self):
        """Removes selected line from linesLst"""
        selected_items = self.linesList.selectedItems()

        for item in selected_items:
            row = self.linesLst.row(item)
            self.linesList.takeItem(row)
            return row
        return None
