"""
All ASCII art in this file
"""

import logging

logger = logging.getLogger(__name__)

# ASCII text colors
colors = {
    "end": "\033[0m",
    "default": "\033[39m",
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "purple": "\033[0;35m",
    "teal": "\033[0;36m",
    "light_blue": "\033[0;94m",
    "white": "\033[0;37m",
    "bold_red": "\033[1;31m",
    "bold_green": "\033[1;32m",
    "bold_yellow": "\033[1;33m",
    "bold_blue": "\033[1;34m",
    "bold_purple": "\033[1;35m",
    "bold_teal": "\033[1;36m",
    "bold_white": "\033[1;37m",
}

ANSI_TO_CSS = {
    "\033[0;31m": "color:#e06c75",  # red
    "\033[0;32m": "color:#98c379",  # green
    "\033[0;33m": "color:#e5c07b",  # yellow
    "\033[0;34m": "color:#61afef",  # blue
    "\033[0;35m": "color:#c678dd",  # purple
    "\033[0;36m": "color:#56b6c2",  # teal
    "\033[0;94m": "color:#82aaff",  # light_blue
    "\033[0;37m": "color:#abb2bf",  # white
    "\033[1;31m": "color:#e06c75;font-weight:bold",
    "\033[1;32m": "color:#98c379;font-weight:bold",
    "\033[1;33m": "color:#e5c07b;font-weight:bold",
    "\033[1;34m": "color:#61afef;font-weight:bold",
    "\033[1;35m": "color:#c678dd;font-weight:bold",
    "\033[1;36m": "color:#56b6c2;font-weight:bold",
    "\033[1;37m": "color:#abb2bf;font-weight:bold",
    "\033[39m": "color:inherit",  # default
    "\033[0m": None,  # reset → close span
}


def ansi_to_html(text: str) -> str:
    html = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for code, css in ANSI_TO_CSS.items():
        if css is not None:
            html = html.replace(code, f'<span style="{css}">')
        else:
            html = html.replace(code, "</span>")
    return f"""
        <pre style="padding:1em;font-family:monospace;line-height:1.4">
            {html}
        </pre>
        """


def print_wave(show_wave, show_large_wave, color):
    """
    Prints Wave
    """
    if color is not None and color.lower() not in colors:
        logger.warning("Invalid color '%s'. Using default 'blue'.", color)
        color = "blue"

    if show_large_wave:
        print(
            colors[color]
            + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⠾⠿⠿⠯⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣾⠛⠁⠀⠀⠀⠀⠀⠀⠈⢻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠿⠁⠀⠀⠀⢀⣤⣾⣟⣛⣛⣶⣬⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠃⠀⠀⠀⠀⠀⣾⣿⠟⠉⠉⠉⠉⠛⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠋⠀⠀⠀⠀⠀⠀⠀⣿⡏⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⡿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠷⣤⣤⣠⣤⣤⡤⡶⣶⢿⠟⠹⠿⠄⣿⣿⠏⠀⣀⣤⡦⠀⠀⠀⠀⣀⡄
⢀⣄⣠⣶⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠓⠚⠋⠉⠀⠀⠀⠀⠀⠀⠈⠛⡛⡻⠿⠿⠙⠓⢒⣺⡿⠋⠁
⠉⠉⠉⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀
"""
            + colors["end"]
        )
    elif show_wave:
        print(
            colors[color]
            + """
      .-``'.
    .`   .`
_.-'     '._
        """
            + colors["end"]
        )
