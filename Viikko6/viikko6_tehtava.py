# Copyright (c) 2025 Juha Jouppi
# License: MIT

from datetime import date, datetime

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
                float(rivi[1].replace(",", ".")),
                float(rivi[2].replace(",", ".")),
                float(rivi[3].replace(",", "."))
            ]
        )
    return taulukko

def nayta_valikko(taso: int) -> int:
    """
    Tulostaa valikon, pyytää valinnan, tarkistaa syötteen kelpoisuuden ja palauttaa käyttäjän valinnan lukuna.
    
    Parametrit:
     taso (int): 1 -> Päävalikko, 2 -> toinen valikko, muilla arvoilla palauttaa -1

    Palauttaa:
     (int): Käyttäjän valitsema toiminto numerona (tai -1 jos virheellinen parametri)
    """
    if taso == 1:
        print("Valitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
        print("3) Koko vuoden yhteenveto")
        print("4) Lopeta ohjelma")
        valintoja = 4
    elif taso == 2:
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Kirjoita raportti tiedostoon raportti.txt")
        print("2) Luo uusi raportti")
        print("3) Lopeta")
        valintoja = 3
    else:
        return -1        # Palautetaan -1 merkiksi virheellisestä parametrista
    syote_ok = False
    while not syote_ok:
        syote = input("Anna valinta: ")
        try:
            syote = int(syote)
        except:
            print(f"Tuo ei ollut numero, yritä uudestaan")
        else:
            if syote >= 1 and syote <= valintoja:
                syote_ok = True
            else:
                print(f"Valinta pitäisi olla numero väliltä 1-{valintoja} !")
    return syote

def pyyda_pvm(kehoite: str) -> date:
    """
    Pyytää käyttäjältä päivämäärän muodossa pv.kk.vvvv parametrina annettavan saatetekstin saattelemana.
    Tarkistetaan, että syöte on kelvollinen ja palautetaan päivämäärämuodossa.
    
    Parametrit:
     kehoite (str): kehoiteteksti käyttäjälle.

    Palauttaa:
     (date): käyttäjän syötteen kelvollisessa päivämäärämuodossa.
    """
    syote_ok = False
    while not syote_ok:
        syote = input(kehoite)
        try:
            syote = datetime.strptime(syote, "%d.%m.%Y").date()
        except:
            print(f"Tuo ei ollut kelvollinen päivämäärä (pv.kk.vvvv), yritä uudelleen")
        else:
            syote_ok = True
    return syote

def paivakohtainen_raportti(taulukko: list) -> str:
    """
    Pyytää käyttäjältä alku- ja loppupäivämäärät, laskee päivämäärien perusteella parametrina annetusta taulukosta
    kulutukset ja tuotot yhteensä sekä keskilämpötilojen keskiarvon. Lasketut tiedot palautetaan tulostettavana
    tekstinä.
    
    Parametrit:
     taulukko (list): tuotanto/kulutusdata eli lista, jonka jokainen alkio on lista.

    Palauttaa:
     (str): laskettu yhteenveto raporttimuodossa.
    """
    while True:
        alku_pvm = pyyda_pvm("Anna alkupäivä (pv.kk.vvvv)\n")
        loppu_pvm = pyyda_pvm("Anna loppupäivä (pv.kk.vvvv)\n")
        if alku_pvm > loppu_pvm:
            print("Alkupäivän pitäisi olla ennen loppupäivää. Yritä uudelleen, ole hyvä!")
            continue
        else:
            break
    kulutus = 0
    tuotanto = 0
    lampotila = 0
    paivalaskuri = 0
    for rivi in taulukko:
        if rivi[0] >= alku_pvm and rivi[0] <= loppu_pvm:
            kulutus += rivi[1]
            tuotanto += rivi[2]
            lampotila += rivi[3]
            paivalaskuri += 1
    kulutus = f"{kulutus:.2f}".replace(".", ",")
    tuotanto = f"{tuotanto:.2f}".replace(".", ",")
    lampotila = f"{(lampotila/paivalaskuri):.2}".replace(".", ",")
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti väliltä {alku_pvm:%d.%m.%Y}-{loppu_pvm:%d.%m.%Y}\n"
    raportti += f"Sähkön kulutus:  {kulutus} kWh\n"
    raportti += f"Sähkön tuotanto: {tuotanto} kWh\n"
    raportti += f"Jakson keskilämpötila: {lampotila} °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

def kuukausiraportti(taulukko: list) -> str:
    """
    Pyytää käyttäjältä kuukauden numerona, laskee sen perusteella parametrina annetusta taulukosta
    kulutukset ja tuotot yhteensä sekä keskilämpötilojen keskiarvon. Lasketut tiedot palautetaan tulostettavana
    tekstinä.
    
    Parametrit:
     taulukko (list): tuotanto/kulutusdata eli lista, jonka jokainen alkio on lista.

    Palauttaa:
     (str): laskettu yhteenveto raporttimuodossa.
    """
    # Sanakirja kuukausista
    kuukausi = {
        1: "Tammikuu",
        2: "Helmikuu",
        3: "Maaliskuu",
        4: "Huhtikuu",
        5: "Toukokuu",
        6: "Kesäkuu",
        7: "Heinäkuu",
        8: "Elokuu",
        9: "Syyskuu",
        10: "Lokakuu",
        11: "Marraskuu",
        12: "Joulukuu"
    }
    syote_ok = False
    while not syote_ok:
        syote = input("Anna kuukausi numerona (1-12): ")
        try:
            syote = int(syote)
        except:
            print(f"Tuo ei ollut numero, yritä uudestaan")
        else:
            if syote >= 1 and syote <= 12:
                syote_ok = True
            else:
                print(f"Kuukausi pitäisi olla numero väliltä 1-12 !")
    kulutus = 0
    tuotanto = 0
    lampotila = 0
    paivalaskuri = 0
    for rivi in taulukko:
        if rivi[0].month == syote:
            kulutus += rivi[1]
            tuotanto += rivi[2]
            lampotila += rivi[3]
            paivalaskuri += 1
    kulutus = f"{kulutus:.2f}".replace(".", ",")
    tuotanto = f"{tuotanto:.2f}".replace(".", ",")
    lampotila = f"{(lampotila/paivalaskuri):.2}".replace(".", ",")
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti kuukaudelta: {kuukausi.get(syote)}\n"
    raportti += f"Sähkön kulutus:  {kulutus} kWh\n"
    raportti += f"Sähkön tuotanto: {tuotanto} kWh\n"
    raportti += f"Jakson keskilämpötila: {lampotila} °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

def vuosiraportti(taulukko: list) -> str:
    """
    Laskee parametrina annetusta taulukosta kulutukset ja tuotot yhteensä sekä keskilämpötilojen
    keskiarvon. Lasketut tiedot palautetaan tulostettavana tekstinä.
    
    Parametrit:
     taulukko (list): tuotanto/kulutusdata eli lista, jonka jokainen alkio on lista.

    Palauttaa:
     (str): laskettu yhteenveto raporttimuodossa.
    """
    kulutus = 0
    tuotanto = 0
    lampotila = 0
    paivalaskuri = 0
    for rivi in taulukko:
        kulutus += rivi[1]
        tuotanto += rivi[2]
        lampotila += rivi[3]
        paivalaskuri += 1
    kulutus = f"{kulutus:.2f}".replace(".", ",")
    tuotanto = f"{tuotanto:.2f}".replace(".", ",")
    lampotila = f"{(lampotila/paivalaskuri):.2}".replace(".", ",")
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti vuodelta {taulukko[0][0].year}\n"
    raportti += f"Sähkön kulutus:  {kulutus} kWh\n"
    raportti += f"Sähkön tuotanto: {tuotanto} kWh\n"
    raportti += f"Jakson keskilämpötila: {lampotila} °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

def main():
    """
    Ohjelman pääfunktio: lukee datan, näyttää valikot ja ohjaa raporttien luomista.
    """
    # Luetaan ensin csv-tiedosto ja taulukoidaan data
    data = pilko_ja_muunna(lue_csv("2025.csv"))
    # Alustetaan raportti
    raportti = ""
    # Siirrytään ohjelmasilmukkaan
    while True:
        # Aloitetaan valikosta 1
        valinta = nayta_valikko(1)
        if valinta == 1:
            # Raportti käyttäjän antamalta päivämääräväliltä
            raportti = paivakohtainen_raportti(data)
            print(raportti)
        elif valinta == 2:
            # Raportti käyttäjän valitsemalta kuukaudelta
            raportti = kuukausiraportti(data)
            print(raportti)
        elif valinta == 3:
            # Raportti koko datasta/vuodelta
            raportti = vuosiraportti(data)
            print(raportti)
        elif valinta == 4:    
            # Ohjelman lopetus
            break
        # Raportti näytetty, siirrytään valikkoon 2
        valinta = nayta_valikko(2)
        if valinta == 1:
            # Raportin tallennus tekstitiedostoon ja paluu alkuun
            with open("raportti.txt", "w", encoding="utf-8") as f:
                f.write(raportti)
            print(f"Raportti kirjoitettu tiedostoon\nPalataan alkuun")
            continue
        elif valinta == 2:
            # Paluu valikkoon 1
            print(f"Takaisin alkuun")
            continue
        elif valinta == 3:   
            # Ohjelman lopetus
            break

if __name__ == "__main__":
    main()