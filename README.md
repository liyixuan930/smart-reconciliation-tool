# 智能对账工具

## 功能
- 上传银行流水和财务账Excel
- 自动按金额匹配交易
- 展示匹配成功与异常记录
- AI分析异常交易可能原因

## 技术难点与解决方案

### 难点1：整数溢出导致页面崩溃
- **现象**：银行流水号（如20230401100100000）过长，Streamlit渲染时报错“int too big to convert”
- **解决过程**：
  1. 尝试将金额列转为float，但流水号仍报错
  2. 查阅资料后，采用“展示与计算分离”思路：读取时所有列先转为字符串（`dtype=str`）
  3. 匹配时单独将金额列转为数值（`pd.to_numeric`）
  4. 展示时使用字符串版本，彻底避免溢出
- **收获**：深入理解了数据类型与前端渲染的关系

### 难点2：AI API版本不兼容
- **现象**：按旧版文档写`zhipuai.model_api.invoke()`，报错`AttributeError: module 'zhipuai' has no attribute 'model_api'`
- **解决过程**：
  1. 查阅智谱AI官方文档，发现SDK已升级到v2
  2. 改用新版调用方式：`client.chat.completions.create()`
  3. 修改prompt结构为messages格式
- **收获**：学会了阅读官方文档和适配API变更

## 技术栈
- Python + pandas + Streamlit
- 智谱AI API

## 如何运行
1. 安装依赖：`pip install pandas openpyxl streamlit zhipuai`
2. 运行：`streamlit run app.py`
3. 上传示例Excel文件即可

## 演示视频

[智能对账工具 | 银行流水 VS 财务账 | AI自动匹配+异常分析](https://www.bilibili.com/video/BV1wY9FBuErY?vd_source=b76564aa9e293a9390d03cda6f099a86)

## 未来改进方向
- 增加日期+金额双重匹配，提高准确率
- 添加可视化图表，展示每日对账成功率趋势
- 支持多语言分析结果（中/英文）
- 支持导出对账报告为 Excel 或 PDF
