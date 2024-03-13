from py2neo import Graph
from py2neo import Node, Relationship
import json
from tqdm import tqdm
from retrying import retry
import time

# graph = Graph("http://192.168.31.8:7474", auth=("neo4j", 'abc12345'), name="kg_ver_0_1")
# graph = Graph("http://localhost:7474", auth=("neo4j", 'abc12345'), name="kg_ver_0_1")
graph = Graph("http://localhost:7474", password='abc12345', name="neo4j")
print("graph:", graph)

@retry(stop_max_attempt_number=3, wait_fixed=10)
def create_node(e_node):
    graph.create(e_node)


print("process and inserting ... ")
cnt = 0 
with open("/home/lc/data/all_entities.txt", 'r') as fp:
    for line in tqdm(fp.readlines()):
        cnt += 1
        if cnt < 2426:
            continue
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
            if key == "":
                continue
            e_node[key] = e_info[key]
            
        create_node(e_node)
        # graph.create(e_node)
        # break
        