# Copyright (c) 2025 Juha Jouppi
# License: MIT

from datetime import date, timedelta

# funktiot voisi varmaan noutaa myös 5A-tehtävän koodista:
# from tulosta_viikko import lue_csv, pilko_ja_muunna, laske_paivasummat, hae_viikonpaiva, muotoile_tuloste

def lue_csv(tiedoston_nimi: str) -> list:
    """
    Avaa parametrina annetun csv-tiedoston ja palauttaa tietosisällön teksti-listana.

    Parametrit:
     tiedoston_nimi (str): luettavan csv-tiedoston nimi.

    Palauttaa:
     (list): palauttaa listan, jossa jokainen alkio on yksi rivi tiedostosta.
    """
    sisalto = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # Jätetään otsikkorivi huomiotta
        for rivi in f:
            sisalto.append(rivi)
    return sisalto

def pilko_ja_muunna(rivit: list) -> list:
    """
    Pilkkoo listaksi luetun csv-tiedoston rivit erotinmerkin mukaan ja tekee tietotyyppimuunnokset.
    
    Parametrit:
     rivit (list): tekstinä luetun csv-tiedoston rivit

    Palauttaa:
     (list): taulukko eli lista, jossa jokainen alkio on lista, jossa tarkoituksenmukaiset tietotyypit
    """
    taulukko = []
    for rivi in rivit:
        rivi = rivi.split(";")
        taulukko.append(
            [
                date.fromisoformat(rivi[0][:10]),
                int(rivi[1]),
                int(rivi[2]),
                int(rivi[3]),
                int(rivi[4]),
                int(rivi[5]),
                int(rivi[6])
            ]
        )
    return taulukko

def laske_paivasummat(taulukko: list) -> list:
    """
    Tekee päivätason summaukset taulukosta, jossa seitsemälle peräkkäiselle päivälle on useita rivejä.
    
    Parametrit:
     taulukko (list): tuntitasoinen data eli lista, jonka jokainen alkio on lista.

    Palauttaa:
     (list): päivätasolle summattu taulukko eli lista, jossa alkio jokaiselle viikonpäivälle.
    """
    # Aineiston perusteella oletetaan, että ensimmäisen rivin päiväys on myös järjestyksessä ensimmäinen
    # (Jos tätä epäiltäisiin, niin sortattaisiin ensin..)
    paiva1 = taulukko[0][0]
    # Alustetaan summataulukko
    summataulukko = []
    for i in range(7):
        summataulukko.append([
            (paiva1 + timedelta(days = i)),
            0,
            0,
            0,
            0,
            0,
            0
        ])
    # Käydään taulukko läpi rivi riviltä ja summataan vaihekohtaiset tiedot kunkin päivän osalta    
    for rivi in taulukko:
        paiva = int((rivi[0] - paiva1).days) # päiväindeksi
        # summataan rivin tiedot oikeiin alkioihin
        for i in range(1, 7):
            summataulukko[paiva][i] += rivi[i] 
    return summataulukko

def hae_viikonpaiva(paivamaara: date) -> str:
    """
    Palauttaa parametrinä annettavan päivämäärän viikonpäivän nimen.
    
    Parametrit:
     paivamaara (date): päivämäärä, jonka viikonpäivä halutaan tietää, date-luokkana.

    Palauttaa:
     (str): viikonpäivän nimen.
    """
    paivanumero = paivamaara.isoweekday()
    # Sanakirja viikonpäivistä
    viikonpaiva = {
        1: "Maanantai",
        2: "Tiistai",
        3: "Keskiviikko",
        4: "Torstai",
        5: "Perjantai",
        6: "Lauantai",
        7: "Sunnuntai"
    }
    return viikonpaiva.get(paivanumero, "Mahdotontai")

def muotoile_tuloste(taulukko: list) -> str:
    """
    Muotoilee parametrinä annettavan taulukon haluttuun tulostusmuotoon ja palauttaa sen tekstinä .
    
    Parametrit:
     taulukko (list): taulukkomuotoinen data, päivä- ja vaihekohtaiset kulutukset ja tuotot

    Palauttaa:
     (str): taulukon tiedot muotoiltuna tulosteeksi.
    """
    # Lisätään ensin otsikkotiedot
    tuloste =  "Päivä       Pvm            Kulutus [kWh]                 Tuotanto [kWh]\n"
    tuloste += "            pv.kk.vvvv     v1      v2      v3            v1      v2      v3\n"
    tuloste += "------------------------------------------------------------------------------"
    for rivi in taulukko:
        tuloste += f"\n{hae_viikonpaiva(rivi[0]):<12}"
        tuloste += f"{rivi[0]:%d.%m.%Y}    "
        for i in range(1, 7):
            luku = f"{(rivi[i]/1000):.2f}"         # muunnetaan Wh-> kWh, luvuksi ja pyöristetään
            luku = luku.replace(".", ",")          # korvataan desimaalipiste -pilkulla
            luku = f"{luku:>6}"
            if i == 3:                             # huomioidaan pidempi väli asettelussa tuotannon ja kulutuksen osalta
                tuloste += f"{luku:<14}"
            else:
                tuloste += f"{luku:<8}"
    return tuloste

def main():
    """
    Ohjelman pääfunktio: lukee datan, laskee viikkoyhteenvedot ja kirjoittaa raportin tiedostoon.
    """
    viikko41 = "\nViikon 41 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    viikko41 += muotoile_tuloste(laske_paivasummat(pilko_ja_muunna(lue_csv("viikko41.csv"))))
    viikko41 += "\n------------------------------------------------------------------------------\n"
    viikko42 = "\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    viikko42 += muotoile_tuloste(laske_paivasummat(pilko_ja_muunna(lue_csv("viikko42.csv"))))
    viikko42 += "\n------------------------------------------------------------------------------\n"
    viikko43 = "\nViikon 43 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    viikko43 += muotoile_tuloste(laske_paivasummat(pilko_ja_muunna(lue_csv("viikko43.csv"))))
    viikko43 += "\n------------------------------------------------------------------------------\n"
    
    tiedoston_nimi = "yhteenveto.txt"
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        f.write(viikko41)
        f.write(viikko42)
        f.write(viikko43)
    
    print(f"Raportti kirjoitettu tiedostoon {tiedoston_nimi}")


if __name__ == "__main__":
    main()