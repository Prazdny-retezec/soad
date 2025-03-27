FROM python:3.12-alpine

EXPOSE 80
WORKDIR /src

# setup python enviroment
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# copy source code
COPY src/ .

# run application
CMD ["fastapi", "run", "/src/main.py", "--port", "80"]