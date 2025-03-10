class UserStats:
    def __init__(self):
        self.total.attempt = 0
        self.correct.answers = 0
        self.incorrect.answers = 0

    def update_stats(self, is_correct: bool):
        self.total.attempt += 1
        if is_correct:
            self.correct.answers += 1
        else:
            self.incorrect.answers += 1
        
    def akurasi (self):
        if self.total.attempt == 0:
            return 0
        return (self.correct.answers / self.total.attempt)*100
    
    def display_stats (self):
        print("\n ===== Statistik =====")
        print(f"Total kartu dijawab : {self.total.attempt}")
        print(f"Total jawaban benar : {self.correct.answers}")
        print(f"Total jumlah salah : {self.uncorrect.answers}")
        print(f"Akurasi : {self.get.akurasi():.02f}%")

    