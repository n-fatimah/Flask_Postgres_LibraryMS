"""user table

Revision ID: 3e2cafcfc261
Revises: 
Create Date: 2024-07-26 18:52:45.458019

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e2cafcfc261"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(length=80), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
