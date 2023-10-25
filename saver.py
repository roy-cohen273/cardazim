from pathlib import Path
import json

from card import Card

from utils import is_parent


class Saver:
    """An object used to save cards."""
    def __init__(self, dir_path: Path):
        """Initialize a new Saver with a given directory to save in."""
        self.dir_path = dir_path

    def save(self, card: Card):
        """Save a given card to a given path."""
        card_path = self.get_card_path(card)
        card_path.mkdir(parents=True, exist_ok=True)
        metadata_path = card_path / "metadata.json"
        image_path = card_path / "image.jpg"

        metadata = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "image_path": str(image_path)
        }
        with metadata_path.open('w') as f:
            json.dump(metadata, f)

        card.image.save_image(image_path)

    def get_card_path(self, card: Card) -> Path:
        """Get the path to save the card in."""

        # the `is_parent` checks are necessary to protect from creators and names like: '..', '/home', ...

        creator_path = self.dir_path / card.creator
        if not is_parent(creator_path, self.dir_path):
            raise ValueError(f"Cannot save card due to invalid creator: {card.creator!r}")

        card_path = creator_path / card.name
        if not is_parent(card_path, creator_path):
            raise ValueError(f"Cannot save card due to invalid name: {card.name!r}")
        
        return card_path
