# <center>CLI Surf</center>

<p align="center">
  <img src="./images/wave.png" height=100>
</p>

Surfs up!

CLI Surf is a real time ocean data and forecasting service used in the command line. 

## Usage

Using your browser or CLI you can access the service

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
| location / loc  | Specify the location of your forecast. Ex: `location=new_york_city` **or** `location=nyc`.    |
| forecast / fc  | Number of forecast days. Max = 7, default = 0  |
| hide_wave / hw | Hide the default wave art    |
| show_large_wave / slw   | Show the large wave art   | 
| hide_uv / huv    | Hide uv index   | 
| hide_height / hh    | Hide surf height   | 
| hide_direction / hdir    | Hide Swell direction    | 
| hide_period / hp  | Hide swell period    | 
| hide_location / hl    | Hide location   | 
| hide_date / hdate  | Hide date in forecast   | 
| metric / m  | Numbers in Metric units. Defaults to Imperial   | 
| decimal / dec   | Specify decimal points in output   | 
| color / c   | Choose color of wave art. Ex: `color=light_blue`   | 

**Examples**
* Arguments are seperated by commas.
* `curl localhost:8000`
* `curl localhost:8000?args=location=new_york,hide_height,hide_wave,show_large_wave`
* `curl localhost:8000?args=fc=3,hdate,loc=trestles`

**For detailed information you can access the [help](https://github.com/ryansurf/cli-surf/blob/main/help.txt) page**

* `curl localhost:8000?args=help`


## Installation

**Python Dependencies**
* python>=3.8.1
* geopy
* openmeteo_requests
* pandas
* python-dotenv
* Requests
* requests_cache
* retry_requests

To run locally on your machine, I recommend either:

**Using a [Python Virtual Environment](https://docs.python.org/3/library/venv.html)** 
1. `git clone https://github.com/ryansurf/cli-surf.git`
2. `cd cli-surf`
3. `mv .env.example .env`
4. `python3 -m venv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`
7. `cd src`
8. `python3 server.py`

**Or running Docker (install [Docker](https://docs.docker.com/engine/install/))**
1. `git clone https://github.com/ryansurf/cli-surf.git`
2. `cd cli-surf`
3. `mv .env.example .env`
4. `docker build -t cli-surf .`
5. `docker run -d -p 8000:8000 cli-surf`
    * Add `--restart unless-stopped` for automatic start on reboot

**Variables**

Change `.env.example` to `.env`

| Variable    | Description|
| -------- | ------- | 
| `PORT=`  | The port you want to open to run the application. Default = 8000 |


## Contributing

Questions? Comments?

* Email: [ryanfrederich@gmail.com](mailto:ryanfrederich@gmail.com)
* GitHub: [ryansurf](https://github.com/ryansurf)

## License
[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://badges.mit-license.org)