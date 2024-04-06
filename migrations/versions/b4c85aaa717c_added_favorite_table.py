"""Added favorite table

Revision ID: b4c85aaa717c
Revises: 82df071a5667
Create Date: 2024-04-03 21:59:21.674650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c85aaa717c'
down_revision = '82df071a5667'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('plant_name', sa.String(length=255), nullable=False),
    sa.Column('plant_common_name', sa.String(length=255), nullable=True),
    sa.Column('plant_scientific_name', sa.String(length=255), nullable=True),
    sa.Column('plant_image_url', sa.String(length=255), nullable=True),
    sa.Column('plant_description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite')
    # ### end Alembic commands ###