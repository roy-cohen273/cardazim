import struct

from PIL import Image

from card import Card


def assert_card(data, name, creator, riddle, solution=None, image_file=None, *, is_solved):
	"""Test that the given data represents a valid card and check the card's fields.

	is_solved represents whether the card is expected to be solved.

	When the solution to card is unknown, solution and image_file can be unspecified.
	If the card is not solved and a solution and image_file are specified, the test will try to solve the card.
	"""

	# test the message protocol
	assert len(data) >= 4
	length, = struct.unpack('<I', data[:4])
	data = data[4:]
	assert length == len(data)

	# test deserialization and card fields
	card = Card.deserialize(data)
	assert card.name == name
	assert card.creator == creator
	assert card.riddle == riddle

	if is_solved:
		# assert that the card is solved
		if solution is None:
			assert card.solution is not None
		else:
			assert card.solution == solution
		assert card.image.key_hash is None
	else:
		# assert that the card is not solved
		assert card.solution is None
		assert card.image.key_hash is not None

		# try to solve the card
		if solution is not None and image_file is not None:
			assert card.solve(solution)
			assert card.solution == solution
			assert card.image.key_hash is None
			assert card.image.image_data == Image.open(image_file).tobytes()
