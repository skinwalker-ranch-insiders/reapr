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
$ sudo docker run -it -name reapr --rm --volume $(pwd):/usr/src/reapr -net=host reapr:latest sh
/usr/src/reapr # python3 ./reapr.py [YouTube StreamID REQUIRED]
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
        /usr/local/bin/python3 ./reapr.py $1
   fi
done
```
Change permissions and run reapr's cloak:
```
/usr/src/reapr # chmod 755 ./rcloak.sh
/usr/src/reapr # ./rcloak.sh
```
You should be up and running. Send a test event #EVENT: REAPR Test in YT Chat and 
```
mysql> USE reaper_database;
mysql> SELECT * FROM yt_events;
```
