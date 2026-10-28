import json
#写入json文件内容

Love = {
    "name":"wangwenjing",
    "hobby":"beaytiful "
}
with open("love.json","w",encoding="utf-8") as f:
    json.dump(Love,f,ensure_ascii=False,indent=2 )

#读取json文件内容
with open("love.json","r",encoding="utf-8") as f:
    love = json.load(f)
    print(love)
    print(type(love))