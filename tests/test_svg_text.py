from xml.etree.ElementTree import Element

from src.renderer.svg.text import add_text


def test_add_text_creates_svg_text_element():
    """add_text should create a text element."""

    # Arrange
    root = Element("svg")

    # Act
    text = add_text(
        root,
        content="Hello",
        x=10,
        y=20,
        font_size=18,
        font_weight="bold",
    )

    # Assert
    assert text.tag == "text"
    assert text.text == "Hello"

    assert text.attrib["x"] == "10"
    assert text.attrib["y"] == "20"

    assert text.attrib["font-size"] == "18"
    assert text.attrib["font-weight"] == "bold"

    assert len(root) == 1
