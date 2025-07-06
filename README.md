import os
import shutil

# Caminho da pasta onde o script está rodando
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pasta de destino
templates_dir = os.path.join(base_dir, 'templates')

# Cria a pasta 'templates' se não existir
os.makedirs(templates_dir, exist_ok=True)

# Percorre todos os arquivos e subpastas na raiz do projeto
for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    # Move apenas arquivos .html que estão na pasta raiz (não em subpastas)
    if os.path.isfile(item_path) and item.lower().endswith('.html'):
        shutil.move(item_path, os.path.join(templates_dir, item))
        print(f"Movido: {item} -> templates/{item}")

print("Todos os arquivos .html foram movidos para a pasta 'templates'.")
