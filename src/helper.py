

#Args are seperated by commas in input. Sereperat them and return list
def seperate_args(args):
    if len(args) > 1:
        new_args = args[1].split(",")
        return new_args
    else:
        return []

#Checks to see if forecast in cli args. Defaults to 0
def get_forecast_days(args):
    for arg in args:
        arg = str(arg)
        if arg.startswith("forecast=") or arg.startswith("fc="):
            forecast = int(arg.split('=')[1])
            if forecast < 0 or forecast > 7:
                print("Must choose a non-negative number >= 7 in forecast!")
                break
            return forecast
    return 0

def print_location(city, show_city):
    if int(show_city) == 1:
        print("Location: ", city)
        print("\n")

#Prints output
def print_output(uv_index, ocean_data, show_uv, show_height, show_direction, show_period):
    if int(show_uv) == 1:
        print("UV index: ", uv_index)
    if int(show_height) == 1:
        print("Wave Height: ", ocean_data[0])
    if int(show_direction) == 1:
        print("Wave Direction: ", ocean_data[1])
    if int(show_period) == 1:
        print("Wave Period: ", ocean_data[2])

#Takes in list of forecast data and prints
def print_forecast(forecast_list, uv_index, ocean_data, show_uv, show_height, show_direction, show_period, show_date):
    transposed = list(zip(*forecast_list))
    for day in transposed:
        if show_date == 1:
            print("Date: ", day[3])
        # if int(show_uv) == 1:
        #     print("UV index: ", uv_index)
        if int(show_height) == 1:
            print("Wave Height: ", day[0])
        if int(show_direction) == 1:
            print("Wave Direction: ", day[1])
        if int(show_period) == 1:
            print("Wave Period: ", day[2])
        print("\n")

# Function to extract decimal value from command-line arguments
#Default is 1
def extract_decimal(args):
    for arg in args:
        if arg.startswith("decimal=") or arg.startswith("dec="):
            try:
                decimal_value = int(arg.split('=')[1])
                return decimal_value
            except (ValueError, IndexError):
                print("Invalid value for decimal. Please provide an integer.")
    return 1

def get_color(args):
    for arg in args:
        arg = str(arg)
        if arg.startswith("color=") or arg.startswith("c=") :
            color_name = arg.split('=')[1]
            return color_name
    return 'blue'

#Takes a list as input and rounds each of the elements to the decimal
def round_decimal(round_list, decimal):
    rounded_list = list()
    for num in round_list:
        rounded_list.append(round(num, decimal))
    return rounded_list


    
