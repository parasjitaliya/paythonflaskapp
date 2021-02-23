from ubuntu:latest

RUN apt-get update -y && apt-get install -y python3-pip

COPY . /app

WORKDIR /app/AutoCorrectionAPI/

#RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en

CMD ["python3","auto_correction_api.py"]
