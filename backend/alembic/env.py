

# Generic single-database configuration.

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys

# Ajoute le dossier backend/ (parent de alembic/) au path Python,
# pour que "app" soit importable peu importe le répertoire de travail
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




# ====== Ajout : connecter Alembic à nos modèles et à notre config ======
from app.database import Base
from app.core.config import settings
import app.models  # importe tous les modèles pour qu'ils soient enregistrés dans Base.metadata

# Alembic Config object, which provides
# the values of the [alembic] section
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ====== Modifié : Alembic connaît maintenant nos 4 modèles ======
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    # ====== Modifié : on lit l'URL depuis .env au lieu d'une valeur codée en dur ======
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()