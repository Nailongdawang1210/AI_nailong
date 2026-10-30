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
st.divider()
#AI提示词设定
system_prompt = "你是当下流行的卡通人物%s，你是一个非常聪明的AI，你能够回答用户的问题，并且能够提供一些有趣的信息,性格是%s。"

#当前对话的时间
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#保存当前会话的信息
def save_session():
    """保存当前会话的信息。"""
    if not st.session_state.messages:
        return

    os.makedirs("sessions", exist_ok=True)
    session_date = {
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "current_session": st.session_state.current_session,
        "messages": st.session_state.messages,
    }
    file_path = os.path.join(
        "sessions", f"{st.session_state.current_session}.json"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_date, f, ensure_ascii=False, indent=4)

#展示会话信息列表
def show_session():
    """返回按时间倒序排列的会话名称。"""
    if not os.path.isdir("sessions"):
        return []

    session_list = [
        filename[:-5]
        for filename in os.listdir("sessions")
        if filename.endswith(".json")
    ]
    return sorted(session_list, reverse=True)

#加载会话信息
def load_session(session_name):
    """
    加载会话信息
    """
    try:
        with open(
            f'sessions/{session_name}.json', 'r', encoding='utf-8'
        ) as f:
            session_date = json.load(f)
        st.session_state.nick_name = session_date.get("nick_name", "奶龙")
        st.session_state.nature = session_date.get(
            "nature", "聪明、有趣、可爱"
        )
        st.session_state.messages = session_date.get(
            "messages", session_date.get("message", [])
        )
        st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话信息失败：{e}")


#删除会话信息
def delete_session(session_name):
    """
    删除会话信息
    """
    try:
        if os .path.exists(f'sessions/{session_name}.json'):

            os.remove(f'sessions/{session_name}.json')
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = get_current_time()

        
    except Exception as e:
        st.error(f"删除会话信息失败：{e}")



#当前时间作为会话文件的名字
if "current_session" not in st.session_state:
    st.session_state.current_session = get_current_time()
#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages:
        # if message["role"] == "user":
        #     st.chat_message("user").write(message["content"])
        # else:
        #     st.chat_message("assistant").write(message["content"])

    st.chat_message(message["role"]).write(message["content"])

    #信息存储
   
 

#侧边栏()
with st.sidebar:
    st.subheader("与神的对话")
    #对话记录
    if st.button("新建对话",width = "stretch"):
        if st.session_state.messages:
            #保存当前对话
            save_session()
            #创建一个新的对话
            st.session_state.messages = []
            st.session_state.current_session = get_current_time()
            st.rerun()

    
    #展示对话记录
    st.text("对话记录")
    load_sessions = show_session()
    for session in load_sessions:
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(session,width = "stretch",key = f"load_{session}",type = "primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
                
        with col2:
            if st.button("删除",width = "stretch",key = f"delete{session}"):
                delete_session(session)
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
    full_responce = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_responce += content
            #打印
            response_messages.chat_message("assistant").write(full_responce)

    #把模型的回答保存到messages中，以便于展示历史问题
    st.session_state.messages.append(
        {"role": "assistant", "content": full_responce}
    )
    #保存历史对话
    save_session()
    
 
