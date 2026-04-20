import streamlit as st
import pandas as pd
import os
import datetime

# -------------------------- 配置区 --------------------------
DATA_FILE = "data.xlsx"
APPLY_FILE = "apply_data.xlsx"
ADMIN_PASSWORD = "123456"

# 初始化数据文件
def init_files():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["code", "level", "level_name", "create_time"])
        df.to_excel(DATA_FILE, index=False)
    
    if not os.path.exists(APPLY_FILE):
        df = pd.DataFrame(columns=[
            "name", "phone", "company", "email", 
            "apply_level", "apply_time", "status", "code"
        ])
        df.to_excel(APPLY_FILE, index=False)

# 读取资格数据
def load_qualify_data():
    try:
        df = pd.read_excel(DATA_FILE)
        return df.to_dict("records")
    except:
        return []

# 读取报名数据
def load_apply_data():
    try:
        df = pd.read_excel(APPLY_FILE)
        return df.to_dict("records")
    except:
        return []

# 添加资格账号
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

# 保存报名信息
def save_apply_info(name, phone, company, email, apply_level):
    df = pd.read_excel(APPLY_FILE)
    new_row = {
        "name": name,
        "phone": phone,
        "company": company,
        "email": email,
        "apply_level": apply_level,
        "apply_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待审核",
        "code": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(APPLY_FILE, index=False)
    return True

# 初始化
init_files()
QUALIFIED_LIST = load_qualify_data()

# -------------------------- 页面 --------------------------
st.set_page_config(
    page_title="深信服托管云渠道机器人",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 深信服托管云渠道机器人")
st.markdown("### 渠道资格查询 | 认证流程 | 报名开通")
st.markdown("---")

# 选项卡
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 资格查询",
    "📖 认证流程指导",
    "📝 智能报名开通",
    "⚙️ 后台管理"
])

# ==============================================
# 选项卡1：资格查询
# ==============================================
with tab1:
    st.subheader("🏅 渠道资格等级查询")
    user_code = st.text_input("请输入渠道公式名称", placeholder="例如：SXF2025001")
    if st.button("立即查询", type="primary"):
        if not user_code:
            st.error("请输入渠道公式名称！")
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
                st.markdown(f"""
                #### 认证信息
                - 等级：**{lv_name}**
                - 编码：**{lv}**
                """)
                if lv == "SCTA":
                    st.info("📌 初级渠道认证 SCTA")
                elif lv == "SCTP":
                    st.warning("📌 中级渠道认证 SCTP")
                elif lv == "SCTE":
                    st.error("📌 高级渠道认证 SCTE")
                st.balloons()
            else:
                st.error("❌ 未查询到该账号信息")

# ==============================================
# 选项卡2：认证流程指导
# ==============================================
with tab2:
    st.subheader("📖 深信服托管云渠道认证流程")
    st.markdown("""
    ### 一、认证等级说明
    1. **初级 SCTA**：基础渠道认证
    2. **中级 SCTP**：进阶渠道认证
    3. **高级 SCTE**：最高级别渠道认证

    ### 二、认证流程（4步完成）
    1. 填写报名信息（姓名、公司、电话、等级）
    2. 提交审核（系统自动记录）
    3. 管理员审核开通账号
    4. 收到渠道公式名称 → 可查询认证资格

    ### 三、使用说明
    - 认证通过后，会自动生成**唯一渠道公式名称**
    - 凭公式名称可查询认证等级、使用渠道权限
    - 认证信息永久有效，可随时查询
    """)
    st.success("按照流程完成报名，1-3个工作日内完成审核开通！")

# ==============================================
# 选项卡3：智能报名开通
# ==============================================
with tab3:
    st.subheader("📝 智能获取报名信息 - 自动开通认证账号")
    st.markdown("请填写以下信息，提交后管理员将尽快为您开通认证账号")
    
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
                st.error("⚠️ 姓名、电话、公司为必填项！")
            else:
                save_apply_info(name, phone, company, email, apply_level)
                st.success("✅ 报名信息提交成功！\n\n管理员将在1-3个工作日内审核并开通认证账号，请耐心等待。")

# ==============================================
# 选项卡4：后台管理
# ==============================================
with tab4:
    st.subheader("⚙️ 管理员后台 - 账号开通 & 数据管理")
    pwd = st.text_input("请输入管理员密码", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("✅ 管理员登录成功")
        
        # 1. 手动添加账号
        st.markdown("#### 1. 手动开通认证账号")
        with st.form("add_form"):
            code = st.text_input("渠道公式名称 *")
            level = st.selectbox("等级", ["SCTA", "SCTP", "SCTE"])
            level_map = {"SCTA":"初级","SCTP":"中级","SCTE":"高级"}
            lv_name = level_map[level]
            add_btn = st.form_submit_button("添加并开通账号")
            
            if add_btn:
                if not code:
                    st.error("请输入渠道公式名称！")
                else:
                    res = add_qualify_data(code, level, lv_name)
                    if res:
                        st.success(f"✅ 账号 {code} 开通成功！")
                        st.rerun()
                    else:
                        st.error("❌ 该账号已存在")
        
        st.markdown("---")
        
        # 2. 查看报名列表
        st.markdown("#### 2. 报名信息列表")
        apply_data = load_apply_data()
        if apply_data:
            df_apply = pd.DataFrame(apply_data)
            st.dataframe(df_apply, use_container_width=True)
        else:
            st.info("暂无报名信息")
        
        st.markdown("---")
        
        # 3. 查看已开通账号
        st.markdown("#### 3. 已开通认证账号列表")
        if QUALIFIED_LIST:
            df_q = pd.DataFrame(QUALIFIED_LIST)
            st.dataframe(df_q, use_container_width=True)
        else:
            st.info("暂无开通账号")
            
    elif pwd != "":
        st.error("❌ 密码错误！")

st.markdown("---")
st.caption("📌 本系统仅限深信服托管云渠道内部使用 | 技术支持：渠道管理团队")
