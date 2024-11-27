# Generator poročila o turi
Pretvori tabelo vzponov iz ao-trzic.si/vzponi v Poročila o turi. 

## Uporaba

### Potrebni podatki
Sistem pričakuje tabelo z vzponi v slogu AO Tržič  (pojdi na [sistem za beleženje vzponov]( https://www.ao-trzic.si/wp-admin/admin.php?page=prikaz-vzponov) in pritisni gumb "izvozi") in tabelo z informacijo o poročilih. 

V tabelo z vzponi dodaj nov stolpec "Poročilo" in za vsak vzpon napiši ime poročila, v katerega zapiši preplezano smer. 

Glej priložen demo za primer uporabe.

### Klicanje programa

Za delovanje porgrama potrebuješ [python](https://www.python.org/) in knjižnici [pandas](https://pandas.pydata.org/) ter [markdown-pdf](https://pypi.org/project/markdown-pdf/). 

Najlažje je kar zamenjati tabeli `example/demo_vzponi.csv` in `porocila.csv` s svojima tabelama in pognati 
`python3 demo.py` **iz mape src!**