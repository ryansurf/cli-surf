# CLI Surf Report

CLI Surf Report is a surf report and forecasting service used in the command line. It uses the [Open-Meteo](https://open-meteo.com/en/docs/marine-weather-api) weather API

You can see it running here: [TODO]()

## Usage

Using your browser or CLI you can access the service

<put screenshot of service in use>

```
$ curl localhost:8000

Location:  San Diego

      .-``'.
    .`   .`
_.-'     '._ 
        
UV index:  6.4
Wave Height:  3.9
Wave Direction:  238.0
Wave Period:  9.8

```

**Arguments**
| Argument    | Description|
| -------- | ------- |
| location  | Specify the location of your forecast. Ex: location=new_york_city **or** location=nyc.    |
| forecast  | Number of forecast days. Max = 7, default = 0  |
| hide_wave | Hide the default wave art    |
| show_large_wave   | Show the large wave art   | 
| hide_uv    | Hide uv index   | 
| hide_height    | Hide surf height   | 
| hide_direction    | Hide Swell direction    | 
| hide_period   | Hide swell period    | 
| hide_location    | Hide location   | 
| hide_date   | Hide date in forecast   | 
| metric   | Numbers in Metric units. Defaults to Imperial   | 
| decimal   | Specify decimal points in output   | 

**Examples**
* Arguments are seperated by commas.
* `curl http://localhost:8000`
* `curl http://localhost:8000?args=location=new_york,hide_height,hide_wave,show_large_wave`
* `curl http://localhost:8000?args=location=trestles,forecast=3`



## Installation

**Python Dependencies**
* geopy
* openmeteo_requests
* pandas
* Requests
* requests_cache
* retry_requests
* termcolor

To run locally on your machine, I recommend using a [Python Virtual Environment](https://docs.python.org/3/library/venv.html)
1. `git clone https://github.com/ryansurf/surf_report.git`
2. `cd surf_report`
3. `python3 -m venv <myenvname>`
4. `cd <myenvname>/bin/`
5. `source activate `
6. `cd ../..`
7. `pip install -r requirements.txt`
8.  `cd backend`
9. `python3 main.py` **OR** `python3 server.py` if you would like to run a Flask server


## Contributing

Questions? Comments?

* Email: [ryanfrederich@gmail.com](mailto:ryanfrederich@gmail.com)
* GitHub: [ryansurf](https://github.com/ryansurf)

## License

[MIT](https://choosealicense.com/licenses/mit/)