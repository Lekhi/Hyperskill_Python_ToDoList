from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from datetime import timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def print_menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")


option = 'z'

while option != '0':
    print_menu()
    option = input()

    if option == '1':
        counter = 1
        rows = session.query(Table).filter(Table.deadline == datetime
                                           .today().date()).all()
        print(f'\nToday {datetime.today().day}'
              f' {datetime.strftime(datetime.today(), "%b")}:')
        if rows:
            for row in rows:
                print(f'{counter}. {row}')
                counter += 1
        else:
            print('Nothing to do!')

    if option == '2':
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline <= datetime
                                           .today().date()
                                           + timedelta(days=6)).all()

        for i in range(7):
            day = today + timedelta(days=i)
            count_of_activities = 0
            counter = 1
            print()
            print(f'{day.strftime("%A %d %b")}')
            for row in rows:
                if row.__dict__['deadline'] == day:
                    count_of_activities += 1
                    print(f'{counter}. {row}')
                    counter += 1

            if count_of_activities == 0:
                print('Nothing to do!')

    if option == '3':
        counter = 1
        rows = session.query(Table).all()
        print('\nAll tasks:')
        if rows:
            for u in session.query(Table).all():
                date = u.__dict__['deadline']
                print(f"{counter}. {u.__dict__['task']}. "
                      f"{date.day} {datetime.strftime(date, '%b')}")
                counter += 1
        else:
            print('Nothing to do!')

    if option == '4':
        counter = 1
        rows = session.query(Table).filter(Table.deadline <= datetime
                                           .today().date()).all()
        print('Missed tasks:')

        if rows:
            for row in rows:
                print(f'{counter}. {row.__dict__["task"]}.'
                      f' {row.__dict__["deadline"].strftime("%d %b")}')
                counter += 1
        else:
            print('Nothing is missed!')

    if option == '5':
        print('\nEnter task')
        entered_task = input()
        print('Enter deadline')
        entered_deadline = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Table(task=entered_task, deadline=entered_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!')

    if option == '6':
        print("Chose the number of the task you want to delete:")
        counter = 1
        rows = session.query(Table).filter(Table.deadline <= datetime
                                           .today().date()).all()
        if rows:
            for row in rows:
                print(f'{counter}. {row.__dict__["task"]}.'
                      f' {row.__dict__["deadline"].strftime("%d %b")}')
                counter += 1
            choice = int(input()) - 1
            specific_row = rows[choice]
            session.delete(specific_row)

            session.commit()

            print('The task has been deleted!')
        else:
            print('Nothing to delete')

    if option == '0':
        print('Bye!')

    print()
