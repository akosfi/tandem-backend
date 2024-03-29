from datetime import datetime

from flask_restplus import marshal

from app.main import db
from app.main.model.event import Event
from app.main.model.user import User
from ..util import create_response_object
from ..util.dto import EventDTO


def save_new_event(data, creator_id): 
    new_event = Event(
        name=data['name'],
        public=data['public'],
        date=datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        location=data['location'],
        details=data['details'],
        creator_id=creator_id,
        cover_photo='a'#?
    )
    save_changes(new_event)
    return create_response_object(201, 'Successfully created.', marshal(new_event, EventDTO.event)), 201


def get_an_event_detailed(id, user_id): 
    event = Event \
            .query \
            .filter_by(id=id) \
            .first()

    people_going = len(Event.query.filter_by(id=id).first().users)
    
    user_joined_events = User \
                            .query \
                            .filter_by(id=user_id) \
                            .first() \
                            .events_joined
    
    user_joined = False

    if event in user_joined_events:
        user_joined=True
    else: 
        user_joined=False
    
    event = marshal(event, EventDTO.event_detailed)

    event['people_going']=people_going
    event['user_joined']=user_joined

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

    event.users.remove(user)
    db.session.commit() 


    return create_response_object(201, 'Successfully left event.'), 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def set_event_cover_picture(id, picture):
    event = db.session.query(Event) \
            .filter_by(id=id) \
            .first()

    event.cover_photo = picture

    db.session.commit()

    return picture
