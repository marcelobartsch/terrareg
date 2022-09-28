"""Add table for namespaces and replace namespace field in module provider with foreign key

Revision ID: d72c5339c21b
Revises: acd5e83c690f
Create Date: 2022-09-28 06:14:12.046484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72c5339c21b'
down_revision = 'acd5e83c690f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('namespace',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('module_provider', sa.Column('namespace_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_module_provider_namespace_id_namespace_id', 'module_provider', 'namespace', ['namespace_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('module_provider', 'namespace')
    op.drop_constraint('fk_module_version_file_module_version_id_module_version_id', 'module_version_file', type_='foreignkey')
    op.create_foreign_key('fk_module_version_file_module_version_id_module_version_id', 'module_version_file', 'module_version', ['module_version_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_module_version_file_module_version_id_module_version_id', 'module_version_file', type_='foreignkey')
    op.create_foreign_key('fk_module_version_file_module_version_id_module_version_id', 'module_version_file', 'submodule', ['module_version_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('module_provider', sa.Column('namespace', sa.VARCHAR(length=1024), nullable=True))
    op.drop_constraint('fk_module_provider_namespace_id_namespace_id', 'module_provider', type_='foreignkey')
    op.drop_column('module_provider', 'namespace_id')
    op.drop_table('namespace')
    # ### end Alembic commands ###
