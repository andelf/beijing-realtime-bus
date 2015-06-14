#!/usr/bin/python
# #  FileName    : draw.py
# #  Author      : ShuYu Wang <andelf@gmail.com>
# #  Created     : Sat Jun 13 22:35:50 2015 by ShuYu Wang
# #  Copyright   : Feather Workshop (c) 2015
# #  Description : description
# #  Time-stamp: <2015-06-14 23:39:12 andelf>


import psycopg2
import ppygis
from pylab import *

connection = psycopg2.connect("host=192.168.1.38 user=mmgis dbname=beijingbus")

print connection

cursor = connection.cursor()



sql = "SELECT bus.bus_id, ST_LineLocatePoint(route, bus.coords), bus.next_station_no, station.name, bus.gps_time FROM bus_line line INNER JOIN bus_realtime bus ON line.id = bus.line_id INNER JOIN bus_station station ON bus.next_station_no = station.no and line.id = station.line_id  WHERE bus.bus_id = 2113 and line.id = 113 ORDER BY gps_time"


# AND DATE '2015-06-13' + TIME '22:57' > bus.gps_time AND bus.gps_time > (DATE '2015-06-13' + TIME '22:00')
cursor.execute(sql)
print cursor.description

x = []
y = []
for row in cursor.fetchall():
    print row[-1]
    x.append(row[-1])           # gps_time
    y.append(row[1])            # ration

# plt.xkcd()
plt.plot_date(x, y, fmt="r+", tz='Asia/Chongqing')


sql = "SELECT ST_LineLocatePoint(route, station.coords), station.name from bus_station station INNER JOIN bus_line line ON station.line_id = line.id WHERE line.id = 113";
cursor.execute(sql)
for row in cursor.fetchall():
    position = row[0]
    name = row[1]
    plt.hlines(position, min(x), max(x), label = unicode(name, 'utf8'), color='y', linestyles='dashed')

plt.grid(True)
plt.xlabel('Time')
plt.ylabel('Route')
plt.title('Line 105, Down')
plt.show()
