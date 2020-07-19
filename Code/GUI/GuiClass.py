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
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self.mouse_callback_function)

    def get_track_ROIs(self):
        pass

    def update_window(self, image):
        self._current_image = image
        cv2.imshow(self._window_name, self._current_image)

    def update_rectangles(self):
        self._overlay = self._current_image.copy()
        self._output  = self._current_image.copy()
        if self._rectangles_to_draw:
            self.draw_rectangles(self._rectangles_to_draw)

    def draw_rectangles(self, rectangles):
        for rect in rectangles:
            cv2.rectangle(self._overlay, rect.start_point, rect.end_point, self._rectangle_color, self._rectangle_thickness)

        cv2.addWeighted(self._overlay, self._rectangle_alpha, self._output, 1 - self._rectangle_alpha, 0, self._output)
        cv2.imshow(self._window_name, self._output)

    def close_window(self):
        pass

    def clear_rectangles(self):
        self._rectangles_to_draw = []

    def mouse_callback_function(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Left mouse was pressed")
            self._drawing = True
            self._drawing_start_position = (x, y)
            # The region that is currently drawn is saved in the last place of the list
            self._rectangles_to_draw.append(Rectangle((x, y), (x + 1, y + 1)))

        elif event == cv2.EVENT_LBUTTONUP:
            print("Left mouse was released")

            if self._drawing:
                self._drawing = False
                self._rectangles_to_draw.pop()

            self._drawing_end_position = (x, y)
            window = cv2.getWindowImageRect(self._window_name)
            top_left_x = max(min(self._drawing_start_position[0], self._drawing_end_position[0]), 0)
            top_left_y = max(min(self._drawing_start_position[1], self._drawing_end_position[1]), 0)
            bottom_right_x = min(max(self._drawing_start_position[0], self._drawing_end_position[0]), window[2] - 1)
            bottom_right_y = min(max(self._drawing_start_position[1], self._drawing_end_position[1]), window[3] - 1)
            self._rectangles_to_draw.append(Rectangle((top_left_x, top_left_y), (bottom_right_x, bottom_right_y)))

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
            self._rectangles_to_draw[-1] = Rectangle((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))


class Rectangle():
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point