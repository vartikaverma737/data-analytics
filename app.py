import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pytz
import numpy as np
import random
from datetime import datetime, timedelta
import time
import re

# Set page config
st.set_page_config(
    page_title="App Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .time-display {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #333;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 1000;
    }
    .chart-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid #ddd;
    }
    .status-indicator {
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        background-color: #e7f3ff;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation function
@st.cache_data
def generate_sample_data():
    """Generate realistic sample app data matching Kaggle dataset structure"""
    categories = [
        'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE',
        'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION', 'ENTERTAINMENT',
        'EVENTS', 'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME',
        'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'GAME', 'FAMILY', 'MEDICAL', 'SOCIAL',
        'SHOPPING', 'PHOTOGRAPHY', 'SPORTS', 'TRAVEL_AND_LOCAL', 'TOOLS',
        'PERSONALIZATION', 'PRODUCTIVITY', 'PARENTING', 'WEATHER', 'VIDEO_PLAYERS',
        'NEWS_AND_MAGAZINES', 'MAPS_AND_NAVIGATION'
    ]
    
    content_ratings = ['Everyone', 'Teen', 'Mature 17+', 'Everyone 10+', 'Adults only 18+', 'Unrated']
    android_versions = ['4.0.3 and up', '4.1 and up', '4.4 and up', '5.0 and up', '6.0 and up', '7.0 and up', '8.0 and up', '9.0 and up']
    types = ['Free', 'Paid']
    
    data = []
    for i in range(1000):
        category = random.choice(categories)
        installs_options = ['1+', '5+', '10+', '50+', '100+', '500+', '1,000+', '5,000+', '10,000+', 
                           '50,000+', '100,000+', '500,000+', '1,000,000+', '5,000,000+', '10,000,000+', '50,000,000+']
        
        # Generate realistic last updated dates
        last_updated = datetime(2018, random.randint(1, 12), random.randint(1, 28))
        
        # Generate price - most apps are free
        app_type = random.choice(types)
        if app_type == 'Free':
            price = '0'
        else:
            price = f'${random.randint(1, 50)}'
        
        data.append({
            'App': f'App {i + 1}',
            'Category': category,
            'Rating': round(1.0 + random.random() * 4, 1),  # 1.0 to 5.0
            'Reviews': random.randint(0, 100000),
            'Size': f'{random.randint(1, 100)}M',
            'Installs': random.choice(installs_options),
            'Type': app_type,
            'Price': price,
            'Content Rating': random.choice(content_ratings),
            'Genres': category.lower().replace('_', ' '),
            'Last Updated': last_updated.strftime('%B %d, %Y'),
            'Current Ver': f'{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}',
            'Android Ver': random.choice(android_versions)
        })
    
    return pd.DataFrame(data)

# Time controller utilities
def get_current_ist_time():
    """Get current IST time"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def is_time_in_range(start_hour, end_hour):
    """Check if current IST time is within specified range"""
    current_time = get_current_ist_time()
    current_hour = current_time.hour
    return start_hour <= current_hour < end_hour

# Translation utilities
def translate_categories(category):
    """Translate category names to different languages"""
    translations = {
        'BEAUTY': 'सौंदर्य',  # Hindi
        'BUSINESS': 'வணிகம்',  # Tamil
        'DATING': 'Dating',  # German (same)
        'TRAVEL_AND_LOCAL': 'Voyage et Local',  # French
        'PRODUCTIVITY': 'Productividad',  # Spanish
        'PHOTOGRAPHY': '写真',  # Japanese
        'GAME': 'Games'  # Simplified
    }
    return translations.get(category, category)

# Helper functions for data processing
def parse_installs(installs_str):
    """Convert installs string to numeric value"""
    if pd.isna(installs_str):
        return 0
    installs_str = str(installs_str)
    # Remove + and , from strings like "1,000,000+"
    numeric_str = re.sub(r'[+,]', '', installs_str)
    try:
        return int(numeric_str)
    except:
        return 0

def parse_size(size_str):
    """Convert size string to MB"""
    if pd.isna(size_str):
        return 0
    size_str = str(size_str)
    if 'k' in size_str.lower():
        return float(re.findall(r'[\d.]+', size_str)[0]) / 1024  # Convert KB to MB
    elif 'm' in size_str.lower():
        return float(re.findall(r'[\d.]+', size_str)[0])
    else:
        # If it's just a number, assume MB
        try:
            return float(size_str)
        except:
            return 0

def parse_price(price_str):
    """Convert price string to numeric value"""
    if pd.isna(price_str) or price_str == '0':
        return 0
    price_str = str(price_str)
    # Remove $ and extract numeric value
    numeric_str = re.sub(r'[$,]', '', price_str)
    try:
        return float(numeric_str)
    except:
        return 0

# Data filtering functions
def filter_chart1_data(data):
    """Filter data for Chart 1: rating >= 4.0, size >= 10MB, updated in 2018"""
    try:
        return data[
            (data['rating'] >= 4.0) &
            (data['size_mb'] >= 10) &
            (data['last_updated'].dt.year == 2018)
        ]
    except:
        return data.head(0)  # Return empty dataframe if filtering fails

def filter_chart2_data(data):
    """Filter data for Chart 2: Categories not starting with A,C,G,S and installs > 1M"""
    try:
        return data[
            (~data['Category'].str[0].str.upper().isin(['A', 'C', 'G', 'S'])) &
            (data['installs_numeric'] > 1000000)
        ]
    except:
        return data.head(0)

def filter_chart3_data(data):
    """Filter data for Chart 3: Complex filtering for dual-axis chart"""
    try:
        return data[
            (data['installs_numeric'] >= 10000) &
            (data['price_numeric'] >= 0) &  # Include free apps too
            (data['size_mb'] > 15) &
            (data['Content Rating'] == 'Everyone') &
            (data['App'].str.len() <= 30)
        ]
    except:
        return data.head(0)

def filter_chart4_data(data):
    """Filter data for Chart 4: Time series with specific conditions"""
    try:
        return data[
            (~data['App'].str[0].str.upper().isin(['X', 'Y', 'Z'])) &
            (data['Category'].str[0].str.upper().isin(['E', 'C', 'B'])) &
            (data['Reviews'] > 500) &
            (~data['App'].str.lower().str.contains('s'))
        ]
    except:
        return data.head(0)

def filter_chart5_data(data):
    """Filter data for Chart 5: Bubble chart with specific categories"""
    valid_categories = ['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 
                       'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS']
    try:
        return data[
            (data['rating'] > 3.5) &
            (data['Category'].isin(valid_categories)) &
            (data['Reviews'] > 500) &
            (~data['App'].str.lower().str.contains('s')) &
            (data['installs_numeric'] > 50000)
        ]
    except:
        return data.head(0)

def filter_chart6_data(data):
    """Filter data for Chart 6: Stacked area chart conditions"""
    try:
        return data[
            (data['rating'] >= 4.2) &
            (~data['App'].str.contains(r'\d')) &
            (data['Category'].str[0].str.upper().isin(['T', 'P'])) &
            (data['Reviews'] > 1000) &
            (data['size_mb'] >= 20) &
            (data['size_mb'] <= 80)
        ]
    except:
        return data.head(0)

# Chart creation functions
def create_chart1_grouped_bar(data):
    """Chart 1: Grouped Bar Chart (3PM-5PM IST)"""
    filtered_data = filter_chart1_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 1.")
        return None
    
    # Group by category and calculate stats
    grouped = filtered_data.groupby('Category').agg({
        'rating': 'mean',
        'Reviews': 'sum',
        'installs_numeric': 'sum'
    }).reset_index()
    
    # Apply translations
    grouped['Category'] = grouped['Category'].apply(translate_categories)
    
    # Get top 10 by installs
    top_10 = grouped.nlargest(10, 'installs_numeric')
    
    # Create dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=top_10['Category'], y=top_10['rating'], name="Avg Rating", marker_color='#8884d8'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Bar(x=top_10['Category'], y=top_10['Reviews'], name="Total Reviews", marker_color='#82ca9d'),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Categories")
    fig.update_yaxes(title_text="Average Rating", secondary_y=False)
    fig.update_yaxes(title_text="Total Reviews", secondary_y=True)
    
    fig.update_layout(
        title="Chart 1: Top 10 Categories - Average Rating vs Total Reviews (3PM-5PM IST)",
        height=500
    )
    
    return fig

def create_chart2_category_map(data):
    """Chart 2: Category visualization (6PM-8PM IST)"""
    filtered_data = filter_chart2_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 2.")
        return None
    
    # Group by category
    grouped = filtered_data.groupby('Category').agg({
        'installs_numeric': 'sum',
        'rating': 'mean'
    }).reset_index()
    
    # Apply translations
    grouped['Category'] = grouped['Category'].apply(translate_categories)
    
    # Get top 5
    top_5 = grouped.nlargest(5, 'installs_numeric')
    
    # Create bar chart with color coding
    colors = ['#ff6b6b' if x > 1000000 else '#4ecdc4' for x in top_5['installs_numeric']]
    
    fig = go.Figure(data=[
        go.Bar(x=top_5['Category'], y=top_5['installs_numeric'], marker_color=colors, name="Total Installs")
    ])
    
    fig.update_layout(
        title="Chart 2: Top 5 Categories by Installs (Filtered) (6PM-8PM IST)",
        xaxis_title="Categories",
        yaxis_title="Total Installs",
        height=500
    )
    
    return fig

def create_chart3_dual_axis(data):
    """Chart 3: Dual-axis chart (1PM-2PM IST)"""
    filtered_data = filter_chart3_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 3.")
        return None
    
    # Separate free and paid apps
    free_apps = filtered_data[filtered_data['Type'] == 'Free']
    paid_apps = filtered_data[filtered_data['Type'] == 'Paid']
    
    # Group by category
    free_grouped = free_apps.groupby('Category').agg({'installs_numeric': 'mean', 'Reviews': 'mean'}).reset_index()
    paid_grouped = paid_apps.groupby('Category').agg({'installs_numeric': 'mean', 'Reviews': 'mean'}).reset_index()
    
    # Apply translations
    free_grouped['Category'] = free_grouped['Category'].apply(translate_categories)
    paid_grouped['Category'] = paid_grouped['Category'].apply(translate_categories)
    
    # Create dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    if not free_grouped.empty:
        top_free = free_grouped.head(3)
        fig.add_trace(
            go.Bar(x=top_free['Category'], y=top_free['installs_numeric'], name="Free Apps Installs", marker_color='#8884d8'),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Bar(x=top_free['Category'], y=top_free['Reviews'], name="Free Apps Reviews", marker_color='#ffc658'),
            secondary_y=True,
        )
    
    if not paid_grouped.empty:
        top_paid = paid_grouped.head(3)
        fig.add_trace(
            go.Bar(x=top_paid['Category'], y=top_paid['installs_numeric'], name="Paid Apps Installs", marker_color='#82ca9d'),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Bar(x=top_paid['Category'], y=top_paid['Reviews'], name="Paid Apps Reviews", marker_color='#ff7c7c'),
            secondary_y=True,
        )
    
    fig.update_xaxes(title_text="Categories")
    fig.update_yaxes(title_text="Average Installs", secondary_y=False)
    fig.update_yaxes(title_text="Average Reviews", secondary_y=True)
    
    fig.update_layout(
        title="Chart 3: Free vs Paid Apps - Top 3 Categories (1PM-2PM IST)",
        height=500
    )
    
    return fig

def create_chart4_time_series(data):
    """Chart 4: Time Series Line Chart (6PM-9PM IST)"""
    filtered_data = filter_chart4_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 4.")
        return None
    
    # Group by month and category
    filtered_data['month'] = filtered_data['last_updated'].dt.to_period('M').astype(str)
    grouped = filtered_data.groupby(['month', 'Category'])['installs_numeric'].sum().reset_index()
    
    # Apply translations
    grouped['Category'] = grouped['Category'].apply(translate_categories)
    
    # Pivot for plotting
    pivot_data = grouped.pivot(index='month', columns='Category', values='installs_numeric').fillna(0)
    
    fig = go.Figure()
    
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1']
    
    for i, category in enumerate(pivot_data.columns):
        fig.add_trace(go.Scatter(
            x=pivot_data.index,
            y=pivot_data[category],
            mode='lines',
            name=category,
            line=dict(color=colors[i % len(colors)])
        ))
    
    fig.update_layout(
        title="Chart 4: Time Series - Installs by Category (6PM-9PM IST)",
        xaxis_title="Month",
        yaxis_title="Installs",
        height=500
    )
    
    return fig

def create_chart5_bubble_chart(data):
    """Chart 5: Bubble Chart (5PM-7PM IST)"""
    filtered_data = filter_chart5_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 5.")
        return None
    
    # Apply translations
    filtered_data = filtered_data.copy()
    filtered_data['Category'] = filtered_data['Category'].apply(translate_categories)
    
    # Limit for performance
    sample_data = filtered_data.head(100)
    
    # Create colors for Game category (Pink)
    colors = ['#ff69b4' if cat == 'Games' else '#8884d8' for cat in sample_data['Category']]
    
    fig = go.Figure(data=go.Scatter(
        x=sample_data['size_mb'],
        y=sample_data['rating'],
        mode='markers',
        marker=dict(
            size=sample_data['installs_numeric']/50000,  # Scale down for visibility
            color=colors,
            opacity=0.6,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        text=sample_data['App'],
        hovertemplate='<b>%{text}</b><br>' +
                      'Size: %{x} MB<br>' +
                      'Rating: %{y}<br>' +
                      'Installs: %{marker.size}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Chart 5: Bubble Chart - Size vs Rating vs Installs (5PM-7PM IST)",
        xaxis_title="Size (MB)",
        yaxis_title="Rating",
        height=500
    )
    
    return fig

def create_chart6_stacked_area(data):
    """Chart 6: Stacked Area Chart (4PM-6PM IST)"""
    filtered_data = filter_chart6_data(data)
    if filtered_data.empty:
        st.warning("⚠️ No data available after applying filters for Chart 6.")
        return None
    
    # Group by month and category
    filtered_data['month'] = filtered_data['last_updated'].dt.to_period('M').astype(str)
    grouped = filtered_data.groupby(['month', 'Category'])['installs_numeric'].sum().reset_index()
    
    # Apply translations
    grouped['Category'] = grouped['Category'].apply(translate_categories)
    
    # Pivot for plotting
    pivot_data = grouped.pivot(index='month', columns='Category', values='installs_numeric').fillna(0)
    
    fig = go.Figure()
    
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1']
    
    for i, category in enumerate(pivot_data.columns):
        fig.add_trace(go.Scatter(
            x=pivot_data.index,
            y=pivot_data[category],
            mode='lines',
            name=category,
            stackgroup='one',
            fill='tonexty' if i > 0 else 'tozeroy',
            line=dict(color=colors[i % len(colors)])
        ))
    
    fig.update_layout(
        title="Chart 6: Stacked Area - Cumulative Installs (4PM-6PM IST)",
        xaxis_title="Month",
        yaxis_title="Cumulative Installs",
        height=500
    )
    
    return fig

# File upload function
def load_csv_data(uploaded_file):
    """Load and parse Google Play Store CSV data"""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Ensure we have the expected columns for Google Play Store dataset
        expected_columns = ['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 
                          'Type', 'Price', 'Content Rating', 'Genres', 'Last Updated', 
                          'Current Ver', 'Android Ver']
        
        st.write(f"Loaded CSV with columns: {list(df.columns)}")
        
        # Process data types to match what the dashboard expects
        if 'Rating' in df.columns:
            df['rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
        
        if 'Reviews' in df.columns:
            df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0)
        
        if 'Size' in df.columns:
            df['size_mb'] = df['Size'].apply(parse_size)
        
        if 'Installs' in df.columns:
            df['installs_numeric'] = df['Installs'].apply(parse_installs)
        
        if 'Price' in df.columns:
            df['price_numeric'] = df['Price'].apply(parse_price)
        
        # Convert Last Updated to datetime
        if 'Last Updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
            # For apps without valid date, assign a random date in 2018
            mask = df['last_updated'].isna()
            df.loc[mask, 'last_updated'] = pd.date_range('2018-01-01', '2018-12-31', periods=mask.sum())
        
        return df
        
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None

# Main dashboard function
def main():
    st.markdown('<h1 class="main-header">📊 Google Play Store App Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Get current IST time
    current_ist = get_current_ist_time()
    current_hour = current_ist.hour
    
    # Display current time
    st.sidebar.markdown(f"""
    <div class="time-display">
        <strong>Current Time (IST):</strong><br>
        {current_ist.strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Current Hour:</strong> {current_hour}:00
    </div>
    """, unsafe_allow_html=True)
    
    # Data source selection
    st.sidebar.header("📂 Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Sample Data", "Upload Google Play Store CSV", "Use Local File Path"]
    )
    
    # Load data based on selection
    if data_source == "Upload Google Play Store CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Choose the Google Play Store CSV file",
            type=['csv'],
            help="Upload the Google Play Store Apps dataset from Kaggle"
        )
        
        if uploaded_file is not None:
            with st.spinner("Loading Google Play Store CSV data..."):
                app_data = load_csv_data(uploaded_file)
            if app_data is not None:
                st.sidebar.success(f"✅ Loaded {len(app_data)} apps from CSV")
            else:
                st.sidebar.error("❌ Failed to load CSV data")
                app_data = generate_sample_data()
        else:
            st.sidebar.info("👆 Please upload the Google Play Store CSV file or use sample data")
            app_data = generate_sample_data()
    
    elif data_source == "Use Local File Path":
        # Add your file path here
        file_path = "googleplaystore.csv"  # Change this to your actual file path
        
        try:
            with st.spinner("Loading data from local file..."):
                app_data = pd.read_csv(file_path)
                # Process the data same as upload function
                if 'Rating' in app_data.columns:
                    app_data['rating'] = pd.to_numeric(app_data['Rating'], errors='coerce').fillna(0)
                if 'Reviews' in app_data.columns:
                    app_data['Reviews'] = pd.to_numeric(app_data['Reviews'], errors='coerce').fillna(0)
                if 'Size' in app_data.columns:
                    app_data['size_mb'] = app_data['Size'].apply(parse_size)
                if 'Installs' in app_data.columns:
                    app_data['installs_numeric'] = app_data['Installs'].apply(parse_installs)
                if 'Price' in app_data.columns:
                    app_data['price_numeric'] = app_data['Price'].apply(parse_price)
                if 'Last Updated' in app_data.columns:
                    app_data['last_updated'] = pd.to_datetime(app_data['Last Updated'], errors='coerce')
                    mask = app_data['last_updated'].isna()
                    app_data.loc[mask, 'last_updated'] = pd.date_range('2018-01-01', '2018-12-31', periods=mask.sum())[:mask.sum()]
                
            st.sidebar.success(f"✅ Loaded {len(app_data)} apps from local file")
        except FileNotFoundError:
            st.sidebar.error("❌ File not found. Please check the file path.")
            app_data = generate_sample_data()
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {str(e)}")
            app_data = generate_sample_data()
    
    else:
        app_data = generate_sample_data()
    
    # Time ranges
    time_ranges = {
        'chart1': {'start': 15, 'end': 17, 'name': 'Chart 1 (Grouped Bar)', 'time': '3PM-5PM'},
        'chart2': {'start': 18, 'end': 20, 'name': 'Chart 2 (Category Map)', 'time': '6PM-8PM'},
        'chart3': {'start': 13, 'end': 14, 'name': 'Chart 3 (Dual-Axis)', 'time': '1PM-2PM'},
        'chart4': {'start': 18, 'end': 21, 'name': 'Chart 4 (Time Series)', 'time': '6PM-9PM'},
        'chart5': {'start': 17, 'end': 19, 'name': 'Chart 5 (Bubble Chart)', 'time': '5PM-7PM'},
        'chart6': {'start': 16, 'end': 18, 'name': 'Chart 6 (Stacked Area)', 'time': '4PM-6PM'}
    }
    
    # Display active charts status
    st.markdown('<div class="status-indicator">', unsafe_allow_html=True)
    st.subheader("📊 Active Charts Status:")
    
    cols = st.columns(3)
    for i, (key, info) in enumerate(time_ranges.items()):
        col = cols[i % 3]
        is_active = is_time_in_range(info['start'], info['end'])
        status = "🟢 Active" if is_active else "🔴 Inactive"
        col.write(f"**{info['name']}**: {status} ({info['time']})")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display charts based on time
    charts_displayed = False
    
    # Chart 1: 3PM-5PM IST
    if is_time_in_range(15, 17):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart1 = create_chart1_grouped_bar(app_data)
        if chart1:
            st.plotly_chart(chart1, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 2: 6PM-8PM IST
    if is_time_in_range(18, 20):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart2 = create_chart2_category_map(app_data)
        if chart2:
            st.plotly_chart(chart2, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 3: 1PM-2PM IST
    if is_time_in_range(13, 14):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart3 = create_chart3_dual_axis(app_data)
        if chart3:
            st.plotly_chart(chart3, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 4: 6PM-9PM IST
    if is_time_in_range(18, 21):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart4 = create_chart4_time_series(app_data)
        if chart4:
            st.plotly_chart(chart4, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 5: 5PM-7PM IST
    if is_time_in_range(17, 19):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart5 = create_chart5_bubble_chart(app_data)
        if chart5:
            st.plotly_chart(chart5, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 6: 4PM-6PM IST
    if is_time_in_range(16, 18):
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart6 = create_chart6_stacked_area(app_data)
        if chart6:
            st.plotly_chart(chart6, use_container_width=True)
            charts_displayed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # No active charts message
    if not charts_displayed:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0;">
            <h2>🕐 No Charts Active</h2>
            <p>Charts are only visible during their designated time windows:</p>
            <ul style="list-style: none; padding: 0;">
                <li>📊 Chart 1: 3:00 PM - 5:00 PM IST</li>
                <li>🗺️ Chart 2: 6:00 PM - 8:00 PM IST</li>
                <li>📈 Chart 3: 1:00 PM - 2:00 PM IST</li>
                <li>📉 Chart 4: 6:00 PM - 9:00 PM IST</li>
                <li>⚪ Chart 5: 5:00 PM - 7:00 PM IST</li>
                <li>📊 Chart 6: 4:00 PM - 6:00 PM IST</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Dashboard information
    st.markdown("""
    <div style="margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <h4>📋 Dashboard Information:</h4>
        <p><strong>Dataset:</strong> Google Play Store Apps (Kaggle)</p>
        <p><strong>Features:</strong> App name, Category, Rating, Reviews, Installs, Size, Last Updated, Type/Price, etc.</p>
        <p><strong>Time-based Charts:</strong> Different visualizations appear based on IST time</p>
        <p><strong>Multi-language Support:</strong> Some categories translated to Hindi, Tamil, French, Spanish, Japanese</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Apps Loaded", len(app_data))
    
    with col2:
        st.metric("Current IST Hour", f"{current_hour}:00")
    
    with col3:
        active_charts = sum([
            is_time_in_range(15, 17),
            is_time_in_range(18, 20),
            is_time_in_range(13, 14),
            is_time_in_range(18, 21),
            is_time_in_range(17, 19),
            is_time_in_range(16, 18)
        ])
        st.metric("Active Charts", active_charts)
    
    # Display sample data preview if using CSV
    if data_source == "Upload Google Play Store CSV" and app_data is not None:
        with st.expander("📋 Data Preview", expanded=False):
            st.write("**First 5 rows of loaded data:**")
            st.dataframe(app_data.head())
            
            st.write("**Dataset Info:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Shape:** {app_data.shape}")
            with col2:
                if 'Category' in app_data.columns:
                    st.write(f"**Categories:** {app_data['Category'].nunique()}")
            with col3:
                if 'Type' in app_data.columns:
                    free_apps = len(app_data[app_data['Type'] == 'Free'])
                    st.write(f"**Free Apps:** {free_apps}")

if __name__ == "__main__":
    main()