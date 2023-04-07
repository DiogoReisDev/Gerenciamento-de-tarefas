import sqlite3

conexao = sqlite3.connect('Atividade.db')
cursor = conexao.cursor()

#Criando as tabelas necessárias para nosso código:
sql = '''CREATE TABLE IF NOT EXISTS afazeres(
id INTEGER PRIMARY KEY,
descricao TEXT,
data_concluida TEXT,
completo BOOLEAN,
categoria_id INT,
FOREIGN KEY (categoria_id) REFERENCES categoria(id)
)'''
cursor.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS categoria(
id INTEGER PRIMARY KEY,
nome TEXT
)'''

cursor.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS afazeres_categoria(
afazeres_id INT,
categoria_id INT,
FOREIGN KEY (afazeres_id) REFERENCES afazeres(id),
FOREIGN KEY (categoria_id) REFERENCES categoria(id)
)'''    

cursor.execute(sql)

#função para adicionar tarefas:
def add_func(descricao, categoria_id):
    valores = [descricao, False, categoria_id]
    sql = '''INSERT INTO afazeres (descricao, completo, categoria_id) VALUES (?,?,?)'''
    cursor.execute(sql, valores)
    conexao.commit()
    print('='*30)
    print('||Tarefa adicionada à lista!||')
    print('='*30)

#função para listar todas as tarefas:
def lista_afazeres():
    sql = '''SELECT a.id, a.descricao, a.data_concluida, a.completo, categoria.nome, categoria.id
    FROM afazeres as a
    JOIN categoria ON a.categoria_id = categoria.id'''
    cursor.execute(sql)
    afazeres = cursor.fetchall()
    for funções in afazeres:
        boleana = 'Concluído' if funções[3] else 'Em aberto'
        print('|ID:',funções[0],'|Tarefa:',funções[1],'|Data:',funções[2],'|Andamento:',boleana,'|Categoria:',funções[4],'|ID categoria:',funções[5],'|')
    print('↑'*26)
    print('='*26)
    print('||Lista de tarefas acima||')
    print('='*26)


#função para marcar uma tarefa como concluída
def func_finalizada(id_funcao):
    valores = [True, id_funcao]
    sql = '''UPDATE afazeres SET completo = ? WHERE id = ?'''
    cursor.execute(sql, valores)
    conexao.commit()
    print('='*21)
    print('||Tarefa concluída!||')
    print('='*21)

#função para remover uma tarefa:
def func_delete(id_funcao):
    valores = [id_funcao]
    sql = '''DELETE FROM afazeres WHERE id = ?'''
    cursor.execute(sql, valores)
    conexao.commit()
    print('='*20)
    print('||Tarefa Removida!||')
    print('='*20)

#função para adicionar uma nova categoria:
def add_categoria(nome):
    valores = [nome]
    sql = '''INSERT INTO categoria (nome) VALUES (?)'''
    cursor.execute(sql, valores)
    conexao.commit()
    print('='*30)
    print('||Nova Categoria adicionada!||')
    print('='*30)

#função para listar todas as categorias:
def lista_categoria():
    sql = '''SELECT * FROM categoria'''
    cursor.execute(sql)
    categoria = cursor.fetchall()
    for categorias in categoria:
        print(categorias)
    print('↑'*30)
    print('='*30)    
    print('||Lista de categorias acima!||')
    print('='*30)
#função para excluir uma categoria:
def categoria_delete(categoria_id):
    valores = [categoria_id]
    sql = '''DELETE FROM categoria WHERE id = ?'''
    cursor.execute(sql, valores)
    conexao.commit()
    print('='*23)
    print('||Categoria removida!||')
    print('='*23)

#Adiciona uma associação entre uma tarefa e uma categoria na tabela afazeres_categoria:
def add_funcs_categoria(id_func, categoria_id):
    valores = [categoria_id, id_func]
    sql = '''INSERT INTO afazeres_categoria (afazeres_id, categoria_id) VALUES (?,?)'''
    cursor.execute(sql, valores)
    conexao.commit()

#Função que Lista as tarefas que pertencem a uma determinada categoria.
def lista_funcs_categoria(categoria_id):
    valores = [categoria_id]
    sql = '''SELECT a.id, a.descricao, a.completo
    FROM afazeres as a
    JOIN afazeres_categoria as ac ON a.id = ac.afazeres_id
    WHERE ac.categoria_id = ? AND a.completo = 0'''
    cursor.execute(sql, valores)
    categoria = cursor.fetchall()
    for funcoes in categoria:
        boleana = 'Concluído' if funcoes[2] else 'Em aberto'
        print('|ID:',funcoes[0], '|Tarefa:',funcoes[1], '|Andamento:',boleana,'|')
    print('='*52)
    print('||Todas as tarefas da categoria selecionada, acima||')
    print('='*52)

while True:
    print('='*25)
    print('||| Oque deseja fazer |||')
    print('='*25)
    print('↓'*25)
    instrução = input('\n• Para Organizar categoria e tarefa (Digite organizar)\n• Para inserir tarefa (Digite tarefa);\n• Para ver todas as tarefas de uma categoria (Digite ver categoria);\n• Para marcar que a tarefa foi concluida (Digite concluido);\n• Para remover uma tarefa (Digite remover tarefa); \n• Para adicionar uma nova categoria (Digite nova categoria); \n• Para mostrar todas as categorias (Digite categorias);\n• Para remover uma categoria (Digite remover categoria):  \n')
    
    if instrução == 'tarefa':
        lista_afazeres()
        descricao = input('Descrição da tarefa: ')
        categoria_id = input('Digite o ID da categoria desta tarefa: ')
        add_func(descricao, categoria_id)
        id_func =  input('Digite o ID da tarefa atual seguindo a lista acima: ')
        categoria_id = input('Digite o ID da categoria: ')
        add_funcs_categoria(id_func, categoria_id)
    elif instrução == 'ver categoria':
        lista_categoria()
        categoria_id = input("Digite o ID da categoria que deseja saber as tarefas em aberto:")
        lista_funcs_categoria(categoria_id)
    elif instrução == 'concluido':
        id_funcao = input('Digite o ID da tarefa que foi concluída: ')
        print('A Tarefa foi marcada como concluida!')
        func_finalizada(id_funcao)
    elif instrução == 'remover tarefa':
        lista_afazeres()
        id_funcao = input('Digite o ID da tarefa que deseja remover: ')
        print('Tarefa removida com sucesso!')
        func_delete(id_funcao)
    elif instrução == 'nova categoria':
        nome = input('Digite o nome da nova categoria: ')
        print('Categoria criada com sucesso!')
        add_categoria(nome)
    elif instrução == 'categorias':
        lista_categoria()
    elif instrução == 'remover categoria':
        lista_categoria()
        categoria_id = input('Digite o ID da categoria que deseja remover: ')
        print('Categoria removida com sucesso!')
        categoria_delete(categoria_id)
    elif instrução == 'organizar':
        lista_categoria()
        categoria_id = input('Digite o ID da categoria que deseja adicionar uma tarefa: ')
        lista_afazeres()
        id_func = input('Digite o ID da tarefa: ')
        print('Categoria e tarefa organizadas!')
        add_funcs_categoria(categoria_id, id_func)
    else:
        print('Comando inválido, selecione uma opção que exista!')
