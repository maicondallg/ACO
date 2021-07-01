import plotly.graph_objects as go
import numpy as np


def plot_graficos_comparacao(his, his_gen):
    his_gen = np.array(his_gen)
    his = np.array(his)

    # Plot das médias das 10 iterações do PSO e do AlgGen
    fig = go.Figure(layout=go.Layout(width=800,height=400,
                                     margin=dict(l=5, r=5, t=5, b=5))
                    )
    fig.add_scatter(y=np.mean([his[i][0][10:] for i in range(10)], axis=0), name='Média PSO', line={'color':'red', 'width':0.95})
    fig.add_scatter(y=np.mean([his[i][1][10:] for i in range(10)], axis=0),name='Mínimo PSO', line={'dash': 'dash', 'color':'red', 'width':0.95})
    fig.add_scatter(y=np.mean([his_gen[i][0][10:] for i in range(10)], axis=0),name='Média Alg Gen', line={'color':'blue', 'width':0.95})
    fig.add_scatter(y=np.mean([his_gen[i][1][10:] for i in range(10)], axis=0),name='Mínimo Alg Gen', line={'dash': 'dash', 'color':'blue', 'width':0.95})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.write_image('Figuras/Ex1/Normal.pdf')

    # Plot das da média das 10 iterações do PSO e do Alg Genético transformado por Log
    fig = go.Figure(layout=go.Layout(width=800,height=400,
                                     margin=dict(l=5, r=5, t=5, b=5))
                    )
    fig.add_scatter(y=np.log(np.mean([his[i][0] for i in range(10)], axis=0)), name='Média PSO', line={'color':'red', 'width':0.95})
    fig.add_scatter(y=np.log(np.mean([his[i][1] for i in range(10)], axis=0)),name='Mínimo PSO', line={'dash': 'dash', 'color':'red', 'width':0.95})
    fig.add_scatter(y=np.log(np.mean([his_gen[i][0] for i in range(10)], axis=0)),name='Média Alg Gen', line={'color':'blue', 'width':0.95})
    fig.add_scatter(y=np.log(np.mean([his_gen[i][1] for i in range(10)], axis=0)),name='Mínimo Alg Gen', line={'dash': 'dash', 'color':'blue', 'width':0.95})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.write_image('Figuras/Ex1/Log.pdf')