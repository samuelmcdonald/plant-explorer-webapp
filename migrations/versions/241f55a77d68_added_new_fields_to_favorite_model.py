"""Added new fields to Favorite model

Revision ID: 241f55a77d68
Revises: 7c1d15a62f7e
Create Date: 2024-04-04 15:35:05.907187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '241f55a77d68'
down_revision = '7c1d15a62f7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('duration', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('edible', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('vegetable', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('edible_parts', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('synonyms', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_column('synonyms')
        batch_op.drop_column('edible_parts')
        batch_op.drop_column('vegetable')
        batch_op.drop_column('edible')
        batch_op.drop_column('duration')

    # ### end Alembic commands ###
