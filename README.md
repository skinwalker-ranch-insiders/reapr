# reapr

A BIG THANKS to https://pypi.org/project/pytchat/ for making this happen.

johns67567 contributed the ability to send events to MySQL.

DATABASE SETUP:
```
$ docker pull mysql
$ docker run --name reapr-mysql --net=host -e MYSQL_ROOT_PASSWORD=your-sql-password -e MYSQL_USER=reapr_user -e MYSQL_PASSWORD=your-reapr-password -d mysql:latest
```
Connect to your new database server and create the database:
```
mysql> CREATE DATABASE reapr_database;
mysql> CREATE TABLE yt_events (id MEDIUMINT NOT NULL AUTO_INCREMENT, YT_Tag VARCHAR(30),
       YT_DateTime DATETIME, YT_User VARCHAR(60), YT_Msg VARCHAR(200), PRIMARY KEY (id));
```
Give your user access to this database with permission to write.
Save database hostname, database name, username and password for later

Dockerfile included:
```
$ screen
$ git clone git@github.com:skinwalker-ranch-insiders/reapr.git
$ cd reapr
$ mkdir /usr/src/reapr
$ cp reapr/* /usr/src/reapr
$ cd /usr/src/reapr
$ vi /usr/src/reapr/settings.py
```

Set the following variables:
```
db_server='ServerIP'
db_user='username'
db_passwd='password'
db_name='reaper_database'
```
Build andn run your REAPR container:
```
$ sudo docker build -t reapr
$ sudo docker run -it --name reapr --rm --volume $(pwd):/usr/src/reapr --net=host reapr:latest sh ./rcloak.sh [YouTube StreamID REQUIRED]
```
Once it is running you will see the follwing:
```
Starting REAPR - Reporting Events, Anomalous Phenomena and Requests
```
You should be up and running. Send a test event #EVENT: REAPR Test in YT Chat
of the Live Stream and it should pop on screen within a few moments.
```
EVENT: 2022-11-27 22:27:37 [Robert Davies] #EVENT: Example event.
```
To make sure it is reaching your database, connect to your database server:
```
mysql> USE reaper_database;
mysql> SELECT * FROM yt_events;
```
You should be able to see the #EVENT: you sent.
```
+-----+---------+---------------------+-------------------+-------------------------------------------------------------------------------+
| id  | YT_Tag  | YT_DateTime         | YT_User           | YT_Msg                                                                        |
+-----+---------+---------------------+-------------------+-------------------------------------------------------------------------------+
|   1 | EVENT   | 2022-11-27 22:27:37 | Robert Davies     | #EVENT: Example event.                                                        |
```
After validating that REAPR is receiving data and sending it to the database you can turn the container into a daemon:
```
sudo docker run -it --name reapr -d --rm --volume $(pwd):/usr/src/reapr --net=host reapr:latest sh ./rcloak.sh
```
Next install reapr-web: https://github.com/skinwalker-ranch-insiders/reapr-web
