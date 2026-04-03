# 智能对账工具

## 功能
- 上传银行流水和财务账Excel
- 自动按金额匹配交易
- 展示匹配成功与异常记录
- AI分析异常交易可能原因

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
