from app.main import db
from app.main.model.event import Event

save_new_event, get_all_events, get_an_event

def save_new_event: 
    new_event = Event(
        name=data['name'],
        public=data['public'],
        location=data['location'],
        details=data['details']
    )
    save_changes(new_event)
    return create_response_object(201, 'Successfully created.'), 201
    

def get_an_event: 
    return Event.query.filter_by(id=id).first()

def get_all_events():
    return Event.query.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()