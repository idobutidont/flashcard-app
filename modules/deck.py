from modules.flashcard import Flashcard

class Deck:
    def __init__(self, name, flashcards=None):
        """
        Initialize flashcard deck.
        """
        self.name = name
        self.flashcards = flashcards if flashcards else []
    
    def add_flashcard(self, front, back, notes=""):
        """
        
        """
        card = Flashcard(front, back, notes)
        self.flashcards.append(card)
        return card
    
    def remove_flashcard(self, card_id):
        """
        
        """
        self.flashcards = [card for card in self.flashcards if card.id != card_id]
    
    def get_flashcard(self, index):
        """
        
        """
        if 0 <= index < len(self.flashcards):
            return self.flashcards[index]
        return None
    
    def to_dict(self):
        """
        
        """
        return {
            "name": self.name,
            "flashcards": [card.to_dict() for card in self.flashcards]
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        
        """
        flashcards = [Flashcard.from_dict(card_data) for card_data in data.get("flashcards", [])]
        return cls(name=data.get("name", ""), flashcards=flashcards)
