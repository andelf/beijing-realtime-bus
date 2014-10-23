from hy.core.language import is_integer, map, range
import urllib2
import hashlib
import lxml.etree as ET


class Cipher(object):
    __doc__ = u'encrypt & decrypt base64 data'

    def __init__(self, key):
        self.key = str(key)
        self.key
        return None

    @staticmethod
    def new_from_key(key):
        return Cipher((u'aibang' + str(key)))

    def _make_translate_table(self):

        def _hy_anon_fn_3():
            key_bytes = bytearray(hashlib.md5(self.key).hexdigest(), u'utf-8')
            ret_val = list(range(256L))
            k = 0L
            m = 0L
            for i in range(256L):
                k = (255L & ((k + key_bytes[m]) + ret_val[i]))
                [ret_val[i], ret_val[k]] = [ret_val[k], ret_val[i]]
                [ret_val[i], ret_val[k]]
                m = ((1L + m) % len(key_bytes))
            return ret_val
        return _hy_anon_fn_3()

    def translate(self, raw):

        def _hy_anon_fn_5():
            trans_table = self._make_translate_table()
            raw_bytes = bytearray(raw)
            ret_val = bytearray(len(raw_bytes))
            j = 0L
            k = 0L
            for i in range(len(raw_bytes)):
                k = (255L & (k + 1L))
                j = (255L & (j + trans_table[k]))
                [trans_table[j], trans_table[k]] = [trans_table[k], trans_table[j]]
                [trans_table[j], trans_table[k]]
                n = (255L & (trans_table[k] + trans_table[j]))
                ret_val[i] = (raw_bytes[i] ^ trans_table[n])
                ret_val[i]
            return str(ret_val)
        return _hy_anon_fn_5()

    def decrypt(self, cipher_text):
        return self.translate(cipher_text.decode(u'base64'))

    def encrypt(self, plain_text):
        return self.translate(plain_text).encode(u'base64')

def decrypt_busline_info(busline):

    def _hy_anon_fn_9():
        cipher = Cipher.new_from_key(busline[u'lineid'])
        return dict(*[busline], **{k: cipher.decrypt(v).decode(u'utf-8') for (k, v) in busline.items() if (k in [u'shotname', u'coord', u'linename'])})
    return _hy_anon_fn_9()

def decrypt_bus_realtime_info(bus):

    def _hy_anon_fn_11():
        cipher = Cipher.new_from_key(bus[u'gt'])
        return dict(*[bus], **{k: cipher.decrypt(v).decode(u'utf-8') for (k, v) in bus.items() if (k in [u'ns', u'nsn', u'sd', u'srt', u'st', u'x', u'y'])})
    return _hy_anon_fn_11()

def etree_xpath_children_to_dict_list(et, path):

    def _hy_anon_fn_13():
        f_1236 = (lambda it: {elem.tag: elem.text for elem in it.getchildren()})
        for v_1235 in et.xpath(path):
            yield f_1236(v_1235)
    return list(_hy_anon_fn_13())

def xpath_etree_children_to_dict_list(path, et):

    def _hy_anon_fn_15():
        f_1238 = (lambda it: {elem.tag: elem.text for elem in it.getchildren()})
        for v_1237 in et.xpath(path):
            yield f_1238(v_1237)
    return list(_hy_anon_fn_15())


class BeijingBusApi(object):
    __doc__ = u'Beijing Realtime Bus API.'

    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener
        self.uid = u'233333333333333333333333333333333333333'
        self.uid
        self.opener.addheaders = [(u'SOURCE', u'1'), (u'PKG_SOURCE', u'1'), (u'OS', u'android'), (u'ROM', u'4.2.1'), (u'RESOLUTION', u'1280*720'), (u'MANUFACTURER', u'2013022'), (u'MODEL', u'2013022'), (u'UA', u'2013022,17,4.2.1,HBJ2.0,Unknown,1280*720'), (u'IMSI', u'233333333333333'), (u'IMEI', u'233333333333333'), (u'UID', self.uid), (u'CID', self.uid), (u'PRODUCT', u'nextbus'), (u'PLATFORM', u'android'), (u'VERSION', u'1.0.5'), (u'FIRST_VERSION', u'2'), (u'PRODUCTID', u'5'), (u'VERSIONID', u'2'), (u'CUSTOM', u'aibang')]
        self.opener.addheaders
        return None

    def api_open(self, path, url_base=u'http://mc.aibang.com'):
        return self.opener.open((url_base + path)).read()

    def check_update(self):

        def _hy_anon_fn_19():
            f_1240 = (lambda it: {k: int(v) for (k, v) in it.items()})
            for v_1239 in xpath_etree_children_to_dict_list(u'//line', ET.fromstring(self.api_open(u'/aiguang/bjgj.c?m=checkUpdate&version=1'))):
                yield f_1240(v_1239)
        return list(_hy_anon_fn_19())

    def get_busline_info(self, id, *ids):
        return list(map(decrypt_busline_info, xpath_etree_children_to_dict_list(u'//busline', ET.fromstring(self.api_open(u'/aiguang/bjgj.c?m=update&id={0}'.format(u'%2C'.join(map(str, ([id] + list(ids))))))))))

    def get_busline_realtime_info(self, id, no):

        def _hy_anon_fn_22():
            f_1242 = (lambda it: decrypt_bus_realtime_info(it))
            for v_1241 in etree_xpath_children_to_dict_list(ET.fromstring(self.api_open(u'/bus.php?city=%E5%8C%97%E4%BA%AC&id={0}&no={1}&type={2}&encrypt={3}&versionid=2'.format(id, no, 1L, 1L), u'http://bjgj.aibang.com:8899')), u'//data/bus'):
                yield f_1242(v_1241)
        return list(_hy_anon_fn_22())

def inspect(thing):
    print(u'DEBUG', thing)
    return thing

def main(*args):
    b = BeijingBusApi()

    def _hy_anon_fn_25():
        f_1245 = (lambda it: it[u'id'])
        for v_1244 in inspect(b.check_update()):
            yield f_1245(v_1244)
    print(len(list(_hy_anon_fn_25())))
    print(b.get_busline_info(457L, 273L))
    print(Cipher.new_from_key(1413772960L).decrypt(u'ycCx9MhBlIC3XYEfN4ZZ'))
    print(b.get_busline_realtime_info(87L, 3L))
    return 0L
if (__name__ == u'__main__'):
    import sys
    G_1243 = main(*sys.argv)
    _hy_anon_var_1 = (sys.exit(G_1243) if is_integer(G_1243) else None)
else:
    _hy_anon_var_1 = None
