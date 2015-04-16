# Beijing Realtime Bus 北京实时公交

少年不装逼何以平天下。

用 [Hy](http://docs.hylang.org/en/latest/) 写的。

逆向自客户端。

当然。。。增加了 Python 版本。

## 使用

``main.py``.

## API doc

所有座标为高德地图座标。

BeijingBusApi

```
- check_update()
  - [{'status': 状态, 'version': 线路版本号, 'id': 线路id}, ...]
- get_busline_info(线路id0, 线路id1, 线路id2, ...)
  - [{'status': 状态, 'totalPrice': 总价, 'stations': [{'lat': , 'lon': , 'name': 站名, 'no': 站号},...],
  -   'coord': 线路经纬度折线图,
  -   'shotname': 短站名, 'linename': 长站名, version': 线路版本号, 'time': 运营时间, 'distince': 线路全长, 'ticket': 票价,
  -   'lineid': 线路id, 'type': 线路类型}, ...]
- get_busline_realtime_info(线路id, 站号) 具体还不清楚
  - [{'gt': gpsupdateTime, 'nsn': nextStationNo, 'ut': ？更新时间, 'nsrt': nextStationRunTimes 距离下一站时间,
  -   'nsd': nextStationDistince, 'st': stationTime, 't': '1', 'srt': stationRunTimes,
  -   'y': , 'x': , 'ns': nextStation 下一站, 'nst': nextStationTime, 'id': BUS-id, 'sd': u'stationDistince'}, ...]
```

## TODO

* 部分站点有问题，如 id=273 , 站点名解析错误
