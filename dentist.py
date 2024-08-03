import eel
import sqlite3

CLIENT_ROW_COUNT = '10'
ENTRY_ROW_COUNT = '10'

conn = sqlite3.connect('dentist.db')

conn.execute('''CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prix REAL NOT NULL,
    date NUMERIC NOT NULL,
    acte TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients (id));''')

conn.execute('''CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    telephone TEXT NOT NULL);''')

eel.init('web')


def checkInput(input):
    for i in input:
        if not input[i] or input[i] == '':
            return False
        
    return True

@eel.expose
def pyGetEntry(entry):
    try:
        print(entry)
        if not checkInput(entry):
            return False
        
        conn.execute("INSERT INTO entries (client_id, prix, date, acte) VALUES (?, ?, ?, ?)", 
                    (entry['client_id'], entry['prix'], entry['date'], entry['acte']))
        conn.commit()
        return True
    except:
        return False

@eel.expose
def pyGetClient(client):
    try:
        print(client)
        if not checkInput(client):
            return False
        
        conn.execute("INSERT INTO clients (nom, prenom, telephone) VALUES (?, ?, ?)", 
                    (client['nom'], client['prenom'], client['telephone']))
        conn.commit()
        return True
    except:
        return False

def querize(query):
    for i in query:
        query[i] = f"%{query[i]}%"
    return query

@eel.expose
def pySendClients(query=None):
    if query != None:
        query = querize(query)
        #print('query: ' + str(query))
        clients = conn.execute('SELECT id, nom, prenom, telephone FROM clients where id LIKE ? AND nom LIKE ? AND prenom LIKE ? AND telephone LIKE ?', 
                                 (query['id'], query['nom'], query['prenom'], query['telephone']))
    else:
        clients = conn.execute(f"SELECT id, nom, prenom, telephone FROM clients LIMIT {CLIENT_ROW_COUNT}")

    clients = [{'id': row[0], 'nom': row[1], 'prenom': row[2], 'telephone': row[3]} for row in clients]
    #print('clients\n' + str(clients))
    return clients

@eel.expose
def pySendEntries(query=None):
    if query != None:
        query = querize(query)
        #print('query: ' + str(query))
        entries = conn.execute('SELECT id, client_id, prix, date, acte FROM entries WHERE id LIKE ? AND client_id LIKE ? AND prix LIKE ? AND date LIKE ?',
                                 (query['entry_id'], query['client_id'], query['prix'], query['date']))
    else:
        entries = conn.execute(f"SELECT id, client_id, prix, date, acte FROM entries LIMIT {ENTRY_ROW_COUNT}")

    entries = [{'entry_id': row[0], 'client_id': row[1], 'prix': row[2], 'date': row[3], 'acte': row[4]} for row in entries]
    #print('entries\n' + str(entries))
    return entries

@eel.expose
def pySendClient(id):
    client = conn.execute('SELECT * FROM clients WHERE id = ?', (id,))
    return client.fetchone()

@eel.expose
def pySendEntry(entry_id):
    entry = conn.execute('SELECT id, client_id, prix, date, acte FROM entries WHERE id = ?', (entry_id,))
    return entry.fetchone()


eel.start('main.html')