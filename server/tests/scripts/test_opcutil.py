import pytest

from scripts import opcutil

valid_colors = ['#000000', '#123456', '#987abc', '#abcdef', '#ffffff']
invalid_colors = ['#fffffg', 'fail', 'abcdef', '#abcdef0', '#abcde', '#abc']


def test_is_color():
    for color in valid_colors:
        assert opcutil.is_color(color)

    for color in invalid_colors:
        assert not opcutil.is_color(color)


def test_get_color():
    assert opcutil.get_color('#000000') == (0, 0, 0)
    assert opcutil.get_color('#0eff32') == (14, 255, 50)

    get_color_match = "Please provide a color in the format '#RRGGBB'.*"
    for color in invalid_colors:
        with pytest.raises(ValueError, match=get_color_match):
            opcutil.get_color(color)
