import pandas as pd
import matplotlib.pyplot as plt

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """Load sales CSV and prepare datetime and revenue columns."""
    df = pd.read_csv(file_path)
    
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'])
    
    if 'TotalRevenue' not in df.columns and 'Quantity' in df.columns and 'UnitPrice' in df.columns:
        df['TotalRevenue'] = df['Quantity'] * df['UnitPrice']
        
    return df

def analyze_sales(df: pd.DataFrame):
    """Compute core business metrics."""
    # 1. Total Revenue
    total_rev = df['TotalRevenue'].sum()
    
    # 2. Top Products by Revenue
    top_products = df.groupby('Product')['TotalRevenue'].sum().sort_values(ascending=False)
    
    # 3. Monthly Trends
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_trend = df.groupby('Month')['TotalRevenue'].sum()
    
    return total_rev, top_products, monthly_trend

def plot_dashboard(top_products: pd.Series, monthly_trend: pd.Series, output_path: str = "sales_dashboard.png"):
    """Generate side-by-side bar and line charts."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Bar Chart: Revenue by Product
    top_products.plot(kind='bar', ax=axes[0], color='#2b5c8f', edgecolor='black', alpha=0.85)
    axes[0].set_title('Top Products by Revenue', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Product', fontsize=11)
    axes[0].set_ylabel('Revenue ($)', fontsize=11)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    
    # 2. Line Chart: Monthly Trend
    monthly_trend_str = monthly_trend.copy()
    monthly_trend_str.index = monthly_trend_str.index.astype(str)
    axes[1].plot(monthly_trend_str.index, monthly_trend_str.values, marker='o', linewidth=2.5, color='#e05a47')
    axes[1].set_title('Monthly Revenue Trend', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Month', fontsize=11)
    axes[1].set_ylabel('Revenue ($)', fontsize=11)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].yaxis.set_major_formatter('${x:,.0f}')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Dashboard visualization saved to {output_path}")

def print_summary(total_rev, top_products, monthly_trend):
    """Print readable summary to console."""
    print("=" * 50)
    print("SALES DASHBOARD SUMMARY REPORT")
    print("=" * 50)
    print(f"Total Revenue: ${total_rev:,.2f}")
    print(f"Top Performing Product: {top_products.index[0]} (${top_products.iloc[0]:,.2f})")
    print(f"Lowest Performing Product: {top_products.index[-1]} (${top_products.iloc[-1]:,.2f})")
    print(f"Peak Sales Month: {monthly_trend.idxmax()} (${monthly_trend.max():,.2f})")
    print(f"Lowest Sales Month: {monthly_trend.idxmin()} (${monthly_trend.min():,.2f})")
    print("=" * 50)

if __name__ == "__main__":
    df = load_and_prepare_data("sales_data.csv")
    total_rev, top_products, monthly_trend = analyze_sales(df)
    print_summary(total_rev, top_products, monthly_trend)
    plot_dashboard(top_products, monthly_trend)
