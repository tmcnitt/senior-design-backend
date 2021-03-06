"""Work on lessons

Revision ID: 939c248d42e9
Revises: b2b0ca940f20
Create Date: 2022-03-10 03:13:24.057457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '939c248d42e9'
down_revision = 'b2b0ca940f20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_id'), 'lesson', ['id'], unique=False)
    op.create_table('lessonstudent',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.Column('is_unlocked', sa.Boolean(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'lesson_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lessonstudent')
    op.drop_index(op.f('ix_lesson_id'), table_name='lesson')
    op.drop_table('lesson')
    # ### end Alembic commands ###
