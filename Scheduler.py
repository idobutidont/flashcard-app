from datetime import datetime, timedelta
import math

class Scheduler:
    def __init__(self):
        self.base_interval = 1  # Base interval in days
        self.max_interval = 365  # Maximum interval in days
        self.learning_rate = 1.0  # Adjusted based on user performance
    
    def calculate_retention_score(self, card, is_right):
        """
        Calculate retention score based on performance and time since last review.
        """
        time_since_review = (datetime.now() - datetime.fromisoformat(card.last_reviewed)).days
        if time_since_review < 1:
            time_since_review = 1
        
        # Base retention score update
        if is_right:
            score = card.retention_score + (0.1 * (1 / card.difficulty))
        else:
            score = max(0.0, card.retention_score - (0.2 * card.difficulty))
        
        # Factor in time decay
        decay_factor = 1 / (1 + time_since_review / 30)  # Decay over 30 days
        score = score * decay_factor
        
        return min(1.0, max(0.0, score))
    
    def update_learning_rate(self, deck):
        """
        Adjust learning rate based on overall deck performance.
        """
        if not deck.flashcards:
            return
        
        total_attempts = sum(card.right_count + card.wrong_count for card in deck.flashcards)
        total_right = sum(card.right_count for card in deck.flashcards)
        accuracy = total_right / total_attempts if total_attempts > 0 else 0
        
        # Increase learning rate for high accuracy, decrease for low
        if accuracy > 0.8:
            self.learning_rate = min(self.learning_rate + 0.1, 2.0)
        elif accuracy < 0.5:
            self.learning_rate = max(self.learning_rate - 0.1, 0.5)
    
    def schedule_card(self, card, is_right):
        """
        Schedule the next review for a card based on performance.
        """
        card.retention_score = self.calculate_retention_score(card, is_right)
        card.last_reviewed = datetime.now().isoformat()
        
        # Calculate interval based on retention score, difficulty, and learning rate
        interval = self.base_interval * (card.retention_score * 5) * (1 / card.difficulty) * self.learning_rate
        interval = max(1, min(self.max_interval, interval))
        
        # Adjust interval based on consecutive correct answers
        if is_right and card.right_count > card.wrong_count:
            interval *= (1 + card.right_count * 0.1)
        
        card.next_review = (datetime.now() + timedelta(days=interval)).isoformat()
        return card.next_review
    
    def get_next_card_index(self, deck):
        """
        Select the next card to review based on due date and priority.
        """
        if not deck.flashcards:
            return 0
        
        now = datetime.now()
        due_cards = [(i, card) for i, card in enumerate(deck.flashcards) if datetime.fromisoformat(card.next_review) <= now]
        
        if not due_cards:
            return 0  # Default to first card if none are due
        
        # Prioritize cards with lower retention scores and higher difficulty
        sorted_cards = sorted(due_cards, key=lambda x: (x[1].retention_score, -x[1].difficulty))
        return sorted_cards[0][0]