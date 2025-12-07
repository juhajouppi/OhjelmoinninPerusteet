# Copyright (c) 2025 Juha Jouppi
# License: MIT

from datetime import date, timedelta

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
        print(f"{(paiva1 + timedelta(days = i)):%d.%m.%Y}")
    #for rivi in taulukko:
     #   if 
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


def main():
    """
    Ohjelman pääfunktio: lukee datan tiedostosta, käsittelee ja tulostaa raportin.
    """
    csv_sisalto = lue_csv("viikko42.csv")
    print(f"Eka rivi\n{csv_sisalto[0]}")
    viikonpaiva = hae_viikonpaiva(date.today())
    print(f"\nTänään on {viikonpaiva}")
    data = pilko_ja_muunna(csv_sisalto)
    print(f"\n{data[0]}")
    # print(f"\n{data[0][0].date():%d.%m.%Y}")
    koonti = laske_paivasummat(data)


if __name__ == "__main__":
    main()