"""add users data

Revision ID: f4398eb0d2a4
Revises: 8bf5d32f88a7
Create Date: 2023-04-13 10:38:08.066533

"""
from alembic import op
from sqlalchemy import Integer, String, column, table

# revision identifiers, used by Alembic.
revision = "f4398eb0d2a4"
down_revision = "8bf5d32f88a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    users_table = table("users", column("username", String), column("api_key", String))

    op.bulk_insert(
        users_table,
        [
            {"username": "test1", "api_key": "test"},
            {"username": "test2", "api_key": "test2"},
            {"username": "test3", "api_key": "test3"},
        ],
    )

    users_to_users_table = table(
        "user_to_user", column("followers_id", Integer), column("following_id", Integer)
    )

    op.bulk_insert(
        users_to_users_table,
        [
            {"followers_id": 1, "following_id": 2},
            {"followers_id": 2, "following_id": 1},
        ],
    )


def downgrade() -> None:
    pass
