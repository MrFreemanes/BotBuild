import pyautogui

from config.action_config import ClickType


def click(x, y, clicks: int, button: ClickType):
    pyautogui.click(x, y, clicks=clicks, button=button.value)
