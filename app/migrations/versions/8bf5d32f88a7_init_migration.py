"""Init migration

Revision ID: 8bf5d32f88a7
Revises: 
Create Date: 2023-04-13 10:38:01.616182

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bf5d32f88a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("tweet_data", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tweets_id"), "tweets", ["id"], unique=False)
    op.create_table(
        "user_to_user",
        sa.Column("followers_id", sa.Integer(), nullable=False),
        sa.Column("following_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["followers_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["following_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("followers_id", "following_id"),
    )
    op.create_table(
        "likes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tweets_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tweets_id"],
            ["tweets.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_likes_id"), "likes", ["id"], unique=False)
    op.create_table(
        "medias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("path_media", sa.String(), nullable=False),
        sa.Column("tweet_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tweet_id"],
            ["tweets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_medias_id"), "medias", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_medias_id"), table_name="medias")
    op.drop_table("medias")
    op.drop_index(op.f("ix_likes_id"), table_name="likes")
    op.drop_table("likes")
    op.drop_table("user_to_user")
    op.drop_index(op.f("ix_tweets_id"), table_name="tweets")
    op.drop_table("tweets")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
