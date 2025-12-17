# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

from datetime import datetime

def muunna_varaustiedot(varaus: list) -> dict:
    return {
        "id": int(varaus[0]),
        "nimi": varaus[1],
        "sähköposti": varaus[2],
        "puhelin": varaus[3],
        "pvm": datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        "klo": datetime.strptime(varaus[5], "%H:%M").time(),
        "kesto": int(varaus[6]),
        "hinta": float(varaus[7]),
        "vahvistettu": varaus[8].lower() == "true",
        "tila": varaus[9],
        "luotu": datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset:
        if(varaus["vahvistettu"]):
            print(f"- {varaus['nimi']}, {varaus['tila']}, {varaus['pvm'].strftime('%d.%m.%Y')} klo {varaus['klo'].strftime('%H.%M')}")

    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset:
        if(varaus['kesto'] >= 3):
            print(f"- {varaus['nimi']}, {varaus['pvm'].strftime('%d.%m.%Y')} klo {varaus['klo'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['tila']}")

    print()

def varausten_vahvistusstatus(varaukset: list):
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")

    print()

def varausten_lkm(varaukset: list):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    varaustenTulot = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            varaustenTulot += varaus[6]*varaus[7]

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    #varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    #varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()