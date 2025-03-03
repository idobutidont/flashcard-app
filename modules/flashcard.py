#****************************************************************
#* FILENAME: flashcard.py
#* DESCRIPTION: 
#* AUTHOR:
#* DATE: 03 / 03 / 2025
#****************************************************************

import uuid

class Flashcard:
    def __init__(self, front="", back="", notes="", id=None):
        """
        Initialize a new flashcard.
        """
        self.front = front
        self.back = back
        self.notes = notes
        self.id = id if id is not None else str(uuid.uuid4())
    
    def to_dict(self):
        """
        Store flashcard data as a dictionary.
        """
        return {
            "id": self.id,
            "front": self.front,
            "back": self.back,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Load/parse flashcard data from a dictionary.
        """
        return cls(
            front=data.get("front", ""),
            back=data.get("back", ""),
            notes=data.get("notes", ""),
            id=data.get("id")
        )
