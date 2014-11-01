#!/usr/bin/env hy
;;; FileName    : bjgj.hy
;;; Author      : ShuYu Wang <andelf@gmail.com>
;;; Created     : Wed Oct 22 20:51:12 2014 by ShuYu Wang
;;; Copyright   : Feather Workshop (c) 2014
;;; Description : Beijing Realtime Bus
;;; Time-stamp: <2014-11-01 16:13:07 andelf>

(import urllib2
        hashlib
        [lxml.etree :as ET])
(require hy.contrib.anaphoric)


(defclass Cipher [object]
  "encrypt & decrypt base64 data"
  [[--init--
    (fn [self key]
      (setv self.key (str key))
      None)]
   [new-from-key
    (with-decorator staticmethod
      (fn [key]
        (Cipher (+ "aibang" (str key)))))]
   [-make-translate-table
    (fn [self]
      (let [[key-bytes (-> self.key (hashlib.md5) (.hexdigest)
                           (bytearray "utf-8"))]
            [ret-val (list (range 256))]
            [k 0] [m 0]]
        (for [i (range 256)]
             (setv k (& 255 (+ k (get key-bytes m) (get ret-val i))))
             (setv [(get ret-val i) (get ret-val k)]
                   [(get ret-val k) (get ret-val i)])
             (setv m (% (+ 1 m) (len key-bytes))))
        ret-val))]
   [translate
    (fn [self raw]
      (let [[trans-table (self.-make-translate-table)]
            [raw-bytes (bytearray raw)]
            [ret-val (bytearray (len raw-bytes))]
            [j 0] [k 0]]
        (for [i (range (len raw-bytes))]
          (setv k (& 255 (+ k 1)))
          (setv j (& 255 (+ j (get trans-table k))))
          (setv [(get trans-table j) (get trans-table k)]
                [(get trans-table k) (get trans-table j)])
          (setv n (& 255 (+ (get trans-table k)
                            (get trans-table j))))
          (setv (get ret-val i) (^ (get raw-bytes i)
                                   (get trans-table n))))
        (str ret-val)))]
   [decrypt
    (fn [self cipher-text]
      (-> cipher-text
          (.decode "base64")
          (self.translate)))]
   [encrypt
    (fn [self plain-text]
      (-> plain-text
          (self.translate)
          (.encode "base64")))]])

(defn decrypt-busline-etree [et]
  (let [[busline (get (xpath-etree-children-to-dict-list "//busline" et) 0)]
        [stations (xpath-etree-children-to-dict-list "//busline/stations/station" et)]
        [cipher (Cipher.new-from-key (get busline "lineid"))]]
    (setv busline (apply dict [busline] (dict-comp k (.decode (cipher.decrypt v) "utf-8")
                                                   [(, k v) (busline.items)]
                                                   (in k ["shotname" "coord" "linename"]))))
    (setv stations (list (ap-map (dict-comp k (.decode (cipher.decrypt v) "utf-8" "replace") ; some line can't decode here.
                                            [(, k v) (it.items)])
                                 stations)))
    (assoc busline "stations" stations)
    busline))

(defn decrypt-bus-realtime-info [bus]
  (let [[cipher (Cipher.new-from-key (get bus "gt"))]]
    (apply dict [bus] (dict-comp k (.decode (cipher.decrypt v) "utf-8")
                                     [(, k v) (bus.items)]
                                     (in k ["ns" "nsn" "sd" "srt" "st" "x" "y"])))))


(defn etree-xpath-children-to-dict-list [et path]
  (xpath-etree-children-to-dict-list path et))

(defn xpath-etree-children-to-dict-list [path et]
  (list
   (ap-map (dict-comp elem.tag elem.text [elem (.getchildren it)]) (et.xpath path))))


(defclass BeijingBusApi [object]
  "Beijing Realtime Bus API."
  [[--init--
    (fn [self]
      (setv self.opener (urllib2.build_opener))
      (setv self.uid "233333333333333333333333333333333333333")
      (setv self.opener.addheaders
            [(, "SOURCE" "1") (, "PKG_SOURCE" "1") (, "OS" "android") (, "ROM"  "4.2.1")
             (, "RESOLUTION" "1280*720") (, "MANUFACTURER" "2013022") (, "MODEL" "2013022")
             (, "UA" "2013022,17,4.2.1,HBJ2.0,Unknown,1280*720")
             (, "IMSI" "233333333333333")
             (, "IMEI" "233333333333333")
             (, "UID" self.uid) (, "CID" self.uid)
             (, "PRODUCT" "nextbus") (, "PLATFORM" "android")
             (, "VERSION" "1.0.5") (, "FIRST_VERSION" "2")
             (, "PRODUCTID" "5") (, "VERSIONID" "2") (,"CUSTOM" "aibang")])
      None)]
   [api-open
    (fn [self path &optional [url-base "http://mc.aibang.com"]]
      (-> (+ url-base path) (self.opener.open) (.read)))]
   ;; <line><id>621</id><status>0</status><version>16</version></line
   [check-update
    ;; "fetch new line id and version"
    ;; {'status': 0, 'version': 3, 'id': 141}
    (fn [self]
      (->> (self.api-open "/aiguang/bjgj.c?m=checkUpdate&version=1")
          (ET.fromstring)
          (xpath-etree-children-to-dict-list "//line")
          (ap-map (dict-comp k (int v) [(, k v) (.items it)]))
          (list)))]
   [get-busline-info
    ;; "fetch busline detail info. name, stations, locations."
    (fn [self id &rest ids]
      (setv buslines (.xpath (->> (+ [id] (list ids))
                                  (map str)
                                  (.join "%2C")
                                  (.format "/aiguang/bjgj.c?m=update&id={0}")
                                  (self.api-open)
                                  (ET.fromstring))
                             "//busline"))
      (list (map decrypt-busline-etree buslines)))]
   [get-busline-realtime-info
    ;; "realtime bus location lookup. busline-id station-no"
    (fn [self id no]
      (list (ap-map (decrypt-bus-realtime-info it)
                    (-> (.format "/bus.php?city=%E5%8C%97%E4%BA%AC&id={0}&no={1}&type={2}&encrypt={3}&versionid=2"
                                 id no 1 1)
                        (self.api-open "http://bjgj.aibang.com:8899")
                        (ET.fromstring)
                        (etree-xpath-children-to-dict-list "//data/bus")
                        ))))]
   ])


(defn inspect [thing]
  (print "DEBUG" (repr thing) thing )
  thing)


(defmain [&rest args]
  (def b (BeijingBusApi))
  (-> (ap-map (get it "id")
              (-> (.check-update b) (inspect)))
      (list)
      (len)
      (print))
  (-> (b.get-busline-info 457)
      (print))
  ;; test decrypt
  ;; (-> (Cipher.new-from-key 1413772960)
  ;;     (.decrypt "ycCx9MhBlIC3XYEfN4ZZ")
  ;;     (print))
  (-> (b.get-busline-realtime-info 87 3)
      (print))
  0)
