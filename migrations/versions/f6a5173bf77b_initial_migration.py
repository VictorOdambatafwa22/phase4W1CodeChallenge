"""Initial migration

Revision ID: f6a5173bf77b
Revises: 
Create Date: 2023-09-24 04:21:28.249619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6a5173bf77b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Pizza',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('super_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Restaurant_pizzas',
    sa.Column('Restaurant_id', sa.Integer(), nullable=False),
    sa.Column('Pizza_id', sa.Integer(), nullable=False),
    sa.Column('Price', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Pizza_id'], ['Pizza.id'], ),
    sa.ForeignKeyConstraint(['Restaurant_id'], ['Restaurant.id'], ),
    sa.PrimaryKeyConstraint('Restaurant_id', 'Pizza_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Restaurant_pizzas')
    op.drop_table('Restaurant')
    op.drop_table('Pizza')
    # ### end Alembic commands ###
