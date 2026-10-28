import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

#网页页面设置
st.set_page_config(
    page_title="奶龙AI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#大标题
st.title("奶龙AI")
#logo
st.image("logo.png", caption="logo", width=100)
st.write("奶龙AI，一个基于GPT-6的AI伴侣，可以与你进行对话，分享你的快乐和烦恼，帮助你度过每一个孤独的夜晚。")

#侧边栏
st.sidebar.subheader("我的朋友——奶龙")

#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "奶龙"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "聪明、有趣、可爱"

#昵称
nick_name = st.sidebar.text_input("昵称",placeholder="请输入昵称",value= "奶龙")
if nick_name:
     st.session_state.nick_name = nick_name
     
# 性格
nature = st.sidebar.text_input("性格",placeholder="请输入性格",value= "聪明、有趣、可爱") 
if nature:
     st.session_state.nature = nature

#AI提示词设定
system_prompt = "你是当下流行的卡通人物%s，你是一个非常聪明的AI，你能够回答用户的问题，并且能够提供一些有趣的信息,性格是%s。"


#保存当前会话的信息
def save_session():
    # if st.session_state.current_message:
        session_date = {
              "nick_name":st.session_state.nick_name,
              "nature":st.session_state.nature,
              "current_message":datetime.now().strftime("%Y-%m-%d_%H：M：%S"),
              "message":st.session_state.messages
        }
        if not os.path.exists('sessions'):
            os.makedirs('sessions')
        with open(f'sessions/{datetime.now().strftime("%Y-%m-%d_%H：%M：%S")}.json','w',encoding='utf-8') as f:
            json.dump(session_date,f,ensure_ascii=False,indent=4)



#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
for message in st.session_state.messages:
        # if message["role"] == "user":
        #     st.chat_message("user").write(message["content"])
        # else:
        #     st.chat_message("assistant").write(message["content"])

    st.chat_message(message["role"]).write(message["content"])

    #信息存储
    #当前时间作为会话文件的名字
# if "current_message" not in st.session_state:
#         now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         st.session_state.current_message = now
 

#侧边栏()
with st.sidebar:
    st.subheader("与神的对话")
    #对话记录
    if st.button("新建对话",width = "stretch"):
    #保存当前对话
     if st.session_state.messages:
       save_session()
    #创建一个新的对话
       if st.session_state.messages:
         
             
         st.session_state.messages = []
        #  st.session_state.current_message = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #  st.session_state.current_message = st.session_state.current_message
         
        #  save_session()

         st.rerun()

#连接模型
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)
 #消息输入框
prompt = st.chat_input("请输入你的问题")


if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content":  prompt })

#发给大模型的消息
response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt %(st.session_state.nick_name, st.session_state.nature)  },
            *st.session_state.messages
            
        ],
        stream= True,
    )
#流式输出模型的回答相应
response_messages = st.empty()
full_responce = " "
for chunk in response:
        
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        full_responce += content
            #打印
        response_messages.chat_message("assistant").write(full_responce)

#把模型的回答保存到messages中，以便于展示历史问题
st.session_state.messages.append({"role": "assistant", "content": full_responce})
    
 
