import os
from difflib import get_close_matches

from colorama import init, Fore

init(autoreset=True)

#Base de dados
reciclagem = {
    "garrafa_pet": ("Plástico", "Limpe a garrafa e descarte no local correto!"),
    "jornal": ("Papel", "Descarte no local correto!"),
    "casca_de_banana": ("Orgânico", "Descarte no local correto!"),
    "lata_de_refrigerante": ("Metal", "Descarte no local correto!"),
    "garrafa_de_vidro": ("Vidro", "Guarde em um recipiente fechado e descarte no local correto!"),
    "saco_plastico": ("Plástico", "Descarte no local correto!"),
    "caixa_de_papelão": ("Papel", "Descarte no local correto!"),
    "pilha": ("Perigoso", "Leve até um ponto de coleta especializado!"),
    "óleo": ("Perigoso", "Não jogue no ralo, leve até ponto de coleta!"),
}

usuarios = {}
#Funções de usuários
def carregar_usuarios():
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            for linha in f:
                nome, senha = linha.strip().split(";")
                usuarios[nome] = senha


def salvar_usuarios():
    with open("usuarios.txt", "w", encoding="utf-8") as f:
        for u, s in usuarios.items():
            f.write(f"{u};{s}\n")


def cadastrar_usuario():
    nome = input("Digite o nome do usuário: ").lower()
    if nome in usuarios:
        print(Fore.RED + "❌ Usuário já existe!")
        return None
    senha = input("Digite a senha: ")
    usuarios[nome] = senha
    salvar_usuarios()
    print(Fore.GREEN + "✅ Usuário cadastrado!")
    return nome


def login_usuario():
    nome = input("Digite seu usuário: ").lower()
    senha = input("Digite sua senha: ")
    if nome in usuarios and usuarios[nome] == senha:
        print(Fore.GREEN + f"✅ Bem-vindo, {nome}!")
        return nome
    else:
        print(Fore.RED + "❌ Usuário ou senha incorretos.")
        return None


def alterar_senha(usuario_atual):
    senha_atual = input("Digite sua senha atual: ")
    if usuarios[usuario_atual] != senha_atual:
        print(Fore.RED + "❌ Senha incorreta!")
        return
    nova_senha = input("Digite a nova senha: ")
    usuarios[usuario_atual] = nova_senha
    salvar_usuarios()
    print(Fore.GREEN + "✅ Senha alterada com sucesso!")


#Funções do histórico
def carregar_historico(usuario):
    arquivo = f"historico_{usuario}.txt"
    historico = []
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                objeto, categoria = linha.strip().split(";")
                historico.append((objeto, categoria))
    return historico


def salvar_historico(usuario, historico):
    arquivo = f"historico_{usuario}.txt"
    with open(arquivo, "w", encoding="utf-8") as f:
        for objeto, categoria in historico:
            f.write(f"{objeto};{categoria}\n")


# Funcionalidades principais
def reciclar_objeto(historico, usuario_atual):
    objeto = input(Fore.BLUE + "Digite o objeto que deseja reciclar: ").lower()

    if objeto in reciclagem:
        categoria, dica = reciclagem[objeto]
        print(Fore.GREEN + f"\n✅ Categoria: {categoria}")
        print(Fore.BLUE + f"💡 Dica: {dica}")
        historico.append((objeto, categoria))
        salvar_historico(usuario_atual, historico)

    else:
        # Buscar até 3sugestões
        sugestoes = get_close_matches(objeto, reciclagem.keys(), n=3, cutoff=0.6)

        if sugestoes:
            print(Fore.MAGENTA + "\n❓ Objeto não encontrado. Sugestões próximas:")
            for i, s in enumerate(sugestoes, 1):
                cat, dica = reciclagem[s]
                print(Fore.BLUE + f"{i}. {s} - Categoria: {cat}, Dica: {dica}")

            while True:
                escolha = input(
                    Fore.MAGENTA + "Digite o número da sugestão para confirmar ou 'n' para cancelar: ").lower()

                if escolha == 'n':
                    print(Fore.RED + "❌ Operação cancelada.")
                    break
                elif escolha.isdigit() and 1 <= int(escolha) <= len(sugestoes):
                    escolhido = sugestoes[int(escolha) - 1]
                    categoria, _ = reciclagem[escolhido]
                    historico.append((escolhido, categoria))
                    salvar_historico(usuario_atual, historico)
                    print(Fore.GREEN + f"✅ '{escolhido}' adicionado ao histórico!")
                    break
                else:
                    print(Fore.RED + "❌ Entrada inválida. Digite um número válido ou 'n' para cancelar.")

        else:
            print(Fore.RED + "❌ Objeto não encontrado na base de dados e nenhuma sugestão disponível.")


def cadastrar_objeto():
    nome_objeto = input("Digite o nome do objeto: ").lower()
    categoria = input("Digite a categoria do objeto: ")
    dica = input("Digite a dica de descarte: ")
    reciclagem[nome_objeto] = (categoria, dica)
    print(Fore.GREEN + f"\n✅ Objeto '{nome_objeto}' cadastrado com sucesso!\n")


def ver_historico(historico):
    print(Fore.BLUE + "\n📜 HISTÓRICO DE RECICLAGEM")
    if historico:
        for item, categoria in historico:
            print(Fore.BLUE + f"- {item.title()} ({categoria})")
    else:
        print(Fore.RED + "Nenhum item registrado ainda.")


def ver_estatisticas(historico):
    print(Fore.BLUE + "\n📊 ESTATÍSTICAS")
    if historico:
        estatistica = {}
        for _, categoria in historico:
            estatistica[categoria] = estatistica.get(categoria, 0) + 1
        total = sum(estatistica.values())
        for cat, cont in estatistica.items():
            print(Fore.BLUE + f"{cat}: {cont} itens ({cont / total * 100:.1f}%)")
    else:
        print(Fore.RED + "Nenhum dado disponível ainda.")


def trocar_usuario():
    usuario = None
    while not usuario:
        escolha_login = input(Fore.MAGENTA + "Digite 'login' ou 'cadastro': ").lower()
        if escolha_login == "login":
            usuario = login_usuario()
        elif escolha_login == "cadastro":
            usuario = cadastrar_usuario()
    return usuario


#Menu
def menu(usuario_atual, historico):
    while True:
        print(Fore.MAGENTA + "\n♻️ UM MUNDO MELHOR, VAMOS RECICLAR!!!")
        print(Fore.GREEN + "1 - Reciclar um objeto")
        print(Fore.GREEN + "2 - Cadastrar novo objeto")
        print(Fore.GREEN + "3 - Ver histórico")
        print(Fore.GREEN + "4 - Ver estatísticas")
        print(Fore.GREEN + "5 - Alterar senha")
        print(Fore.GREEN + "6 - Trocar usuário")
        print(Fore.GREEN + "7 - Sair")

        escolha = input(Fore.MAGENTA + "Digite o número da opção: ").strip()

        if escolha == "1":
            reciclar_objeto(historico, usuario_atual)
        elif escolha == "2":
            cadastrar_objeto()
        elif escolha == "3":
            ver_historico(historico)
        elif escolha == "4":
            ver_estatisticas(historico)
        elif escolha == "5":
            alterar_senha(usuario_atual)
        elif escolha == "6":
            usuario_atual = trocar_usuario()
            historico = carregar_historico(usuario_atual)
        elif escolha == "7":
            print(Fore.GREEN + "👋 Obrigado por usar o programa!")
            break
        else:
            print(Fore.RED + "❌ Opção inválida, digite de 1 a 7.")


#Programa principal
if __name__ == "__main__":
    carregar_usuarios()
    usuario_atual = trocar_usuario()
    historico = carregar_historico(usuario_atual)
    menu(usuario_atual, historico)
