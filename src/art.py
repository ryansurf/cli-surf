"""
All ASCII art in this file
"""

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
    "light_blue": "\033[0;34m",
    "white": "\033[0;37m",
    "bold_red": "\033[1;31m",    
    "bold_green": "\033[1;32m",  
    "bold_yellow": "\033[1;33m", 
    "bold_blue": "\033[1;34m",   
    "bold_purple": "\033[1;35m", 
    "bold_teal": "\033[1;36m",   
    "bold_white": "\033[1;37m",      
}


def print_wave(show_wave, show_large_wave, color):
    """
    Prints Wave
    """
    if color is not None and color.lower() not in colors:
        print("Not a valid color")
        color = "blue"

    if int(show_large_wave) == 1:
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
    elif int(show_wave) == 1:
        print(
            colors[color]
            + """
      .-``'.
    .`   .`
_.-'     '._
        """
            + colors["end"]
        )
