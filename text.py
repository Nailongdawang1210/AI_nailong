#打开文件
# f = open('她不一样.txt', 'r', encoding='utf-8')
with open('真的爱她.txt', 'w', encoding='utf-8')as f:

#读取文件内容
# try:
    f.write("真的爱她，真的爱她，真的爱她\n")
    f.write("Love\n") 


#关闭文件
# finally:
    # f.close() 
