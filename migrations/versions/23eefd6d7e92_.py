"""empty message

Revision ID: 23eefd6d7e92
Revises: 
Create Date: 2018-07-07 05:16:50.432266

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '23eefd6d7e92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instagram_queuer',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.Text(), nullable=True),
                    sa.Column('image_url', sa.Text(), nullable=False),
                    sa.Column('date_queued', sa.DateTime(), nullable=True),
                    sa.Column('date_posted', sa.DateTime(), nullable=True),
                    sa.Column('user_email', sa.Text(), nullable=False),
                    sa.Column('status', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('instagram_queuer')
    # ### end Alembic commands ###
