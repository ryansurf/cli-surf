import helper
import sys

args = helper.seperate_args(sys.argv)
#sys cli inputs
#Defaults. 1 == Show, anything else == hide
coordinates = helper.get_coordinates(args)
lat = coordinates[0]
long = coordinates[1]
city = coordinates[2]

show_wave = 1
show_large_wave = 0
show_uv = 1
show_height = 1
show_direction = 1
show_period = 1
show_city = 1
show_date = 1
unit = "imperial"
decimal = helper.extract_decimal(args)
forecast_days = helper.get_forecast_days(args)
color = helper.get_color(args)

if "hide_wave" in args or "hw" in args:
    show_wave = 0
if "show_large_wave" in args or "slw" in args:
    show_large_wave = 1
if "hide_uv" in args or "huv" in args:
    show_uv = 0
if "hide_height" in args or "hh" in args:
    show_height = 0
if "hide_direction" in args or "hdir" in args:
    show_direction = 0
if "hide_period" in args or "hp" in args:
    show_period = 0
if "hide_location" in args or "hl" in args:
    show_city = 0
if "hide_date" in args or "hdate" in args:
    show_date = 0
if "metric" in args or "m" in args:
    unit = "metric"

# Calls APIs though python files 
ocean_data = helper.ocean_information(lat, long, decimal, unit)
uv_index = helper.get_uv(lat, long, decimal, unit)

def main():
    print("\n")
    if coordinates == "No data":
        print("No location found")
    if ocean_data == "No data":
        print(coordinates)
        print("No ocean data at this location.")
    else:
        helper.print_location(city, show_city)
        helper.print_wave(show_wave, show_large_wave, color)
        helper.print_output(uv_index, ocean_data, show_uv, show_height, show_direction, show_period)
    print("\n")
    forecast = helper.forecast(lat, long, decimal, forecast_days)
    helper.print_forecast(forecast, uv_index, ocean_data, show_uv, show_height, show_direction, show_period, show_date)

main()