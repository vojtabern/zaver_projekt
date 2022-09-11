# Ročníkový projekt
## __Webové stránky s psychologickými testy__

Cílem je vytvořit plně funkční webové stránky pomocí frameworku Django a Bootstrap. 
S nejlépe co nejlehčí možností editace informací na stránce. 

## Body
- Plně funkční webovky dle původních ([janbernard.cz](http://www.janbernard.cz/index.html)), ale vylepšené, modernější a hezčí
- Psychologický test/y s vyhodnocením v grafech
- export výsledků do PDF 
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
