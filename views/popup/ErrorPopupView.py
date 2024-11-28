from views.popup.PopupView import PopupView
from constants.Colors import Colors

class ErrorPopupView(PopupView):
    def __init__(self, screen, message: str) -> None:
        super().__init__(screen, message)
        self._bg_color = Colors.POPUP_ERROR_COLOR.value

        self._icon_path = "assets/popup/error.png"
        self._load_icon()

