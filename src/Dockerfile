FROM python:3.9

WORKDIR /app

COPY /5-25_gym_hardstyle.csv  /app/25_gym_hardstyle.csv

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit","run"]

CMD ["app.py"]