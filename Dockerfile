FROM python:slim
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY nltk_download.py .
RUN python nltk_download.py
WORKDIR /usr/app/
