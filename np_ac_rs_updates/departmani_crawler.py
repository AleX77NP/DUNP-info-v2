import requests
from bs4 import BeautifulSoup
# from dateutil.parser import parse
from pprint import pprint
import os
import json
from datetime import datetime
import hashlib

# Moram ovo da ubacim u HTTP request inace mi vraca Error: 447
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

base_url = "http://www.dunp.np.ac.rs/"

# vraca sve 'a' html elemente koje nadje na pocetnoj stranici sajta fakulteta u meniju koji sadrzi departmane
def svi_departmani():
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    departmani = soup.select("#menu-meni-departmani-pocetna a")
    # pprint(departmani)
    return departmani

# vraca sve 'a' html elemente nekog departmana
def sve_sekcije_departmana(url_departmana):
    r = requests.get(url_departmana, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    sekcije = soup.select(".gdlr-core-sidebar-item a")
    # pprint(sekcije)
    return sekcije

# ovo koliko ja vidim radi samo za raspored predavanja i raspored ispita
def svi_linkovi_na_stranici(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    rasporedi_ispta = soup.select(".gdlr-core-pbf-column-content a")
    # pprint(rasporedi_ispta)
    return rasporedi_ispta

# vraca last modified header field za neki url
def last_modified(url):
    r = requests.head(url, headers=headers)
    if (r.status_code == 200):
        return r.headers["last-modified"]
    else:
        raise Exception(f"Greska prilikom slanja zahteva url-u {url} sa metodom HEAD da bi uzeo last-modified!")

def nadji_sve_rasporede(sekcija):
    if sekcija.text != "Raspored ispita" and sekcija.text != "Raspored predavanja":
        raise Exception("Ovo radi samo za rasporede ispita i rasporede predavanja!")

    podaci = []
    rasporedi = svi_linkovi_na_stranici(sekcija["href"])
    for raspored in rasporedi:
        # Da izbacim neke nepotrebne karaktere iz naziva smera
        smer = raspored.text
        smer = smer.replace('\xa0', '').replace('←', '')

        url = raspored["href"]
        podaci.append({
            # id(se podrazumeva), tip, naslov, opis, link, datum, hash
            "tip": sekcija.text.lower(),
            "naslov": f"Novi {sekcija.text.lower()} za smer {smer}",
            "opis": f"Novi {sekcija.text.lower()} za smer {smer}",
            "link": url,
            "datum": last_modified(url),
        })
    return podaci

def uzmi_hash_contenta(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.select(".kingster-page-wrapper")[0]
    # Sad sam izvojio div u kojem se nalaze ceo sadrzaj koji mene interesuje
    # Da ne bih sad previse komplikovao stvari, ja cu ceo taj sadrzaj da heshujem
    # i taj hash value da pamtim u bazi, i na osnovu njega cu da znam da li je doslo do promene sarzaja
    hash_value = hashlib.md5(str(div.contents).encode("utf-8")).hexdigest()
    return hash_value

def nadji_termine_kosultacija(sekcija, departman):
    if sekcija.text != "Termini konsultacija":
        raise Exception("Ovo radi samo za termine konsultacija!")

    # Otvori stranicu na kojoj se nalaze termini konsultacija, izdvoji vazni sadrzaj i heshuj ga
    hash_value = uzmi_hash_contenta(sekcija["href"])
    return {
        "tip": sekcija.text.lower(),
        "naslov": f"Novi {sekcija.text.lower()} za departman {departman.text}",
        "opis": "",
        "link": sekcija["href"],
        "datum": str(datetime.now()) + " GMT",
        "hash_value": hash_value,
    }

def nadji_sva_obavestenja(sekcija):
    if sekcija.text != "Obaveštenja" and sekcija.text != "Obaveštenje":
        raise Exception("Ovo radi samo za obavestenja!")

    podaci = []
    # Otvori stranicu na kojoj se nalaze linkovi ka obavestenjima svih smerova
    r = requests.get(sekcija["href"], headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    linkovi_ka_smerovima = soup.select(".gdlr-core-text-box-item-content a")
    if len(linkovi_ka_smerovima) == 0: # To znaci da direktno otvara obavestenja a ne izbor smera
        smer = soup.select(".kingster-page-title")[0].text[12:]
        podaci.append({
            "tip": "obavestenja smera",
            "naslov": f"Nova obavestenja za smer {smer}",
            "opis": "",
            "link": sekcija["href"],
            "datum": str(datetime.now()) + " GMT",
            "hash_value": uzmi_hash_contenta(sekcija["href"]),
        })
    else: # Prodji kroz sve linkove ka smerovima i uzmi odatle podatke
        for a in linkovi_ka_smerovima:
            smer = a.text.replace('\xa0', '').replace('←', '')
            podaci.append({
                "tip": "obavestenja smera",
                "naslov": f"Nova obavestenja za smer {smer}",
                "opis": "",
                "link": a["href"],
                "datum": str(datetime.now()) + " GMT",
                "hash_value": uzmi_hash_contenta(a["href"]),
            })
    return podaci

def spdunp_instagram():
    podaci = []
    url = "https://www.instagram.com/spdunp/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    posts = soup.select(".v1Nh3")
    pprint(posts)
    return podaci

def uzmi_sve_podatke_o_departmanima():
    podaci = []
    trenutno_vreme = datetime.now()

    departmani = svi_departmani()
    for departman in departmani:
        sekcije = sve_sekcije_departmana(departman["href"])
        for sekcija in sekcije:
            try:
                if sekcija.text == "Raspored ispita" or sekcija.text == "Raspored predavanja":
                    print(f"Pretrazuje se {sekcija.text} za departman {departman.text} link je {sekcija['href']}")
                    rasporedi = nadji_sve_rasporede(sekcija)
                    podaci.extend(rasporedi)
                elif sekcija.text == "Termini konsultacija":
                    print(f"Pretrazuje se {sekcija.text} za departman {departman.text} link je {sekcija['href']}")
                    podaci.append(nadji_termine_kosultacija(sekcija, departman))
                elif sekcija.text == "Obaveštenja" or sekcija.text == "Obaveštenje":
                    print(f"Pretrazuje se {sekcija.text} za departman {departman.text} link je {sekcija['href']}")
                    obavestenja_smera = nadji_sva_obavestenja(sekcija)
                    podaci.extend(obavestenja_smera)
            except Exception as e:
                print(f"Greska u crawlowanju {sekcija.text} za departman {departman.text} : {e}")
            
    # pprint(podaci)
    return podaci

if __name__ == "__main__":
    # uzmi_sve_podatke_o_departmanima()
    # spdunp_instagram()
    temp = uzmi_sve_podatke_o_departmanima()
    pprint(temp)