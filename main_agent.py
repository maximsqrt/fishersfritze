import threading

class MainAgent:
    def __init__(self):
        self.lock = threading.Lock()
        self.cur_img = None
        self.cur_imgHSV = None
        self.agents = []
        self.fishing_thread = None
        self.zone = "Feralas"
        self.time = "night"
        print("MainAgent setup complete...")

    def get_cur_img(self):
        with self.lock:
            return self.cur_img

    def set_cur_img(self, img):
        with self.lock:
            self.cur_img = img

    def add_agent(self, agent):
        if agent not in self.agents:
            self.agents.append(agent)

    def start_agents(self):
        for agent in self.agents:
            agent.start()

    def stop_agents(self):
        for agent in self.agents:
            agent.stop()
