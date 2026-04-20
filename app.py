import streamlit as st
import pandas as pd
import os
import datetime

# -------------------------- 配置区 --------------------------
DATA_FILE = "data.xlsx"
APPLY_FILE = "apply_data.xlsx"
ADMIN_PASSWORD = "123456"

st.set_page_config(
    page_title="深信服托管云渠道机器人",
    page_icon="🤖",
    layout="wide"
)

# 页面样式美化（商务深蓝色风格）
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stTextInput, .stSelectbox { border-radius: 8px; }
    .stButton>button {
        border-radius: 8px;
        background-color: #004682;
        color: white;
        font-size:16px;
    }
    .stButton>button:hover {
        background-color: #003366;
        color:white;
    }
    .card {
        background-color:white;
        padding:20px;
        border-radius:12px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        margin-bottom:16px;
    }
    h1 { color: #004682; }
    h3 { color: #004682; }
</style>
""", unsafe_allow_html=True)

# 初始化文件
def init_files():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["code", "level", "level_name", "create_time"])
        df.to_excel(DATA_FILE, index=False)
    if not os.path.exists(APPLY_FILE):
        df = pd.DataFrame(columns=["name","phone","company","email","apply_level","apply_time","status","code"])
        df.to_excel(APPLY_FILE, index=False)

def load_qualify_data():
    try:
        df = pd.read_excel(DATA_FILE)
        return df.to_dict("records")
    except:
        return []

def load_apply_data():
    try:
        df = pd.read_excel(APPLY_FILE)
        return df.to_dict("records")
    except:
        return []

def add_qualify_data(new_code, new_level, new_level_name):
    df = pd.read_excel(DATA_FILE)
    if new_code in df["code"].astype(str).values:
        return False
    new_row = {
        "code": new_code,
        "level": new_level,
        "level_name": new_level_name,
        "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)
    return True

def save_apply_info(name, phone, company, email, apply_level):
    df = pd.read_excel(APPLY_FILE)
    new_row = {
        "name": name, "phone": phone, "company": company, "email": email,
        "apply_level": apply_level, "apply_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待审核", "code": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(APPLY_FILE, index=False)
    return True

init_files()
QUALIFIED_LIST = load_qualify_data()

# -------------------------- 页面标题 --------------------------
st.title("🤖 深信服托管云渠道机器人")
st.markdown("#### 渠道资格查询 | 认证流程 | 报名开通 | 数据管理")
st.markdown("---")

# 选项卡
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 资格查询",
    "📖 认证流程",
    "📝 报名开通",
    "⚙️ 管理后台"
])

# ==============================================
# 选项卡1：资格查询
# ==============================================
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏅 渠道资格等级查询")
    user_code = st.text_input("渠道公式名称", placeholder="例如：SXF2025001")
    if st.button("立即查询", type="primary"):
        if not user_code:
            st.error("请输入渠道公式名称")
        else:
            find = None
            for item in QUALIFIED_LIST:
                if str(item["code"]).strip() == user_code.strip():
                    find = item
                    break
            if find:
                lv = find["level"]
                lv_name = find["level_name"]
                st.success(f"✅ 查询成功：{user_code}")
                st.markdown(f"**等级：** {lv_name}")
                st.markdown(f"**编码：** {lv}")
                if lv == "SCTA":
                    st.info("📌 初级渠道认证 SCTA")
                elif lv == "SCTP":
                    st.warning("📌 中级渠道认证 SCTP")
                elif lv == "SCTE":
                    st.error("📌 高级渠道认证 SCTE")
                st.balloons()
            else:
                st.error("❌ 未查询到该账号信息")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================
# 选项卡2：认证流程
# ==============================================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 渠道认证流程说明")
    st.markdown("""
    **🏅 认证等级**
    • 初级 SCTA：基础渠道认证
    • 中级 SCTP：进阶渠道认证
    • 高级 SCTE：高级别渠道认证

    **📌 认证流程**
    1. 填写报名信息（姓名、公司、电话）
    2. 提交申请，等待管理员审核
    3. 审核通过后自动开通认证账号
    4. 凭渠道公式名称可查询资格等级

    **💡 说明**
    • 唯一渠道公式名称开通后生效
    • 可随时查询认证状态
    • 数据永久保存，安全可靠
    """)
    st.success("✅ 提交报名后，1-3个工作日内完成审核开通")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================
# 选项卡3：报名开通
# ==============================================
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 智能报名 - 自动开通认证账号")
    with st.form("apply_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("姓名 *")
            phone = st.text_input("联系电话 *")
            company = st.text_input("公司名称 *")
        with col2:
            email = st.text_input("邮箱")
            apply_level = st.selectbox("申请认证等级", ["初级 SCTA", "中级 SCTP", "高级 SCTE"])
        submit = st.form_submit_button("✅ 提交报名信息")
        
        if submit:
            if not name or not phone or not company:
                st.error("请填写完整必填信息")
            else:
                save_apply_info(name, phone, company, email, apply_level)
                st.success("✅ 报名提交成功！管理员将尽快审核开通")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================
# 选项卡4：管理后台
# ==============================================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ 管理员后台")
    pwd = st.text_input("管理员密码", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("✅ 已登录管理员模式")

        st.markdown("#### 1. 开通认证账号")
        with st.form("add_form"):
            code = st.text_input("渠道公式名称")
            level = st.selectbox("等级", ["SCTA", "SCTP", "SCTE"])
            level_map = {"SCTA":"初级","SCTP":"中级","SCTE":"高级"}
            lv_name = level_map[level]
            add_btn = st.form_submit_button("添加并开通账号")
            if add_btn:
                if not code:
                    st.error("请输入渠道公式名称")
                else:
                    r = add_qualify_data(code, level, lv_name)
                    if r:
                        st.success(f"✅ {code} 开通成功")
                        st.rerun()
                    else:
                        st.error("❌ 已存在")

        st.markdown("---")
        st.markdown("#### 2. 报名信息列表")
        apply_data = load_apply_data()
        if apply_data:
            st.dataframe(pd.DataFrame(apply_data), use_container_width=True)
        else:
            st.info("暂无报名")

        st.markdown("---")
        st.markdown("#### 3. 已开通账号列表")
        if QUALIFIED_LIST:
            st.dataframe(pd.DataFrame(QUALIFIED_LIST), use_container_width=True)
        else:
            st.info("暂无开通账号")
    elif pwd != "":
        st.error("密码错误")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("📌 深信服托管云渠道专用系统 | 内部使用")
