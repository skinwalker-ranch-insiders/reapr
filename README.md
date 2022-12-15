# reapr

A BIG THANKS to https://pypi.org/project/pytchat/ for making this happen.

johns67467 contributed the ability to send events to MySQL.

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
s_login='email@address.com for insiders website'
s_password='password'
db_server='DB_SERVER_IP'
db_user='reapr_user'
db_passwd='your-reapr-password'
db_name='reapr_db'
sheet_id='Google Sheet ID'
```
Build andn run your REAPR container:
```
$ sudo docker build -t reapr
$ sudo docker run -it -name reapr --rm --volume $(pwd):/usr/src/reapr -net=host reapr:latest python3 ./rcloak.sh
```
If the script has timeout issues staying connected to chat, you may need REAPR's Cloak
rcloak.sh
```
#!/bin/sh
while true
do
   pgrep -f 'python3 ./reapr'>/dev/null
   if [[ $? -ne 0 ]] ; then
        echo "Restarting REAPR:     $(date)" >> ./reapr_restarts.txt
        /usr/local/bin/python3 ./reapr.py
   fi
done
```
Change permissions and run reapr's cloak:
```
/usr/src/reapr # chmod 755 ./rcloak.sh
/usr/src/reapr # ./rcloak.sh
```
You should be up and running. Send a test event '#EVENT: REAPR Test' in YT Chat and on your MySQL DB:
```
mysql> USE reaper_database;
mysql> SELECT * FROM yt_events;
```
Now that data collection is in progress, it is time to setup REAPR-web from https://github.com/skinwalker-ranch-insiders/reapr-web.
