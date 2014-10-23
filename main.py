#!/usr/bin/python
# -*- coding: utf-8 -*-


from bjgj import BeijingBusApi



def main():
    b = BeijingBusApi()

    # for id in b.check_update():
    #     line = b.get_busline_info(id['id'])[0]
    #     print line['linename'], line['time'], id['id']

    line = b.get_busline_info(535)[0]
    print line['linename'], line['time'], line
    print b.get_busline_realtime_info(535, 23)



if __name__ == '__main__':
    main()
