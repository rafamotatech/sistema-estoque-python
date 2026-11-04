import sqlite3
import tkinter as tk
from tkinter import messagebox
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





def cadastrar_produto():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title('Cadastrar Produto')
    janela_cadastro.geometry('350x300')

    tk.Label(
        janela_cadastro,
        text='Nome do produto'
    ).pack(pady=5)

    campo_nome = tk.Entry(janela_cadastro)
    campo_nome.pack()

    tk.Label(
        janela_cadastro,
        text='Preço (R$)'
    ).pack(pady=5)

    campo_preco = tk.Entry(janela_cadastro)
    campo_preco.pack()

    tk.Label(
        janela_cadastro,
        text='Quantidade'
    ).pack(pady=5)

    campo_quantidade = tk.Entry(janela_cadastro)
    campo_quantidade.pack()

    def salvar():
        nome = campo_nome.get()
        preco = campo_preco.get()
        quantidade = campo_quantidade.get()

        if not nome.strip():
            messagebox.showwarning('Atenção', 'Digite o nome do produto!')
            return

        if not any(letra.isalpha() for letra in nome):
            messagebox.showwarning(
                'Atenção',
                'O nome do produto deve conter pelo menos uma letra!'
            )
            return
         

        
        try:
            preco = float(preco)

            if preco <=0:
               messagebox.showwarning(
                    'Atenção',
                    'O preço digitado é inválido'
               )
               return
            

        except ValueError:
         messagebox.showwarning(
            'Atenção',
            'Você precisa digitar um preço númerico!'
         )
         return

        try:
           quantidade = int(quantidade)

           if quantidade <=0:
              messagebox.showwarning(
                 'Atenção',
                 'A quantidade digitada é inválida!'
              )
              return
           
        except ValueError:
           messagebox.showwarning(
              'Atenção ',
              'Você precisa digitar um número inteiro!'
           )
           return
        cursor.execute(
           '''
           INSERT INTO produtos (nome,preco,quantidade)
           VALUES (?,?,?)
              
              ''',
            (nome,preco,quantidade)
        )
        conexao.commit()

        messagebox.showinfo (
           'Sucesso',
           'Produto cadastrado com sucesso!'
        )

        campo_nome.delete(0,tk.END)
        campo_preco.delete(0,tk.END)
        campo_quantidade.delete(0,tk.END)
        

    botao_salvar = tk.Button(
        janela_cadastro,
        text='Salvar Produto',
        command=salvar
    )
    botao_salvar.pack(pady=15)


def listar_produtos():
   cursor.execute('SELECT * FROM produtos')
   produtos = cursor.fetchall()

   janela_lista = tk.Toplevel(janela)
   janela_lista.title('Lista de produtos')
   janela_lista.geometry('500x400')

   if not produtos:
      tk.Label(
         janela_lista,
         text='Nenhum produto cadastrado!'
      ).pack(pady=10)

   else:
      for produto in produtos:
          texto = (
             f'ID: {produto[0]} |'
             f'Nome: {produto[1]} | '
             f'Preço: R$ {produto[2]:.2f} | '
             f'Quantidade: {produto[3]} | '
          )

          tk.Label(
             janela_lista,
             text=texto
          ).pack(pady=5)



def atualizar_estoque():
    janela_atualizar = tk.Toplevel(janela)
    janela_atualizar.title('Atualizar Estoque')
    janela_atualizar.geometry('350x300')

    tk.Label(
        janela_atualizar,
        text='Digite o nome do produto:'
    ).pack(pady=10)

    campo_nome_atualizar = tk.Entry(janela_atualizar)
    campo_nome_atualizar.pack(pady=5)


    def buscar_produto():
        nome = campo_nome_atualizar.get().strip()

        cursor.execute(
            'SELECT * FROM produtos WHERE nome = ?',
            (nome,)
        )

        produto = cursor.fetchone()

        if produto is not None:
            print('Produto encontrado!')

            tk.Label(
                janela_atualizar,
                text='Digite a nova quantidade:'
            ).pack(pady=5)

            campo_nova_quantidade = tk.Entry(janela_atualizar)
            campo_nova_quantidade.pack(pady=5)
            def salvar_alteracao():
                try:
                   nova_quantidade = int(campo_nova_quantidade.get())

                   if nova_quantidade <= 0:
                      messagebox.showwarning(
                         'Atenção',
                         'A quantidade deve ser maior que zero!'
                      )
                      return
                   
                   cursor.execute(
                      'UPDATE produtos SET quantidade = ? WHERE id = ?',
                      (nova_quantidade, produto[0])
                   )

                   conexao.commit()

                   messagebox.showinfo(
                      'Sucesso',
                      'Estoque atualizado!'
                   )

                   janela_atualizar.destroy()

                except ValueError:
                    messagebox.showwarning(
                       'Atenção',
                       'Digite uma quantidade inteira válida!'
                    )

            tk.Button(
               janela_atualizar,
               text='Salvar Alteração',
               command=salvar_alteracao
            ).pack(pady=10)

        else:
            messagebox.showwarning(
                'Atenção',
                'Produto não encontrado!'
            )

    botao_buscar = tk.Button(
        janela_atualizar,
        text='Buscar Produto',
        command=buscar_produto
    )
    botao_buscar.pack(pady=10)


def remover_produto():
    janela_remover = tk.Toplevel(janela)
    janela_remover.title('Remover Produto')
    janela_remover.geometry('350x250')

    tk.Label(
        janela_remover,
        text='Digite o nome do produto:'
    ).pack(pady=10)

    campo_nome_remover = tk.Entry(janela_remover)
    campo_nome_remover.pack(pady=5)

    def buscar_produto():
        nome = campo_nome_remover.get().strip()

        if not nome:
            messagebox.showwarning(
                'Atenção',
                'Digite o nome do produto!',
                parent=janela_remover
            )
            return

        cursor.execute(
            'SELECT * FROM produtos WHERE nome = ?',
            (nome,)
        )

        produto = cursor.fetchone()

        if produto is not None:
            confirmar = messagebox.askyesno(
                'Confirmar remoção',
                f'Deseja remover o produto "{produto[1]}"?',
                parent=janela_remover
            )

            if confirmar:
                cursor.execute(
                    'DELETE FROM produtos WHERE id = ?',
                    (produto[0],)
                )
                conexao.commit()

                messagebox.showinfo(
                    'Sucesso',
                    'Produto removido com sucesso!',
                    parent=janela_remover
                )

                janela_remover.destroy()

        else:
            messagebox.showwarning(
                'Atenção',
                'Produto não encontrado!',
                parent=janela_remover
            )

    tk.Button(
        janela_remover,
        text='Buscar e Remover Produto',
        command=buscar_produto
    ).pack(pady=15)




   
    


    

    



    
janela = tk.Tk()

janela.title('Sistema de Estoque')

janela.geometry('600x400')

titulo = tk.Label(
    janela,
    text = 'Sistema de Estoque',
    font=('Arial', 18, 'bold')
)

titulo.pack(pady=20)

botao_cadastrar = tk.Button(
    janela,
    text = 'Cadastrar Produto',
    command = cadastrar_produto
)

botao_cadastrar.pack(pady=10)

botao_listar = tk.Button(
    janela,
    text='Listar Produtos',
    command=listar_produtos
)
botao_listar.pack(pady=10)


botao_atualizar = tk.Button(
    janela,
    text = 'Atualizar Estoque',
    command=atualizar_estoque
)
botao_atualizar.pack(pady=10)

botao_remover = tk.Button(
    janela,
    text= 'Remover Produto',
    command = remover_produto
)
botao_remover.pack(pady=10)

janela.mainloop()

