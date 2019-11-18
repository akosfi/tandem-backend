import datetime


from app.main import db
from app.main.model.event import Event
from app.main.model.user import User
from ..util import create_response_object

def save_new_event(data, creator_id): 
    new_event = Event(
        name=data['name'],
        public=data['public'],
        date=datetime.datetime.utcnow(),
        cover_photo='asd', #TODOTODOTODO
        location=data['location'],
        details=data['details'],
        creator_id=creator_id
    )
    save_changes(new_event)
    return create_response_object(201, 'Successfully created.', new_event.toDTO()), 201


def get_an_event_detailed(id, user_id): 
    event = Event \
            .query \
            .filter_by(id=id) \
            .first() \
            .toDTO()


    user_joined = Event.query.filter_by(id=id).filter(Event.users.any(id=user_id)).first()

    if user_joined:
        event['user_joined']=True
    else: 
        event['user_joined']=False

    return event

def get_all_events():
    return Event \
            .query \
            .all()

def get_user_created_events(user_id):
    return Event \
            .query \
            .filter_by(creator_id=user_id) \
            .all()

def get_user_joined_events(user_id):
    #TODO
    return Event.query.filter_by(creator_id=user_id).all()


def user_join_event(user_id, event_id):
    event = Event \
            .query \
            .filter_by(id=event_id) \
            .first()

    user = User \
            .query \
            .filter_by(id=user_id) \
            .first()

    event.users.append(user)
    db.session.commit() 

    return create_response_object(201, 'Successfully joined event.'), 201

def user_leave_event(user_id, event_id):
    event = Event \
            .query \
            .filter_by(id=event_id) \
            .first()

    user = User \
            .query \
            .filter_by(id=user_id) \
            .first()
    
    print(event)
    print(user)

    event.users.remove(user)
    db.session.commit() 


    return create_response_object(201, 'Successfully left event.'), 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()