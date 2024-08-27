FROM python:3.11.6-slim

# set the working directory
WORKDIR /app

# install dependencies
COPY requirements.txt ./

# RUN echo requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000
    # copy the all files to docker /app folder
COPY . .

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
