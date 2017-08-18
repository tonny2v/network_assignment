"""
this code demostrates the famous braess paradox in transport economics:
adding new links to the network does not necessarily reduce the social cost
due to traffic congestion
"""

from assignment.solver import *
import matplotlib.pyplot as plt

# solving the traffic assignment problem


def getEquilibrium(G, with_new_link=False):
    if with_new_link:
        # to add or not to add the new link
        G.add_edge('c', 'b', {'length': 2, 'fft': 1 / 100.,
                              'alpha': 0.05, 'beta': 4, 'cap': 500, 'vol': 0, 'type': 'H'})
    sol = fw(G, od_flow, origins, destinations)
    print "the social cost of current network is %s" % network_cost(sol)
    print sol.edges(data=True)

    pos = nx.circular_layout(sol)
    label = nx.get_edge_attributes(sol, 'vol')
    nx.draw(sol, pos, with_labels=True)
    nx.draw_networkx_edge_labels(sol, pos, label)
    return network_cost(sol)

if __name__ == '__main__':
    # specify O-D travel demand: e.g. 500 ppl going from a to d
    origins = ['a']
    destinations = ['d']
    od_flow = {'a': {'d': 500}}

    ##constructing the network graph###
    G = nx.DiGraph()
    ##length, free-flow travel time per unit length, congestion parameter alpha & gamma, road type
    G.add_edge('a', 'b', {'length': 15, 'fft': 1 / 60.,
                          'alpha': 0.05, 'beta': 4, 'cap': 500, 'vol': 0, 'type': 'H'})
    G.add_edge('a', 'c', {'length': 10, 'fft': 1 / 80.,
                          'alpha': 0.05, 'beta': 4, 'cap': 500, 'vol': 0, 'type': 'H'})
    G.add_edge('b', 'd', {'length': 10, 'fft': 1 / 80.,
                          'alpha': 0.05, 'beta': 4, 'cap': 500, 'vol': 0, 'type': 'H'})
    G.add_edge('c', 'd', {'length': 15, 'fft': 1 / 60.,
                          'alpha': 0.05, 'beta': 4, 'cap': 500, 'vol': 0, 'type': 'H'})

    fig = plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(121)
    scost_wo = getEquilibrium(G)
    plt.title('social cost without new link = %s' % scost_wo)
    ax2 = plt.subplot(122)
    scost_w = getEquilibrium(G, True)
    plt.title('social cost with new link  = %s' % scost_w)
    plt.show()
