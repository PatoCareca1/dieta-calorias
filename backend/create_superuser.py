import argparse
from sqlalchemy.orm import Session
from getpass import getpass

# Importamos os componentes necessários do nosso projeto
from src.database import SessionLocal
from src.crud import usuario as crud_usuario
from src.api.schemas import UsuarioCreate

def create_superuser(db: Session, email: str, senha: str):
    """
    Cria um superusuário no banco de dados.
    """
    # 1. Verifica se o usuário já existe
    db_user = crud_usuario.get_usuario_by_email(db, email=email)
    if db_user:
        print(f"Erro: O usuário com o e-mail '{email}' já existe.")
        # Se já existir e não for admin, pergunta se quer torná-lo admin
        if not db_user.is_admin:
            choice = input("Deseja tornar este usuário um administrador? (s/n): ").lower()
            if choice == 's':
                db_user.is_admin = True
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                print(f"Sucesso: O usuário '{email}' agora é um administrador.")
            else:
                print("Operação cancelada.")
        else:
            print("Este usuário já é um administrador.")
        return

    # 2. Se não existir, cria um novo usuário
    print(f"Criando novo superusuário com e-mail: {email}")
    
    # Prepara os dados do usuário para criação
    # Note que o nome é opcional, pode ser preenchido depois no perfil
    usuario_in = UsuarioCreate(
        email=email,
        nome=email.split('@')[0], # Usa a parte local do e-mail como nome padrão
        senha=senha,
        is_admin=True # AQUI ESTÁ A MÁGICA!
    )
    
    # 3. Usa a função CRUD existente para criar o usuário
    user = crud_usuario.create_usuario(db=db, usuario=usuario_in)
    
    print(f"Sucesso: Superusuário '{user.email}' criado.")


if __name__ == "__main__":
    # Esta parte permite que executemos o script com argumentos no terminal
    parser = argparse.ArgumentParser(description="Cria um superusuário para a aplicação FitTrack.")
    parser.add_argument("--email", type=str, required=True, help="E-mail do novo superusuário.")
    args = parser.parse_args()

    # Pede a senha de forma segura, sem exibi-la no terminal
    password = getpass("Digite a senha para o superusuário: ")
    if len(password) < 8:
        print("Erro: A senha precisa ter no mínimo 8 caracteres.")
    else:
        # Cria uma sessão de banco de dados e executa a função principal
        db = SessionLocal()
        try:
            create_superuser(db=db, email=args.email, senha=password)
        finally:
            db.close()