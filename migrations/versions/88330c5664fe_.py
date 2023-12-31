"""empty message

Revision ID: 88330c5664fe
Revises: 
Create Date: 2022-12-23 18:00:40.492107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88330c5664fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_name', sa.String(length=20), nullable=False),
    sa.Column('admin_password', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('admin_name')
    )
    op.create_table('students_infos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.String(length=20), nullable=False),
    sa.Column('student_class', sa.String(length=50), nullable=True),
    sa.Column('student_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('grade_infos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.String(length=20), nullable=True),
    sa.Column('student_class_id', sa.String(length=20), nullable=True),
    sa.Column('grade', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students_infos.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students_decision_infos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.String(length=20), nullable=True),
    sa.Column('student_class_id', sa.String(length=20), nullable=False),
    sa.Column('teacher_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students_infos.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students_decision_infos')
    op.drop_table('grade_infos')
    op.drop_table('students_infos')
    op.drop_table('admins')
    # ### end Alembic commands ###
