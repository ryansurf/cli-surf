import helper
import sys

#sys cli inputs
#Defaults. 1 == Show, anything else == hide
coordinates = helper.get_coordinates(sys.argv)
lat = coordinates[0]
long = coordinates[1]
city = coordinates[2]

show_art = 1
show_uv = 1
show_height = 1
show_direction = 1
show_period = 1
show_city = 1
decimal = helper.extract_decimal(sys.argv)

if "hide_art" in sys.argv:
    show_art = 0
if "hide_uv" in sys.argv:
    show_uv = 0
if "hide_height" in sys.argv:
    show_height = 0
if "hide_direction" in sys.argv:
    show_direction = 0
if "hide_period" in sys.argv:
    show_period = 0
if "hide_location" in sys.argv:
    show_city = 0


# Calls APIs though python files 
ocean_data = helper.ocean_information(lat, long, decimal)
uv_index = helper.get_uv(lat, long, decimal)

def main():
    print("\n")
    if coordinates == "No data":
        print("No location found")
    if ocean_data == "No data":
        print("No ocean data at this location.")
    else:
        helper.print_location(city, show_city)
        helper.print_blue_wave(show_art)
        helper.print_output(uv_index, ocean_data, show_uv, show_height, show_direction, show_period)
    print("\n")

main()