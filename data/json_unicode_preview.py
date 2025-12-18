import json5

import json
path="../data/json/test.json"
with open(path,'r',encoding='utf-8')as f:
    data=json5.load(f)  #automatically 还原\uXXXX

#看前两条,ensure——ascii="False"用于打印中文
print(json5.dumps(data[:3],ensure_ascii=False,indent=2))

#data的结构应是[[en,zh],[en,zh],……]
print(type(data),len(data),type(data[0]),len(data[0]))