# MSiA423 Pokemon Recommender

Author: Wenyang Pan

QA: Xaiver Dong

## Project Charter 

<img src="figures/pokemon_show.png" alt="drawing" height="300" width="360"/>



#### Background 

[Pokemon](https://en.wikipedia.org/wiki/Pok%C3%A9mon#Gameplay_of_Pok%C3%A9mon) is a Japanese multimedia franchise, including video games, books, anime film series, live-action films, etc. The popularity of the Pokemon franchise starts from video games and one of the famous releases is the augmented reality mobile game Pokémon GO in 2016. The game players are the "Pokemon Trainers" and they try to capture Pokemons and train them.

#### Vision

When playing Pokemon video games, players can be overwhelmed by the vast information. The game includes more than 800 different Pokemons and each Pokemon has more than 20 attributes. Sometimes, the player might like a certain Pokemon and want to find Pokemon with similar characteristics for implementing a playing strategy. However, given the large number of Pokemons, it is hard to go over all of them and identify similar Pokemons manually. 

This app aims to solve this problem by building models based on existing Pokemon data and automatically finding the most similar Pokemons of a certain Pokemon. As a result, players can spend their time enjoying the game instead of reading through a Pokemon encyclopedia.

#### Mission

The user will input a name of Pokemon and the recommender will output 10 most similar Pokemons according to an underlying cluster algorithm. The data for this project comes from this [Pokemon dataset](https://www.kaggle.com/rounakbanik/pokemon). 

An example of running the app will look like the following. In a text input field, the user will input a Pokemon they like and the app will output some recommended Pokemons. For example, if the user input "Bulbasaur" (the name of a Pokemon), the app might output the following table, where each row represents a recommended Pokemon. 


|      | name       | type1 | link                                     |
| ---: | :--------- | :---- | :--------------------------------------- |
|    1 | Charmeleon | fire  | https://pokemondb.net/pokedex/Charmeleon |
|    2 | Wartortle  | water | https://pokemondb.net/pokedex/Wartortle  |

The actual format and recommended content in the app will probably be different than the table above. Specifically, the app will probably recommend more than 2 Pokemons and include some other features of each Pokemon, like location/environment found, counter type, etc. But the idea of recommending relevant Pokemons given user's input should remain the same.

#### Success Criteria

##### Machine Learning Metrics

Because the app uses an unsupervised clustering algorithm, we will not use fixed number of certain metrics as the deployment threshold. Instead, we will deploy the algorithm after identifying the best number of clusters with inertia and silhouette score and verifying the clustering algorithm is stable; that is, the model will predict similar clusters when we fit the model with half of the data and predict the cluster for the other half of the data.

Once the app goes live, we can calculate and monitor some other metrics, like the precision of recommendation by observing user behavior. For example, we can count a recommendation as correct when the user clicks the link to learn more about a recommended Pokemon. We can also conduct A/B testing to see whether a certain recommendation algorithm leads to higher precision.

##### Business Metrics

To determine the success of the app from a business perspective, we can measure the number of visits to the app and the user engagement to the Pokemon game. For user engagement, we might send surveys to the app users to learn more about their game performance and satisfaction after using the app. Overall, a successful deployment of the app will help Pokemon players to better explore and enjoy the game.



## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile_app                <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│   ├── model_config.yaml             <- Configuration for model pipeline
│
├── data                              <- Folder that contains data used or generated, will be synced with git
│   ├── raw/                          <- the raw Pokemon data
│   ├── interim/                      <- the intermediate data generated during the model pipeline
│   ├── final/                        <- the final data generated from the model pipeline; will be stored in database
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source module for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run_s3.py                         <- Download and Upload data from/to S3
├── run_rds.py                        <- Create and update table in RDS
├── run_model.py                      <- Model pipeline and create recommendation results
├── requirements.txt                  <- Python package dependencies 
```



## Setup :stars:

### Software Requirements

+ If you want to run the code in this project repo locally, you need to have python 3.6 or above. 
+ In the Docker image :whale:, we use Python 3.6.9 as the running python version.

### Environment Variable

#### AWS Credential

You need to have two environment variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`  setup in your computer to run the following commands with S3. A simple way to do this run the following two lines in your terminal shell. Note that you need to replace "YOUR_ACCESS_KEY_ID" and "YOUR_SECRET_ACCESS_KEY" to your real id and secret access key. 

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

#### RDS Credential

##### Database Connection URI

You need to define an environment variable call `SQLALCHEMY_DATABASE_URI` to create database and ingest data into the remote database. The format for this URI is described below.  

```bash
export SQLALCHEMY_DATABASE_URI = "YOUR_DATABASE_URI"
```

A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 

##### Database Information 

The URI above should be sufficient to run most of docker commands in this project. However, as we will discuss later, we need to be able to enter the interactive session for the remote mysql database. Thus, you also need to define these environment variables. Note that you need to replace these with your actual connection credentials. 

```bash
export MYSQL_USER="YOUR_SQL_USER_NAME"
export MYSQL_PASSWORD="YOUR_SQL_PASSWORD"
export MYSQL_HOST="YOUR_SQL_HOST"
export MYSQL_PORT="YOUR_SQL_PORT"
export MYSQL_DATABASE="YOUR_DATABASE_NAME"
```

### Docker Image :whale:

This project relies on two Docker image to run the command.  You can build these two images with the following command.

```bash
make image-data
make image-app
```

+ The `make image-data` will produce a Docker image called `pokemon_data_wpz3146`, which are used to get the raw data, run the model pipeline, and interact with database. 
+ The `make image-app` will produce a Docker image called `pokemon_wpz3146`, which are used to launch the flask app. 

## Data Source

The dataset used for this app comes from Kaggle. To download the data, you can go to this [website](https://www.kaggle.com/rounakbanik/pokemon) and click the Download button at the top of the page.    Note that you will need to register a Kaggle account in order to download dataset if you do not have one. Because the dataset is relatively small, we also save a copy in `data/raw/pokemon.csv`. Another copy is also uploaded to s3 and we will describe how to download the data from s3. If you want to upload this data to your own S3 bucket,  see this optional section below.

#### [Optional] Upload data to S3


 To upload the data to S3 with docker, you can run the following command. You need to specify your local data path and s3 data path by replacing the `{your_local_path}` and `{your_s3_path}` below. The default `S3_PATH` is `'s3://2021-msia423-wenyang-pan/raw/pokemon.csv'`and the default `LOCAL_PATH` is `data/raw/pokemon.csv`.
```bash
make s3-upload LOCAL_PATH={your_local_path} S3_PATH={your_s3_path}
```
## Model Pipeline :robot:

### Whole Model Pipeline 

You can run the whole model pipeline with the following the command.

```bash
make model-all
```

This command will run the whole model pipeline, including downloading the raw data from s3, preprocessing the data, training the model and generating the recommendation results. The final output is stored in `data/final/results.csv`. Next, we will describe how to run each step in the in the pipeline and the location of artifacts produced from each step. Note that those four steps below need to be run sequentially. 

### Download Raw Data from S3

You can download the data from s3 to local with the following command. You can specify your S3 path by replacing the `{your_s3_path}` below. The default `S3_PATH` is `'s3://2021-msia423-wenyang-pan/raw/pokemon.csv'`. This step will store the raw data to `data/raw/pokemon.csv`.

```bash
make s3-raw S3_PATH={your_s3_path}
```

### Preprocess Data

You can preprocess the data with `make preprocess`, which will store the preprocessed data to `data/interim/data_scale.csv`.

### Train Model

You can train the model with `make train`, which will store the trained model to `models/kmeans.joblib` and the cluster selection plot to `figures/cluster_selection.png`.

### Generate Recommendation Results

You can generate the recommendation results with `make recommend`, which will store the results in `data/final/results.csv`.

## Store Results in Database

### Local Database configuration 

#### SQLite Path

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/pokemons.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite:////Users/martinpan/Repos/2021-msia423-wenyang-pan/data/pokemons.db'
```

#### Create Database Locally

You can create the database locally with the following command. 

```bash
make create-db
```

By default, the sqlite engine string is `sqlite:///data/msia423_pokemons.db`. You can configure your own sqlite engine by setting the environment variable `SQLALCHEMY_DATABASE_URI`. For example, you can do the following.

```bash
export SQLALCHEMY_DATABASE_URI = "sqlite:///data/msia423_pokemons_haha.db"
```

Then when you run `make create-db-local`, the engine string will be set to `sqlite:///data/msia423_pokemons_haha.db`

#### Add information to the Databases Locally

You can ingest the recommendation result to the local database with the following command. Note that this command requires you have already created the database locally. Note that a unique constraint was set to the pair of two columns - `input` and `recommendation`. Thus, you might receive unique constraint errors if you insert duplicate pairs into the database.

```bash
make ingest-to-db
```

By default, this code ingests the csv file located in `data/final/results.csv`. If you need to specify an alternative data path, you can do the following by replacing the `{your_data_path}` below.

```
make ingest-to-db FINAL_DATA_PATH={your_data_path}
```

#### Examine the Added Information in Local

If you create the database locally, you can view your result by using any sqlite client, such as [DB Browser](https://sqlitebrowser.org/), to open the `.db` file created after running the commands above.  

### Remote Database Connection

#### Prerequisites

In order to proceed with the following command, you need to satisfy the following requirements:

1. You need to **connect to the northwestern VPN**.

3. You set up your environment variable correctly as describe in the [RDS Credential section](#rds-credential). 


#### Test Connection to Database

You can run the following to test whether you can connect to the database. 

```bash
make mysql-it
```

If succeed, you should be able to enter an interactive mysql session and you can show all databases you have with the command: `show databases;`.

#### Change Database Encoding 

Because some name of Pokemons contain special characters, you will need to change the encoding of the mysql database to utf8. 

You can check your current encoding with the following command. Note that you need to change `msia423_pokemons` to your own schema name.

```sql
SELECT default_character_set_name FROM information_schema.SCHEMATA 
WHERE schema_name = "msia423_pokemons";
```

Now you can change the encoding for the whole database with following command. Again, you need to change `msia423_pokemons` to your own database name.

```sql
ALTER DATABASE `msia423_pokemons` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

Alternatively, you can change the encoding for a specific table in the database. You need to change `msia423_pokemons.pokemons` to your own table name.

```sql
ALTER TABLE msia423_pokemons.pokemons CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

#### Create Databases Remotely

You can create a new database with the following command. Note that the engine string is configured by the `SQLALCHEMY_DATABASE_URI` environment variable. You should specify this variable to decide where to create the database.

```bash
make create-db
```

#### Add Information to the Databases Remotely

Similar to the this section in the local database, this command ingest a csv file into the table.  The `SQLALCHEMY_DATABASE_URI` variable again determines the engine string for the database. Note that a unique constraint was set to the pair of two columns - `input` and `recommendation`. Thus, you might receive unique constraint errors if you insert duplicate pairs into the database. See [this section](#add-information-to-the-databases-locally) above about how to configure the path of the csv file if you don't want to use the default for some reason. Note that this command might take few minutes to complete.

```bash
make ingest-to-db
```

#### Examine the Added Information in Remote

You can reenter the mysql interactive session by using the command under section [Test Connection to Database](#test-connection-to-database). Then you can type the following command to examine whether the table was created. Note that you need to replace `<your_target_database_name>` to the real database name. 

```sql
show databases;
use <your_target_database_name>;
show tables; 
```

## Launch the App :tada:

### Launch with Established Database

You already ingest the recommendation results into the database as described above. You should be able to launch the app with the following command. Note that the `SQLALCHEMY_DATABASE_URI` environment variable will determine which database the app connects to. 

```bash
make docker-app-local
```

Now you should be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pokeomn` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### Launch from Scratch

If you have only built the two docker images but do not run the model pipeline and set up the database, you can do all the work and launch the app with the following.

```bash
make launch-in-one
```

### Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

## Unit Test

Unit tests are implemented when appropriate for modules in this project. You can run these tests 
with this command:
```bash
make test
```
