# 把各种原始数据，转为实体，以json的格式输出
import json
import hashlib
from tqdm import tqdm


def gen_id(name_str):
    hasher = hashlib.sha256()
    hasher.update(name_str.encode("utf-8"))
    return hasher.hexdigest()

all_entity = {}
print("process input file ...")
cnt = 0
with open("/home/lc/data/ownthink_v2.csv", 'r') as fp:
    for line in tqdm(fp.readlines()):
        cnt += 1
        if cnt == 1:
            continue
        # if cnt > 10:
        #     break
        line = line.strip()
        terms = line.split(",")
        if len(terms) != 3:
            continue
        s, p, o = terms
        
        if len(s.split("[")) > 0:
            name = s.split("[")[0]
            spec = s.replace(name, "")[1:-1]
            full_name = s
        else:
            name = s
            full_name = s
            spec = ""
            
        eid = gen_id(full_name)
        if eid in all_entity:
            if p in ('name', "full_name"):
                p = "alias_name"
            p_info = all_entity[eid].get(p, None)
            if p_info is not None:
                p_info.append(o)
            else:
                all_entity[eid][p] = [o]
        else:
            all_entity[eid] = {}
            all_entity[eid][p] = [o]
            all_entity[eid]["name"] = name
            all_entity[eid]["full_name"] = full_name
            all_entity[eid]["spec"] = spec
            all_entity[eid]["alias_name"] = []

        
# 输出
print("writing entity file ...")
with open("/home/lc/data/all_entities.txt", 'w') as wp:
    for eid in tqdm(all_entity):
        wp.write(json.dumps([eid, all_entity[eid]]) + "\n")       
