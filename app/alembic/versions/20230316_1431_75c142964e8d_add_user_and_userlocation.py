"""add user and userlocation

Revision ID: 75c142964e8d
Revises: 
Create Date: 2023-03-16 14:31:51.177038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75c142964e8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userlocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('street_number', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('postcode', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('nationality', sa.String(length=50), nullable=True),
    sa.Column('cell', sa.String(length=50), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['userlocations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('userlocations')
    # ### end Alembic commands ###
