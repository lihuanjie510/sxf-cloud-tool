import streamlit as st
import pandas as pd
import datetime
import os

# ===================== 路径初始化 =====================
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
QUALIFY_FILE = os.path.join(DATA_FOLDER, "qualify_data.xlsx")
APPLY_FILE = os.path.join(DATA_FOLDER, "apply_data.xlsx")
CONFIG_FILE = os.path.join(DATA_FOLDER, "config.xlsx")

# ===================== 初始化表结构 =====================
def init_files():
    # 核心认证表（匹配业务字段）
    if not os.path.exists(QUALIFY_FILE):
        cols = [
            "code",
            "渠道名称",
            "区域",
            "认证是否有效",
            "认证等级",
            "别名",
            "姓名",
            "手机号",
            "证书编号",
            "证书有效期",
            "录入时间",
            "备注"
        ]
        pd.DataFrame(columns=cols).to_excel(QUALIFY_FILE, index=False)

    # 报名表
    if not os.path.exists(APPLY_FILE):
        apply_cols = [
            "单位名称","姓名","手机号","邮箱","身份证后四位",
            "申请认证等级","报名时间","状态","审核时间","管理员备注"
        ]
        pd.DataFrame(columns=apply_cols).to_excel(APPLY_FILE, index=False)

    # 配置表（管理员密码）
    if not os.path.exists(CONFIG_FILE):
        pd.DataFrame([{"key":"admin_pwd","value":"123456"}]).to_excel(CONFIG_FILE, index=False)

def load_df(file):
    try:
        return pd.read_excel(file, dtype=str)
    except:
        return pd.DataFrame()

def save_df(file, df):
    df.to_excel(file, index=False)

init_files()

# ===================== 公共方法 =====================
def get_admin_pwd():
    df = load_df(CONFIG_FILE)
    return df[df["key"]=="admin_pwd"]["value"].values[0] if not df.empty else "123456"

def save_admin_pwd(new_pwd):
    df = load_df(CONFIG_FILE)
    df.loc[df["key"]=="admin_pwd", "value"] = new_pwd
    save_df(CONFIG_FILE, df)

def add_qualify_full(data):
    df = load_df(QUALIFY_FILE)
    if str(data["code"]).strip() in df["code"].astype(str).str.strip().values:
        return False
    data["录入时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_df(QUALIFY_FILE, df)
    return True

def batch_import_qualify(df_upload):
    df = load_df(QUALIFY_FILE)
    existing = df["code"].astype(str).str.strip().values
    new_data = df_upload[~df_upload["code"].astype(str).str.strip().isin(existing)].copy()
    new_data["录入时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data["备注"] = new_data.get("备注", "")
    df = pd.concat([df, new_data], ignore_index=True)
    save_df(QUALIFY_FILE, df)
    return len(new_data)

def save_apply(data):
    df = load_df(APPLY_FILE)
    if str(data["手机号"]).strip() in df["手机号"].astype(str).str.strip().values:
        return False
    data["报名时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data["状态"] = "待审核"
    data["审核时间"] = ""
    data["管理员备注"] = ""
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_df(APPLY_FILE, df)
    return True

# ===================== 页面样式 =====================
st.set_page_config(page_title="深信服托管云认证管理系统", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.main { background: #f5f7fa; }
.card { background: white; padding: 24px; border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.06); margin-bottom:20px; }
.stat-card { background: white; padding: 20px; border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); text-align: center; }
.stButton>button { background:#004682; color:white; border-radius:8px; font-size:15px; }
</style>
""", unsafe_allow_html=True)

# ===================== 页面内容 =====================
st.title("🤖 深信服托管云认证管理系统")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 资格查询","📖 认证流程","📝 报名开通","⚙️ 管理后台"])

# 1. 资格查询
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏅 渠道资格查询")
    code = st.text_input("请输入渠道编号（如 QD001）")
    if st.button("立即查询"):
        if not code:
            st.warning("请输入渠道编号")
        else:
            df = load_df(QUALIFY_FILE)
            res = df[df["code"].astype(str).str.strip() == str(code).strip()]
            if len(res) > 0:
                r = res.iloc[0]
                st.success(f"✅ 查询成功：{code}")
                col1, col2 = st.columns(2)
                col1.info(f"渠道名称：{r.get('渠道名称','无')}")
                col2.info(f"区域：{r.get('区域','无')}")
                col1.info(f"认证状态：{r.get('认证是否有效','无')}")
                col2.info(f"认证等级：{r.get('认证等级','无')}")
                col1.info(f"联系人：{r.get('姓名','无')}")
                col2.info(f"手机号：{r.get('手机号','无')}")
                col1.info(f"证书编号：{r.get('证书编号','无')}")
                col2.info(f"证书有效期：{r.get('证书有效期','无')}")
                st.balloons()
            else:
                st.error("❌ 未查询到该渠道信息")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. 认证流程
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 托管云认证流程说明")
    st.markdown("""
    ### 一、报名方式
    1. **在线链接**：[https://www.wjx.cn/vm/wBFmQyO.aspx#](https://www.wjx.cn/vm/wBFmQyO.aspx#)  
    2. **微信扫码**：（扫码后填写报名信息）  
    3. **线下提交**：提供单位名称、姓名、手机号、邮箱、身份证后4位至渠道经理

    ### 二、认证流程（免费）
    **线上报名 → 在线课程学习 → 实验练习 → 知识自检 → 认证考核 → 颁发证书**

    ### 三、认证形式
    - 初级（SCTA）：笔试 + 初级实验  
    - 中级（SCTP）：笔试 + 中级实验  
    - 高级（SCTE）：笔试 + 线上面试  

    ### 四、⚠️ 重要注意事项
    1. 认证需从初级到高级，不可直接考高级；过期需重考，流程与新考一致  
    2. 课程无截止时间，视频/实验可按需学习；实验暂不支持在线模拟，需联系李换杰经理获取练习环境  
    3. 笔试未通过需联系渠道经理重置成绩；笔试通过后，初中级实验/高级面试需提前1天预约（提供笔试截图、认证级别、邮箱、考试时间）  
    4. 考试70分通过：初中级3次补考机会，高级1次；连续未过需3个月后重考  
    5. 初中级笔试3小时（等保组件+平台操作+RDS+监控）；初级实验2小时，中级实验3小时（1天内未完成视为未通过）  
    6. 高级面试15分钟（计算机基础+平台操作）
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. 报名开通
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 在线报名")
    with st.form("apply_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("单位名称（全称）*")
            name = st.text_input("姓名 *")
            phone = st.text_input("手机号 *")
        with col2:
            email = st.text_input("邮箱 *")
            id_last4 = st.text_input("身份证后4位 *")
            apply_level = st.selectbox("申请认证等级", ["初级（SCTA）", "中级（SCTP）", "高级（SCTE）"])
        submitted = st.form_submit_button("提交报名信息")
        
        if submitted:
            if not all([company, name, phone, email, id_last4]):
                st.error("请填写完整所有必填项（带 * 为必填）")
            else:
                apply_data = {
                    "单位名称": company, "姓名": name, "手机号": phone,
                    "邮箱": email, "身份证后四位": id_last4, "申请认证等级": apply_level
                }
                ok = save_apply(apply_data)
                if ok:
                    st.success("✅ 报名成功！管理员将在1-3个工作日内审核并开通账号")
                else:
                    st.warning("⚠️ 该手机号已提交过报名，请勿重复提交")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. 管理后台
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pwd_input = st.text_input("请输入管理员密码", type="password")
    correct_pwd = get_admin_pwd()

    if pwd_input == correct_pwd:
        st.success("✅ 管理员已登录")
        df_qualify = load_df(QUALIFY_FILE)
        df_apply = load_df(APPLY_FILE)

        # 统计面板
        st.subheader("📊 数据统计中心")
        total_qualify = len(df_qualify)
        valid_qualify = len(df_qualify[df_qualify["认证是否有效"] == "是"]) if "认证是否有效" in df_qualify.columns else 0
        total_apply = len(df_apply)
        waiting_apply = len(df_apply[df_apply["状态"] == "待审核"]) if "状态" in df_apply.columns else 0
        scta = len(df_qualify[df_qualify["认证等级"] == "SCTA"]) if "认证等级" in df_qualify.columns else 0
        sctp = len(df_qualify[df_qualify["认证等级"] == "SCTP"]) if "认证等级" in df_qualify.columns else 0
        scte = len(df_qualify[df_qualify["认证等级"] == "SCTE"]) if "认证等级" in df_qualify.columns else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("总认证数", total_qualify)
        col2.metric("有效认证", valid_qualify)
        col3.metric("总报名数", total_apply)
        col4.metric("待审核报名", waiting_apply)

        colA, colB, colC = st.columns(3)
        colA.metric("初级（SCTA）", scta)
        colB.metric("中级（SCTP）", sctp)
        colC.metric("高级（SCTE）", scte)
        st.markdown("---")

        # 子标签页
        tab_a, tab_b, tab_c, tab_d = st.tabs(["1⃣ 单条开通","2⃣ 批量导入","3⃣ 数据列表","4⃣ 系统设置"])

        # 单条开通
        with tab_a:
            st.subheader("新增认证账号")
            with st.form("add_form"):
                col1, col2 = st.columns(2)
                with col1:
                    code = st.text_input("渠道编号（如 QD001）*")
                    channel_name = st.text_input("渠道名称 *")
                    area = st.text_input("区域")
                    cert_valid = st.selectbox("认证是否有效", ["是", "否"])
                    level = st.selectbox("认证等级", ["SCTA", "SCTP", "SCTE"])
                with col2:
                    alias = st.text_input("别名")
                    name = st.text_input("联系人姓名")
                    phone = st.text_input("联系人手机号")
                    cert_no = st.text_input("证书编号")
                    cert_expire = st.text_input("证书有效期（YYYY-MM-DD）")
                remark = st.text_input("备注（可选）")
                if st.form_submit_button("添加并开通"):
                    if not (code and channel_name):
                        st.error("渠道编号和渠道名称为必填项")
                    else:
                        qualify_data = {
                            "code": code, "渠道名称": channel_name, "区域": area,
                            "认证是否有效": cert_valid, "认证等级": level, "别名": alias,
                            "姓名": name, "手机号": phone, "证书编号": cert_no,
                            "证书有效期": cert_expire, "备注": remark
                        }
                        res = add_qualify_full(qualify_data)
                        if res:
                            st.success(f"✅ 账号 {code} 开通成功")
                            st.rerun()
                        else:
                            st.error("❌ 该渠道编号已存在")

        # 批量导入
        with tab_b:
            st.subheader("Excel批量导入认证账号")
            st.markdown("**导入模板要求**：需包含以下列（顺序不限）：")
            st.code("code（渠道编号）、渠道名称、区域、认证是否有效、认证等级、别名、姓名、手机号、证书编号、证书有效期")
            uploaded = st.file_uploader("上传Excel文件（.xlsx格式）", type=["xlsx"])
            if uploaded and st.button("确认导入"):
                try:
                    df_upload = pd.read_excel(uploaded, dtype=str)
                    required_cols = ["code", "渠道名称"]
                    if all(col in df_upload.columns for col in required_cols):
                        cnt = batch_import_qualify(df_upload)
                        st.success(f"✅ 导入成功！新增 {cnt} 条认证数据")
                        st.rerun()
                    else:
                        st.error(f"❌ 导入失败：Excel需包含 'code' 和 '渠道名称' 列")
                except Exception as e:
                    st.error(f"❌ 导入失败：{str(e)}")

        # 数据列表
        with tab_c:
            st.subheader("📋 认证账号列表")
            st.dataframe(df_qualify, use_container_width=True)
            st.download_button("导出认证数据", df_qualify.to_excel(index=False), file_name="深信服认证账号列表.xlsx")

            st.subheader("📋 报名信息列表")
            st.dataframe(df_apply, use_container_width=True)
            st.download_button("导出报名数据", df_apply.to_excel(index=False), file_name="深信服报名信息列表.xlsx")

        # 系统设置
        with tab_d:
            st.subheader("🔧 修改管理员密码")
            old_pwd = st.text_input("原密码", type="password")
            new_p1 = st.text_input("新密码", type="password")
            new_p2 = st.text_input("确认新密码", type="password")
            if st.button("更新密码"):
                if old_pwd != correct_pwd:
                    st.error("❌ 原密码输入错误")
                elif new_p1 != new_p2:
                    st.error("❌ 两次新密码输入不一致")
                elif not new_p1:
                    st.error("❌ 新密码不能为空")
                else:
                    save_admin_pwd(new_p1)
                    st.success("✅ 密码更新成功！下次登录请使用新密码")

    elif pwd_input != "":
        st.error("❌ 管理员密码错误")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("📌 系统版本：V1.0 | 技术支持：深信服渠道管理团队")
