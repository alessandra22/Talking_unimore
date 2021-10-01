Talking Unimore è un forum nato per dare l'opportunità di chiedere e rispondere alle solite domande universitarie,
col vantaggio di mantenere salvati i post, rendendoli utili per i posteri.


ISTRUZIONI PER L'INSTALLAZIONE

Dopo aver estratto la cartella contentente il progetto, accedervi da terminale tramite
cd talking_unimore

Dopodiché, assicurarsi di avere python installato ed usare i seguenti comandi
python -m venv env
env\Scripts\activate
pip install django Pillow django-crispy-forms
python manage.py runserver

Infine, dal proprio browser, accedere alla pagina indicata (solitamente http://127.0.0.1:8000/)


CREDENZIALI

Credenziali dell'admin:
 username = ale
 password = admin

Credenziali testuser:
 username = TestUser (o TestUser2, TestUser3, TestUser44)
 password = prova123