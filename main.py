import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd
from modelo import SalaDeAulaModel

numero_de_estudantes = 10
passos_simulacao = 25

# 1. Prepara a janela do gráfico e abre espaço em baixo para os sliders
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.3)

# Cria as linhas iniciais (vazias por enquanto)
linha_estresse, = ax.plot([], [], label="Estresse Médio da Turma", color="red", linewidth=2)
linha_competencia, = ax.plot([], [], label="Competência Média (Equipe)", color="blue", linewidth=2)
linha_dificuldade, = ax.plot([], [], label="Dificuldade do Cenário", color="black", linestyle="--")

ax.set_xlim(0, passos_simulacao)
ax.set_ylim(0, 1.1)
ax.set_title("Simulação Interativa: Desenvolvimento de Competências")
ax.set_xlabel("Tempo (Passos)")
ax.set_ylabel("Nível (0.0 a 1.0)")
ax.legend(loc="upper left")
ax.grid(True)

# 2. Define a posição e desenha os Sliders na janela
ax_taxa = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_res = plt.axes([0.2, 0.05, 0.65, 0.03])

# (Eixo, Nome, Valor Mínimo, Valor Máximo, Valor Inicial, Passos)
slider_taxa = Slider(ax_taxa, 'Taxa Dificuldade', 0.01, 0.20, valinit=0.05, valstep=0.01)
slider_res = Slider(ax_res, 'Resiliência Média', 0.1, 1.0, valinit=0.5, valstep=0.1)

# 3. A função que faz a magia acontecer
def atualizar(val):
    # Pega os valores atuais dos sliders
    taxa = slider_taxa.val
    res = slider_res.val

    # Roda a simulação inteira de novo instantaneamente
    modelo = SalaDeAulaModel(numero_de_estudantes, taxa, res)
    for _ in range(passos_simulacao):
        modelo.step()

    # Extrai os novos dados
    dados_modelo = modelo.datacollector.get_model_vars_dataframe()
    dados_agentes = modelo.datacollector.get_agent_vars_dataframe()
    estresse_medio = dados_agentes.groupby("Step")["Estresse"].mean()
    competencia_media = dados_agentes.groupby("Step")["Competencia"].mean()

    # Atualiza as linhas no gráfico
    x = range(passos_simulacao)
    linha_estresse.set_data(x, estresse_medio)
    linha_competencia.set_data(x, competencia_media)
    linha_dificuldade.set_data(x, dados_modelo["Dificuldade"])

    # Pede ao Matplotlib para redesenhar a tela
    fig.canvas.draw_idle()

# 4. Conecta os sliders à nossa função para que ela rode sempre que mexermos neles
slider_taxa.on_changed(atualizar)
slider_res.on_changed(atualizar)

# Roda a função uma vez logo no início para desenhar o primeiro gráfico
atualizar(0)

# Mostra a janela interativa
plt.show()