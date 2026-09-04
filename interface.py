import customtkinter as ctk
from tkinter import messagebox
import banco
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.after_atualizacao = None
            
        # Deixa a aplicação maximizada
        self.after(0,lambda: self.state("zoomed"))
        
        self.construir_telalogin()
    
    def abrir_sistema(self):
        
        # Essa função é responsável por abrir a interface principal do sistema de estoque. Ela configura a janela principal, cria a barra lateral e a área de abas, e adiciona as abas de "Estoque", "Movimentações" e "Usuários" dependendo do perfil do usuário logado. Além disso, ela chama funções para construir o conteúdo das abas e iniciar a atualização automática dos dados.
        
        self.title("Sistema de Estoque")
            
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
            
        #Barra Lateral
        self.barra_lateral = ctk.CTkFrame(self, width=200)
        self.barra_lateral.grid(row=0, column=0, sticky="nsew")
            
        #Parte Principal
        self.janela_abas = ctk.CTkTabview(self, width=400)
        self.janela_abas.grid(row=0, column=1, sticky="nsew", padx=10)
            
        self.janela_abas.add("Estoque")
        
        # Se o perfil do usuário logado for "admin", adiciona as abas de "Movimentações" e "Usuários"
        if banco.sessao['perfil'] == "admin":
            self.janela_abas.add("Movimentações")
            self.janela_abas.add("Usuários")
            
            self.construir_abamovimentacoes()
            self.construir_abausuarios()
          
        self.construir_abalateral()
        self.boas_vindas()
        
        self.construir_abaestoque()
        
        self.atualizar_automatico()
        
    def construir_abalateral(self):
        
        # Essa função é responsável por construir a barra lateral da interface do sistema de estoque. Ela cria um frame para exibir o ícone do usuário, adiciona labels para mostrar uma mensagem de boas-vindas e o nome do usuário logado, e inclui um switch para alternar entre os modos claro e escuro. Além disso, a função adiciona botões para acessar as configurações e atualizar o sistema, configurando suas cores e ações correspondentes.
        
        self.frame_usuario = ctk.CTkFrame(
            self.barra_lateral,
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#1f538d"
        )
        self.frame_usuario.pack(pady=(40,20),padx=20,side="top")
        self.frame_usuario.propagate(False)
        
        self.label_icone = ctk.CTkLabel(
            master=self.frame_usuario,
            text="👤",
            font=("Arial",28),
            text_color="white"
        )
        self.label_icone.place(rely=0.4,relx=0.5,anchor="center")
            
        
        self.titulo = ctk.CTkLabel(
            self.barra_lateral,
            text="Bem-Vindo"
        )
        self.titulo.pack(padx=20)
        
        self.subtitulo= ctk.CTkLabel(
            self.barra_lateral,
            text="",
            font=("Arial",20)
        )
        self.subtitulo.pack(pady=(0,100),padx=(20,20))
        
        self.switch_tema = ctk.CTkSwitch(
            self.barra_lateral,
            text="Modo Escuro",
            command= self.mudar_tema
        )
        self.switch_tema.pack(pady=(20,40),padx=20, side="bottom")
        self.switch_tema.select()
        
        self.botao_config = ctk.CTkButton(
            self.barra_lateral,
            text="Configurações ⚙️",
            command= self.construir_telaconfig
        )
        self.botao_config.pack(pady=20,padx=20,side="bottom")
        
        if ctk.get_appearance_mode() == "Dark":
            self.switch_tema.select()
        else:
            self.switch_tema.deselect()
            
        self.botao_atualizar = ctk.CTkButton(
            self.barra_lateral,
            text="🔄 Atualizar Sistema",
            fg_color="green",
            hover_color="darkgreen",
            command=self.atualizar_tudo
        )
        self.botao_atualizar.pack(pady=10, padx=20, side="bottom")
        
    def construir_abaestoque(self):
        
        # Essa função é responsável por construir a aba de "Estoque" na interface do sistema. Ela cria a aba correspondente, adiciona uma barra de opções com botões para entrada e saída de estoque, atualização, reativação e desativação de produtos, além de um botão para cadastrar novos produtos. A função também cria um frame para exibir a tabela de estoque e chama a função para atualizar os dados da tabela. A visibilidade e funcionalidade dos botões dependem do perfil do usuário logado (admin ou comum).
        
        self.aba_estoque = self.janela_abas.tab("Estoque")
        
        if banco.sessao['perfil'] == "admin":
        
            self.barra_opcoes = ctk.CTkFrame(
                self.aba_estoque,
                width=200,
            )
            self.barra_opcoes.pack(fill="y", side="left", padx=10)
            
            self.tabela_frame = ctk.CTkScrollableFrame(
                self.aba_estoque,
                width=560,
                height=340
            )
            self.tabela_frame.pack(pady=20,padx=20, fill="both", expand=True)
            
            self.atualizar_tabela_estoque()
            
            self.botao_entrada = ctk.CTkButton(
                self.barra_opcoes,
                text="Entrada Estoque",
                width=100,
                font=("Arial",20),
                fg_color="green",
                hover_color="darkgreen",
                command= self.construir_tela_entrada_estoque
            )
            self.botao_entrada.pack(pady=(10,50), padx=20,side="top")
            
            self.botao_atualizar_produto = ctk.CTkButton(
                self.barra_opcoes,
                text="Atualizar Produto",
                width=100,
                font=("Arial",20),
                fg_color="blue",
                hover_color="darkblue",
                command= self.construir_tela_atualiza_produto
            )
            self.botao_atualizar_produto.pack(pady=50,side="top")
            
            self.botao_saida = ctk.CTkButton(
                self.barra_opcoes,
                text="Saída Estoque",
                width=150,
                font=("Arial",20),
                fg_color="red",
                hover_color="darkred",
                command= self.construir_tela_saida_estoque
            )
            self.botao_saida.pack(pady=50, padx=20, side="top")
            
            self.botao_reativar_produto = ctk.CTkButton(
                self.barra_opcoes,
                text="Reativar produto",
                width=100,
                font=("Arial",20),
                fg_color="green",
                hover_color="darkgreen",
                command= self.construir_tela_reativar_produto
            )
            self.botao_reativar_produto.pack(pady=50, padx=20, side="top")
            
            self.botao_excluir_produto = ctk.CTkButton(
                self.barra_opcoes,
                text="Desativar Produto",
                width=100,
                font=("Arial",20),
                fg_color="red",
                hover_color="darkred",
                command= self.construir_tela_desativar_produto
            )
            self.botao_excluir_produto.pack(pady=50,padx=20, side="top")
            
            self.botao_cadastrar_produto = ctk.CTkButton(
                self.barra_opcoes,
                text="Cadastrar Produto",
                width=100,
                font=("Arial",20),
                fg_color="green",
                hover_color="darkgreen",
                command= self.construir_tela_cadastra_produto
            )
            self.botao_cadastrar_produto.pack(pady=50,padx=20, side="top")
            
        else:
            
            self.tabela_frame = ctk.CTkScrollableFrame(
                self.aba_estoque,
                width=560,
                height=340
            )
            self.tabela_frame.pack(pady=20,padx=20, fill="both", expand=True)
            
            self.atualizar_tabela_estoque()
            
            self.frame_botoes = ctk.CTkFrame(
                self.aba_estoque,
                width=600,
                height=100, 
                fg_color="transparent"
            )
            self.frame_botoes.pack(pady=40, padx=40, fill="x", side="bottom")
            
            self.botao_entrada = ctk.CTkButton(
                self.frame_botoes,
                text="Entrada Estoque",
                width=100,
                font=("Arial",20),
                fg_color="green",
                hover_color="darkgreen",
                command= self.construir_tela_entrada_estoque
            )
            self.botao_entrada.pack(side="right")
            
            self.botao_saida = ctk.CTkButton(
                self.frame_botoes,
                text="Saída Estoque",
                width=150,
                font=("Arial",20),
                fg_color="red",
                hover_color="darkred",
                command= self.construir_tela_saida_estoque
            )
            self.botao_saida.pack(side="left")
              
    def construir_abamovimentacoes(self):
        
        # Essa função é responsável por construir a aba de "Movimentações" na interface do sistema de estoque. Ela cria a aba correspondente e adiciona um frame rolável para exibir a tabela de movimentações. A função também chama a função para atualizar os dados da tabela de movimentações.
        
        self.aba_movimentacoes = self.janela_abas.tab("Movimentações")
        
        self.tabela_frame_mov = ctk.CTkScrollableFrame(
            self.aba_movimentacoes,
            width=560,
            height=340
        )
        self.tabela_frame_mov.pack(pady=20,padx=20, fill="both", expand=True)
        
        self.atualizar_tabela_movimentacoes()
    
    def construir_abausuarios(self):
            
        # Essa função é responsável por construir a aba de "Usuários" na interface do sistema de estoque. Ela cria a aba correspondente, adiciona um frame rolável para exibir a tabela de usuários e um frame para os botões de ação (Cadastrar, Atualizar e Excluir Usuário). A função também chama a função para atualizar os dados da tabela de usuários.      
            
        self.aba_usuarios = self.janela_abas.tab("Usuários")
            
        self.tabela_frame_usuario = ctk.CTkScrollableFrame(
            self.aba_usuarios,
            width=560,
            height=340
        )
        self.tabela_frame_usuario.pack(pady=20,padx=20, fill="both", expand=True)
            
        self.atualizar_tabela_usuarios()
        
        # Frame dos botões
        self.frame_botoes = ctk.CTkFrame(
            self.aba_usuarios,
            fg_color="transparent"
        )
        self.frame_botoes.pack(fill="x", padx=20, pady=20)

        # Três colunas com o mesmo tamanho
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)

        # Botão Cadastrar
        self.botao_cadastrar_usuario = ctk.CTkButton(
            self.frame_botoes,
            text="Cadastrar Usuário",
            fg_color="green",
            hover_color="darkgreen",
            width=180,
            font=("Arial", 20),
            command= self.construir_tela_cadastrar_usuario
        )
        self.botao_cadastrar_usuario.grid(row=0, column=0, sticky="w")

        # Botão Atualizar
        self.botao_atualizar_usuario = ctk.CTkButton(
            self.frame_botoes,
            text="Atualizar Usuário",
            fg_color="blue",
            hover_color="darkblue",
            width=180,
            font=("Arial", 20),
            command= self.construir_tela_atualizar_usuario
        )
        self.botao_atualizar_usuario.grid(row=0, column=1)

        # Botão Excluir
        self.botao_excluir_usuario = ctk.CTkButton(
            self.frame_botoes,
            text="Excluir Usuário",
            fg_color="red",
            hover_color="darkred",
            width=180,
            font=("Arial", 20),
            command=self.construir_tela_excluir_usuario
        )
        self.botao_excluir_usuario.grid(row=0, column=2, sticky="e")
    
    def construir_tela_atualizar_usuario(self):
        
        # Essa função é responsável por construir a tela de atualização de usuário na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do usuário, nome, celular, data de nascimento, CPF, e-mail, senha e perfil do usuário. Além disso, inclui botões para buscar o usuário pelo ID e salvar as alterações feitas. A função também chama a função para parar a atualização automática dos dados enquanto a tela de atualização está aberta.
        
        self.parar_atualizacao_automatica()

        self.janela_abas.destroy()
        self.barra_lateral.destroy()

        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )

        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)

        ctk.CTkLabel(
            self.aba,
            text="👤 Atualizar Usuário",
            font=("Arial", 22)
        ).pack(pady=20)

        # ID
        self.id_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do usuário",
            width=300
        )
        self.id_usuario.pack(pady=8)

        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Usuário",
            command=self.buscar_usuario
        )
        self.botao_buscar.pack(pady=(0, 20))

        # NOME
        self.nome_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome",
            width=300
        )
        self.nome_usuario.pack(pady=8)

        # CELULAR
        self.celular_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="(XX) XXXXX-XXXX",
            width=300
        )
        self.celular_usuario.pack(pady=8)

        self.celular_usuario.bind(
            "<KeyRelease>",
            self.mascara_celular_evento
        )

        # DATA
        self.data_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="DD/MM/AAAA",
            width=300
        )
        self.data_usuario.pack(pady=8)

        self.data_usuario.bind(
            "<KeyRelease>",
            self.mascara_data
        )

        # CPF
        self.cpf_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="CPF",
            width=300
        )
        self.cpf_usuario.pack(pady=8)

        self.cpf_usuario.bind(
            "<KeyRelease>",
            self.mascara_cpf
        )

        # EMAIL
        self.email_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="E-mail",
            width=300
        )
        self.email_usuario.pack(pady=8)

        # FRAME DA SENHA
        self.frame_senha = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_senha.pack(pady=8)
        
        # SENHA
        self.senhac = ctk.CTkEntry(
            self.frame_senha,
            placeholder_text="Nova senha (deixe em branco para manter)",
            width=255,
            show="*"
        )
        self.senhac.pack(side="left")
        
        # BOTÃO OLHO
        self.botao_mostrar_senha = ctk.CTkButton(
            self.frame_senha,
            text="👁️",
            width=45,
            height=28,
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.mostrar_senhac
        )
        self.botao_mostrar_senha.pack(
            side="left",
            padx=(5, 0)
        )
            

        self.perfil_usuario = ctk.CTkOptionMenu(
            self.aba,
            values=["admin","comum"],
            width=300
        )
        self.perfil_usuario.pack(pady=8)

        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="Salvar Alterações",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.salvar_usuario
        )
        self.botao_salvar.pack(pady=25)
        
    def construir_tela_cadastrar_usuario(self):
        
        # Essa função é responsável por construir a tela de cadastro de usuário na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o nome, celular, data de nascimento, CPF, e-mail, senha e perfil do usuário. Além disso, inclui um botão para cadastrar o usuário. A função também chama a função para parar a atualização automática dos dados enquanto a tela de cadastro está aberta.
        
        self.parar_atualizacao_automatica()

        self.janela_abas.destroy()
        self.barra_lateral.destroy()

        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )

        # BOTÃO VOLTAR
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)

        # TÍTULO
        ctk.CTkLabel(
            self.aba,
            text="👤 Cadastrar Usuário",
            font=("Arial", 22)
        ).pack(pady=20)

        # NOME
        self.nome_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome",
            width=300
        )
        self.nome_usuario.pack(pady=8)

        # CELULAR
        self.celular_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="(XX) XXXXX-XXXX",
            width=300
        )
        self.celular_usuario.pack(pady=8)

        self.celular_usuario.bind(
            "<KeyRelease>",
            self.mascara_celular_evento
        )

        # DATA DE NASCIMENTO
        self.data_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="DD/MM/AAAA",
            width=300
        )
        self.data_usuario.pack(pady=8)

        self.data_usuario.bind(
            "<KeyRelease>",
            self.mascara_data
        )

        # CPF
        self.cpf_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="CPF",
            width=300
        )
        self.cpf_usuario.pack(pady=8)

        self.cpf_usuario.bind(
            "<KeyRelease>",
            self.mascara_cpf
        )

        # EMAIL
        self.email_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="E-mail",
            width=300
        )
        self.email_usuario.pack(pady=8)

        # FRAME DA SENHA
        self.frame_senha = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_senha.pack(pady=8)

        # CAMPO SENHA
        self.senhac = ctk.CTkEntry(
            self.frame_senha,
            placeholder_text="Senha",
            width=255,
            show="*"
        )
        self.senhac.pack(side="left")

        # BOTÃO OLHO
        self.botao_mostrar_senha = ctk.CTkButton(
            self.frame_senha,
            text="👁️",
            width=45,
            height=28,
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.mostrar_senhac
        )
        self.botao_mostrar_senha.pack(
            side="left",
            padx=(5, 0)
        )

        # PERFIL
        self.perfil_usuario = ctk.CTkOptionMenu(
            self.aba,
            values=["admin", "comum"],
            width=300
        )
        self.perfil_usuario.set("comum")
        self.perfil_usuario.pack(pady=8)

        # BOTÃO CADASTRAR
        self.botao_cadastrar = ctk.CTkButton(
            self.aba,
            text="Cadastrar Usuário",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.cadastrar_usuario_tela
        )
        self.botao_cadastrar.pack(pady=25)
        
    def cadastrar_usuario_tela(self):

        # Essa função é responsável por cadastrar um novo usuário no sistema de estoque. Ela coleta os dados inseridos nos campos de entrada da tela de cadastro, valida se todos os campos obrigatórios foram preenchidos e, em seguida, chama a função do módulo "banco" para realizar o cadastro no banco de dados. Se o cadastro for bem-sucedido, exibe uma mensagem de sucesso e limpa os campos da tela. Caso ocorra algum erro durante o processo, exibe uma mensagem de erro.
        
        nome = self.nome_usuario.get().strip()
        celular = self.celular_usuario.get().strip()
        data_nascimento = self.data_usuario.get().strip()
        cpf = self.cpf_usuario.get().strip()
        email = self.email_usuario.get().strip()
        senha = self.senhac.get().strip()
        perfil = self.perfil_usuario.get().strip()

        # Verifica os campos
        if not nome:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Nome."
            )
            return

        if not celular:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Celular."
            )
            return

        if not data_nascimento:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Data de nascimento."
            )
            return

        if not cpf:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo CPF."
            )
            return

        if not email:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo E-mail."
            )
            return

        if not senha:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Senha."
            )
            return

        if not perfil:
            messagebox.showwarning(
                "Atenção",
                "Selecione o perfil do usuário."
            )
            return

        try:

            banco.cadastrar_usuario(
                nome,
                celular,
                data_nascimento,
                cpf,
                email,
                senha,
                perfil
            )

            messagebox.showinfo(
                "Sucesso",
                "Usuário cadastrado com sucesso!"
            )

            # LIMPA OS CAMPOS
            self.nome_usuario.delete(0, "end")
            self.celular_usuario.delete(0, "end")
            self.data_usuario.delete(0, "end")
            self.cpf_usuario.delete(0, "end")
            self.email_usuario.delete(0, "end")
            self.senhac.delete(0, "end")

            self.perfil_usuario.set("usuario")
            
            self.barra_lateral.destroy()
            self.aba.destroy()
            
            self.voltar_sistema()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )
        
    def construir_tela_excluir_usuario(self):

        # Essa função é responsável por construir a tela de exclusão de usuário na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do usuário, nome, celular, data de nascimento, CPF, e-mail e perfil do usuário. Além disso, inclui botões para buscar o usuário pelo ID e excluir o usuário. A função também chama a função para parar a atualização automática dos dados enquanto a tela de exclusão está aberta.
        
        self.parar_atualizacao_automatica()

        self.janela_abas.destroy()
        self.barra_lateral.destroy()

        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(row=0,column=0,sticky="nsew")

        self.aba = ctk.CTkFrame(self)
        self.aba.grid(row=0,column=1,sticky="nsew",padx=10)

        # BOTÃO VOLTAR
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)

        # TÍTULO
        ctk.CTkLabel(
            self.aba,
            text="👤 Excluir Usuário",
            font=("Arial", 22)
        ).pack(pady=20)

        # ID
        self.id_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do usuário",
            width=300
        )
        self.id_usuario.pack(pady=8)

        # BUSCAR
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Usuário",
            command=self.buscar_usuario
        )
        self.botao_buscar.pack(pady=(0, 20))

        # NOME
        self.nome_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome",
            width=300
        )
        self.nome_usuario.pack(pady=8)

        # CELULAR
        self.celular_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="(XX) XXXXX-XXXX",
            width=300
        )
        self.celular_usuario.pack(pady=8)

        self.celular_usuario.bind(
            "<KeyRelease>",
            self.mascara_celular_evento
        )

        # DATA
        self.data_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="DD/MM/AAAA",
            width=300
        )
        self.data_usuario.pack(pady=8)

        self.data_usuario.bind(
            "<KeyRelease>",
            self.mascara_data
        )

        # CPF
        self.cpf_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="CPF",
            width=300
        )
        self.cpf_usuario.pack(pady=8)

        self.cpf_usuario.bind(
            "<KeyRelease>",
            self.mascara_cpf
        )

        # EMAIL
        self.email_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="E-mail",
            width=300
        )
        self.email_usuario.pack(pady=8)

        # PERFIL
        self.perfil_usuario = ctk.CTkOptionMenu(
            self.aba,
            values=["admin", "usuario"],
            width=300
        )
        self.perfil_usuario.pack(pady=8)

        # BOTÃO EXCLUIR
        self.botao_excluir = ctk.CTkButton(
            self.aba,
            text="Excluir Usuário",
            fg_color="red",
            hover_color="darkred",
            font=("Arial", 20),
            command=self.excluir_usuario_tela
        )
        self.botao_excluir.pack(pady=25)
        
    def excluir_usuario_tela(self):

        # Essa função é responsável por excluir um usuário do sistema de estoque. Ela coleta o ID do usuário inserido no campo de entrada da tela de exclusão, valida se o ID foi preenchido e se é um número. Em seguida, solicita a senha do administrador para autorização da exclusão. Se a senha estiver correta, chama a função do módulo "banco" para realizar a exclusão no banco de dados. Se a exclusão for bem-sucedida, exibe uma mensagem de sucesso e limpa os campos da tela. Caso ocorra algum erro durante o processo ou se a senha for inválida, exibe uma mensagem de erro.
        
        id_usuario = self.id_usuario.get().strip()

        # Verifica se o ID foi preenchido
        if not id_usuario:

            messagebox.showwarning(
                "Atenção",
                "Digite o ID do usuário."
            )

            return

        # Verifica se o ID é número
        if not id_usuario.isdigit():

            messagebox.showwarning(
                "Atenção",
                "O ID deve ser um número."
            )

            return
        
        if int(id_usuario) == banco.sessao['id']:
            messagebox.showwarning(
                "Atenção",
                "Você não pode excluir o seu próprio usuário."
            )

            return

        # Pede a senha do administrador
        dialogo = ctk.CTkInputDialog(
            text="Digite a senha do administrador:",
            title="Autorização"
        )

        senha_admin = dialogo.get_input()

        # Se cancelou
        if senha_admin is None:
            return

        # Se deixou vazio
        if not senha_admin.strip():

            messagebox.showwarning(
                "Atenção",
                "Digite a senha do administrador."
            )

            return

        if str(banco.sessao['senha']) == senha_admin:
        
            try:

                # Chama a função do banco
                banco.excluir_usuario(
                    int(id_usuario),
                    senha_admin
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Usuário excluído com sucesso."
                )

                # Limpa os campos
                self.id_usuario.delete(0, "end")
                self.nome_usuario.delete(0, "end")
                self.celular_usuario.delete(0, "end")
                self.data_usuario.delete(0, "end")
                self.cpf_usuario.delete(0, "end")
                self.email_usuario.delete(0, "end")
                
                self.voltar_sistema()

            except Exception as erro:

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )
                
        else:
            
            messagebox.showerror(
                "Erro",
                "Senha Inválida"
            )
        
    def buscar_usuario(self):

        # Essa função é responsável por buscar um usuário no sistema de estoque com base no ID fornecido. Ela coleta o ID do usuário inserido no campo de entrada, valida se o ID foi preenchido e se é um número. Em seguida, chama a função do módulo "banco" para buscar o usuário no banco de dados. Se o usuário for encontrado, os campos da tela são preenchidos com as informações do usuário, incluindo nome, celular, data de nascimento, CPF, e-mail e perfil. Caso ocorra algum erro durante o processo ou se o ID não for válido, exibe uma mensagem de erro.
        
        try:

            id_usuario = self.id_usuario.get().strip()

            if not id_usuario:
                messagebox.showwarning(
                    "Buscar Usuário",
                    "Digite o ID do usuário."
                )
                return

            if not id_usuario.isdigit():
                messagebox.showwarning(
                    "Buscar Usuário",
                    "O ID deve conter apenas números."
                )
                return

            usuario = banco.buscar_usuario_por_id(
                int(id_usuario)
            )

            # Limpa os campos
            self.nome_usuario.delete(0, "end")
            self.celular_usuario.delete(0, "end")
            self.data_usuario.delete(0, "end")
            self.cpf_usuario.delete(0, "end")
            self.email_usuario.delete(0, "end")

            # Nome
            self.nome_usuario.insert(
                0,
                usuario["nome"]
            )

            # Celular
            celular = usuario["celular"]

            if celular:

                celular = self.formatar_numero_label(
                    celular
                )

                self.celular_usuario.insert(
                    0,
                    celular
                )

            # Data
            data = usuario["data_nascimento"]

            if data:

                if hasattr(data, "strftime"):

                    data = data.strftime(
                        "%d/%m/%Y"
                    )

                else:

                    data = str(data)

                    try:

                        data = datetime.strptime(
                            data,
                            "%Y-%m-%d"
                        ).strftime("%d/%m/%Y")

                    except ValueError:
                        pass

                self.data_usuario.insert(
                    0,
                    data
                )

            # CPF
            cpf = usuario["cpf"]

            if cpf:

                cpf = self.formatar_cpf(
                    cpf
                )

                self.cpf_usuario.insert(
                    0,
                    cpf
                )

            # E-mail
            if usuario["email"]:

                self.email_usuario.insert(
                    0,
                    usuario["email"]
                )

            # Perfil
            perfil = usuario["perfil"]

            if perfil == "admin":

                # Usuário admin só pode continuar como admin
                self.perfil_usuario.configure(
                    values=["admin"]
                )

                self.perfil_usuario.set("admin")

            else:

                # Usuário comum pode ser comum ou admin
                self.perfil_usuario.configure(
                    values=["admin", "comum"]
                )

                self.perfil_usuario.set("comum")

        except Exception as erro:

            messagebox.showerror(
                "Buscar Usuário",
                str(erro)
            )
            
    def formatar_celular(self, celular):

        # Essa função é responsável por formatar um número de celular no formato brasileiro. Ela recebe um número de celular como entrada, remove todos os caracteres que não são dígitos e verifica o comprimento do número resultante. Se o número tiver 11 dígitos, ele será formatado como "(XX) XXXXX-XXXX". Se tiver 10 dígitos, será formatado como "(XX) XXXX-XXXX". Caso contrário, o número será retornado sem formatação.
        
        numeros = "".join(
            filter(str.isdigit, str(celular))
        )

        if len(numeros) == 11:

            return (
                f"({numeros[:2]}) "
                f"{numeros[2:7]}-"
                f"{numeros[7:]}"
            )

        elif len(numeros) == 10:

            return (
                f"({numeros[:2]}) "
                f"{numeros[2:6]}-"
                f"{numeros[6:]}"
            )

        return numeros
    
    def mascara_celular_evento(self, event):

        # Essa função é responsável por aplicar uma máscara de formatação em tempo real no campo de entrada de celular. Ela é acionada sempre que uma tecla é liberada no campo de entrada. A função obtém o valor atual do campo, remove todos os caracteres que não são dígitos e aplica a formatação adequada com base no comprimento do número. O resultado formatado é então inserido de volta no campo de entrada.
        
        campo = event.widget

        numeros = "".join(
            filter(str.isdigit, campo.get())
        )

        numeros = numeros[:11]

        if len(numeros) <= 2:

            texto = numeros

        elif len(numeros) <= 7:

            texto = f"({numeros[:2]}) {numeros[2:]}"

        else:

            texto = (
                f"({numeros[:2]}) "
                f"{numeros[2:7]}-"
                f"{numeros[7:]}"
            )

        campo.delete(
            0,
            "end"
        )

        campo.insert(
            0,
            texto
        )

    def formatar_cpf(self, cpf):

        # Essa função é responsável por formatar um número de CPF no formato brasileiro. Ela recebe um número de CPF como entrada, remove todos os caracteres que não são dígitos e verifica o comprimento do número resultante. Se o número tiver 11 dígitos, ele será formatado como "XXX.XXX.XXX-XX". Caso contrário, o número será retornado sem formatação.
        
        numeros = "".join(filter(str.isdigit, str(cpf)))

        if len(numeros) == 11:
            return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

        return numeros
            
    def salvar_usuario(self):
        
        # Essa função é responsável por salvar as alterações feitas em um usuário existente no sistema de estoque. Ela coleta o ID do usuário e os dados atualizados inseridos nos campos de entrada da tela de atualização, valida se o ID foi preenchido e se é um número. Em seguida, solicita a senha do administrador para autorização da atualização. Se a senha estiver correta, chama a função do módulo "banco" para realizar a atualização no banco de dados. Se a atualização for bem-sucedida, exibe uma mensagem de sucesso e decide se encerra a sessão do usuário atualizado ou retorna à tela principal do sistema. Caso ocorra algum erro durante o processo ou se a senha for inválida, exibe uma mensagem de erro.
        
        try:

            id_usuario = self.id_usuario.get().strip()

            if not id_usuario:
                raise Exception(
                    "Digite o ID do usuário."
                )

            if not id_usuario.isdigit():
                raise Exception(
                    "O ID deve conter apenas números."
                )
                
            # Pede a senha do administrador
            dialogo = ctk.CTkInputDialog(
                text="Digite a senha do administrador:",
                title="Autorização"
            )
            senha_admin = dialogo.get_input()
            
            # Se cancelou
            if senha_admin is None:
                return
            
            # Se deixou vazio
            if not senha_admin.strip():
                messagebox.showwarning(
                    "Atenção",
                    "Digite a senha do administrador."
                )
                return
            
            if str(banco.sessao['senha']) == senha_admin:
                banco.atualizar_usuario(
                    int(id_usuario),
                    self.nome_usuario.get(),
                    self.celular_usuario.get(),
                    self.data_usuario.get(),
                    self.cpf_usuario.get(),
                    self.email_usuario.get(),
                    self.senha_usuario.get(),
                    self.perfil_usuario.get()
                )

                messagebox.showinfo(
                    "Atualizar Usuário",
                    "Usuário atualizado com sucesso!"
                )
                
                if int(id_usuario) == banco.sessao['id']: 
                    self.encerrar_sessao()
                else:
                    self.voltar_sistema()
                
            else:
                messagebox.showerror(
                    "Erro",
                    "Senha Inválida"
                )

        except Exception as erro:

            messagebox.showerror(
                "Atualizar Usuário",
                str(erro)
            )
    
    def construir_telalogin(self):
        
        # Essa função é responsável por construir a tela de login na interface do sistema de estoque. Ela cria um frame principal para o login, adiciona campos de entrada para o e-mail ou ID do usuário e a senha, além de botões para efetuar o login e mostrar/ocultar a senha. A função também define o título da janela como "Tela Login".
          
        self.title("Tela Login")

        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(fill="both", expand=True)
        
        self.label_usuario = ctk.CTkLabel(
            self.frame_login,
            text="Digite seu email ou ID"
        )
        self.label_usuario.pack(pady=(120,10))
        
        self.usuario = ctk.CTkEntry(
            self.frame_login,
            placeholder_text="Tente xxxxx@gmail.com ou Digite seu ID",
            width=300
        )
        self.usuario.pack(pady=(10,20))
        
        self.frame = ctk.CTkFrame (
            self.frame_login,
            fg_color="transparent",
            width=600,
            height=100
        )
        self.frame.pack(fill="x")
        
        self.label_senha = ctk.CTkLabel(
            self.frame,
            text="Senha"
        )
        self.label_senha.pack()
        
        self.senha = ctk.CTkEntry(
            self.frame,
            placeholder_text="Digite sua senha (Enter your password)",
            width=300,
            show="*"
        )
        self.senha.pack(pady=20)
        
        self.botao_ver = ctk.CTkButton(
            self.frame_login,
            text="👀",
            fg_color="gray",
            hover_color="darkgray",
            text_color=("black","white"),
            font=("Arial",20),
            width=1,
            command= self.mostrar_senha
        )
        self.botao_ver.place(rely=0.349, relx=0.61, anchor="center")
        
        self.botao_login = ctk.CTkButton(
            self.frame_login,
            text="Efetuar Login",
            fg_color="green",
            hover_color="darkgreen",
            command= self.realizar_login
        )
        self.botao_login.pack()
        
    def realizar_login(self):
        
        # Essa função é responsável por realizar o login do usuário no sistema de estoque. Ela coleta o e-mail ou ID do usuário e a senha inseridos nos campos de entrada da tela de login, chama a função do módulo "banco" para verificar as credenciais no banco de dados e, se o login for bem-sucedido, inicia a sessão do usuário, exibe uma mensagem de boas-vindas e abre a interface principal do sistema. Caso as credenciais sejam inválidas, exibe uma mensagem de erro.
        
        email = self.usuario.get()
        senha = self.senha.get()
        
        usuario = banco.login_usuario(email,senha)
        
        if usuario is not None:
            
            banco.iniciar_sessao(usuario)
            
            messagebox.showinfo(
                "Login",
                f"Bem-Vindo {usuario['nome']}"
            )
            
            self.frame_login.destroy()
            
            self.abrir_sistema()
            
        else:
            
            messagebox.showerror(
                "Erro",
                "Usuário ou senha inválidos"
            )
        
    def mudar_tema(self):
        
        # Essa função é responsável por alterar o tema da interface do sistema de estoque entre os modos "Dark" e "System". Ela verifica o valor da variável `switch_tema` e, com base nesse valor, define o modo de aparência usando a função `set_appearance_mode` da biblioteca `ctk`. Se o valor for 1, o tema será alterado para "Dark"; caso contrário, será definido como "System".
        
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System")

    def boas_vindas(self):
        
        # Essa função é responsável por exibir uma mensagem de boas-vindas ao usuário logado no sistema de estoque. Ela obtém o nome do usuário a partir da sessão iniciada no banco de dados e atualiza o texto do rótulo `subtitulo` para exibir uma saudação personalizada com o nome do usuário.
        
        nome = banco.sessao['nome']
        
        self.subtitulo.configure(text=f"{nome}")
        
    def construir_telaconfig(self):

        # Essa função é responsável por construir a tela de configurações da conta do usuário na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de exibição para o nome completo, data de nascimento, CPF e e-mail do usuário, além de botões para voltar à tela principal e encerrar a sessão. A função também chama a função para parar a atualização automática dos dados enquanto a tela de configurações está aberta.
        
        self.parar_atualizacao_automatica()

        self.barra_lateral.destroy()
        self.janela_abas.destroy()

        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(row=0,column=0,sticky="nsew")

        self.aba = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.aba.grid(row=0,column=1,sticky="nsew",padx=20,pady=20)

        self.aba.grid_columnconfigure(0, weight=1)
        self.aba.grid_columnconfigure(1, weight=1)

        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20,padx=20,side="top")

        self.botao_logout = ctk.CTkButton(
            self.barra_lateral,
            text="Encerrar Sessão",
            command=self.encerrar_sessao,
            fg_color="red",
            hover_color="darkred",
            font=("Arial", 15)
        )
        self.botao_logout.pack(pady=20,padx=20,side="bottom",fill="x")

        self.titulo_config = ctk.CTkLabel(
            self.aba,
            text="Configurações da conta",
            font=("Arial", 26, "bold")
        )
        self.titulo_config.grid(row=0,column=0,columnspan=2,sticky="w",padx=10,pady=(0, 20))

        self.frame_nome = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_nome.grid(row=1,column=0,padx=10,pady=8,sticky="ew")
        self.frame_nome.grid_columnconfigure(0, weight=1)

        self.label_nome_titulo = ctk.CTkLabel(
            self.frame_nome,
            text="Nome completo",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_nome_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        self.label_nome = ctk.CTkLabel(
            self.frame_nome,
            text=f"{banco.sessao['nome']}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_nome.grid(row=1,column=0,sticky="ew")
        
        self.frame_nasc = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_nasc.grid(row=1,column=1,padx=10,pady=8,sticky="ew")
        self.frame_nasc.grid_columnconfigure(0, weight=1)

        self.label_nasc_titulo = ctk.CTkLabel(
            self.frame_nasc,
            text="Data de nascimento",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_nasc_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        self.label_data_nasc = ctk.CTkLabel(
            self.frame_nasc,
            text=f"{banco.sessao['data_nascimento']:%d/%m/%Y}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_data_nasc.grid(row=1,column=0,sticky="ew")

        self.frame_cpf = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_cpf.grid(row=2,column=0,padx=10,pady=8,sticky="ew")
        self.frame_cpf.grid_columnconfigure(0, weight=1)

        self.label_cpf_titulo = ctk.CTkLabel(
            self.frame_cpf,
            text="CPF",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_cpf_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))
        
        self.label_cpf = ctk.CTkLabel(
            self.frame_cpf,
            text=f"{banco.sessao['cpf'][:3]}.***.***-{banco.sessao['cpf'][-2:]}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )

        self.label_cpf.grid(row=1,column=0,sticky="ew")

        self.frame_email = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_email.grid(row=2,column=1,padx=10,pady=8,sticky="ew")
        self.frame_email.grid_columnconfigure(0, weight=1)

        self.label_email_titulo = ctk.CTkLabel(
            self.frame_email,
            text="E-mail",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_email_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        self.label_email = ctk.CTkLabel(
            self.frame_email,
            text=f"{banco.sessao['email']}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_email.grid(row=1,column=0,sticky="ew")

        self.frame_contato = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_contato.grid(row=3,column=0,padx=10,pady=8,sticky="ew")
        self.frame_contato.grid_columnconfigure(0, weight=1)

        self.label_contato_titulo = ctk.CTkLabel(
            self.frame_contato,
            text="Telefone celular",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_contato_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        celular_formatado = self.formatar_numero_label(
            banco.sessao['celular']
        )

        self.label_celular = ctk.CTkLabel(
            self.frame_contato,
            text=celular_formatado,
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_celular.grid(row=1,column=0,sticky="ew")

        self.frame_id = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_id.grid(row=3,column=1,padx=10,pady=8,sticky="ew")
        self.frame_id.grid_columnconfigure(0, weight=1)

        self.label_id_titulo = ctk.CTkLabel(
            self.frame_id,
            text="ID",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_id_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        self.label_id = ctk.CTkLabel(
            self.frame_id,
            text=f"{banco.sessao['id']}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_id.grid(row=1,column=0,sticky="ew")

        self.frame_permissoes = ctk.CTkFrame(
            self.aba,
            fg_color="transparent"
        )
        self.frame_permissoes.grid(row=4,column=0,padx=10,pady=8,sticky="ew")
        self.frame_permissoes.grid_columnconfigure(0, weight=1)

        self.label_perfil_titulo = ctk.CTkLabel(
            self.frame_permissoes,
            text="Permissões",
            font=("Arial", 14),
            anchor="w"
        )
        self.label_perfil_titulo.grid(row=0,column=0,sticky="w",padx=5,pady=(0, 4))

        self.label_nivelperfil = ctk.CTkLabel(
            self.frame_permissoes,
            text=f"{banco.sessao['perfil'].capitalize()}",
            font=("Arial", 16),
            anchor="w",
            height=45,
            corner_radius=5,
            fg_color=("white", "#2b2b2b"),
            border_width=1,
            border_color=("gray70", "gray40")
        )
        self.label_nivelperfil.grid(row=1,column=0,sticky="ew")
              
    def encerrar_sessao(self):
        
        # Essa função é responsável por encerrar a sessão do usuário no sistema de estoque. Ela chama a função do módulo "banco" para encerrar a sessão, exibe uma mensagem de aviso informando que o usuário foi desconectado, destrói a aba e a barra lateral da interface atual e, em seguida, reconstrói a tela de login para permitir que outro usuário faça login.
        
        banco.encerrar_sessao()
        
        messagebox.showwarning(
            "Logout",
            "Usuário Desconectado"
        )
        
        self.aba.destroy()
        self.barra_lateral.destroy()
        
        self.construir_telalogin()
        
    def voltar_sistema(self):

        # Essa função é responsável por retornar à tela principal do sistema de estoque. Ela destrói a barra lateral e a aba da interface atual e, em seguida, chama a função para abrir a interface principal do sistema.
        
        self.barra_lateral.destroy()
        self.aba.destroy()

        self.abrir_sistema()

    def voltar_config(self):

        # Essa função é responsável por retornar à tela de configurações da conta do usuário. Ela destrói a barra lateral e a aba da interface atual e, em seguida, chama a função para construir a tela de configurações.
        
        self.barra_lateral.destroy()
        self.aba.destroy()

        self.construir_telaconfig()    
    
    def mostrar_senha(self):
        
        # Essa função é responsável por alternar a visibilidade da senha no campo de entrada da tela de login. Ela verifica o estado atual do campo de senha e, se a senha estiver oculta (representada por "*"), ela a torna visível; caso contrário, ela a oculta novamente.
        
        if self.senha.cget("show") == "*":
            self.senha.configure(show="")
        else:
            self.senha.configure(show="*")
            
    def mostrar_senhac(self):
        
        # Essa função é responsável por alternar a visibilidade da senha no campo de entrada da tela de cadastro. Ela verifica o estado atual do campo de senha e, se a senha estiver oculta (representada por "*"), ela a torna visível; caso contrário, ela a oculta novamente.
         
        if self.senhac.cget("show") == "*":
            self.senhac.configure(show="")
        else:
            self.senhac.configure(show="*")
      
    def validar_e_mascarar(self, variavel_texto, componente_entry):
        
        # Essa função é responsável por validar e aplicar uma máscara de formatação em tempo real no campo de entrada de celular. Ela é acionada sempre que uma tecla é liberada no campo de entrada. A função obtém o valor atual do campo, remove todos os caracteres que não são dígitos, aplica a formatação adequada com base no comprimento do número e atualiza o campo de entrada com o texto formatado. Além disso, ela mantém a posição do cursor correta após a formatação, garantindo uma experiência de digitação suave para o usuário.
        
        valor_atual = variavel_texto.get()
        
        # Guarda a posição atual do cursor antes de alterar o texto
        posicao_cursor = componente_entry.index("insert")
        
        # Filtra mantendo apenas números
        numeros = "".join(filter(str.isdigit, valor_atual))[:11]
        
        # Aplica a máscara dinamicamente
        texto_formatado = ""
        tam = len(numeros)
        
        if tam > 0:
            texto_formatado += f"({numeros[:2]}"
        if tam > 2:
            texto_formatado += f") {numeros[2:7]}"
        if tam > 7:
            texto_formatado += f"-{numeros[7:]}"
            
        # Atualiza o campo apenas se houver mudança real
        if valor_atual != texto_formatado:
            variavel_texto.set(texto_formatado)
            
            # Se o usuário estava digitando no final do texto, calculamos a nova posição
            if posicao_cursor >= len(valor_atual):
                nova_posicao = len(texto_formatado)
            else:
                # Caso ele esteja editando o meio do texto, calcula o deslocamento proporcional
                mascara_antes = sum(1 for c in valor_atual[:posicao_cursor] if not c.isdigit())
                numeros_antes = posicao_cursor - mascara_antes
                
                nova_posicao = 0
                contagem_num = 0
                for char in texto_formatado:
                    if contagem_num >= numeros_antes:
                        if not char.isdigit():
                            nova_posicao += 1
                        break
                    if char.isdigit():
                        contagem_num += 1
                    nova_posicao += 1

            # O SEGREDO: Agenda a correção do cursor para 1 milissegundo depois.
            # Isso burla o comportamento padrão do Tkinter que puxava o cursor de volta.
            self.after(1, lambda: componente_entry.icursor(nova_posicao))
            
    def formatar_numero_label(self, numero_cru):
        
        # Essa função é responsável por formatar um número de telefone ou celular para exibição em um rótulo (label) na interface do sistema de estoque. Ela recebe um número cru como entrada, remove quaisquer caracteres que não sejam dígitos e verifica o comprimento do número resultante. Se o número tiver 11 dígitos, ele será formatado como "(XX) XXXXX-XXXX". Se tiver 10 dígitos, será formatado como "(XX) XXXX-XXXX". Caso contrário, o número será retornado sem formatação.
        
        # Remove qualquer caractere residual e limpa o texto
        numeros = "".join(filter(str.isdigit, str(numero_cru)))
        
        # Se for um celular válido com DDD (11 dígitos): (XX) XXXXX-XXXX
        if len(numeros) == 11:
            return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
        # Se for um fixo válido com DDD (10 dígitos): (XX) XXXX-XXXX
        elif len(numeros) == 10:
            return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
        
        # Se não tiver o tamanho padrão, retorna o número original limpo
        return numeros
    
    def mascara_data(self, event):

        # Essa função é responsável por aplicar uma máscara de formatação em tempo real no campo de entrada de data. Ela é acionada sempre que uma tecla é liberada no campo de entrada. A função obtém o valor atual do campo, remove todos os caracteres que não são dígitos e aplica a formatação adequada com base no comprimento do número. O resultado formatado é então inserido de volta no campo de entrada.
        
        texto = "".join(filter(str.isdigit, event.widget.get()))[:8]

        if len(texto) > 4:
            texto = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
        elif len(texto) > 2:
            texto = f"{texto[:2]}/{texto[2:]}"

        event.widget.delete(0, "end")
        event.widget.insert(0, texto)
        
    def mascara_cpf(self, event):

        # Essa função é responsável por aplicar uma máscara de formatação em tempo real no campo de entrada de CPF. Ela é acionada sempre que uma tecla é liberada no campo de entrada. A função obtém o valor atual do campo, remove todos os caracteres que não são dígitos e aplica a formatação adequada com base no comprimento do número. O resultado formatado é então inserido de volta no campo de entrada.
        
        cpf = "".join(filter(str.isdigit, event.widget.get()))[:11]

        if len(cpf) > 9:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        elif len(cpf) > 3:
            cpf = f"{cpf[:3]}.{cpf[3:]}"
        else:
            cpf = cpf

        event.widget.delete(0, "end")
        event.widget.insert(0, cpf)
    
    def atualizar_tudo(self):
        """Atualiza todas as tabelas do sistema."""

        if hasattr(self, "tabela_frame"):
            self.atualizar_tabela_estoque()
            
        if banco.sessao['perfil'] == 'admin':

            if hasattr(self, "tabela_frame_usuario"):
                self.atualizar_tabela_usuarios()

            if hasattr(self, "tabela_frame_mov"):
                self.atualizar_tabela_movimentacoes()
        
    def atualizar_tabela_estoque(self):

        # Limpa a tabela
        for widget in self.tabela_frame.winfo_children():
            widget.destroy()

        conexao = banco.conectar()
        cursor = conexao.cursor()

        if banco.sessao['perfil'] == 'admin':

            cursor.execute("SELECT * FROM produtos")
            dados = cursor.fetchall()

            colunas = [
                "ID", "Nome do Produto", "Valor Compra",
                "Valor Venda", "Qtd", "Qtd Mínima", "Ativo"
            ]

        else:

            cursor.execute("""
                SELECT id, nome, valor_compra, valor_venda,
                    quantidade, quantidade_minima
                FROM produtos
                WHERE ativo = 'S'
            """)
            dados = cursor.fetchall()

            colunas = [
                "ID", "Nome do Produto", "Valor Compra",
                "Valor Venda", "Qtd", "Qtd Mínima"
            ]

        conexao.close()

        # Lista dos produtos ativos com estoque baixo
        produtos_estoque_baixo = []

        # Configuração das colunas
        for i in range(len(colunas)):
            peso = 2 if i == 1 else 1
            self.tabela_frame.grid_columnconfigure(i, weight=peso)

        # Cabeçalhos
        for col_idx, texto_coluna in enumerate(colunas):

            header = ctk.CTkLabel(
                self.tabela_frame,
                text=texto_coluna,
                font=("Arial", 14, "bold"),
                anchor="w",
                text_color="#3a7ebf"
            )

            header.grid(
                row=0,
                column=col_idx,
                padx=8,
                pady=(5, 15),
                sticky="ew"
            )

        # Dados
        for row_idx, linha in enumerate(dados, start=1):

            # Verifica se o produto está com estoque baixo
            estoque_baixo = False

            if banco.sessao['perfil'] == 'admin':

                id_produto = linha[0]
                nome = linha[1]
                quantidade = linha[4]
                quantidade_minima = linha[5]
                ativo = linha[6]

                # SOMENTE produtos ativos podem gerar alerta
                if (
                    ativo == "S"
                    and quantidade is not None
                    and quantidade_minima is not None
                    and int(quantidade) < int(quantidade_minima)
                ):
                    estoque_baixo = True

                    produtos_estoque_baixo.append(
                        f"{nome} - Qtd: {quantidade} "
                        f"(Mínimo: {quantidade_minima})"
                    )

            else:

                nome = linha[1]
                quantidade = linha[4]
                quantidade_minima = linha[5]

                if (
                    quantidade is not None
                    and quantidade_minima is not None
                    and int(quantidade) < int(quantidade_minima)
                ):
                    estoque_baixo = True
                    
                    produtos_estoque_baixo.append(
                    f"{nome} - Qtd: {quantidade} "
                    f"(Mínimo: {quantidade_minima})"
                )

            # Cria as células
            for col_idx, valor in enumerate(linha):

                if valor is None:
                    texto_celula = "-"

                elif hasattr(valor, "strftime"):
                    texto_celula = valor.strftime("%d/%m/%Y %H:%M:%S")

                else:
                    texto_celula = str(valor)

                # Destaca somente estoque baixo de produto ativo
                if estoque_baixo:
                    cor_fundo = "yellow"
                    cor_texto = "black"
                else:
                    cor_fundo = "transparent"
                    cor_texto = ("black", "white")

                celula = ctk.CTkLabel(
                    self.tabela_frame,
                    text=texto_celula,
                    anchor="w",
                    font=("Arial", 12),
                    fg_color=cor_fundo,
                    text_color=cor_texto
                )

                celula.grid(
                    row=row_idx,
                    column=col_idx,
                    padx=8,
                    pady=6,
                    sticky="ew"
                )

        # Exibe o alerta somente se houver produtos ativos com estoque baixo
        if produtos_estoque_baixo:

            mensagem = (
                "Os seguintes produtos ativos estão abaixo "
                "da quantidade mínima:\n\n"
                + "\n".join(produtos_estoque_baixo)
            )

            messagebox.showwarning(
                "Estoque Baixo",
                mensagem
            )   

    def atualizar_tabela_usuarios(self):
        
        # Essa função é responsável por atualizar a tabela de usuários na interface do sistema de estoque. Ela limpa a tabela existente, consulta o banco de dados para obter os dados dos usuários e exibe os resultados em uma tabela formatada. A função também ajusta os cabeçalhos das colunas e formata os valores das células conforme necessário, incluindo a formatação de números de celular, datas e CPF.
        
        # Limpa a tabela
        for widget in self.tabela_frame_usuario.winfo_children():
            widget.destroy()

        conexao = banco.conectar()
        cursor = conexao.cursor()
        cursor.execute("""SELECT id, nome, celular, data_nascimento,
                    cpf, email, perfil, data_cadastro FROM usuarios""")
        dados = cursor.fetchall()
        conexao.close()

        colunas = [
            "ID", "Nome", "Celular", "Data de Nascimento",
            "CPF", "E-mail", "Perfil", "Data Cadastro"
        ]

        for i in range(len(colunas)):
            peso = 2 if i in [1, 5] else 1
            self.tabela_frame_usuario.grid_columnconfigure(i, weight=peso)

        for col_idx, texto_coluna in enumerate(colunas):
            ctk.CTkLabel(
                self.tabela_frame_usuario,
                text=texto_coluna,
                font=("Arial",14, "bold"),
                text_color="#3a7ebf",
                anchor="w"
            ).grid(row=0, column=col_idx, padx=8, pady=(5, 15), sticky="ew")

        for row_idx, linha in enumerate(dados, start=1):
            for col_idx, valor in enumerate(linha):

                if valor is None:
                    texto_celula = "-"

                # Celular
                elif col_idx == 2:
                    celular = "".join(filter(str.isdigit, str(valor)))

                    if len(celular) == 11:
                        texto_celula = f"({celular[:2]}) {celular[2:7]}-{celular[7:]}"
                    else:
                        texto_celula = str(valor)

                # Datas
                elif col_idx in [3, 8]:
                    if hasattr(valor, "strftime"):
                        texto_celula = valor.strftime("%d/%m/%Y")
                    else:
                        texto_celula = str(valor)

                # CPF
                elif col_idx == 4:
                    cpf = "".join(filter(str.isdigit, str(valor)))

                    if len(cpf) == 11:
                        texto_celula = f"{cpf[:3]}.***.***-{cpf[-2:]}"
                    else:
                        texto_celula = str(valor)
                else:
                    texto_celula = str(valor)

                ctk.CTkLabel(
                    self.tabela_frame_usuario,
                    text=texto_celula,
                    anchor="w",
                    font=("Arial",12)
                ).grid(row=row_idx, column=col_idx, padx=8, pady=6, sticky="ew")
                
    def atualizar_tabela_movimentacoes(self):

        # Essa função é responsável por atualizar a tabela de movimentações na interface do sistema de estoque. Ela limpa a tabela existente, consulta o banco de dados para obter os dados das movimentações e exibe os resultados em uma tabela formatada. A função também ajusta os cabeçalhos das colunas e formata os valores das células conforme necessário, incluindo a formatação de datas e horas.
        
        # Limpa a tabela
        for widget in self.tabela_frame_mov.winfo_children():
            widget.destroy()

        conexao = banco.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT *
            FROM movimentacoes
            ORDER BY data_movimentacao DESC
        """)

        dados = cursor.fetchall()
        conexao.close()

        colunas = [
            "ID Movimentação",
            "ID Produto",
            "Produto",
            "ID Usuário",
            "Usuário",
            "Tipo",
            "Quantidade",
            "Data/Hora"
        ]

        for i in range(len(colunas)):
            peso = 2 if i in [1, 4] else 1
            self.tabela_frame_mov.grid_columnconfigure(i, weight=peso)

        for col_idx, texto_coluna in enumerate(colunas):
            ctk.CTkLabel(
                self.tabela_frame_mov,
                text=texto_coluna,
                font=("Arial",14,"bold"),
                text_color="#3a7ebf",
                anchor="w"
            ).grid(row=0, column=col_idx, padx=8, pady=(5, 15), sticky="ew")

        for row_idx, linha in enumerate(dados, start=1):
            for col_idx, valor in enumerate(linha):

                if valor is None:
                    texto_celula = "-"

                elif hasattr(valor, "strftime"):
                    texto_celula = valor.strftime("%d/%m/%Y %H:%M:%S")

                else:
                    texto_celula = str(valor)

                ctk.CTkLabel(
                    self.tabela_frame_mov,
                    text=texto_celula,
                    anchor="w",
                    font=("Arial",12)
                ).grid(row=row_idx, column=col_idx, padx=8, pady=6, sticky="ew")          

    def atualizar_automatico(self):
        """Atualiza o sistema automaticamente a cada 1 minuto."""

        self.atualizar_tudo()

        self.after_atualizacao = self.after(
            60000,
            self.atualizar_automatico
        )
    
    def parar_atualizacao_automatica(self):

        # Essa função é responsável por interromper a atualização automática do sistema. Ela verifica se há uma atualização agendada (armazenada na variável `after_atualizacao`) e, se houver, cancela essa atualização usando o método `after_cancel`. Em seguida, define a variável `after_atualizacao` como `None`, indicando que não há atualizações automáticas em andamento.
        
        if self.after_atualizacao is not None:

            self.after_cancel(
                self.after_atualizacao
            )

            self.after_atualizacao = None
            
    def construir_tela_entrada_estoque(self):

        # Essa função é responsável por construir a tela de entrada de estoque na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do produto, nome, valor de compra, valor de venda, quantidade, quantidade mínima e quantidade de entrada. Além disso, inclui botões para buscar o produto e salvar a entrada no estoque. A função também chama a função para parar a atualização automática dos dados enquanto a tela de entrada de estoque está aberta.
        
        self.parar_atualizacao_automatica()
        
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
        
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
        
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
        
        ctk.CTkLabel(
            self.aba,
            text="🛒 Entrada Estoque",
            font=("Arial", 22)
        ).pack(pady=20)
        
        # ID
        self.id_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do produto",
            width=300
        )
        self.id_produto.pack(pady=8)
        
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Produto",
            command=self.buscar_produto_estoque
        )
        self.botao_buscar.pack(pady=(0, 20))
        
        self.label_nome = ctk.CTkLabel(
            self.aba,
            text="Nome do Produto",
            font=("Arial", 16)
        )
        self.label_nome.pack(pady=8)
        
        # NOME
        self.nome_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome do produto",
            width=300
        )
        self.nome_produto.pack(pady=8)
        
        self.nome_produto._entry.configure(cursor="no")
        
        self.label_valor_compra = ctk.CTkLabel(
            self.aba,
            text="Valor de Compra",
            font=("Arial", 16)
        )
        self.label_valor_compra.pack(pady=8)
        
        # Valor Compra
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
        
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.valor_compra._entry.configure(cursor="no")
        
        self.label_valor_venda = ctk.CTkLabel(
            self.aba,
            text="Valor de Venda",
            font=("Arial", 16)
        )
        self.label_valor_venda.pack(pady=8)
        
        # Valor Venda
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
        
        
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.valor_venda._entry.configure(cursor="no")
        
        self.label_quantidade = ctk.CTkLabel(
            self.aba,
            text="Quantidade",
            font=("Arial", 16)
        )
        self.label_quantidade.pack(pady=8)

        # Quantidade
        self.quantidade = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantidade.pack(pady=8)
        
        self.quantidade._entry.configure(cursor="no")
        
        self.label_quantidade_minima = ctk.CTkLabel(
            self.aba,
            text="Quantidade Mínima",
            font=("Arial", 16)
        )
        self.label_quantidade_minima.pack(pady=8)

        # Quantidade Mínima
        self.quantidade_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300,
        )
        self.quantidade_minima.pack(pady=8)
        
        self.quantidade_minima._entry.configure(cursor="no")
        
        self.label = ctk.CTkLabel(
            self.aba,
            text="Digite a quantidade que deseja adicionar ao estoque",
            font=("Arial", 16)
        )
        self.label.pack(pady=8)
        
        self.qtd_entrada = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade de Entrada",
            width=300
        )
        self.qtd_entrada.pack(pady=8)
        
        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="Salvar Entrada de Produto",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.entrada_estoque
        )
        self.botao_salvar.pack(pady=25)
        
    def entrada_estoque(self):
        
        # Essa função é responsável por processar a entrada de produtos no estoque. Ela obtém o ID do produto e a quantidade de entrada a partir dos campos de entrada da interface, realiza validações para garantir que os valores sejam válidos (como verificar se o ID e a quantidade foram fornecidos, se a quantidade é um número positivo, etc.), e então chama uma função do módulo "banco" para registrar a entrada no banco de dados. Se a operação for bem-sucedida, exibe uma mensagem de sucesso e limpa os campos de entrada; caso contrário, exibe uma mensagem de erro.
        
        id_produto = self.id_produto.get().strip()
        qtd_entrada = self.qtd_entrada.get().strip()
    
        if not id_produto:
            messagebox.showwarning(
                "Atenção",
                "Digite o ID do produto."
            )
            return
    
        if not qtd_entrada:
            messagebox.showwarning(
                "Atenção",
                "Digite a quantidade de entrada."
            )
            return
    
        if not qtd_entrada.isdigit():
            messagebox.showwarning(
                "Atenção",
                "A quantidade de entrada deve conter apenas números."
            )
            return
        
        if int(qtd_entrada) <= 0:
            messagebox.showwarning(
                "Atenção",
                "A quantidade de entrada deve ser maior que zero."
            )
            return
    
        try:
            banco.entrada_estoque(int(id_produto), int(qtd_entrada))
    
            messagebox.showinfo(
                "Entrada de Estoque",
                f"Entrada de {qtd_entrada} unidades realizada com sucesso!"
            )
    
            # Limpa os campos
            self.id_produto.delete(0, "end")
            self.nome_produto.delete(0, "end")
            self.valor_compra.delete(0, "end")
            self.valor_venda.delete(0, "end")
            self.quantidade.delete(0, "end")
            self.quantidade_minima.delete(0, "end")
            self.qtd_entrada.delete(0, "end")
            
            self.voltar_sistema()
    
        except Exception as erro:
    
            messagebox.showerror(
                "Erro na Entrada de Estoque",
                str(erro)
            )
        
    def buscar_produto_estoque(self):
        
        # Essa função é responsável por buscar informações de um produto no estoque com base no ID fornecido pelo usuário. Ela realiza validações para garantir que o ID seja fornecido e seja um número válido. Em seguida, consulta o banco de dados para obter os detalhes do produto, como nome, valor de compra, valor de venda, quantidade e quantidade mínima. Se o produto estiver inativo, exibe uma mensagem de aviso. Caso contrário, preenche os campos da interface com as informações do produto e bloqueia os campos para edição.
        
        try:
    
            id_produto = self.id_produto.get().strip()
    
            if not id_produto:
                messagebox.showwarning(
                    "Buscar Produto",
                    "Digite o ID do produto."
                )
                return
    
            if not id_produto.isdigit():
                messagebox.showwarning(
                    "Buscar Produto",
                    "O ID deve conter apenas números."
                )
                return
    
            produto = banco.buscar_produto_por_id(
                int(id_produto)
            )
            
            if produto['ativo'] == 'N':
                messagebox.showwarning(
                    "Buscar Produto",
                    "O produto está inativo."
                )
                return
            
            # Desbloqueia os campos para edição, caso haja mais de uma consulta
            self.nome_produto.configure(state="normal")
            self.valor_compra.configure(state="normal")
            self.valor_venda.configure(state="normal")
            self.quantidade.configure(state="normal")
            self.quantidade_minima.configure(state="normal")
    
            # Limpa os campos
            self.nome_produto.delete(0, "end")
            self.valor_compra.delete(0, "end")
            self.valor_venda.delete(0, "end")
            self.quantidade.delete(0, "end")
            self.quantidade_minima.delete(0, "end")
            
            # Nome
            self.nome_produto.insert(0,produto["nome"])
    
            # Valor de Compra
            self.valor_compra.insert(0, produto["valor_compra"])
    
            # Valor de Venda
            self.valor_venda.insert(0, produto["valor_venda"])
    
            # Quantidade
            self.quantidade.insert(0, produto["quantidade"])
    
            # Quantidade Mínima
            self.quantidade_minima.insert(0, produto["quantidade_minima"])
            
            # Bloqueia novamente
            self.nome_produto.configure(state="disabled")
            self.valor_compra.configure(state="disabled")
            self.valor_venda.configure(state="disabled")
            self.quantidade.configure(state="disabled")
            self.quantidade_minima.configure(state="disabled")
    
    
        except Exception as erro:
    
            messagebox.showerror(
                "Buscar Produto",
                str(erro)
            )
            
    def construir_tela_saida_estoque(self):

        # Essa função é responsável por construir a tela de saída de estoque na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do produto, nome, valor de compra, valor de venda, quantidade, quantidade mínima e quantidade de saída. Além disso, inclui botões para buscar o produto e salvar a saída do estoque. A função também chama a função para parar a atualização automática dos dados enquanto a tela de saída de estoque está aberta.
        
        self.parar_atualizacao_automatica()
            
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
            
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
            
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
            
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
            
        ctk.CTkLabel(
            self.aba,
            text="🛒 Saída Estoque",
            font=("Arial", 22)
        ).pack(pady=20)
            
        # ID
        self.id_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do produto",
            width=300
        )
        self.id_produto.pack(pady=8)
            
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Produto",
            command=self.buscar_produto_estoque
        )
        self.botao_buscar.pack(pady=(0, 20))
            
        self.label_nome = ctk.CTkLabel(
            self.aba,
            text="Nome do Produto",
            font=("Arial", 16)
        )
        self.label_nome.pack(pady=8)
            
        # NOME
        self.nome_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome do produto",
            width=300
        )
        self.nome_produto.pack(pady=8)
            
        self.nome_produto._entry.configure(cursor="no")
            
        self.label_valor_compra = ctk.CTkLabel(
            self.aba,
            text="Valor de Compra",
            font=("Arial", 16)
        )
        self.label_valor_compra.pack(pady=8)
            
        # Valor Compra
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
            
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
            
        self.valor_compra._entry.configure(cursor="no")
            
        self.label_valor_venda = ctk.CTkLabel(
            self.aba,
            text="Valor de Venda",
            font=("Arial", 16)
        )
        self.label_valor_venda.pack(pady=8)
            
        # Valor Venda
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
            
            
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
            
        self.valor_venda._entry.configure(cursor="no")
            
        self.label_quantidade = ctk.CTkLabel(
            self.aba,
            text="Quantidade",
            font=("Arial", 16)
        )
        self.label_quantidade.pack(pady=8)

        # Quantidade
        self.quantidade = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantidade.pack(pady=8)
            
        self.quantidade._entry.configure(cursor="no")
            
        self.label_quantidade_minima = ctk.CTkLabel(
            self.aba,
            text="Quantidade Mínima",
            font=("Arial", 16)
        )
        self.label_quantidade_minima.pack(pady=8)

        # Quantidade Mínima
        self.quantidade_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300,
        )
        self.quantidade_minima.pack(pady=8)
            
        self.quantidade_minima._entry.configure(cursor="no")
            
        self.label = ctk.CTkLabel(
            self.aba,
            text="Digite a quantidade que saíra do estoque",
            font=("Arial", 16)
        )
        self.label.pack(pady=8)
            
        self.qtd_entrada = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade de Saída",
            width=300
        )
        self.qtd_entrada.pack(pady=8)
            
        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="Salvar Saída de Produto",
            fg_color="red",
            hover_color="darkred",
            font=("Arial", 20),
            command=self.saida_estoque
        )
        self.botao_salvar.pack(pady=25)
            
    def saida_estoque(self):
        
        # Essa função é responsável por processar a saída de produtos do estoque. Ela obtém o ID do produto e a quantidade de saída a partir dos campos de entrada da interface, realiza validações para garantir que os valores sejam válidos (como verificar se o ID e a quantidade foram fornecidos, se a quantidade é um número positivo, se não excede a quantidade em estoque, etc.), e então chama uma função do módulo "banco" para registrar a saída no banco de dados. Se a operação for bem-sucedida, exibe uma mensagem de sucesso e limpa os campos de entrada; caso contrário, exibe uma mensagem de erro.
        
        id_produto = self.id_produto.get().strip()
        qtd_saida = self.qtd_entrada.get().strip()
    
        if not id_produto:
            messagebox.showwarning(
                "Atenção",
                "Digite o ID do produto."
            )
            return
    
        if not qtd_saida:
            messagebox.showwarning(
                "Atenção",
                "Digite a quantidade de saída."
            )
            return
    
        if not qtd_saida.isdigit():
            messagebox.showwarning(
                "Atenção",
                "A quantidade de saída deve conter apenas números."
            )
            return
        
        if int(qtd_saida) <= 0:
            messagebox.showwarning(
                "Atenção",
                "A quantidade de saída deve ser maior que zero."
            )
            return
        
        if int(qtd_saida) > int(self.quantidade.get()):
            messagebox.showwarning(
                "Atenção",
                "A quantidade de saída não pode ser maior que a quantidade em estoque."
            )
            return
    
        try:
            banco.saida_estoque(int(id_produto), int(qtd_saida))
    
            messagebox.showinfo(
                "Saída de Estoque",
                f"Saída de {qtd_saida} unidades realizada com sucesso!"
            )
    
            # Limpa os campos
            self.id_produto.delete(0, "end")
            self.nome_produto.delete(0, "end")
            self.valor_compra.delete(0, "end")
            self.valor_venda.delete(0, "end")
            self.quantidade.delete(0, "end")
            self.quantidade_minima.delete(0, "end")
            self.qtd_entrada.delete(0, "end")
            
            self.voltar_sistema()
    
        except Exception as erro:
    
            messagebox.showerror(
                "Erro na Saída de Estoque",
                str(erro)
            )
            
    def construir_tela_cadastra_produto(self):
        
        # Essa função é responsável por construir a tela de cadastro de produtos na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o nome do produto, valor de compra, valor de venda e quantidade mínima. Além disso, inclui um botão para cadastrar o produto. A função também chama a função para parar a atualização automática dos dados enquanto a tela de cadastro de produtos está aberta.
        
        self.parar_atualizacao_automatica()
        
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
        
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
        
        # BOTÃO VOLTAR
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
        
        # TÍTULO
        ctk.CTkLabel(
            self.aba,
            text="🛒 Cadastrar Produto",
            font=("Arial", 22)
        ).pack(pady=20)
        
        # NOME
        self.nome_usuario = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome",
            width=300
        )
        self.nome_usuario.pack(pady=8)
        
        # VALOR DE COMPRA
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
        
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        # VALOR DE VENDA
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
        
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        # QUANTIDADE MÍNIMA
        self.qtd_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300
        )
        self.qtd_minima.pack(pady=8)
        
        # BOTÃO CADASTRAR
        self.botao_cadastrar = ctk.CTkButton(
            self.aba,
            text="Cadastrar Produto",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.cadastrar_produto
        )
        self.botao_cadastrar.pack(pady=25)
        
    def cadastrar_produto(self):
        
        # Essa função é responsável por cadastrar um novo produto no sistema de estoque. Ela obtém os valores dos campos de entrada (nome, valor de compra, valor de venda e quantidade mínima), realiza validações para garantir que os campos estejam preenchidos corretamente e solicita a senha do administrador para autorização. Se a senha estiver correta, chama a função do módulo "banco" para cadastrar o produto no banco de dados. Em caso de sucesso, exibe uma mensagem de confirmação e limpa os campos; caso contrário, exibe mensagens de erro apropriadas.
        
        nome = self.nome_usuario.get().strip()
        valor_compra = self.valor_compra.get().strip()
        valor_venda = self.valor_venda.get().strip()
        qtd_minima = self.qtd_minima.get().strip()
    
        # Verifica os campos
        if not nome:
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Nome."
            )
            return
    
        if not valor_compra or valor_compra == "R$ 0,00":
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Valor de Compra.\nDigite um valor maior que zero."
            )
            return
    
        if not valor_venda or valor_venda == "R$ 0,00":
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Valor de Venda.\nDigite um valor maior que zero."
            )
            return

        if not qtd_minima or qtd_minima == "0":
            messagebox.showwarning(
                "Atenção",
                "Preencha o campo Quantidade Mínima.\nDigite um valor maior que zero."
            )
            return

        # Pede a senha do administrador
        dialogo = ctk.CTkInputDialog(
            text="Digite a senha do administrador:",
            title="Autorização"
        )
        senha_admin = dialogo.get_input()
        
        # Se cancelou
        if senha_admin is None:
            return
        
        # Se deixou vazio
        if not senha_admin.strip():
            messagebox.showwarning(
                "Atenção",
                "Digite a senha do administrador."
            )
            return
        
        if str(banco.sessao['senha']) == senha_admin:
        
            try:
        
                banco.cadastrar_produto(
                    nome,
                    float(valor_compra.replace("R$ ", "").replace(".", "").replace(",", ".")),
                    float(valor_venda.replace("R$ ", "").replace(".", "").replace(",", ".")),
                    int(qtd_minima)
                )
        
                messagebox.showinfo(
                    "Sucesso",
                    "Produto cadastrado com sucesso!"
                )
        
                # LIMPA OS CAMPOS
                self.nome_usuario.delete(0, "end")
                self.valor_compra.delete(0, "end")
                self.valor_venda.delete(0, "end")
                self.qtd_minima.delete(0, "end")
        
        
                self.barra_lateral.destroy()
                self.aba.destroy()
        
                self.voltar_sistema()
        
            except Exception as erro:
        
                messagebox.showerror(
                    "Erro",
                    str(erro)
                )
            
        else:
            messagebox.showerror(
                "Erro",
                "Senha Inválida"
            )   
                
    def construir_tela_atualiza_produto(self):
        
        # Essa função é responsável por construir a tela de atualização de produtos na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do produto, nome, valor de compra, valor de venda, quantidade e quantidade mínima. Além disso, inclui botões para buscar o produto e atualizar as informações do produto. A função também chama a função para parar a atualização automática dos dados enquanto a tela de atualização de produtos está aberta.
        
        self.parar_atualizacao_automatica()
        
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
        
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
        
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
        
        ctk.CTkLabel(
            self.aba,
            text="🔄️ Atualizar Produto",
            font=("Arial", 22)
        ).pack(pady=20)
        
        # ID
        self.id_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do produto",
            width=300
        )
        self.id_produto.pack(pady=8)
        
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Produto",
            command=self.buscar_produto
        )
        self.botao_buscar.pack(pady=(0, 20))
        
        self.label_nome = ctk.CTkLabel(
            self.aba,
            text="Nome do Produto",
            font=("Arial", 16)
        )
        self.label_nome.pack(pady=8)
        
        # NOME
        self.nome_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome do produto",
            width=300
        )
        self.nome_produto.pack(pady=8)
        
        self.label_valor_compra = ctk.CTkLabel(
            self.aba,
            text="Valor de Compra",
            font=("Arial", 16)
        )
        self.label_valor_compra.pack(pady=8)
        
        # Valor Compra
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
        
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_valor_venda = ctk.CTkLabel(
            self.aba,
            text="Valor de Venda",
            font=("Arial", 16)
        )
        self.label_valor_venda.pack(pady=8)
        
        # Valor Venda
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
        
        
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_quantidade = ctk.CTkLabel(
            self.aba,
            text="Quantidade",
            font=("Arial", 16)
        )
        self.label_quantidade.pack(pady=8)
        
        # Quantidade
        self.quantidade = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantidade.pack(pady=8)
        
        self.quantidade._entry.configure(cursor="no")
        
        self.label_quantidade_minima = ctk.CTkLabel(
            self.aba,
            text="Quantidade Mínima",
            font=("Arial", 16)
        )
        self.label_quantidade_minima.pack(pady=8)
        
        # Quantidade Mínima
        self.quantidade_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300,
        )
        self.quantidade_minima.pack(pady=8)
        
        
        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="Atualizar Produto",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.atualizar_produto
        )
        self.botao_salvar.pack(pady=25)
    
    def atualizar_produto(self):
        
        # Essa função é responsável por atualizar as informações de um produto no sistema de estoque. Ela obtém o ID do produto e os novos valores dos campos de entrada (nome, valor de compra, valor de venda e quantidade mínima), realiza validações para garantir que o ID seja fornecido e seja um número válido, e solicita a senha do administrador para autorização. Se a senha estiver correta, chama a função do módulo "banco" para atualizar as informações do produto no banco de dados. Em caso de sucesso, exibe uma mensagem de confirmação; caso contrário, exibe mensagens de erro apropriadas.
        
        try:
        
            id_produto = self.id_produto.get().strip()
        
            if not id_produto:
                raise Exception(
                    "Digite o ID do produto."
                )
        
            if not id_produto.isdigit():
                raise Exception(
                    "O ID deve conter apenas números."
                )
        
            # Pede a senha do administrador
            dialogo = ctk.CTkInputDialog(
                text="Digite a senha do administrador:",
                title="Autorização"
            )
            senha_admin = dialogo.get_input()
        
            # Se cancelou
            if senha_admin is None:
                return
        
            # Se deixou vazio
            if not senha_admin.strip():
                messagebox.showwarning(
                    "Atenção",
                    "Digite a senha do administrador."
                )
                return
        
            if str(banco.sessao['senha']) == senha_admin:
        
                banco.atualizar_produto(
                    int(id_produto),
                    self.nome_produto.get(),
                    self.valor_compra.get().strip().replace("R$ ", "").replace(".", "").replace(",", "."),
                    self.valor_venda.get().strip().replace("R$ ", "").replace(".", "").replace(",", "."),
                    self.quantidade_minima.get()
                )
        
                messagebox.showinfo(
                    "Atualizar Produto",
                    "Produto atualizado com sucesso!"
                )
        
                self.voltar_sistema()
        
            else:
                messagebox.showerror(
                    "Erro",
                    "Senha Inválida"
                )
        
        except Exception as erro:
        
            messagebox.showerror(
                "Atualizar Produto",
                str(erro)
            )
    
    def buscar_produto(self):
        
        # Essa função é responsável por buscar informações de um produto no sistema de estoque com base no ID fornecido pelo usuário. Ela realiza validações para garantir que o ID seja fornecido e seja um número válido. Em seguida, consulta o banco de dados para obter os detalhes do produto, como nome, valor de compra, valor de venda, quantidade e quantidade mínima. Se o produto estiver inativo, exibe uma mensagem de aviso. Caso contrário, preenche os campos da interface com as informações do produto.
        
        try:
    
            id_produto = self.id_produto.get().strip()
    
            if not id_produto:
                messagebox.showwarning(
                    "Buscar Produto",
                    "Digite o ID do produto."
                )
                return
    
            if not id_produto.isdigit():
                messagebox.showwarning(
                    "Buscar Produto",
                    "O ID deve conter apenas números."
                )
                return
    
            produto = banco.buscar_produto_por_id(
                int(id_produto)
            )
            
            if produto['ativo'] == 'N':
                messagebox.showwarning(
                    "Buscar Produto",
                    "O produto está inativo."
                )
                return
    
            # Limpa os campos
            self.nome_produto.delete(0, "end")
            self.valor_compra.delete(0, "end")
            self.valor_venda.delete(0, "end")
            self.quantidade.delete(0, "end")
            self.quantidade_minima.delete(0, "end")
    
            # Nome
            self.nome_produto.insert(0,produto["nome"])
    
            # Valor de Compra
            self.valor_compra.insert(0, produto["valor_compra"])
    
            # Valor de Venda
            self.valor_venda.insert(0, produto["valor_venda"])
    
            # Quantidade
            self.quantidade.insert(0, produto["quantidade"])
    
            # Quantidade Mínima
            self.quantidade_minima.insert(0, produto["quantidade_minima"])
            
            self.quantidade.configure(state="disabled")
    
        except Exception as erro:
    
            messagebox.showerror(
                "Buscar Produto",
                str(erro)
            )
            
    def construir_tela_desativar_produto(self):
        
        # Essa função é responsável por construir a tela de desativação de produtos na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do produto, nome, valor de compra, valor de venda, quantidade e quantidade mínima. Além disso, inclui botões para buscar o produto e desativá-lo. A função também chama a função para parar a atualização automática dos dados enquanto a tela de desativação de produtos está aberta.
        
        self.parar_atualizacao_automatica()
        
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
        
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
        
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
        
        ctk.CTkLabel(
            self.aba,
            text="❌ Desativar Produto",
            font=("Arial", 22)
        ).pack(pady=20)
        
        # ID
        self.id_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do produto",
            width=300
        )
        self.id_produto.pack(pady=8)
        
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Produto",
            command=self.buscar_produto_estoque
        )
        self.botao_buscar.pack(pady=(0, 20))
        
        self.label_nome = ctk.CTkLabel(
            self.aba,
            text="Nome do Produto",
            font=("Arial", 16)
        )
        self.label_nome.pack(pady=8)
        
        # NOME
        self.nome_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome do produto",
            width=300
        )
        self.nome_produto.pack(pady=8)
        
        self.nome_produto._entry.configure(cursor="no")
        
        self.label_valor_compra = ctk.CTkLabel(
            self.aba,
            text="Valor de Compra",
            font=("Arial", 16)
        )
        self.label_valor_compra.pack(pady=8)
        
        # Valor Compra
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
        
        self.valor_compra._entry.configure(cursor="no")
        
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_valor_venda = ctk.CTkLabel(
            self.aba,
            text="Valor de Venda",
            font=("Arial", 16)
        )
        self.label_valor_venda.pack(pady=8)
        
        # Valor Venda
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
        
        self.valor_venda._entry.configure(cursor="no")
        
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_quantidade = ctk.CTkLabel(
            self.aba,
            text="Quantidade",
            font=("Arial", 16)
        )
        self.label_quantidade.pack(pady=8)
        
        # Quantidade
        self.quantidade = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantidade.pack(pady=8)
        
        self.quantidade._entry.configure(cursor="no")
        
        self.label_quantidade_minima = ctk.CTkLabel(
            self.aba,
            text="Quantidade Mínima",
            font=("Arial", 16)
        )
        self.label_quantidade_minima.pack(pady=8)
        
        # Quantidade Mínima
        self.quantidade_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300,
        )
        self.quantidade_minima.pack(pady=8)
        
        self.quantidade_minima._entry.configure(cursor="no")
        
        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="❌ Desativar Produto",
            fg_color="red",
            hover_color="darkred",
            font=("Arial", 20),
            command=self.desativar_produto
        )
        self.botao_salvar.pack(pady=25)
        
    def desativar_produto(self):
        
        # Essa função é responsável por desativar um produto no sistema de estoque. Ela obtém o ID do produto a partir do campo de entrada da interface, realiza validações para garantir que o ID seja fornecido e seja um número válido, e solicita a senha do administrador para autorização. Se a senha estiver correta, chama a função do módulo "banco" para desativar o produto no banco de dados. Em caso de sucesso, exibe uma mensagem de confirmação; caso contrário, exibe mensagens de erro apropriadas.
        
        try:
    
            id_produto = self.id_produto.get().strip()
    
            if not id_produto:
                messagebox.showwarning(
                    "Desativar Produto",
                    "Digite o ID do produto."
                )
                return
    
            if not id_produto.isdigit():
                messagebox.showwarning(
                    "Desativar Produto",
                    "O ID deve conter apenas números."
                )
                return
            
            # Pede a senha do administrador
            dialogo = ctk.CTkInputDialog(
                text="Digite a senha do administrador:",
                title="Autorização"
            )
            senha_admin = dialogo.get_input()
            
            # Se cancelou
            if senha_admin is None:
                return
            
            # Se deixou vazio
            if not senha_admin.strip():
                messagebox.showwarning(
                    "Atenção",
                    "Digite a senha do administrador."
                )
                return
            
            if str(banco.sessao['senha']) == senha_admin:
    
                banco.desativar_produto(int(id_produto))
        
                messagebox.showinfo(
                    "Desativar Produto",
                    "Produto desativado com sucesso!"
                )
        
                self.voltar_sistema()
                
            else:
                messagebox.showerror(
                    "Erro",
                    "Senha Inválida"
                )
    
        except Exception as erro:
    
            messagebox.showerror(
                "Desativar Produto",
                str(erro)
            )
    
    def construir_tela_reativar_produto(self):
        
        # Essa função é responsável por construir a tela de reativação de produtos na interface do sistema de estoque. Ela cria a barra lateral e a área principal da tela, adiciona campos de entrada para o ID do produto, nome, valor de compra, valor de venda, quantidade e quantidade mínima. Além disso, inclui botões para buscar o produto e reativá-lo. A função também chama a função para parar a atualização automática dos dados enquanto a tela de reativação de produtos está aberta.
        
        self.parar_atualizacao_automatica()
        
        self.janela_abas.destroy()
        self.barra_lateral.destroy()
        
        self.barra_lateral = ctk.CTkFrame(
            self,
            width=200
        )
        self.barra_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        
        self.aba = ctk.CTkFrame(self)
        self.aba.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
        )
        
        self.botao_voltar = ctk.CTkButton(
            self.barra_lateral,
            text="←",
            font=("Arial", 30),
            fg_color="transparent",
            hover_color="gray",
            text_color=("black", "white"),
            command=self.voltar_sistema
        )
        self.botao_voltar.pack(pady=20)
        
        ctk.CTkLabel(
            self.aba,
            text="✅ Reativar Produto",
            font=("Arial", 22)
        ).pack(pady=20)
        
        # ID
        self.id_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Digite o ID do produto",
            width=300
        )
        self.id_produto.pack(pady=8)
        
        self.botao_buscar = ctk.CTkButton(
            self.aba,
            text="Buscar Produto",
            command=self.buscar_produto_reativar
        )
        self.botao_buscar.pack(pady=(0, 20))
        
        self.label_nome = ctk.CTkLabel(
            self.aba,
            text="Nome do Produto",
            font=("Arial", 16)
        )
        self.label_nome.pack(pady=8)
        
        # NOME
        self.nome_produto = ctk.CTkEntry(
            self.aba,
            placeholder_text="Nome do produto",
            width=300
        )
        self.nome_produto.pack(pady=8)
        
        self.nome_produto._entry.configure(cursor="no")
        
        self.label_valor_compra = ctk.CTkLabel(
            self.aba,
            text="Valor de Compra",
            font=("Arial", 16)
        )
        self.label_valor_compra.pack(pady=8)
        
        # Valor Compra
        self.valor_compra = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Compra",
            width=300
        )
        self.valor_compra.pack(pady=8)
        
        self.valor_compra._entry.configure(cursor="no")
        
        self.valor_compra.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_valor_venda = ctk.CTkLabel(
            self.aba,
            text="Valor de Venda",
            font=("Arial", 16)
        )
        self.label_valor_venda.pack(pady=8)
        
        # Valor Venda
        self.valor_venda = ctk.CTkEntry(
            self.aba,
            placeholder_text="Valor de Venda",
            width=300
        )
        self.valor_venda.pack(pady=8)
        
        self.valor_venda._entry.configure(cursor="no")
        
        self.valor_venda.bind(
            "<KeyRelease>",
            self.formatar_valor
        )
        
        self.label_quantidade = ctk.CTkLabel(
            self.aba,
            text="Quantidade",
            font=("Arial", 16)
        )
        self.label_quantidade.pack(pady=8)
        
        # Quantidade
        self.quantidade = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantidade.pack(pady=8)
        
        self.quantidade._entry.configure(cursor="no")
        
        self.label_quantidade_minima = ctk.CTkLabel(
            self.aba,
            text="Quantidade Mínima",
            font=("Arial", 16)
        )
        self.label_quantidade_minima.pack(pady=8)
        
        # Quantidade Mínima
        self.quantidade_minima = ctk.CTkEntry(
            self.aba,
            placeholder_text="Quantidade Mínima",
            width=300,
        )
        self.quantidade_minima.pack(pady=8)
        
        self.quantidade_minima._entry.configure(cursor="no")
        
        # SALVAR
        self.botao_salvar = ctk.CTkButton(
            self.aba,
            text="✅ Reativar Produto",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 20),
            command=self.reativar_produto
        )
        self.botao_salvar.pack(pady=25)
        
    def reativar_produto(self):
        
        # Essa função é responsável por reativar um produto no sistema de estoque. Ela obtém o ID do produto a partir do campo de entrada da interface, realiza validações para garantir que o ID seja fornecido e seja um número válido, e solicita a senha do administrador para autorização. Se a senha estiver correta, chama a função do módulo "banco" para reativar o produto no banco de dados. Em caso de sucesso, exibe uma mensagem de confirmação; caso contrário, exibe mensagens de erro apropriadas.
        
        try:
        
            id_produto = self.id_produto.get().strip()
        
            if not id_produto:
                messagebox.showwarning(
                    "Reativar Produto",
                    "Digite o ID do produto."
                )
                return
        
            if not id_produto.isdigit():
                messagebox.showwarning(
                    "Reativar Produto",
                    "O ID deve conter apenas números."
                )
                return
        
            # Pede a senha do administrador
            dialogo = ctk.CTkInputDialog(
                text="Digite a senha do administrador:",
                title="Autorização"
            )
            senha_admin = dialogo.get_input()
        
            # Se cancelou
            if senha_admin is None:
                return
        
            # Se deixou vazio
            if not senha_admin.strip():
                messagebox.showwarning(
                    "Atenção",
                    "Digite a senha do administrador."
                )
                return
        
            if str(banco.sessao['senha']) == senha_admin:
        
                banco.reativar_produto(int(id_produto))
        
                messagebox.showinfo(
                    "Reativar Produto",
                    "Produto reativado com sucesso!"
                )
        
                self.voltar_sistema()
        
            else:
                messagebox.showerror(
                    "Erro",
                    "Senha Inválida"
                )
        
        except Exception as erro:
        
            messagebox.showerror(
                "Reativar Produto",
                str(erro)
            )
            
    def buscar_produto_reativar(self):
        
        # Essa função é responsável por buscar informações de um produto inativo no sistema de estoque com base no ID fornecido pelo usuário. Ela realiza validações para garantir que o ID seja fornecido e seja um número válido. Em seguida, consulta o banco de dados para obter os detalhes do produto, como nome, valor de compra, valor de venda, quantidade e quantidade mínima. Se o produto estiver ativo, exibe uma mensagem de aviso. Caso contrário, preenche os campos da interface com as informações do produto.
        
        try:
        
            id_produto = self.id_produto.get().strip()
        
            if not id_produto:
                messagebox.showwarning(
                    "Buscar Produto",
                    "Digite o ID do produto."
                )
                return
        
            if not id_produto.isdigit():
                messagebox.showwarning(
                    "Buscar Produto",
                    "O ID deve conter apenas números."
                )
                return
        
            produto = banco.buscar_produto_por_id(
                int(id_produto)
            )
                
            if produto['ativo'] == 'S':
                messagebox.showwarning(
                    "Buscar Produto",
                    "O produto está ativo."
                )
                return
                
            # Desbloqueia os campos para edição, caso haja mais de uma consulta
            self.nome_produto.configure(state="normal")
            self.valor_compra.configure(state="normal")
            self.valor_venda.configure(state="normal")
            self.quantidade.configure(state="normal")
            self.quantidade_minima.configure(state="normal")
        
            # Limpa os campos
            self.nome_produto.delete(0, "end")
            self.valor_compra.delete(0, "end")
            self.valor_venda.delete(0, "end")
            self.quantidade.delete(0, "end")
            self.quantidade_minima.delete(0, "end")
            
            # Nome
            self.nome_produto.insert(0,produto["nome"])
    
            # Valor de Compra
            self.valor_compra.insert(0, produto["valor_compra"])
    
            # Valor de Venda
            self.valor_venda.insert(0, produto["valor_venda"])
    
            # Quantidade
            self.quantidade.insert(0, produto["quantidade"])
    
            # Quantidade Mínima
            self.quantidade_minima.insert(0, produto["quantidade_minima"])
            
            # Bloqueia novamente
            self.nome_produto.configure(state="disabled")
            self.valor_compra.configure(state="disabled")
            self.valor_venda.configure(state="disabled")
            self.quantidade.configure(state="disabled")
            self.quantidade_minima.configure(state="disabled")
        
        
        except Exception as erro:
        
            messagebox.showerror(
                "Buscar Produto",
                str(erro)
            )
    
    def formatar_valor(self, event):

        # Essa função é responsável por formatar o valor monetário digitado pelo usuário em um campo de entrada da interface do sistema de estoque. Ela captura o evento de digitação, filtra apenas os dígitos numéricos, converte o valor para um formato monetário brasileiro (R$), e atualiza o campo de entrada com o valor formatado. Se o campo estiver vazio, ele é limpo.
        
        entrada = event.widget

        valor = "".join(
            filter(str.isdigit, entrada.get())
        )

        if not valor:
            entrada.delete(0, "end")
            return

        valor = int(valor)

        valor_formatado = valor / 100

        texto = (
            f"R$ {valor_formatado:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        entrada.delete(0, "end")
        entrada.insert(0, texto)

        entrada.icursor("end")