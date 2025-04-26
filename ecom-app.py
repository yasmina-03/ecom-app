import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load CSV
df = pd.read_csv('final_order_details.csv')

# Add English category translation (in case it's missing in the CSV)
category_translation = {
    'cool_stuff': 'Cool Stuff',
    'pet_shop': 'Pet Shop',
    'moveis_decoracao': 'Furniture & Decor',
    'perfumaria': 'Perfumes',
    'ferramentas_jardim': 'Garden Tools',
    'utilidades_domesticas': 'Home Utilities',
    'telefonia': 'Mobile Phones',
    'beleza_saude': 'Beauty & Health',
    'livros_tecnicos': 'Technical Books',
    'fashion_bolsas_e_acessorios': 'Fashion - Bags & Accessories',
    'cama_mesa_banho': 'Bed, Bath & Table',
    'esporte_lazer': 'Sports & Leisure',
    'consoles_games': 'Consoles & Games',
    'moveis_escritorio': 'Office Furniture',
    'malas_acessorios': 'Luggage & Accessories',
    'alimentos': 'Food',
    'agro_industria_e_comercio': 'Agro Industry & Commerce',
    'eletronicos': 'Electronics',
    'informatica_acessorios': 'Computing Accessories',
    'construcao_ferramentas_construcao': 'Construction Tools',
    'audio': 'Audio',
    'bebes': 'Baby',
    'construcao_ferramentas_iluminacao': 'Lighting Tools',
    'brinquedos': 'Toys',
    'papelaria': 'Stationery',
    'industria_comercio_e_negocios': 'Industry & Business',
    'relogios_presentes': 'Watches & Gifts',
    'automotivo': 'Automotive',
    'eletrodomesticos': 'Home Appliances',
    'moveis_cozinha_area_de_servico_jantar_e_jardim': 'Kitchen & Dining Furniture',
    'climatizacao': 'Air Conditioning',
    'casa_conforto': 'Home Comfort',
    'telefonia_fixa': 'Landline Phones',
    'portateis_casa_forno_e_cafe': 'Portable Kitchen Appliances',
    'fraldas_higiene': 'Diapers & Hygiene',
    'sinalizacao_e_seguranca': 'Signage & Safety',
    'instrumentos_musicais': 'Musical Instruments',
    'eletroportateis': 'Portable Electronics',
    'construcao_ferramentas_jardim': 'Garden Construction Tools',
    'artes': 'Arts',
    'casa_construcao': 'Home Construction',
    'livros_interesse_geral': 'General Books',
    'artigos_de_festas': 'Party Supplies',
    'construcao_ferramentas_seguranca': 'Safety Tools',
    'cine_foto': 'Photography & Cinema',
    'fashion_underwear_e_moda_praia': 'Underwear & Swimwear',
    'fashion_roupa_masculina': 'Men’s Clothing',
    'alimentos_bebidas': 'Food & Beverages',
    'bebidas': 'Beverages',
    'moveis_sala': 'Living Room Furniture',
    'market_place': 'Marketplace',
    'musica': 'Music',
    'fashion_calcados': 'Footwear',
    'flores': 'Flowers',
    'eletrodomesticos_2': 'Home Appliances (Other)',
    'fashion_roupa_feminina': 'Women’s Clothing',
    'pcs': 'Computers',
    'livros_importados': 'Imported Books',
    'artigos_de_natal': 'Christmas Items',
    'moveis_quarto': 'Bedroom Furniture',
    'casa_conforto_2': 'Home Comfort (Other)',
    'portateis_cozinha_e_preparadores_de_alimentos': 'Kitchen Prep Appliances',
    'dvds_blu_ray': 'DVDs & Blu-ray',
    'cds_dvds_musicais': 'Music CDs & DVDs',
    'artes_e_artesanato': 'Arts & Crafts',
    'moveis_colchao_e_estofado': 'Mattresses & Upholstery',
    'tablets_impressao_imagem': 'Tablets, Printers & Imaging',
    'construcao_ferramentas_ferramentas': 'Construction Tools (General)',
    'fashion_esporte': 'Sports Fashion',
    'la_cuisine': 'La Cuisine',
    'pc_gamer': 'Gaming PCs',
    'seguros_e_servicos': 'Insurance & Services',
    'fashion_roupa_infanto_juvenil': 'Children’s Clothing'
}

# Apply the translation
df['product_category_english'] = df['product_category_name'].map(category_translation).fillna('Other')

# Create Seller Performance Tables

# Top 15 Sellers by Total Revenue
df_top_revenue_sellers = (
    df.groupby('seller_id')
    .agg(total_revenue=('total_payment_value', 'sum'),
         total_orders=('order_id', 'count'),
         avg_processing_days=('approval_time_days', 'mean'))
    .sort_values(by='total_revenue', ascending=False)
    .head(15)
)

df_top_revenue_sellers['rank_label'] = ['Seller_' + str(i+1) for i in range(len(df_top_revenue_sellers))]

# Top 15 Fastest Sellers by Avg Processing Time
df_top_fastest_sellers = (
    df.groupby('seller_id')
    .agg(avg_processing_days=('approval_time_days', 'mean'),
         total_orders=('order_id', 'count'),
         total_revenue=('total_payment_value', 'sum'))
    .sort_values(by='avg_processing_days', ascending=True)
    .head(15)
)

df_top_fastest_sellers['rank_label'] = ['Seller_' + str(i+1) for i in range(len(df_top_fastest_sellers))]



# Default filtered dataframe (super important now!)
df_filtered = df.copy()

# ---- PAGE NAVIGATION ----
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Sales", "Customers", "Delivery", "Products", "Sellers"]
)


# ---- PAGE 1: HOME ----
if page == "Home":
    st.title("🛒 Olist E-commerce Dashboard")
    st.write("Welcome to our final project dashboard for the Olist dataset.")
    st.write("Use the sidebar to explore sales, customer insights, delivery performance, and more.")

# ---- PAGE 2: SALES ----
elif page == "Sales":
    st.title("💰 Sales Performance Overview")

    # --- KPIs Section ---
    total_revenue = round(df['total_payment_value'].sum(), 2)
    total_orders = df['order_id'].nunique()
    avg_order_value = round(total_revenue / total_orders, 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🧾 Total Revenue", f"R$ {total_revenue:,.2f}")

    with col2:
        st.metric("📦 Total Orders", f"{total_orders:,}")

    with col3:
        st.metric("💳 Avg Order Value", f"R$ {avg_order_value:,.2f}")

    st.markdown("---")

    # --- Revenue Over Time ---
    st.subheader("📈 Revenue Over Time (Monthly)")
    df['order_purchase_month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M').astype(str)
    monthly_revenue = df.groupby('order_purchase_month')['total_payment_value'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_revenue['order_purchase_month'], monthly_revenue['total_payment_value'], marker='o')
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (BRL)")
    ax.set_title("Monthly Revenue Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("---")

    # --- Revenue by State ---
    st.subheader("📍 Revenue by Customer State")
    revenue_by_state = df.groupby('customer_state')['total_payment_value'].sum().sort_values(ascending=False).reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.bar(revenue_by_state['customer_state'], revenue_by_state['total_payment_value'])
    ax2.set_xlabel("State")
    ax2.set_ylabel("Revenue (BRL)")
    ax2.set_title("Total Revenue by State")
    plt.xticks(rotation=45)
    st.pyplot(fig2)



# ---- PAGE 3: CUSTOMERS ----
elif page == "Customers":
    st.title("👥 Customer Insights")

    # Convert timestamps
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Sidebar Filters
    st.sidebar.subheader("Filter Customers")
    state_filter = st.sidebar.multiselect(
        "Select Customer States",
        options=df['customer_state'].dropna().unique(),
        default=list(df['customer_state'].dropna().unique())
    )

    min_date = df['order_purchase_timestamp'].min()
    max_date = df['order_purchase_timestamp'].max()

    date_range = st.sidebar.date_input(
        "Select Order Date Range",
        value=(min_date.date(), max_date.date())
    )

    # Filtered DataFrame
    df_filtered = df[
        (df['customer_state'].isin(state_filter)) &
        (df['order_purchase_timestamp'].dt.date.between(date_range[0], date_range[1]))
    ]

    # KPIs (Metrics)
    st.metric("🧍‍♀️ Unique Customers", f"{df_filtered['customer_unique_id'].nunique():,}")
    top_state = df_filtered['customer_state'].value_counts().idxmax()
    st.metric("📍 Top State", top_state)
    avg_order_value = df_filtered['total_payment_value'].sum() / df_filtered['customer_unique_id'].nunique()
    st.metric("💸 Avg Order Value / Customer", f"R${avg_order_value:,.2f}")

    # --- New Customers Over Time ---
    st.subheader("📈 New Customer Acquisition Over Time")
    new_customers = df_filtered.groupby(df_filtered['order_purchase_timestamp'].dt.to_period('M'))['customer_unique_id'].nunique()
    fig1, ax1 = plt.subplots()
    new_customers.plot(ax=ax1, color='mediumblue')
    plt.ylabel("New Customers")
    plt.xlabel("Month")
    st.pyplot(fig1)

    # --- Customers by State ---
    st.subheader("📍 Top Customer States")
    state_counts = df_filtered['customer_state'].value_counts().head(10)
    fig2, ax2 = plt.subplots()
    state_counts.plot(kind='bar', ax=ax2, color='teal')
    plt.ylabel("Customers")
    plt.xlabel("State")
    st.pyplot(fig2)

    # --- Avg Order Value by State ---
    st.subheader("💳 Avg Order Value by State")
    aov_by_state = df_filtered.groupby('customer_state')['total_payment_value'].mean().sort_values(ascending=False).head(10)
    fig3, ax3 = plt.subplots()
    aov_by_state.plot(kind='bar', ax=ax3, color='darkorange')
    plt.ylabel("Avg Order Value (R$)")
    plt.xlabel("State")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# ---- PAGE 4: DELIVERY ----
elif page == "Delivery":
    st.title("🚚 Delivery & Logistics Insights")

    # Sidebar Filters
    st.sidebar.subheader("Filter Deliveries")
    state_filter = st.sidebar.multiselect(
        "Select Customer States",
        options=df['customer_state'].dropna().unique(),
        default=list(df['customer_state'].dropna().unique())
    )

    review_score_range = st.sidebar.slider(
        "Select Review Score Range",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )

    df_filtered = df[
        (df['customer_state'].isin(state_filter)) &
        (df['review_score'].between(review_score_range[0], review_score_range[1]))
    ]

    # KPIs
    avg_delivery_time = df_filtered['total_delivery_time_days'].mean()
    late_deliveries = df_filtered[df_filtered['delivery_delay_days'] > 0].shape[0]
    total_deliveries = df_filtered.shape[0]
    late_delivery_pct = (late_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0
    avg_review_score = df_filtered['review_score'].mean()

    st.metric("📦 Avg Delivery Time", f"{avg_delivery_time:.1f} days")
    st.metric("⏰ Late Delivery Rate", f"{late_delivery_pct:.1f}%")
    st.metric("⭐ Avg Review Score", f"{avg_review_score:.2f}")

    # --- Average Delivery Time by State ---
    st.subheader("🚛 Average Delivery Time by State")
    avg_time_by_state = df_filtered.groupby('customer_state')['total_delivery_time_days'].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots()
    avg_time_by_state.plot(kind='bar', ax=ax1, color='darkgreen')
    plt.ylabel("Avg Delivery Time (Days)")
    plt.xlabel("State")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # --- Delivery Delay Distribution ---
    st.subheader("⏱️ Delivery Delay Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(df_filtered['delivery_delay_days'].dropna(), bins=30, kde=True, color='tomato', ax=ax2)
    plt.xlabel("Delivery Delay (Days)")
    st.pyplot(fig2)

    # --- On-Time vs Late Deliveries ---
    st.subheader("✅ On-Time vs Late Deliveries")
    on_time = df_filtered[df_filtered['delivery_delay_days'] <= 0].shape[0]
    late = df_filtered[df_filtered['delivery_delay_days'] > 0].shape[0]
    fig3, ax3 = plt.subplots()
    ax3.pie([on_time, late], labels=['On-Time', 'Late'], autopct='%1.0f%%', startangle=90, colors=['seagreen', 'salmon'])
    ax3.axis('equal')
    st.pyplot(fig3)

    # --- Review Score vs Delivery Delay ---
    st.subheader("⭐ Review Score vs Delivery Delay")
    fig4, ax4 = plt.subplots()
    sns.boxplot(x=df_filtered['review_score'], y=df_filtered['delivery_delay_days'], ax=ax4)
    plt.ylabel("Delivery Delay (Days)")
    plt.xlabel("Review Score")
    st.pyplot(fig4)
#
elif page == "Sellers":
    st.title("🏬 Seller Distribution Insights")
    # --- KPIs SECTION ---
    avg_processing_time = round(df['approval_time_days'].mean(), 2)
    total_sellers = df['seller_id'].nunique()
    top_revenue_seller = df_top_revenue_sellers.index[0]  # Seller with highest revenue
    top_speed_seller = df_top_fastest_sellers.index[0]    # Seller with fastest processing time

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("⏳ Avg Processing Time (Days)", f"{avg_processing_time}")

    with col2:
        st.metric("🏬 Total Sellers", f"{total_sellers}")

    with col3:
        st.metric("💰 Top Revenue Seller", top_revenue_seller)

    with col4:
        st.metric("⚡ Fastest Processing Seller", top_speed_seller)
    


    st.subheader("Top Seller States")
    seller_counts = df.groupby('seller_state')['seller_id'].nunique().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    seller_counts.plot(kind='bar', ax=ax, color='darkcyan')
    ax.set_ylabel("Number of Sellers")
    ax.set_xlabel("State")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Sellers and Delivery Impact")
    st.write("Most sellers are concentrated in SP, PR, and MG. Remote seller locations correlate with longer delivery times and higher customer dissatisfaction.")



    tab1, tab2 = st.tabs(["Top Revenue Sellers", "Top Fastest Sellers"])

    with tab1:
        st.subheader("Top 15 Sellers by Total Revenue")
        st.dataframe(df_top_revenue_sellers)

    with tab2:
        st.subheader("Top 15 Fastest Sellers (Lowest Processing Time)")
        st.dataframe(df_top_fastest_sellers)



# ---- PAGE 5: PRODUCTS ----
elif page == "Products":
    st.title("🛍️ Product & Category Performance")

    # Sidebar Filters
    st.sidebar.subheader("Filter Products")
    category_filter = st.sidebar.multiselect(
        "Select Product Categories",
        options=df['product_category_english'].dropna().unique(),
        default=list(df['product_category_english'].dropna().unique())
    )

    review_score_range = st.sidebar.slider(
        "Select Review Score Range",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )

    # Filtered DataFrame
    df_filtered = df[
        (df['product_category_english'].isin(category_filter)) &
        (df['review_score'].between(review_score_range[0], review_score_range[1]))
    ]

    # KPIs
    num_categories = df_filtered['product_category_english'].nunique()
    top_revenue_category = df_filtered.groupby('product_category_english')['total_payment_value'].sum().idxmax()
    top_review_category = df_filtered.groupby('product_category_english')['review_score'].mean().idxmax()

    st.metric("🛒 Product Categories", num_categories)
    st.metric("💰 Top Revenue Category", top_revenue_category)
    st.metric("⭐ Best Rated Category", top_review_category)

    # --- Top 10 Product Categories by Revenue ---
    st.subheader("💰 Top 10 Product Categories by Revenue")
    top_categories = df_filtered.groupby('product_category_english')['total_payment_value'].sum().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    top_categories.plot(kind='bar', ax=ax1, color='royalblue')
    ax1.set_ylabel("Total Revenue (R$)", fontsize=12)
    ax1.set_xlabel("Category", fontsize=12)
    ax1.set_title("Top 10 Categories Driving Revenue", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig1)

    # --- Product Volume vs Revenue ---
    st.subheader("📦 Product Volume vs Revenue")
    volume_revenue = df_filtered.groupby('product_category_english').agg({
        'order_item_id': 'count',
        'total_payment_value': 'sum'
    }).reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.scatter(volume_revenue['order_item_id'], volume_revenue['total_payment_value'], alpha=0.7)
    for i in range(len(volume_revenue)):
        ax2.annotate(volume_revenue['product_category_english'][i], 
                     (volume_revenue['order_item_id'][i], volume_revenue['total_payment_value'][i]),
                     fontsize=6, alpha=0.7)
    ax2.set_xlabel("Units Sold", fontsize=12)
    ax2.set_ylabel("Total Revenue (R$)", fontsize=12)
    ax2.set_title("Volume of Products Sold vs Revenue", fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig2)

    # --- Categories with Lowest Avg Review Score ---
    st.subheader("⚠️ Categories with Lowest Avg Review Scores")
    low_reviews = df_filtered.groupby('product_category_english')['review_score'].mean().sort_values().head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    low_reviews.plot(kind='bar', ax=ax3, color='firebrick')
    ax3.set_ylabel("Average Review Score", fontsize=12)
    ax3.set_xlabel("Category", fontsize=12)
    ax3.set_title("Lowest Satisfaction Categories", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig3)


