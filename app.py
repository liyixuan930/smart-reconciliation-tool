import streamlit as st
import pandas as pd

st.title("智能对账工具")

uploaded_bank = st.file_uploader("上传银行流水", type=["xlsx", "xls"])
uploaded_account = st.file_uploader("上传财务账", type=["xlsx", "xls"])

if uploaded_bank and uploaded_account:
    # 读取 Excel
    bank = pd.read_excel(uploaded_bank)
    account = pd.read_excel(uploaded_account)

    # 保存原始金额列用于匹配（假设列名为“金额”，如果不是请修改）
    amount_col = "金额"   # ← 这里改成你实际的金额列名（如果不同）
    
    # 按金额匹配（使用原始数值）
    matched = bank.merge(account, on=amount_col, how="inner")
    unmatched_bank = bank[~bank[amount_col].isin(account[amount_col])]
    
    # 将所有数值列（包括整数和浮点数）转换为字符串，避免 Arrow 转换报错
    def convert_numeric_to_str(df):
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].astype(str)
        return df
    
    # 转换要显示的 DataFrame
    matched_display = convert_numeric_to_str(matched.copy())
    unmatched_bank_display = convert_numeric_to_str(unmatched_bank.copy())
    
    st.write(f"✅ 匹配成功：{len(matched)} 条")
    st.dataframe(matched_display)
    
    st.write(f"⚠️ 银行侧未匹配：{len(unmatched_bank)} 条")
    if len(unmatched_bank) > 0:
        st.dataframe(unmatched_bank_display)

# 导入新版SDK
from zhipuai import ZhipuAI

# 初始化客户端（用你的API Key）
client = ZhipuAI(api_key="9bd388bb4f004529ab95f3e69e31fd61.bQIj14sT29ZtzRzH")  

# 添加按钮
if st.button("🤖 AI 分析未匹配交易"):
    if len(unmatched_bank) > 0:
        # 获取未匹配的商户名(根据你的Excel列名修改)
        merchant_col = "交易对手"
        if merchant_col in unmatched_bank.columns:
            merchants = unmatched_bank[merchant_col].tolist()
            merchants_text = "、".join(str(m) for m in merchants[:10])  
            prompt = f"以下是一些银行交易记录,但在财务账上没有匹配到.请分析可能的原因(例如未及时记账、商户名不一致、交易未入账等):\n{merchants_text}"
        else:
            # 如果没有商户名列,用金额列
            amount_col = "金额"
            if amount_col in unmatched_bank.columns:
                amounts = unmatched_bank[amount_col].tolist()
                amounts_text = "、".join(str(a) for a in amounts[:10])
                prompt = f"以下是一些银行交易金额,但在财务账上没有匹配到.请分析可能的原因:\n{amounts_text}"
            else:
                prompt = "未匹配的交易记录存在,但缺少商户名或金额信息,无法具体分析."

        try:
            # 新版API调用方式
            response = client.chat.completions.create(
                model="glm-4-flash",  # 使用免费模型,或者用 "glm-4"
                messages=[
                    {"role": "system", "content": "你是一个专业的财务分析助手."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            ai_answer = response.choices[0].message.content
            st.success("AI 分析结果:")
            st.write(ai_answer)
        except Exception as e:
            st.error(f"调用 AI 失败:{e}")
    else:
        st.info("没有未匹配的交易,无需分析.")