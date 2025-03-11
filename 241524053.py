import uuid

class Flashcard:
    def __init__(self, front, back, notes="", id=None, right_count=0, wrong_count=0):
        """
        Representasi satu flashcard dengan pertanyaan, jawaban, dan statistik.
        """
        self.front = front
        self.back = back
        self.notes = notes
        self.id = id if id is not None else str(uuid.uuid4())
        self.right_count = right_count
        self.wrong_count = wrong_count
    
    def to_dict(self):
        """Mengubah flashcard menjadi dictionary agar bisa disimpan dalam JSON."""
        return {
            "id": self.id,
            "front": self.front,
            "back": self.back,
            "notes": self.notes,
            "right_count": self.right_count,
            "wrong_count": self.wrong_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """Membuat flashcard dari dictionary."""
        return cls(
            front=data.get("front", ""),
            back=data.get("back", ""),
            notes=data.get("notes", ""),
            id=data.get("id"),
            right_count=data.get("right_count", 0),
            wrong_count=data.get("wrong_count", 0)
        )


class Deck:
    def __init__(self, name, flashcards=None):
        """
        Kumpulan flashcard dalam satu deck.
        """
        self.name = name
        self.flashcards = flashcards if flashcards else []
    
    def add_flashcard(self, front, back, notes=""):
        """Menambahkan flashcard baru ke deck."""
        card = Flashcard(front, back, notes)
        self.flashcards.append(card)
        return card
    
    def remove_flashcard(self, card_id):
        """Menghapus flashcard berdasarkan ID."""
        self.flashcards = [card for card in self.flashcards if card.id != card_id]
    
    def get_flashcard(self, index):
        """Mengambil flashcard berdasarkan indeks."""
        if 0 <= index < len(self.flashcards):
            return self.flashcards[index]
        return None
    
    def to_dict(self):
        """Mengubah deck menjadi dictionary agar bisa disimpan dalam JSON."""
        return {
            "name": self.name,
            "flashcards": [card.to_dict() for card in self.flashcards]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Membuat deck dari dictionary."""
        flashcards = [Flashcard.from_dict(card_data) for card_data in data.get("flashcards", [])]
        return cls(name=data.get("name", ""), flashcards=flashcards)
