import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean the data
data = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Remove outliers: exclude top 2.5% and bottom 2.5% of page views
lower_limit = data['value'].quantile(0.025)
upper_limit = data['value'].quantile(0.975)
cleaned_data = data[(data['value'] >= lower_limit) & (data['value'] <= upper_limit)].copy()

def draw_line_plot():
    df = cleaned_data.copy()
    fig, ax = plt.subplots(figsize=(15,5))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    fig.tight_layout()
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df = cleaned_data.copy()
    df['Year'] = df.index.year
    df['Month'] = df.index.month_name()
    
    # Calculate average page views for each month grouped by year
    monthly_avg = df.groupby(['Year', 'Month'])['value'].mean().unstack()
    
    # Sort months in calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg = monthly_avg[month_order]
    
    fig = monthly_avg.plot(kind='bar', figsize=(15,8)).figure
    
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df = cleaned_data.copy()
    df.reset_index(inplace=True)
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.strftime('%b')
    df['Month_num'] = df['date'].dt.month
    
    # Sort by month number to maintain calendar order
    df = df.sort_values('Month_num')
    
    fig, axes = plt.subplots(1, 2, figsize=(15,5))
    
    # Year-wise box plot
    sns.boxplot(x='Year', y='value', data=df, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise box plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='Month', y='value', data=df, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig
