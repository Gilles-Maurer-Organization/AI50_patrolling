from views.popup.PopupView import PopupView
from constants.Colors import Colors

class InfoPopupView(PopupView):
    def __init__(self, screen, message: str) -> None:
        super().__init__(screen, message)
        self._bg_color = Colors.POPUP_INFO_COLOR.value

        self._icon_path = "assets/popup/information.png"
        self._load_icon()

