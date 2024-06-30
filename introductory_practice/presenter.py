from PyQt5.QtCore import QCoreApplication
class ImagePresenter:
    """Presenter for image editor application"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()
        self.ignoreWarns = False

    def connect_signals(self):
        """Binds commands with signals"""
        self.view.loadImageBtn.triggered.connect(self.load_image)
        self.view.captureImageBtn.triggered.connect(self.capture_image)
        self.view.saveImageBtn.triggered.connect(self.save_image)
        self.view.exitBtn.triggered.connect(QCoreApplication.quit)
        
        self.view.originalRB.clicked.connect(self.apply_channel)
        self.view.greyscaleRB.clicked.connect(self.apply_channel)
        self.view.redRB.clicked.connect(self.apply_channel)
        self.view.greenRB.clicked.connect(self.apply_channel)
        self.view.blueRB.clicked.connect(self.apply_channel)
        
        self.view.upSB.valueChanged.connect(self.add_margin)
        self.view.rightSB.valueChanged.connect(self.add_margin)
        self.view.bottomSB.valueChanged.connect(self.add_margin)
        self.view.leftSB.valueChanged.connect(self.add_margin)
        
        self.view.drawBtn.clicked.connect(self.draw_line)
        self.view.linesLst.doubleClicked.connect(self.remove_line)

    def load_image(self):
        """Loads image from your pc"""
        file_path = self.view.select_image_file()
        if file_path:
            try:
                self.ignoreWarns = True
                self.view.set_default()
                self.model.set_default()
                self.model.load_image(file_path)
                self.view.display_image(self.model.image)
                self.view.set_status(file_path)
            except ValueError as e:
                self.view.display_error(str(e))

    def capture_image(self):
        """Takes photo from your webcam (if it exists, of course)"""
        try:
            self.ignoreWarns = True
            self.view.set_default()
            self.model.set_default()
            self.model.capture_image()
            self.view.display_image(self.model.image)
            self.view.set_status("Webcam snapshot")
        except ValueError as e:
            self.view.display_error(str(e))

    def apply_channel(self):
        """Applies channel to your photo"""
        if self.ignoreWarns:
            self.ignoreWarns = False
            return
        if self.model.image is None:
            self.view.display_error("No image loaded")
            return
        
        channel_id = self.view.get_channel_id()
        try:
            self.model.channel_id = channel_id
            self.model.redraw_all()
            self.view.display_image(self.model.image)
        except ValueError as e:
            self.view.display_error(str(e))

    def add_margin(self):
        """Adds margin. Margin hides parts of lines below its"""
        if self.model.image is None:
            self.view.display_error("No image loaded")
            return
        
        try:
            size = self.view.get_margin_size()
            self.model.set_margin(*size)
            self.model.redraw_all()
            self.view.display_image(self.model.image)
        except ValueError as e:
            self.view.display_error(str(e))

    def draw_line(self):
        """Draws one green line. Can change its color if you'll decide to select new channel"""
        if self.model.image is None:
            self.view.display_error("No image loaded")
            return
        
        params = self.view.get_line_params()
        if params is not None:
            try:
                self.model.draw_line(*params)
                self.view.add_line_to_list(*params)
                self.model.redraw_all()
                self.view.display_image(self.model.image)
            except ValueError as e:
                self.view.display_error(str(e))

    def save_image(self):
        """Saves image om your pc"""
        if self.model.image is None:
            self.view.display_error("No image to save")
            return
        
        file_path = self.view.save_image_file()
        if file_path:
            try:
                self.model.save_image(file_path)
            except ValueError as e:
                self.view.display_error(str(e))

    def remove_line(self):
        """Removes line"""
        if self.model.image is None:
            self.view.display_error("No image loaded")
            return
        
        row = self.view.remove_selected_line_from_list()
        if row is not None:
            try:
                self.model.remove_line(row)
                self.model.redraw_all()
                self.view.display_image(self.model.image)
            except ValueError as e:
                self.view.display_error(str(e))

