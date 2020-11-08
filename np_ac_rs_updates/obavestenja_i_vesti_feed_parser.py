import feedparser
import requests
from pprint import pprint
# from dateutil.parser import parse

# Moram ovo da ubacim u HTTP request inace mi vraca Error: 447
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

def uzmi_obavestenja_i_vesti():
    print("Pocinje parsovanje rss feeda sa dunp.np.ac.rs i izvlacenje podataka")
    obavestenja_i_vesti = []
    base_url = "http://www.dunp.np.ac.rs/feed/"
    r = requests.get(base_url, headers=headers)
    d = feedparser.parse(r.content)
    for item in d.entries:
        data = {
            #tip, naslov, opis, link, datum, hash
            "tip": item["tags"][0]["term"].lower(),
            "link": item["link"],
            "naslov": item["title"],
            "opis": item["summary"],
            "datum": item["published"],
        }
        obavestenja_i_vesti.append(data)
        # pprint(data)
        # print(data["datum"])
    print("Zavrseno parsovanje rss feeda sa dunp.np.ac.rs")
    return obavestenja_i_vesti
