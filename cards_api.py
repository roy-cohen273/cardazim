import sys
import argparse

from flask import Flask, jsonify, current_app, send_file, abort

from driver import Driver
import all_drivers

app = Flask(__name__)

def get_db():
	return current_app.config['database']


@app.route('/creators/')
def creators():
	db = get_db()
	objects = db.find_objects(projection=('creator',))
	creators = list({obj['creator'] for obj in objects})
	return jsonify(creators)


@app.route('/creators/<string:creator>/cards/')
def cards(creator):
	db = get_db()
	objects = db.find_objects(filter={'creator': creator}, projection=('name',))
	card_names = list({obj['name'] for obj in objects})
	return jsonify(card_names)


@app.route('/creators/<string:creator>/cards/<string:card_name>/')
def card(creator, card_name):
	db = get_db()
	card = db.find_one_object(filter={'creator': creator, 'name': card_name})
	if card is None:
		abort(404)
	card.pop('image_file_id', None)
	return jsonify(card)


@app.route('/creators/<string:creator>/cards/<string:card_name>/image.jpg')
def card_image(creator, card_name):
	db = get_db()
	card = db.find_one_object(filter={'creator': creator, 'name': card_name}, projection=('image_file_id',))
	if card is None:
		abort(404)
	image_file_id = card['image_file_id']
	file = db.get_file(image_file_id)
	if file is None:
		raise Exception(f'card has bad file ID. {creator = !r} {card_name = !r} {image_file_id = !r}')
	return send_file(file, download_name='image.jpg', mimetype='image/jpeg')


def get_args():
	parser = argparse.ArgumentParser(description='run the API server.')
	parser.add_argument('server_ip', type=str,
						help='The server\'s ip')
	parser.add_argument('server_port', type=int,
						help='The server\'s port')
	parser.add_argument('database_url', type=str,
						help='The URL used to connect to the database')
	return parser.parse_args()


def main():
	args = get_args()
	try:
		app.config['database'] = Driver.get_driver(args.database_url)
		app.run(args.server_ip, args.server_port)
	except Exception as error:
		print(f'ERROR: {error}', file=sys.stderr)
		return 1


if __name__ == '__main__':
	sys.exit(main())
