from pathlib import Path
import json

from card import Card

class Saver:
    def save(self, card: Card, dir_path='.'):
        """Save a given card to a given path."""
        creator_path = Path(dir_path) / card.creator
        creator_path.mkdir(exist_ok=True)
        card_path = creator_path / card.name
        card_path.mkdir(exist_ok=True)
        
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

        card.image.image.save(image_path)
