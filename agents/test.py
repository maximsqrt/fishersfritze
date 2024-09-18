import logging
from .audio_agent import AudioAgent
from main_agent import MainAgent

# Initialisiere das Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def test_audio_agent():
    # Erstelle eine Instanz von MainAgent (du kannst die Implementierung von MainAgent anpassen, wenn nötig)
    main_agent = MainAgent()
    
    # Erstelle eine Instanz von AudioAgent
    audio_agent = AudioAgent(main_agent)
    
    # Gib eine Debug-Nachricht aus, um zu sehen, ob der AudioAgent richtig erstellt wurde
    logging.debug("AudioAgent wurde erfolgreich erstellt.")
    
    # Optional: Führe eine Methode von AudioAgent aus (falls verfügbar)
    # audio_agent.some_method()  # Kommentiere das ein, wenn du eine Methode testen möchtest

if __name__ == "__main__":
    test_audio_agent()
