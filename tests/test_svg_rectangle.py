from xml.etree.ElementTree import Element

from src.renderer.svg.rectangle import add_rectangle


def test_add_rectangle_creates_svg_rect_element():
    """add_rectangle should create a rectangle element."""

    # Arrange
    root = Element("svg")

    # Act
    rect = add_rectangle(
        root,
        x=10,
        y=20,
        width=300,
        height=120,
        fill="#ffffff",
        stroke="#000000",
        stroke_width=2,
        rx=12,
        ry=12,
    )

    # Assert
    assert rect.tag == "rect"

    assert rect.attrib["x"] == "10"
    assert rect.attrib["y"] == "20"

    assert rect.attrib["width"] == "300"
    assert rect.attrib["height"] == "120"

    assert rect.attrib["fill"] == "#ffffff"
    assert rect.attrib["stroke"] == "#000000"
    assert rect.attrib["stroke-width"] == "2"

    assert rect.attrib["rx"] == "12"
    assert rect.attrib["ry"] == "12"

    assert len(root) == 1
