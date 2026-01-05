import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 全量语言词库 (Translation Dictionary)
# ==========================================
LANG_DICT = {
    "zh": {
        "page_title": "亚马逊数据看板",
        "title": "📦 亚马逊爆款分析器 v0.9 (真实数据版)",
        "guide_title": "📖 使用指南与数据规范 (必读)",
        "guide_usage": "本系统通过**文件名关键字**自动分类。请确保文件包含：`sales` (销售)、`traffic` (流量)、`ad` (广告)、`product` (信息)、`inventory` (库存)。",
        "guide_table": {
            "type": ["销售表", "流量表", "广告表", "产品信息表", "库存表"],
            "cols": ["Date, SKU, Amount, Unit_Cost", "Date, SKU, Sessions", "SKU, Spend/Cost", "SKU, Real_FBA_Fee, Weight", "SKU, Quantity_Available"],
            "func": ["计算利润", "计算转化率", "诊断广告", "运费分级", "补货建议"]
        },
        "guide_table_headers": ["报表类型", "必需列名", "功能描述"],
        "upload_label": "上传报表 (支持多选拖入)",
        "sidebar_header": "📊 控制面板",
        "lang_select": "选择语言",
        "ad_setting": "杂费设置",
        "other_costs": "其他杂费 (总额分摊)",
        "metric_sales": "💰 总销售额",
        "metric_qty": "📦 总销量",
        "metric_profit": "最终净利润",
        "metric_ad": "🔥 真实广告费",
        "chart_trend_title": "📈 每日销售趋势",
        "chart_pie_title": "🍕 SKU 销售占比",
        "table_title": "🏆 真实利润榜单",
        "ai_advice": "🤖 经营建议",
        "unit": "件",
        "sign": "¥",
        "report_header": "本期经营报告",
        "error_cost": "❌ 你的表格缺少 'Unit_Cost' (成本) 列！",
        "filter_header": "🔍 筛选条件",
        "select_date": "请选择日期",
        "vampire_title": "🧛‍♂️ 广告吸血鬼诊断 (基于真实花费)",
        "vampire_help": "⚠️ 发现 {} 个 SKU 广告正在亏钱（真实 ROAS 低于保本线）！",
        "roas_label": "真实 ROAS",
        "recommend_action": "💡 财务小贴士：当 [真实 ROAS] < [保本 ROAS] 时，您的每一笔广告投入都在侵蚀产品利润。",
        "metric_cvr": "转化率 (CVR)",
        "error_no_sales": "❌ 请至少上传一份销售报表！",
        "download_btn": "📥 下载榜单数据 (CSV)",
        "error_general": "❌ 发生错误",
        "upload_info": "👆 请参考上方指南并上传报表以获得数据",
        "filter_all": "📅 所有日期",
        "advice_danger": "⚠️ 风险预警：净利为负！请检查广告投产比。",
        "advice_good": "✅ 经营稳健：有一定利润空间。",
        "advice_best": "🚀 利润丰厚：该产品表现优异！",
        "warn_no_ad": "⚠️ 未检测到广告报表！广告费目前显示为 0。",
        "col_sku": "SKU",
        "col_ad_spend": "广告费支出",
        "col_be_roas": "保本 ROAS",
        "vampire_safe": "✅ 表现优秀！未发现广告吸血鬼。",
        "vampire_none": "💡 暂无广告数据，请上传广告报表。",
        "vampire_no_spend": "ℹ️ 当前筛选时段内无广告花费。",
        "tpl_download_section": "📂 **下载标准模板 (填入数据后上传)：**",
        "tpl_sales": "📊 销售模板",
        "tpl_traffic": "🌐 流量模板",
        "tpl_ad": "🔥 广告模板",
        "tpl_info": "📦 信息模板",
        "tpl_tip": "💡 **小建议**：您可以直接下载模板，填入数据即可识别。",
        "metric_storage": "📦 预估总仓储费",
        "storage_help": "💡 仓储费根据 1-9月($0.87/cuft) 和 10-12月($2.40/cuft) 动态计算。",
        "metric_v": "🚀 日均销量 (14天)",
        "metric_days": "⌛ 可售天数",
        "restock_title": "📊 智能补货建议 (基于14天销量动态)",
        "col_inv": "当前可用库存",
        "col_suggest": "建议补货量",
        "target_days_label": "目标库存覆盖天数",
        "tpl_inv": "📦 库存模板",
        "error_inv_col": "❌ 库存表中缺少关键列:Quantity_Available"
    },
    "en": {
        "page_title": "Amazon Dashboard",
        "title": "📦 Amazon Analyzer v0.9",
        "guide_title": "📖 Usage Guide & Data Standards",
        "guide_usage": "System identifies files by **keywords**: `sales`, `traffic`, `ad`, `product`, `inventory`.",
        "guide_table": {
            "type": ["Sales", "Traffic", "Ads", "Info", "Inventory"],
            "cols": ["Date, SKU, Amount, Unit_Cost", "Date, SKU, Sessions", "SKU, Spend", "SKU, Real_FBA_Fee, Weight", "SKU, Quantity_Available"],
            "func": ["Profit", "CVR", "Ad Audit", "Shipping", "Restock"]
        },
        "guide_table_headers": ["Type", "Required Columns", "Features"],
        "upload_label": "Upload Reports (Drag & Drop)",
        "sidebar_header": "Dashboard",
        "lang_select": "Language",
        "ad_setting": "Overhead Costs",
        "other_costs": "Other Costs",
        "metric_sales": "💰 Revenue",
        "metric_qty": "📦 Volume",
        "metric_profit": "Net Profit",
        "metric_ad": "🔥 Ad Spend",
        "chart_trend_title": "📈 Daily Sales Trend",
        "chart_pie_title": "🍕 SKU Distribution",
        "table_title": "🏆 Profit Ranking",
        "ai_advice": "🤖 AI Insights",
        "unit": "units",
        "sign": "$",
        "report_header": "Performance Report",
        "error_cost": "❌ Missing 'Unit_Cost'!",
        "filter_header": "🔍 Filters",
        "select_date": "Select Date",
        "vampire_title": "🧛‍♂️ Ad Vampire Detection",
        "vampire_help": "⚠️ Found {} SKUs losing money!",
        "roas_label": "Real ROAS",
        "recommend_action": "💡 Finance Tip: If Actual ROAS < BE ROAS, ads are losing money.",
        "metric_cvr": "Conv. Rate (CVR)",
        "error_no_sales": "❌ No Sales Report!",
        "download_btn": "📥 Download CSV",
        "error_general": "❌ Error",
        "upload_info": "👆 Upload reports to start",
        "filter_all": "📅 All Dates",
        "advice_danger": "⚠️ Warning: Negative Profit!",
        "advice_good": "✅ Healthy Margin.",
        "advice_best": "🚀 Excellent Profit!",
        "warn_no_ad": "⚠️ No Ad Report detected!",
        "col_sku": "SKU",
        "col_ad_spend": "Ad Spend",
        "col_be_roas": "BE ROAS",
        "vampire_safe": "✅ Excellent! No Vampires.",
        "vampire_none": "💡 No ad data.",
        "vampire_no_spend": "ℹ️ No ad spend in period.",
        "tpl_download_section": "📂 **Download Templates:**",
        "tpl_sales": "📊 Sales Tpl",
        "tpl_traffic": "🌐 Traffic Tpl",
        "tpl_ad": "🔥 Ad Tpl",
        "tpl_info": "📦 Info Tpl",
        "tpl_tip": "💡 **Tip**: Use templates for best results.",
        "metric_storage": "📦 Est. Total Storage",
        "storage_help": "💡 Storage fee calculated based on Jan-Sep($0.87) and Oct-Dec($2.40).",
        "metric_v": "🚀 Daily Velocity",
        "metric_days": "⌛ Days Left",
        "restock_title": "📊 Smart Restock Plan",
        "col_inv": "Available Stock",
        "col_suggest": "Suggest Qty",
        "target_days_label": "Target Stock Days",
        "tpl_inv": "📦 Inv Tpl",
        "error_inv_col": "❌ Missing column: Quantity_Available in Inventory Report",
    }
}

#设置页面标签 (必须在所有命令之前)
st.set_page_config(page_title="Amazon Analyzer", layout="wide")

#让用户选择语言
lang_choice = st.sidebar.radio('Language/语言', ['中文', 'English'])
lang = 'zh' if lang_choice == '中文' else 'en'
text = LANG_DICT[lang]

st.title(text["title"])

# ==========================================
# 1. 技能区 (Functions)
# ==========================================
# 上传文件
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

# 绘图
def plot_charts(df, text):
    # 1. 折线图
    daily_trend = df.groupby('Date')['Total_Sales'].sum().reset_index()
    fig_trend = px.line(
        daily_trend,
        x='Date',
        y='Total_Sales',
        title=text["chart_trend_title"],
        markers=True,
    )
    # 2. 甜甜圈图
    sku_distribution = df.groupby('SKU')['Total_Sales'].sum().reset_index()
    fig_pie = px.pie(
        sku_distribution,
        values='Total_Sales',
        names='SKU',
        title=text["chart_pie_title"],
        hole=0.3,
    )
    return fig_trend, fig_pie

# 利润率自动生成建议
def generate_summary(revenue, profit, margin, text):
    summary = f'{text["report_header"]}\n\n'
    summary += f'{text["metric_sales"]}: {text["sign"]}{revenue:,.2f}。\n'
    summary += f'{text["metric_profit"]}: {text["sign"]}{profit:,.2f} ({margin*100:.1f}%)。\n\n'
    if margin < 0.1:
        summary += text['advice_danger']
    elif margin < 0.3:
        summary += text['advice_good']
    else:
        summary += text['advice_best']
    return summary

# 清洗数据
def clean_data(df):
    df.columns = [str(c).strip() for c in df.columns]
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
    
    if 'SKU' in df.columns:
        df['SKU'] = df['SKU'].astype(str).str.strip().str.upper()
    
    # 统一清洗数字列
    cols_to_numeric = ['Sessions', 'Amount', 'Total_Sales', 'Unit_Cost', 'Price', 'Spend', 'SPEND', 'Cost', 'Quantity_Available', 'Quantity_Inbound']
    for col in cols_to_numeric:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'[$,¥%]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    df = df.drop_duplicates()
    return df

# 计算运费
def calculate_fba_fee(weight, length=0, width=0, height=0):
    vol_weight = (length * width * height) / 139
    billing_weight = max(weight, vol_weight)
    if billing_weight <= 1:
        return 4.75
    return 4.75 + (billing_weight - 1) * 0.5

# 三级逻辑运算
def get_final_fba(row, fallback_fee):
    if 'Real_FBA_Fee' in row and pd.notnull(row['Real_FBA_Fee']):
        return row['Real_FBA_Fee']
    l = row.get('Length', 0)
    w = row.get('Width', 0)
    h = row.get('Height', 0)
    weight = row.get('Weight', 0)
    if weight > 0 or (l*w*h) > 0:
        return calculate_fba_fee(weight, l, w, h)
    return fallback_fee

# 仓储费
def calculate_monthly_storage_fee(row):
    l = row.get('Length', 0)
    w = row.get('Width', 0)
    h = row.get('Height', 0)
    if (l * w * h) <= 0:
        return 0
    volume_cuft = (l * w * h) / 1728
    rate = 0.87
    if 'Date' in row and pd.notnull(row['Date']):
        month = row['Date'].month
        if month >= 10:
            rate = 2.40
    return volume_cuft * rate

# ==========================================
# 2. 主程序区 (Main App)
# ==========================================

# --- README 引导区 ---
with st.expander(text["guide_title"], expanded=True):
    st.markdown(text["guide_usage"])
    guide_df = pd.DataFrame(text["guide_table"])
    guide_df.columns = text["guide_table_headers"]
    st.table(guide_df)
    
    st.write(text["tpl_download_section"])
    t1, t2, t3, t4, t5 = st.columns(5)
    
    with t1:
        sales_tpl = pd.DataFrame({
            'Date': ['2026-01-01'], 'SKU': ['SKU-A01'], 'Amount': [10], 
            'Unit_Cost': [5.50], 'Total_Sales': [150.00], 'Price': [15.00]
        }).to_csv(index=False).encode('utf-8-sig')
        st.download_button(text["tpl_sales"], data=sales_tpl, file_name="sales_template.csv")

    with t2:
        traffic_tpl = pd.DataFrame({
            'Date': ['2026-01-01'], 'SKU': ['SKU-A01'], 'Sessions': [100]
        }).to_csv(index=False).encode('utf-8-sig')
        st.download_button(text["tpl_traffic"], data=traffic_tpl, file_name="traffic_template.csv")

    with t3:
        ad_tpl = pd.DataFrame({
            'SKU': ['SKU-A01'], 'Spend': [20.50], 'Impressions': [1000]
        }).to_csv(index=False).encode('utf-8-sig')
        st.download_button(text["tpl_ad"], data=ad_tpl, file_name="ad_template.csv")

    with t4:
        info_tpl = pd.DataFrame({
            'SKU': ['SKU-A01'], 'Product_Name': ['Sample'], 'Weight': [1.2], 
            'Length':[3], 'Width':[2], 'Height':[1],
            'Real_FBA_Fee': [4.75], 'Category': ['Home']
        }).to_csv(index=False).encode('utf-8-sig')
        st.download_button(text["tpl_info"], data=info_tpl, file_name="product_info_template.csv")

    with t5: 
        inv_tpl = pd.DataFrame({
            'SKU': ['SKU-A01'], 
            'Quantity_Available': [50], 
            'Quantity_Inbound': [100]  
        }).to_csv(index=False).encode('utf-8-sig')
        st.download_button(text["tpl_inv"], data=inv_tpl, file_name="inventory_template.csv")

    st.info(text["tpl_tip"])

# 加载文件
uploaded_files = st.file_uploader(text["upload_label"], type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    try:
        sales_dfs, traffic_dfs, adv_dfs, product_info_df, inventory_df = [], [], [], None, None

        for file in uploaded_files:
            temp_df = load_data(file)
            f_name = file.name.lower()
            if 'traffic' in f_name:
                traffic_dfs.append(temp_df)
            elif 'product' in f_name:
                product_info_df = temp_df
            elif 'ad' in f_name or 'advertising' in f_name:
                adv_dfs.append(temp_df)
            elif 'inventory' in f_name or 'stock' in f_name or 'fba_inventory' in f_name:
                inventory_df = temp_df
            else:
                sales_dfs.append(temp_df)
        
        if not sales_dfs:
            st.warning(text["error_no_sales"])
            st.stop()

        # 处理销售数据
        df_sales = pd.concat(sales_dfs, ignore_index=True)
        df_sales = clean_data(df_sales)
        # 按天聚合
        df_sales_daily = df_sales.groupby(['SKU', 'Date']).agg({
            'Amount': 'sum',
            'Total_Sales': 'sum',
            'Unit_Cost': 'first',
            'Price': 'mean'
        }).reset_index()

        # 处理产品信息
        if product_info_df is not None:
            product_info_df = clean_data(product_info_df).drop_duplicates('SKU')
            cols_to_use = product_info_df.columns.difference(df_sales_daily.columns.difference(['SKU']))
            df = pd.merge(df_sales_daily, product_info_df[cols_to_use], on='SKU', how='left')
        else:
            df = df_sales_daily.copy()

        # 处理流量数据
        if traffic_dfs:
            df_traffic_all = pd.concat(traffic_dfs, ignore_index=True)
            df_traffic_all = clean_data(df_traffic_all)
            df_traffic_agg = df_traffic_all.groupby(['SKU', 'Date'])['Sessions'].sum().reset_index()
            df = pd.merge(df, df_traffic_agg, on=['SKU', 'Date'], how='left')
            df['Sessions'] = df['Sessions'].fillna(0)
        else:
            df['Sessions'] = 0

        # 检查成本列
        if 'Unit_Cost' not in df.columns:
            st.error(text["error_cost"])
            st.stop()

        # 侧边栏设置
        with st.sidebar.expander(text["ad_setting"]):
            referral_rate = st.slider('Platform Fee(%)', 0, 30, 15) / 100
            avg_fba_fee = st.number_input('Avg FBA Fee', value=3.5, step=0.1)
            other_costs = st.sidebar.number_input(text["other_costs"], value=0.0, step=100.0)

        # 计算运费
        df['FBA_Single'] = df.apply(get_final_fba, axis=1, args=(avg_fba_fee,))
        
        # 计算总销售额 (容错)
        if 'Total_Sales' not in df.columns:
            if 'Price' in df.columns and 'Amount' in df.columns:
                df['Total_Sales'] = df['Price'] * df['Amount']
            else:
                st.error("表格中缺少 'Total_Sales' 或 'Price' 列")
                st.stop()

        # 侧边栏日期筛选
        st.sidebar.header(text["filter_header"])
        df['Date_Only'] = df['Date'].dt.date
        date_list = sorted(df['Date_Only'].unique(), reverse=True)
        all_options = [text["filter_all"]] + date_list
        selected_date = st.sidebar.selectbox(text["select_date"], all_options)

        if selected_date == text["filter_all"]:
            filtered_df = df.copy()
            period_name = text["filter_all"]
        else:
            filtered_df = df[df['Date_Only'] == selected_date].copy()
            period_name = str(selected_date)

        # 计算核心财务数据
        filtered_df['Storage_Single'] = filtered_df.apply(calculate_monthly_storage_fee, axis=1)
        filtered_df['Storage_Total'] = filtered_df['Storage_Single'] * filtered_df['Amount']
        filtered_df['Ref_Fee'] = filtered_df['Total_Sales'] * referral_rate
        filtered_df['FBA_Total'] = filtered_df['FBA_Single'] * filtered_df['Amount']
        filtered_df['Total_Cost'] = filtered_df['Unit_Cost'] * filtered_df['Amount']
        filtered_df['Gross_Profit'] = filtered_df['Total_Sales'] - filtered_df['Ref_Fee'] - filtered_df['FBA_Total'] - filtered_df['Total_Cost'] - filtered_df['Storage_Total']
        
        sku_group = filtered_df.groupby('SKU').agg({
            'Total_Sales': 'sum',
            'Gross_Profit': 'sum',
            'Amount': 'sum',
            'Sessions': 'sum'
        }).reset_index()

        # 处理真实广告费
        if adv_dfs:
            df_adv_all = pd.concat(adv_dfs, ignore_index=True)
            df_adv_all = clean_data(df_adv_all)
            
            spend_col = None
            for c in ['Spend', 'SPEND', 'Cost', 'COST']:
                if c in df_adv_all.columns:
                    spend_col = c
                    break
            
            if 'Advertised SKU' in df_adv_all.columns and 'SKU' not in df_adv_all.columns:
                df_adv_all = df_adv_all.rename(columns={'Advertised SKU': 'SKU'})
            
            # 日期过滤广告费
            if 'Date' in df_adv_all.columns and selected_date != text["filter_all"]:
                df_adv_all = df_adv_all[df_adv_all['Date'].dt.date == selected_date]

            if spend_col:
                sku_adv_agg = df_adv_all.groupby('SKU')[spend_col].sum().reset_index()
                sku_adv_agg.rename(columns={spend_col: 'Real_Ad_Spend'}, inplace=True)
                sku_group = pd.merge(sku_group, sku_adv_agg, on='SKU', how='left')
                sku_group['Real_Ad_Spend'] = sku_group['Real_Ad_Spend'].fillna(0)
            else:
                sku_group['Real_Ad_Spend'] = 0
        else:
            st.warning(text["warn_no_ad"])
            sku_group['Real_Ad_Spend'] = 0

        # 杂费分摊
        total_sales_all = sku_group['Total_Sales'].sum()
        if total_sales_all > 0:
            sku_group['Other_Share'] = (sku_group['Total_Sales'] / total_sales_all) * other_costs
        else:
            sku_group['Other_Share'] = 0
            
        sku_group = sku_group.fillna(0)

        # 最终利润指标
        sku_group['Net_Profit'] = sku_group['Gross_Profit'] - sku_group['Real_Ad_Spend'] - sku_group['Other_Share']
        sku_group['ROAS'] = sku_group.apply(lambda x: x['Total_Sales'] / x['Real_Ad_Spend'] if x['Real_Ad_Spend'] > 0 else 0, axis=1)
        sku_group['CVR'] = sku_group.apply(lambda x: x['Amount'] / x['Sessions'] if x['Sessions'] > 0 else 0, axis=1).clip(upper=1.0)
        sku_group['Gross_Margin'] = (sku_group['Gross_Profit'] / sku_group['Total_Sales']).fillna(0)
        sku_group['BE_ROAS'] = sku_group['Gross_Margin'].apply(lambda x: 1/x if x > 0 else 99.9)

        # 汇总 KPI
        revenue = sku_group['Total_Sales'].sum()
        net_profit = sku_group['Net_Profit'].sum()
        total_real_ad = sku_group['Real_Ad_Spend'].sum()
        total_storage_fee = filtered_df['Storage_Total'].sum()
        real_margin = net_profit / revenue if revenue > 0 else 0

        st.info(generate_summary(revenue, net_profit, real_margin, text))
        
        st.divider()
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric(text["metric_sales"], f"{text['sign']}{revenue:,.2f}")
        with c2: 
            st.metric(text["metric_storage"], f"{text['sign']}{total_storage_fee:,.2f}")
            st.caption(text["storage_help"])
        with c3: st.metric(text["metric_profit"], f"{text['sign']}{net_profit:,.2f}", f"{real_margin*100:.1f}%")
        with c4: st.metric(text["metric_ad"], f"{text['sign']}{total_real_ad + other_costs:,.2f}")

        # 广告吸血鬼
        st.divider()
        st.subheader(text['vampire_title'])
        vampire_mask = (sku_group['Real_Ad_Spend'] > 0) & (sku_group['ROAS'] < sku_group['BE_ROAS'])
        vampires = sku_group[vampire_mask].sort_values(by='ROAS')
        
        if not vampires.empty:
            st.warning(text['vampire_help'].format(len(vampires)))
            vampire_display = vampires[['SKU', 'Total_Sales', 'Real_Ad_Spend', 'ROAS', 'BE_ROAS', 'CVR']].copy()
            vampire_display.columns = [text["col_sku"], text["metric_sales"], text["col_ad_spend"], text["roas_label"], text["col_be_roas"], text["metric_cvr"]]
            st.dataframe(vampire_display.style.format({
                text["metric_cvr"]: '{:.2%}',
                text["col_ad_spend"]: '{:.2f}',
                text["roas_label"]: '{:.2f}',
                text["col_be_roas"]: '{:.2f}'
            }).background_gradient(subset=[text['roas_label']], cmap='Reds_r'), use_container_width=True, hide_index=True)
            st.info(text["recommend_action"])
        else:
            if total_real_ad == 0 and adv_dfs:
                st.info(text["vampire_no_spend"])
            elif total_real_ad > 0:
                st.success(text["vampire_safe"])
            else:
                st.info(text["vampire_none"])

        # 图表
        fig_1, fig_2 = plot_charts(filtered_df, text)
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(fig_1, use_container_width=True)
        with col2: st.plotly_chart(fig_2, use_container_width=True)

        # 榜单
        top_5 = sku_group.sort_values(by='Net_Profit', ascending=False).head(5)
        st.subheader(f"🏆 {period_name} {text['table_title']}")
        st.dataframe(top_5[['SKU', 'Total_Sales', 'Net_Profit', 'Amount', 'CVR']].style.format({
            'CVR': '{:.2%}', 'Total_Sales': '{:,.2f}', 'Net_Profit': '{:,.2f}'
        }), hide_index=True, use_container_width=True)

        # 智能补货
        st.divider()
        st.subheader(text["restock_title"])
        if inventory_df is not None:
            inventory_df = clean_data(inventory_df)
            inv_col_map = {
                'afn-fulfillable-quantity': 'Quantity_Available',
                'afn-inbound-working-quantity': 'Quantity_Inbound',
                'Available': 'Quantity_Available',
                'Fulfillable': 'Quantity_Available'
            }
            inventory_df = inventory_df.rename(columns=inv_col_map)
            
            if 'Quantity_Available' in inventory_df.columns:
                target_days = st.number_input(text["target_days_label"], value=45, step=5)
                
                max_date = df_sales_daily['Date'].max()
                v_df = df_sales_daily[df_sales_daily['Date'] > (max_date - pd.Timedelta(days=14))]
                if not v_df.empty:
                    actual_days = v_df['Date'].nunique()
                    velocity = v_df.groupby('SKU')['Amount'].sum() / (actual_days if actual_days > 0 else 1)
                else:
                    velocity = pd.Series(0, index=df_sales_daily['SKU'].unique())
                
                restock_df = pd.merge(inventory_df, velocity.rename('V'), on='SKU', how='left').fillna(0)
                if 'Quantity_Inbound' not in restock_df.columns:
                    restock_df['Quantity_Inbound'] = 0
                
                restock_df['Total_Stock'] = restock_df['Quantity_Available'] + restock_df['Quantity_Inbound']
                restock_df['Days_Left'] = restock_df.apply(lambda x: x['Total_Stock'] / x['V'] if x['V'] > 0 else 999, axis=1)
                restock_df['Suggest'] = ((restock_df['V'] * target_days) - restock_df['Total_Stock']).clip(lower=0).round(0)
                
                display_cols = ['SKU', 'Quantity_Available', 'Quantity_Inbound', 'V', 'Days_Left', 'Suggest']
                st.dataframe(
                    restock_df[display_cols].sort_values('Days_Left').style.format({
                        'V': '{:.2f}', 'Days_Left': '{:.1f}', 'Suggest': '{:.0f}'
                    }).background_gradient(subset=['Days_Left'], cmap='RdYlGn', low=0, high=0.3),
                    use_container_width=True, hide_index=True
                )
            else:
                st.error(text["error_inv_col"])
        else:
            st.info("💡 " + text["upload_info"])

        # 下载按钮
        csv = top_5.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=text["download_btn"],
            data=csv,
            file_name='top_5_products.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"{text['error_general']}: {e}")
        # 在开发阶段可以打印完整堆栈，面试演示时注释掉
        # import traceback
        # st.text(traceback.format_exc())

else:
    st.info(text["upload_info"])