from app.main import db
from app.main.model.event import Event

def save_new_event(data, creator_id): 
    new_event = Event(
        name=data['name'],
        public=data['public'],
        location=data['location'],
        details=data['details'],
        creator_id=creator_id
    )
    save_changes(new_event)
    return create_response_object(201, 'Successfully created.'), 201


def get_an_event(): 
    return Event.query.filter_by(id=id).first()

def get_all_events():
    return Event.query.all()

def user_join_event(user_id, event_id):
    event = Event.query.filter_by(id=event_id).first()
    user = User.query.filter_by(id=user_id).first()
    
    event.users.add(user)
    db.session.commit() 

def user_quit_event(user_id, event_id):
    event = Event.query.filter_by(id=event_id).first()
    user = User.query.filter_by(id=user_id).first()
    
    event.users.remove(user)
    db.session.commit() 

def save_changes(data):
    db.session.add(data)
    db.session.commit()