from mesa import Agent

class EstudanteAgent(Agent):
    def __init__(self, model, resiliencia_base):
        super().__init__(model)
        self.resiliencia = self.model.random.uniform(max(0.0, resiliencia_base - 0.2), min(1.0, resiliencia_base + 0.2)) 
        self.competencia_equipe = self.model.random.uniform(0.1, 1.0)
        self.estresse = 0.0 

    def step(self):
        impacto = self.model.dificuldade_cenario * (1.0 - self.resiliencia)
        self.estresse += impacto
        
        outros_estudantes = list(self.model.agents)
        colega = self.random.choice(outros_estudantes)
        
        if colega != self:
            if colega.estresse < 0.5:
                self.estresse -= (colega.competencia_equipe * 0.15)
                self.competencia_equipe += 0.02 
            else:
                self.estresse += 0.05
        
        self.estresse = max(0.0, min(1.0, self.estresse))
        self.competencia_equipe = max(0.0, min(1.0, self.competencia_equipe))