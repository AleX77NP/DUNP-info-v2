from .models import Novost
from dateutil.parser import parse
from .departmani_crawler import uzmi_sve_podatke_o_departmanima
from .obavestenja_i_vesti_feed_parser import uzmi_obavestenja_i_vesti
from .nastavni_materijali_crawler import fetchuj_sve_nastvne_matrijale
from .instagram_api.get_insta_posts import uzmi_sve_nove_instagram_postove
from .send_notifications import send_notification, send_notification_filter

# Ovaj modul uzima sve novosti sa np.ac.rs i instagrama i unosi ih u bazu ako su stvarno novi
# Da li je nesto novo ili ne odlucuje se razicitno za svaki tip novosti

def popuni_bazu():
    print('Zapocinje popunjavanje baze')
    sta_je_dodato_u_bazu = []
    novosti = []

    try:
        # Uzmi listu id-eva koje vec imam u bazi
        instagram_postovi_u_bazi = Novost.objects.filter(tip='instagram')
        id_postova_u_bazi = [x.hash_value for x in instagram_postovi_u_bazi]
        # Uzmi sve postove sa instagram profila spdunp
        instagram_postovi = uzmi_sve_nove_instagram_postove(id_postova_u_bazi)
        print('Uzimanje novih instagram postova zavrseno, novih postova ima: ' + str(len(instagram_postovi)))
        # Dodaj ih u listu novosti
        novosti.extend(instagram_postovi)
    except Exception as e:
        print(f'Greska prilkom uzimanja postova od spdunp sa instagrama: {e}')

    try:
        # Uzmi sve podatke sa departmana, rasporede ispita, rasporede predavanja, termine konsultacija, obavestenja...
        departmani = uzmi_sve_podatke_o_departmanima()
        novosti.extend(departmani)
    except Exception as e:
        print(f'Greska prilkom uzimanja svih podatak o departmanima: {e}')
    
    # try:
    #     # Uzmi sve nastavne materijale sa nastava.np.ac.rs
    #     nastavni_materijali = fetchuj_sve_nastvne_matrijale()
    #     novosti.extend(nastavni_materijali)
    # except Exception as e:
    #     print(f'Greska prilkom uzimanja nastavnih materijala: {e}')
    
    try:
        # Uzmi sva obavestenja i vesti iz rss feeda fakulteta
        obavestenja_i_vesti = uzmi_obavestenja_i_vesti()
        novosti.extend(obavestenja_i_vesti)
    except Exception as e:
        print(f'Greska prilkom uzimanja obavestenja i vesti iz rss feed-a: {e}')

    print('Svi podaci su preuzeti i izvodjeni')
    for novost in novosti:
        try:
            # U zavisnosti od tipa novosti razlicito se postupa sa njima
            tip_novosti = novost['tip']
            datum = parse(novost['datum'])
            if tip_novosti == 'raspored ispita' or tip_novosti == 'raspored predavanja' or tip_novosti == 'nastavni materijal':
                # Raspored ispita i raspored predavanja se dodaje u bazu samo ako ne postoji zapis koji ima isti link i isti datum
                # isto tako i za nastavni materijal
                q = Novost.objects.filter(link=novost['link'], datum=datum)
                if q.count() == 0:
                    sta_je_dodato_u_bazu.append(novost)
                    send_notification_filter(novost['naslov'], novost['opis'], novost['tip']) #kada dodje nova novost, posalji korisniku koji prati to...
                    n = Novost(tip=novost['tip'], naslov=novost['naslov'], opis=novost['opis'], link=novost['link'], datum=datum)
                    n.save()
            elif tip_novosti == 'obavestenja' or tip_novosti == 'vesti':
                # Obavestenja i vesti se dodaju u bazu samo ako ne postoji neki zapis sa takvim linkom, pretpostavlja se da su linkovi
                # uvek isti i jedinstveni za svaki item u rss feed-u odakle i vucem ove podatke
                q = Novost.objects.filter(link=novost['link'])
                if q.count() == 0:
                    sta_je_dodato_u_bazu.append(novost)
                    send_notification_filter(novost['naslov'], novost['opis'], novost['tip']) #kada dodje nova novost, posalji korisniku koji prati to...
                    n = Novost(tip=novost['tip'], naslov=novost['naslov'], opis=novost['naslov'], link=novost['link'], datum=datum)
                    n.save()
            elif tip_novosti == 'termini konsultacija' or tip_novosti == 'obavestenja smera':
                q = Novost.objects.filter(link=novost['link'], hash_value=novost['hash_value'])
                if q.count() == 0:
                    sta_je_dodato_u_bazu.append(novost)
                    send_notification_filter(novost['naslov'], novost['opis'], novost['tip']) #kada dodje nova novost, posalji korisniku koji prati to...
                    n = Novost(tip=novost['tip'], naslov=novost['naslov'], opis=novost['naslov'], link=novost['link'], datum=datum, hash_value=novost['hash_value'])
                    n.save()
            elif tip_novosti == 'instagram':
                send_notification_filter(novost['naslov'], novost['opis'], novost['tip']) #kada dodje nova novost, posalji korisniku koji prati to...
                n = Novost(tip=novost['tip'], naslov=novost['naslov'], opis=novost['opis'], link=novost['link'], datum=datum, hash_value=novost['id'])
                n.save()
        except Exception as e:
            print(f'Greska prilikom dodavanja novosti u bazu: {e}')
    # print(f'Ovo je iz funkcije popuni_bazu(): {sta_je_dodato_u_bazu}')
    print('Azuriranje baze uspesno zavrseno!')
    return sta_je_dodato_u_bazu

if __name__ == '__main__':
    novosti = popuni_bazu()
    print(novosti)