import random
from mesa import Agent

class EstudanteAgent(Agent):
    # Agora recebemos a 'resiliencia_base' definida pelo slider
    def __init__(self, model, resiliencia_base):
        super().__init__(model)
        
        # Cria uma pequena variação (+/- 0.2) em torno da média escolhida, sem passar de 0 ou 1
        self.resiliencia = random.uniform(max(0.0, resiliencia_base - 0.2), min(1.0, resiliencia_base + 0.2)) 
        self.competencia_equipe = random.uniform(0.1, 1.0)
        self.estresse = 0.0 

    def step(self):
        impacto = self.model.dificuldade_cenario * (1.0 - self.resiliencia)
        self.estresse += impacto
        
        outros_estudantes = list(self.model.agents)
        colega = self.random.choice(outros_estudantes)
        
        if colega != self:
            if colega.estresse < 0.5:
                self.estresse -= (colega.competencia_equipe * 0.05)
                self.competencia_equipe += 0.01 
            else:
                self.estresse += 0.05
        
        self.estresse = max(0.0, min(1.0, self.estresse))
        self.competencia_equipe = max(0.0, min(1.0, self.competencia_equipe))