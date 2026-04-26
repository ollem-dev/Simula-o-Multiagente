import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd
from modelo import SalaDeAulaModel

numero_de_estudantes = 30
passos_simulacao = 50

fig, ax = plt.subplots(figsize=(12, 7)) 
plt.subplots_adjust(bottom=0.3, right=0.75) 

linha_estresse, = ax.plot([], [], label="Estresse Médio da Turma", color="red", linewidth=2)
linha_competencia, = ax.plot([], [], label="Competência Média", color="blue", linewidth=2)
linha_dificuldade, = ax.plot([], [], label="Dificuldade do Cenário", color="black", linestyle="--")

ax.set_xlim(0, passos_simulacao)
ax.set_ylim(0, 1.1)
ax.set_title("Simulação Interativa: Desenvolvimento de Competências")
ax.set_xlabel("Tempo (Passos)")
ax.set_ylabel("Nível (0.0 a 1.0)")
ax.legend(loc="upper left")
ax.grid(True)

caixa_texto = ax.text(1.05, 0.95, "", transform=ax.transAxes, fontsize=10, 
                      verticalalignment='top', 
                      bbox=dict(boxstyle='round', facecolor='whitesmoke', alpha=0.8, edgecolor='gray'))

ax_taxa = plt.axes([0.15, 0.15, 0.55, 0.03])
ax_res = plt.axes([0.15, 0.05, 0.55, 0.03])

slider_taxa = Slider(ax_taxa, 'Taxa Dificuldade', 0.01, 0.20, valinit=0.02, valstep=0.01)
slider_res = Slider(ax_res, 'Resiliência Média', 0.1, 1.0, valinit=0.8, valstep=0.1)

def atualizar(val):
    taxa = slider_taxa.val
    res = slider_res.val

    modelo = SalaDeAulaModel(numero_de_estudantes, taxa, res, seed=42)
    for _ in range(passos_simulacao):
        modelo.step()

    dados_modelo = modelo.datacollector.get_model_vars_dataframe()
    dados_agentes = modelo.datacollector.get_agent_vars_dataframe()
    
    estresse_medio = dados_agentes.groupby("Step")["Estresse"].mean()
    competencia_media = dados_agentes.groupby("Step")["Competencia"].mean()

    x = range(passos_simulacao)
    linha_estresse.set_data(x, estresse_medio)
    linha_competencia.set_data(x, competencia_media)
    linha_dificuldade.set_data(x, dados_modelo["Dificuldade"])

    estresse_variancia = dados_agentes.groupby("Step")["Estresse"].var()
    var_max = estresse_variancia.max()
    estresse_final = dados_agentes.xs(passos_simulacao - 1, level="Step")["Estresse"]
    
    texto_estatisticas = (
        "ESTATÍSTICAS FINAIS\n"
        "-------------------------------\n"
        f"Variância Máx: {var_max:.4f}\n\n"
        "Distribuição do Estresse:\n"
        f"• Média:   {estresse_final.mean():.1f}\n"
        f"• Mínimo:  {estresse_final.min():.1f}\n"
        f"• Máximo:  {estresse_final.max():.1f}\n"
    )
    caixa_texto.set_text(texto_estatisticas)
    fig.canvas.draw_idle()

slider_taxa.on_changed(atualizar)
slider_res.on_changed(atualizar)

atualizar(0)
plt.show()