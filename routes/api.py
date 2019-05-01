from flask import Blueprint, request, jsonify
from app.response.message_build import BuilderResponse
from app.base import interpreter
from app.models import Requests

bp = Blueprint('api', __name__)


@bp.route('/city')
def user_city():
    inp = request.args.get('station_name')
    Requests.insert_city(inp)
    status, value = interpreter.user_city(inp)
    data = BuilderResponse.get_response(status, value)

    return jsonify(data)


@bp.route('/state')
def user_state():
    dict_inp = [{'station_name': request.args.get('station_name'), 'state_name': request.args.get('state_name'), 'station_ids': "1", 'type': 'STATION'}]
    inp = request.args.get('state_name')
    Requests.insert_state(inp)
    status, value = interpreter.user_state(dict_inp)
    data = BuilderResponse.get_response(status, value)

    return jsonify(data)


@bp.route('/date')
def date():
    date = request.args.get('date')
    Requests.insert_date(date)
    status, value = interpreter.user_travel_date(date)
    data = BuilderResponse.get_response(status, value)

    return jsonify(data)
