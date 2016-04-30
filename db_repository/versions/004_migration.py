from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
)

human = Table('human', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('fisrtname', VARCHAR(length=64)),
    Column('middlename', VARCHAR(length=64)),
    Column('surname', VARCHAR(length=64)),
    Column('birthdate', VARCHAR(length=64)),
    Column('TIN', VARCHAR(length=64)),
    Column('phone', VARCHAR(length=64)),
    Column('address', VARCHAR(length=64)),
    Column('country', VARCHAR(length=64)),
    Column('city', VARCHAR(length=64)),
    Column('diploma', INTEGER),
    Column('last_medical_exam', VARCHAR(length=64)),
    Column('insurance_num', VARCHAR(length=64)),
    Column('insurance_expires', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    pre_meta.tables['user'].drop()
    pre_meta.tables['human'].columns['TIN'].drop()
    pre_meta.tables['human'].columns['address'].drop()
    pre_meta.tables['human'].columns['birthdate'].drop()
    pre_meta.tables['human'].columns['city'].drop()
    pre_meta.tables['human'].columns['country'].drop()
    pre_meta.tables['human'].columns['diploma'].drop()
    pre_meta.tables['human'].columns['insurance_expires'].drop()
    pre_meta.tables['human'].columns['insurance_num'].drop()
    pre_meta.tables['human'].columns['last_medical_exam'].drop()
    pre_meta.tables['human'].columns['phone'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    pre_meta.tables['user'].create()
    pre_meta.tables['human'].columns['TIN'].create()
    pre_meta.tables['human'].columns['address'].create()
    pre_meta.tables['human'].columns['birthdate'].create()
    pre_meta.tables['human'].columns['city'].create()
    pre_meta.tables['human'].columns['country'].create()
    pre_meta.tables['human'].columns['diploma'].create()
    pre_meta.tables['human'].columns['insurance_expires'].create()
    pre_meta.tables['human'].columns['insurance_num'].create()
    pre_meta.tables['human'].columns['last_medical_exam'].create()
    pre_meta.tables['human'].columns['phone'].create()
