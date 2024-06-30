from email.mime import image
import cv2

class ImageModel:
    """Features image"""
    def __init__(self):
        self.set_default()

    def load_image(self, file_path):
        """Loads image by file path"""
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("Could not load image")
            self.original_channel_image = self.original_image.copy()
            self.__image = self.original_image.copy()
        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")

    def capture_image(self):
        """Captures image using webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise ValueError("Could not open webcam")
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise ValueError("Could not capture image")
        self.original_image = frame
        self.original_channel_image = self.original_image.copy()
        self.image = self.original_image.copy()

    def apply_channel(self):
        """Applies channel to the image that could be already altered (margin or lines)
        Channel id list:
        0 - original
        1 - greyscale
        2 - red
        3 - green
        4 - blue"""
        if self.original_image is None:
            raise ValueError("No image loaded")
        self.image = self.original_channel_image.copy()
        match(self.__channel_id):
            case 1:
                #greyscale
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            case 2:
                #red
                self.image[:, :, 0] = 0
                self.image[:, :, 1] = 0
            case 3:
                #green
                self.image[:, :, 0] = 0
                self.image[:, :, 2] = 0
            case 4:
                #blue
                self.image[:, :, 1] = 0
                self.image[:, :, 2] = 0

    def add_margin_to_image(self):
        """Adds border/margin to the image that may already has drawn lines and saves it to original_channel_image"""
        if self.original_image is None:
            raise ValueError("No image loaded")
        self.original_channel_image = cv2.copyMakeBorder(
            self.original_channel_image, self.__margin[0], self.__margin[2], self.__margin[3], self.__margin[1], cv2.BORDER_CONSTANT, value=(0, 0, 0))

    def draw_line(self, x1, y1, x2, y2, thickness):
        """Draws line on the original image and saves it to original_channel_image.
        Also adds line to lines"""
        if self.original_image is None:
            raise ValueError("No image loaded")
        self.lines.append((x1, y1, x2, y2, thickness))
        cv2.line(self.original_channel_image, (x1, y1), (x2, y2), (0, 255, 0), thickness)

    def remove_line(self, index):
        """Removes line with specified index from lines list"""
        if 0 <= index < len(self.lines):
            self.lines.pop(index)

    def redraw_lines(self):
        """Draws lines again from lines list on original image and saves it to original_channel_image"""
        if self.original_image is None:
            raise ValueError("No image loaded")
        self.reset_original_channel_image()
        for line in self.lines:
            cv2.line(self.original_channel_image, 
                        (line[0], line[1]), (line[2], line[3]), (0, 255, 0), line[4])  

    def save_image(self, file_path):
        """Saves image to the specified location"""
        if self.original_image is None:
            raise ValueError("No image to save")
        cv2.imwrite(file_path, self.image)

    def reset_original_channel_image(self):
        """Assigns original_image to original_channel_image"""
        if self.original_image is not None:
            self.original_channel_image = self.original_image.copy()
            
    def redraw_all(self):
        """Draws all again and saves it to image"""
        self.redraw_lines()
        self.add_margin_to_image()
        self.apply_channel()
        
    def set_default(self):
        """Returns everything to the way it was"""
        self.__image = None
        self.original_image = None
        self.original_channel_image = None
        self.__channel_id = 0
        self.__margin = [0,0,0,0]
        self.lines = []

    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self,value):
        self.__image = value
        
    @property
    def channel_id(self):
        return self.__channel_id
    
    @channel_id.setter
    def channel_id(self,value):
        self.__channel_id = value
    
    def set_margin(self,up,right,bottom,left):
        self.__margin[0] = up
        self.__margin[1] = right
        self.__margin[2] = bottom
        self.__margin[3] = left
        