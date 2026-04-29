from PIL import ImageGrab
import cv2
import numpy as np

from core.actions.base_action import Action
from core.actions.halpers.context import Context


class ImageSearchAction(Action):
    def __init__(self, template_path: str, threshold=0.8):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        self.w, self.h = self.template.shape[::-1]
        self.threshold = threshold

    def run(self, context: Context) -> bool:
        screenshot = ImageGrab.grab()
        gray_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        res = cv2.matchTemplate(gray_screenshot, self.template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)

        if loc[0].size > 0:
            pt = (loc[1][0], loc[0][0])
            context.coordinates = (pt[0] + self.w // 2, pt[1] + self.h // 2)
            return True
        return False

# При добавлении поиска вокруг мыши ставить minimal value = размеру шаблона.
# Вокруг мыши, в области
