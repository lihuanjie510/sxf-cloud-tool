import streamlit as st
import pandas as pd
import datetime
import os
import re

# -------------------------- 企业版：本地文件永久存储 --------------------------
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

QUALIFY_FILE = os.path.join(DATA_FOLDER, "qualify_data.xlsx")
APPLY_FILE = os.path.join(DATA_FOLDER, "apply_data.xlsx")
CONFIG_FILE = os.path.join(DATA_FOLDER, "config.xlsx")

# 初始化文件
def init_files():
    if not os.path.exists(QUALIFY_FILE):
        pd.DataFrame(columns=["code","level","level_name","create_time"]).to_excel(QUALIFY_FILE, index=False)
    if not os.path.exists(APPLY_FILE):
        pd.DataFrame(columns=["company","name","phone","email","id_last4","apply_time","status","admin_note"]).to_excel(APPLY_FILE, index=False)
    if not os.path.exists(CONFIG_FILE):
        pd.DataFrame([{"key":"admin_pwd","value":"123456"}]).to_excel(CONFIG_FILE, index=False)

# 读取/保存数据
def load_df(file):
    try:
        return pd.read_excel(file)
    except:
        return pd.DataFrame()

def save_df(file, df):
    df.to_excel(file, index=False)

init_files()

# -------------------------- 核心功能 --------------------------
def get_admin_pwd():
    df = load_df(CONFIG_FILE)
    return df[df["key"]=="admin_pwd"]["value"].values[0]

def save_admin_pwd(new_pwd):
    df = load_df(CONFIG_FILE)
    df.loc[df["key"]=="admin_pwd", "value"] = new_pwd
    save_df(CONFIG_FILE, df)

def add_qualify(code, level, level_name):
    df = load_df(QUALIFY_FILE)
    if str(code).strip() in df["code"].astype(str).str.strip().values:
        return False
    new_row = {"code":code,"level":level,"level_name":level_name,"create_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(QUALIFY_FILE, df)
    return True

def batch_import_qualify(df_upload):
    df = load_df(QUALIFY_FILE)
    existing = df["code"].astype(str).str.strip().values
    new_data = df_upload[~df_upload["code"].astype(str).str.strip().isin(existing)]
    df = pd.concat([df, new_data], ignore_index=True)
    save_df(QUALIFY_FILE, df)
    return len(new_data)

def save_apply(company, name, phone, email, id_last4):
    df = load_df(APPLY_FILE)
    phone_exist = str(phone).strip() in df["phone"].astype(str).str.strip().values
    if phone_exist:
        return False
    new_row = {
        "company":company,"name":name,"phone":phone,"email":email,"id_last4":id_last4,
        "apply_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status":"待审核","admin_note":""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_df(APPLY_FILE, df)
    return True

# -------------------------- 页面样式 --------------------------
st.set_page_config(page_title="深信服托管云渠道机器人", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.main { background: #f5f7fa; }
.card { background: white; padding: 24px; border-radius: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.06); margin-bottom:20px; }
.stat-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    text-align: center;
}
.stButton>button { 
    background:#004682; 
    color:white; 
    border-radius:8px;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- 界面 --------------------------
st.title("🤖 深信服托管云渠道机器人")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 资格查询","📖 认证流程","📝 报名开通","⚙️ 管理后台"])

with tab1:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏅 渠道资格查询")
        code = st.text_input("渠道公式名称")
        if st.button("立即查询"):
            if not code:
                st.warning("请输入渠道编号")
            else:
                df = load_df(QUALIFY_FILE)
                res = df[df["code"].astype(str).str.strip() == str(code).strip()]
                if len(res) > 0:
                    r = res.iloc[0]
                    st.success(f"✅ 有效账号：{code}")
                    st.info(f"等级：{r['level_name']}（{r['level']}）")
                    st.balloons()
                else:
                    st.error("❌ 未查询到信息")
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📖 托管云认证流程说明")
        st.markdown("""
您好，有需要托管云认证的同事可以通过在线链接或微信扫码形式进行托管云认证课程报名，报名后同步下我及时给大家开通学习账号

**在线链接**：https://www.wjx.cn/vm/wBFmQyO.aspx#
**微信扫码**：（请使用微信扫描上方二维码报名）

或者有需要认证的同事,直接将公司名称全称、姓名、电话、邮箱、身份证后4位请提供下
单位名称：
姓名：
手机号码：
邮箱：
身份证后四位:
请报完名后通知下我 这边开通学习考试账号

---
## 托管云认证流程（免费认证）
线上报名->在线课程学习->线上实验练习->知识自检->认证考核->颁发证书

## 认证形式：
PT1（SCTA）初级笔试+初级实验
PT2（SCTP）中级笔记+中级实验
PT3（SCTE）高级笔试+线上面试

---
## ⚠️ 请仔细阅读下面注意事项！！！！！！！！！
认证必须从初级到高级，不能直接考高级的,之前认证过期了需要重考,重考和新考的流程是一样的

当前所有认证都是线上形式，课程没有设置截止时间，课程中的视频和实验不要求全部完成，里面的内容都是分版块的，大家可以根据需要自行查漏补缺选择学习

课程上面的实验当前暂时无法在线模拟使用，但可以点开查看学习左边的实验手册，如果想要实战练习，可以联系渠道经理李换杰获取练习环境

课程最后会有笔试，课程最后的笔试若未通过，需要联系渠道经理重置考试成绩，才能再次进行考试，笔试通过后，初中级实验和高级面试需要单独找渠道经理李换杰预约下哈，预约请提供笔试通过的截图，说明要认证的级别并提供邮箱和考试时间（至少要提前一天预约）后会发送考试通知

托管云相关考试都是70分通过，初中各三次补考机会，高级一次机会，若连续未过，需要等三个月后才能重新认证

初中级笔试都是3小时，涉及到等保组件+平台基础操作+RDS+监控告警配置

初级实验是2小时，中级实验是3小时，收到考试通知后，1天内未完成考试视为考试未通过，环境会被重置，需要重新预约考试

高级面试线上进行，预计15分钟，涉及到计算机基础知识+平台基础操作
""")
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 托管云认证报名")
        with st.form("apply_form"):
            c1, c2 = st.columns(2)
            with c1:
                company = st.text_input("单位名称（全称）*")
                name = st.text_input("姓名 *")
                phone = st.text_input("手机号码 *")
            with c2:
                email = st.text_input("邮箱 *")
                id_last4 = st.text_input("身份证后四位 *")
            submitted = st.form_submit_button("提交报名信息")
            
            if submitted:
                if not all([company,name,phone,email,id_last4]):
                    st.error("请填写完整信息")
                else:
                    ok = save_apply(company,name,phone,email,id_last4)
                    if ok:
                        st.success("✅ 报名成功！资料已收到，将尽快为您开通账号")
                    else:
                        st.warning("⚠️ 该手机号已报名，请勿重复提交")
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        pwd_input = st.text_input("管理员密码", type="password")
        correct_pwd = get_admin_pwd()

        if pwd_input == correct_pwd:
            st.success("✅ 管理员已登录")

            # ==============================================
            # 📊 【新增】数据统计面板
            # ==============================================
            st.subheader("📊 数据统计中心")
            df_apply = load_df(APPLY_FILE)
            df_qualify = load_df(QUALIFY_FILE)

            total_apply = len(df_apply)
            waiting = len(df_apply[df_apply["status"] == "待审核"]) if "status" in df_apply.columns else 0
            total_account = len(df_qualify)
            
            scta = len(df_qualify[df_qualify["level"] == "SCTA"])
            sctp = len(df_qualify[df_qualify["level"] == "SCTP"])
            scte = len(df_qualify[df_qualify["level"] == "SCTE"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='stat-card'><h3>{total_apply}</h3><p>总报名人数</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='stat-card'><h3>{waiting}</h3><p>待审核人数</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='stat-card'><h3>{total_account}</h3><p>已开通账号</p></div>", unsafe_allow_html=True)

            colA, colB, colC = st.columns(3)
            with colA:
                st.markdown(f"<div class='stat-card'><h3>{scta}</h3><p>初级 SCTA</p></div>", unsafe_allow_html=True)
            with colB:
                st.markdown(f"<div class='stat-card'><h3>{sctp}</h3><p>中级 SCTP</p></div>", unsafe_allow_html=True)
            with colC:
                st.markdown(f"<div class='stat-card'><h3>{scte}</h3><p>高级 SCTE</p></div>", unsafe_allow_html=True)

            st.markdown("---")

            # 子菜单
            tab_a, tab_b, tab_c, tab_d = st.tabs([
                "1⃣ 开通账号",
                "2⃣ 批量导入",
                "3⃣ 数据列表",
                "4⃣ 系统设置"
            ])

            with tab_a:
                st.subheader("单个开通认证账号")
                with st.form("add_form"):
                    code = st.text_input("渠道公式名称")
                    level = st.selectbox("等级", ["SCTA","SCTP","SCTE"])
                    level_map = {"SCTA":"初级","SCTP":"中级","SCTE":"高级"}
                    if st.form_submit_button("添加并开通"):
                        if code:
                            res = add_qualify(code, level, level_map[level])
                            if res:
                                st.success(f"✅ {code} 开通成功")
                            else:
                                st.error("❌ 编号已存在")

            with tab_b:
                st.subheader("Excel批量导入账号")
                st.caption("模板列：code、level、level_name")
                uploaded = st.file_uploader("上传Excel", type=["xlsx"])
                if uploaded and st.button("确认导入"):
                    df_upload = pd.read_excel(uploaded)
                    cnt = batch_import_qualify(df_upload)
                    st.success(f"✅ 导入成功 {cnt} 条新数据")

            with tab_c:
                st.subheader("用户报名列表（可导出）")
                st.dataframe(df_apply, use_container_width=True)
                st.download_button("导出报名数据", df_apply.to_excel(index=False), file_name="报名列表.xlsx")

                st.subheader("已开通资格列表")
                st.dataframe(df_qualify, use_container_width=True)
                st.download_button("导出资格数据", df_qualify.to_excel(index=False), file_name="资格列表.xlsx")

            with tab_d:
                st.subheader("修改管理员密码")
                new_p1 = st.text_input("新密码", type="password")
                new_p2 = st.text_input("确认新密码", type="password")
                if st.button("更新密码"):
                    if new_p1 == new_p2 and new_p1 != "":
                        save_admin_pwd(new_p1)
                        st.success("✅ 密码已修改")
                    else:
                        st.error("两次密码不一致")

        elif pwd_input != "":
            st.error("密码错误")
        st.markdown("</div>", unsafe_allow_html=True)

st.caption("📌 深信服托管云渠道专用系统 | 企业正式版")
