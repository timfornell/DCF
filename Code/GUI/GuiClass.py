import cv2
from Track.TrackClass import Track
import Defs.GlobalVariables as glob

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
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self._window_name, 0, 0)
        cv2.setMouseCallback(self._window_name, self.mouse_callback_function)

    def get_rectangles(self):
        ret_list = self._rectangles_to_draw
        if self._drawing:
            # The last rectangle hasn't been finished yet
            ret_list = ret_list[0:-1]
        return ret_list


    def update_rectangle_positions(self, new_positions):
        for obj in new_positions:
            for rect in self._rectangles_to_draw:
                if obj.id == rect.id:
                    rect.update_position(obj._start_point, obj._end_point)

    def update_window(self, image):
        """ This function takes an image that it will display and save a copy of. """
        self._current_image = image
        cv2.resizeWindow(self._window_name, 2 * image.shape[1], 2 * image.shape[0])
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
            cv2.putText(self._overlay, "{}".format(rect.id), rect.start_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1)

        cv2.addWeighted(self._overlay, self._rectangle_alpha, self._output, 1 - self._rectangle_alpha, 0, self._output)
        cv2.imshow(self._window_name, self._output)

    def close_window(self):
        cv2.destroyAllWindows()

    def window_is_open(self):
        return cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE)

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
            if len(self._rectangles_to_draw) < glob.MAX_NUMBER_OF_TRACKS:
                self._drawing = True
                self._drawing_start_position = (x, y)
                # The region that is currently drawn is saved in the last place of the list
                self._rectangles_to_draw.append(Rectangle((x, y), (x + 1, y + 1), self._id_counter))
                self._id_counter += 1
            else:
                print("Maximum number of tracks has been reached.")

        elif event == cv2.EVENT_LBUTTONUP:
            print("Left mouse was released")
            if self._drawing:
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
