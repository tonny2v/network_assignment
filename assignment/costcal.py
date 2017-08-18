import networkx as nx

def update_cost(nw):
    for r, s, data in nw.edges(data=True):
        if data['type'] == 'H':
            c = 2400 * (data['fft'] + data['alpha'] * (data['vol'] /
                                                       data['cap']) ** data['beta']) * data['length']
        elif data['type'] == 'R':
            c = 2400 * data['fft'] * data['length']
        elif data['type'] == 'P' or data['type'] == 'PR':
            c = data['cost']
        else:
            c = 0
        nw.add_edge(r, s, cost=c)


def update_path_costs(nw, origins, destinations):
    for o in origins:
        for d in destinations:
            paths = nx.all_simple_paths(nw, o, d, 'cost')
            for path in paths:
                length = 0
                for r, s in zip(path[:-1], path[1:]):
                    length += nw[r][s]['cost']
                if path[1][0] == 'H' and path[-2][0] == 'H':
                    nw.add_node(o, {"mode_cost_H": length})
                elif path[1][0] == 'R' and path[-2][0] == 'R':
                    nw.add_node(o, {"mode_cost_R": length})
                else:
                    nw.add_node(o, {"mode_cost_P": length})


def network_cost(nw):
    res = 0
    for r, s, d in nw.edges(data=True):
        if d['type'] == 'H' or d['type'] == 'R':
            res += d['cost'] * d['vol']
        if d['type'] == 'P':
            pass
            #res += d['vol'] * 300
        if d['type'] == 'PR':
            #res += d['vol'] * 100
            pass
    return res


def fd(nw, potential_nw, step):
    # objective function for finding the optimal step
    res = 0
    tmp_nw = nw.copy()
    for r, s in tmp_nw.edges():
        tmp_nw[r][s]['vol'] = nw[r][s]['vol'] + step * \
            (potential_nw[r][s]['vol'] - nw[r][s]['vol'])
    update_cost(tmp_nw)
    for r, s in tmp_nw.edges():
        res += tmp_nw[r][s]['cost'] * \
            (potential_nw[r][s]['vol'] - nw[r][s]['vol'])
    return res


def optimal_step(nw, potential_nw, tol=10e-5):
    # bisection method to get the optimal step for frank-wolf algorithm
    ub = 1.
    lb = 0.
    x = (ub + lb) / 2
    while ub - lb > 2 * tol:
        if fd(nw, potential_nw, x) <= 0:
            lb = x
        else:
            ub = x
        x = (ub + lb) / 2
    return x
