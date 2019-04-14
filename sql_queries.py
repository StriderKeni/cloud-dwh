import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stg_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS stg_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""

CREATE TABLE stg_events
(
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(2),
    item_session INTEGER,
    last_name VARCHAR,
    length NUMERIC(18,0),
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration NUMERIC(18,0),
    session_id INTEGER,
    song VARCHAR,
    status INTEGER,
    ts INT8,
    user_agent TEXT,
    user_id INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE stg_songs
(
    num_song INTEGER,
    artist_id VARCHAR,
    artist_latitude NUMERIC(18,0),
    artist_longitude NUMERIC(18,0),
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration NUMERIC(18,0),
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE songplays
(
    songplay_id INTEGER,
    start_time INT8,
    user_id VARCHAR,
    level VARCHAR,
    song_id VARCHAR,
    session_id VARCHAR,
    location VARCHAR,
    user_agent TEXT
)
""")

user_table_create = ("""
CREATE TABLE users
(
    user_id VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(2),
    level VARCHAR(10)
)
""")

song_table_create = ("""
CREATE TABLE songs
(
    user_id VARCHAR,
    title VARCHAR,
    artist_id VARCHAR,
    year INTEGER,
    duration NUMERIC(18,0)
)
""")

artist_table_create = ("""
CREATE TABLE artists
(
    artist_id VARCHAR,
    name VARCHAR,
    location VARCHAR,
    lattitude NUMERIC(18,0),
    longitude NUMERIC(18,0)
)
""")

time_table_create = ("""
CREATE TABLE time
(
    start_time VARCHAR,
    hour INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY stg_events FROM {}
credentials 'aws_iam_role={}'
compupdate off region 'us-west-2'
json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY stg_songs FROM 's3://udacity-dend/song-data'
credentials 'aws_iam_role={}'
compupdate off region 'us-west-2'
FORMAT as JSON 'auto' TRUNCATECOLUMNS
blanksasnull emptyasnull maxerror 50000;
""").format(*config['IAM_ROLE'].values())

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""

""")

song_table_insert = ("""

""")

artist_table_insert = ("""

""")

time_table_insert = ("""

""")

# QUERY LISTS

table_list = ['songplays', 'users', 'songs', 'artists', 'time']  # ['stg_events'  # , 'stg_songs',


create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create, time_table_create]
# [staging_events_table_create, staging_songs_table_create,

drop_table_queries = [songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
# [staging_events_table_drop, staging_songs_table_drop,

copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
