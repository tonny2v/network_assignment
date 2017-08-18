from costcal import *

def all_or_nothing(nw, od_flow, origins, destinations):
    """
    all-or-nothing assignment:
    given OD, assigning all traffic to the fastest route
    """
    res = nw.copy()
    nx.set_edge_attributes(res, 'vol', 0)
    for o in origins:
        for d in destinations:
            sp = nx.shortest_path(res, o, d, 'cost')
            for r, s in zip(sp[:-1], sp[1:]):
                res[r][s]['vol'] += od_flow[o][d]
    return res


def msa(nw, od_flow, origins, destinations, tol=10e-5):
    """
    method of successive average (MSA) algorithm
    """
    update_cost(nw)
    nw = all_or_nothing(nw, od_flow, origins, destinations)
    dif = 1

    n = 1
    while dif > tol:
        n += 1
        tmp_nw = nw.copy()
        update_cost(nw)
        potential_nw = all_or_nothing(nw, od_flow, origins, destinations)
        for r, s in nw.edges():
            nw[r][s]['vol'] = nw[r][s]['vol'] + 1. / \
                (n + 1) * (potential_nw[r][s]['vol'] - nw[r][s]['vol'])
        dif = 0
        for r, s in nw.edges():
            dif += (nw[r][s]['vol'] - tmp_nw[r][s]['vol'])**2
        dif = dif**0.5 / sum(nx.get_edge_attributes(tmp_nw, 'vol').values())
    print 'total iteration = %s' % n
    return nw


def fw(nw, od_flow, origins, destinations, tol=10e-5):
    """
    frank-wolf algorithm
    """
    update_cost(nw)
    nw = all_or_nothing(nw, od_flow, origins, destinations)
    dif = 1
    n = 1
    while dif > tol:
        n += 1
        tmp_nw = nw.copy()
        update_cost(nw)
        potential_nw = all_or_nothing(nw, od_flow, origins, destinations)
        step = optimal_step(nw, potential_nw, tol)
        for r, s in nw.edges():
            nw[r][s]['vol'] = nw[r][s]['vol'] + step * \
                (potential_nw[r][s]['vol'] - nw[r][s]['vol'])
        dif = 0
        # print nw['H15']['R15']['vol']
        for r, s in nw.edges():
            dif += (nw[r][s]['vol'] - tmp_nw[r][s]['vol'])**2
        dif = dif**0.5 / sum(nx.get_edge_attributes(tmp_nw, 'vol').values())
    print 'total iteration = %s' % n
    return nw
