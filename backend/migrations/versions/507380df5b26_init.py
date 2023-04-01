"""init

Revision ID: 507380df5b26
Revises: 
Create Date: 2023-03-25 21:55:37.983284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "507380df5b26"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pastel_art",
        sa.Column("row_id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.String(), nullable=False),
        sa.Column("neg_prompt", sa.String(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("steps", sa.Integer(), nullable=False),
        sa.Column("guidance", sa.Integer(), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("row_id"),
        sa.UniqueConstraint("image"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pastel_art")
    # ### end Alembic commands ###
