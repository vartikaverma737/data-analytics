# App Analytics Dashboard

A sophisticated Streamlit-based analytics dashboard for visualizing mobile app data with time-based chart visibility and multi-language support.

## Features

### Time-Based Chart Display
- **Chart 1 (Grouped Bar)**: Active 3:00 PM - 5:00 PM IST
- **Chart 2 (Category Map)**: Active 6:00 PM - 8:00 PM IST  
- **Chart 3 (Dual-Axis)**: Active 1:00 PM - 2:00 PM IST
- **Chart 4 (Time Series)**: Active 6:00 PM - 9:00 PM IST
- **Chart 5 (Bubble Chart)**: Active 5:00 PM - 7:00 PM IST
- **Chart 6 (Stacked Area)**: Active 4:00 PM - 6:00 PM IST

### Data Sources
- **Sample Data**: Auto-generated realistic app store data
- **CSV Upload**: Support for custom Google Play Store datasets

### Advanced Filtering
Each chart applies sophisticated filters based on:
- App ratings and review counts
- Installation numbers and revenue
- App categories and content ratings
- Update dates and Android versions
- App size and naming patterns

### Multi-Language Support
Category names are translated to:
- Hindi (सौंदर्य)
- Tamil (வணிகம்)
- French (Voyage et Local)
- Spanish (Productividad)
- Japanese (写真)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd app-analytics-dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
app-analytics-dashboard/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
└── data/                 # Optional: Place CSV files here
    └── sample_data.csv   # Example data file
```

## Chart Descriptions

### Chart 1: Grouped Bar Chart (3PM-5PM IST)
- **Filters**: Rating ≥ 4.0, Size ≥ 10MB, January updates
- **Display**: Top 10 categories by installs
- **Metrics**: Average rating vs Total reviews
- **Languages**: Translated category names

### Chart 2: Category Map (6PM-8PM IST)
- **Filters**: Categories not starting with A,C,G,S and installs > 1M
- **Display**: Top 5 categories by installs
- **Visual**: Color-coded bars based on install count

### Chart 3: Dual-Axis Chart (1PM-2PM IST)
- **Filters**: Complex filtering for high-quality apps
- **Display**: Free vs Paid apps comparison
- **Metrics**: Average installs vs Average revenue

### Chart 4: Time Series (6PM-9PM IST)
- **Filters**: Specific naming and category patterns
- **Display**: Monthly install trends
- **Type**: Stacked area chart by category

### Chart 5: Bubble Chart (5PM-7PM IST)
- **Filters**: High-rated apps with good sentiment
- **Display**: Size vs Rating with install-based bubbles
- **Special**: Pink highlighting for Beauty category

### Chart 6: Stacked Area (4PM-6PM IST)
- **Filters**: Premium apps (rating ≥ 4.2, size 20-80MB)
- **Display**: Cumulative installs over time
- **Categories**: Travel & Productivity focused

## 📋 CSV Upload Format

 CSV file should contain these columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| App | Application name | "WhatsApp Messenger" |
| Category | App category | "Communication" |
| Rating | User rating (0-5) | 4.4 |
| Reviews | Number of reviews | "2,345,678" |
| Size | App size | "25M" |
| Installs | Install count | "1,000,000,000+" |
| Type | Free or Paid | "Free" |
| Price | App price | "$0" |
| Content Rating | Age rating | "Everyone" |
| Last Updated | Update date | "February 11, 2018" |
| Android Ver | Min Android version | "4.0.3 and up" |

## ⚙️ Configuration

### Time Zone Settings
- Dashboard uses IST (India Standard Time)
- Charts activate automatically based on current IST time
- Time display in top-right corner shows current IST

### Data Generation
- Sample data creates 1000 realistic app entries
- 18 different app categories
- Random but realistic metrics (ratings, installs, reviews)
- Date ranges from 2023-2024

## 🎨 Styling Features

- **Custom CSS**: Modern, responsive design
- **Color Schemes**: Consistent color palette across charts
- **Interactive Elements**: Hover effects and tooltips
- **Status Indicators**: Real-time chart availability display
- **Responsive Layout**: Works on different screen sizes

## 🔧 Troubleshooting

### Common Issues

1. **Charts not showing**
   - Check current IST time matches chart schedule
   - Verify data filters aren't too restrictive

2. **CSV upload errors**
   - Ensure column names match expected format
   - Check for special characters in data
   - Verify date formats are readable

3. **Performance issues**
   - Large datasets are automatically sampled
   - Consider using smaller CSV files for testing

### Debug Mode
To run with debug information:
```bash
streamlit run app.py --logger.level=debug
```

## 📈 Performance Optimizations

- **Data Caching**: Uses `@st.cache_data` for faster reloads
- **Efficient Filtering**: Pre-filters data before visualization
- **Sample Limiting**: Bubble chart limited to 100 points
- **Memory Management**: Automatic garbage collection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please:
1. Check this README for common solutions
2. Review the troubleshooting section
3. Create an issue with detailed error information
4. Include your Python version and operating system

## 🔄 Version History

- **v1.0.0**: Initial release with time-based charts
- **v1.1.0**: Added CSV upload functionality
- **v1.2.0**: Implemented multi-language support
- **v1.3.0**: Enhanced filtering and performance optimizations

---

**Made with ❤️ using Streamlit and Plotly**