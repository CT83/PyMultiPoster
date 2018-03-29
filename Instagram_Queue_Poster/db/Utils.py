from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Instagram_Queue_Poster.db.models.InstagramQueuer import Base, Person, Address

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_person = Person(name='new person')
session.add(new_person)
session.commit()

new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()
