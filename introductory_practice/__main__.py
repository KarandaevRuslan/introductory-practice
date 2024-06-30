import sys
from PyQt5.QtWidgets import QApplication
from model import ImageModel
from view import MainWindowView
from presenter import ImagePresenter

def main():
    app = QApplication(sys.argv)
    model = ImageModel()
    view = MainWindowView()
    presenter = ImagePresenter(model, view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
