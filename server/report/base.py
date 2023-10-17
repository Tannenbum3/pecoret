import matplotlib.font_manager as font_manager
import matplotlib as mpl
from pathlib import Path
from .mixins.error import ErrorMixin
from . import config


class BaseDefaultReport(ErrorMixin):
    """
    some common setups and adjustments across finding exports, pdf reports, ...
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        origin = Path(__file__).parent
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Regular.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Bold.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Light.ttf'))
        mpl.rcParams['font.family'] = 'Roboto'
        mpl.rcParams['font.size'] = 9
        self.config = config
