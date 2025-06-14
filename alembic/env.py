# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adiciona o diretório raiz do projeto ao sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importar Base dos seus modelos
from src.models import Base # Certifique-se que seus modelos completos estão aqui

config = context.config # Objeto de configuração do Alembic

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir target_metadata para o autogenerate e para o contexto
target_metadata = Base.metadata
print(f"DEBUG env.py: target_metadata tabelas: {list(target_metadata.tables.keys() if target_metadata else 'None')}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    print("DEBUG env.py: Executando run_migrations_offline")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
    print("DEBUG env.py: run_migrations_offline concluído")

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    print("DEBUG env.py: Executando run_migrations_online")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        print("DEBUG env.py: Conectado ao banco. Configurando contexto com transactional_ddl=False.")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transactional_ddl=False # Chave aqui!
        )
        print("DEBUG env.py: Contexto configurado. Iniciando run_migrations.")
        with context.begin_transaction(): # Mantemos para a tabela alembic_version
            context.run_migrations()
        print("DEBUG env.py: run_migrations concluído.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

print("DEBUG env.py: Fim do env.py")
    