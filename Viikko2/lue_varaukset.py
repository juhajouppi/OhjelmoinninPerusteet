"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime, timedelta

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    # Pilkotaan varaus listaksi
    varaus = varaus.split('|')

    # Sijoitetaan varauksen kentät omiin oikeaa tyyppiä oleviin muuttujiinsa
    varausnumero = int(varaus[0])
    varaaja = varaus[1]
    paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    aika = datetime.strptime(varaus[3], "%H:%M").time()
    aloitus = datetime.combine(paiva, aika) # Muodostetaan kelvollinen aikaleima, helpottaa operointia
    kesto = int(varaus[4])    # Eikö kesto voi olla muutakuin tasatunteja 
    loppuu = aloitus + timedelta(hours = kesto) # Lasketaan varauksen päättymisaika
    tuntihinta = float(varaus[5])
    kokonaishinta = kesto * tuntihinta
    maksettu = bool(varaus[6])
    kohde = varaus[7]
    puhelin = varaus[8]
    email = varaus[9]

    # Tulostetaan tiedot konsoliin
    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaaja}")
    print(f"Päivämäärä: {aloitus:%d.%m.%Y}")
    print(f"Aloitusaika: {aloitus:%H.%M}")
    print(f"Tuntimäärä: {kesto}")
    print(f"Päättymisaika: {loppuu:%H.%M}")
    print(f"Tuntihinta: {tuntihinta:.2f} €".replace('.', ','))
    print(f"Kokonaishinta: {kokonaishinta:.2f} €".replace('.', ','))
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {email}")
    # Tulostetaan varaus konsoliin
    #print(varaus)

    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))
    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()