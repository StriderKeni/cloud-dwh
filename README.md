# Cloud DWH with AWS [![Build Status](https://travis-ci.org/kennycontreras/cloud-dwh.svg?branch=master)](https://travis-ci.org/kennycontreras/cloud-dwh)

Cloud DataWareHouse is an ETL project for a startup called Sparkify.
This project create a database based on a star-schema. The database is located in Amazon Redshift which is a columnar database part of the larger cloud-computing platform Amazon Web Services. One of the features of Amazon Redshift is it's build on a columnar storage arquitecture allowing fast writing for Big-Data.

This project will create two staging tables, all of raw data is available in JSON files obtained from a S3 bucket. After created staging tables, it's time to insert data into analytics tables.

## Pre-requisites

List of all libraries necessaries to execute the project

* psycopg2
* pandas
* sqlalchemy

## Getting Started

***NOTE***
To execute successfully this project please make sure that you have an AWS account and you have credits or free-trial to create a Cluster, DB on Redshift, etc.

- Fill the `dwh.cfg` file with all information about your own AWS Cluster. I provided an IaC file configuration to create a Cluster by your own. This is a jupyter notebook file called `cluster_iac_config.ipynb` feel free to use it if you want to create a cluster using IaC (Infrastructure-as-Code configuration).

- Execute file _create_tables.py_. Open your terminal and execute the file like this: `python create_tables.py`
This file create all tables required for our schema, like staging table and the complete star-schema.

- Execute file _etl.py_. Following the same method as before. Execute the next file: `python etl.py`
After this, all copy statements to insert data into staging tables will be executed. This proccess can take a moment so please be patient.
After that, all insert statements will be executed to insert data into the star-schema.

## Aditional Information

`sql_queries.py`
This file contain all query statements like create tables, copy and insert.

`cluster_iac_config.ipynb`
IaC configuration to create a Cluster, IAM Role, Database and obtain files from a Bucket.


## Development

Want to contribute? Great! please feel free to open issues and push.
