import logging
from agents.screen_agent import ScreenAgent
from agents.audio_agent import AudioAgent
from agents.fishing_agent import FishingAgent
from main_agent import MainAgent

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    
    main_agent = MainAgent()
    logging.debug("MainAgent initialized")

    
    screen_agent = ScreenAgent(main_agent)
    main_agent.screen_agent = screen_agent
    logging.debug("ScreenAgent initialized")
    screen_agent.start()
    
    logging.debug("ScreenAgent started")
    

    
    audio_agent = AudioAgent(main_agent)
    logging.debug("AudioAgent initialized")

    
    
    fishing_agent = None
    # show menu
    print("\nEnter a command:")
    print("\tF\tStart Fishing")
    print("\tQ\tQuit")
    
    # wait
    while True:
        user_input = input("Please enter a command: ").strip().upper()
        
        if user_input == 'F':
            if fishing_agent is None:  # Initialisiere den FishingAgent nur einmal, wenn F gedrückt wird
                print("Starting Fishing Agent...")
                logging.debug("FishingAgent initialization started")
                fishing_agent = FishingAgent(main_agent, audio_agent, screen_agent)
  # INITIALISIERUNG HIER
                logging.debug("FishingAgent initialized")
                fishing_agent.start()
            else:
                print("Fishing Agent is already running.")
        
        elif user_input == 'Q':
            print("Quitting...")
            screen_agent.stop()
            audio_agent.stop()
            if fishing_agent:
                fishing_agent.stop()
            break  # Beende das Program
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
