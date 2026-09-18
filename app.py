import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="شركة الأفق العقارية",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stApp {
    background-color: #f5f7fb;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* Main Title */

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 5px;
}


/* Subtitle */

.sub-title {
    color: #6b7280;
    font-size: 19px;
    text-align: center;
    margin-bottom: 30px;
}


/* Section Titles */

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 15px;
}


/* KPI Cards */

.kpi-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
    text-align: center;
    min-height: 115px;
}

.kpi-title {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 8px;
}

.kpi-value {
    color: #111827;
    font-size: 25px;
    font-weight: 800;
}


/* Insights */

.insight {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border-right: 5px solid #2563eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    margin-top: 20px;
    margin-bottom: 20px;
}


/* Dataframe */

[data-testid="stDataFrame"] {
    direction: rtl;
}


/* Buttons */

.stButton > button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel("Ex_Dashboard.xlsx")

    df["التاريخ"] = pd.to_datetime(df["التاريخ"])

    df["السنة"] = df["التاريخ"].dt.year
    df["الشهر"] = df["التاريخ"].dt.month
    df["اليوم"] = df["التاريخ"].dt.day

    weekday_map = {
        "Monday": "الاثنين",
        "Tuesday": "الثلاثاء",
        "Wednesday": "الأربعاء",
        "Thursday": "الخميس",
        "Friday": "الجمعة",
        "Saturday": "السبت",
        "Sunday": "الأحد"
    }

    df["اسم اليوم"] = (
        df["التاريخ"]
        .dt.day_name()
        .map(weekday_map)
    )

    return df


df = load_data()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):
    return f"{value:,.0f}"


def kpi(title, value):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title):

    st.markdown(
        f"""
        <div class="section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(text):

    st.markdown(
        f"""
        <div class="insight">
            💡 {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏢 شركة الأفق العقارية")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📌 اختر الصفحة",
    [
        "🏠 الرئيسية",
        "🏢 تحليل العقارات",
        "📍 تحليل المناطق",
        "👨‍💼 أداء المندوبين",
        "🏗️ تحليل المشاريع",
        "📅 التحليل الزمني",
        "💰 التحليل المالي",
        "📋 تفاصيل العمليات"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("🎛️ الفلاتر")


# =========================================================
# FILTER FUNCTION
# =========================================================

def multiselect_filter(label, column):

    values = sorted(
        df[column].dropna().unique()
    )

    return st.sidebar.multiselect(
        label,
        values,
        default=values
    )


# =========================================================
# FILTERS
# =========================================================

selected_years = multiselect_filter(
    "📅 السنة",
    "السنة"
)

selected_cities = multiselect_filter(
    "📍 المنطقة",
    "المدينة / المنطقة"
)

selected_projects = multiselect_filter(
    "🏗️ المشروع",
    "المشروع"
)

selected_types = multiselect_filter(
    "🏢 نوع العقار",
    "نوع العقار"
)

selected_agents = multiselect_filter(
    "👨‍💼 المندوب",
    "مندوب المبيعات"
)

selected_status = multiselect_filter(
    "📌 حالة العملية",
    "حالة العملية"
)

selected_payment = multiselect_filter(
    "💳 طريقة الدفع",
    "طريقة الدفع"
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["السنة"].isin(selected_years)
    &
    df["المدينة / المنطقة"].isin(selected_cities)
    &
    df["المشروع"].isin(selected_projects)
    &
    df["نوع العقار"].isin(selected_types)
    &
    df["مندوب المبيعات"].isin(selected_agents)
    &
    df["حالة العملية"].isin(selected_status)
    &
    df["طريقة الدفع"].isin(selected_payment)
].copy()


# =========================================================
# GLOBAL KPIs
# =========================================================

total_sales = filtered_df[
    "السعر الإجمالي (جنيه)"
].sum()

total_operations = len(filtered_df)

avg_transaction = (
    filtered_df[
        "السعر الإجمالي (جنيه)"
    ].mean()
    if total_operations > 0
    else 0
)

total_commission = filtered_df[
    "قيمة العمولة (جنيه)"
].sum()

sold_count = (
    filtered_df["حالة العملية"]
    .eq("تم البيع")
    .sum()
)

sold_rate = (
    sold_count / total_operations * 100
    if total_operations > 0
    else 0
)


# =========================================================
# PAGE 1
# HOME
# =========================================================

if page == "🏠 الرئيسية":

    st.markdown(
        """
        <div class="main-title">
            🏢 شركة الأفق العقارية
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
            لوحة تحليل الأداء العقاري
        </div>
        """,
        unsafe_allow_html=True
    )

    # KPI ROW

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "💰 إجمالي المبيعات",
            f"{money(total_sales)} جنيه"
        )

    with c2:
        kpi(
            "📋 عدد العمليات",
            f"{total_operations:,}"
        )

    with c3:
        kpi(
            "📊 متوسط قيمة الصفقة",
            f"{money(avg_transaction)} جنيه"
        )

    with c4:
        kpi(
            "💵 إجمالي العمولات",
            f"{money(total_commission)} جنيه"
        )

    st.markdown("---")

    # STATUS

    section("📌 حالة العمليات")

    status = (
        filtered_df[
            "حالة العملية"
        ]
        .value_counts()
        .reset_index()
    )

    status.columns = [
        "حالة العملية",
        "عدد العمليات"
    ]

    fig = px.pie(
        status,
        names="حالة العملية",
        values="عدد العمليات",
        hole=0.55,
        title="توزيع حالات العمليات"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # TYPE + CITY

    c1, c2 = st.columns(2)

    with c1:

        section(
            "🏢 المبيعات حسب نوع العقار"
        )

        data = (
            filtered_df
            .groupby("نوع العقار")[
                "السعر الإجمالي (جنيه)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        fig = px.bar(
            data,
            x="نوع العقار",
            y="السعر الإجمالي (جنيه)",
            text_auto=".2s",
            title="إجمالي المبيعات حسب نوع العقار"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📍 المبيعات حسب المنطقة"
        )

        data = (
            filtered_df
            .groupby("المدينة / المنطقة")[
                "السعر الإجمالي (جنيه)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        fig = px.bar(
            data,
            x="المدينة / المنطقة",
            y="السعر الإجمالي (جنيه)",
            text_auto=".2s",
            title="إجمالي المبيعات حسب المنطقة"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    insight(
        f"تم تحليل {total_operations:,} عملية "
        f"بإجمالي مبيعات {money(total_sales)} جنيه، "
        f"ونسبة عمليات البيع الحالية {sold_rate:.1f}%."
    )


# =========================================================
# PAGE 2
# PROPERTY ANALYSIS
# =========================================================

elif page == "🏢 تحليل العقارات":

    st.title("🏢 تحليل العقارات")

    section(
        "💰 إجمالي المبيعات حسب نوع العقار"
    )

    data = (
        filtered_df
        .groupby("نوع العقار")[
            "السعر الإجمالي (جنيه)"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        data,
        x="نوع العقار",
        y="السعر الإجمالي (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        section("📋 عدد العمليات")

        data = (
            filtered_df[
                "نوع العقار"
            ]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "نوع العقار",
            "عدد العمليات"
        ]

        fig = px.bar(
            data,
            x="نوع العقار",
            y="عدد العمليات",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📊 متوسط قيمة الصفقة"
        )

        data = (
            filtered_df
            .groupby("نوع العقار")[
                "السعر الإجمالي (جنيه)"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="نوع العقار",
            y="السعر الإجمالي (جنيه)",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "💵 متوسط سعر المتر حسب نوع العقار"
    )

    data = (
        filtered_df
        .groupby("نوع العقار")[
            "سعر المتر (جنيه)"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        data,
        x="نوع العقار",
        y="سعر المتر (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📐 متوسط المساحة حسب نوع العقار"
    )

    data = (
        filtered_df
        .groupby("نوع العقار")[
            "المساحة (م²)"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        data,
        x="نوع العقار",
        y="المساحة (م²)",
        text_auto=".0f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📌 حالة العمليات حسب نوع العقار"
    )

    data = pd.crosstab(
        filtered_df["نوع العقار"],
        filtered_df["حالة العملية"]
    ).reset_index()

    for col in [
        "تم البيع",
        "محجوز",
        "ملغي"
    ]:

        if col not in data.columns:
            data[col] = 0

    fig = px.bar(
        data,
        x="نوع العقار",
        y=[
            "تم البيع",
            "محجوز",
            "ملغي"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "💳 طريقة الدفع حسب نوع العقار"
    )

    data = pd.crosstab(
        filtered_df["نوع العقار"],
        filtered_df["طريقة الدفع"]
    ).reset_index()

    for col in [
        "تقسيط",
        "نقدي"
    ]:

        if col not in data.columns:
            data[col] = 0

    fig = px.bar(
        data,
        x="نوع العقار",
        y=[
            "تقسيط",
            "نقدي"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    residential = filtered_df[
        filtered_df["نوع العقار"].isin(
            [
                "شقة سكنية",
                "فيلا",
                "دوبلكس",
                "شاليه"
            ]
        )
    ]

    if len(residential) > 0:

        section(
            "🛏️ تحليل عدد الغرف للعقارات السكنية"
        )

        rooms = (
            residential
            .groupby("عدد الغرف")
            .agg(
                عدد_العمليات=(
                    "رقم العملية",
                    "count"
                ),
                إجمالي_المبيعات=(
                    "السعر الإجمالي (جنيه)",
                    "sum"
                ),
                متوسط_قيمة_الصفقة=(
                    "السعر الإجمالي (جنيه)",
                    "mean"
                ),
                متوسط_المساحة=(
                    "المساحة (م²)",
                    "mean"
                ),
                متوسط_سعر_المتر=(
                    "سعر المتر (جنيه)",
                    "mean"
                )
            )
            .reset_index()
        )

        c1, c2 = st.columns(2)

        with c1:

            fig = px.bar(
                rooms,
                x="عدد الغرف",
                y="إجمالي_المبيعات",
                text_auto=".2s",
                title="المبيعات حسب عدد الغرف"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with c2:

            fig = px.bar(
                rooms,
                x="عدد الغرف",
                y="متوسط_سعر_المتر",
                text_auto=".2s",
                title="متوسط سعر المتر حسب عدد الغرف"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# PAGE 3
# CITY ANALYSIS
# =========================================================

elif page == "📍 تحليل المناطق":

    st.title("📍 تحليل المناطق")

    c1, c2 = st.columns(2)

    with c1:

        section("💰 إجمالي المبيعات")

        data = (
            filtered_df
            .groupby("المدينة / المنطقة")[
                "السعر الإجمالي (جنيه)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        fig = px.bar(
            data,
            x="المدينة / المنطقة",
            y="السعر الإجمالي (جنيه)",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section("📋 عدد العمليات")

        data = (
            filtered_df[
                "المدينة / المنطقة"
            ]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "المدينة / المنطقة",
            "عدد العمليات"
        ]

        fig = px.bar(
            data,
            x="المدينة / المنطقة",
            y="عدد العمليات",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "📊 متوسط قيمة الصفقة حسب المنطقة"
    )

    data = (
        filtered_df
        .groupby("المدينة / المنطقة")[
            "السعر الإجمالي (جنيه)"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        data,
        x="المدينة / المنطقة",
        y="السعر الإجمالي (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "💵 متوسط سعر المتر حسب المنطقة"
    )

    data = (
        filtered_df
        .groupby("المدينة / المنطقة")[
            "سعر المتر (جنيه)"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        data,
        x="المدينة / المنطقة",
        y="سعر المتر (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📌 حالة العمليات حسب المنطقة"
    )

    data = pd.crosstab(
        filtered_df["المدينة / المنطقة"],
        filtered_df["حالة العملية"]
    ).reset_index()

    for col in [
        "تم البيع",
        "محجوز",
        "ملغي"
    ]:

        if col not in data.columns:
            data[col] = 0

    fig = px.bar(
        data,
        x="المدينة / المنطقة",
        y=[
            "تم البيع",
            "محجوز",
            "ملغي"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "🏢 أنواع العقارات داخل كل منطقة"
    )

    data = pd.crosstab(
        filtered_df["المدينة / المنطقة"],
        filtered_df["نوع العقار"]
    ).reset_index()

    property_types = [
        "دوبلكس",
        "شاليه",
        "شقة سكنية",
        "فيلا",
        "محل تجاري",
        "مكتب إداري"
    ]

    for col in property_types:

        if col not in data.columns:
            data[col] = 0

    fig = px.bar(
        data,
        x="المدينة / المنطقة",
        y=property_types,
        barmode="stack"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📐 العلاقة بين المساحة والسعر الإجمالي"
    )

    fig = px.scatter(
        filtered_df,
        x="المساحة (م²)",
        y="السعر الإجمالي (جنيه)",
        color="نوع العقار",
        hover_data=[
            "المدينة / المنطقة",
            "المشروع",
            "مندوب المبيعات"
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📐 العلاقة بين المساحة وسعر المتر"
    )

    fig = px.scatter(
        filtered_df,
        x="المساحة (م²)",
        y="سعر المتر (جنيه)",
        color="نوع العقار",
        hover_data=[
            "المدينة / المنطقة",
            "المشروع"
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 4
# AGENTS
# =========================================================

elif page == "👨‍💼 أداء المندوبين":

    st.title("👨‍💼 تحليل أداء المندوبين")

    agent = (
        filtered_df
        .groupby("مندوب المبيعات")
        .agg(
            عدد_العمليات=(
                "رقم العملية",
                "count"
            ),
            إجمالي_المبيعات=(
                "السعر الإجمالي (جنيه)",
                "sum"
            ),
            متوسط_قيمة_الصفقة=(
                "السعر الإجمالي (جنيه)",
                "mean"
            ),
            إجمالي_العمولة=(
                "قيمة العمولة (جنيه)",
                "sum"
            ),
            متوسط_العمولة=(
                "قيمة العمولة (جنيه)",
                "mean"
            )
        )
        .reset_index()
    )

    sold_rate_agent = (
        filtered_df
        .groupby("مندوب المبيعات")[
            "حالة العملية"
        ]
        .apply(
            lambda x:
            (x == "تم البيع").mean() * 100
        )
        .reset_index(
            name="نسبة البيع"
        )
    )

    agent = agent.merge(
        sold_rate_agent,
        on="مندوب المبيعات"
    )

    c1, c2 = st.columns(2)

    with c1:

        section(
            "💰 إجمالي المبيعات حسب المندوب"
        )

        data = agent.sort_values(
            "إجمالي_المبيعات",
            ascending=False
        )

        fig = px.bar(
            data,
            x="مندوب المبيعات",
            y="إجمالي_المبيعات",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📋 عدد العمليات"
        )

        data = agent.sort_values(
            "عدد_العمليات",
            ascending=False
        )

        fig = px.bar(
            data,
            x="مندوب المبيعات",
            y="عدد_العمليات",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "📊 متوسط قيمة الصفقة"
    )

    fig = px.bar(
        agent.sort_values(
            "متوسط_قيمة_الصفقة",
            ascending=False
        ),
        x="مندوب المبيعات",
        y="متوسط_قيمة_الصفقة",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        section(
            "💵 إجمالي العمولات"
        )

        fig = px.bar(
            agent.sort_values(
                "إجمالي_العمولة",
                ascending=False
            ),
            x="مندوب المبيعات",
            y="إجمالي_العمولة",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📈 نسبة البيع"
        )

        fig = px.bar(
            agent.sort_values(
                "نسبة البيع",
                ascending=False
            ),
            x="مندوب المبيعات",
            y="نسبة البيع",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "📋 ملخص أداء المندوبين"
    )

    st.dataframe(
        agent.sort_values(
            "إجمالي_المبيعات",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 5
# PROJECTS
# =========================================================

elif page == "🏗️ تحليل المشاريع":

    st.title("🏗️ تحليل المشاريع")

    project = (
        filtered_df
        .groupby("المشروع")
        .agg(
            عدد_العمليات=(
                "رقم العملية",
                "count"
            ),
            إجمالي_المبيعات=(
                "السعر الإجمالي (جنيه)",
                "sum"
            ),
            متوسط_قيمة_الصفقة=(
                "السعر الإجمالي (جنيه)",
                "mean"
            ),
            إجمالي_العمولة=(
                "قيمة العمولة (جنيه)",
                "sum"
            )
        )
        .reset_index()
    )

    section(
        "💰 إجمالي المبيعات حسب المشروع"
    )

    fig = px.bar(
        project.sort_values(
            "إجمالي_المبيعات",
            ascending=False
        ),
        x="المشروع",
        y="إجمالي_المبيعات",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        section(
            "📋 عدد العمليات"
        )

        fig = px.bar(
            project.sort_values(
                "عدد_العمليات",
                ascending=False
            ),
            x="المشروع",
            y="عدد_العمليات",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📊 متوسط الصفقة"
        )

        fig = px.bar(
            project.sort_values(
                "متوسط_قيمة_الصفقة",
                ascending=False
            ),
            x="المشروع",
            y="متوسط_قيمة_الصفقة",
            text_auto=".2s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "🥧 حصة المشاريع من إجمالي المبيعات"
    )

    fig = px.pie(
        project,
        names="المشروع",
        values="إجمالي_المبيعات",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📌 حالة العمليات حسب المشروع"
    )

    status = pd.crosstab(
        filtered_df["المشروع"],
        filtered_df["حالة العملية"]
    ).reset_index()

    for col in [
        "تم البيع",
        "محجوز",
        "ملغي"
    ]:

        if col not in status.columns:
            status[col] = 0

    fig = px.bar(
        status,
        x="المشروع",
        y=[
            "تم البيع",
            "محجوز",
            "ملغي"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "💳 طرق الدفع حسب المشروع"
    )

    payment = pd.crosstab(
        filtered_df["المشروع"],
        filtered_df["طريقة الدفع"]
    ).reset_index()

    for col in [
        "تقسيط",
        "نقدي"
    ]:

        if col not in payment.columns:
            payment[col] = 0

    fig = px.bar(
        payment,
        x="المشروع",
        y=[
            "تقسيط",
            "نقدي"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "🏢 أنواع العقارات داخل المشاريع"
    )

    project_type = pd.crosstab(
        filtered_df["المشروع"],
        filtered_df["نوع العقار"]
    ).reset_index()

    property_types = [
        "دوبلكس",
        "شاليه",
        "شقة سكنية",
        "فيلا",
        "محل تجاري",
        "مكتب إداري"
    ]

    for col in property_types:

        if col not in project_type.columns:
            project_type[col] = 0

    fig = px.bar(
        project_type,
        x="المشروع",
        y=property_types,
        barmode="stack"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 6
# TIME ANALYSIS
# =========================================================

elif page == "📅 التحليل الزمني":

    st.title("📅 التحليل الزمني")

    section(
        "📆 المبيعات حسب السنة"
    )

    yearly = (
        filtered_df
        .groupby("السنة")[
            "السعر الإجمالي (جنيه)"
        ]
        .sum()
        .reset_index()
    )

    fig = px.line(
        yearly,
        x="السنة",
        y="السعر الإجمالي (جنيه)",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    monthly = (
        filtered_df
        .groupby("الشهر")
        .agg(
            إجمالي_المبيعات=(
                "السعر الإجمالي (جنيه)",
                "sum"
            ),
            عدد_العمليات=(
                "رقم العملية",
                "count"
            ),
            متوسط_الصفقة=(
                "السعر الإجمالي (جنيه)",
                "mean"
            )
        )
        .reset_index()
    )

    c1, c2 = st.columns(2)

    with c1:

        section(
            "💰 المبيعات حسب الشهر"
        )

        fig = px.line(
            monthly,
            x="الشهر",
            y="إجمالي_المبيعات",
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        section(
            "📋 عدد العمليات حسب الشهر"
        )

        fig = px.bar(
            monthly,
            x="الشهر",
            y="عدد_العمليات",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    section(
        "📊 متوسط قيمة الصفقة حسب الشهر"
    )

    fig = px.line(
        monthly,
        x="الشهر",
        y="متوسط_الصفقة",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📌 حالة العمليات شهريًا"
    )

    monthly_status = pd.crosstab(
        filtered_df["الشهر"],
        filtered_df["حالة العملية"]
    ).reset_index()

    for col in [
        "تم البيع",
        "محجوز",
        "ملغي"
    ]:

        if col not in monthly_status.columns:
            monthly_status[col] = 0

    fig = px.bar(
        monthly_status,
        x="الشهر",
        y=[
            "تم البيع",
            "محجوز",
            "ملغي"
        ],
        barmode="stack"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📅 المبيعات حسب يوم الأسبوع"
    )

    weekday = (
        filtered_df
        .groupby("اسم اليوم")
        .agg(
            عدد_العمليات=(
                "رقم العملية",
                "count"
            ),
            إجمالي_المبيعات=(
                "السعر الإجمالي (جنيه)",
                "sum"
            ),
            متوسط_الصفقة=(
                "السعر الإجمالي (جنيه)",
                "mean"
            )
        )
        .reset_index()
    )

    fig = px.bar(
        weekday,
        x="اسم اليوم",
        y="إجمالي_المبيعات",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📋 عدد العمليات حسب يوم الأسبوع"
    )

    fig = px.bar(
        weekday,
        x="اسم اليوم",
        y="عدد_العمليات",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 7
# FINANCIAL ANALYSIS
# =========================================================

elif page == "💰 التحليل المالي":

    st.title("💰 التحليل المالي")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        kpi(
            "💰 المبيعات",
            money(total_sales)
        )

    with c2:

        kpi(
            "💵 العمولات",
            money(total_commission)
        )

    with c3:

        avg_commission = (
            filtered_df[
                "قيمة العمولة (جنيه)"
            ].mean()
            if len(filtered_df)
            else 0
        )

        kpi(
            "📊 متوسط العمولة",
            money(avg_commission)
        )

    with c4:

        avg_rate = (
            filtered_df[
                "نسبة العمولة %"
            ].mean()
            if len(filtered_df)
            else 0
        )

        kpi(
            "📈 متوسط نسبة العمولة",
            f"{avg_rate:.2f}%"
        )

    section(
        "💳 مقارنة طرق الدفع"
    )

    payment = (
        filtered_df
        .groupby("طريقة الدفع")
        .agg(
            عدد_العمليات=(
                "رقم العملية",
                "count"
            ),
            إجمالي_المبيعات=(
                "السعر الإجمالي (جنيه)",
                "sum"
            ),
            متوسط_الصفقة=(
                "السعر الإجمالي (جنيه)",
                "mean"
            )
        )
        .reset_index()
    )

    fig = px.bar(
        payment,
        x="طريقة الدفع",
        y="إجمالي_المبيعات",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "📊 متوسط قيمة الصفقة حسب طريقة الدفع"
    )

    fig = px.bar(
        payment,
        x="طريقة الدفع",
        y="متوسط_الصفقة",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "💵 إجمالي العمولة حسب نوع العقار"
    )

    commission_type = (
        filtered_df
        .groupby("نوع العقار")[
            "قيمة العمولة (جنيه)"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        commission_type,
        x="نوع العقار",
        y="قيمة العمولة (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "🏗️ إجمالي العمولة حسب المشروع"
    )

    commission_project = (
        filtered_df
        .groupby("المشروع")[
            "قيمة العمولة (جنيه)"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        commission_project,
        x="المشروع",
        y="قيمة العمولة (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "👨‍💼 إجمالي العمولة حسب المندوب"
    )

    commission_agent = (
        filtered_df
        .groupby("مندوب المبيعات")[
            "قيمة العمولة (جنيه)"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        commission_agent,
        x="مندوب المبيعات",
        y="قيمة العمولة (جنيه)",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 8
# TRANSACTIONS DETAILS
# =========================================================

elif page == "📋 تفاصيل العمليات":

    st.title("📋 تفاصيل العمليات")

    st.write(
        f"عدد العمليات بعد تطبيق الفلاتر: "
        f"**{len(filtered_df):,}**"
    )

    columns = [
        "رقم العملية",
        "التاريخ",
        "المدينة / المنطقة",
        "المشروع",
        "نوع العقار",
        "عدد الغرف",
        "المساحة (م²)",
        "سعر المتر (جنيه)",
        "السعر الإجمالي (جنيه)",
        "مندوب المبيعات",
        "حالة العملية",
        "طريقة الدفع",
        "نسبة العمولة %",
        "قيمة العمولة (جنيه)"
    ]

    st.dataframe(
        filtered_df[columns],
        use_container_width=True,
        hide_index=True
    )

    section(
        "🏆 أكبر 10 عمليات"
    )

    top10 = (
        filtered_df[
            [
                "رقم العملية",
                "التاريخ",
                "المدينة / المنطقة",
                "المشروع",
                "نوع العقار",
                "مندوب المبيعات",
                "السعر الإجمالي (جنيه)",
                "حالة العملية"
            ]
        ]
        .sort_values(
            "السعر الإجمالي (جنيه)",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )