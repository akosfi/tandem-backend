import jwt

from flask import request
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from app.main.model.event import Event

from ..util import create_response_object, jwt_required, upload_image, get_user_from_request
from ..util.dto import EventDTO
from ..service.event_service import set_event_cover_picture, save_new_event, user_leave_event, user_join_event, get_all_events, get_an_event_detailed, get_user_created_events, get_user_joined_events
from ..config import key

api = EventDTO.api


@api.route('/')
class EventList(Resource):
    @api.doc('list_of_events')
    @api.marshal_list_with(EventDTO.event, envelope='events')
    def get(self):
        """List all events"""
        return get_all_events()

    @api.response(201, 'Event successfully created.')
    @api.doc('create a new event')
    @api.expect(EventDTO.event_creation, validate=True)
    @jwt_required
    def post(self):
        """Creates a new Event """

        user = get_user_from_request(request)

        data = request.json
        return save_new_event(data, user['id'])



@api.route('/<id>/join')
class EventJoin(Resource):
    @api.doc('Join event')
    @jwt_required
    def get(self, id):
        """Join event"""

        user = get_user_from_request(request)

        return user_join_event(user['id'], id)


@api.route('/<id>/leave')
class EventLeave(Resource):
    @api.doc('Leave event')
    @jwt_required
    def get(self, id):
        """Leave event"""

        user = get_user_from_request(request)

        return user_leave_event(user['id'], id)

@api.route('/<id>/picture/')
class EventPicture(Resource):

    @jwt_required
    def post(self, id):
        data = request.json

        event_picture = upload_image(request)

        set_event_cover_picture(id, event_picture)

        return create_response_object(200, 'Image uploaded succesfully.', event_picture), 200


@api.route('/user_created')
class EventUserCreatedList(Resource):
    @api.doc('list_of_user_created_events')
    @api.marshal_list_with(EventDTO.event, envelope='events')
    @jwt_required
    def get(self):
        """List all events"""
        user = get_user_from_request(request)
          
        return get_user_created_events(user['id'])

@api.route('/user_joined')
class EventUserJoinedList(Resource):
    @api.doc('list_of_user_joined_events')
    @api.marshal_list_with(EventDTO.event, envelope='events')
    @jwt_required
    def get(self):
        """List all events"""
        user = get_user_from_request(request)
          
        return get_user_joined_events(user['id'])



@api.route('/<id>')
@api.param('id', 'The Event identifier')
@api.response(404, 'Event not found.')
class EventEntity(Resource):
    @api.doc('get an event')
    @api.marshal_with(EventDTO.event_detailed)
    def get(self, id):
        """get an event given its identifier"""

        user = get_user_from_request(request)

        event = get_an_event_detailed(id, user['id'])
        if not event:
            api.abort(404)
        else:
            return event


    