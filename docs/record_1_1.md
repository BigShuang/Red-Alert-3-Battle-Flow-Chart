## 解决1.1BUG

#### 2020-10-2
- 发现bug：
现象：苏联机场未统计入内，
原因：排查发现是苏联最后一个在建建筑加入失败
深入分析：
mcv的pack和deploy对应出错
mcv structure pas:
1646, 1807, 1907, 2233
正确关系为
1646 pack-> 1775 deploy->
1807 pack-> 1870 deploy->
1888 pack-> 1897 deploy->
1907 pack-> 2321 deploy->
2233
核心在于，这有段展开deploy后无操作然后收起pack的（第三行）
所以1870deploy了1907
从前往后匹配pack和deploy会导致最后一段 2233被中间1897对应到，原因：
从后往前会导致建筑物对应到1897
解决方法，把mcv的pack和deploy和建筑物的绑定一起做，在bind_structures_and_units里面，
而不是在get_json_from_root里面弄