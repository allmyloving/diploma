from flask import *
import functions

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/data/train/<string:lang>', methods=['GET'])
def get_train_data(lang):
    return jsonify(functions.retrieve_train_data(lang)), 200


@app.route('/data/train/<string:lang>', methods=['POST'])
def create_train_data(lang):
    validate_request_has('amount')
    validate_is_number('amount')
    try:
        functions.load_train_data(lang, int(request.json['amount']))
    except Exception as e:
        return error_response(str(e), 500)
    return '', 201


@app.route('/data/test/<string:lang>', methods=['GET'])
def get_test_data(lang):
    return jsonify(functions.retrieve_test_data(lang)), 200


@app.route('/data/test/<string:lang>', methods=['POST'])
def create_test_data(lang):
    validate_request_has('amount')
    validate_is_number('amount')
    try:
        functions.load_test_data(lang, int(request.json['amount']))
    except Exception as e:
        return error_response(str(e), 500)
    return '', 201


@app.route('/data/', methods=['DELETE'])
def clear_all_data():
    functions.cleanup_all_data()
    return jsonify(), 204


@app.route('/lang/detect', methods=['POST'])
def detect_language():
    validate_request_has('text')
    if 'classifier' in request.json:
        result = functions.detect_language(request.json['text'], classifier=request.json['classifier'])
    else:
        result = functions.detect_language(request.json['text'])
    return jsonify(result), 200


def error_response(message, status):
    return make_response(jsonify({'error': message}), status)


def validate_request_has(param: str):
    if not request.json or not param in request.json:
        abort(error_response('Missing `%s` in request' % str(param), 400))


def validate_is_number(param):
    value = request.json[param]
    if not value.isdigit() or int(value) <= 0:
        abort(error_response('%s should be positive integer' % param, 400))


if __name__ == '__main__':
    app.run(debug=True)
