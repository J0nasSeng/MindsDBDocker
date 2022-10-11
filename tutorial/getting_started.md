# MindsDB - Getting Started
This tutorial will show you how you get started with using MindsDB as your "smart" database.
It will cover a basic setup as well as an introductory example on how MindsDB can be easily used for prediction tasks.

## What is MindsDB?
Before we start with a techincal setup, let's see what is MindsDB, what it is ment for and why it is useful as a rapid out-of-the-box ML-tool.
MindsDB is basically a Machine Learning layer placed on top of a database of your choice provided through a SQL. Say, you have conducted experiments and you have imported the data into a Postgres-database-instance. You want to use this data for some prediction task but you (1) don't have that much knowledge about ML and (2) don't want to have much additional overhead to train a ML-model in the "classical" way. This is where MindsDB can help you a lot since it doesn't require you to run your own python scripts or any other "external" code to build predictive models. All you have to know is SQL and a bit about your data, the rest will be done by MindsDB.

## How to setup
MindsDB can be set up easily using Docker or by installing it using `pip`. However, using Docker is recommended if you want to keep the setup as simple as possible. You can use the following docker-compose-file for a basic setup:
```yaml
version: '3.1'

services:

  db:
    image: postgres
    restart: always
    volumes:
      - [user-specific-path]/docker-volumes/postgres:/app/postgres/data
    environment:
      POSTGRES_USER: mindsdb
      POSTGRES_PASSWORD: example
      POSTGRES_DB: mindsdb

  adminer:
    image: adminer
    restart: always
    ports:
      - 8081:8081

  mindsdb:
    image: mindsdb/mindsdb
    ports:
      - 47334:47334
      - 47335:47335
    volumes:
      - ./config/config.json:/app/mindsdb/config/config.json
    depends_on:
      - db
    command: bash -c "python3 -m mindsdb --config=/app/mindsdb/config/config.json --api=http
```
The docker-compose file starts a Postgres-database, adminer which is a database-administration tool and MindsDB. If you already have data stored at some partition, ensure that you correctly mount your database-volume(s). 

Executing `docker-compose up` will start all three containers. Once they are running, you can open [localhost:47334](localhost:47334). Now your browser should show the web-interface of MindsDB. This allows you to connect to your database-instance you have just started.

> NOTE: If you have a database-instance already running, you don't need the database-service in the docker-compose file!

## Running Queries
Once you are connected to your database, you can run arbitrary SQL-queries using the MindsDB-web-interface. This means you can use all the SQL-statements supported by the database-backend you are using. However, those are not the interesting part of MindsDB. Let's see what's so special about MindsDB: The ML-utilities.

MindsDB extends the regular SQL-syntax by a few additional keywords. One of those is `PREDICTOR` which can be used to create predictors just as you create tables in SQL:
With the following syntax you can create predictors which are trained on the data you specify:
```SQL
CREATE PREDICTOR mindsdb.[name]
FROM [data]
  (SELECT * FROM [your_db].[table])
PREDICT [target_variable];
```
By this query we will build a predictor based on `[data]` predicting `[target_variable]`. If you're wondering about hyperaprameters and how they are set: This is done automatically! However, using the Python-API provided by MindsDB can be used to set hyperparameters if you need this to do.

To check the status of your predictor (i.e. if it is training or has already finished) you can use the following query:
```SQL
SELECT status
FROM mindsdb.predictors
WHERE name='[name]';
```

Once the status indicates that your predictor is ready to make predictions, you can query your predictor by using:
```SQL
SELECT [target_variable]
FROM mindsdb.[name]
WHERE feature_1=2
AND feature_2=1000;
```

## An Example
Let's see a concrete example how you can build models using SQL! To do so, navigate to the tutorial directory by `cd ./tutorial`. After that, run `docker-compose up`, now there should happen pretty much on your terminal and you should see something saying *Started at port 47334*. This is MindsDB! You can navigate to [localhost:47334](localhost:47334) (by clicking here your browser should open up). Now, click on `Add data`, choose `Postgres` from the list, you should see a `CREATE TABLE ...`-query in front of you. The default name of the database is `display_name`, change it to something more nice to read, e.g. `data` and fill in the required fields (you find the corresponding values in the `config`-directory). Hit `Run` and you should be connected to the database!

We have to return to Docker once more. This time navigate to the `data-importers`-directory, run `docker build -t iris-importer .` followed by `docker run -it --network=tutorial_default iris-importer`. This will import the Iris-dataset in the Postgres-database which is being used by MindsDB to retrieve data.

Finally, it's time to use MindsDB!

### Building a Predictor
Let's build an estimator using the following statement:

```SQL
CREATE PREDICTOR mindsdb.iris_classifier
FROM data
  (SELECT * FROM public.iris)
PREDICT class;
```

This will take a while to be trained, but once done you can query the `iris_classifier` using:

```SQL
SELECT class
FROM mindsdb.iris_classifier
WHERE sepal_width=5
AND sepal_length=3
AND petal_width=4
AND petal_length=2
```
You should obtain class 1.

Congrats, you've just built your first ML-model using MindsDB!