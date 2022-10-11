from json import load
from multiprocessing.forkserver import connect_to_new_process
from sqlite3 import connect
from time import sleep
import psycopg2 as psy
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

#sleep(10) # wait until database is ready

connection = psy.connect(dbname='mindsdb', user='mindsdb', host='tutorial_db_1', password='example')

cur = connection.cursor()

iris = load_iris()
data_with_labels = np.hstack((iris['data'], iris['target'].reshape(-1, 1)))
df = pd.DataFrame(data=data_with_labels, columns=['sepal_length', 'sepal_width', 'petal_wdith', 'petal_length', 'class'])

cur.execute('CREATE TABLE IF NOT EXISTS iris (id serial PRIMARY KEY, sepal_length float8, sepal_width float8, petal_wdith float8, petal_length float8, class INT)')

columns = ",".join(list(df.columns))
for id, row in df.iterrows():
    if id % 100 == 0:
        print(f"INSERTING {id}")
    np_row = row.to_numpy()
    values = "VALUES({})".format(",".join([str(num) for num in np_row]))
    insert_stmt = "INSERT INTO iris ({}) {}".format(columns, values)

    cur.execute(insert_stmt)
    connection.commit()

connection.close()
