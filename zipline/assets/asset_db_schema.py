import sqlalchemy as sa


# Define a version number for the database generated by these writers
# Increment this version number any time a change is made to the schema of the
# assets database
# NOTE: When upgrading this remember to add a downgrade in:
# .asset_db_migrations
ASSET_DB_VERSION = 6

# A frozenset of the names of all tables in the assets db
# NOTE: When modifying this schema, update the ASSET_DB_VERSION value
asset_db_table_names = frozenset({
    'asset_router',
    'equities',
    'equity_symbol_mappings',
    'futures_contracts',
    'futures_exchanges',
    'futures_root_symbols',
    'options_contracts',
    'options_exchanges',
    'version_info',
})

metadata = sa.MetaData()

equities = sa.Table(
    'equities',
    metadata,
    sa.Column(
        'sid',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('asset_name', sa.Text),
    sa.Column('start_date', sa.Integer, default=0, nullable=False),
    sa.Column('end_date', sa.Integer, nullable=False),
    sa.Column('first_traded', sa.Integer),
    sa.Column('auto_close_date', sa.Integer),
    sa.Column('exchange', sa.Text),
    sa.Column('exchange_full', sa.Text)
)

equity_symbol_mappings = sa.Table(
    'equity_symbol_mappings',
    metadata,
    sa.Column(
        'id',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column(
        'sid',
        sa.Integer,
        sa.ForeignKey(equities.c.sid),
        nullable=False,
        index=True,
    ),
    sa.Column(
        'symbol',
        sa.Text,
        nullable=False,
    ),
    sa.Column(
        'company_symbol',
        sa.Text,
        index=True,
    ),
    sa.Column(
        'share_class_symbol',
        sa.Text,
    ),
    sa.Column(
        'start_date',
        sa.Integer,
        nullable=False,
    ),
    sa.Column(
        'end_date',
        sa.Integer,
        nullable=False,
    ),
)

futures_exchanges = sa.Table(
    'futures_exchanges',
    metadata,
    sa.Column(
        'exchange',
        sa.Text,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('timezone', sa.Text),
)

futures_root_symbols = sa.Table(
    'futures_root_symbols',
    metadata,
    sa.Column(
        'root_symbol',
        sa.Text,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('root_symbol_id', sa.Integer),
    sa.Column('sector', sa.Text),
    sa.Column('description', sa.Text),
    sa.Column(
        'exchange',
        sa.Text,
        sa.ForeignKey('futures_exchanges.exchange'),
    ),
)

futures_contracts = sa.Table(
    'futures_contracts',
    metadata,
    sa.Column(
        'sid',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('symbol', sa.Text, unique=True, index=True),
    sa.Column(
        'root_symbol',
        sa.Text,
        sa.ForeignKey('futures_root_symbols.root_symbol'),
        index=True
    ),
    sa.Column('asset_name', sa.Text),
    sa.Column('start_date', sa.Integer, default=0, nullable=False),
    sa.Column('end_date', sa.Integer, nullable=False),
    sa.Column('first_traded', sa.Integer),
    sa.Column(
        'exchange',
        sa.Text,
        sa.ForeignKey('futures_exchanges.exchange'),
    ),
    sa.Column('notice_date', sa.Integer, nullable=False),
    sa.Column('expiration_date', sa.Integer, nullable=False),
    sa.Column('auto_close_date', sa.Integer, nullable=False),
    sa.Column('multiplier', sa.Float),
    sa.Column('tick_size', sa.Float),
)

options_exchanges = sa.Table(
    'options_exchanges',
    metadata,
    sa.Column(
        'exchange',
        sa.Text,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('timezone', sa.Text),
)

options_root_symbols = sa.Table(
    'options_root_symbols',
    metadata,
    sa.Column(
        'root_symbol',
        sa.Text,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('root_symbol_id', sa.Integer),
    sa.Column('sector', sa.Text),
    sa.Column('description', sa.Text),
    sa.Column(
        'exchange',
        sa.Text,
        sa.ForeignKey('options_exchanges.exchange'),
    ),
)

options_contracts = sa.Table(
    'options_contracts',
    metadata,
    sa.Column(
        'sid',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column('symbol', sa.Text, unique=True, index=True),
    sa.Column(
        'root_symbol',
        sa.Text,
        sa.ForeignKey('options_root_symbols.root_symbol'),
        index=True
    ),
    sa.Column('asset_name', sa.Text),
    sa.Column('start_date', sa.Integer, default=0, nullable=False),
    sa.Column('end_date', sa.Integer, nullable=False),
    sa.Column('first_traded', sa.Integer),
    sa.Column(
        'exchange',
        sa.Text,
        sa.ForeignKey('options_exchanges.exchange'),
    ),
    sa.Column('notice_date', sa.Integer, nullable=False),
    sa.Column('expiration_date', sa.Integer, nullable=False),
    sa.Column('auto_close_date', sa.Integer, nullable=False),
    sa.Column('multiplier', sa.Float),
    sa.Column('strike', sa.Float),
    sa.Column('option_type', sa.Text),
    sa.Column('delta', sa.Float),
    sa.Column('gamma', sa.Float),
    sa.Column('theta', sa.Float),
    sa.Column('vega', sa.Float),
    sa.Column('open_interest', sa.Float),
    sa.Column('volume', sa.Integer),
    sa.Column('tick_size', sa.Integer),
)

asset_router = sa.Table(
    'asset_router',
    metadata,
    sa.Column(
        'sid',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True),
    sa.Column('asset_type', sa.Text),
)

version_info = sa.Table(
    'version_info',
    metadata,
    sa.Column(
        'id',
        sa.Integer,
        unique=True,
        nullable=False,
        primary_key=True,
    ),
    sa.Column(
        'version',
        sa.Integer,
        unique=True,
        nullable=False,
    ),
    # This constraint ensures a single entry in this table
    sa.CheckConstraint('id <= 1'),
)
