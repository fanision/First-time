import spacy
import networkx as nx


nlp = spacy.load('en')



text = (
"Remarkably, Sab exhibited a high preference for binding to Btk rather than to other cytoplasmic tyrosine kinases, which suggests a unique role of Sab in the Btk signal transduction pathway."
)


p1 = (25,25)
# p2 = (1,1)
# p3 = (2,2)
# p4 = (3,3)
# p5 = (4,4)
# p6 = (5,5)


parsed = nlp(text)

#print(parsed[p1[0]:p1[1] + 1])
# print(parsed[p2[0]:p2[1] + 1])
# print(parsed[p3[0]:p3[1] + 1])
# print(parsed[p4[0]:p4[1] + 1])
# print(parsed[p5[0]:p5[1] + 1])
# print(parsed[p6[0]:p6[1] + 1])



def parse_tree_to_graph(document: spacy.tokens.doc.Doc) -> nx.DiGraph:
    graph = nx.DiGraph()

    for token in document:
        for child in token.children:
            # add the dependency between parent
            # and child with label "1"
            graph.add_edge(
                token.i, child.i, label=child.dep_,
                direction=1, ent_a=token, ent_b=child
            )
            # add the opposite dependency (e.g., 
            # child to parent, with direction label -1)
            graph.add_edge(
                child.i, token.i, label=child.dep_,
                direction=-1, ent_a=child, ent_b=token
            )

    return graph

def get_entity_head(entity_tokens: spacy.tokens.span.Span, graph: nx.DiGraph) -> int:
    if len(entity_tokens) < 2:
    	return entity_tokens[0].i

    for token in entity_tokens:
    # get direction of all edges from s
        edges_dirs = [graph[token.i][target.i]['direction'] for target in entity_tokens if target.i in graph[token.i]]

    # check if all other terms in the entity
    # has an edge to are children
        if all(map(lambda e: e == 1, edges_dirs)):
            return token.i


def get_nodes_between_entities(ent_a_pos, ent_b_pos, graph):
    """Return the id of nodes between tokens in positions 
    ent_a_pos and ent_b_pos"""
    return nx.shortest_path(graph, ent_a_pos, ent_b_pos)




def get_edges_between_entites(ent_a_pos, ent_b_pos, graph):
    """Return the edges between tokens in position ent_a_pos
    and ent_b_pos"""

    path = nx.shortest_path(graph, ent_a_pos, ent_b_pos)
    edges = [
        (s, t, graph[s][t]['label'], graph[s][t]['direction'])
        for s, t in zip(path, path[1:])
    ]

    return edges





nlp = spacy.load('en')

a="Remarkably, Sab exhibited a high preference for binding to Btk rather than to other cytoplasmic tyrosine kinases, which suggests a unique role of Sab in the Btk signal transduction pathway."

text=("Remarkably, Sab exhibited a high preference for binding to Btk rather than to other cytoplasmic tyrosine kinases, which suggests a unique role of Sab in the Btk signal transduction pathway.")

p1 = (2, 2)
p2 = (25, 25)

parsed = nlp(text)

print(parsed)

dep_graph = parse_tree_to_graph(parsed)


ent1 = parsed[p1[0]:p1[1] + 1]
ent2 = parsed[p2[0]:p2[1] + 1]
# print("xxxx")
# print(ent1)
# print(ent2)
# print(a[12:15])
# print(a[146:149])


ent1_head = get_entity_head(ent1, dep_graph)
print('The head of "{}" is "{}"'.format(ent1, parsed[ent1_head]))

ent2_head = get_entity_head(ent2, dep_graph)
print('The head of "{}" is "{}"'.format(ent2, parsed[ent2_head]))



path = get_edges_between_entites(ent1_head, ent2_head, dep_graph)
# print(path)
path = sorted(path, key=lambda tup: (tup[3], tup[0] * tup[3], tup[1] * tup[3]))
#print(path)

print(' '.join(
    '{}{}{}'.format(parsed[s], '<-' if d > 0 else '->', parsed[t]) 
    for s, t, _, d in path
))























