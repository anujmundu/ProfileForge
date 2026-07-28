"""
SVG text utilities.
"""

from xml.etree.ElementTree import Element, SubElement


def add_text(
    parent: Element,
    *,
    content: str,
    x: int,
    y: int,
    font_size: int = 16,
    font_weight: str = "normal",
) -> Element:
    """Add a text element to an SVG."""

    text = SubElement(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "font-size": str(font_size),
            "font-weight": font_weight,
        },
    )

    text.text = content

    return text