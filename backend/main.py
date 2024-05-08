import ocean_data
import location_to_cordinates
import uv_index
import output
import wave_art

location = input("Where are you?: ")

cordinates = location_to_cordinates.get_cordinates(location)
lat = cordinates[0]
long = cordinates[1]

# Calls APIs though python files 
ocean_data = ocean_data.ocean_information(lat, long, 1)
uv_index = uv_index.get_uv(lat, long, 1)

def main():
    print("\n")
    wave_art.print_blue_wave()
    output.print_output(uv_index, ocean_data)
    print("\n")

main()