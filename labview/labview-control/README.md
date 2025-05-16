# Camera Control API Example
This REST API is only example.
The LabVIEW program sets hyperspectral camera and periodically (every 1000 ms) calls HTTP GET method on specified endpoint, if endpoint is returning 1 it will take a picture, else it just waits.
**Also parameters of the hyperspectral camera have to be set, before running LabVIEW!**

## Installation
1. Install python

2. Create Virtual Enviroment
`python -m venv venv`

3. Install dependencies
`pip install -r requirements.txt`

4. Run example REST API
`uvicorn camera-control-api-example:app`