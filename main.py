import networkx as nx
import random 
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import traveling_salesman_problem

def generate_complete_graph(num_nodes, weight_range=(1, 100)):
    g = nx.complete_graph(num_nodes)
    for conection, edge in g.edges():
        g.edges[conection, edge]['weight'] = random.randint(*weight_range)
    return g

def plot_graph_step(g, tour, current_node, pos):
    # os parametros são grafico, o que já foi antado (tour), o node que está e a posição
    plt.clf()
    nx.draw(g, pos, with_labels=True, node_color='lightblue', node_size=500)
    path_edges = list(zip(tour, tour[1:]))
    # esse código acima é o caminho/path que fizemos
    nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_nodes(g, pos, nodelist=[current_node], node_color='green',node_size=500)

    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    plt.pause(0.5)
    
def calculate_tour_cost(g, tour):
    return sum(g[tour[i]][tour[i+1]]['weight'] for i in range(len(tour)-1))


def nearest_neihbor_tsp(g, start_node=None):
    if start_node is None:
        start_node = random.choice(list(g.nodes))

    pos = nx.spring_layout(g)
    plt.ion()
    plt.show()

    unvisited_nodes = set(g.nodes)
    unvisited_nodes.remove(start_node)
    tour = [start_node]
    current_node = start_node

    plot_graph_step(g, tour, current_node, pos)

    while unvisited_nodes: 
        next_node = min(unvisited_nodes, key = lambda node: g[current_node][node]['weight'])
        # logica é, vamos pegar os nodes que não foram visitados e aplicar uma função que vai escolher o menor 
        # peso entre os nodes que podem ser próximos
        unvisited_nodes.remove(next_node)
        tour.append(next_node)
        current_node = next_node
        plot_graph_step(g, tour, current_node, pos)

    tour.append(start_node)
    plot_graph_step(g, tour, current_node, pos)
    tour_cost = calculate_tour_cost(g, tour)
    print(f'Contruction tour cost: {tour_cost}')

    plt.ioff()
    plt.show()

if __name__ == '__main__':
    g = generate_complete_graph(5)
    aprox_tour = traveling_salesman_problem(g, cycle=True)
    aprox_tour_cost = calculate_tour_cost(g, aprox_tour)

    print(aprox_tour)
    print(aprox_tour_cost)
    print('Minha Solução')
    nearest_neihbor_tsp(g, start_node=0)