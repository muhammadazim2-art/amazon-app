import streamlit as st
import pandas as pd

st.set_page_config(page_title="亚马逊数据看板", layout="wide") # 🔥 小彩蛋：把网页变宽，更像大屏

st.title('📊 亚马逊店铺爆款分析器 v0.5 (全能筛选版)')

uploaded_file = st.file_uploader("请上传销售报表 (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # 1. 读取文件
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file)
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='gbk')
        else:
            df = pd.read_excel(uploaded_file)
            
        # -------------------------------------------------------
        # 🔥 改动 1：构造包含“所有日期”的选项列表
        # list(...) 是为了把 numpy 数组转成普通列表，才能和 ['所有日期'] 相加
        # -------------------------------------------------------
        all_dates = ['所有日期'] + list(df['Date'].unique())
        
        st.sidebar.header("🔍 筛选条件")
        selected_date = st.sidebar.selectbox("请选择日期", all_dates)
        
        # -------------------------------------------------------
        # 🔥 改动 2：智能判断逻辑
        # -------------------------------------------------------
        if selected_date == '所有日期':
            # 如果选了所有，就不筛选，直接用 df
            filtered_df = df
            period_name = "所有历史数据"
        else:
            # 如果选了某一天，就按日期筛选
            filtered_df = df[df['Date'] == selected_date]
            period_name = selected_date
        
        # 计算销售额 (这一步不管筛没筛选，都要算)
        filtered_df['Total_Sales'] = filtered_df['Price'] * filtered_df['Amount']
        
        # -------------------------------------------------------
        # 后面所有的展示，都基于 filtered_df (它可能是某一天，也可能是全部)
        # -------------------------------------------------------
        
        # 1. 核心指标 KPI
        total_revenue = filtered_df['Total_Sales'].sum()
        total_quantity = filtered_df['Amount'].sum()
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 总销售额", f"¥{total_revenue:,.2f}")
        with col2:
            st.metric("📦 总销量", f"{total_quantity} 件")
        st.divider()

        # 2. 只有当看“所有日期”时，展示每天的趋势图 (这在单日视角下没意义)
        if selected_date == '所有日期':
            st.subheader("📈 每日销售趋势")
            # 按日期分组看每天卖了多少钱
            daily_trend = filtered_df.groupby('Date')['Total_Sales'].sum()
            st.line_chart(daily_trend)

        # 3. 商品排行榜
        result_df = filtered_df.groupby('SKU')['Total_Sales'].sum().reset_index()
        sorted_df = result_df.sort_values(by='Total_Sales', ascending=False)
        top_5 = sorted_df.head(5)
        
        st.subheader(f"🏆 {period_name} 热销榜单")
        
        # 这里把图表和表格左右排布，更好看
        c1, c2 = st.columns([2, 1]) # 左边图表占2份宽，右边表格占1份宽
        with c1:
            st.bar_chart(top_5, x='SKU', y='Total_Sales')
        with c2:
            st.dataframe(top_5, hide_index=True) # hide_index=True 可以隐藏左边那列 0,1,2,3 序号
        
    except Exception as e:
        st.error(f"发生错误：{e}")
else:
    st.info("👆 请上传文件")