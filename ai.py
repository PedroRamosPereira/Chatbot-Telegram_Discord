from openai import OpenAI
import sqlite3
import json

with open('token.json') as token_file:
    token = json.load(token_file)

client = OpenAI(
    api_key = token['OpenAI']
)

conn = sqlite3.connect('chatbot.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS historico(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user varchar(20) NOT NULL,
                   plataforma varchar(10) NOT NULL,
                   role varchar(10) NOT NULL,
                   mensagem TEXT NOT NULL
                   )
                """
                )
conn.commit()

def salvar_mensagem(usuario, plataforma, role, mensagem):
    cursor.execute('INSERT INTO historico(user, plataforma, role, mensagem) VALUES(?, ?, ?, ?)', [usuario, plataforma, role, mensagem])
    conn.commit()

def carregar_historico(usuario):
    cursor.execute("SELECT role, mensagem FROM historico WHERE user = ? ORDER BY id ASC", (usuario,))
    return([{"role": row[0], "content": row[1]} for row in cursor.fetchall()])

def limpar_historico(usuario):
    cursor.execute("DELETE FROM historico WHERE user = ?", (usuario,))
    usuario = "gpt-4o-mini"
    cursor.execute("DELETE FROM historico WHERE user = ?", (usuario,))
    conn.commit()
    
    return('Historico do usuario excluido')  
    
def responder(user, plataforma, mensagem):
    
    salvar_mensagem(user, plataforma, "user", mensagem)
    hist = carregar_historico(user)
    
    response = client.chat.completions.create(
        messages=hist,
        model="gpt-4o-mini",
    )
    
    resposta_texto = response.choices[0].message.content
    
    salvar_mensagem("gpt-4o-mini", plataforma, "client", resposta_texto)
    
    return(resposta_texto)

for row in cursor.execute('SELECT * FROM historico'):
    print(row)