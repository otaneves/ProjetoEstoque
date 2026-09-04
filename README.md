# 📦 Sistema de Gestão de Estoque

Um sistema de gerenciamento de estoque desktop moderno e intuitivo desenvolvido em **Python**, utilizando a interface gráfica **CustomTkinter** e persistência de dados em banco de dados **MySQL**.

O sistema possui controle de acesso baseado em níveis de permissão (Administrador e Usuário Comum), permitindo gerenciar produtos, registrar movimentações de entrada/saída e controlar os usuários do sistema com total segurança.

---

## ⚠️ NOTA CRÍTICA DE CONFIGURAÇÃO (OBRIGATÓRIO)

Antes de rodar o programa, **você DEVE abrir o arquivo `banco.py`** e modificar os parâmetros dentro da função `conectar()`. O código original vem configurado com credenciais específicas do desenvolvedor:

```python
def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",         # <--- Altere para o seu usuário do MySQL
        password="Ot@vio123", # <--- Substitua pela SUA senha pessoal do MySQL
        database="estoque"
    )
    return conexao
```

Se você não alterar a senha `"Ot@vio123"` para a senha real do seu banco de dados local, o sistema **não irá iniciar** e retornará um erro de conexão (`Access denied for user`).

---

## 🔍 Como Descobrir Seus Parâmetros do MySQL

Se você não sabe qual é o seu Host, Porta ou Usuário, siga o guia prático abaixo para coletar esses dados direto do seu sistema:

### 1. Host e Porta Padrão
Na grande maioria das instalações locais (como XAMPP, WampServer ou o instalador oficial do MySQL), os valores padrão quase sempre são:
* **Host:** `localhost` (ou o IP local `127.0.0.1`)
* **Porta:** `3306`

### 2. Rodando o Script de Diagnóstico
Para descobrir exatamente o seu **Usuário atual** e confirmar se a **Porta** do seu servidor é a padrão, abra o terminal do seu computador (Prompt de Comando ou PowerShell) e digite o comando abaixo para entrar no console do seu MySQL:

```bash
mysql -u seu_usuario -p
```
*(Substitua `seu_usuario` pelo usuário que você acha que é, geralmente `root`, e digite sua senha quando solicitado)*.

Assim que conseguir entrar no terminal interno do MySQL, digite os seguintes comandos para extrair os dados corretos:

* **Para descobrir o Usuário correto:**
  ```sql
  SELECT USER();
  ```
  *(O retorno mostrará algo como `root@localhost`. O que vem antes do `@` é o seu **user**).*

* **Para descobrir a Porta correta:**
  ```sql
  SHOW VARIABLES LIKE 'port';
  ```
  *(O banco retornará uma tabela mostrando o valor numérico exato da porta ativa, por exemplo, `3306`).*

### 3. Como descobrir a Senha?
A senha do MySQL é definida de forma estritamente pessoal no momento em que você instalou o banco de dados no computador. 
* **Se você usa XAMPP ou WampServer:** Por padrão, o usuário é `root` e a senha vem **totalmente vazia** (`password=""`).
* **Se você usa o MySQL Workbench/Installer oficial:** A senha é exatamente aquela que você criou no campo *Root Password* durante o assistente de instalação.

---

## 🚀 Funcionalidades

### 🔐 Controle de Acesso e Sessão
* **Login Seguro:** Autenticação baseada em e-mail ou ID numérico integrado ao banco de dados.
* **Níveis de Permissão (NPS):** 
  * `admin`: Acesso total ao sistema (Gestão de produtos, usuários e relatórios de movimentações).
  * `comum`: Visualização limitada do estoque e permissão apenas para realizar entradas e saídas de mercadorias.

### 🛒 Gestão de Estoque
* **Cadastro e Atualização:** Registro de produtos com preço de compra, preço de venda e estoque mínimo.
* **Entrada e Saída Automatizadas:** Atualiza o saldo atual e impede saídas que causem estoque negativo.
* **Desativação Lógica:** Opção de desativar e reativar produtos em vez de apagá-los permanentemente, preservando o histórico físico.
* **Formatação em Tempo Real:** Máscaras monetárias brasileiras (`R$ 0,00`) e travas de digitação para evitar erros do usuário.

### 👥 Controle de Usuários (Apenas Administradores)
* Cadastro, edição e exclusão de contas operacionais.
* Validação rigorosa de dados com masks integradas de **CPF**, **Data de Nascimento** e **Telefone Celular**.
* **Confirmação de Segurança:** Exige a senha do administrador logado antes de efetuar exclusões ou modificações críticas.

---

## 🛠️ Arquitetura do Código

O projeto está dividido em três módulos principais seguindo uma arquitetura limpa:

1. **`main.py`**: O ponto de entrada da aplicação. Inicializa a interface do CustomTkinter e inicia o loop principal do programa.
2. **`interface.py`**: Gerencia toda a parte visual (janelas, abas, campos de entrada, máscaras dinâmicas e popups de aviso/erro).
3. **`banco.py`**: Camada de persistência responsável pelas conexões, transações SQL, segurança de sessões e controle de rollback em caso de falhas.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
* Python 3.10 ou superior
* Servidor MySQL ativo (Localhost)

---

## 🔧 Configuração e Instalação

### 1. Clonar ou copiar os arquivos
Certifique-se de manter os três arquivos no mesmo diretório:
```bash
├── main.py
├── interface.py
└── banco.py
```

### 2. Instalar as dependências
Instale as bibliotecas necessárias utilizando o gerenciador de pacotes `pip`:
```bash
pip install customtkinter mysql-connector-python
```

### 3. Configurar o Banco de Dados
Para criar a estrutura de tabelas, chaves estrangeiras, massa de dados inicial e o gatilho (`TRIGGER`), escolha **uma** das duas opções abaixo:

#### Opção A: Executando diretamente pelo MySQL Workbench (Visual)
Se você utiliza o Workbench instalado em sua máquina, siga este fluxo simplificado:
1. Salve o script SQL estrutural completo em um arquivo de texto chamado `schema.sql` (ou abra uma nova aba de query no programa).
2. No menu superior do Workbench, clique em **File** -> **Open SQL Script...** e selecione o arquivo gerado.
3. Certifique-se de que a conexão local está ativa e clique no **ícone do raio (Execute)** na barra de ferramentas para processar todo o arquivo.
4. Clique com o botão direito na área de *Schemas* na barra lateral esquerda e selecione **Refresh All** para ver a nova base `estoque` mapeada.

#### Opção B: Executando diretamente pelo Terminal (CLI)
Se prefere importar o arquivo rapidamente por linha de comando utilizando o utilitário nativo do banco:
1. Abra o prompt do sistema operacional dentro da pasta onde salvou o arquivo `schema.sql`.
2. Rode o comando abaixo informando suas credenciais pessoais:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. Digite sua senha pessoal quando solicitado. O banco processará toda a estrutura de forma totalmente automatizada.

#### Script Estrutural Completo (`schema.sql`)
```sql
CREATE DATABASE IF NOT EXISTS `estoque` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `estoque`;

-- 1. TABELA DE PRODUTOS
DROP TABLE IF EXISTS `produtos`;
CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `valor_compra` decimal(10,2) DEFAULT NULL,
  `valor_venda` decimal(10,2) NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  `quantidade_minima` int NOT NULL DEFAULT '0',
  `ativo` enum('S','N') NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Carga inicial de produtos para amostragem base
INSERT INTO `produtos` VALUES 
(1,'Mouse Gamer',75.00,150.00,10,5,'S'),
(2,'Mochila',30.00,65.00,20,15,'S'),
(3,'Notebook Gamer',1000.00,2000.00,8,5,'S'),
(4,'Monitor Gamer',900.00,1500.00,5,2,'S'),
(5,'Televisão Samsung',1500.00,2500.00,3,3,'S'),
(6,'Caixa de Som',150.00,500.00,10,3,'S'),
(9,'PowerBank 10000mAh',30.00,80.00,10,10,'S'),
(10,'Caderno LogiTech',15.00,30.00,0,5,'S'),
(11,'Caderno Tilibra',8.00,30.00,41,5,'S'),
(14,'Samsung S22',1500.00,3000.00,0,1,'S'),
(15,'Moletom Pichau',100.00,130.00,0,15,'S');


-- 2. TABELA DE USUÁRIOS
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `celular` varchar(11) NOT NULL,
  `data_nascimento` date DEFAULT (curdate()),
  `cpf` varchar(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `perfil` enum('admin','comum') NOT NULL,
  `data_cadastro` date DEFAULT (curdate()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `celular` (`celular`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Massa de dados dos Administradores e Usuários Comuns nativos
INSERT INTO `usuarios` VALUES 
(1,'Otávio','12345678910','2006-01-10','12345678910','otavio@gmail.com','1234','admin','2026-08-18'),
(2,'Victória','12345678911','2007-05-08','12345678911','vic@gmail.com','5678','admin','2026-08-18'),
(5,'Mirela','12345678913','1973-10-03','12345678913','mirela@gmail.com','1001','admin','2026-08-18'),
(11,'Guilherme','12345678900','2010-09-17','12345678900','gui@gmail.com','0000','comum','2026-08-21'),
(12,'Patricia','12345678912','2005-01-01','12345678912','paty@gmail.com','0123','comum','2026-08-21');


-- 3. TABELA DE MOVIMENTAÇÕES
DROP TABLE IF EXISTS `movimentacoes`;
CREATE TABLE `movimentacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `produto_id` int NOT NULL,
  `nome_produto` varchar(100) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  `nome_usuario` varchar(100) DEFAULT NULL,
  `tipo` enum('ENTRADA','SAIDA') NOT NULL,
  `quantidade` int NOT NULL,
  `data_movimentacao` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `produto_id` (`produto_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `movimentacoes_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`),
  CONSTRAINT `movimentacoes_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 4. GATILHO (TRIGGER) PARA INTEGRIDADE DENORMALIZADA
DELIMITER ;;
CREATE TRIGGER `preencher_dados_movimentacao` BEFORE INSERT ON `movimentacoes` FOR EACH ROW 
BEGIN
    DECLARE nomeProdutoTemp VARCHAR(50);
    DECLARE nomeUsuarioTemp VARCHAR(100);

    SELECT nome INTO nomeProdutoTemp FROM produtos WHERE id = NEW.produto_id;
    SELECT nome INTO nomeUsuarioTemp FROM usuarios WHERE id = NEW.usuario_id;

    SET NEW.nome_produto = nomeProdutoTemp;
    SET NEW.nome_usuario = nomeUsuarioTemp;
END;;
DELIMITER ;
```

## 🏃 Mudando para Execução

Para iniciar o sistema, basta rodar o arquivo principal através do terminal:
```bash
python main.py
```

## 👤 Autor (Otávio)

* Desenvolvimento do ecossistema e regras de negócio do sistema de estoque.
