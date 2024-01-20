from card import Card
from fs_driver import FSDriver
from mongodb_driver import MongoDBDriver


class Saver:
    """An object used to save cards."""

    def __init__(self, url: str):
        """Initialize a new Saver with a given url to save in."""
        # TODO: parse `url` and determine the driver.
        #       for now, it is hardcoded.
        # self.driver = FSDriver(url)
        self.driver = MongoDBDriver('localhost', 27017, 'test_db')

    def save(self, card: Card):
        """Save a given card."""
        file_id, file = self.driver.insert_file()
        with file:
            card.image.save_image(file, format='JPEG')

        metadata = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "image_file_id": file_id,
        }
        self.driver.insert_object(metadata)
