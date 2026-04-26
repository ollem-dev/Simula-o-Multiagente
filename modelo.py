from mesa import Model
from mesa.datacollection import DataCollector
from agente import EstudanteAgent

class SalaDeAulaModel(Model):
    def __init__(self, N, taxa_dificuldade, resiliencia_media, seed=42):
        super().__init__(seed=seed)
        
        self.num_agents = N
        self.dificuldade_cenario = 0.1 
        self.taxa_dificuldade = taxa_dificuldade
        
        for _ in range(self.num_agents):
            EstudanteAgent(self, resiliencia_media)
            
        self.datacollector = DataCollector(
            model_reporters={"Dificuldade": "dificuldade_cenario"},
            agent_reporters={"Estresse": "estresse", "Competencia": "competencia_equipe"}
        )

    def step(self):
        self.dificuldade_cenario = min(1.0, self.dificuldade_cenario + self.taxa_dificuldade)
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")