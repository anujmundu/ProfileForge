"""
SVG canvas utilities.
"""

from xml.etree.ElementTree import Element


class SvgCanvas:
    """Creates the root SVG element."""

    def create(
        self,
        width: int,
        height: int,
    ) -> Element:
        return Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "width": str(width),
                "height": str(height),
                "viewBox": f"0 0 {width} {height}",
            },
        )