from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
human = Table('human', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('fisrtname', VARCHAR(length=64)),
    Column('middlename', VARCHAR(length=64)),
    Column('surname', VARCHAR(length=64)),
)

human = Table('human', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstname', String(length=64)),
    Column('middlename', String(length=64)),
    Column('surname', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['human'].columns['fisrtname'].drop()
    post_meta.tables['human'].columns['firstname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['human'].columns['fisrtname'].create()
    post_meta.tables['human'].columns['firstname'].drop()
