# Copyright (c) 2025 Juha Jouppi
# License: MIT

from datetime import date, timedelta
# hyödynnetään funktion 5A-tehtävän koodista:
from tulosta_viikko import lue_csv, pilko_ja_muunna, laske_paivasummat, hae_viikonpaiva, muotoile_tuloste

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
    #print(viikko41)
    #print(viikko42)
    #print(viikko43)
    tiedoston_nimi = "yhteenveto_v2.txt"
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        f.write(viikko41)
        f.write(viikko42)
        f.write(viikko43)
    
    print(f"Raportti kirjoitettu tiedostoon {tiedoston_nimi}")


if __name__ == "__main__":
    main()