import networkx as nx
import numpy as np

def propflow(G, vs, l):
    """
    G Graph (networkx, directed or undirected)
    vs source vertex for whom propflow is to be calculated
    l max length
    
    Implements algorithm described in "New perspectives and Methods in Link Prediction" by Lichtenwalter et al
    """
    
    Found = set()
    Found.add(vs)

    NewSearch = []
    NewSearch.append(vs)

    S = {}
    S[vs] = 1

    for CurrentDegree in range(0, l + 1):
        # print(CurrentDegree)
        # print(NewSearch)

        OldSearch = list(NewSearch)
        NewSearch.clear()

        while len(OldSearch) > 0:
            vi = OldSearch.pop()

            NodeInput = S[vi]
            # print("For " + str(vi) + ", NodeInput is " + str(NodeInput))

            SumOutput = 0
            for vj in G.neighbors(vi):
                SumOutput += G[vi][vj]['weight']
            # print("For " + str(vi) + ", SumOutput is " + str(SumOutput))

            Flow = 0
            for vj in G.neighbors(vi):
                wij = G[vi][vj]['weight']
                Flow = NodeInput * wij * 1.0 / SumOutput
                
                if vj not in S:
                    S[vj] = 0
                S[vj] += Flow
                print("Flow of " + str(vj) + " = " + str(S[vj]))

                if vj not in Found:
                    Found.add(vj)
                    NewSearch.append(vj)

    sum = 0
    for key in S.keys():
        sum += S[key]

    for key in S.keys():
        S[key] /= sum

    return S

def rooted_pagerank_solve(g, node, d):
    """ Returns rooted pagerank vector
    g graph (networkx, directed or undirected)
    node root
    d damping coefficient
    """
    ordered_nodes = sorted(g.nodes())
    root = ordered_nodes.index(node)
    adjecancy = nx.to_numpy_array(g, nodelist = ordered_nodes)
    m = np.copy(adjecancy)

    for i in range(len(g)):
        row_norm = np.linalg.norm(m[i], ord = 1)
        if row_norm != 0:
            m[i] = m[i] / row_norm

    m = m.transpose()

    rootvec = np.zeros(len(g))
    rootvec[root] = 1
    # rootvec = np.ones(len(g))
    # rootvec = rootvec / len(g)

    d = 0.85

    # find steady state vector
    eigenvector = np.linalg.solve(np.identity(len(g)) - d * m, ((1 - d)  * rootvec))
    # first order normalisation- now entries represent probabilities
    eigenvector = eigenvector / np.linalg.norm(eigenvector, ord = 1)

    eigen_dict = {}
    for i in range(len(ordered_nodes)):
        eigen_dict[ordered_nodes[i]] = eigenvector[i]

    return eigen_dict


def rooted_pagerank(g, node, d = 0.85, epsilon = 1e-5):
    """ Returns rooted pagerank vector
    g graph
    node root
    d damping coefficient
    """
    ordered_nodes = sorted(g.nodes())
    root = ordered_nodes.index(node)
    adjecancy = nx.to_numpy_array(g, nodelist = ordered_nodes)
    m = np.copy(adjecancy)

    n = len(g)

    for i in range(len(g)):
        row_norm = np.linalg.norm(m[i], ord = 1)
        if row_norm != 0:
            m[i] = m[i] / row_norm

    m = m.transpose()

    rootvec = np.zeros(len(g))
    rootvec[root] = 1

    d = 0.85

    vect = np.random.rand(n)
    vect = vect / np.linalg.norm(vect, ord = 1)
    last_vect = np.ones(n) * 100 # to ensure that does not hit epsilon randomly in first step

    iterations = 0
    while np.linalg.norm(vect - last_vect, ord = 2) > epsilon:
        last_vect = vect.copy()
        vect = d * np.matmul(m, vect) + (1 - d) * rootvec
        iterations += 1

    eigenvector = vect / np.linalg.norm(vect, ord = 1)

    eigen_dict = {}
    for i in range(len(ordered_nodes)):
        eigen_dict[ordered_nodes[i]] = eigenvector[i]

    return eigen_dict

def adamic_adar(g, root):
    index_dict = {}

    bunch = [(root, node) for node in g.nodes()]

    adamic_op = nx.link_prediction.adamic_adar_index(g, bunch)

    for key in adamic_op.keys():
        index_dict[key[1]] = bunch[(key[0], key[1])]

    return index_dict


