"""Launch module"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from model import ImageModel
from view import MainWindowView
from presenter import ImagePresenter

def main():
    """Starts application"""
    app = QApplication(sys.argv)
    model = ImageModel()
    view = MainWindowView()
    presenter = ImagePresenter(model, view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()
