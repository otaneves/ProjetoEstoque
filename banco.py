from datetime import datetime
import mysql.connector  # type: ignore

sessao = None

def conectar():
    #Essa função estabelece a conexão com o banco de dados MySQL usando as credenciais fornecidas. Ela retorna o objeto de conexão que pode ser usado para executar consultas SQL.
    conexao = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Ot@vio123",
        database="estoque"
    )

    return conexao

def login_usuario(email, senha):
    #Essa função realiza o login do usuário verificando se o email ou ID e a senha fornecidos correspondem a um registro no banco de dados. Se a autenticação for bem-sucedida, ela retorna um dicionário com os detalhes do usuário; caso contrário, retorna None.
    
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            SELECT id, nome, perfil, data_nascimento, cpf, email, celular, senha
            FROM usuarios
            WHERE (email = %s OR id = %s)
            AND senha = %s
        """

        try:
            email_int = int(email)
        except ValueError:
            email_int = 0

        valores = (email, email_int, senha)

        cursor.execute(sql, valores)

        resultado = cursor.fetchone()

        if resultado is None:
            return None

        usuario = {
            "id": resultado[0],
            "nome": resultado[1],
            "perfil": resultado[2],
            "data_nascimento": resultado[3],
            "cpf": resultado[4],
            "email": resultado[5],
            "celular": resultado[6],
            "senha":resultado[7]
        }

        return usuario

    except Exception as erro:

        return None

    finally:

        cursor.close()
        conexao.close()

def cadastrar_usuario(nome,celular,data_nascimento,cpf,email,senha,perfil):
    
    # Essa função cadastra um novo usuário no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, valida a data de nascimento e insere os dados do novo usuário na tabela "usuarios". Se ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception("Acesso negado. Nenhum usuário conectado.")

    if sessao["perfil"] != "admin":
        raise Exception(
            "Acesso negado. Apenas administradores podem cadastrar usuários."
        )

    try:

        data = datetime.strptime(
            data_nascimento,
            "%d/%m/%Y"
        )

    except ValueError:

        raise Exception(
            "A data de nascimento deve estar no formato DD/MM/AAAA."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            INSERT INTO usuarios
            (
                nome,
                celular,
                data_nascimento,
                cpf,
                email,
                senha,
                perfil
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cpf = "".join(filter(str.isdigit, str(cpf)))
        celular = "".join(filter(str.isdigit, str(celular)))

        valores = (
            nome,
            celular,
            data,
            cpf,
            email,
            senha,
            perfil
        )

        cursor.execute(sql, valores)

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def buscar_usuario_por_id(usuario_id):

    #Essa função busca um usuário no banco de dados pelo seu ID. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, executa uma consulta SQL para recuperar os dados do usuário correspondente ao ID fornecido. Se o usuário não for encontrado, uma exceção é lançada. A função retorna um dicionário com os detalhes do usuário encontrado.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem acessar usuários."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                nome,
                celular,
                data_nascimento,
                cpf,
                email,
                senha,
                perfil
            FROM usuarios
            WHERE id = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise Exception("Usuário não encontrado.")

        return {
            "id": resultado[0],
            "nome": resultado[1],
            "celular": resultado[2],
            "data_nascimento": resultado[3],
            "cpf": resultado[4],
            "email": resultado[5],
            "senha": resultado[6],
            "perfil": resultado[7]
        }

    finally:

        cursor.close()
        conexao.close()
        
def buscar_produto_por_id(produto_id):

    # Essa função busca um produto no banco de dados pelo seu ID. Ela verifica se há uma sessão ativa e, em seguida, executa uma consulta SQL para recuperar os dados do produto correspondente ao ID fornecido. Se o produto não for encontrado, uma exceção é lançada. A função retorna um dicionário com os detalhes do produto encontrado.

    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )


    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                nome,
                valor_compra,
                valor_venda,
                quantidade,
                quantidade_minima,
                ativo
            FROM produtos
            WHERE id = %s
        """, (produto_id,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise Exception("Produto não encontrado.")

        return {
            "nome": resultado[0],
            "valor_compra": formatar_valor(resultado[1]),
            "valor_venda": formatar_valor(resultado[2]),
            "quantidade": resultado[3],
            "quantidade_minima": resultado[4],
            "ativo": resultado[5]
        }

    finally:

        cursor.close()
        conexao.close()
        
def formatar_valor(valor):

    # Essa função formata um valor numérico para o formato monetário brasileiro (R$). Se o valor for None, retorna "R$ 0,00". Caso contrário, converte o valor para float e formata com duas casas decimais, substituindo os separadores de milhar e decimal conforme o padrão brasileiro.
    
    if valor is None:
        return "R$ 0,00"

    valor = float(valor)

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def atualizar_usuario(usuario_id,nome,celular,data_nascimento,cpf,email,senha,perfil):

    # Essa função atualiza os dados de um usuário existente no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, busca o usuário pelo ID fornecido e atualiza os campos com os novos valores, mantendo os valores antigos caso algum campo esteja vazio. A função também valida a data de nascimento, o celular e o CPF antes de realizar a atualização. Se ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception("Acesso negado.")

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem atualizar usuários."
        )

    usuario = buscar_usuario_por_id(usuario_id)

    # Nome
    if nome.strip():
        nome = nome.strip()
    else:
        nome = usuario["nome"]

    # Data
    if data_nascimento.strip():

        try:

            data = datetime.strptime(
                data_nascimento,
                "%d/%m/%Y"
            )

        except ValueError:

            raise Exception(
                "A data deve estar no formato DD/MM/AAAA."
            )

    else:

        data = usuario["data_nascimento"]

    # Celular
    if celular.strip():

        celular = "".join(
            filter(str.isdigit, str(celular))
        )

        if len(celular) not in [10, 11]:
            raise Exception(
                "O celular deve possuir 10 ou 11 números."
            )

    else:

        celular = usuario["celular"]

    # CPF
    if cpf.strip():

        cpf = "".join(
            filter(str.isdigit, str(cpf))
        )

        if len(cpf) != 11:
            raise Exception(
                "O CPF deve possuir 11 números."
            )

    else:

        cpf = usuario["cpf"]

    # E-mail
    if email.strip():
        email = email.strip()
    else:
        email = usuario["email"]

    # Senha
    if senha.strip():
        senha = senha.strip()
    else:
        senha = usuario["senha"]

    # Perfil
    if perfil.strip():
        perfil = perfil.strip()
    else:
        perfil = usuario["perfil"]

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            UPDATE usuarios
            SET
                nome = %s,
                celular = %s,
                data_nascimento = %s,
                cpf = %s,
                email = %s,
                senha = %s,
                perfil = %s
            WHERE id = %s
        """, (
            nome,
            celular,
            data,
            cpf,
            email,
            senha,
            perfil,
            usuario_id
        ))

        if cursor.rowcount == 0:
            raise Exception(
                "Usuário não encontrado."
            )

        conexao.commit()

        # Se o administrador estiver atualizando
        # o próprio usuário, atualiza a sessão também.
        if sessao["id"] == int(usuario_id):

            sessao["nome"] = nome
            sessao["celular"] = celular
            sessao["data_nascimento"] = data
            sessao["cpf"] = cpf
            sessao["email"] = email
            sessao["perfil"] = perfil

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def listar_produtos():

    # Essa função lista todos os produtos ativos no banco de dados. Ela verifica se há uma sessão ativa e, em seguida, executa uma consulta SQL para recuperar os produtos com o status "ativo". A função retorna uma lista de produtos encontrados.
    
    if sessao is None:
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM produtos WHERE ativo = 'S'"
        )

        produtos = cursor.fetchall()

        return produtos

    finally:

        cursor.close()
        conexao.close()

def cadastrar_produto(nome,valor_compra,valor_venda,quantidade_minima):

    # Essa função cadastra um novo produto no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, insere os dados do novo produto na tabela "produtos". Se ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem cadastrar produtos."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            INSERT INTO produtos
            (
                nome,
                valor_compra,
                valor_venda,
                quantidade_minima
            )
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            nome,
            valor_compra,
            valor_venda,
            quantidade_minima
        )

        cursor.execute(sql, valores)

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def atualizar_produto(produto_id,nome,valor_compra,valor_venda,quantidade_minima):

    # Essa função atualiza os dados de um produto existente no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, executa uma consulta SQL para atualizar os campos do produto com os novos valores fornecidos. Se o produto não for encontrado ou ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem atualizar produtos."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            UPDATE produtos
            SET
                nome = %s,
                valor_compra = %s,
                valor_venda = %s,
                quantidade_minima = %s
            WHERE id = %s
            AND ativo = 'S'
        """

        valores = (
            nome,
            valor_compra,
            valor_venda,
            quantidade_minima,
            produto_id
        )

        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            raise Exception(
                "Produto não encontrado."
            )

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def desativar_produto(produto_id):

    # Essa função desativa um produto existente no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, executa uma consulta SQL para atualizar o status do produto para "inativo". Se o produto não for encontrado ou já estiver inativo, uma exceção é lançada. A função também trata erros durante o processo, revertendo a transação se necessário.

    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem desativar produtos."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            UPDATE produtos
            SET ativo = 'N'
            WHERE id = %s
            AND ativo = 'S'
        """

        cursor.execute(sql, (produto_id,))

        if cursor.rowcount == 0:
            raise Exception(
                "Produto não encontrado."
            )

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def reativar_produto(produto_id):

    # Essa função reativa um produto existente no banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, executa uma consulta SQL para atualizar o status do produto para "ativo". Se o produto não for encontrado ou já estiver ativo, uma exceção é lançada. A função também trata erros durante o processo, revertendo a transação se necessário.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if sessao["perfil"] != "admin":
        raise Exception(
            "Apenas administradores podem reativar produtos."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
            UPDATE produtos
            SET ativo = 'S'
            WHERE id = %s
            AND ativo = 'N'
        """

        cursor.execute(sql, (produto_id,))

        if cursor.rowcount == 0:
            raise Exception(
                "Produto não encontrado ou já está ativo."
            )

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def entrada_estoque(produto_id, quantidade):

    # Essa função registra a entrada de estoque de um produto existente no banco de dados. Ela verifica se há uma sessão ativa e se a quantidade fornecida é maior que zero. Em seguida, atualiza a quantidade do produto no banco de dados e registra a movimentação como uma entrada. Se o produto não for encontrado ou ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if quantidade <= 0:
        raise Exception(
            "A quantidade deve ser maior que zero."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade + %s
            WHERE id = %s
            AND ativo = 'S'
        """, (quantidade, produto_id))

        if cursor.rowcount == 0:
            raise Exception(
                "Produto não encontrado."
            )

        cursor.execute("""
            INSERT INTO movimentacoes
            (
                produto_id,
                usuario_id,
                tipo,
                quantidade
            )
            VALUES (%s, %s, 'ENTRADA', %s)
        """, (
            produto_id,
            sessao["id"],
            quantidade
        ))

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def saida_estoque(produto_id, quantidade):

    # Essa função registra a saída de estoque de um produto existente no banco de dados. Ela verifica se há uma sessão ativa e se a quantidade fornecida é maior que zero. Em seguida, verifica se o produto possui estoque suficiente para a saída e atualiza a quantidade do produto no banco de dados, registrando a movimentação como uma saída. Se o produto não for encontrado, não houver estoque suficiente ou ocorrer algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    if sessao is None:
        raise Exception(
            "Acesso negado. Nenhum usuário conectado."
        )

    if quantidade <= 0:
        raise Exception(
            "A quantidade deve ser maior que zero."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT quantidade
            FROM produtos
            WHERE id = %s
            AND ativo = 'S'
        """, (produto_id,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise Exception(
                "Produto não encontrado."
            )

        estoque_atual = resultado[0]

        if estoque_atual <= 0:
            raise Exception(
                "Produto sem estoque disponível."
            )

        if estoque_atual < quantidade:
            raise Exception(
                f"Quantidade solicitada maior que o estoque disponível.\n"
                f"Estoque disponível: {estoque_atual}"
            )

        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade - %s
            WHERE id = %s
            AND ativo = 'S'
        """, (quantidade, produto_id))

        cursor.execute("""
            INSERT INTO movimentacoes
            (
                produto_id,
                usuario_id,
                tipo,
                quantidade
            )
            VALUES (%s, %s, 'SAIDA', %s)
        """, (
            produto_id,
            sessao["id"],
            quantidade
        ))

        conexao.commit()

    except Exception as erro:

        conexao.rollback()

        raise erro

    finally:

        cursor.close()
        conexao.close()

def iniciar_sessao(usuario):

    # Essa função inicia a sessão do usuário, armazenando as informações do usuário conectado na variável global "sessao". Ela recebe um dicionário contendo os detalhes do usuário e atualiza a variável global para indicar que o usuário está logado. A função também imprime uma mensagem indicando que a sessão foi iniciada com sucesso.
    
    global sessao

    sessao = usuario

def encerrar_sessao():

    # Essa função encerra a sessão do usuário, limpando a variável global "sessao" e definindo-a como None. Ela indica que não há mais nenhum usuário conectado e imprime uma mensagem informando que a sessão foi encerrada.
    
    global sessao

    sessao = None

def excluir_usuario(id_usuario, senha_admin):

    # Essa função exclui um usuário do banco de dados. Ela verifica se há uma sessão ativa e se o usuário conectado tem perfil de administrador. Em seguida, valida a senha do administrador fornecida e verifica se o usuário a ser excluído existe. A função também impede que o administrador exclua a própria conta. Se todas as verificações forem bem-sucedidas, o usuário é excluído do banco de dados. Caso ocorra algum erro durante o processo, a transação é revertida e uma exceção é lançada.
    
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        # Verifica se existe um administrador com essa senha
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE perfil = 'admin'
            AND senha = %s
            """,
            (senha_admin,)
        )

        admin = cursor.fetchone()

        if not admin:
            raise Exception("Senha do administrador incorreta.")

        # Verifica se o usuário existe
        cursor.execute(
            """
            SELECT id, nome
            FROM usuarios
            WHERE id = %s
            """,
            (id_usuario,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            raise Exception("Usuário não encontrado.")

        # Impede o administrador de excluir a própria conta
        if sessao and int(id_usuario) == int(sessao["id"]):
            raise Exception(
                "Você não pode excluir o usuário que está logado."
            )

        # Exclui o usuário
        cursor.execute(
            """
            DELETE FROM usuarios
            WHERE id = %s
            """,
            (id_usuario,)
        )

        conexao.commit()

        return True

    except Exception as erro:

        conexao.rollback()
        raise erro

    finally:

        cursor.close()
        conexao.close()