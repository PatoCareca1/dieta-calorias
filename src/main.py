from database import engine, Base
import models 

def create_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db()
    print("Banco de dados criado com sucesso!")
