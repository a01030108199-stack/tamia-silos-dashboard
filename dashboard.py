import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ضبط إعدادات الصفحة لتكون عريضة وبمظهر فخم
st.set_page_config(
    page_title="لوحة تحكم صوامع طامية",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)



# 1. تخصيص المظهر بأكواد CSS (Premium Dark Mode Style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
        background-color: #0b0f17 !important;
        color: #ffffff;
        font-weight: 700 !important; /* فرض خط عريض على كامل التطبيق */
    }
    
    /* فرض الخط العريض على جميع النصوص والقوائم والبطاقات والجداول */
    .stApp *, [data-testid="stSidebar"] *, .metric-card * {
        font-weight: 700 !important;
    }
    
    /* فرض الخط العريض بشكل خاص على الجداول التفاعلية */
    [data-testid="stTable"] *, [data-testid="stDataFrame"] *, [data-testid="stDataFrame"] div, [data-testid="stDataFrame"] span {
        font-weight: 700 !important;
    }
    
    /* إزالة كل الفراغات والبادينج الأبيض في الأعلى والأسفل */
    [data-testid="block-container"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
        background-color: #0b0f17 !important;
    }
    
    /* إلغاء الفراغ بين البانر وعناصر التحكم والكروت */
    [data-testid="stImage"] {
        margin-bottom: -40px !important;
        position: relative;
        z-index: 1;
    }
    [data-testid="stHorizontalBlock"] {
        position: relative;
        z-index: 2;
    }
    
    /* ستايل الكروت الإحصائية - مدمجة وبارزة بحدود ذهبية وخلفية شفافة */
    .metric-card {
        background-color: rgba(26, 32, 44, 0.85) !important;
        backdrop-filter: blur(10px);
        border: 2px solid #d69e2e !important;
        border-radius: 12px;
        padding: 12px 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.6), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #f6ad55 !important;
    }
    .metric-title {
        color: #cbd5e0;
        font-size: 13px;
        font-weight: 700 !important;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700 !important;
        font-family: 'Cairo', monospace, sans-serif;
        letter-spacing: 0.5px;
    }
    .metric-subtitle {
        color: #a0aec0;
        font-size: 11px;
        margin-top: 4px;
        font-weight: 700 !important;
    }
    
    /* ستايل القائمة الجانبية وتحسين تباين النصوص */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-left: 1px solid #2d3748;
    }
    
    /* إجبار عناوين ونصوص القائمة الجانبية على اللون الأبيض والرمادي الفاتح */
    [data-testid="stSidebar"] label {
        color: #f7fafc !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #d69e2e !important;
        font-weight: 700 !important;
    }
    
    /* الحفاظ على نصوص حقول الإدخال (الخلفية البيضاء) داكنة ومقروءة */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #1a202c !important;
        font-weight: 700 !important;
    }
    
    /* زر استرجاع البيانات الفخم باللون الذهبي البارز للتوضيح */
    [data-testid="stSidebar"] button {
        background-color: #d69e2e !important;
        color: #0d1117 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: background-color 0.2s ease !important;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #f6ad55 !important;
        color: #0d1117 !important;
    }
    
    /* خط فاصل رأسي بين الأعمدة في الشاشات الكبيرة */
    @media (min-width: 768px) {
        [data-testid="column"] + [data-testid="column"] {
            border-right: 1px solid #2d3748 !important;
            padding-right: 30px !important;
        }
    }
    
    /* إخفاء الهيدر الافتراضي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات
data_path = r"F:\شغل طامية\صوامع_طامية_مجمع_التفاصيل.xlsx"

@st.cache_data(ttl=5) # التحديث كل 5 ثوانٍ تلقائياً إذا تغير الملف
def load_data():
    # 1. محاولة القراءة محلياً أولاً (أسرع ولا تحتاج إنترنت)
    if os.path.exists(data_path):
        try:
            df_trans = pd.read_excel(data_path, sheet_name="البيانات التفصيلية")
            df_vendors = pd.read_excel(data_path, sheet_name="الموردين الموحدين")
            df_trans['التاريخ'] = pd.to_datetime(df_trans['التاريخ']).dt.date
            return df_trans, df_vendors, "محلي (قرص F)"
        except Exception:
            pass
            
    # 2. إذا لم يكن الملف محلياً (تشغيل سحابي)، نقوم بالتحميل من رابط OneDrive/SharePoint المشترك
    try:
        import requests
        download_url = "https://commercezuedu-my.sharepoint.com/:x:/g/personal/am_mohamed26_commerce_zu_edu_eg/IQAcTy0xJArZTKwhwPN8F9psAfK5z2SaSj-eu4uZADdvyk8?download=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        
        response = requests.get(download_url, headers=headers, allow_redirects=True)
        
        # التحقق من أن الملف المسترجع هو ملف اكسيل حقيقي وليس صفحة خطأ HTML
        if not response.content.startswith(b"PK\x03\x04"):
            raise ValueError("محتوى الملف المسترجع من OneDrive غير صالح (ربما تم حظر الاتصال كـ Bot).")
            
        # حفظ الملف في ملف مؤقت لقراءته
        temp_file = "temp_cloud_data.xlsx"
        with open(temp_file, "wb") as f:
            f.write(response.content)
            
        df_trans = pd.read_excel(temp_file, sheet_name="البيانات التفصيلية")
        df_vendors = pd.read_excel(temp_file, sheet_name="الموردين الموحدين")
        df_trans['التاريخ'] = pd.to_datetime(df_trans['التاريخ']).dt.date
        
        # تنظيف الملف المؤقت
        try:
            os.remove(temp_file)
        except Exception:
            pass
            
        return df_trans, df_vendors, "سحابي (OneDrive)"
    except Exception as e:
        st.error(f"خطأ أثناء جلب البيانات السحابية: {str(e)}")
        return None, None, None

df_trans, df_vendors, data_source_type = load_data()

if df_trans is None:
    st.error("❌ لم يتم العثور على ملف البيانات المجمع. يرجى التأكد من تشغيل سكريبت الدمج أو ربط الرابط السحابي بشكل صحيح.")
    st.stop()



# 3. القائمة الجانبية (Sidebar) للفلاتر والتصفية
st.sidebar.markdown("<div style='text-align: center; padding: 10px;'><h2 style='color: #d69e2e;'>🌾 صوامع طامية</h2><p style='color: #a0aec0; font-size: 12px;'>نظام الأتمتة والتحليل الذكي</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# زر استرجاع البيانات كاملة وإلغاء كل التصفية
if st.sidebar.button("🔄 استرجاع البيانات كاملة", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")

# فلتر تحديد الموردين
st.sidebar.subheader("🔍 تصفية الموردين")
all_vendors = sorted(df_vendors['الاسم'].unique())
selected_vendors = st.sidebar.multiselect(
    "اختر موردين محددين (اتركه فارغاً لعرض الجميع):",
    options=all_vendors,
    key="sel_vendors"
)

# فلتر التواريخ
st.sidebar.subheader("📅 تصفية الفترة الزمنية")
min_date = df_trans['التاريخ'].min()
max_date = df_trans['التاريخ'].max()
start_date, end_date = st.sidebar.date_input(
    "اختر نطاق التاريخ:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date,
    key="sel_dates"
)

# فلتر درجة النقاء (الدرجات)
st.sidebar.subheader("🌾 درجات القمح")
grades = ['22.5', '23.0', '23.5']
selected_grades = []
col_g1, col_g2, col_g3 = st.sidebar.columns(3)
with col_g1:
    if st.checkbox("22.5", value=True, key="cb_22.5"): selected_grades.append(22.5)
with col_g2:
    if st.checkbox("23.0", value=True, key="cb_23.0"): selected_grades.append(23.0)
with col_g3:
    if st.checkbox("23.5", value=True, key="cb_23.5"): selected_grades.append(23.5)

# فلتر الملف المصدر
st.sidebar.subheader("📂 تصفية ملفات الإدخال")
source_files = sorted(df_trans['الملف_المصدر'].unique())
selected_files = st.sidebar.multiselect(
    "تصفية بحسب ملف إكسل محدد:",
    options=source_files,
    key="sel_files"
)

# تطبيق الفلاتر على البيانات
filtered_df = df_trans.copy()

if selected_vendors:
    filtered_df = filtered_df[filtered_df['الاسم'].isin(selected_vendors)]
    
# فلترة التاريخ
filtered_df = filtered_df[(filtered_df['التاريخ'] >= start_date) & (filtered_df['التاريخ'] <= end_date)]

# فلترة الدرجة
# نقوم بجمع الكميات للدرجات المحددة
grade_cols_to_check = []
if 22.5 in selected_grades: grade_cols_to_check.append('22.5')
if 23.0 in selected_grades: grade_cols_to_check.append('23.0')
if 23.5 in selected_grades: grade_cols_to_check.append('23.5')

# إذا تم إيقاف كل التشيك بوكس، نعيد رسالة خطأ
if not grade_cols_to_check:
    st.warning("⚠️ يرجى تحديد درجة واحدة على الأقل لعرض البيانات.")
    st.stop()

if selected_files:
    filtered_df = filtered_df[filtered_df['الملف_المصدر'].isin(selected_files)]

# 4. العنوان الرئيسي ولوحة الأرقام (Dashboard Header)
st.image("premium_header_banner.png", use_container_width=True)
st.markdown("<h1 style='text-align: center; color: #d69e2e; font-weight: 700; margin-top: 15px; font-size: 30px;'>🌾 لوحة المؤشرات والتحليلات التفاعلية - صوامع طامية</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: 10px; margin-bottom: 25px; border-color: #2d3748;'>", unsafe_allow_html=True)

# صف الكروت الإحصائية (Metrics Section)
total_qty = filtered_df['الكمية'].sum()
total_value = filtered_df['القيمة'].sum()
total_net = filtered_df['الصافي'].sum()
total_trans = filtered_df['رقم المحضر'].nunique()
total_unique_v = filtered_df['الكود'].nunique()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🌾 إجمالي الكمية الموردة</div>
        <div class="metric-value">{total_qty:,.3f}</div>
        <div class="metric-subtitle">طن / أردب</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 إجمالي القيمة الإجمالية</div>
        <div class="metric-value">{total_value:,.2f}</div>
        <div class="metric-subtitle">جنيه مصري</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💵 إجمالي مستحقات الموردين (الصافي)</div>
        <div class="metric-value">{total_net:,.2f}</div>
        <div class="metric-subtitle">جنيه مصري</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📋 إجمالي عدد المحاضر</div>
        <div class="metric-value">{total_trans:,}</div>
        <div class="metric-subtitle">محضر توريد فريد</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">👤 عدد الموردين النشطين</div>
        <div class="metric-value">{total_unique_v:,}</div>
        <div class="metric-subtitle">مورد مسجل بالفترة</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. الرسوم البيانية (Charts Section)
chart_col1, chart_col2 = st.columns([2, 1], gap="large")

with chart_col1:
    # أ) رسم منحنى التوريد اليومي التفاعلي
    st.markdown("<h3 style='color: #d69e2e;'>📈 حركة التوريد اليومية بالطن</h3>", unsafe_allow_html=True)
    daily_data = filtered_df.groupby('التاريخ')['الكمية'].sum().reset_index()
    daily_data['التاريخ'] = pd.to_datetime(daily_data['التاريخ'])
    
    fig_line = px.area(
        daily_data, 
        x='التاريخ', 
        y='الكمية',
        labels={'التاريخ': 'تاريخ التوريد', 'الكمية': 'الكمية الموردة (طن)'},
        template='plotly_dark'
    )
    fig_line.update_traces(line_color='#d69e2e', fillcolor='rgba(214, 158, 46, 0.2)')
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2d3748'),
        margin=dict(l=20, r=20, t=10, b=20),
        font=dict(family="Cairo", size=12, color="#ffffff", weight="bold")
    )
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    # ب) رسم توزيع درجات القمح (Donut Chart)
    st.markdown("<h3 style='color: #d69e2e;'>🍩 نسب درجات القمح</h3>", unsafe_allow_html=True)
    grade_totals = []
    grade_labels = []
    
    for g in grade_cols_to_check:
        grade_totals.append(filtered_df[g].sum())
        grade_labels.append(f"درجة {g}")
        
    fig_pie = go.Figure(data=[go.Pie(
        labels=grade_labels, 
        values=grade_totals, 
        hole=.4,
        marker=dict(colors=['#f6ad55', '#dd6b20', '#d69e2e'])
    )])
    fig_pie.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=0),
        font=dict(family="Cairo", size=12, color="#ffffff", weight="bold")
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# الصف الثاني من الرسومات
chart_col3, chart_col4 = st.columns([1, 1], gap="large")

with chart_col3:
    # ج) أكبر 10 موردين من حيث كمية التوريد (Bar Chart)
    st.markdown("<h3 style='color: #d69e2e;'>🏆 كبار الموردين (أعلى 10)</h3>", unsafe_allow_html=True)
    top_vendors = filtered_df.groupby('الاسم')['الكمية'].sum().nlargest(10).reset_index()
    # عكس الترتيب ليظهر الأكبر في الأعلى عند الرسم الأفقي
    top_vendors = top_vendors.iloc[::-1]
    
    fig_bar = px.bar(
        top_vendors, 
        x='الكمية', 
        y='الاسم',
        orientation='h',
        labels={'الكمية': 'الكمية (طن)', 'الاسم': 'اسم المورد'},
        template='plotly_dark'
    )
    fig_bar.update_traces(marker_color='#dd6b20')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#2d3748'),
        yaxis=dict(showgrid=False),
        margin=dict(l=180, r=20, t=10, b=20),
        font=dict(family="Cairo", size=12, color="#ffffff", weight="bold")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col4:
    # د) إحصائيات التوريد حسب ملف الإدخال المصدر
    st.markdown("<h3 style='color: #d69e2e;'>📁 التوريدات بحسب ملف الإدخال</h3>", unsafe_allow_html=True)
    file_summary = filtered_df.groupby('الملف_المصدر')['الكمية'].sum().reset_index()
    file_summary = file_summary.sort_values(by='الكمية', ascending=False).head(10)
    
    fig_file_bar = px.bar(
        file_summary, 
        y='الكمية', 
        x='الملف_المصدر',
        labels={'الكمية': 'الكمية (طن)', 'الملف_المصدر': 'اسم الملف'},
        template='plotly_dark'
    )
    fig_file_bar.update_traces(marker_color='#4a5568')
    fig_file_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#2d3748'),
        xaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=10, b=20),
        font=dict(family="Cairo", size=12, color="#ffffff", weight="bold")
    )
    st.plotly_chart(fig_file_bar, use_container_width=True)

# 6. جدول البيانات التفاعلي بالكامل (Data Table)
st.markdown("<h3 style='color: #d69e2e;'>📋 تفاصيل التوريدات المفلترة</h3>", unsafe_allow_html=True)

# عرض الجدول بشكل احترافي مع إمكانية البحث والفلترة المباشرة وتنسيق الخط العريض والأرقام
styled_df = filtered_df[['التاريخ', 'رقم المحضر', 'عدد', 'الكود', 'الاسم', '22.5', '23.0', '23.5', 'الكمية', 'القيمة', 'الصافي', 'الملف_المصدر']].style.format(
    formatter={
        'الكمية': '{:,.3f}',
        'القيمة': '{:,.2f}',
        'الصافي': '{:,.2f}',
        '22.5': '{:,.3f}',
        '23.0': '{:,.3f}',
        '23.5': '{:,.3f}'
    },
    na_rep='-'
).set_properties(**{
    'font-weight': 'bold'
})

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

# زر التحميل المباشر للجدول الحالي
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 تصدير الجدول المفلتر الحالي كملف CSV",
    data=csv,
    file_name="بيانات_صوامع_طامية_المفلترة.csv",
    mime="text/csv",
)

# حالة تحديث المراقبة اللحظية ومصدر البيانات في الفوتر
try:
    total_original_files = len([f for f in os.listdir(r"F:\شغل طامية\صوامع طامية") if f.endswith('.xlsx')])
    status_text = f"🟢 نظام المراقبة اللحظية متصل ويعمل حالياً • عدد الملفات الأصلية المستكشفة: {total_original_files} ملف • مصدر البيانات: {data_source_type}"
except Exception:
    status_text = f"☁️ تم تشغيل لوحة التحكم سحابياً بنجاح • مصدر البيانات: {data_source_type}"

st.markdown(f"""
<div style='text-align: center; color: #a0aec0; font-size: 12px; margin-top: 40px; padding: 20px; border-top: 1px solid #2d3748;'>
    {status_text}
</div>
""", unsafe_allow_html=True)
