from sqlalchemy.orm import Session
from src.models import Usuario

def create_user(db: Session, *, nome: str, email: str, senha: str,
                peso: float, altura: float, meta_calorica_diaria: int) -> Usuario:
    """
    Cria e persiste um novo usuário no banco.
    """
    novo = Usuario(
        nome=nome,
        email=email,
        senha=senha,
        peso=peso,
        altura=altura,
        meta_calorica_diaria=meta_calorica_diaria
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def get_user_by_email(db: Session, email: str) -> Usuario | None:
    """
    Retorna o usuário com o e-mail informado, ou None.
    """
    return db.query(Usuario).filter(Usuario.email == email).first()

def update_user(db: Session, user: Usuario, **kwargs) -> Usuario:
    """
    Atualiza campos do usuário de forma dinâmica.
    Exemplo: update_user(db, usuario, peso=80, meta_calorica_diaria=2800)
    """
    for field, value in kwargs.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: Usuario) -> None:
    """
    Remove o usuário do banco.
    """
    db.delete(user)
    db.commit()
