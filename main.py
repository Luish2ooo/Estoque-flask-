
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar banco de dados
def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_compra REAL NOT NULL,
        preco_venda REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco_compra = float(request.form['preco_compra'])
        preco_venda = float(request.form['preco_venda'])
        
        conn = get_db_connection()
        conn.execute('INSERT INTO produtos (nome, quantidade, preco_compra, preco_venda) VALUES (?, ?, ?, ?)',
                     (nome, quantidade, preco_compra, preco_venda))
        conn.commit()
        conn.close()
        
        flash('Produto adicionado com sucesso!')
        return redirect(url_for('index'))
    
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco_compra = float(request.form['preco_compra'])
        preco_venda = float(request.form['preco_venda'])
        
        conn.execute('UPDATE produtos SET nome = ?, quantidade = ?, preco_compra = ?, preco_venda = ? WHERE id = ?',
                     (nome, quantidade, preco_compra, preco_venda, id))
        conn.commit()
        conn.close()
        
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar.html', produto=produto)

@app.route('/excluir/<int:id>')
def excluir_produto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Produto excluído com sucesso!')
    return redirect(url_for('index'))

@app.route('/alertas')
def alertas():
    conn = get_db_connection()
    produtos_baixo = conn.execute('SELECT * FROM produtos WHERE quantidade <= 5').fetchall()
    conn.close()
    return render_template('alertas.html', produtos_baixo=produtos_baixo)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
