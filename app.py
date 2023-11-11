from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = "pifibra"


# Configurações do SQLite
DATABASE = "database.db"

# Função para criar a tabela do usuário


def create_user_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                             nome TEXT, endereço TEXT, telefone VARCHAR, senha TEXT)'''
    )
    connection.commit()
    connection.close()


create_user_table()

# Página inicial


@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Página de endereços informando a manutenção da fibra ótica


@app.route('/endereco')
def endereco():
    return render_template('endereco.html')

# Página de enviar as imagens contendo as informações de onde efetuará a  manutenção da fibra ótica

@app.route('/enviar')
def enviar():
    return render_template('enviar.html')


# Rota para lidar com o formulário de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    endereço = request.form['endereço']
    telefone = request.form['telefone']
    senha = request.form['senha']

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (nome, endereço, telefone, senha) VALUES (?, ?, ?, ?)",
                   (nome, endereço, telefone, senha))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

# Página de autenticação


@app.route('/autenticar', methods=['POST'])
def autenticar():
    nome = request.form['nome']
    senha = request.form['senha']

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE nome=? AND senha=?",
                   (nome, senha))
    user = cursor.fetchone()
    connection.close()

    if user:
        return render_template('endereco.html')
    else:
        flash('USUARIO INVALIDO')
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
