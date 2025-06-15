import json
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from Ido_241524047 import Deck, DataManager

class DeckIOHandler:
    @staticmethod
    def export_deck(deck, parent):
        """Mengekspor deck ke file JSON"""
        options = QFileDialog.Option.ReadOnly
        path, _ = QFileDialog.getSaveFileName(
            parent, 
            "Export Deck", 
            f"{deck.name}.deck", 
            "Deck Files (*.deck);;All Files (*)", 
            options=options
        )
        
        if path:
            try:
                if not path.endswith('.deck'):
                    path += '.deck'
                    
                with open(path, 'w') as f:
                    json.dump(deck.to_dict(), f, indent=2)
                QMessageBox.information(parent, "Success", "Deck exported successfully!")
            except Exception as e:
                QMessageBox.critical(parent, "Error", f"Failed to export: {str(e)}")

    @staticmethod
    def import_deck(data_manager, decks, parent):
        """Mengimpor deck dari file JSON"""
        path, _ = QFileDialog.getOpenFileName(
            parent,
            "Import Deck",
            "",
            "Deck Files (*.deck);;All Files (*)"
        )
        
        if path:
            try:
                with open(path, 'r') as f:
                    deck_data = json.load(f)
                
                new_deck = Deck.from_dict(deck_data)
                existing_names = [d.name for d in decks]
                
                # Handle nama duplikat
                if new_deck.name in existing_names:
                    msg = QMessageBox(parent)
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText("A deck with this name already exists!")
                    msg.setInformativeText("Choose an action:")
                    msg.addButton("Overwrite", QMessageBox.ButtonRole.AcceptRole)
                    msg.addButton("Rename", QMessageBox.ButtonRole.YesRole)
                    msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
                    ret = msg.exec()
                    
                    if ret == 0:  # Timpa
                        data_manager.delete_deck(new_deck.name)
                        decks[:] = [d for d in decks if d.name != new_deck.name]
                    elif ret == 1:  # Ganti Nama
                        new_name, ok = QInputDialog.getText(
                            parent,
                            "Ganti Nama Deck",
                            "Masukkan nama baru:"
                        )
                        if ok and new_name:
                            new_deck.name = new_name
                        else:
                            return
                    else:  # Batal
                        return
                
                decks.append(new_deck)
                data_manager.save_deck(new_deck)
                QMessageBox.information(parent, "Success", "Deck imported successfully!")
                
            except Exception as e:
                QMessageBox.critical(parent, "Error", f"Failed to import: {str(e)}")