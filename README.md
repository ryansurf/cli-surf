# CLI Surf Report

CLI Surf Report is a surf report and forecasting service used in the command line. 

## Usage

Using your browser or CLI you can access the service

<put screenshot of service in use>

`$ curl <whatever my domain will be>`

## Installation

**Python dependencies**
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