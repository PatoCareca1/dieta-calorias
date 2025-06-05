from sqlalchemy.orm import Session
from passlib.context import CryptContext # Para hashing de senha

from src import models
from src.api import schemas # Importar nossos schemas Pydantic

# Configuração do Passlib para hashing de senha
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    """
    Retorna um usuário pelo ID.
    """
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    """
    Retorna o usuário com o e-mail informado, ou None.
    """
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[models.Usuario]:
    """
    Retorna uma lista de usuários com paginação.
    """
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """
    Cria e persiste um novo usuário no banco, incluindo os novos campos de perfil.
    """
    hashed_password = get_hashed_password(usuario.senha)
    
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        hashed_password=hashed_password, # Salvar a senha hasheada
        is_active=usuario.is_active if usuario.is_active is not None else True, # Default se não fornecido
        
        peso_kg=usuario.peso_kg,
        altura_cm=usuario.altura_cm,
        data_nascimento=usuario.data_nascimento,
        genero=usuario.genero,
        nivel_atividade=usuario.nivel_atividade,
        objetivo=usuario.objetivo,
        restricoes_alimentares=usuario.restricoes_alimentares,
        observacoes=usuario.observacoes
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, db_user: models.Usuario, user_update: schemas.UsuarioUpdate) -> models.Usuario:
    """
    Atualiza campos do usuário de forma dinâmica, incluindo os novos campos de perfil.
    Apenas os campos presentes em user_update (e que não são None) serão atualizados.
    """
    update_data = user_update.dict(exclude_unset=True) # Pega apenas os campos que foram enviados

    for field, value in update_data.items():
        if field == "senha": # Se a senha está sendo atualizada, precisa hashear
            if value: # Garante que a senha não é uma string vazia para atualizar
                setattr(db_user, "hashed_password", get_hashed_password(value))
        else:
            setattr(db_user, field, value)
            
    db.add(db_user) # Adiciona o objeto à sessão para que o SQLAlchemy rastreie as mudanças
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    """
    Remove um usuário do banco pelo ID.
    Retorna o usuário deletado ou None se não encontrado.
    """
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# def authenticate_user(db: Session, email: str, password: str) -> models.Usuario | None:
#     user = get_usuario_by_email(db, email=email)
#     if not user:
#         return None
#     if not verify_password(password, user.hashed_password):
#         return None
#     return user

