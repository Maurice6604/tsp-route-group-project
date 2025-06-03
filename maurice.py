
def generate_city_graph(locations, distances):
    G = nx.Graph()
    for i, loc in enumerate(locations):
        G.add_node(i, name=loc)
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            G.add_edge(i, j, weight=distances[i][j])
    return G

def plot_graph_step(G, tour, current_node, pos):
    plt.clf()
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'name'), node_color='lightblue', node_size=500)
    
    if len(tour) > 1:
        path_edges = list(zip(tour[:-1], tour[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='green', node_size=500)

    edge_labels = nx.get_edge_attributes(G, name='weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.pause(0.5)

def visualize_route(G, tour):
    pos = nx.spring_layout(G)
    plt.ion()
    plt.show()
    for i in range(len(tour) - 1):
        plot_graph_step(G, tour, tour[i], pos)
    plot_graph_step(G, tour, tour[0], pos)
    plt.ioff()
    plt.show()

def main():
    api_key = '5b3ce3597851110001cf62483a7ef6b3f2ea4f02b858dce85ab66f4b'  
    client = openrouteservice.Client(key=api_key)
    
    locations = [
        'Nairobi, Kenya',
        'Nyeri, Kenya',
        'Nakuru, Kenya',
        'Laikipia, Kenya',
        'Nandi, Kenya',
        'Meru, Kenya'
    ]
    
    print("Calculating shortest route...")
    shortest_route, shortest_distance = calculate_shortest_route(client, locations)
    
    if shortest_route and shortest_distance is not None:
        print('Shortest route:')
        for location in shortest_route:
            print(location)
        print(f'Total distance: {shortest_distance:.2f} km')

        # Generating and visualizing the graph
        coordinates = [client.pelias_search(place)['features'][0]['geometry']['coordinates'] for place in locations]
        distances = get_distance_matrix(client, coordinates)
        G = generate_city_graph(locations, distances)
        visualize_route(G, [locations.index(loc) for loc in shortest_route])
    else:
        print("Could not calculate the route. Please check your API key and input locations.")

if __name__ == '__main__':
    main()
