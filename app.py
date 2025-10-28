# streamlit run app_new3.py
import streamlit as st
import pandas as pd
import json
import requests
import os
from pathlib import Path
from PIL import Image, ImageOps
import base64
def render_sidebar():
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 1rem 0;">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin: 0; color: #2c3e50;">📚 网文探索平台</h2>', unsafe_allow_html=True)
        st.markdown('<p style="margin: 0; color: #7f8c8d;">清华大学水木书院秦奕扬</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider-dashed"></div>', unsafe_allow_html=True)
        
        st.markdown('### 功能导航')
        if st.button('首页', use_container_width=True, key='sidebar_home'):
            go_to_home()
        if st.button('网文发展历史', use_container_width=True, key='sidebar_history'):
            go_to_history()
        if st.button('网文类型与书目', use_container_width=True, key='sidebar_categories'):
            go_to_categories()
        if st.button('书荒查询', use_container_width=True, key='sidebar_book_search'):
            go_to_book_search()
        if st.button('与角色对话', use_container_width=True, key='sidebar_character_dialog'):
            go_to_character_dialog()
        if st.button('穿书play', use_container_width=True, key='sidebar_story_mode'):
            go_to_story_mode()
        if st.button('AI带你写小说', use_container_width=True, key='sidebar_writing'):
            go_to_wrting()
        if st.button('我的喜爱小说', use_container_width=True, key='sidebar_my_love'):
            go_to_my_love_novel()
        
        st.markdown('<div class="divider-dashed"></div>', unsafe_allow_html=True)
        
        st.markdown('### API配置')
        api_key = st.text_input(
            "DeepSeek API密钥",
            type="password",
            value=st.session_state.DEEPSEEK_API_KEY,
            placeholder="输入API密钥",
            key='sidebar_api'
        )
        if api_key != st.session_state.DEEPSEEK_API_KEY:
            st.session_state.DEEPSEEK_API_KEY = api_key
            st.success("API密钥已更新！")
        
        st.info("没有API密钥？可以使用共享密钥：\nsk-2a83ebece503432b9eed4becf2478b24")
st.set_page_config(
    page_title="中国网络文学探索平台——(清华大学水木书院秦奕扬)",
    page_icon="📚",
    layout="wide"
)

# 自定义CSS样式 - 增强版（丰富色彩和排版）
st.markdown("""
<style>
    /* 移除全局通配符样式（引发DOM冲突的核心原因） */
    /* 原代码中的 * { margin:0; padding:0; box-sizing:border-box; } 已移除 */
    
    /* 将body样式改为Streamlit根容器.stApp，避免影响全局DOM */
    .stApp {
        background-color: #f8f9fa;
        background-image: 
            radial-gradient(#e9ecef 0.5px, transparent 0.5px),
            radial-gradient(#e9ecef 0.5px, #f8f9fa 0.5px);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
        color: #343a40;
        line-height: 1.6;
    }
    
    /* 标题样式（完全保留） */
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin: 1.5rem 0 2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
        position: relative;
        padding-bottom: 0.8rem;
    }
    
    .main-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #9b59b6, #3498db);
        border-radius: 2px;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #34495e;
        margin: 1.8rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #9b59b6;
        display: inline-block;
        position: relative;
    }
    
    .sub-header::after {
        content: "";
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 40%;
        height: 2px;
        background-color: #3498db;
    }
    
    /* 卡片样式（完全保留） */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 
                    0 4px 6px -2px rgba(0, 0, 0, 0.03);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 4px solid #3498db;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 
                    0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .card-primary {
        border-top-color: #3498db;
    }
    
    .card-secondary {
        border-top-color: #9b59b6;
    }
    
    .card-tertiary {
        border-top-color: #1abc9c;
    }
    
    .card-accent {
        border-top-color: #f39c12;
    }
    
    /* 按钮样式（完全保留） */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .stButton>button:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 
                    0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .btn-primary {
        background-color: #3498db;
        color: white;
    }
    
    .btn-primary:hover {
        background-color: #2980b9;
    }
    
    .btn-secondary {
        background-color: #9b59b6;
        color: white;
    }
    
    .btn-secondary:hover {
        background-color: #8e44ad;
    }
    
    .btn-tertiary {
        background-color: #1abc9c;
        color: white;
    }
    
    .btn-tertiary:hover {
        background-color: #16a085;
    }
    
    .btn-accent {
        background-color: #f39c12;
        color: white;
    }
    
    .btn-accent:hover {
        background-color: #d35400;
    }
    
    /* 输入框样式（完全保留） */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #bdc3c7;
        padding: 0.6rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        background-color: #fdfdfd;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        outline: none;
    }
    
    /* 调整侧边栏样式选择器，避免冲突（核心修改） */
    [data-testid="stSidebar"] .stBlockContainer {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
        background-image: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* 图片样式（完全保留） */
    .image-card {
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .image-card:hover {
        transform: scale(1.03);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* 滚动条样式（完全保留） */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #bdc3c7;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #95a5a6;
    }
    
    /* 动画效果（完全保留） */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    .slide-in {
        animation: slideInLeft 0.5s ease forwards;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* 网格布局优化（完全保留） */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    /* 标签样式（完全保留） */
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .tag-primary {
        background-color: #ebf5fb;
        color: #3498db;
    }
    
    .tag-secondary {
        background-color: #f5eef8;
        color: #9b59b6;
    }
    
    .tag-tertiary {
        background-color: #eafaf1;
        color: #1abc9c;
    }
    
    .tag-accent {
        background-color: #fef5e7;
        color: #f39c12;
    }
    
    .tag:hover {
        transform: translateY(-2px);
    }
    
    /* 分隔线（完全保留） */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #bdc3c7, transparent);
        margin: 2rem 0;
    }
    
    .divider-dashed {
        height: 1px;
        background: linear-gradient(90deg, transparent, #bdc3c7, transparent);
        background-size: 20px 1px;
        background-repeat: repeat-x;
        margin: 2rem 0;
    }
    
    /* 导航栏样式（完全保留） */
    .nav-item {
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background-color: #f1f5f9;
        transform: translateX(5px);
    }
    
    /* 信息框样式（完全保留） */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
        background-color: #ebf5fb;
    }
    
    .warning-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #f39c12;
        background-color: #fef5e7;
    }
    
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #1abc9c;
        background-color: #eafaf1;
    }
    
    /* 小说展示样式（完全保留） */
    .novel-card {
        border-radius: 8px;
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .novel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    /* 进度指示器（完全保留） */
    .progress-step {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #ebf5fb;
        color: #3498db;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 新增：添加背景图片处理函数
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 图片处理函数优化
def add_border(img_path, target_size=(300, 450), color=(255, 255, 255)):
    """添加边框，将图片调整为目标尺寸（不扭曲）"""
    try:
        img = Image.open(img_path)
        # 按比例缩放图片，使其能放入目标尺寸
        img.thumbnail(target_size)
        # 创建目标尺寸的空白画布（白色背景）
        canvas = Image.new('RGB', target_size, color)
        # 计算图片在画布中的位置（居中）
        x = (target_size[0] - img.width) // 2
        y = (target_size[1] - img.height) // 2
        canvas.paste(img, (x, y))
        return canvas
    except Exception as e:
        st.error(f"图片处理错误: {str(e)}")
        return None

# 图片路径
image_paths = [
    "photo/dpcq.png",
    "photo/gmzz.jpg",
    "photo/gs.jpg",
    "photo/kjdtmdl.jpg",
    "photo/srzy.png",
    "photo/smfs.jpg",
    "photo/wbsxs.jpg",
    "photo/wyzslmddjlhhlb.png",
    "photo/wzjsbyxzs.jpg",
    "photo/xtyq.jpg",
    "photo/ysmc.jpg",
    "photo/zsyx.png",
    "photo/zt.png"
]
valid_images = [p for p in image_paths if os.path.exists(p)]

# API调用函数保持不变
def get_deepseek_response(prompt, character_info=None, max_tokens=3000):
    """调用DeepSeek API获取回复"""
    api_key = st.session_state.get("DEEPSEEK_API_KEY", "")
    
    if not api_key:
        return "请先在首页配置DeepSeek API密钥"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    if character_info:
        system_prompt = f"你正在扮演{character_info['name']}，角色设定：{character_info['description']}。性格特点：{character_info['personality']}。请完全融入角色，用角色的口吻和思维方式来回复用户。"
    else:
        system_prompt = "你是一个有帮助的AI助手"
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=180
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API请求失败: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"请求出错: {str(e)}"

def get_book_recommendations(user_preferences):
    """获取书籍推荐（使用DeepSeek）"""
    prompt = f"""
    用户阅读偏好：{user_preferences}
    
    请基于以上偏好，从中国网络文学中推荐3-5本合适的小说。
    请按照以下格式回复：
    
    推荐理由：[简要说明推荐原因]#
    
    推荐书目：
    1. 《书名》- 作者：推荐理由（2-3句话）
    2. 《书名》- 作者：推荐理由（2-3句话）
    3. 《书名》- 作者：推荐理由（2-3句话）
    """
    
    return get_deepseek_response(prompt, max_tokens=800)

def get_new_novel(user_demand):
    '''生成小说（使用DeepSeek）'''
    prompt = f'''
    用户需求的小说的创作信息：{user_demand}

    请基于用户给出的信息，创作出一章合适的小说（1000-2000字左右），每次生成这本小说的其中一章节。
    如果用户第一次没有给出详细的情节，可以自行生成该类型小说的一个新颖故事
    如果用户第一次给出了详细细节，按照用户给出的想法生成小说
    不要让字数超过限制！每次都要把小说每一章完整生成完成
    '''
    return get_deepseek_response(prompt, max_tokens=3000) 

def generate_story_continuation(theme, previous_story, user_choice):
    """生成故事续写（使用DeepSeek）"""
    prompt = f"""
    主题：{theme['name']} - {theme['description']}
    
    之前的故事发展：{previous_story}
    
    用户选择：{user_choice}
    
    请基于以上信息，续写一个有趣的故事片段（200-300字），然后提供4个合理的后续发展选项。
    
    请按照以下格式回复：
    
    【故事续写】
    [这里写故事内容]
    
    【选项】
    A. [选项A内容]
    B. [选项B内容]
    C. [选项C内容]
    D. [选项D内容]
    """
    return get_deepseek_response(prompt, max_tokens=1000)

# 数据加载部分保持不变
default_novel_data = {}
with open("txt/novel_data.json",'r',encoding='utf-8') as file:
    default_novel_data=json.load(file)

default_characters_data = {}
with open('txt/characters_data.json','r',encoding='utf-8') as file:
    default_characters_data = json.load(file)

default_themes_data = {}
with open('txt/themes_data.json','r',encoding='utf-8') as file:
    default_themes_data = json.load(file)

with open('txt/history.txt','r',encoding='utf-8') as file:
    history_text = file.read()

with open('txt/novel.txt','r',encoding='utf-8') as file:
    novel_text = file.read()

# 初始化会话状态
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'category' not in st.session_state:
    st.session_state.category = None
if 'selected_character' not in st.session_state:
    st.session_state.selected_character = None
if 'selected_novel' not in st.session_state:
    st.session_state.selected_novel = None
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = None
if 'story_progress' not in st.session_state:
    st.session_state.story_progress = []
if 'current_story_step' not in st.session_state:
    st.session_state.current_story_step = None
if 'dialog_history' not in st.session_state:
    st.session_state.dialog_history = []
if 'DEEPSEEK_API_KEY' not in st.session_state:
    st.session_state.DEEPSEEK_API_KEY = ""
if 'novel_progress' not in st.session_state:
    st.session_state.novel_progress = ""
if 'writing_prompt' not in st.session_state:
    st.session_state.writing_prompt = ""

# 导航函数保持不变
def go_to_home():
    st.session_state.page = 'home'

def go_to_history():
    st.session_state.page = 'history'

def go_to_categories():
    st.session_state.page = 'categories'

def go_to_book_search():
    st.session_state.page = 'book_search'

def go_to_character_dialog():
    st.session_state.page = 'character_dialog'

def go_to_story_mode():
    st.session_state.page = 'story_mode'

def go_to_my_love_novel():
    st.session_state.page = 'my_love_novel'

def go_to_category(category):
    st.session_state.page = 'category_detail'
    st.session_state.category = category

def go_to_wrting():
    st.session_state.page='write_novel'

def select_novel_for_character(novel_name):
    st.session_state.selected_novel = novel_name
    st.session_state.selected_character = None

def go_to_novel1():
    st.session_state.page = "novel1"
def go_to_novel2():
    st.session_state.page = "novel2"
def go_to_novel3():
    st.session_state.page = "novel3"
def go_to_novel4():
    st.session_state.page = "novel4"
def go_to_novel5():
    st.session_state.page = "novel5"
def go_to_novel6():
    st.session_state.page = "novel6"
def go_to_novel7():
    st.session_state.page = "novel7"
def go_to_novel8():
    st.session_state.page = "novel8"
def go_to_novel9():
    st.session_state.page = "novel9"
def go_to_novel10():
    st.session_state.page = "novel10"
def go_to_novel11():
    st.session_state.page = "novel11"
def go_to_novel12():
    st.session_state.page = "novel12"
def go_to_novel13():
    st.session_state.page = "novel13"
def go_to_novel14():
    st.session_state.page = "novel14"

def select_character(character):
    st.session_state.selected_character = character
    st.session_state.dialog_history = [
        {
            "role": "assistant",
            "content": f"你好！我是{character['name']}，有什么想对我说的吗？"
        }
    ]

def select_theme(theme):
    st.session_state.selected_theme = theme
    st.session_state.story_progress = []
    st.session_state.current_story_step = {
        "text": f"你进入了【{theme['name']}】的世界。{theme['description']} 你的冒险即将开始...",
        "options": [
            "选项A：开始探索这个世界",
            "选项B：寻找这个世界的居民了解情况",
            "选项C：先观察周围环境",
            "选项D：回忆自己是如何来到这里的"
        ]
    }
    st.session_state.story_progress.append(st.session_state.current_story_step)

def choose_story_option(option):
    current_choice = {
        "choice": option,
        "text": f"你选择了：{option}"
    }
    st.session_state.story_progress.append(current_choice)
    
    with st.spinner("正在生成故事发展..."):
        previous_story = "\n".join([
            step.get('text', '') for step in st.session_state.story_progress 
            if 'text' in step
        ])
        
        story_continuation = generate_story_continuation(
            st.session_state.selected_theme,
            previous_story,
            option
        )
        
        if "【故事续写】" in story_continuation and "【选项】" in story_continuation:
            parts = story_continuation.split("【选项】")
            story_text = parts[0].replace("【故事续写】", "").strip()
            options_text = parts[1] if len(parts) > 1 else ""
            
            options = []
            for line in options_text.split('\n'):
                line = line.strip()
                if line.startswith(('A.', 'B.', 'C.', 'D.')):
                    options.append(line)
            
            if not options:
                options = [
                    "选项A：继续沿着当前方向前进",
                    "选项B：尝试另一种方法", 
                    "选项C：与遇到的人物互动",
                    "选项D：探索周围的环境"
                ]
        else:
            story_text = story_continuation
            options = [
                "选项A：继续沿着当前方向前进",
                "选项B：尝试另一种方法",
                "选项C：与遇到的人物互动", 
                "选项D：探索周围的环境"
            ]
        
        st.session_state.current_story_step = {
            "text": story_text,
            "options": options
        }
        st.session_state.story_progress.append(st.session_state.current_story_step)

# 渲染首页 - 优化版
def render_home():
    # 添加页面标题和介绍
    st.markdown('<h1 class="main-header fade-in">中国网络文学探索平台</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 2rem;">—— 清华大学水木书院秦奕扬</p>', unsafe_allow_html=True)
    
    # 首页横幅
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ebf5fb 0%, #f5eef8 100%); 
                    border-radius: 12px; 
                    padding: 2rem; 
                    margin-bottom: 2rem;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <p style="font-size: 1.3rem; color: #2c3e50; margin: 0;">
                探索中国网络文学的魅力，发现属于你的精彩故事
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # API密钥配置 - 优化样式
    with st.container():
        st.subheader("DeepSeek API配置")
        with st.expander("点击展开API配置", expanded=False):
            col_api, col_help = st.columns([3, 1])
            with col_api:
                api_key = st.text_input(
                    "请输入DeepSeek API密钥：",
                    type="password",
                    value=st.session_state.DEEPSEEK_API_KEY,
                    placeholder="在此输入您的DeepSeek API密钥"
                )
                if api_key != st.session_state.DEEPSEEK_API_KEY:
                    st.session_state.DEEPSEEK_API_KEY = api_key
                    st.success("API密钥已更新！")
            with col_help:
                st.info("没有API密钥？可以使用共享密钥：\nsk-2a83ebece503432b9eed4becf2478b24")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 功能导航 - 优化布局和样式
    st.subheader("功能导航")
    # 使用网格布局展示功能卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown('<div class="card card-primary">', unsafe_allow_html=True)
            st.markdown('📜 **中国网文的发展历史**', unsafe_allow_html=True)
            st.write("了解中国网络文学的起源与发展历程，探索网文文化演变")
            if st.button("进入", use_container_width=True, key="history_btn"):
                go_to_history()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card card-secondary">', unsafe_allow_html=True)
            st.markdown('📚 **网文类型与书目**', unsafe_allow_html=True)
            st.write("浏览各类网络文学作品，发现不同流派的经典之作")
            if st.button("进入", use_container_width=True, key="categories_btn"):
                go_to_categories()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="card card-tertiary">', unsafe_allow_html=True)
            st.markdown('🔍 **书荒查询**', unsafe_allow_html=True)
            st.write("输入你的阅读偏好，AI将为你推荐最合适的网络小说")
            if st.button("进入", use_container_width=True, key="search_btn"):
                go_to_book_search()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col1:
        with st.container():
            st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
            st.markdown('💬 **与角色对话**', unsafe_allow_html=True)
            st.write("与你喜爱的小说角色进行互动，体验沉浸式交流")
            if st.button("进入", use_container_width=True, key="dialog_btn"):
                go_to_character_dialog()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card card-primary">', unsafe_allow_html=True)
            st.markdown('🎭 **穿书play**', unsafe_allow_html=True)
            st.write("选择小说主题，开启你的定制化冒险故事")
            if st.button("进入", use_container_width=True, key="story_btn"):
                go_to_story_mode()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="card card-secondary">', unsafe_allow_html=True)
            st.markdown('✍️ **AI带你写小说**', unsafe_allow_html=True)
            st.write("输入创意灵感，AI将协助你创作属于自己的小说")
            if st.button("进入", use_container_width=True, key="writing_btn"):
                go_to_wrting()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 开发者推荐区域
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.container():
       st.subheader("开发者推荐")
       st.markdown('<div class="card card-tertiary">', unsafe_allow_html=True)
       st.markdown("""
    <div class="info-box">
        <p style="margin: 0;"><strong>编者寄语：</strong>作为一个资深小说迷，我精选了一些优质作品推荐给大家，希望你们能在文字的世界中找到属于自己的乐趣。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用网格布局展示推荐小说（带图片）
       cols = st.columns(5)
       recommended = [
        ("我不是戏神", go_to_novel1, "photo/wbsxs.jpg"),  # 第三个参数为图片路径占位符
        ("十日终焉", go_to_novel2, "photo/srzy.png"),
        ("诡秘之主", go_to_novel3, "photo/gmzz.jpg"),
        ("雪中悍刀行", go_to_novel11, "photo/xzhdx.jpg"),
        ("道诡异仙", go_to_novel5, "photo/dgyxOIP-C.png"),
        ("诸神愚戏", go_to_novel6, "photo/zsyx.png"),
        ("斗破苍穹", go_to_novel7, "photo/dpcq.png"),
        ("开局地摊卖大力", go_to_novel8, "photo/kjdtmdl.jpg"),
        ("夜的命名术", go_to_novel9, "photo/ydmms.png"),
        ("遮天", go_to_novel10, "photo/zt.png")
    ]
    
       for i, (name, func, img_path) in enumerate(recommended):
           with cols[i % 5]:
            # 图片位置（使用占位图，实际使用时替换为真实图片路径）
              try:
                # 尝试加载图片，如果不存在则显示占位文本
                st.image(img_path, use_container_width=True, caption=name)
              except:
                # 占位区域，显示提示文本
                st.markdown(f"""
                <div style="background-color: #f0f2f6; height: 150px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                    <span style="color: #64748b;">{name} 图片位置</span>
                </div>
                """, unsafe_allow_html=True)
            
            # 图片下方的跳转按钮
              if st.button(name, use_container_width=True):
                func()
    
       if st.button("查看更多推荐", use_container_width=True):
        go_to_my_love_novel()
       st.markdown('</div>', unsafe_allow_html=True)
    
    # 热门小说封面展示 - 优化布局
       if valid_images:
          st.subheader("热门小说封面展示")
        # 使用网格布局展示图片
          bordered_images = [add_border(p) for p in valid_images if add_border(p) is not None]
        
        # 添加轮播效果的指示
          st.markdown('<p style="color: #7f8c8d; margin-bottom: 1rem;">左右滑动可查看更多</p>', unsafe_allow_html=True)
        
        # 创建一个水平滚动的容器
          st.markdown("""
        <div style="overflow-x: auto; padding: 10px 0; -webkit-overflow-scrolling: touch;">
            <div style="display: flex; gap: 15px; padding: 5px;">
        """, unsafe_allow_html=True)
        
        # 每行显示多个图片，允许水平滚动
          cols = st.columns(len(bordered_images))
          for col, img in zip(cols, bordered_images):
            with col:
                st.image(img, use_container_width=True, caption=f"热门小说 {cols.index(col)+1}")
        
            st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

# 渲染历史页面 - 优化版
def render_history():
    st.markdown('<h1 class="main-header fade-in">中国网文的发展历史</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    with st.container():
        st.markdown('<div class="card card-primary">', unsafe_allow_html=True)
        # 添加目录导航卡片
        with st.expander("历史时期导航", expanded=True):
            st.markdown("""
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                <a href="#起源阶段" style="text-decoration: none; padding: 8px 15px; background-color: #ebf5fb; color: #3498db; border-radius: 20px; font-size: 0.9rem;">起源阶段</a>
                <a href="#发展阶段" style="text-decoration: none; padding: 8px 15px; background-color: #ebf5fb; color: #3498db; border-radius: 20px; font-size: 0.9rem;">发展阶段</a>
                <a href="#繁荣阶段" style="text-decoration: none; padding: 8px 15px; background-color: #ebf5fb; color: #3498db; border-radius: 20px; font-size: 0.9rem;">繁荣阶段</a>
                <a href="#多元化阶段" style="text-decoration: none; padding: 8px 15px; background-color: #ebf5fb; color: #3498db; border-radius: 20px; font-size: 0.9rem;">多元化阶段</a>
            </div>
            """, unsafe_allow_html=True)
        
        # 优化文本显示格式，添加装饰元素
        st.markdown("""
        <div style="padding: 1rem; line-height: 1.8;">
        """ + history_text.replace(
            "一、", "## 一、<span id='起源阶段'></span>").replace(
            "二、", "## 二、<span id='发展阶段'></span>").replace(
            "三、", "## 三、<span id='繁荣阶段'></span>").replace(
            "四、", "## 四、<span id='多元化阶段'></span>")
        + """
        </div>
        """, unsafe_allow_html=True)
        
        # 添加时间线装饰
        st.markdown("""
        <div style="margin: 2rem 0; padding: 1rem; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
            <h4 style="margin-top: 0; color: #2c3e50;">网文发展时间轴</h4>
            <ul style="padding-left: 1.5rem; margin-bottom: 0;">
                <li>1990年代末-2002年：网络文学萌芽期</li>
                <li>2003-2008年：付费阅读模式形成期</li>
                <li>2009-2014年：移动阅读爆发期</li>
                <li>2015年至今：IP开发黄金期</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染分类页面 - 优化版
def render_categories():
    st.markdown('<h1 class="main-header fade-in">中国网文类型以及各类型书目</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    with st.container():
        st.markdown('<div class="card card-secondary">', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            <p style="margin: 0;">中国网络文学类型丰富多样，以下为主要分类，点击可查看代表作品。每个类型都有其独特的魅力和忠实读者群体。</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 使用网格布局展示分类，带不同颜色标识
        categories = list(default_novel_data.keys())
        cols = st.columns(3)
        
        # 为不同类别分配不同的标签样式
        tag_styles = ['tag-primary', 'tag-secondary', 'tag-tertiary', 'tag-accent']
        
        for i, category in enumerate(categories):
            with cols[i % 3]:
                # 循环使用不同的标签样式
                tag_style = tag_styles[i % len(tag_styles)]
                st.markdown(f'<div class="tag {tag_style}">{category}</div>', unsafe_allow_html=True)
                if st.button(
                    f"查看 {len(default_novel_data[category])} 本作品", 
                    use_container_width=True,
                    key=f"category_btn_{category}"  # 添加唯一key，使用分类名称作为标识
):
                    go_to_category(category)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染分类详情页面 - 优化版
def render_category_detail():
    category = st.session_state.category
    if not category or category not in default_novel_data:
        go_to_categories()
        return
    
    st.markdown(f'<h1 class="main-header fade-in">{category}类网文小说</h1>', unsafe_allow_html=True)
    col_back, col_info = st.columns([1, 5])
    with col_back:
        if st.button("返回类型列表"):
            go_to_categories()
    with col_info:
        st.markdown(f"""
        <div class="success-box">
            <p style="margin: 0;">本类别共收录 <strong>{len(default_novel_data[category])}</strong> 本经典小说，点击展开可查看详细信息</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card card-secondary">', unsafe_allow_html=True)
        # 高级搜索功能卡片
        st.markdown('<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_term = st.text_input("搜索本类别小说：")
        with col_filter:
            status_filter = st.selectbox("状态筛选：", ["全部", "已完结", "连载中"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 过滤小说
        filtered_novels = default_novel_data[category]
        if search_term:
            search_term = search_term.lower()
            filtered_novels = [
                novel for novel in filtered_novels 
                if search_term in novel['title'].lower() or 
                   search_term in novel['author'].lower() or
                   any(search_term in tag.lower() for tag in novel['tags'])
            ]
        
        if status_filter != "全部":
            filtered_novels = [
                novel for novel in filtered_novels 
                if novel['status'] == status_filter
            ]
        
        st.subheader(f"《{category}》类小说列表（{len(filtered_novels)}本）：")
        
        # 分页显示
        novels_per_page = 6
        total_pages = (len(filtered_novels) + novels_per_page - 1) // novels_per_page
        page = st.select_slider("选择页码", options=range(1, total_pages+1), value=1)
        
        start_idx = (page - 1) * novels_per_page
        end_idx = start_idx + novels_per_page
        current_novels = filtered_novels[start_idx:end_idx]
        
        # 以卡片形式展示小说
        for i, novel in enumerate(current_novels, start=start_idx+1):
            status_label = "连载中" if novel['status'] == "连载中" else "已完结"
            status_color = "#e74c3c" if status_label == "连载中" else "#27ae60"
            status_bg = "#fdedeb" if status_label == "连载中" else "#eafaf1"
            
            with st.expander(f"{i}. 《{novel['title']}》- {novel['author']}"):
    # 渲染带HTML样式的标题
                st.markdown(
                    f"{i}. 《{novel['title']}》- {novel['author']} <span style='background-color:{status_bg}; color:{status_color}; padding:2px 8px; border-radius:12px; font-size:0.8rem;'>{status_label}</span>",
                    unsafe_allow_html=True
                )
                # 显示标签，使用不同样式
                tag_styles = ['tag-primary', 'tag-secondary', 'tag-tertiary', 'tag-accent']
                for j, tag in enumerate(novel['tags']):
                    tag_style = tag_styles[j % len(tag_styles)]
                    st.markdown(f'<span class="tag {tag_style}">{tag}</span>', unsafe_allow_html=True)
                
                # 显示简介，优化格式
                st.markdown(f"""
                <div style="margin-top: 1rem; line-height: 1.7; text-align: justify;">
                    <strong>简介：</strong>{novel['description']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染书荒查询页面 - 优化版
def render_book_search():
    st.markdown('<h1 class="main-header fade-in">书荒查询</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    # 检查API密钥
    if not st.session_state.DEEPSEEK_API_KEY:
        st.markdown("""
        <div class="warning-box">
            <p style="margin: 0;">请先在首页配置DeepSeek API密钥，否则无法使用AI推荐功能</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    with st.container():
        st.markdown('<div class="card card-tertiary">', unsafe_allow_html=True)
        st.write("请输入您的阅读偏好，AI将为您推荐合适的小说：")
        
        # 提供推荐示例，美化样式
        with st.expander("查看推荐示例", expanded=False):
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                <p><strong>例如：</strong></p>
                <p>1. 我喜欢玄幻类小说，特别是有修炼体系和冒险元素的，类似《斗破苍穹》这样的作品</p>
                <p>2. 想找一些克苏鲁风格的网络小说，带有悬疑和恐怖元素</p>
                <p>3. 有没有轻松搞笑的都市小说，主角有特殊能力的那种？</p>
            </div>
            """, unsafe_allow_html=True)
        
        # AI对话框界面，美化表单
        with st.form("book_recommendation_form"):
            st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
            user_input = st.text_area(
                "请描述您喜欢的小说类型、情节、风格或您最近喜欢的作品：",
                placeholder="例如：我喜欢玄幻类小说，特别是有修炼体系和冒险元素的...",
                height=120
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("获取推荐", use_container_width=True)
            
            if submitted and user_input:
                with st.spinner("AI正在为您分析并推荐书籍..."):
                    recommendation = get_book_recommendations(user_input)
                    st.success("推荐结果：")
                    # 优化推荐结果显示，添加卡片样式
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 1.2rem; border-radius: 8px; border-left: 4px solid #1abc9c; margin-top: 1rem;">
                        {recommendation.replace("#", "\n\n").replace("\n", "<br>")}
                    </div>
                    """, unsafe_allow_html=True)
            elif submitted:
                st.markdown("""
                <div class="warning-box">
                    <p style="margin: 0;">请输入您的阅读偏好</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 作者原创小说展示
        st.subheader('作者原创小说展示：《渎神》前几章')
        # 优化小说展示格式，添加阅读体验
        with st.expander("点击阅读", expanded=False):
            st.markdown(f"""
            <div style="background-color: #fdfdfd; padding: 2rem; border-radius: 8px; line-height: 1.8; font-size: 1.05rem; text-align: justify; max-width: 800px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
                {novel_text.replace("\n", "<br><br>")}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染与角色对话页面 - 优化版
def render_character_dialog():
    st.markdown('<h1 class="main-header fade-in">与角色对话</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    # 检查API密钥
    if not st.session_state.DEEPSEEK_API_KEY:
        st.markdown("""
        <div class="warning-box">
            <p style="margin: 0;">请先在首页配置DeepSeek API密钥，否则无法使用角色对话功能</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    with st.container():
        st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
        # 如果还没有选择小说
        if not st.session_state.selected_novel:
            st.write("请选择一部小说：")
            novels = list(default_characters_data.keys())
            
            # 使用网格布局展示小说选择，带图标
            cols = st.columns(2)
            for i, novel in enumerate(novels):
                with cols[i % 2]:
                    # 添加小说选择卡片样式
                    st.markdown(f"""
                    <div style="background-color: #fef5e7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; transition: all 0.2s ease;">
                        <p style="margin: 0 0 0.5rem 0; font-weight: 500;">📖 {novel}</p>
                    """, unsafe_allow_html=True)
                    if st.button(f"选择《{novel}》", use_container_width=True):
                        select_novel_for_character(novel)
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # 如果还没有选择角色
        if not st.session_state.selected_character:
            st.write(f"您选择了《{st.session_state.selected_novel}》，请选择一个角色：")
            characters = default_characters_data[st.session_state.selected_novel]
            
            for character in characters:
                # 角色卡片样式
                with st.expander(f"👤 {character['name']}", expanded=False):
                    st.markdown(f"""
                    <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                        <div style="flex: 1; background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                            <p><strong>简介：</strong>{character['description']}</p>
                        </div>
                        <div style="flex: 1; background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                            <p><strong>性格：</strong>{character['personality']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"与{character['name']}对话", use_container_width=True):
                        select_character(character)
            
            if st.button("返回选择其他小说", use_container_width=True):
                st.session_state.selected_novel = None
                st.session_state.selected_character = None
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # 已选择角色，显示对话界面
        character = st.session_state.selected_character
        st.subheader(f"与《{st.session_state.selected_novel}》中的{character['name']}对话中...")
        
        # 角色信息卡片
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #f39c12;">
                <p><strong>角色简介：</strong>{character['description']}</p>
            </div>
            <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #9b59b6;">
                <p><strong>性格特点：</strong>{character['personality']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示对话历史，优化样式和滚动体验
        st.markdown('<div style="background-color: #f7fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; max-height: 450px; overflow-y: auto; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
        for message in st.session_state.dialog_history:
            if message["role"] == "user":
                # 用户消息样式
                st.markdown(f'''
                <div style="text-align: right; margin: 0.8rem 0;">
                    <div style="display: inline-block; max-width: 80%;">
                        <span style="font-size: 0.8rem; color: #7f8c8d;">你</span>
                        <div style="background-color: #3498db; color: white; padding: 0.7rem 1rem; border-radius: 18px 18px 4px 18px; margin-top: 4px; display: inline-block; text-align: left;">
                            {message["content"]}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                # 角色消息样式
                st.markdown(f'''
                <div style="text-align: left; margin: 0.8rem 0;">
                    <div style="display: inline-block; max-width: 80%;">
                        <span style="font-size: 0.8rem; color: #7f8c8d;">{character['name']}</span>
                        <div style="background-color: #f1f5f9; color: #2d3748; padding: 0.7rem 1rem; border-radius: 18px 18px 18px 4px; margin-top: 4px; display: inline-block;">
                            {message["content"]}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 输入新消息
        user_message = st.chat_input(f"向{character['name']}发送消息...")
        if user_message:
            # 添加用户消息到历史
            st.session_state.dialog_history.append({
                "role": "user",
                "content": user_message
            })
            
            # 调用DeepSeek API获取角色回复
            with st.spinner(f"{character['name']}正在回复..."):
                ai_response = get_deepseek_response(user_message, character)
                st.session_state.dialog_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
            
            # 刷新页面以显示新消息
            st.rerun()
        
        # 切换角色或小说的按钮，美化样式
        col1, col2 = st.columns(2)
        with col1:
            if st.button("选择其他角色", use_container_width=True):
                st.session_state.selected_character = None
        with col2:
            if st.button("选择其他小说", use_container_width=True):
                st.session_state.selected_novel = None
                st.session_state.selected_character = None
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染穿书play页面 - 优化版
def render_story_mode():
    st.markdown('<h1 class="main-header fade-in">穿书play</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    # 检查API密钥
    if not st.session_state.DEEPSEEK_API_KEY:
        st.markdown("""
        <div class="warning-box">
            <p style="margin: 0;">请先在首页配置DeepSeek API密钥，否则无法使用穿书功能</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    with st.container():
        st.markdown('<div class="card card-primary">', unsafe_allow_html=True)
        # 如果还没有选择主题
        if not st.session_state.selected_theme:
            st.write("请选择一个你感兴趣的小说主题：")
            # 使用网格布局展示主题，带不同颜色
            cols = st.columns(2)
            themes = default_themes_data
            for i, theme in enumerate(themes):
                with cols[i % 2]:
                    # 主题卡片样式
                    with st.expander(f"🎭 {theme['name']}", expanded=False):
                        st.markdown(f"""
                        <div style="background-color: #ebf5fb; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <p>{theme['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"选择【{theme['name']}】", use_container_width=True):
                            select_theme(theme)
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # 显示当前主题和进度
        st.subheader(f"当前主题：{st.session_state.selected_theme['name']}")
        
        # 显示进度指示器
        progress_percent = min(100, len(st.session_state.story_progress) * 10)
        st.progress(progress_percent)
        st.caption(f"故事进度：{len(st.session_state.story_progress)} 步")
        
        # 显示故事进展，优化滚动区域和样式
        st.write("### 故事进展：")
        st.markdown('<div style="background-color: #f7fafc; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; max-height: 350px; overflow-y: auto; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
        for i, step in enumerate(st.session_state.story_progress):
            if "options" in step:  # 故事节点
                st.markdown(f'''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px dashed #e2e8f0;">
                    <span class="progress-step">{i+1}</span>
                    <strong>情节发展：</strong>
                    <p style="margin-top: 0.5rem; line-height: 1.7;">{step['text']}</p>
                </div>
                ''', unsafe_allow_html=True)
            else:  # 选择记录
                st.markdown(f'''
                <div style="margin-bottom: 1rem; padding: 0.8rem; background-color: #f1f5f9; border-radius: 6px;">
                    <span class="progress-step" style="background-color: #f5eef8; color: #9b59b6;">→</span>
                    <strong>你的选择：</strong>
                    <p style="margin-top: 0.3rem;">{step['text']}</p>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示当前步骤和选项，优化选项样式
        if st.session_state.current_story_step:
            st.write("### 请做出选择：")
            options = st.session_state.current_story_step["options"]
            
            cols = st.columns(2)
            for i, option in enumerate(options):
                with cols[i % 2]:
                    # 选项按钮样式
                    st.markdown(f'''
                    <div style="margin-bottom: 1rem;">
                    ''', unsafe_allow_html=True)
                    if st.button(option, use_container_width=True):
                        choose_story_option(option)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # 重新开始或选择其他主题，美化按钮样式
        col1, col2 = st.columns(2)
        with col1:
            if st.button("重新开始这个主题", use_container_width=True):
                select_theme(st.session_state.selected_theme)
        with col2:
            if st.button("选择其他主题", use_container_width=True):
                st.session_state.selected_theme = None
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染写小说页面 - 优化版
def render_write_novel():
    st.markdown('<h1 class="main-header fade-in">AI带你写小说</h1>', unsafe_allow_html=True)
    if st.button("返回首页", use_container_width=True):
        go_to_home()
    
    # 检查API密钥
    if not st.session_state.DEEPSEEK_API_KEY:
        st.markdown("""
        <div class="warning-box">
            <p style="margin: 0;">请先在首页配置DeepSeek API密钥，否则无法使用AI写作功能</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    with st.container():
        st.markdown('<div class="card card-secondary">', unsafe_allow_html=True)
        # 写作指南
        with st.expander("写作指南", expanded=False):
            st.markdown("""
            <div class="info-box">
                <p><strong>如何获得更好的创作结果：</strong></p>
                <ul>
                    <li>提供详细的小说类型（如：玄幻、科幻、都市等）</li>
                    <li>描述主要角色特点和世界观设定</li>
                    <li>说明你希望的故事开端或关键情节</li>
                    <li>可以指定小说的风格（如：轻松搞笑、严肃深沉、悬疑惊悚等）</li>
                </ul>
                <p><strong>示例：</strong>想写一个修仙小说，主角是一个资质平平的门派杂役，但意外获得了一个神秘玉佩，能吸收他人的修为...请写第一章。</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 小说创作表单
        with st.form("novel_writing_form"):
            st.write("请输入你的小说创意或情节要求：")
            user_demand = st.text_area(
                "小说创意：",
                value=st.session_state.writing_prompt,
                placeholder="例如：想写一个穿越到古代的小说，主角是现代的历史学家，带着现代知识在古代生存...",
                height=150
            )
            
            col_submit, col_clear = st.columns([3, 1])
            with col_submit:
                submitted = st.form_submit_button("生成小说章节", use_container_width=True)
            with col_clear:
                clear = st.form_submit_button("清空内容", use_container_width=True)
            
            if clear:
                st.session_state.writing_prompt = ""
                st.session_state.novel_progress = ""
                st.rerun()
            
            if submitted and user_demand:
                st.session_state.writing_prompt = user_demand
                with st.spinner("AI正在创作中..."):
                    novel_chapter = get_new_novel(user_demand)
                    st.session_state.novel_progress = novel_chapter
        
        # 显示创作结果
        if st.session_state.novel_progress:
            st.subheader("生成的小说章节：")
            st.markdown(f"""
            <div style="background-color: #fdfdfd; padding: 2rem; border-radius: 8px; line-height: 1.8; font-size: 1.05rem; text-align: justify; box-shadow: 0 2px 10px rgba(0,0,0,0.03); margin-top: 1rem;">
                {st.session_state.novel_progress.replace("\n", "<br><br>")}
            </div>
            """, unsafe_allow_html=True)
            
            # 继续创作按钮
            col_continue, col_new = st.columns(2)
            with col_continue:
                if st.button("继续写下一章节", use_container_width=True):
                    with st.spinner("AI正在继续创作..."):
                        continuation_prompt = f"{st.session_state.writing_prompt}\n\n已经写了：{st.session_state.novel_progress}\n\n请继续写下一章节，保持风格一致，情节连贯。"
                        next_chapter = get_new_novel(continuation_prompt)
                        st.session_state.novel_progress += "\n\n" + next_chapter
                        st.rerun()
            with col_new:
                if st.button("开始新的创作", use_container_width=True):
                    st.session_state.writing_prompt = ""
                    st.session_state.novel_progress = ""
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# 渲染我喜欢的小说页面 - 优化版
def render_novel1():
    st.title('我不是戏神')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/wbsxs.jpg'
    st.image(photo_path)
    st.subheader('本书作者:三九音域')
    st.markdown("三九音域，番茄小说 签约作者，著作第一本小说《超能：我有一面复刻镜》（已完结），第二本小说《我在精神病院学斩神》（已完结），第三本小说《我不是戏神》（连载中）")
    st.subheader('作品简介:')
    st.markdown('''
赤色流星划过天际，人类文明陷入停滞。
从那天起，人们再也无法制造一枚火箭，一颗核弹，一架飞机，一台汽车……近代科学堆砌而成的文明金字塔轰然坍塌，而灾难，远不止此。
灰色的世界随着赤色流星降临，像是镜面后的鬼魅倒影，将文明世界一点点拖入无序的深渊。
在这个时代，人命渺如尘埃； 在这个时代，人类灿若星辰。
大厦将倾，有人见一戏子屹立文明废墟之上，红帔似血，时笑时哭， 时代的帘幕在缓缓打开，他张开双臂，对着累累众生低语——“好戏……开场。”
 ''')
    st.subheader('神道')
    st.markdown("“传闻大灾变之前，世间共有十八通神大道，道道不同，但随着时代变迁，文明凋零，如今十八通神大道仅剩十四。”")
    st.markdown("“这十四大道分别为——”")
    st.markdown("“书医兵黄青巧弈，戏偶巫力卜盗娼；”")
    st.markdown("“传闻每一条通神大道，都通往一个‘神位’，若是将其全部走完，即可超脱凡尘，登临成神……”")  
    st.subheader('')
    st.markdown("想了解更多，请访问链接：https://baike.baidu.com/item/%E6%88%91%E4%B8%8D%E6%98%AF%E6%88%8F%E7%A5%9E/63558730")
    st.subheader('作品评价：')
    st.markdown('''
**01独特的世界观构建:**
故事始于一颗赤色流星划过天际，随之而来的是人类文明的停滞。在这个末世背景下，作者构建了一个充满诡秘色彩的世界：科学与玄学交织，超能与异术并存。这个世界里，人命渺如尘埃，但又有人类灿若星辰。一位戏子站在文明废墟之上，红帔似血，时笑时哭，预示着一场好戏即将开场。

**02精妙的叙事手法:**
《我不是戏神》最令人称道的是其精妙的叙事手法。作者善于铺梗填坑，每一处看似随意的描写都可能暗藏玄机。正如一位读者所说：“前期埋的梗后面都有对应，常常在章节结束时出现反转。”这种叙事手法让读者在阅读过程中时刻保持紧张感，生怕错过任何一个细节。

**03出色的文笔与逻辑:**
在众多网络小说中，《我不是戏神》的文笔和逻辑性尤为突出。作者没有为了追求爽感而牺牲剧情的合理性，反而通过精心设计的剧情和人物塑造，让读者在阅读过程中既能感受到刺激，又能体会到文学作品的美感。正如一位读者评价的那样：“这作者特色就是很会铺梗填坑，然后剧情诡秘+反转。”

**04热烈的读者反响:**
《我不是戏神》在番茄小说的热度居高不下，成功入选年度巅峰榜TOP10，近百万用户参与评选。在豆瓣上，已经有10人读过，7人想读。读者们普遍认为这是一部值得推荐的作品，有人甚至表示：“这本好看，看到后面了，白银之王线解释很多之前埋的坑。”

如果你正在寻找一部既能让你感受到刺激，又能体会到文学作品美感的小说，那么《我不是戏神》绝对值得一试。它不仅能满足你对爽文的期待，还能让你在阅读过程中体会到文学作品的美感。''')
    video_path='video/wbsxs.mp4'
    st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel2():
    st.title('十日终焉')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/srzy.png'
    st.image(photo_path)
    st.subheader('本书作者:杀虫队队员')
    st.markdown("曾著书：传说管理局")
    st.subheader('作品简介:')
    st.markdown('''《十日终焉》通过精密设计的十日轮回体系，将悬疑推理与人性拷问深度融合。 主线以齐夏的记忆觉醒为脉络，层层揭开终焉之地的血腥规则与历史阴谋，最终在自我牺牲与集体存亡的哲学命题中达到高潮。 背景设定中十二生肖的游戏机制、回响异能的觉醒条件、以及天龙叛变的因果链条，共同构建出一个逻辑自洽的残酷异世界。 作品在生存游戏的外壳下，实质探讨了人类在绝境中的道德抉择与文明存续的代价，成为近年来反乌托邦题材的标杆之作。
                ''')
    st.markdown('''本书讲的是一群普通人被捕入“终焉之地”，进行每十日一次的生死轮回，他们在这里生了死，死了生。想要逃出此地，必须要进行由「十二生肖」设计的死亡游戏。可是在一个又一个十日之后，部分人开始觉醒了超自然能力的故事。''')
    
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E5%8D%81%E6%97%A5%E7%BB%88%E7%84%89/63368747')
    st.subheader('作品评价：')
    st.markdown('''
作为2022年至2024年现象级网络小说，《十日终焉》以“无限流+悬疑智斗”的叙事框架，构建了一个充满绝望与抗争的终焉世界。这部作品既因宏大的世界观和精妙的伏笔设计被奉为“神作候选”，又因后期节奏失衡和人物塑造争议引发两极评价。本文将从设定创新、叙事张力、人物群像及创作争议四方面，剖析其作为“游戏现实主义”力作的价值与不足。

**设定创新：数据库写作下的生存隐喻**

《十日终焉》以“终焉之地”为核心舞台，将十二生肖、生死游戏、轮回记忆等经典元素重构为充满隐喻的生存系统。参与者需通过智斗游戏获取“道”，在十日周期内逃离这个被天龙篡改规则的异界。这种设定既是对传统“无限流”框架的继承，又通过“回响”与“轮回”机制实现了突破：主角齐夏通过保留记忆的无限重生，逐渐揭开终焉之地与“桃源计划”的关联，最终指向对权力规则的反抗。
作品中“游戏”不仅是生存工具，更是现实的镜像投射。如“说谎者”游戏揭示信任危机，“天平游戏”拷问人性善恶，而“生肖游戏”则暗喻社会阶层的固化与倾轧。邵燕君评价其为“游戏现实主义”，认为其通过虚拟世界的极端规则，映射现代人困于系统化生存的集体焦虑。这种将流行文化元素升华为社会批判的尝试，使小说超越了一般爽文的娱乐性，具备寓言性深度。

**叙事张力：环形伏笔与智斗美学的双重奏**

小说的核心魅力在于“烧脑”体验。作者采用“环形叙事”，从开篇密闭房间的“第十人爆头”到后期跨越百章的伏笔回收（如林檎引导众人进入便利店、人蛇的100个问题），形成严密的逻辑闭环。智斗场景如“朔望月”卡牌游戏，融合二十四节气与五行生克，既考验角色推理能力，也挑战读者的思维极限，被读者誉为“封神章节”。
然而，叙事张力在中后期逐渐失衡。随着齐夏觉醒“生生不息”能力，生死轮回的紧迫感被削弱，部分游戏因规则过度复杂而陷入“自说自话”的窠臼。例如“仓颉棋”章节因拖沓的逻辑解释和配角降智化处理，被批评为“画蛇添足”。这种从“智斗博弈”滑向“主角开挂”的转变，暴露了长篇网文维持叙事强度的普遍困境。

**人物群像：神性与人性的撕裂**

群像塑造是《十日终焉》的突出亮点。主角齐夏初登场时兼具“骗子”的狡黠与对妻子的深情，其智谋与脆弱性形成强烈反差。但随着记忆恢复，他逐渐蜕变为近乎全知的“神”，频繁的“霸总语录”和对他人的冷漠态度，使其人性维度被稀释。相较之下，配角反而更具生命力：陈俊南以幽默掩饰自卑，楚天秋在疯狂中坚守救赎初心，肖冉作为“恶的化身”展现极端利己主义的真实逻辑。
女性角色塑造则存在争议。章律师、甜甜等人物虽摆脱了“物化”标签，但其背景故事多围绕身体创伤展开（如性暴力、重男轻女），被指陷入另一种刻板叙事。这种矛盾性折射出男作者在性别议题上的探索与局限。

**创作争议：长篇网文的“破圈”代价**

作为番茄小说“巅峰榜”榜首作品，《十日终焉》的爆火揭示了免费阅读平台对网文生态的重塑。其“不后宫、不套路”的宣言，试图打破下沉市场对“爽文”的固有认知，但超长篇体量（800余章）仍导致节奏问题：前期伏笔密集如“草蛇灰线”，后期填坑时却因仓促收束留下逻辑漏洞（如天龙计划细节不清）。
读者的分化评价亦凸显网文审美的代际差异：老白读者批评其“高开低走”，年轻群体则沉浸于“绝望中寻找希望”的情感共鸣。项蕾指出，这种分化本质是“无限流”类型内在矛盾的体现——既需通过循环结构隐喻现代生存困境，又不得不依赖线性叙事满足阅读爽感。

**在终焉之地窥见网文的可能性**

《十日终焉》的得失，恰是当代网络文学转型的缩影。它以“游戏化叙事”重构现实焦虑，用群像刻画突破类型桎梏，但其对长篇模式的依赖也暴露了商业性与文学性的冲突。正如结局所言“人生再也不会停留在十日之内”，这部作品的价值或许不在于完美无瑕，而在于它证明了：在流量至上的网文江湖，依然有人愿以“笨拙”的伏笔与“不合时宜”的情怀，叩问生存的意义。
对于读者而言，若追求极致的智斗快感和世界观解谜，前中期章节堪称盛宴；若期待人物弧光的完整与叙事密度的始终如一，则需容忍后期的波动。但无论如何，这部让166万人熬夜追更的现象级作品，已然在网文史留下了独特的“回响”。''')
    video_path="video/srzy.mp4"
    st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel3():
    st.title('诡秘之主')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/gmzz.jpg'
    st.image(photo_path)
    st.subheader('本书作者:爱潜水的乌贼')
    st.markdown("爱潜水的乌贼，本名袁野，起点签约作家，阅文集团白金作家，橙瓜见证·网络文学20年十大奇幻作家，百强大神作家，百位行业代表人物。 完本作品有《灭运图录》（原名是《成仙途》）、《奥术神座》《一世之尊》《武道宗师》《诡秘之主》《长夜余火》。 2017年11月，荣获第二届“中华文学基金会茅盾文学新人奖网络文学新人奖”。 2018年5月，荣获第三届“橙瓜网络文学奖”百强大神。")
    st.subheader('作品简介:')
    st.markdown('''《诡秘之主》（Lord of Mysteries），是阅文集团白金作家爱潜水的乌贼创作的西方玄幻类小说 ，共8部，1418章，总计446.52万字 [81]，融汇了克苏鲁风格、西方魔幻元素、第一次工业革命时代风情和蒸汽朋克情怀 [3]，2018年4月1日在起点中文网连载，6月1日上架，2020年5月1日完结。 
《诡秘之主》故事背景设定在“灰雾之上”的神秘大陆，世界历经混沌纪、黑暗纪、灾变纪等纪元，由22条神之途径和9大源质构成力量体系。讲述了主角因“转运仪式”意外进入源堡，伪装成复苏的“愚者”建立塔罗会，通过扮演法消化魔药晋升序列。他穿越至克莱恩·莫雷蒂身上破解廷根惨案，并“死而复生”。化身夏洛克·莫里亚蒂阻止贝克兰德大雾霾。以格尔曼·斯帕罗身份在海上狩猎海盗，换取魔药材料，晋升半神。成功阻止乔治三世成神并揭露“黑皇帝”复活阴谋，与阿蒙在神弃之地“游戏”，最终成为“诡秘之主”的故事。''')
    st.markdown('''在工业革命的浪潮中，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语。从诡秘中醒来，睁眼看见这个世界：
枪械，大炮，巨舰，飞空艇，差分机；魔药，占卜，诅咒，倒吊人，封印物……光明依旧照耀，神秘从未远离，这是一段“愚者”的传说。 
黑铁纪元，七位正统神灵与四大国统治着北大陆。蒸汽与机械的浪潮中，工业化社会迅速发展成形，而在看似平静繁荣的表面下，则是一个神秘扭曲，乃至疯狂的非凡世界。''')
    st.subheader('创作背景:')
    st.markdown('''《诡秘之主》最初的灵感就来自克苏鲁神话体系，而这个神话源自欧美近代，与资本主义上升期的欧美有密切关系，然后作者就自然地选择了维多利亚时代做背景。这个背景下，蒸汽朋克就成为一个很好的、除开神话外的社会构建选择。同时，在考虑具体的物品设定时，又选择了类SCP的形式。
''')
    
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BB/22466085')
    st.subheader('作品评价：')
    st.markdown('''
很久没有看到这么精彩的小说了，又回到了最初看网文的那种澎湃，对未知和纷繁世界的澎湃。作者很明白自己小说的优点，就像他上架感言里说的：22条途径和220种职业，融入了克苏鲁神话和SCP基金会元素和第一次工业革命的风情以及蒸汽朋克的情怀。就是这样神秘的世界让我们踏上了网络小说之旅，但是现在很多作者却迷失在了套路的道路上，这就是我给这本书接近仙草的原因。
另外，写作技法上最令人着迷的就是超大的信息量和叙而不论的克制。信息呈现的安排很抓人，富有探索的激情。少见的草蛇灰线，每个细节都藏着丰富的信息。''')
    st.subheader('综合评价：')
    st.markdown('''
《诡秘之主》无疑是近年来网络文学中现象级的作品，甚至可以说是定义了“网文神作”新高度的里程碑。它成功地将西方克苏鲁神话、维多利亚时代风情、SCP基金会元素与一套严谨如科幻的“魔药晋升体系”完美融合，创造出了一个既瑰丽奇诡又逻辑自洽的幻想世界。

以下是从几个核心维度对其进行的评价：

**一、 超凡的想象力与严谨的世界构建**
独一无二的力量体系： “二十二条神之途径”和“魔药体系”是其最伟大的创举。它不再是简单的等级提升，而是充满了代价、风险和疯狂。

“扮演法”：这一核心设定极具巧思，它让力量的增长与对世界规则的理解、对自我认知的深化紧密结合，充满了哲学意味。“扮演”不是为了表演，而是为了消化和掌控，这种“守则”极大地提升了故事的深度和角色的真实感。

失控风险：时刻存在的失控风险，让每一次晋升都扣人心弦，力量从来不是免费的午餐，这使得故事始终保持着高度的紧张感和合理性。

栩栩如生的世界： 作者爱潜水的乌贼构建了一个堪比史诗奇幻巨著的宏大世界。从鲁恩王国的贝克兰德到海上的狂暴海，从神弃之地到星星高原，每个地区都有独特的历史、文化和信仰。书中对维多利亚时代底层民众的苦难描绘——大雾、污染、贫富差距、童工——赋予了这个世界沉重的真实感，让超凡故事有了坚实的社会根基。

**二、 深刻的人文关怀与精神内核**
这是《诡秘之主》超越绝大多数网络小说的核心所在。

“为所欲为，但勿伤害”：主角克莱恩·莫雷蒂坚守的这条准则，在弱肉强食的网文世界里显得尤为珍贵。他从一个只想保全自己的普通人，在拥有力量后，依然能对底层人民抱有深切的同情与怜悯，这种“人性的锚”是他在疯狂世界中保持自我的关键。

对底层命运的关照：书中花了大量笔墨描绘老科勒、流浪的贫民等小人物的命运。班西港的遭遇、贝克兰德大雾霾事件，不仅仅是推动剧情的背景，更是作者对工业革命时期社会不公的深刻批判。这种悲天悯人的情怀，让作品拥有了震撼人心的力量。

“守护”的主题：无论是值夜者小队对城市的守护，克莱恩对家人朋友的守护，还是最终面对外神时对整个世界的守护，这种积极、正面的价值观贯穿始终，形成了作品温暖的精神底色。

**三、 精妙绝伦的细节与伏笔**
乌贼是“草蛇灰线，伏脉千里”的大师。

细节的真实：从货币体系、社交礼仪、饮食文化到报纸新闻，无数细节共同堆砌出了世界的可信度。

宏大的布局：从故事开篇的“安提哥努斯笔记”，到廷根市的故事，再到贝克兰德的风云变幻，几乎所有看似偶然的事件，最终都被编织进一张跨越千年、涉及神明与命运的巨网中。重读时，会发现几乎每一句对话、每一个物品都可能是一个关键伏笔，这种阅读的惊喜感和成就感无与伦比。

**四、 成功的人物群像塑造**
主角克莱恩/周明瑞：他可能是网文史上最“怂”也最让人有共鸣的主角之一。他的谨慎、他的吐槽、他的贪财（但取之有道）、他对家乡的思念，都让他无比真实。他的成长不是变成冷酷无情的“神”，而是在获得神性的同时，竭力守护着自己的人性。

配角熠熠生辉：无论是“正义”奥黛丽小姐从天真贵族少女成长为洞察人心的心理医生，还是“倒吊人”阿尔杰的挣扎与忠诚，“星星”伦纳德的直率，“月亮”埃姆林的傲娇……塔罗会的每一位成员都有自己的完整故事弧光，他们不是主角的附庸，而是共同成长的伙伴。

**可能存在的争议点（或称“门槛”）**
慢热与高门槛：小说前期节奏相对舒缓，需要读者有耐心去适应其世界观和设定。大量的西方人名、地名和组织名称对部分读者可能构成阅读障碍。

战斗描写：与一些以激烈打斗见长的小说相比，《诡秘》的战斗更侧重于信息差、规则利用和位格压制，可能不够“爽快”，但更具智斗色彩。

情感线薄弱：对于期待传统男女主角感情戏的读者来说，本书几乎可以算是“无CP”，克莱恩的感情更多地倾注给了家人和战友。

**总结**
《诡秘之主》是一部超越了通俗娱乐范畴，具备深刻文学性和思想性的杰作。它不仅仅是一个关于成神的故事，更是一个关于“人”在疯狂、绝望与宏大的命运面前，如何努力保持自我、守护所爱的故事。

它重新定义了网络文学的潜力，证明了网文同样可以拥有复杂的结构、深邃的思想和打动人心的力量。无论从世界构建、设定创新、人物塑造还是人文深度来看，它都无愧于“神作”之名，是每一位奇幻文学爱好者都不容错过的巅峰体验。''')
    st.subheader('诡秘之主中的序列表')
    photo_path='photo/gmzz_xlb2.jpg'
    st.image(photo_path)
    st.markdown('---------------------------------------------------------------------------------------------------------------------------')
    st.title('力量体系')
    st.subheader('**神之途径**')
    st.markdown('''在第一块亵渎石板之后出现。通过服食魔药完成生命层次的晋升，最终成神，这种进化的路径称为神之途径。在地球存在的神之途径共22条。各途径的名称来源于亵渎石板上面记载的魔药名称，一般底层非凡者常用各途径的序列9作为整个途径的代指，见识更广的非凡者则习惯以序列0作为该途径的名称。
在地球存在的22条序列途径，因为最初在地球短暂苏醒而被聚合到地球的途径。
星空外神途径：对于地球二十二条途径之外的超凡途径。从某种意义上来说，序列的划分是符合这个世界底层规则的。''')
    photo_path="photo/gmzz-sztj1.png"
    st.image(photo_path)
    photo_path='photo/gmzz-sztj2.png'
    st.image(photo_path)
    st.subheader('源质')
    st.markdown('''在第二纪，古神们相信，“最初造物主”有遗留一些事物，那或许是TA身体一部分衍化出来的国度，也或许是TA制造出来的东西，这些事物蕴藏“源质”，是成为“旧日”必不可少的部分。''')
    st.markdown('''根据《宿命之环》里愚者所说:源质是象征的集合、权柄的源泉、力量的本源；正常情况下，源质和唯一性一样，不可分割、不能复制、永不损毁。只有“最初造物主”才能撕裂源质，被撕裂的源质可以自我补完。''')
    photo_path='photo/gmzz-yz1.png'
    st.image(photo_path)
    photo_path='photo/gmzz-yz2.png'
    st.image(photo_path)
    photo_path='photo/gmzz-my.png'
    st.image(photo_path)
    st.markdown('---')
    st.markdown('诡秘之主的内容太多，在此无法展示，如果感兴趣，可以访问：https://baike.baidu.com/item/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BB/22466085')
    video_path="video/gmzz.mp4"
    st.video(video_path)
    ########################################################################################################################################################
def render_novel4():
    st.title('神秘复苏')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/smfx.jpg'
    st.image(photo_path)
    st.subheader('本书作者:佛前献花')
    st.markdown("佛前献花是阅文集团旗下起点中文网签约的网络小说作家，截至2025年5月共创作了3部作品，累计创作字数超1000万字，创作天数超过2000天。其作品以悬疑、仙侠题材为主，代表作《神秘复苏》以超自然现象为背景，累计收藏超50万次 ；《天倾之后》为连载中的仙侠类小说，曾登上起点首页推荐。其作品《聊斋大圣人》结合志怪元素，讲述了主角在奇幻世界的冒险经历")
    st.subheader('作品简介:')
    st.markdown('''讲述了一个诡异复苏的世界，杨间依靠自身的智慧和力量，与各种灵异展开激烈斗争，在生死边缘挣扎。在这个世界中有着不同的杀人规律，例如敲门鬼通过敲门声杀人，因脚印重合导致他人死亡。普通人在灵异事件中若能发现的杀人规律也可能存活。驭鬼者通常是被附身的普通人，驾驭能获得其能力，但身体会呈现部分特征，且频繁使用或时间过长都会导致体内复苏。在经历了各种事件，杨间利用自己的力量和智慧，与灵异势力进行的决战，成功击败了所有的灵异势力，终结了灵异时代，并彻底变成了杨戬，他用自己的力量守护人类，为这个世界带来了和平。
         **五浊恶世，地狱已空，灵异复苏，人间如狱。这个世界灵异出现了......那么神又在哪里，求神救世，可世上已无神。**
         **“我叫杨间，当你看到这句话的时候我已经死了......”
一张灵异的纸，一只窥视黑暗的眼睛，这是一个活下来的人经历的故事。**
                ''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E7%A5%9E%E7%A7%98%E5%A4%8D%E8%8B%8F/23574246')
    st.subheader('''作品设定
''')
    st.markdown('**鬼**:无法被杀死，能对付的只有鬼，普通人只能洞察其规律，找到破绽才能活下来。鬼是一种规则之力的化身，只有黄金可以不受鬼的灵异影响，但也会被用蛮力摧毁。')
    st.markdown('**驭鬼者**：驾驭了鬼能使用力量的人被称为驭鬼者。鬼也会逐渐的驾驭人，驭鬼之路大致有四种。')
    st.markdown('---**平衡**：鬼之间能力相互克制产生平衡，延长复苏的时间，但驾驭的越多越难进行平衡。代表人物民国七老。')
    st.markdown('---**死机**：利用规律，让鬼相互对抗导致死机。死机了几乎可以无偿使用的能力而不用担心复苏，寿命与普通人无异，但自身性格仍会受到影响。代表人物童倩。')
    st.markdown('---**异类**：用自己的意识取代鬼的意识，或者转移自己的意识到灵异物品上成为拥有活人记忆的鬼。异类不用担心复苏，也可以在某种范围内无代价使用灵异力量。但异类也有限制，等到鬼的本能完全压制了自身意识时异类就相当于死亡。代表人物杨间、卫景、李乐平、柳三。')
    st.markdown('---**诅咒**：身体为普通人，但是身受诅咒，可以借用力量，但却需要承受一定代价。代表人物王察灵、赵开明。')
    st.markdown('**复苏**:鬼的力量用一次，身体中的鬼就会复苏一分，即使长时间不动用灵异，厉鬼也会逐渐复苏。对于大多数人来说，从驾驭的那一刻起，生命就已进入了倒计时。')
    st.markdown('**鬼域**:在这里距离会扭曲事物会改变，眼前的景象也会改变，所有的一切既是假的也是真的，同时能隔绝外界的一切，之内是一个围绕着鬼运作的世界，因而出现而变化。')
    st.markdown('**危害等级**:以鬼对世界的危害程度各国政府将划分为以下几个级别,危害等级并不能代表恐怖等级。)')
    photo_path='photo/smfs_weixiandengji.png'
    st.image(photo_path)
    # video_path=""
    # st.video(video_path)
##################################################################################################################################################################################################################################################################################################################################################################################################################################################################
def render_novel5():
    st.title('道诡异仙')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/dgyxOIP-C.png'
    st.image(photo_path)
    st.subheader('本书作者:狐尾的笔')
    st.markdown("狐尾的笔，本名胡炜，1991年11月出生于鹰潭，江西余江人，阅文集团白金作家，2022年网络文学榜样作家十二天王之一，代表作品有《道诡异仙》《诡秘地海》《故障乌托邦》《太吾传人响当当》《艾泽拉斯变形大师》《旧域怪诞》等。")
    st.subheader('作品简介:')
    st.markdown('''《道诡异仙》是网络小说作家狐尾的笔创作的玄幻题材网络小说，2021年11月30日首发于起点中文网，2023年5月22日完结 [18-19]。作品创新采用双重世界观设定，通过主角李火旺在精神病院现实与神魔横行的大傩世界之间的认知撕裂，将克苏鲁恐怖元素与道教修仙体系深度融合，创造出具有哲学思辨色彩的东方克系叙事 [4] [13-14]。该作在连载期间长期占据起点平台悬疑品类月票榜首，并于2025年2月成为阅文IP盛典历史上首部同时入选"年度现象级作品"和"20大荣耀IP"的双料得主 [5] [7] [10-11]。其改编3D动画《火旺》2024年登陆哔哩哔哩国创区，凭借独特的视觉美学引发二次创作热潮
                ''')
    st.markdown('''**诡异的天道，异常的仙佛，是真？是假？ 陷入迷惘的李火旺无法分辨。

火爆全网的《道诡异仙》讲了个什么故事？ #道诡异仙 #网文小说 #小说推文
可让他无法分辨的不仅仅只是这些。还有他自己，他病了，病的很重。**''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E9%81%93%E8%AF%A1%E5%BC%82%E4%BB%99/60978835')
    video_path="video/dgyx.mp4"
    st.video(video_path)
    video_path="video/dgyx1.mp4"
    st.video(video_path)
    video_path="video/dgyx2.mp4"
    st.video(video_path)
#################################################################################################################################################################################################################################

def render_novel6():
    st.title('诸神愚戏')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/zsyx.png'
    st.image(photo_path)
    st.subheader('本书作者:一月九十秋')
    st.markdown("一月九十秋，中国网络小说作家，番茄小说旗下作家，代表作品包括《诸神愚戏》《恩赐的游戏》。一月九十秋在番茄小说平台从事文学创作，已完成奇幻题材小说《恩赐的游戏》。2023年连载新作包括《诸神愚戏》及玄幻穿越题材作品《苟在诡异修仙世界经营宗门》，后者属玄幻脑洞类型，截至2023年11月11日更新至第一百二十九章《聚水阵成》，累计创作31.9万字。该作品以召唤玩家振兴宗门的互动情节为核心，包含‘魍魉宗内好风光’等章节内容。")
    st.subheader('作品简介:')
    st.markdown('''《诸神愚戏》是一本由一月九十秋创作的都市高武小说，于2024年2月21日连载于番茄小说，310.4万字。 [1]某个平行世界自诸神降临被无形的空气墙分割为了无数碎片，成为了一款名为信仰游戏的载体，而这个平行世界的人则成为了所谓的玩家。程实就是被分配到了某栋楼的楼顶上，不管他如何尝试都无法离开这个看似正常，但其实被封的死死地独立空间中。
这个世界的人类想要活命就须选择踏入一种命途，信仰其中的某位神明，选择成为战士、法师、牧师、刺客、猎人、歌者六种职业之一。这样他就能开启各种试炼来获得包括食物和水在内的各种生存必需品，以及最关键的超凡力量的提升。每隔一段时间玩家就必须进行一次随机的团体试炼。程实被欺诈之神看中了成为欺诈途径的小丑牧师。而作为背叛命运的代价他的运气就一直很差，而且说出的话就只能是谎言，不过相应的他也获得了特殊的能力，不仅能够伪装成其他途径的牧师，从而获得该途径牧师的特有技能，还能模糊的感应他人是否说谎。每当程实有意或无意的吐槽命运时，总能引起命运和欺诈两位神的额外关注，让自己的运气临时变好或者变得更差，从而为命运和欺诈两位乐子神带来更多的欢乐。
''')
    st.markdown('''
做人有两个原则：
1.从不骗人
2.从不相信任何人说的话，包括自己
“先生，想提醒您，您说的第二点跟第一点冲突了。”
“哪里冲突”
“您既然从不骗人，为何不相信自己说的话呢”
“哦，抱歉，忘了说，没把自己当人。”
...
介绍一下，叫程实，从不骗人的程实。
什么，你没听说过
没关系，你只是还没被骗过。
很快，你就会记得了。
...
书名《诸神愚戏》，其他均为推广。
【神明末世+排位游戏+多命途职业组合+欢乐脑洞+沾点克系+无限流+偏群像】''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E8%AF%B8%E7%A5%9E%E6%84%9A%E6%88%8F/64939970#:~:text=%E3%80%8A%E8%AF%B8%E7%A5%9E%E6%84%9A%E6%88%8F%E3%80%8B%E6%98%AF%E4%B8%80%E6%9C%AC%E7%94%B1%20%E4%B8%80%E6%9C%88%E4%B9%9D%E5%8D%81%E7%A7%8B%20%E5%88%9B%E4%BD%9C%E7%9A%84%E9%83%BD%E5%B8%82%E9%AB%98%E6%AD%A6%E5%B0%8F%E8%AF%B4%EF%BC%8C%E4%BA%8E2024%E5%B9%B42%E6%9C%8821%E6%97%A5%E8%BF%9E%E8%BD%BD%E4%BA%8E,%E7%95%AA%E8%8C%84%E5%B0%8F%E8%AF%B4%EF%BC%8C200.7%E4%B8%87%E5%AD%97%E3%80%82%20%5B1%5D%20%E6%9F%90%E4%B8%AA%E5%B9%B3%E8%A1%8C%E4%B8%96%E7%95%8C%E8%87%AA%E8%AF%B8%E7%A5%9E%E9%99%8D%E4%B8%B4%E8%A2%AB%E6%97%A0%E5%BD%A2%E7%9A%84%E7%A9%BA%E6%B0%94%E5%A2%99%E5%88%86%E5%89%B2%E4%B8%BA%E4%BA%86%E6%97%A0%E6%95%B0%E7%A2%8E%E7%89%87%EF%BC%8C%E6%88%90%E4%B8%BA%E4%BA%86%E4%B8%80%E6%AC%BE%E5%90%8D%E4%B8%BA%E4%BF%A1%E4%BB%B0%E6%B8%B8%E6%88%8F%E7%9A%84%E8%BD%BD%E4%BD%93%EF%BC%8C%E8%80%8C%E8%BF%99%E4%B8%AA%E5%B9%B3%E8%A1%8C%E4%B8%96%E7%95%8C%E7%9A%84%E4%BA%BA%E5%88%99%E6%88%90%E4%B8%BA%E4%BA%86%E6%89%80%E8%B0%93%E7%9A%84%E7%8E%A9%E5%AE%B6%E3%80%82%20%E7%A8%8B%E5%AE%9E%E5%B0%B1%E6%98%AF%E8%A2%AB%E5%88%86%E9%85%8D%E5%88%B0%E4%BA%86%E6%9F%90%E6%A0%8B%E6%A5%BC%E7%9A%84%E6%A5%BC%E9%A1%B6%E4%B8%8A%EF%BC%8C%E4%B8%8D%E7%AE%A1%E4%BB%96%E5%A6%82%E4%BD%95%E5%B0%9D%E8%AF%95%E9%83%BD%E6%97%A0%E6%B3%95%E7%A6%BB%E5%BC%80%E8%BF%99%E4%B8%AA%E7%9C%8B%E4%BC%BC%E6%AD%A3%E5%B8%B8%EF%BC%8C%E4%BD%86%E5%85%B6%E5%AE%9E%E8%A2%AB%E5%B0%81%E7%9A%84%E6%AD%BB%E6%AD%BB%E5%9C%B0%E7%8B%AC%E7%AB%8B%E7%A9%BA%E9%97%B4%E4%B8%AD%E3%80%82')
    st.subheader('诸神愚戏职业表')
    photo_path='photo/zsyx-xingyangbiao.png'
    st.image(photo_path)
    st.markdown('---')
    st.subheader('各职业介绍')
    st.markdown('**杂技演员**:【欺诈】的战士，祂赐予了杂技演员超高的肢体柔韧性和顶尖的身体平衡能力，能够做出各种匪夷所思的肢体动作。')
    st.markdown('**诡术大师**:【欺诈】的法师，模糊事实，变假为真。')
    st.markdown('**受害者**:【欺诈】的刺客，这个群体与其他职业群体完全不同，他们是一群谎言至上的疯子，是一群不可理喻的狂徒，他们有着挑衅一切的狂傲，和不顾死活的勇气。他们善于激怒别人，做事丝毫不留情面，甚至从不担心被打击报复。而让他们敢于做出以上所有举动的底气，便是【欺诈】赐予受害者的唯一特性:致命回赠:当想要杀死的时候你不妨猜猜看，这致命的伤害会不会被我回赠回去。他们可以把自己受到的某一次伤害返还给伤害来源，所以他们杀人从不需要自己动手，全靠敌人的致命一击。')
    st.markdown('**驯兽师**:【欺诈】的猎人，精通兽语，操纵动物，也能化身动物。')
    st.markdown('**小丑**:【欺诈】的牧师，以谎言治愈他人的牧师，正如以假笑博取笑声的小丑，本质如一，殊途同归。')
    st.markdown('**魔术师**:【欺诈】的歌者，在祂的注视下这些歌者们可以将自己骗人的谎言化为一张张带有特殊效果的扑克牌。每当他们骗过一个人后，都会在手里凝结出一张扑克，但这张扑克具体有什么效果就要看魔术师有什么【欺诈】天赋了。其他的歌者为了增幅队友或许需要一展歌喉，但魔术师们更倾向于通过赠予扑克牌来代替歌唱。')
    st.markdown('**今日勇士**:【命运】的战士，【命运】的谕行是掷出命运之骰，而今日勇士能不能成为勇士，全看骰子的点数。当点数为一时被命运抛弃的可怜人将失去全部神力跟普通人一样毫无用处。但当点数为满点时，被命运眷顾的强者将神力盈身，强如推土机一般推平一切。')
    st.markdown('**编剧**:【命运】的法师，可以改写剧本影响故事的走向，也可以通过改写路人”的故事去变相的影响主角的路。')
    st.markdown('**窃命之贼**:【命运】的刺客，专门窃取他人的命运的窃贼，在【命运】的眷佑下，这些【命运】的刺客隐藏在阴影之中不断审视着众生的命运，当碰到他们感兴趣的命运时，他们便会现身窃走这些人的命运，在这段自己看中的命运中临时扮演一回剧本的主角。简单点说，他们可以暂时取代别人的身份。')
    st.markdown('**终末之笔**:【命运】的猎人，一个可以预见猎物命终之地并于此守株待兔的诡秘职业，他现身的地点往往代表着猎物命运的终点，像极了为他人生命篇章描下句点的命运笔触，终末之笔的称谓由此而来。')
    st.markdown('**织命师**:【命运】的牧师，嫁接信仰，缝补命运，织命师关注的并非肉体上的伤痛，也非灵魂上的净化，而是聚焦在目标的命运上，对其命运运缝缝补补，让其由重伤垂死变成轻伤逃生，甚至于无伤幸免。')
    st.markdown('**预言家**:【命运】的歌者，可以通过掷骰子来预见不久后的未来，但也只能看到未来无数条命运线的一根，甚至还有失败的可能。命运永远在变化，谁都不能确定所预见的未来能不能到来。可这不妨碍它能成为一个指引。')
    st.markdown('**镜中人**:【记忆】的战士，一个可以通过铭记对手招式从而快速复制对方战斗体系的“速记’职业。')
    st.markdown('**回忆旅者**：【记忆】的法师，以旅行者的身份穿梭于目标的记忆片段中，不断寻找自己感兴趣的场景和画面，宛如一次快速的旅行。')
    st.markdown('**旧日追猎者**：【记忆】的刺客，可以将刺中的目标放逐到了过去的历史之中，它并不会改变历史，等到目标淹没在历史的巨浪中时就安全了')
    st.markdown('**窥梦游侠**：【记忆】的猎人，能窥视梦境，一般来说在窥梦游侠窥梦之后的第二夜，由于被窥梦的人在【记忆】的影响下回忆起了过去的记忆。')
    st.markdown('**史学家**:【记忆】的歌者，他们擅长记录历史更擅长篡改历史，这是一群被历史学派称赞。因为他们中的很多人喜欢在历史中尽情的。')
    st.markdown('**指针骑士**:【时间】的战士，一个非常善于抓时机空档的真正timing侠，能够迟滞或者是凝固对手的动作，甚至是将一片空间的时间都凝滞下来')
    st.markdown('**时间行者**:【时间】的法师，可以在整点开辟时间战场在其中操纵时间。当布下【时间战场】必须在整点开启它，并将战局和争端结束于另一个整点。如果做不到，将会陷于永恒的时间循环中直到做到为止。但每一次循环都会消解对时间的概念，过度循环会迷失在时间的长河中')
    st.markdown('**另日刺客**:【时间】的刺客，一个把【时间】的推演利用到极致的职业他们可以穿梭于不同的推演未来中，在另一个时空杀死目标，而后将这推演的结果覆写到当下的时空中来。')
    st.markdown('**驯风游侠**:【时间】的猎人【时间】掌握了“速度”，而“速度”又衍生了“风”，所以祂的信徒才会对风有亲和力。而驯风游侠几乎将这种亲和力拉到了最大。他们可以跟随自己的心意化作一阵微风。当然也有可能是肃杀的寒风。作为【时间】的信徒，他们也可以抓住对手在时间长河里留下的影子，并将敌人钉在过往的时间里。当光阴逆流之矢命中过去的敌人时，将会瞬间爆发出时间堆积的伤痛。')
    st.markdown('**遗忘医生**:【时间】的牧师，作为祂的牧师，遗忘医生的治疗技能有两个，一个是回溯状态，用来把身体状态回溯到上一个被记录的整点，一个是加速代谢，大幅加速目标代谢，以时间治愈伤势身体负面状态，正应了那句话时间将治愈一切。')
    st.markdown('**吟游诗人**:【时间】的歌者，这个职业向来以召唤时间长河中的过往英雄而闻名')
    st.markdown('**酋长**:【诞育】的战士，生育能力非常强大的职业。他们的攻击中携带着非常恐怖的致孕能力，能让敌人在受创的同时有几率怀上他们的孩子，而当他们将怀孕的敌人杀死，尸体上的胎儿便会破体而出吞食尸体长大，变成这个部落的新族人，并成为他们的狂热追随者，酋长之名因此而来。')
    st.markdown('**子嗣牧师**:【诞育】的牧师，在祝福或者治疗同伴时往往有概率会使同伴怀孕。怀孕孕育的东西也不一定是什么正经生命体，界门纲目之间随意搭配，外观更是五花八门应有尽有。但是不要小看这意外的受孕，被治疗者身体内每孕育一个新生命，其受到的治疗效果便会增加三分。')
    st.markdown('**借诞之婴**：【诞育】的刺客，可以把自己种进他人肚子里，使他人处于半清醒半受控的状态，还可以从他人的肚中破胎而出。')
    st.markdown('**德鲁伊**:【繁荣】的战士，可以横跨多物种变换形体的尚战职业，输出手段大多生猛，能抗能打可谓全能。')
    st.markdown('**木精灵**:【繁荣】的法师，亲近植物，操纵植物。')
    st.markdown('**死亡编织者**:【死亡】的刺客，在死亡送葬的专属技能下，他们不能像其他刺客职业那样一击即退，而是需要一直潜伏在阴影中，持续不断的制造杀戮。最后再一击收尾。这种持续保持近距离接触的杀局对刺客很不利风险很大。但同样收益很高因为死亡送葬是必中的。')
    st.markdown('**守墓人**:【死亡】的牧师，作为【死亡】的信徒，他们代行祂的意志，既可以让治愈的光辉化作死亡的暗芒，又可以决定接受了自己治疗的目标是否可以死去。他们如同地狱的看门人，凭着自己心意挑选着敬献给祂的祭品。当然本属于祂的祭品不能随意的减少，守墓人每取走一个祭品，就需要为祂补上一个。这也导致守墓人登顶杀人最多的牧师职业，成了真正带去死亡的奶妈。')
    st.markdown('**尖啸伯爵**:【污堕】的战士，【污堕】阵营里最懂制造恐惧和收割恐惧的玩家，他们常以恐惧为食，不断的折磨敌人，在不当人的行径上与某些【战争】的信徒能打个旗鼓相当。而据说被恐惧母树吸收寰宇恐惧后诞下的恐魔，就是尖啸伯爵这个职业的原型。')
    st.markdown('**欲望主宰**:【污堕】的法师，一个可以欲望炮制傀儡的职业。')
    st.markdown('**感官追猎者**:【污堕】的猎人，他们善于放纵自己的欲望，并引导猎物与自己同流，拉扯猎物的神经，折磨猎物的心态，让对方在放纵中迷失自己，在沉沦中丧失抵抗力。')
    st.markdown('**木乃伊**:【腐朽】的战士，他们是少有的守御能力出色的职业，不同于【秩序】战士可以保护全团，他们更注重于自身的防御提升。他们包裹着光鲜亮丽的外衣，而内里，早已腐朽不堪。宛如一具被时间埋葬的木乃伊。')
    st.markdown('**瘟疫枢机**：【腐朽】的法师，一个在【信仰游戏】中堪称AOE之王的职业。瘟疫枢机散播瘟疫的速度非常快，一旦让瘟疫肆意传播下去，哪怕有所应对，得到的结局也只会是数不清的生命朽烂在原地或者撤出合围区域。')
    st.markdown('**凋零祭司**:【腐朽】的牧师，祂的【谕行】是加速腐朽，所以祂的信徒为了完成【谕行】，往往会进行自残。而【腐朽】的神力也在于此，每一个【腐朽】的信徒自身腐朽越快，其获得的神力反馈就越多。他们可以用自己的生命换取队友的生命。他们越自残伤重，队友越恢复迅猛，正因他们的治疗特性，他们也被被众人称之为:换血牧。当然凋零祭司不仅能给人带去治愈也能带去腐朽。')
    st.markdown('**清道夫**:【湮灭】的战士，他们有力量自己去摧毁一切，也乐于去创造毁灭，他们行走在【湮灭】的道路上，顺手就会把自己看到的东西拖入毁灭的深渊，一举一动都像是在替世界清除一切杂质，所以才会被称为清道夫。')
    st.markdown('**烬灭者**:【湮灭】的法师，一个可以抛开世界规则随手抹去现实存在的职业。烬灭者有属于自己的【湮灭】方式。他们会调动[湮灭]之力将视野中选定的区域整片抹去，而这种区域的抹除并不考虑物体的完整性，也就是说在他们攻击之下，现实世界的战场残留往往加狼藉。他们是出了名的团战能手，人数规模一多起来，甚至能把整座城市都从现实中抹掉。')
    st.markdown('**寂灭使徒**：【湮灭】的刺客，举手投足间便能让身前挡路的存在消失。终焉行者:【湮灭】的猎人，拥有名为寂无声箭的恐怖杀箭。他们追踪目标，标记位置，张弓搭弦，而后，再无声的送走猎物。将猎物送往就要崩毁的世界，亦或，送往即将湮灭的时空。')
    st.markdown('**毁灭宣告**:【湮灭】的歌者，他们吟诵毁灭的诗篇，践行【湮灭】的意志，秉持着能摧毁就不放过、能践踏就不饶恕的原则虔诚的向他们的恩主持续不断的敬献着。但他们毕竟是歌者，用来毁灭一切的手段往往是调动别人的毁灭欲并在事后放肆歌颂这湮灭一切的壮举。')
    st.markdown('**铁律骑士**:【秩序】的战士，他们遵行【秩序】的意志，尊重规则，约束自我，是整个游戏里最受欢迎的战友，几乎没有之一，可靠又好用。专属技能【圣光长城】，可召唤一面圣光城墙进行防御。')
    st.markdown('**元素法官**:【秩序】的法师，可以深研并掌控一种元素。【憎恶之怒】在某个纪元被【秩序】囚禁，便成为了祂赐予其座下元素法官的最高威能。只需将囚禁【憎恶之怒】的牢门拉开一瞬，并瞄准某个区域，被压抑了无数时光的怒火便会倾泻而下。说了这么多，无非是想证明一件事，那就是陨石火雨凡人无法可解。')
    st.markdown('**搜查官**：【秩序】的猎人，祂赐予的天赋之一便是识人辨人。只要见过真人、照片或素描，就能牢牢记住目标的样子，获得额外感应。对自己走过的路线有着额外的记忆能力。能够察觉到不正常的因素，把握到不明显的痕迹。当距离足够近时，能侦察感应到与邪恶、混乱、疯狂相关的未做屏蔽的事物。')
    st.markdown('**律者**:【秩序】的歌者，凡【秩序】信徒，都可以通过唱诵相应的“审判歌谣”来使自己“临时颁布”的法律生效。只不过律者是【秩序】的歌者，他们在唱起歌谣时还能施加额外的效果。')
    st.markdown('**博识学者**:【真理】的法师，这个职业是目前所有职业中变种最多的职业，没有之一。博识学者可以选修不同的知识学派，并以此为追求【真理】的基点，衍生出复杂且繁多的变种职业。诸如:造物炼金学系、虚空质能学系、机械工造学、生命延展学系、存在溯源学系等。')
    st.markdown('**暗杀博士**：【真理】的刺客，是所有刺客职业中最懂得传统刺杀的人，非常善于寻找敌人的弱点，从而可以在最合适的时机给予敌人最精准的暗杀。')
    st.markdown('**博闻诗人**:【真理】的歌者，可以把技能书写成册页，随时使用的牛逼职业。')
    st.markdown('**陷阵勇士**：【战争】的战士，虽被称为陷阵勇士，可他们也不一定是真的会陷阵，其中很有可能藏着一些自匿身份的统军之帅，又或是运筹帷幄的狡诈谋士。')
    st.markdown('**隙光铁刺**:【战争】的刺客，一群潜行于战场之中伺机斩将夺旗的影子杀手。擅长使用铁刺，那如细丝般的光线本应无影无形，可剑刃砍在其上时竟真的传来了金铁交击之声，嗡鸣不止，形成将敌人禁锢在原地的隙光陷阱。')
    st.markdown('**督战官**:【战争】的牧师，当有士卒不堪重负败下阵来时，督战官只需将手中的长鞭狠狠的抽在这些败军之卒的身上，便能以治疗代替伤害，让这些伤重的士兵恢复活力，重返战场。简单点说，别人动刀杀人，他们动刀救人。因为当督战官激活天赋后，他的伤害就变成了治疗。')
    st.markdown('**异血同袍**:【混乱】的战士，两军交战时，只要他们想，他们可以是任意一方的成员，以便将战局搅的混乱不堪。')
    st.markdown('**灾祸之源**：【混乱】的法师，手中一根呓语着让人癫狂魔音的长鞭一刻不停的抽在了每个人的灵魂之上，是在场的所有人不受控制的向周围发动无差别攻击')
    st.markdown('**渔夫**:【混乱】的猎人，他们是【混乱】信仰中自身最不混乱的一群人，善于“浑水”摸鱼，更擅长制造“浑水”，喜欢引导他人于“浑水”中撕斗，而后待鹬蚌相争独自得利。')
    st.markdown('**理智蚀者**:【混乱】的牧师，受到【混乱】的影响，理智蚀者的治疗会逐渐消融伤者的理智，直到其理智崩解，拥抱混乱，彻底疯狂。')
    st.markdown('**竖壁骑士**:【痴愚】的战士，竖起真知的高墙，拒绝一切愚昧的闯入。他们在恩主的赐福下，可以凭空砌筑“真知高墙”，创造出让人意想不到的地理优势从而与敌人迂回斡旋。')
    st.markdown('**戏师**:【痴愚】的法师，他们以帷幕记录现场，可以收集一场盛大的剧目，并在需要的场景下重现。')
    st.markdown('**解构之眼**：【痴愚】的刺客，是个很神奇的职业，得益于【痴愚】智慧的庇佑，他们有着远比其他【痴愚】职业更快的解构速度，往往对某个事物观察不久便能直接洞悉其作用和原理。')
    st.markdown('**独奏家**:【痴愚】的歌者，可以让被独奏家曲调影响的生命对指定目标产生赞同感，简单来说就是让某个人的言语和决策变得更有鼓动性和号召力。')
    st.markdown('**默剧大师**：【沉默】的法师，有着对小范围战斗的绝对的统治力，可以控制‘表达’，让他人注意不到默剧大师的存在')
    st.markdown('**偃偶师**:【沉默】的刺客，他们是潜行于阴影中的刺客，是行走于【沉默】中的杀手，但杀人的手段却与寻常杀手不同。偃偶师们会将自己的控偶丝线缠绕在目标身上，然后在对方失语的震惊和无声的恐惧中，将目标变成一具永远不可能再开口说话的偃偶。他们杀掉的不是肉体而是灵魂。')
    st.markdown('**变色龙**:【沉默】的猎人，一个极其善于伪装自己静待猎物的猎人。他们就像真的变色龙一般，总能巧妙的消失于众人视野，隐匿身形，让所有人在不经意间忽略他们的存在，善于制作【沉默】的陷阱，使人五感尽失，从而在最出乎人意料的时机，发起狩猎的一击。')
    st.markdown('**囚徒**:【沉默】的歌者，哪怕是以嗓子吃饭的歌者，在祂的意志指引下，也只能用锁链，代替歌声。可发出声响依旧是低分的表现，当囚徒们愈发理解祂的意志，从而愈发靠近祂的时候，这些“外物”便会被抛弃，并渐渐被“无声的嘶吼”和“寂然的呐喊”所取代。他们的辅助能力不仅限于增幅队友，更多的反而是限制对手。当手铐和脚镣互击而鸣的时候，感受到禁锢曲调的敌人们，往往会陷入束手束脚的境地中，暴露破绽引颈受戮。''')
    st.markdown('---')
    st.subheader('诸神愚戏中的真神')
    st.markdown('【信仰游戏】的发起者，是掌握权柄、超越时间和维度的存在，不会随着【时代】的结束而消亡。')
    st.markdown(' 【欺诈】')
    st.markdown('虚无命途的双胞神之一，虚无的表象。【命运】的胞神、姐姐。与【记忆】对立。获得了【混乱】的权柄。祷词是“不辨真伪，勿论虚实”，【公约】的发起者。【谕行】是欺骗他人。外貌：双眼与【命运】相似，眼白涂满螺旋，瞳孔洒遍星点，但眼角微翘，眼中神光更有活力，更像是一个“人”的眼睛。双手晶莹如玉。 [1]虽然【欺诈】平时毫无顾忌，欺诈他人，但是祂对于【源初】有着深刻的恐惧。')
    st.markdown('【命运】')
    st.markdown('虚无命途的双胞神之一，虚无的本质。【欺诈】的胞神、妹妹。祂洞彻寰宇真实，所知甚多，知晓所有过去和无数未来。与【时间】对立。祷词是“命若繁星，望而不及”。【谕行】是占卜，即投掷“命运之骰”。祂拥有随机、变化、既定等诸多权柄。外貌：双眼冰冷静默，毫无感情，眼白里绘满了迷转的螺旋，眼眸中镌刻着分歧的星点。只与祂对视一眼，便会觉得自己的灵魂被拉扯着涌向无尽的虚无。与【欺诈】不同，【命运】是【源初】的靠近者。')
    st.markdown('【记忆】')
    st.markdown('存在命途的双胞神之一，存在的表象。祂回溯过往，无喜无悲，并忠实记录一切，但不代表着忠实地记录真相。与【欺诈】对立。祷词是“昔我长铭，流光拓影”【谕行】是向祂敬献一段记忆，无论是谁的。外貌：双眼是刻写着沧桑的历史之眸。')
    st.markdown('【时间】')
    st.markdown('存在命途的双胞神之一，存在的本质。祂注视当下，亘古不变。与【命运】对立。祷词是“时光如隙，我亦如风”。【谕行】是精准和守时。外貌：双眼是骇人的黑洞之眸。')
    st.markdown('【秩序】')
    st.markdown('文明命途的第一神，文明的序幕。曾是寰宇的至强者，赢得了第一次【神战】。在进入【欲海】后分裂成三部分 [76-77]，【偏执（秩序）】的权柄被【混乱】夺走，【公正（秩序）】和【恐惧（秩序）】填补了公约，【傲慢（秩序）】被囚禁 [29-31]与【混乱】对立。祷词是“文明火起，秩序长存”。【谕行】是寻找秩序，只有遵循某种条律规则的人，才能得到赐福；而想要接受【秩序】庇佑的人，也必须遵守被找到的秩序。')
    st.markdown('【真理】')
    st.markdown('文明命途的第二神，文明的延续。祂是寰宇规律的合集，是宇宙本质的汇总。与【痴愚】对立。祷词是“洞窥本质，行见真理”。【谕行】有两套，辅助职业需要求知、接受知识，任何未知的规律或者知识都能让【真理】的信徒更加接近“真理”；而输出职业需要传播知识。外貌：双眼闪烁着知识光芒和无穷规律。')
    st.markdown('【战争】')
    st.markdown('文明命途的第三神，文明的终局。曾常伴【秩序】，后来躲藏起来，后被【公约】掣肘，与【秩序】的分裂脱不开关系，攫取部分【秩序】的权柄，【欺诈】认为其实力相当于两个“老骨头”（即【死亡】），计划在时代结束时挑战【源初】与【沉默】对立。祷词是“何以求存，唯血与火”。谕行是纷争。外貌：双眼异瞳，左眼是燃烧的火焰，右眼是滚淌的鲜血。祂甫一睁眼，激昂的乐章便在虚空中奏响，每一个音节都让人心魂激荡，战意沸腾。')
    st.markdown('【混乱】')
    st.markdown('混沌命途的第一神，混沌的序幕。祂是无序的癫狂，也是【秩序】的死敌。祂的意志推崇世界上根本没有规律可言，宇宙的终极就应该是混乱无序的。与【秩序】对立。将【混乱】权柄丢弃，获得了【偏执】的权 [29]并假扮起【秩序】，而【混乱】神殿的【混乱】则是由【欺诈】假扮的。祷词是“虚构规律，寰宇笑谈”。')
    st.markdown('【痴愚】')
    st.markdown('混沌命途的第二神，混沌的延续。祂自认为比【真理】更加接近真理，由于过度接近真理，与世间万物产生了断层式差距，所以祂认为世间的一切其他存在都是痴愚的，自称寰宇第一愚者。根据【死亡】所说，【痴愚】曾非常活跃，因为【源初】【痴愚】转入有人称其失去了权柄，似乎是【公约】出现为了某件事选择放手一搏所致 [44]与【真理】对立。祷词是“生命皆痴，文明皆愚”。【谕行】是鄙夷愚昧，所以祂的信徒无时无刻不在斜眼看人。外貌：双眼是写满了不屑与鄙夷的苍白之眸。')
    st.markdown('【沉默】')
    st.markdown('混沌命途的第三神，混沌的终局。与【战争】对立。祷词是“万物归寂，寰宇无音”。【谕行】是保持沉默，跟随、观察、聆听、思考，唯独不与人交流，活的像独行的僧人。')
    st.markdown('【繁荣】')
    st.markdown('生命命途的第二神。祂是心神的丰茂，崇尚加速更迭，肆意生长，被称为【繁荣之母】。与【腐朽】对立。神国是神荫。祷词是“万物滋生，亦繁亦荣”。【谕行】是“堆积养料，以争繁荣”。祂拥有滋生、无垢、同化、丰沛、生机等诸多权柄。祂想要同化众神，使祂们与祂一样拥抱繁荣，与之共生。最终自杀 [12]，将权柄分给众神。在其他“切片宇宙”中，【繁荣】没有自灭，反而同化了整片寰宇。')
    st.markdown('【死亡】')
    st.markdown('生命命途的第三神，生命的尾声。与【湮灭】对立。神国是鱼骨殿堂。祷词是“灵魂安眠，生命终焉”。曾从程实的诈死中获得启发，窃取了【欺诈】与【记忆】的部分权柄。外貌：一只巨大的头骨，眼窝如黑洞一般。祂的声音犹如深渊地狱中喷涌而出的冷炎，刺骨冰冷。')
    st.markdown('【污堕】')
    st.markdown('沉沦命途的第一神，沉沦的序幕。祂推崇人们释放内心深处的欲望。与【诞育】对立。祷词是“解脱枷锁，直面心欲”。【欲海】的主宰，一直隐藏在【欲海】之中。【欺诈】认为祂并不存在。')
    st.markdown('【腐朽】')
    st.markdown('沉沦命途的第二神，沉沦的高潮。祂是宇宙的终墓。神国是陵墓。祷词是“众生应腐，万物将朽”。谕行】是加速腐朽，往往是自残。【腐朽】的信徒自身腐朽越快，其获得的神力反馈就越多。与【繁荣】对立。为接近【源初】，【腐朽】决定腐朽自我以及信仰，并且给予程实一部分的权柄。在其他“切片宇宙”中，【腐朽】陨落。外貌：载体是一具衰老至极的腐烂巨人。')
    st.markdown('【湮灭】')
    st.markdown('沉沦命途的第三神，沉沦的尾声。祂是生灵的崩毁，坚信生命终将消失，宇宙难逃毁灭，一切都将逝去，最终归于寂灭。祂的信徒们认为世界运转的意义就是为了等待最后的审判，然后在祂的注视下，崩为尘埃。与【死亡】对立。祷词是“于无中生，于寂中灭”。 [81]【谕行】就是湮灭。外貌：双眼为黑色，绝类【虚无】。')
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel7():
    st.title('斗破苍穹')
    st.markdown("**玄幻经典神作！**")
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/dpcq.png'
    st.image(photo_path)
    st.subheader('本书作者:天蚕土豆')
    st.markdown('''天蚕土豆，本名李虎。1989年12月28日出生于四川，中国内地网络小说作家、浙江省网络作家协会副主席，中国作协第十届全国委员会委员。''')
    st.markdown('''2008年4月，天蚕土豆在起点中文网创作处女作《魔兽剑圣异界纵横》 [14]；5月成为起点中文网签约作家。 [30]2009年4月，创作《斗破苍穹》，该书在起点中文网总点击破亿 [1]，入选国家图书馆永久典藏网络小说 [28]，天蚕土豆凭借此书成为2009年起点中文网白金作家。 [32]2011年7月，推出《武动乾坤》，该作品在大陆、台湾及亚洲多地的游戏改编权于2012年3月售出 [6]。2013年，创作《大主宰》 [2]，连载期间该书忠实粉丝超过2000万，在小说类网站推荐总数超过200万次。 [21]2016年7月，成立上海未天文化传媒有限公司。 [27]2017年9月，荣登橙瓜《网文圈》杂志第8期封面人物。 [30]2019年，创作《元尊》 [22]，该书拥有英语、印尼语、越南语、西班牙语等多个语言版本。 [45]2021年4月，天蚕土豆创作玄幻小说《万相之王》。 [9]2022年7月，担任编剧的动漫《斗破苍穹 年番1》播出。 [39]次年，担任编剧的电影《斗破苍穹·觉醒》《斗破苍穹·止戈》先后播出。 [52-53]2025年8月，担任编剧的动漫《斗破苍穹 年番4》播出； [39]9月，参加2025中国国际网络文学周。 [25]
2014年4月《斗破苍穹前传之药老传奇》上市后，获中国网络作家富豪榜第三名。 [32]2018年，入选福布斯亚洲30位30岁以下精英榜 [13]，并获第三届“橙瓜网络文学奖”名人堂奖。 [38]2019年，入选2019年宣传思想文化青年英才。 [12]次年，入选橙瓜见证·网络文学20年十大玄幻作家，百强大神作家，百位行业人物。''') 
    st.subheader('作品简介:')
    st.markdown('''讲述了天才少年萧炎在创造了家族空前绝后的修炼纪录后突然成了废人，种种打击接踵而至。就在他即将绝望的时候，一缕灵魂从他手上的戒指里浮现，一扇全新的大门在面前开启，经过艰苦修炼最终成就辉煌的故事。
这里是属于斗气的世界，没有花俏艳丽的魔法，有的，仅仅是繁衍到巅峰的斗气！''')
    st.markdown('''主角萧炎，原是萧家历史上空前绝后的斗气修炼天才，4岁就开始修炼斗之气，10岁拥有了九段斗之气，11岁突破十段斗之气，一跃成为家族百年来最年轻的斗者。然而在11岁那年，他却“丧失”了修炼能力，并且斗气逐渐减少，直至三段斗之气。整整三年多时间，家族冷落，旁人轻视，被未婚妻退婚……种种打击接踵而至。''')
    st.markdown('''就在他即将绝望的时候，一缕灵魂从他手上的戒指里浮现，一扇全新的大门在面前开启！萧炎重新成为家族年轻一辈中的佼佼者，受到众人的仰慕，他却不满足于此。为了一雪退婚带来的耻辱，萧炎来到了魔兽山脉，在药老的帮助下，为了进一步提升自己的修为，在魔兽山脉，他结识了小医仙，云芝（云岚宗宗主云韵）等人，他发现自己面向的世界更加宽广了。''')
    st.markdown('''三十年河东，三十年河西，莫欺少年穷！ 年仅15岁的萧家废物，于此地，立下了誓言，从今以后便一步步走向斗气大陆巅峰！
经历了一系列的磨练：收异火，寻宝物，炼丹药，斗魂族。
最终成为斗帝，为解开斗帝失踪之谜而前往大千世界''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9/54134')


                
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel8():
    st.title('开局地摊卖大力')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/kjdtmdl.jpg'
    st.image(photo_path)
    st.subheader('本书作者:弈青锋')
    st.markdown("弈青锋是活跃于番茄小说网的网络小说作家，以诙谐幽默与热血励志结合的作品风格见长。其代表作《开局地摊卖大力》在2021-2023年连续2年保持每日阅读人数百万以上，改编动画于2023年亮相B站国创发布会 。他出身普通工人家庭，曾从事电焊工等职业，通过坚持创作从“扑街作家”逆袭为平台头部作者。2023年入选中国网络文学影响力榜新人榜 ，2024年获得番茄小说网金番作家称号 ，作品传递积极生活态度并多次参与行业文化交流活动")
    st.subheader('作品简介:')
    st.markdown('''地球进入灵气复苏时代，人类开启异能觉醒！江南开局觉醒最强地摊系统，大力药水，解毒小黄豆，幸运樱桃，供不应求。世界顶级神豪、首富、人气主播、巅峰强者纷纷前来求购。江南：“我对钱亿点都不感兴趣，我只想坑……额，我的愿望是世界和平。”
                ''')
    st.markdown('''蓝星灵气复苏，强者为尊。我们还在为了达到道天而努力。殊不知，遥远的星空之上，一群所谓的神明早已盯上了我们赖以生存的家园。

在我们还在不停内斗之时，而又谁会想的到，这次灵气复苏只不过是所谓的神明对蓝星开发新的开始！

而所谓的神明对蓝星的开发，已经发生过不止一次，期间又有多少人类先辈与神明抗争，拼尽全力，甚至失去了生命，方可打退了神明，虽人类未败，但也未胜。

只因神明退走之时，将蓝星锁灵绝灵，以断人类变强之路，以便于再次开发！

呜呼哀哉！神明在蓝星上来去自如，肆意妄为，待人类为刍狗，可任意欺凌，而人类先辈拼尽生命也只有打退神明的实力，而没有打胜神明，永绝后患的实力！

蓝星绝灵之后，人类再无机会，人类剩余先辈们纷纷留下后手，甚至有先辈宁愿放弃了自己更好的未来，押上自己的一切甚至堵上自己的生命，只为后世抗击神明做准备，把一切押在未来！只为了后世人类一个赢得可能。

而此次灵气复苏人类中竟然有些人来种族危机之迹还为了自身利益，不顾大局，负恩昧良，妄负信任，甘愿为神明驱使，做神明的走狗！

还有些人被迫打上奴印，被神明所控制，身不由己，但却身在神明，心在人类，在战争中给人类放水，多次给予人类机会，甚至得知主角被神明走狗偷袭死亡（其实主角是诈死），为其报仇，找幕后凶手拼命！

卧底，反卧底，此次人类与神明的抗争，人类因之前众多先辈的付出与牺牲，是人类最好的时代，所以只能胜，不能败，败则一无所有，胜，人类方有生存之希望！

而且这场人神博弈，仅仅是星空小小的一步棋，就算取胜，人类又该如何才能成为执棋者。''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E5%BC%80%E5%B1%80%E5%9C%B0%E6%91%8A%E5%8D%96%E5%A4%A7%E5%8A%9B/56846236')
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel9():
    st.title('夜的命名术')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/ydmms.png'
    st.image(photo_path)
    st.subheader('本书作者:会说话的肘子')
    st.markdown("会说话的肘子，本名任禾，1990年出生，男，中国网络作家，起点中文网2020年原创文学白金作家之一。2022年9月加入中国作家协会，代表作包括《大王饶命》《第一序列》《夜的命名术》等，其中《第一序列》入围2020年网络文学重点作品扶持名单，《夜的命名术》获第33届中国科幻银河奖最具改编潜力奖。")
    st.subheader('作品简介:')
    st.markdown('''该书的风格是科幻+都市异能流。这次作者把平行宇宙的概念搬出来，在小说里介绍了两个平行世界，即表世界和里世界，现代世界与赛博朋克的世界并存，虽然近在咫尺，但又远在天边，隔着时空之墙，无法触及。但某一时刻，表世界的一部分人在固定时间内会穿梭到里世界，造成了极大的冲击和变动。
                ''')
    st.markdown('**蓝与紫的霓虹中，浓密的钢铁苍穹下，数据洪流的前端，是科技革命之后的世界，也是现实与虚幻的分界。**')
    st.markdown('**钢铁与身体，过去与未来。**')
    st.markdown('**这里，表世界与里世界并存，面前的一切，像是时间之墙近在眼前。**')
    st.markdown('**黑暗逐渐笼罩。**')
    st.markdown('**可你要明白啊我的朋友，我们不能用温柔去应对黑暗，要用火啊。**')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E5%A4%9C%E7%9A%84%E5%91%BD%E5%90%8D%E6%9C%AF/56771335')
    st.markdown('------')
    photo_path='photo/ydmms_shengsiguan.png'
    st.image(photo_path)
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel10():
    st.title('遮天')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/zt.png'
    st.image(photo_path)
    st.subheader('本书作者:辰东')
    st.markdown('''杨振东，男，笔名辰东，1982年出生于北京， 毕业于中国石油大学。阅文集团白金作家，网络文学代表性人物之一，中国作协成员。开创出太古战争流和悬念玄幻流两大网络小说流派，代表作有《神墓》《遮天》《长生界》《完美世界》《圣墟》等。
2004年底，辰东到网站上连载《不死不灭》的仙侠小说连载效果不错，网站就和其签了约。毕业后，辰东开始了专职网络写作。2006年，在起点中文网连载第二部作品《神墓》，成为了辰东的成名作。2008年，在起点中文网连载第三部作品《长生界》。2010年，在起点中文网连载第四部作品《遮天》。2013年，在起点中文网连载第五部作品《完美世界》， [16]获得第四届起点金键盘奖评选“年度新作王”“年度玄幻奇幻王”“2013年度最佳男主角” [20]2013年，加入了中国作家协会。 [12]2016年底，在起点中文网连载《圣墟》，上架后持续包揽起点月票榜首长达十个月。2017年中国原创文学风云榜，《圣墟》问鼎男生总榜第一。 [15]2019年，获得第二届茅盾文学新人奖·网络文学新人奖。 [8]2020年11月20日，阅文集团宣布阅文起点大学正式成立，辰东成为首批阅文起点大学导师。 [22]2021年5月初，携新作《深空彼岸》登录起点中文网。2023年，在起点中文网连载第八部作品《圣墟：番外》。2024年，在起点中文网连载第九部作品《夜无疆》。
辰东想象力超群，善于制造悬念，行文天马行空，作品恢弘大气，长期占据网站各大榜单前列，人气与口碑兼具。''')
    st.markdown('''《遮天》在中国网络小说中具有极高的影响力，被认为是东方玄幻小说的经典之一。其主要角色如不死天皇和帝尊等，贯穿了整个故事，展现了深厚的世界观和复杂的人物关系，这些都增强了其在读者中的知名度和影响力。此外，小说的叙事风格和宏大的气势使其在同类作品中脱颖而出，成为许多读者心目中的经典。总的来说，《遮天》不仅在文学上有着重要地位，也对后续的网络小说创作产生了深远的影响。''')
    st.subheader('作品简介:')
    st.markdown('冰冷与黑暗并存的宇宙深处，九具庞大的龙尸拉着一口青铜古棺，亘古长存。')
    st.markdown('这是太空探测器在枯寂的宇宙中捕捉到的一幅极其震撼的画面。')
    st.markdown('九龙拉棺，究竟是回到了上古，还是来到了星空的彼岸？')
    st.markdown('一个浩大的仙侠世界，光怪陆离，神秘无尽。')
    st.markdown('热血似火山沸腾，激情若瀚海汹涌，欲望如深渊无止境……')
    st.markdown('登天路，踏歌行，弹指遮天。')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E9%81%AE%E5%A4%A9/7572')
    st.markdown('------')
    st.subheader('主角')
    st.markdown('''叶凡：本书男主角，与众老同学在泰山聚会时一同被九龙拉棺带离地球，进入北斗星域，得知自己是荒古圣体。历险禁地，习得源术，斗圣地世家，战太古生物，重组天庭，叶凡辗转四方得到许多机遇和挑战，功力激增，眼界也渐渐开阔，最后以力证道，取得各族认可，成就天帝果位，率天庭举教成仙。''')
    st.markdown('------')
    st.subheader('作品设定')
    st.markdown('**境界划分**')
    photo_path='photo/zt_jingjie1.png'
    st.image(photo_path)
    photo_path='photo/zt_jingjie2.png'
    st.image(photo_path)
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel11():
    st.title('雪中悍刀行')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/xzhdx.jpg'
    st.image(photo_path)
    st.subheader('本书作者:烽火戏诸侯')
    st.markdown('''烽火戏诸侯（本名陈政华），1985年出生于浙江省杭州市淳安县，毕业于浙江工商大学，中国作家协会会员，第十二届全国青联委员，现任浙江省网络作家协会副主席、杭州市网络作家协会主席。橙瓜见证·网络文学20年十大仙侠作家、百强大神作家、百位行业代表人物，曾获首届泛华文网络文学“金键盘”奖。2005年开始网络文学创作，代表作有《极品公子》《陈二狗的妖孽人生》《老子是癞蛤蟆》《雪中悍刀行》《剑来》等，其文风多变，涵盖现代都市、武侠仙侠、东方玄幻，尤擅以细节动人心。其中《雪中悍刀行》获2015年首届网络文学双年奖银奖，入选中国作家协会2016年“中国网络小说排行榜”年榜，位列《2018猫片·胡润原创文学IP价值榜》第九名，改编同名电视剧在中央电视台播出并入选2023年中国网络文学影响力榜IP影响榜 ；《陈二狗的妖孽人生》改编网剧在腾讯视频点击量突破20亿并荣获年度惊喜网剧荣誉；《剑来》入选2017年“中国网络小说排行榜”年榜 ，改编动画获2025年微博年度国漫IP奖 ，入选2023-2024年度优秀网文IP转化作品 。2025年捐资援建杭州市网络作协石榴籽图书室 ，作品《老子是癞蛤蟆》改编网剧《我叫赵甲第》于2022年登陆优酷视频 。''')
    st.subheader('作品简介:')
    st.markdown('''《雪中悍刀行》是网络作家烽火戏诸侯创作的长篇玄幻武侠小说，2012年6月于纵横中文网首发，2013年9月由江苏文艺出版社出版实体书，全书457万余字。作品以离阳王朝北凉世子徐凤年历经庙堂权谋与江湖纷争的成长为主线，融合架空历史的春秋国战、江湖武学境界体系（金刚、指玄、天象、陆地神仙）与玄幻元素，描绘了三十万北凉铁骑戍守边关、抵御北莽入侵的宏大叙事。小说塑造了徐骁、姜泥、李淳罡等数百位性格鲜明的角色，构建了离阳、北莽、西楚等多势力交织的世界观，获首届网络文学双年奖银奖、金键盘奖玄幻仙侠类奖项，位列2017胡润原创文学IP价值榜第17位。其诗化语言与“以术入道”的武学设定广受读者推崇，结局以“小二上酒”呼应开篇，成为经典符号。
                ''')
    st.markdown('有个白狐脸儿，佩双刀绣冬春雷，要做那天下第一；')
    st.markdown('湖底有白发老魁爱吃荤；')
    st.markdown('缺门牙老仆背剑匣；')
    st.markdown('山上有个骑青牛的年轻师叔祖，不敢下山；')
    st.markdown('有个骑大猫扛向日葵不太冷的少女杀手；')
    st.markdown('江湖是一张珠帘。大人物小人物，是珠子，大故事小故事，是串线。情义二字，则是那些珠子的精气神。开始收官中。最终章将以那一声“小二上酒”结尾。')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E9%9B%AA%E4%B8%AD%E6%82%8D%E5%88%80%E8%A1%8C/7328338')
    st.markdown('------')
    st.subheader('春秋战争')
    st.markdown('''西楚景河之战：十二万大戟士对阵北凉铁骑，全军覆没，死战不屈。
西楚襄樊守城战：春秋第一守将王明阳坐镇死守。二十万襄樊人只剩下不到一万。襄樊攻守，北凉军精锐折损大半，其中就有三百名精于钻地的穴师，死亡殆尽。
西楚西垒壁之战：西楚亡国之战。春秋国战最后一战。北凉军与西楚军对峙两年。北凉旧部马岭等十四人以死替徐骁表忠。王妃一袭白衣缟素亲自敲响战鼓，鼓声如雷，不破西楚鼓不绝。“死战第一”千人鱼鼓营死战不退，最终只活下来十六人，为“骑战第一”三千大雪龙骑兵开辟出一条直插叶白夔大戟军腹地的坦荡血路。陈芝豹坐镇中军，运筹帷幄；王妃吴素亲自擂鼓；徐骁舍弃头盔，持矛首当其冲；三千白马白甲，一路奔雷踏去。其中便有鱼鼓营千余人的袍泽尸体。小人屠陈芝豹与叶白夔死战。叶白夔战死。此战后，杨太岁曾力劝徐骁不杀硕儒方孝梨，最终无果。
西楚灭国后，徐骁受封大柱国，隔天被封北凉王。老皇帝要将以武乱禁的江湖掀翻，徐骁一人请命马踏江湖，不曾开战，便有两万名百战老卒请辞还家，更有无数出身江湖的猛将对徐骁心生怨恨，转投其它军伍。''')
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel12():
    st.title('盗墓笔记')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/dmbj.png'
    st.image(photo_path)
    st.subheader('本书作者:南派三叔')
    st.markdown("南派三叔（Uncle Three），本名徐磊，1982年2月20日出生于浙江省嘉兴市嘉善县，中国作家，编剧 ，中国作家协会会员 [2]，南派投资董事长，橙瓜见证·网络文学20年十大悬疑作家，百强大神作家，百位行业人物。")
    st.subheader('作品简介:')
    st.markdown('''小说以战国帛书为线索展开，五十年前长沙盗墓团伙发掘帛书后遭遇诡异事件，五十年后参与者后人吴邪组建团队再度探秘，经历七星疑棺、青眼狐尸等超自然现象。作品塑造“铁三角”核心人物吴邪、张起灵与王胖子，通过虚实结合的叙事手法融合历史秘闻、风水玄学与悬疑探险，构建包含长白山青铜门、张家古楼等标志性场景的盗墓宇宙
            ''')
    st.markdown('''故事起源于1952年，主角吴邪的祖父吴老狗在长沙的血屍墓里发现战国帛书，而引发后来吴邪从帛书解谜途中的一段段冒险。五十年後，吴邪一个看似单纯的吴家富二代，大学毕业后便经营着古董店，日子过一天是一天，殊不知其身世冒险之离奇，因为发现先人笔记中一个秘密就此展开。抱著好奇和一颗想见世面的心，他硬是跟上他三叔及一群盗墓高手的鲁王宫之旅，欲解开帛书之谜。在这个过程中他遇见了闷油瓶和胖子。在途中，很多他一辈子都没见过的东西，或是连想都没想过的东西，一个接著一个出现。遭遇的每件事，越来越离奇。就在他发现自己的生活满是谜题，并欲寻求解答时，唯一的线索──「三叔」却消失了。不甘放弃的吴邪，决定追根究柢，也决定今後不凡但却不为人知的冒险旅程。''')
    st.markdown('''''')
    st.subheader('作品鉴赏')
    st.markdown('''《盗墓笔记》系列堪称近年来中国出版界的奇迹，与《鬼吹灯》共同开启了中国通俗小说界的“盗墓时代”，获得百万读者狂热追捧。 [6]
看盗墓类小说可能有点儿显得浅薄。好像没什么思想意义，也没有让人积极向上的推动力。可我是个喜欢猎奇的人，而且比较轻信，很容易被这类小说牵着鼻子走，一会儿跟着里面的人物紧张恐惧，一会儿毛骨悚然地想象着各种古怪的场景，然后，合上书，长嘘一口，觉得眼前的生活格外美妙。南派三叔的《盗墓笔记》就属于我猎奇的范围。当然，看这种作品我也没想着以吓唬自己为乐，我觉得它是有含金量的，最大的含金量就是：想象力。而不仅仅是会讲故事。就像喜欢柯南道尔和青山刚昌的侦探想象力、宫崎骏的唯美想象力，关于盗墓的想象力，我也没拒绝喜欢一把。而国内拿得出手的写作盗墓小说高手，南派三叔应该是代表人物之一。灵异、玄幻、推理……如果阅读一个作品，不用沉思，不用哀伤，不用愤怒，不用上纲上线，而只是轻松一下，也不失为一个有益的娱乐活动。 [4]
作家南派三叔《盗墓笔记》，中国盗墓类小说巅峰作品之一，自2007年出版发行，短短四年共出版九本实体书，以长达九卷的鸿篇巨制巧妙布局，集奇思妙想、悬疑恐怖、瑰丽神奇于一身，20年间获百万读者狂热追捧，至今仍是类型小说的经典扛鼎之作。''')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0/21859')
    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel13():
    st.title('我在精神病院学斩神')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/wzjsbyxzs.jpg'
    st.image(photo_path)
    st.subheader('本书作者:三九音域')
    st.markdown("三九音域，番茄小说 签约作者，著作第一本小说《超能：我有一面复刻镜》（已完结），第二本小说《我在精神病院学斩神》（已完结），第三本小说《我不是戏神》（连载中）")
    st.subheader('作品简介:')
    st.markdown('''小说以现代都市为背景，讲述林七夜带领夜幕小队对抗克苏鲁神明、守卫大夏文明的故事，融合中国神话、古希腊神话等多元神系设定，构建守夜人组织、禁墟序列等世界观架构。实体书《夜幕之下》出版后累计销量超10万册，影视改编由南派三叔担任编剧。作品长期占据番茄小说巅峰榜前三名，在平台获超120万读者打出9.8分，网剧概念海报于2024爱奇艺悦享大会首次发布。
      ''')
    st.markdown('你是否想过，在霓虹璀璨的都市之下，潜藏着来自古老神话的怪物？')
    st.markdown('你是否想过，在那高悬于世人头顶的月亮之上，伫立着守望人间的神明？')
    st.markdown('你是否想过，在人潮汹涌的现代城市之中，存在代替神明行走人间的超凡之人？')
    st.markdown('人类统治的社会中，潜伏着无数诡异；')
    st.markdown('在那些无人问津的生命禁区，居住着古老的神明。')
    st.markdown('炽天使米迦勒，冥王哈迪斯，海神波塞冬……')
    st.markdown('而属于大夏的神明，究竟去了何处？')
    st.markdown('在这属于“人”的世界，“神秘”需要被肃清！')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E6%88%91%E5%9C%A8%E7%B2%BE%E7%A5%9E%E7%97%85%E9%99%A2%E5%AD%A6%E6%96%A9%E7%A5%9E/58937945')
    st.markdown('------')
    st.subheader('等级划分')
    photo_path='photo/wzjsbyxzs_dengjihuafen.png'
    st.image(photo_path)
    st.markdown('------')
    st.subheader('神明序列')
    st.markdown('**神明代号**：人类发现神明的顺序，与神明自身的战力和危险程度无关。')
    photo_path='photo/wzjsbyxzs_smxl1.png'
    st.image(photo_path)
    photo_path='photo/wzjsbyxzs_smxl2.png'
    st.image(photo_path)
    photo_path='photo/wzjsbyxzs_smxl3.png'
    st.image(photo_path)
    st.markdown('------')
    st.subheader('禁墟划分')
    st.markdown('**禁墟**：人类对禁墟的危险等级进行划分，排列出的一张序列表，和神明代号一样是从001开始。序列越靠前，代表越危险。')
    st.markdown('**神明领域**：禁墟序列的前30，被称为神明领域。拥有这30个禁墟的存在，已经踏入了神明的范畴')
    st.markdown('神明赐予的力量，也是禁墟的一种，也在序列里。禁墟序列的前30里，有23个都是神墟，还有7个禁墟并非来自于神明，而是源于人类本身，被称为七大“王墟”')
    photo_path='photo/wzjsbyxzs_jingxuhuafen.png'
    st.image(photo_path)
    st.subheader('禁墟')
    photo_path='photo/wzjsbyxzs_jingxu1.png'
    st.image(photo_path)
    photo_path='photo/wzjsbyxzs_jingxu2.png'
    st.image(photo_path)
    photo_path='photo/wzjsbyxzs_jingxu3.png'
    st.image(photo_path)
    photo_path='photo/wzjsbyxzs_jingxu4.png'
    st.image(photo_path)
    st.markdown('**获得禁墟的办法**：')
    st.markdown('第一种，一小部分幸运儿能够生下来就拥有使用禁墟的天赋。')
    st.markdown('第二种，则是借助拥有禁墟的物品。')
    st.markdown('第三种，神明赐予。')
    st.markdown('------')
    st.title('守夜人誓言')
    st.subheader('若黯夜终临，吾必立于万万人前，横刀向渊，血染天穹。 ——大夏守夜人')

    # video_path=""
    # st.video(video_path)
#################################################################################################################################################################################################################################
def render_novel14():
    st.title('我一只史莱姆吊打巨龙很合理吧')
    st.button('返回作者喜欢的书目',on_click=go_to_my_love_novel())
    photo_path='photo/wyzslmddjlhhlb.jpg'
    st.image(photo_path)
    st.subheader('本书作者:三风11')
    st.markdown("作者三风11为全职作家，此前创作过修真、科幻末世等题材作品。")
    st.subheader('作品简介:')
    st.markdown('''小说讲述陈书穿越到以御兽为主导的平行世界，绑定神级选择系统后获得强化宠物能力，培养出能对抗巨龙的史莱姆、元素哈士奇等非常规契约灵。随着凶兽入侵引发时代危机，贪图小利但坚守底线的主角逐步蜕变，带领同伴对抗灾难。作品通过荒诞风格展现非传统御兽战斗，世界观融合现代元素与异空间设定。
            ''')
    st.markdown('一觉醒来，陈书穿越到了以御兽为主的平行世界，同时绑定了神级选择系统！')
    st.markdown('只要做出选择，就能获得各种奖励！在系统的帮助下，他的宠物逐渐变态化：可以一屁股坐死巨龙的史莱姆，用元素技能轰哭凤凰的哈士奇，掌握空间之力的……')
    st.markdown('一只只扯淡离谱的御兽出现，全世界的三观都碎了……御兽界的至高王座上，陈书回首一望，笑着说道：“叔叔我啊，御兽从来不讲科学！')
    st.markdown('想了解更多，请访问链接：https://baike.baidu.com/item/%E6%88%91%E4%B8%80%E4%B8%AA%E5%8F%B2%E8%8E%B1%E5%A7%86%E5%90%8A%E6%89%93%E5%B7%A8%E9%BE%99%E5%BE%88%E5%90%88%E7%90%86%E5%90%A7%EF%BC%9F/60209918')
    # video_path=""
    # st.video(video_path)
default_my_love_novel_data = {"我不是戏神","十日终焉","诡秘之主","神秘复苏","我在精神病院学斩神","诸神愚戏","斗破苍穹","开局地摊卖大力","我一只史莱姆吊打巨龙很合理吧"
                              ,"遮天","雪中悍刀行","盗墓笔记","夜的命名术","道诡异仙"}


def render_my_love_novel():
    st.title('开发者喜欢的小说！（加上一点介绍）')
    st.button("返回首页", on_click=go_to_home)
    cols = st.columns(10) 
    with cols[1]:
        if st.button('我不是戏神',use_container_width=True):
            go_to_novel1()
    with cols[2]:
        if st.button('十日终焉',use_container_width=True):
            go_to_novel2()
    with cols[3]:
        if st.button('诡秘之主',use_container_width=True):
            go_to_novel3()
    with cols[4]:
        if st.button('神秘复苏',use_container_width=True):
            go_to_novel4()
    with cols[5]:
        if st.button('道诡异仙',use_container_width=True):
            go_to_novel5()
    with cols[6]:
        if st.button('诸神愚戏',use_container_width=True):
            go_to_novel6()
    with cols[7]:
        if st.button('斗破苍穹',use_container_width=True):
            go_to_novel7()
    with cols[1]:
        if st.button('开局地摊卖大力',use_container_width=True):
            go_to_novel8()
    with cols[2]:
        if st.button('夜的命名术',use_container_width=True):
            go_to_novel9()
    with cols[3]:
        if st.button('遮天',use_container_width=True):
            go_to_novel10()
    with cols[4]:
        if st.button('雪中悍刀行',use_container_width=True):
            go_to_novel11()
    with cols[5]:
        if st.button('盗墓笔记',use_container_width=True):
            go_to_novel12()
    with cols[6]:
        if st.button('我在精神病院学斩神',use_container_width=True):
            go_to_novel13()
    with cols[7]:
        if st.button('我一只史莱姆吊打巨龙很合理吧',use_container_width=True):
            go_to_novel14()
def main():
    # 渲染侧边栏
    render_sidebar()
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'history':
        render_history()
    elif st.session_state.page == 'categories':
        render_categories()
    elif st.session_state.page == 'category_detail':
        render_category_detail()
    elif st.session_state.page == 'book_search':
        render_book_search()
    elif st.session_state.page == 'character_dialog':
        render_character_dialog()
    elif st.session_state.page == 'story_mode':
        render_story_mode()
    elif st.session_state.page == 'write_novel':
        render_write_novel()
    elif st.session_state.page == 'my_love_novel':
        render_my_love_novel()
    elif st.session_state.page == "novel1":
        render_novel1()
    elif st.session_state.page == "novel2":
        render_novel2()
    elif st.session_state.page == "novel3":
        render_novel3()
    elif st.session_state.page == "novel4":
        render_novel4()
    elif st.session_state.page == "novel5":
        render_novel5()
    elif st.session_state.page == "novel6":
        render_novel6()
    elif st.session_state.page == "novel7":
        render_novel7()
    elif st.session_state.page == "novel8":
        render_novel8()
    elif st.session_state.page == "novel9":
        render_novel9()
    elif st.session_state.page == "novel10":
        render_novel10()
    elif st.session_state.page == "novel11":
        render_novel11()
    elif st.session_state.page == "novel12":
        render_novel12()
    elif st.session_state.page == "novel13":
        render_novel13()
    elif st.session_state.page == "novel14":
        render_novel14()
if __name__ == "__main__":
    main()