import cv2

class GUI():
    def __init__(self):
        self._window_name = "DCF"
        self._drawing = False
        self._drawing_start_position = (0, 0)
        self._drawing_end_position = (0, 0)
        self._rectangle_being_drawed = None
        self._rectangles_to_draw = []
        self._rectangle_color = (255, 0, 0)
        self._rectangle_thickness = 2
        self._rectangle_alpha = 0.5
        self._id_counter = 1
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self.mouse_callback_function)

    def get_track_ROIs(self):
        return self._rectangles_to_draw

    def update_window(self, image):
        """ This function takes an image that it will display and save a copy of. """
        self._current_image = image
        cv2.imshow(self._window_name, self._current_image)

    def update_rectangles(self):
        """
        The purpose of this function is to draw rectangles in the image.

        The rectangles are either being drawn currently or has been drawn previously. If a rectangle is currently
        being drawn it is placed at the back of the array self._rectangles_to_draw which also contains all previously
        drawn rectangles. It is supposed to be called once per frame, therefore the overlay and output variables
        that are needed are initialised here.
        """
        self._overlay = self._current_image.copy()
        self._output  = self._current_image.copy()
        if self._rectangles_to_draw:
            self.draw_rectangles(self._rectangles_to_draw)

    def draw_rectangles(self, rectangles):
        """
        This function takes a list of rectangles to draw and draws it on the overlay that is saved internally.
        """
        for rect in rectangles:
            cv2.rectangle(self._overlay, rect.start_point, rect.end_point, self._rectangle_color, self._rectangle_thickness)

        cv2.addWeighted(self._overlay, self._rectangle_alpha, self._output, 1 - self._rectangle_alpha, 0, self._output)
        cv2.imshow(self._window_name, self._output)

    def close_window(self):
        pass

    def clear_rectangles(self):
        self._rectangles_to_draw = []

    def mouse_callback_function(self, event, x, y, flags, param):
        """
        The purpose of this function is to handle anything related to the mouse.

        If the left mouse button is pressed it will initiate a drawing session by placing a rectangle at the last
        position in the internal array '_rectangles_to_draw' with a corner located at the mouse pointer. While in a
        drawing session and the mouse is moved around the size and width of this rectangle will be changed. When the
        left mouse button is released the drawing session is ended and the position of the mouse pointer determines
        where the second corner is placed. If the middle mouse button is clicked the last added rectangle will be
        removed, if possible.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Left mouse was pressed")
            self._drawing = True
            self._drawing_start_position = (x, y)
            # The region that is currently drawn is saved in the last place of the list
            self._rectangles_to_draw.append(Rectangle((x, y), (x + 1, y + 1), self._id_counter))
            self._id_counter += 1

        elif event == cv2.EVENT_LBUTTONUP:
            print("Left mouse was released")
            self._drawing = False
            self._drawing_end_position = (x, y)
            window = cv2.getWindowImageRect(self._window_name)
            top_left_x = max(min(self._drawing_start_position[0], self._drawing_end_position[0]), 0)
            top_left_y = max(min(self._drawing_start_position[1], self._drawing_end_position[1]), 0)
            bottom_right_x = min(max(self._drawing_start_position[0], self._drawing_end_position[0]), window[2] - 1)
            bottom_right_y = min(max(self._drawing_start_position[1], self._drawing_end_position[1]), window[3] - 1)
            self._rectangles_to_draw[-1].update_position((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))

        elif event == cv2.EVENT_MBUTTONDOWN:
            print("Middle click was pressed")
            if self._rectangles_to_draw:
                self._rectangles_to_draw.pop()

        elif self._drawing:
            window = cv2.getWindowImageRect(self._window_name)
            top_left_x = max(min(self._drawing_start_position[0], x), 0)
            top_left_y = max(min(self._drawing_start_position[1], y), 0)
            bottom_right_x = min(max(self._drawing_start_position[0], x), window[2] - 1)
            bottom_right_y = min(max(self._drawing_start_position[1], y), window[3] - 1)
            self._rectangles_to_draw[-1].update_position((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))


class Rectangle():
    def __init__(self, start_point, end_point, id):
        self.start_point = start_point
        self.end_point = end_point
        self.id = id

    def update_position(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
