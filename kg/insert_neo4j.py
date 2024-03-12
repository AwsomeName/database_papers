from py2neo import Graph
from py2neo import Node, Relationship
import json
from tqdm import tqdm

graph = Graph("http://192.168.31.8://7474", auth=("neo4j", 'abc12345'), name="kg_ver_0_1")
print("graph:", graph)

print("process and inserting ... ")
with open("/home/lc/data/all_entities.txt", 'r') as fp:
    for line in tqdm(fp.readlines()):
        line = line.strip()
        e_id, e_info = json.loads(line)
        e_node = Node(
            e_id, 
            name = e_info['name'], 
            full_name = e_info['full_name'],
            spec = e_info['spec'],
            alias_name = e_info['alias_name'],
        )
        del e_info['name']
        del e_info['full_name']
        del e_info['alias_name']
        del e_info['spec']
        for key in e_info:
            e_node[key] = e_info[key]
            
        graph.create(e_node)
        