FROM python:3.10

WORKDIR /usr/src/app

COPY data-importer.py ./

RUN pip install numpy pandas scikit-learn psycopg2-binary

CMD ["python", "./data-importer.py"]