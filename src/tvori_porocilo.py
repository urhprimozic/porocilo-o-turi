from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import pandas as pd
from datetime import datetime

tabela_vzponi = "../example/demo_vzponi.csv"
tabela_porocila = "../example/porocila.csv"

polja = [ "Datum", "Gorstvo", "Gora", "Smer", "Ocena", "Višina smeri", "Soplezalec", "Opremljenost", "Opombe"]

def pripravi_porocilo( ime_porocila : str, df_vzponi : pd.DataFrame, df_porocila : pd.DataFrame, datum_porocila : str):
    """
    Vrne markdown string s poročilom.

    Parameters
    ----------
    ime_porocila : str
        Ime poročila
    df_vzponi : pd.DataFrame
        DataFrame z vzponi
    df_porocila : pd.DataFrame
        DataFrame s poročili
    
    Returns
    --------
    porocilo : str 
        Celotno poročilo
    """ 
    # preberi uporabnika
    ime_priimek =  df_vzponi["Uporabnik"][0]
    # odstrani vzpone iz ostalih porocil
    df_vzponi = df_vzponi[df_vzponi["Porocilo"] == ime_porocila]
    # izbriši prvi stolpec in stolpes s poročili 
    df_vzponi = df_vzponi.drop(["Uporabnik", "Porocilo"], axis = 1)

    #da ni preširoko: vzemi samo sledeča polja:
    df_vzponi = df_vzponi[polja]

    # vzpone hočmo dat v tabelco v makrownu - lahko uporabiš trik, da exportaš v csv
    #path=None za string, sep = "|", ker to hočeš za markdown tabelco, na_rep="", da je tabela ob praznih vrednostih prazna. index=False, da ni dodatnega stolpca z indeksi
    opravljeni_vzponi = df_vzponi.to_csv(path_or_buf=None, sep='|', na_rep='', index=False, header=False)

    # remove "nan" 
    df_porocila = df_porocila.fillna("0")
    
    # parse other data 
    podatki = df_porocila[df_porocila["Poročilo"] == ime_porocila]
    st_km = str(podatki["Število prevoženih km"].item())
    cestnine= str(podatki["Stroški cestnin"].item())
    parkirnine= str(podatki["Stroški parkirnin"].item())
    ostali_stroski= str(podatki["Ostali stroški"].item())

    glava_tabele = "| " + " | ".join(polja) + "|\n|" + ("---------|" * 9)

    #porocilo = f"### Poročilo o opravljenih vzponih\n### Članica/član: {ime_priimek}\n## {ime_porocila}\n\n### Opravljeni vzponi \n| Datum | Država | Gorstvo | Gora | Orientacija stene | Plezališče | Smer | Ocena | Ocena najtežjega mesta | Višina smeri | Nadmorska višina izstopa | Čas | Soplezalec | Način plezanja | Vloga v navezi | Opremljenost | Opombe | Komentar |\n| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |\n{opravljeni_vzponi}\n\n### Okvirni stroški\n- **Število prevoženih km:** {st_km}\n- **Stroški cestnin:** {cestnine}\n- **Stroški parkirnin:** {parkirnine}\n- **Ostali stroški:** {ostali_stroski}\n\n**Datum poročila:** {datum_porocila}\n\n___________\n*Podpis*\n{ime_priimek} "
    porocilo = f"### Poročilo o opravljenih vzponih\n### Članica/član: {ime_priimek}\n## {ime_porocila}\n\n### Opravljeni vzponi \n{glava_tabele}\n{opravljeni_vzponi}\n\n### Okvirni stroški\n- **Število prevoženih km:** {st_km}\n- **Stroški cestnin:** {cestnine}\n- **Stroški parkirnin:** {parkirnine}\n- **Ostali stroški:** {ostali_stroski}\n\n**Datum poročila:** {datum_porocila}\n\n___________\n*Podpis*\n{ime_priimek} "
    return porocilo

def izvozi_porocilo( ime_porocila : str, df_vzponi : pd.DataFrame, df_porocila : pd.DataFrame, pdf=True):
    """
    Shrani pripravljeno poročilo v ../porocila/ime_porocila.md
    """
    porocilo = pripravi_porocilo(ime_porocila, df_vzponi, df_porocila,  datetime.today().strftime('%d.%m.%Y'))
    if pdf:
        mdpdf = MarkdownPdf(toc_level=2)
        mdpdf.add_section(Section( porocilo, toc=False))
        mdpdf.save(f'../porocila/{ime_porocila}.pdf')

    else:
        with open(f'../porocila/{ime_porocila}.md', "w") as f:
            f.write(porocilo)
    print(f"Uspešno shranil poročilo {ime_porocila}!" )

def izvozi_vsa_porocila(tabela_vzponi : str, tabela_porocila : str):
    """
    Shrani vsa poročila vzponov.

    Parametri
    -----------
    tabela_vzponi : str
        lokacija datoteke z vzponi. Primer: "example/demo_porocilo.csv" 
    tabela_porocila : str
        lokacija datoteke s seznamom poročil 

    TODO podroben opis
    """
    # preberi tabeli
    df_vzponi = pd.read_csv(tabela_vzponi)
    df_porocila = pd.read_csv(tabela_porocila)
    # iterate thru poročila
    imena_porocil = list(df_porocila["Poročilo"])
    for ime_porocila in imena_porocil:
        izvozi_porocilo(ime_porocila, df_vzponi, df_porocila)
    print("Končano")
