import requests
from bs4 import BeautifulSoup
# from dateutil.parser import parse
from pprint import pprint
import os
import json
from datetime import datetime
from .departmani_crawler import last_modified


# Moram ovaku da hardkodujem nazive smerova i linkove jer se nazivi na nastava.np.ac.rs ne poklapaju bas sa nazivima na dunp.np.ac.rs
# Negde neko slovo fali, negde malo drugacije i tako, to posle u bazi ne mogu da nadjem pod tim nazivom
smerovi_i_linkovi = [
    {
        "smer": "Pravo",
        "link": "http://nastava.np.ac.rs/nastava/index.php/pravne-nauke/2-uncategorised/25-sp-pravo-oas",
    },
    {
        "smer": "Ekonomija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/eko/12-sp-ekonomija",
    },
    {
        "smer": "Poslovna informatika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/eko/13-sp-poslovna-informatika",
    },
    {
        "smer": "Srpska književnost i jezik",
        "link": "http://nastava.np.ac.rs/nastava/index.php/filol/2-uncategorised/14-sp-srpska-knjizevnost-i-jezik",
    },
    {
        "smer": "Engleski jezik i književnost",
        "link": "http://nastava.np.ac.rs/nastava/index.php/filol/2-uncategorised/15-sp-engleski-jezik-i-knjizevnost",
    },
    {
        "smer": "Psihologija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/filoz/2-uncategorised/16-sp-psihologija",
    },
    {
        "smer": "Vaspitač u predškolskim ustanovama",
        "link": "http://nastava.np.ac.rs/nastava/index.php/filoz/2-uncategorised/19-sp-vaspitac-u-predskolskim-ustanovama",
    },
    {
        "smer": "Matematika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/mat/2-uncategorised/11-sp-mat",
    },
    {
        "smer": "Matematika - fizika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/mat/2-uncategorised/33-sp-matematika-fizika-oas",
    },
    {
        "smer": "Informatika - matematika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/mat/2-uncategorised/34-sp-informatika-matematika-oas",
    },
    {
        "smer": "Informatika - fizika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/mat/2-uncategorised/37-sp-informatika-fizika-oas",
    },
    {
        "smer": "Arhitektura",
        "link": "http://nastava.np.ac.rs/nastava/index.php/teh/2-uncategorised/40-sp-arhitektura-oas",
    },
    {
        "smer": "Gradjevinarstvo",
        "link": "http://nastava.np.ac.rs/nastava/index.php/teh/2-uncategorised/41-sp-gradjevinarstvo-oas",
    },
    {
        "smer": "Računarska tehnika",
        "link": "http://nastava.np.ac.rs/nastava/index.php/teh/2-uncategorised/42-sp-racunarska-tehnika-oas",
    },
    {
        "smer": "Audio i video tehnologija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/teh/2-uncategorised/45-sp-audio-i-video-tehnologija-oas",
    },
    {
        "smer": "Softversko inženjerstvo",
        "link": "http://nastava.np.ac.rs/nastava/index.php/teh/2-uncategorised/50-sp-softversko-inzenjerstvo-oas",
    },
    {
        "smer": "Hemija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/hemijsko-tehnoloske-nauke/2-uncategorised/52-sp-hemija-oas",
    },
    {
        "smer": "Poljoprivredna proizvodja",
        "link": "http://nastava.np.ac.rs/nastava/index.php/hemijsko-tehnoloske-nauke/2-uncategorised/55-sp-poljoprivredna-proizvodja-oas",
    },
    {
        "smer": "Biologija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/biomed/2-uncategorised/17-sp-biologija",
    },
    {
        "smer": "Rehabilitacija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/biomed/2-uncategorised/18-sp-rehabilitacija",
    },
    {
        "smer": "Sport i fizičko vaspitanje",
        "link": "http://nastava.np.ac.rs/nastava/index.php/biomed/2-uncategorised/20-sp-sport-i-fizicko-vaspitanje",
    },
    {
        "smer": "Likovna umetnost",
        "link": "http://nastava.np.ac.rs/nastava/index.php/ume/2-uncategorised/53-sp-umetnost-oas",
    },
    {
        "smer": "Prehrambena tehnologija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/bioteh/2-uncategorised/58-sp-prehrambena-tehnologija-oas",
    },
    {
        "smer": "Agronomija",
        "link": "http://nastava.np.ac.rs/nastava/index.php/bioteh/2-uncategorised/59-sp-agronomija-oas",
    },
]

headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

base_url = "http://nastava.np.ac.rs"

def fetchuj_sve_nastvne_matrijale():
    podaci = []
    for smer in smerovi_i_linkovi:
        try:
            print(f"Fetchujemo sve podatke za smer {smer['smer']}")
            linkovi = uzmi_sve_linkove(smer["link"], smer["smer"])
            podaci.extend(linkovi)
        except Exception as e:
            print(f"Greska prilikom fetchovanja nastavnog materijala: {e}")
    return podaci

def uzmi_sve_linkove(url, naziv_smera):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    linkovi = soup.select(".item-page a")
    podaci = []
    for a in linkovi:
        link = base_url + a["href"]
        try:
            podaci.append({
                # id(se podrazumeva), tip, naslov, opis, link, datum, hash
                "tip": "nastavni materijal",
                "naslov": f"Novi nastavni materijal za smer {naziv_smera}",
                "opis": a.getText(),
                "link": link,
                "datum": last_modified(link),
            })
        except Exception as e:
            print(f"Greska prilikom fetchovanja nastavnog materijala: {e}")

    return podaci

if __name__ == "__main__":
    temp = fetchuj_sve_nastvne_matrijale()
    # pprint(temp)