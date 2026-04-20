import streamlit as st
import pandas as pd
import os

# -------------------------- 配置区 --------------------------
DATA_FILE = "data.xlsx"
ADMIN_PASSWORD = "123456"

def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["code", "level", "level_name"])
        df = pd.concat([df, pd.DataFrame([
            {"code": "CHAN001", "level": "SCTA", "level_name": "初级"},
            {"code": "CHAN002", "level": "SCTP", "level_name": "中级"},
            {"code": "CHAN003", "level": "SCTE", "level_name": "高级"},
        ])], ignore_index=True)
        df.to_excel(DATA_FILE, index=False)

def load_data():
    try:
        df = pd.read_excel(DATA_FILE)
        return df.to_dict("records")
    except:
        return []

def add_data(new_code, new_level, new_level_name):
    df = pd.read_excel(DATA_FILE)
    if new_code in df["code"].values:
        return False
    new_row = {"code": new_code, "level": new_level, "level_name": new_level_name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)
    return True

init_data()
QUALIFIED_LIST = load_data()

st.set_page_config(
    page_title="深信服托管云渠道机器人",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 深信服托管云渠道机器人")
st.markdown("### 渠道资格等级查询 & 认证数据管理")
st.markdown("---")

tab1, tab2 = st.tabs(["🔍 资格查询", "➕ 补充认证数据"])

with tab1:
    st.subheader("输入渠道公式名称查询")
    user_code = st.text_input("渠道公式名称", key="query_code")
    
    if st.button("查询资格等级", type="primary", key="query_btn"):
        if not user_code:
            st.error("请输入渠道公式名称！")
        else:
            find_item = None
            for item in QUALIFIED_LIST:
                if str(item["code"]).strip() == user_code.strip():
                    find_item = item
                    break
            
            if find_item:
                level = find_item["level"]
                level_name = find_item["level_name"]
                st.success("✅ 查询成功！")
                st.markdown(f"""
                ### 🏅 渠道资格信息
                - **公式名称**：{user_code}
                - **资格等级**：{level_name}（{level}）
                """)
                
                if level == "SCTA":
                    st.info("初级渠道资格 SCTA")
                elif level == "SCTP":
                    st.warning("中级渠道资格 SCTP")
                elif level == "SCTE":
                    st.error("高级渠道资格 SCTE")
                
                st.balloons()
            else:
                st.error("❌ 未查询到该渠道资格信息")

with tab2:
    st.subheader("后台补充认证数据（需密码）")
    pwd = st.text_input("输入管理密码", type="password")
    code = st.text_input("渠道公式名称（必填）")
    level = st.selectbox("资格等级", ["SCTA", "SCTP", "SCTE"])
    level_map = {"SCTA": "初级", "SCTP": "中级", "SCTE": "高级"}
    level_name = level_map[level]
    
    if st.button("添加认证数据"):
        if pwd != ADMIN_PASSWORD:
            st.error("❌ 密码错误！")
        elif not code:
            st.error("⚠️ 请输入渠道公式名称！")
        else:
            result = add_data(code, level, level_name)
            if result:
                st.success(f"✅ 成功添加：{code} → {level_name}({level})")
                st.rerun()
            else:
                st.error("❌ 该公式名称已存在，请勿重复添加！")

st.markdown("---")
st.caption("📌 本系统仅限深信服托管云渠道内部使用")