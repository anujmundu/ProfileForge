"""
SVG rectangle utilities.
"""

from xml.etree.ElementTree import Element, SubElement


def add_rectangle(
    parent: Element,
    *,
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str = "none",
    stroke: str = "none",
    stroke_width: int = 0,
    rx: int = 0,
    ry: int = 0,
) -> Element:
    """Add a rectangle element to an SVG."""

    return SubElement(
        parent,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "fill": fill,
            "stroke": stroke,
            "stroke-width": str(stroke_width),
            "rx": str(rx),
            "ry": str(ry),
        },
    )