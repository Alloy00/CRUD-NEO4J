import os
from neo4j import GraphDatabase, basic_auth

def create(tx, nome, idade, id):
    tx.run("CREATE (:Usuario {nome: $nome, idade: $idade, id: $id})", nome=nome, idade=idade, id=id) 

def criar_user(session):
    nome = input("Nome do Usuário: ")
    idade = input("Idade do Usuário: ")
    id = input("ID do Usuário: ")
    session.write_transaction(create, nome, idade, id)
    print("Usuário criado com sucesso")

def read(tx, id):
    result = tx.run("MATCH (u:Usuario {id: $id}) RETURN u", id=id)
    return result.single()

def read_user(session):
    id = input("Digite o ID do usuário que está buscando: ")
    result = session.read_transaction(read, id)
    print(result["u"])

def update(tx, id, nome, idade):
    tx.run("MATCH (u:Usuario {id: $id}) SET u.nome = $nome, u.idade = $idade", id=id, nome=nome, idade=idade)

def update_user(session):
    id = input("Digite o ID do usuário que deseja atualizar: ")
    nome = input("Digite o novo nome: ")
    idade = input("Digite a nova idade: ")
    session.write_transaction(update, id, nome, idade)
    print("Usuário atualizado com sucesso")

def delete(tx, id):
    tx.run("MATCH (u:Usuario {id: $id}) DELETE u", id=id)

def delete_user(session):
    id = input("Digite o ID do usuário que deseja excluir: ")
    session.write_transaction(delete, id)
    print("Usuário excluído com sucesso")

def read_all(tx):
    result = tx.run("MATCH (u:Usuario) RETURN u")
    records = [{"nome": record["u"]["nome"], "idade": record["u"]["idade"], "id": record["u"]["id"]} for record in result]
    return records

def read_all_users(session):
    result = session.read_transaction(read_all)
    for record in result:
        print("Nome:", record["nome"])
        print("Idade:", record["idade"])
        print("ID:", record["id"])

def opcao_invalida():
    print("Opção inválida. Por favor, escolha uma opção válida.")

def menu(session, opcao):
    opcoes = {
        1: criar_user, 
        2: read_user, 
        3: update_user, 
        4: delete_user,
        5: read_all_users 
    }

    funcao = opcoes.get(opcao, opcao_invalida)
    funcao(session)

def main():
    driver = GraphDatabase.driver(
        "bolt://54.91.205.9:7687",
        auth=basic_auth("neo4j", "sum-sample-atom"))

    #Conexão com banco local
    '''driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=basic_auth("user", "senha"))'''

    with driver.session(database="neo4j") as session:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-- CRUD Neo4j --:")
            print("1. Criar Usuário")
            print("2. Ler Usuário")
            print("3. Atualizar Usuário")
            print("4. Excluir Usuário")
            print("5. Exibir Todos Os Usuários")
            print("0. Sair")
            try:
                escolha = int(input("Digite o número da opção desejada: "))
                if escolha == 0:
                    print("Saindo do programa...")
                    break
                menu(session, escolha)
                input("Pressione Enter para voltar ao menu...")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")

if __name__ == "__main__":
    main()
