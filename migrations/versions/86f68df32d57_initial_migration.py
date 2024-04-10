"""Initial migration.

Revision ID: 86f68df32d57
Revises: 5e83146b2887
Create Date: 2024-04-09 16:16:43.167488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f68df32d57'
down_revision = '5e83146b2887'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plant_name', sa.String(length=100), nullable=False),
    sa.Column('scientific_name', sa.String(length=100), nullable=False),
    sa.Column('guide_type', sa.String(length=100), nullable=False),
    sa.Column('guide_description', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookmark')
    # ### end Alembic commands ###
