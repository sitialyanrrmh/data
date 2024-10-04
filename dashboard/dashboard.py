import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from the CSV file directly
file_path = 'https://raw.githubusercontent.com/sitialyanrrmh/project_analisis_data/5f4e6ceb29ddfb540d650f0df4091c40041649a4/dashboard/main.csv'
day_df = pd.read_csv(file_path)

# Check if required columns are present
required_columns = ['casual', 'registered', 'cnt', 'weekday', 'mnth', 'season', 'temp', 'hum']
if not all(col in day_df.columns for col in required_columns):
    st.error("Missing one or more required columns in the dataset.")
else:
    # Average renters per day
    weekday_total = day_df.groupby('weekday')[['casual', 'registered', 'cnt']].sum().reset_index()
    weekday_average = weekday_total.copy()
    weekday_average[['casual', 'registered', 'cnt']] = weekday_total[['casual', 'registered', 'cnt']] / (52 * 2)  # jumlah bulan dalam 2 tahun * jumlah minggu
    weekday_average.columns = ['weekday', 'avg_casual', 'avg_registered', 'avg_cnt']
    weekday_average[['avg_casual', 'avg_registered', 'avg_cnt']] = weekday_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Mengatur urutan hari dalam seminggu
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_average['weekday'] = pd.Categorical(weekday_average['weekday'], categories=weekday_order, ordered=True)
    weekday_average = weekday_average.sort_values('weekday')

    # Function to plot average renters per day
    def plot_average_renters_per_day():
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(weekday_average['weekday'], weekday_average['avg_cnt'], marker='o', label='Avg Total', color='green')
        ax.set_title('Average Total Renters per Week')
        ax.set_xlabel('Day')
        ax.set_ylabel('Average Total Renters')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Average renters per season
    season_total = day_df.groupby('season')[['casual', 'registered', 'cnt']].sum().reset_index()
    season_average = season_total.copy()
    season_average[['casual', 'registered', 'cnt']] = season_total[['casual', 'registered', 'cnt']] / 2  # jumlah season dalam 2 tahun
    season_average.columns = ['season', 'avg_casual', 'avg_registered', 'avg_cnt']
    season_average[['avg_casual', 'avg_registered', 'avg_cnt']] = season_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Function to plot average renters per season
    def plot_average_renters_per_season():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season', y='avg_cnt', data=season_average, ax=ax)
        ax.set_title('Average Total Renters per Season')
        ax.set_xlabel('Season')
        ax.set_ylabel('Average Total Renters')
        st.pyplot(fig)

    # Average renters per month
    month_total = day_df.groupby('mnth')[['casual', 'registered', 'cnt']].sum().reset_index()
    month_average = month_total.copy()
    month_average[['casual', 'registered', 'cnt']] = month_total[['casual', 'registered', 'cnt']] / 2  # membagi dengan jumlah bulan dalam 2 tahun
    month_average.columns = ['month', 'avg_casual', 'avg_registered', 'avg_cnt']
    month_average[['avg_casual', 'avg_registered', 'avg_cnt']] = month_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Function to plot average renters per month
    def plot_average_renters_per_month():
        fig, ax = plt.subplots(figsize=(12, 6))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        ax.plot(month_average['month'], month_average['avg_cnt'], marker='o', label='Avg Total Renters (cnt)')
        ax.set_title('Average Renters per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Renters')
        ax.set_xticks(month_average['month'])
        ax.set_xticklabels(months, rotation=45)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

    # Heatmap of correlation
    def plot_heatmap():
        correlation_matrix = day_df[['casual', 'registered', 'cnt', 'temp', 'hum']].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        ax.set_title('Correlation Heatmap of Renters and Weather Variables')
        st.pyplot(fig)

    # Main function to layout the dashboard
    st.title('Bicycle Rent Analysis Dashboard')

    col1, col2 = st.columns(2)

    with col1:
        plot_average_renters_per_day()
    
    with col2:
        plot_average_renters_per_season()
    
    with col1:
        plot_average_renters_per_month()
    
    with col2:
        plot_heatmap()
