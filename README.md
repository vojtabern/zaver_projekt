# Ročníkový projekt
## __Webové stránky s psychologickými testy__

Cílem je vytvořit plně funkční webové stránky pomocí frameworku Django a Bootstrap. 
S nejlépe co nejlehčí možností editace informací na stránce. 

## Cíle Projektu
- Plně funkční webovky dle původních ([janbernard.cz](http://www.janbernard.cz/index.html)), ale vylepšené, modernější a hezčí
- Psychologický test/y s vyhodnocením v grafech
- výsledky do PDF 
- zdockerování

## Technologie
- [Django](https://www.djangoproject.com/) - Django framework
- [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/) - Bootstrap v5
- HTML 
- jednoduché CSS

## Instalace

Nainstaluj a spust server:
> pokud používáte pyCharm tak si první založte venv
```
pip install -r requirements.txt
cd mysite
python manage.py makemigration && python manage.py migrate
python manage.py runserver
```
Server by měl běžet na http://127.0.0.1:8000/

## Autoři a konzultanti
- Autor: Vojtěch Bernard
- Konzultanti: 
  - Marek Lučný [(github)](https://github.com/lucny)
  - Ondřej "Toaster" Kinšt [(github)](https://github.com/Toaster192)

## Časový harmonogram
Září: 
- > Navrhnout graficky stránku, základ databázového modelu
- Ztrávený čas:
  - 16 hodin

Říjen:
- > Vyřešit/dodělat databázový model, Vytvořit lehký funkční test

Listopad:
- > Začít řešit možnost uploadu stránky na Internet, Dodělávání testů a uživatelských úrovní

Prosinec: 
- > Kdo ví. Finální úpravy
