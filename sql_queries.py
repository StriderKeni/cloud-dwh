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
    artist          VARCHAR,
    auth            VARCHAR,
    first_name      VARCHAR,
    gender          CHAR(2),
    item_session    INTEGER,
    last_name       VARCHAR,
    length          NUMERIC(18,0),
    level           VARCHAR,
    location        VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    NUMERIC(18,0),
    session_id      INTEGER,
    song            VARCHAR,
    status          INTEGER,
    ts              INT8,
    user_agent      TEXT,
    user_id         INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE stg_songs
(
    num_song            INTEGER,
    artist_id           VARCHAR,
    artist_latitude     NUMERIC(18,0),
    artist_longitude    NUMERIC(18,0),
    artist_location     VARCHAR,
    artist_name         VARCHAR,
    song_id             VARCHAR,
    title               VARCHAR,
    duration            NUMERIC(18,0),
    year                INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE songplays
(
    songplay_id     INTEGER     IDENTITY(1,1),
    start_time      TIMESTAMP   NOT NULL,
    user_id         VARCHAR     NOT NULL,
    level           VARCHAR(10),
    song_id         VARCHAR     NOT NULL,
    artist_id       VARCHAR     NOT NULL,
    session_id      VARCHAR,
    location        VARCHAR,
    user_agent      TEXT,
    PRIMARY KEY(songplay_id)
)  DISTKEY(user_id) SORTKEY(user_id)
""")

user_table_create = ("""
CREATE TABLE users
(
    user_id     INTEGER     NOT NULL,
    first_name  VARCHAR,
    last_name   VARCHAR,
    gender      CHAR(2),
    level       VARCHAR(10),
    PRIMARY KEY(user_id)
) DISTKEY(user_id) SORTKEY(user_id);
""")

song_table_create = ("""
CREATE TABLE songs
(
    song_id     VARCHAR         NOT NULL,
    title       VARCHAR,
    artist_id   VARCHAR         NOT NULL,
    year        INTEGER,
    duration    NUMERIC(18,0),
    PRIMARY KEY(song_id)
) DISTKEY(artist_id) SORTKEY(artist_id)
""")

artist_table_create = ("""
CREATE TABLE artists
(
    artist_id   VARCHAR         NOT NULL,
    name        VARCHAR,
    location    VARCHAR,
    lattitude   NUMERIC(18,0),
    longitude   NUMERIC(18,0),
    PRIMARY KEY(artist_id)
) DISTKEY(artist_id) SORTKEY(artist_id);
""")

time_table_create = ("""
CREATE TABLE time
(
    start_time  TIMESTAMP   NOT NULL,
    hour        INTEGER,
    week        INTEGER,
    month       INTEGER,
    year        INTEGER,
    weekday     INTEGER,
    PRIMARY KEY(start_time)
) DISTSTYLE ALL
""")

# STAGING TABLES

staging_events_copy = ("""
COPY stg_events FROM {}
credentials 'aws_iam_role={}'
compupdate off region 'us-west-2'
json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY stg_songs FROM {}
credentials 'aws_iam_role={}'
compupdate off region 'us-west-2'
FORMAT as JSON 'auto' TRUNCATECOLUMNS
blanksasnull emptyasnull maxerror 50000;
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

'''
No need to add DISTINCT for songplays table
because there's no duplicate data from joining events and songs staging tables.
'''

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT
(TIMESTAMP 'epoch' + events.ts/1000 * INTERVAL '1 Second') as start_time,
events.user_id,
events.level,
songs.song_id,
songs.artist_id,
events.session_id,
events.location,
events.user_agent
FROM stg_events events JOIN stg_songs songs ON (events.artist = songs.artist_name and events.song = songs.title)
WHERE page = 'NextSong'
AND user_id is not null;
""")


'''
The insert statement for users contains a ROW_NUMBER, this because there are a lot of
duplicate data from logs files. Order the data BY level DESC will allow to prioritize
paid level than free level.
'''

user_table_insert = ("""
INSERT INTO users
SELECT DISTINCT user_id, first_name, last_name, gender, level FROM (
SELECT user_id, ROW_NUMBER() OVER(PARTITION BY USER_ID ORDER BY level DESC) NUMB, first_name, last_name, gender, level
FROM public.stg_events) users_filter WHERE numb = 1 AND user_id IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs
SELECT DISTINCT song_id, title, artist_id, year, duration
FROM public.stg_songs;
""")

artist_table_insert = ("""
INSERT INTO artists
SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM public.stg_songs;
""")

time_table_insert = ("""
INSERT INTO time
SELECT DISTINCT
TS as START_TIME,
extract(hour FROM TS) as HOUR,
EXTRACT(WEEK FROM TS) as WEEK,
EXTRACT(MONTH FROM TS) as MONTH,
EXTRACT(YEAR FROM TS) as YEAR,
(EXTRACT(WEEKDAY FROM TS))+1 as WEEKDAY FROM
( select (TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 Second') as TS FROM public.stg_events
limit 10) A;
""")

# QUERY LISTS

table_list = ['stg_events', 'stg_songs', 'songplays', 'users', 'songs',
              'artists', 'time']

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create,
                        user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop,
                      user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
