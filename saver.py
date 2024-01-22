from card import Card
from driver import Driver
import all_drivers


class Saver:
    """An object used to save cards."""

    def __init__(self, url: str):
        """Initialize a new Saver with a given url to save in."""
        self.driver = Driver.get_driver(url)

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
