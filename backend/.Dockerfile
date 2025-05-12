# cannot use ALPINE due to Pypylon library
FROM python:3.13

EXPOSE 80
WORKDIR /src

# setup python enviroment
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# copy source code
COPY src/ .

# copy mock data
COPY mock_data/ mock_data/

# run application
CMD ["fastapi", "run", "/src/main.py", "--port", "80"]