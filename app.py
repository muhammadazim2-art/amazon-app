import streamlit as st
import pandas as pd
import plotly.express as px  # 🔥 新增

# ==========================================
# 1. 技能区 (Functions)
# ==========================================
#上传文件
@st.cache_data 
def load_data(file):
    if file.name.endswith('.csv'):
        try:
            return pd.read_csv(file)
        except:
            file.seek(0)
            return pd.read_csv(file, encoding='gbk')
    else:
        return pd.read_excel(file)
#计算核心值
def calculate_kpi(df):
    total_revenue = df['Total_Sales'].sum()
    total_quantity = df['Amount'].sum()
    return total_revenue, total_quantity
#绘图
def plot_charts(df):
    # 1. 折线图
    daily_trend = df.groupby('Date')['Total_Sales'].sum().reset_index()
    fig_trend = px.line(
        daily_trend, 
        x='Date', 
        y='Total_Sales',
        title="📈 每日销售趋势",
        markers=True, 
    )
    
    # 2. 甜甜圈图 (Pie Chart)
    sku_distribution = df.groupby('SKU')['Total_Sales'].sum().reset_index()
    fig_pie = px.pie(
        sku_distribution, 
        values='Total_Sales', 
        names='SKU', 
        title="🍰 各商品销售占比",
        hole=0.3, # 这里的数字 0.3 控制中间那个洞的大小
    )
    
    return fig_trend, fig_pie
#利润率自动生成建议
def generate_summary(revenue,profit,margin):
    summary=f'本期经营报告\n\n'
    summary+=f'总销售额达到了{revenue:,.2f}。\n'
    summary+=f'预估净利润为{profit:,.2f}(利润率{margin*100:.1f}%)。\n\n'
    if margin < 0.1:
        summary += "⚠️ **风险预警**：利润率低于 10%，建议检查广告支出或重新定价！"
    elif margin >= 0.3:
        summary += "🚀 **表现优异**：高利润产品，建议加大库存周转！"
    else:
        summary += "✅ **运营稳健**：利润率在正常区间，请保持当前策略。"
    return summary

   
# ==========================================
# 2. 主程序区 (Main App)
# ==========================================

st.set_page_config(page_title="亚马逊数据看板", layout="wide")
st.title('📊 亚马逊店铺爆款分析器 v0.7 (Plotly版)')

uploaded_file = st.file_uploader("请上传销售报表 (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        #侧边栏日期
        all_dates = ['所有日期'] + list(df['Date'].unique())
        st.sidebar.header("🔍 筛选条件")
        selected_date = st.sidebar.selectbox("请选择日期", all_dates)
        #侧边栏利润率滑块
        st.sidebar.divider()
        st.sidebar.header('利润分析')
        profit_margin=st.sidebar.slider('预估利润率(Profit Margin)',0.0,1.0,0.2)
        
        if selected_date == '所有日期':
            filtered_df = df
            period_name = "所有历史数据"
        else:
            filtered_df = df[df['Date'] == selected_date]
            period_name = selected_date
        
        filtered_df['Total_Sales'] = filtered_df['Price'] * filtered_df['Amount']
        filtered_df['Estimated_Profit'] = filtered_df['Total_Sales'] * profit_margin
        total_profit=filtered_df['Estimated_Profit'].sum()
        revenue, quantity = calculate_kpi(filtered_df)
        #智能分析
        st.info(generate_summary(revenue, total_profit, profit_margin))
        #核心指标卡
        st.divider()
        c1, c2 ,c3= st.columns(3)
        with c1:
            st.metric("💰 总销售额", f"¥{revenue:,.2f}")
        with c2:
            st.metric("📦 总销量", f"{quantity} 件")
        with c3:
            st.metric("¥ 预估净利润", f"¥{total_profit:,.2f}", f"利润率 {profit_margin*100}%")
        st.divider()

        # 🔥 调用绘图函数
        fig_1, fig_2 = plot_charts(filtered_df)
        
        # 左右布局展示图表
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_1, use_container_width=True)
        with col2:
            st.plotly_chart(fig_2, use_container_width=True)

        # 下面的表格逻辑不变
        result_df = filtered_df.groupby('SKU')['Total_Sales'].sum().reset_index()
        sorted_df = result_df.sort_values(by='Total_Sales', ascending=False)
        top_5 = sorted_df.head(5)
        
        st.subheader(f"🏆 {period_name} 热销榜单")
        st.dataframe(top_5, hide_index=True, use_container_width=True)

        #下载按钮
        csv=top_5.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下载榜单数据(CSV)",
            data=csv,
            file_name='top_5_products.csv'
            mime='text/csv' 
            )
            
    except Exception as e:
        st.error(f"发生错误：{e}")
else:
    st.info("👆 请上传文件")