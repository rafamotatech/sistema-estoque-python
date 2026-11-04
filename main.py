import sqlite3
conexao = sqlite3.connect('estoque.db')
cursor = conexao.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')

conexao.commit()





print('=== SISTEMA DE ESTOQUE ===' )
print('1 - Cadastrar produto' )
print('2 - Listar produtos' )
print('3 - Atualizar estoque' )
print('4 - Remover produto' )
print('5 - Sair')


Cadastrar = '1'
Listar = '2'
Atualizar = '3'

Remover = '4'
Sair = '5'



while True:
    Escolha_opçao = input('Digite uma dessas opções: ')

    if Escolha_opçao == Cadastrar:
        nome_produto = input('Digite o nome do produto que você deseja cadastrar: ').strip()

        while not nome_produto:
            print('O nome do produto não pode ficar vazio')
            nome_produto = input('Digite novamente o nome do produto: ').strip()

        valor_valido = False

        while not valor_valido:
            try:
                valor_produto = float(input('Digite o valor do produto que você deseja cadastrar: '))

                if valor_produto > 0:
                    print('Preço válido!')
                    valor_valido = True
                else:
                    print('O valor precisa ser maior que zero')

            except ValueError:
                print('Você precisa digitar um valor numérico')

        quantidade_valida = False

        while not quantidade_valida:
            try:
                quantidade_produto = int(input('Digite a quantidade desse produto: '))

                if quantidade_produto > 0:
                    print('Quantidade válida!')
                    quantidade_valida = True
                else:
                    print('A quantidade precisa ser maior que zero!')

            except ValueError:
                print('Você precisa digitar um número!')


        cursor.execute(
            '''
            INSERT INTO produtos (nome, preco, quantidade)
            VALUES (?, ?, ?)
            ''',
            (nome_produto, valor_produto, quantidade_produto)
        )

        conexao.commit()

    elif Escolha_opçao == Listar:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()

        for produto in produtos:
            print('--- Produto ---')
            print(produto[1])
            print(produto[2])
            print(produto[3])

    elif Escolha_opçao == Atualizar:
        escolha_produto = input('Qual produto você está buscando? ')

        cursor.execute(
            'SELECT * FROM produtos WHERE nome = ?',
            (escolha_produto,)
        )

        produto = cursor.fetchone()

        if produto is not None:
            print('O produto foi encontrado!')

            atulizaçao_valida = False


            while not atulizaçao_valida:
             try:
                nova_quantidade = int(
                   input('Digite o novo estoque desse produto: ')
               )
 
                if nova_quantidade <= 0:
                  print('O valor dessa quantidade de estoque não existe!')
                else:
                  print('Quantidade válida')
                  atulizaçao_valida = True
             except ValueError:
                print('Voce precisa digitar um numero inteiro! ')
                
            cursor.execute(
                '''
                 UPDATE produtos
                 SET quantidade = ?
                 WHERE nome = ?
                
                    ''',
                 (nova_quantidade, escolha_produto)
                                
                                
                
                 )
            conexao.commit()
            print('A quantidade desse produto foi atualizada com sucesso!')
                
        else:
         print('Produto digitado não foi encontrado!')


        
            

    elif Escolha_opçao == Remover:
        Remova = input('Digite o nome do produto que você deseja remover: ')

        cursor.execute(
            'SELECT * FROM produtos WHERE nome = ?',
            (Remova,)
        )
        produto = cursor.fetchone()

        if produto is not None:
            print('O produto foi encontrado')

            cursor.execute(
                
                ' DELETE FROM produtos WHERE nome = ?',
                 (Remova,)
                  
            )
            conexao.commit()
            print('O produto foi removido com sucesso! ')

        else:
            print('Erro: produto não encontrado')

    elif Escolha_opçao == Sair:
        print('O usuário escolheu sair do sistema!')
        break


    else:
        print('Essa opção é inválida!')
conexao.close()
