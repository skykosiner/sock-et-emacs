import sys

sys.path.append("..")

from app import utils
import unittest


class TestVimColor(unittest.TestCase):
    def test_get_current_colors(self):
        color = utils.current_vim_color_scheme()
        self.assertTrue(color, "rose-pine-main")
