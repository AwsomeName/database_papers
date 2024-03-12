类型-typ,名称-name,编码-ecode,属性-prop,属性值-ppvl,来源-from,标识-uri,ID-id,更新日期-update
实体-node,人物-people,1-1-10-10,name,,string,https://arxiv.org/pdf/,http://192.168.31.8/kg/node/people/,hashid,update
实体-node,机构-inst,1-1-10-11,name,string,https://arxiv.org/pdf/,http://192.168.31.8/kg/node/inst,hashid,update,
实体-node,论文-paper,1-1-10-12,title,string,https://arxiv.org/pdf/,http://192.168.31.8/kg/node/paper,hashid,update,
实体-node,主题-topic,1-2-10-13,name,string,https://arxiv.org/pdf/,http://192.168.31.8/kg/node/topic,hashid,update,
关系-rel,就职-employ,2-1-10-10,Inst,people,node,node,https://arxiv.org/pdf/,http://192.168.31.8/kg/rel/emply,hashid,update,
关系-rel,写作-author,2-1-10-11,Paper,people,node,node,https://arxiv.org/pdf/,http://192.168.31.8/kg/rel/author,hashid,update,
关系-rel,主旨-purpose,2-1-10-12,paper,topic,node,node,https://arxiv.org/pdf/,http://192.168.31.8/kg/rel/purpose,hashid,update,