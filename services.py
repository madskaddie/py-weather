
import time
import urllib
from bs4 import BeautifulSoup

class Place(object):
    def __init__(self, code, description):
        self.code = code
        self.description = description
        return


class Services(object):

    @classmethod
    def add_place(cls, place, row):
        code = place.code
        cls.placeMap[code] = place
        cls.tableRows[code] = row

    placeMap = dict()
    tableRows = dict()

    def __init__(self, endpoint):
        self.endpoint = endpoint
        return

    def get_place_weather(self, placeCode):
        place = self.placeMap.get(placeCode)
        if place is None:
            return None
        url = self.endpoint + "/pt/html.prev.jsp"
        rsp = urllib.request.urlopen(url)
        data = rsp.read()
        text = data.decode('utf-8')

        doc = BeautifulSoup(text, 'html.parser')
        data_table = doc.findAll(attrs={'class':'tablelist'})[0]

        el = data_table.findAll('tr')
        rvalue = find_node(el, self.tableRows[place.code], time.localtime())
        return rvalue

Services.add_place(Place(1, 'Aveiro'), 0)

def find_node(tr_list, n, at):
    it = enumerate(tr_list)
    next(it); next(it)
    for i in range(0, n+1, 2):
        (idx, row) = next(it)
        children = row.findAll('td')
        tmin = children[3].string
        tmax = children[4].string
        if (i == n):
            if at.tm_hour > 12:
                (idx, row) = next(it)
                children = row.findAll('td')
                sky_state = children[1].string
                wind_state = children[2].string
                wind_dir = children[3].string
            else:
                sky_state = children[3].string
                wind_state = children[5].string
                wind_dir = children[6].string
            return (tmax,tmin, sky_state, wind_state, wind_dir)
            break
        next(it)
    return
            

