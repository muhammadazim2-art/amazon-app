import streamlit as st
import pandas as pd
import plotly.express as px 
# 语言字典
# ==========================================
# 全量语言词库 (Translation Dictionary)
# ==========================================
LANG_DICT = {
    "zh": {
        "title": "📦 亚马逊爆款分析器 v0.7",
        "upload_label": "上传亚马逊销售报表 (CSV/Excel)",
        "sidebar_header": "📊 控制面板",
        "lang_select": "选择语言",
        "ad_setting": "广告与成本设置",
        "ad_spend": "本月广告总支出",
        "other_costs": "其他杂费",
        "metric_sales": "💰 总销售额",
        "metric_qty": "📦 总销量",
        "metric_profit": "最终净利润",
        "metric_other": "💸 广告&杂费",
        "chart_trend_title": "📈 每日销售趋势",
        "chart_pie_title": "🍕 SKU 销售占比",
        "table_title": "🏆 热销榜单",
        "ai_advice": "🤖 经营建议",
        "advice_danger": "⚠️ 风险预警：利润率极低，请立即检查广告支出或成本结构！",
        "advice_good": "✅ 经营稳健：利润率不错，建议保持当前节奏。",
        "advice_best": "🚀 爆款预定：利润率优秀！建议加大库存和广告投入，冲刺销量。",
        "unit": "件",
        "sign": "¥",
        "report_header": "本期经营报告",
        "error_cost": "❌ 你的表格缺少 'Unit_Cost' (成本) 列！",
        "filter_header":"🔍 筛选条件",
        "select_date":"请选择日期",
        "vampire_title": "🧛‍♂️ 广告吸血鬼诊断",
        "vampire_help": "以下 SKU 广告投入产出比(ROAS)极低,正在吃掉你的利润！",
        "roas_label": "广告支出回报率 (ROAS)",
        "recommend_action": "优化建议：建议削减广告预算或重新检查 Listing。",
        "metric_cvr": "转化率 (CVR)"
    },
    "en": {
        "title": "📦 Amazon Best-Seller Analyzer v0.7",
        "upload_label": "Upload Amazon Sales Report (CSV/Excel)",
        "sidebar_header": "📊 Dashboard Control",
        "lang_select": "Language Selection",
        "ad_setting": "Ads & Costs Setup",
        "ad_spend": "Monthly Ad Spend",
        "other_costs": "Other Costs",
        "metric_sales": "💰 Total Revenue",
        "metric_qty": "📦 Sales Volume",
        "metric_profit": "Net Profit",
        "metric_other": "💸 Ads & Expenses",
        "chart_trend_title": "📈 Daily Sales Trend",
        "chart_pie_title": "🍕 SKU Sales Distribution",
        "table_title": "🏆 Top Products Ranking",
        "ai_advice": "🤖 AI Insights",
        "advice_danger": "⚠️ Warning: Low profit margin. Review your ad spend immediately!",
        "advice_good": "✅ Healthy: Stable margin. Keep up the good work.",
        "advice_best": "🚀 Best Seller: Excellent margin! Consider increasing inventory and ad budget.",
        "unit": "units",
        "sign": "$",
        "report_header": "Business Performance Report",
        "error_cost": "❌ Missing 'Unit_Cost' column in your file!",
        "filter_header": "🔍 Filters",
        "select_date":"Select Date",
        "vampire_title": "🧛‍♂️ Ad Vampire Detection",
        "vampire_help": "The following SKUs have extremely low ROAS and are eating your profits!",
        "roas_label": "ROAS (Return on Ad Spend)",
        "recommend_action": "Action: Reduce ad budget or audit Product Listing immediately.",
        "metric_cvr": "Conv. Rate (CVR)",

    }
}

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
def plot_charts(df,text):
    # 1. 折线图
    daily_trend = df.groupby('Date')['Total_Sales'].sum().reset_index()
    fig_trend = px.line(
        daily_trend, 
        x='Date', 
        y='Total_Sales',
        title=text["chart_trend_title"],
        markers=True, 
    )
    
    # 2. 甜甜圈图 (Pie Chart,text)
    sku_distribution = df.groupby('SKU')['Total_Sales'].sum().reset_index()
    fig_pie = px.pie(
        sku_distribution, 
        values='Total_Sales', 
        names='SKU', 
        title=text["chart_pie_title"],
        hole=0.3, # 这里的数字 0.3 控制中间那个洞的大小
    )
    
    return fig_trend, fig_pie
#利润率自动生成建议
def generate_summary(revenue,profit,margin,text):
    summary=f'{text["report_header"]}\n\n'
    summary+=f'{text["metric_sales"]}: {text["sign"]}{revenue:,.2f}。\n'
    summary+=f'{text["metric_profit"]}: {text["sign"]}{profit:,.2f}({margin*100:.1f}%)。\n\n'
    if margin < 0.1:
        summary += text['advice_danger']
    elif margin >= 0.3:
        summary += text['advice_good']
    else:
        summary += text['advice_best']
    return summary

   
# ==========================================
# 2. 主程序区 (Main App)
# ==========================================
#让用户选择语言
lang_choice=st.sidebar.radio('Language/语言',['中文','English'])
lang='zh' if lang_choice=='中文' else 'en'
text=LANG_DICT[lang]
#设置页面标签
st.set_page_config(page_title="亚马逊数据看板", layout="wide")
st.title(text["title"])
#加载文件
uploaded_files = st.file_uploader(text["upload_label"], type=['csv', 'xlsx'],accept_multiple_files=True)
if uploaded_files:
    try:
        sales_dfs=[]
        traffic_dfs=[]
        for file in uploaded_files:
            temp_df=load_data(file)
            if 'traffic' in file.name.lower():
                traffic_dfs.append(temp_df)
            else:
                sales_dfs.append(temp_df)
        if not sales_dfs:
            st.warning('请至少上传一份销售报表！')
            st.stop()
        df_sales=pd.concat(sales_dfs,ignore_index=True)

        if traffic_dfs:
            df_traffic_all=pd.concat(traffic_dfs,ignore_index=True)
            df_traffic_agg=df_traffic_all.groupby('SKU')['Sessions'].sum().reset_index()
            #缝合
            df=pd.merge(df_sales,df_traffic_agg,on='SKU',how='left')
            df['Sessions']=df['Sessions'].fillna(0)
        else:
            df=df_sales
            df['Sessions']=0
        #检查是否包含成本列
        if 'Unit_Cost' not in df.columns:
            st.error (text["error_cost"])
            st.stop()#停止运行
        #侧边栏日期
        all_dates = ['所有日期'] + list(df['Date'].unique())
        st.sidebar.header(text["filter_header"])
        selected_date = st.sidebar.selectbox(text["select_date"], all_dates)
        #侧边栏利润率滑块
        ad_spend=st.sidebar.number_input('本期广告费(Ads Spend)',value=0.0,step=100.0)
        other_costs = st.sidebar.number_input('其他成本 (运费/人工)', value=0.0, step=100.0)

        if selected_date == '所有日期':
            filtered_df = df
            period_name = "所有历史数据"
        else:
            filtered_df = df[df['Date'] == selected_date]
            period_name = selected_date
        #计算核心数据
        filtered_df['Total_Sales'] = filtered_df['Price'] * filtered_df['Amount']#单个产品总销售额
        filtered_df['Total_Cost'] = filtered_df['Unit_Cost'] * filtered_df['Amount']#总成本
        filtered_df['Gross_Profit'] = filtered_df['Total_Sales'] - filtered_df['Total_Cost']#单个产品毛利
        total_revenue = filtered_df['Total_Sales'].sum()#总计销售额
        total_gross_profit = filtered_df['Gross_Profit'].sum()#总计毛利
        net_profit = total_gross_profit - ad_spend - other_costs#净利润
        filtered_df['CVR']=filtered_df['Amount']/(filtered_df['Sessions']+0.01)
        if total_revenue>0:
            real_margin=net_profit/total_revenue
        else:
            real_margin=0

        revenue, quantity = calculate_kpi(filtered_df)

        #智能分析
        st.info(generate_summary(revenue, net_profit, real_margin,text))
        #核心指标卡
        st.divider()
        c1, c2 ,c3,c4= st.columns(4)
        with c1:
            st.metric(text["metric_sales"], f"{text['sign']}{revenue:,.2f}")
        with c2:
            st.metric(text["metric_qty"], f"{quantity} {text['unit']}")
        with c3:
            st.metric(text["metric_profit"], f"{text['sign']}{net_profit:,.2f}", f"{real_margin*100:.1f}%")
        with c4:
            st.metric(text["ad_spend"], f"{text['sign']}{ad_spend + other_costs:,.2f}")
        #广告吸血鬼
        st.divider()
        st.subheader(text['vampire_title'])
        sku_group=filtered_df.groupby('SKU').agg({
            'Total_Sales':'sum',
            'Gross_Profit':'sum',
            'Amount': 'sum',
            'Sessions': 'sum'
            }).reset_index()
        avg_ad_per_sku=(ad_spend+other_costs)/len(sku_group) if len(sku_group)>0 else 0
        sku_group['ROAS']=sku_group['Total_Sales']/(avg_ad_per_sku+0.01)
        sku_group['CVR'] = sku_group['Amount'] / (sku_group['Sessions'] + 0.01)
        vampires=sku_group[sku_group['ROAS']<2.0].sort_values(by='ROAS')
        if not vampires.empty:
            st.warning(text['vampire_help'])
            vampire_display = vampires[['SKU', 'Total_Sales', 'ROAS','CVR']]
            vampire_display.columns = ['SKU', text['metric_sales'], text['roas_label'], text['metric_cvr']]
            st.dataframe(vampire_display.style.format({text['metric_cvr']: '{:.2%}'}), 
                         use_container_width=True, hide_index=True)
            st.info(text["recommend_action"])
        else:
            st.success("✅ Excellent! No Ad Vampires detected in this period.")
        
        # 调用绘图函数
        fig_1, fig_2 = plot_charts(filtered_df,text)
        
        # 左右布局展示图表
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_1, use_container_width=True)
        with col2:
            st.plotly_chart(fig_2, use_container_width=True)

        # 下面的表格逻辑不变
        result_df = filtered_df.groupby('SKU')[['Total_Sales', 'Gross_Profit','Amount']].sum().reset_index()
        sorted_df = result_df.sort_values(by='Gross_Profit', ascending=False) # 按赚钱多少排
        top_5 = sorted_df.head(5)
        
        st.subheader(f"🏆 {period_name} {text['table_title']}")
        st.dataframe(top_5, hide_index=True, use_container_width=True)

        #下载按钮
        csv=top_5.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下载榜单数据(CSV)",
            data=csv,
            file_name='top_5_products.csv',
            mime='text/csv' 
            )
            
    except Exception as e:
        st.error(f"发生错误：{e}")
else:
    st.info("👆 请上传文件")