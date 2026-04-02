import streamlit as st
import pandas as pd
import zhipuai
from zhipuai import ZhipuAI

# ========== 页面配置 ==========
st.set_page_config(page_title="智能对账工具", layout="wide")
st.title("🤖 智能对账工具")
st.markdown("上传银行流水与财务账,自动按金额匹配,AI分析异常原因")

# ========== 文件上传 ==========
col1, col2 = st.columns(2)
with col1:
    uploaded_bank = st.file_uploader("📂 上传银行流水", type=["xlsx", "xls"])
with col2:
    uploaded_account = st.file_uploader("📂 上传财务账", type=["xlsx", "xls"])

if uploaded_bank and uploaded_account:
    # 读取所有列为字符串，避免整数溢出
    bank_raw = pd.read_excel(uploaded_bank,dtype=str)
    account_raw = pd.read_excel(uploaded_account,dtype=str)

    # 金额列名（根据实际列名修改）
    amount_col = "金额"

    # 制作数值副本用于匹配
    bank_num = bank_raw.copy()
    account_num = account_raw.copy()
    bank_num[amount_col] = pd.to_numeric(bank_num[amount_col], errors='coerce')
    account_num[amount_col] = pd.to_numeric(account_num[amount_col], errors='coerce')

    # 按金额匹配
    matched_num = bank_num.merge(account_num, on=amount_col, how="inner")
    unmatched_bank_num = bank_num[~bank_num[amount_col].isin(account_num[amount_col])]

    # 用索引筛选原始字符串数据用于展示
    matched = bank_raw.loc[matched_num.index]
    unmatched_bank = bank_raw.loc[unmatched_bank_num.index]

    # ========== 展示指标 ==========
    total_bank = len(bank_raw)
    match_rate = len(matched) / total_bank if total_bank > 0 else 0
    st.metric("📊 匹配成功率", f"{match_rate:.1%}")
    
    # ========== Tab 展示结果 ==========
    tab1, tab2 = st.tabs(["✅ 匹配成功", "⚠️ 未匹配"])
    with tab1:
        st.write(f"共 {len(matched)} 条")
        st.dataframe(matched)
    with tab2:
        st.write(f"共 {len(unmatched_bank)} 条")
        if len(unmatched_bank) > 0:
            st.dataframe(unmatched_bank)
        else:
            st.info("全部匹配成功，无异常")

    # ========== AI 分析 ==========
    st.divider()
    st.subheader("🧠 AI 智能分析")
    
    # 初始化 AI 客户端
    client = ZhipuAI(api_key="9bd388bb4f004529ab95f3e69e31fd61.bQIj14sT29ZtzRzH")  
    
    if st.button("🔍 分析未匹配原因"):
        if len(unmatched_bank) > 0:
            # 获取商户名(根据实际列名修改)
            merchant_col = "交易对手"  # 改成实际列名
            if merchant_col in unmatched_bank.columns:
                merchants = unmatched_bank[merchant_col].tolist()
                merchants_text = "、".join(str(m) for m in merchants[:10])
                prompt = f"以下银行交易在财务账上未匹配到,请分析可能原因(如未及时记账、商户名不一致等):\n{merchants_text}"
            else:
                prompt = "未匹配交易存在,但缺少商户名信息,无法具体分析."
            
            try:
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                ai_answer = response.choices[0].message.content
                st.success("分析结果:")
                st.write(ai_answer)
            except Exception as e:
                st.error(f"AI 调用失败:{e}")
        else:
            st.info("无未匹配交易，无需分析")