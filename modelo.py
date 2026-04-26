from mesa import Model
from mesa.datacollection import DataCollector
from agente import EstudanteAgent

class SalaDeAulaModel(Model):
    # O modelo agora aceita a taxa e a resiliencia
    def __init__(self, N, taxa_dificuldade, resiliencia_media):
        super().__init__()
        self.num_agents = N
        self.dificuldade_cenario = 0.1 
        self.taxa_dificuldade = taxa_dificuldade
        
        for _ in range(self.num_agents):
            # Passamos a resiliência média para cada aluno na hora de criar
            EstudanteAgent(self, resiliencia_media)

        self.datacollector = DataCollector(
            model_reporters={"Dificuldade": "dificuldade_cenario"},
            agent_reporters={"Estresse": "estresse", "Competencia": "competencia_equipe"}
        )

    def step(self):
        # A dificuldade aumenta com base no valor do slider, não num valor fixo
        self.dificuldade_cenario += self.taxa_dificuldade 
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")