# C:\Projetos\dieta-calorias\alembic\env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config # Certifique-se que está importado
from sqlalchemy import pool # Certifique-se que está importado
from sqlalchemy import MetaData # Importe MetaData se for usá-lo diretamente

from alembic import context

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models import Base # Sua Base dos modelos

print("--- DEBUG env.py: Início da execução de env.py ---")
try:
    print(f"DEBUG env.py: Base.metadata.tables ANTES da atribuição: {list(Base.metadata.tables.keys()) if Base and Base.metadata else 'Base ou Base.metadata é None'}")
except Exception as e:
    print(f"DEBUG env.py: Erro (antes): {e}")

config = context.config # Alembic Config object

# Se a URL não estiver no config vinda do alembic.ini, pegue do seu database.py
# Isso garante que o contexto online tenha uma URL.
if not config.get_main_option("sqlalchemy.url"):
    from src.database import DATABASE_URL
    print(f"DEBUG env.py: Definindo sqlalchemy.url no config para: {DATABASE_URL}")
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Configure target_metadata com a Base dos seus modelos
# Este é o ponto crucial para o autogenerate
target_metadata = Base.metadata

try:
    print(f"DEBUG env.py: target_metadata.tables DEPOIS da atribuição: {list(target_metadata.tables.keys()) if target_metadata else 'target_metadata é None'}")
    if target_metadata:
        for table_name, table_obj in target_metadata.tables.items():
            print(f"  DEBUG env.py: Tabela '{table_name}': Colunas: {[c.name for c in table_obj.columns]}")
except Exception as e:
    print(f"DEBUG env.py: Erro (depois): {e}")
print("--- DEBUG env.py: Fim dos prints, antes de run_migrations_offline/online ---")

def run_migrations_offline() -> None:
    # ... (código padrão, certifique-se que usa 'target_metadata') ...
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata, # Importante
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # ... (código padrão, certifique-se que usa 'target_metadata') ...
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata # Importante
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()