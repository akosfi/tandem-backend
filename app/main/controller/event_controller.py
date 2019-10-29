from flask import request
from flask_restplus import Resource

from app.main.model.event import Event

from ..util import create_response_object, jwt_required
from ..util.dto import EventDto
from ..service.event_service import save_new_event, get_all_events, get_an_event

api = EventDto.api
_event_detailed = EventDto.event_detailed
_event = EventDto.event


@api.route('/')
class EventList(Resource):
    @api.doc('list_of_events')
    @api.marshal_list_with(_event, envelope='events')
    def get(self):
        """List all events"""
        return get_all_events()

    @api.response(201, 'Event successfully created.')
    @api.doc('create a new event')
    @api.expect(_event, validate=True)
    @jwt_required
    def post(self):
        """Creates a new Event """

        jwt_auth_token = request.cookies.get('jwt_auth')
        payload = jwt.decode(jwt_auth_token, key)

        data = request.json
        return save_new_event(data, payload['user']['id'])



@api.route('/<id>')
@api.param('id', 'The Event identifier')
@api.response(404, 'Event not found.')
class EventEntity(Resource):
    @api.doc('get an event')
    @api.marshal_with(_event_detailed)
    def get(self, id):
        """get an event given its identifier"""
        event = get_an_event(id)
        if not event:
            api.abort(404)
        else:
            return event


    