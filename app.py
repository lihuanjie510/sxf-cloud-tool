import streamlit as st
import pandas as pd
import datetime

# -------------------------- 云端数据存储（Streamlit 官方） --------------------------
def init_cloud_data():
    if "qualify_data" not in st.session_state:
        st.session_state.qualify_data = pd.DataFrame(columns=["code", "level", "level_name", "create_time"])
    if "apply_data" not in st.session_state:
        st.session_state.apply_data = pd.DataFrame(columns=["name","phone","company","email","id_last4","apply_time","status","code"])

init_cloud_data()
ADMIN_PASSWORD = "123456"

# -------------------------- 页面样式 --------------------------
st.set_page_config(page_title="深信服托管云渠道机器人", page_icon="🤖", layout="wide")
st.markdown("""
<style>
    .main { background: #f5f7fa; }
    .card { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom:20px; }
    .stButton>button { background:#004682; color:white; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# -------------------------- 功能函数 --------------------------
def add_qualify_data(code, level, level_name):
    df = st.session_state.qualify_data
    if code in df["code"].astype(str).values:
        return False
    new_row = {
        "code": code,
        "level": level,
        "level_name": level_name,
        "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df.loc[len(df)] = new_row
    st.session_state.qualify_data = df
    return True

def save_apply(name, phone, company, email, id_last4):
    df = st.session_state.apply_data
    new_row = {
        "name": name,
        "phone": phone,
        "company": company,
        "email": email,
        "id_last4": id_last4,
        "apply_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待审核",
        "code": ""
    }
    df.loc[len(df)] = new_row
    st.session_state.apply_data = df

# -------------------------- 页面 --------------------------
st.title("🤖 深信服托管云渠道机器人")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 资格查询","📖 认证流程","📝 报名开通","⚙️ 管理后台"])

with tab1:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏅 渠道资格查询")
        code = st.text_input("渠道公式名称")
        if st.button("立即查询"):
            df = st.session_state.qualify_data
            res = df[df["code"].astype(str).str.strip() == str(code).strip()]
            if len(res) > 0:
                r = res.iloc[0]
                st.success(f"✅ 有效账号：{code}")
                st.info(f"等级：{r['level_name']} ({r['level']})")
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
        with st.form("apply"):
            c1,c2 = st.columns(2)
            with c1:
                company = st.text_input("单位名称（全称） *")
                name = st.text_input("姓名 *")
                phone = st.text_input("手机号码 *")
            with c2:
                email = st.text_input("邮箱 *")
                id_last4 = st.text_input("身份证后四位 *")
            if st.form_submit_button("提交报名信息"):
                if name and phone and company and email and id_last4:
                    save_apply(name, phone, company, email, id_last4)
                    st.success("✅ 报名信息提交成功！\n\n已收到您的资料，管理员将尽快为您开通学习考试账号！")
                else:
                    st.error("⚠️ 请填写完整所有必填信息！")
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        pwd = st.text_input("管理员密码", type="password")
        if pwd == ADMIN_PASSWORD:
            st.success("✅ 管理员已登录")
            st.subheader("1. 开通认证账号")
            with st.form("add"):
                code = st.text_input("渠道公式名称")
                level = st.selectbox("等级", ["SCTA","SCTP","SCTE"])
                name_map = {"SCTA":"初级","SCTP":"中级","SCTE":"高级"}
                if st.form_submit_button("添加并开通"):
                    if code:
                        res = add_qualify_data(code, level, name_map[level])
                        if res:
                            st.success(f"✅ {code} 开通成功")
                        else:
                            st.error("❌ 已存在")
            st.subheader("2. 报名列表")
            st.dataframe(st.session_state.apply_data, use_container_width=True)
            st.subheader("3. 已开通账号")
            st.dataframe(st.session_state.qualify_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("📌 深信服托管云渠道专用系统 | 内部使用")
