import sys
import argparse

import requests
from flask import Flask, render_template, redirect, url_for, current_app

app = Flask(__name__)


@app.route('/')
def index():
	return redirect(url_for('creators'))


@app.route('/creators/')
def creators():
	creators = requests.get(f"http://{current_app.config['api_url']}/creators/").json()
	return render_template('creators.html', creators=creators)


@app.route('/creators/<string:creator>/cards/')
def cards(creator):
	cards = requests.get(f"http://{current_app.config['api_url']}/creators/{creator}/cards/").json()
	return render_template('cards.html', creator=creator, cards=cards)


@app.route('/creators/<string:creator>/cards/<string:card_name>/')
def card(creator, card_name):
	card = requests.get(f"http://{current_app.config['api_url']}/creators/{creator}/cards/{card_name}/").json()
	return render_template('card.html', card=card)


@app.route('/creators/<string:creator>/cards/<string:card_name>/image.jpg')
def card_image(creator, card_name):
	return redirect(f"http://{current_app.config['api_url']}/creators/{creator}/cards/{card_name}/image.jpg")


def get_args():
	parser = argparse.ArgumentParser(description='run the GUI server.')
	parser.add_argument('server_ip', type=str,
						help='The server\'s ip')
	parser.add_argument('server_port', type=int,
						help='The server\'s port')
	parser.add_argument('api_url', type=str,
						help='The URL used to connect to the API server')
	return parser.parse_args()


def main():
	args = get_args()
	try:
		app.config['api_url'] = args.api_url
		app.run(args.server_ip, args.server_port)
	except Exception as error:
		print(f'ERROR: {error}', file=sys.stderr)
		return 1


if __name__ == '__main__':
	sys.exit(main())
