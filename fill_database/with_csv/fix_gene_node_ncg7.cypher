match (g1:Gene) 
match(g2:Gene) 
where g1.entrezGeneId = g2.entrezGeneId and id(g1) <> id(g2) and g2.ncg7CancerType is not null 
with [g1,g2] as gs
call apoc.refactor.mergeNodes(gs) yield node 
return node