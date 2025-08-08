FROM python

WORKDIR /myapp/

COPY ./sql_demo.py .

RUN pip install psycopg2-binary

CMD [ "python", "sql_demo.py" ]