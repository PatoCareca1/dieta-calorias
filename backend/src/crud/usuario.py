# src/crud/usuario.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src import models
from src.api import schemas

# Configuração do Passlib (usando Argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    """Retorna o hash de uma senha."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

# --- FUNÇÃO DE AUTENTICAÇÃO ---
def authenticate_user(db: Session, email: str, password: str) -> models.Usuario | None:
    """
    Autentica um usuário. Retorna o usuário se a autenticação for bem-sucedida,
    caso contrário, retorna None.
    """
    user = get_usuario_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    """Retorna um usuário pelo ID."""
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    """Retorna o usuário com o e-mail informado, ou None."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[models.Usuario]:
    """Retorna uma lista de usuários com paginação."""
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """Cria e persiste um novo usuário no banco."""
    hashed_password = get_hashed_password(usuario.senha)
    
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        hashed_password=hashed_password,
        is_active=usuario.is_active,
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
    """Atualiza campos do usuário de forma dinâmica."""
    update_data = user_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        if field == "senha":
            if value:
                setattr(db_user, "hashed_password", get_hashed_password(value))
        else:
            setattr(db_user, field, value)
            
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    """Remove um usuário do banco pelo ID."""
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
