import logging
from agents.screen_agent import ScreenAgent
from agents.audio_agent import AudioAgent
from agents.fishing_agent import FishingAgent
from main_agent import MainAgent

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.debug("MainAgent initialization started")
    main_agent = MainAgent()
    logging.debug("MainAgent initialized")

    logging.debug("ScreenAgent initialization started")
    screen_agent = ScreenAgent(main_agent)
    logging.debug("ScreenAgent initialized")

    # Starte den ScreenAgent zuerst
    logging.debug("Starting ScreenAgent")
    screen_agent.start()
    logging.debug("ScreenAgent started")
    

    # Initialisiere die restlichen Agenten
    logging.debug("AudioAgent initialization started")
    audio_agent = AudioAgent(main_agent)
    logging.debug("AudioAgent initialized")

    logging.debug("FishingAgent initialization started")
    fishing_agent = FishingAgent(main_agent, audio_agent)
    logging.debug("FishingAgent initialized")

    # Zeige das Menü einmal an
    print("\nEnter a command:")
    print("\tF\tStart Fishing")
    print("\tQ\tQuit")

    # Warte auf die erste Benutzereingabe
    while True:
        user_input = input("Please enter a command: ").strip().upper()
        if user_input == 'F':
            print("Starting Fishing Agent...")
            fishing_agent.start()
            break  # Beende die Schleife nach dem Start des Fishing Agents
        elif user_input == 'Q':
            print("Quitting...")
            # Stoppe die Agenten und beende das Programm
            screen_agent.stop()
            audio_agent.stop()
            fishing_agent.stop()
            return
        else:
            print("Invalid command. Please try again.")

    # Nach dem Start des Fishing Agents nur noch 'Q' zum Beenden akzeptieren
    while True:
        user_input = input("Press 'Q' to Quit: ").strip().upper()
        if user_input == 'Q':
            print("Quitting...")
            break
        else:
            print("Invalid command. Press 'Q' to Quit.")

    # Stoppe alle Agenten vor dem Beenden
    fishing_agent.stop()
    screen_agent.stop()
    audio_agent.stop()

if __name__ == "__main__":
    main()
