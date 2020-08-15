# from igraph import *

def dump_tree(g, tree):

    for node in tree.children():
        edges                    = []
        g.vs[node.id()]["label"] = node.data().label()

        for child in node.children():
            edges.append((node.id(), child.id()))

        g.add_edges(edges)

        dump_tree(g, node)

def print_statement_tree(tree):
    g = Graph(tree.count_nodes() + 1)
    g.vs[0]["label"] = tree.data().label()

    for child in tree.children():
        g.add_edges([(tree.id(), child.id())])

    dump_tree(g, tree)

    layout = g.layout_reingold_tilford(root=[0])
    # plot(g, layout=layout, bbox=(1000, 1000))
    plot(g, layout=layout)
