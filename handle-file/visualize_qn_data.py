#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để visualize dữ liệu Quảng Ninh
Tạo các biểu đồ: time series, phân bố theo trạm, correlation, box plot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Cấu hình style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# Đường dẫn
DATA_PATH = Path(__file__).parent.parent / "data" / "data_quang_ninh" / "qn_env_clean_ready.csv"
OUTPUT_DIR = Path(__file__).parent / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)

# Đọc dữ liệu
print("Đang đọc dữ liệu...")
df = pd.read_csv(DATA_PATH)
df['Quarter'] = pd.to_datetime(df['Quarter'])

# Chuyển đổi tất cả các cột số sang numeric, xử lý các giá trị không hợp lệ
numeric_cols_all = ['DO', 'Temperature', 'pH', 'Salinity', 'NH3', 'PO4', 
                    'TSS', 'Coliform', 'Transparency', 'COD', 'CN',
                    'As', 'Cd', 'Pb', 'Cu', 'Hg', 'Zn', 'Total_Cr',
                    'H2S', 'BOD5', 'Alkalinity', 'X', 'Y']
for col in numeric_cols_all:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Các thông số chính để visualize
MAIN_PARAMS = {
    'DO': 'Oxy hòa tan (mg/L)',
    'Temperature': 'Nhiệt độ (°C)',
    'pH': 'pH',
    'Salinity': 'Độ mặn (‰)',
    'NH3': 'Amoni (mg/L)',
    'PO4': 'Phosphat (mg/L)',
    'TSS': 'TSS (mg/L)',
    'Transparency': 'Độ trong (m)',
}

# Các kim loại nặng
HEAVY_METALS = ['As', 'Cd', 'Pb', 'Cu', 'Hg', 'Zn', 'Total_Cr']

print(f"Tổng số bản ghi: {len(df)}")
print(f"Số trạm quan trắc: {df['Station'].nunique()}")
print(f"Thời gian: {df['Quarter'].min()} đến {df['Quarter'].max()}")


def plot_time_series():
    """Vẽ biểu đồ time series cho các thông số chính"""
    print("\n1. Vẽ biểu đồ time series...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    params_to_plot = ['DO', 'Temperature', 'pH', 'Salinity']
    
    for idx, param in enumerate(params_to_plot):
        ax = axes[idx]
        
        # Đảm bảo cột là numeric
        df_param = df[[param, 'Quarter']].copy()
        df_param[param] = pd.to_numeric(df_param[param], errors='coerce')
        
        # Tính trung bình theo quý cho tất cả các trạm
        quarterly_avg = df_param.groupby('Quarter')[param].mean()
        
        # Vẽ đường trung bình
        ax.plot(quarterly_avg.index, quarterly_avg.values, 
                linewidth=2.5, marker='o', markersize=6, 
                label='Trung bình', color='#2E86AB')
        
        # Vẽ min-max band
        quarterly_min = df_param.groupby('Quarter')[param].min()
        quarterly_max = df_param.groupby('Quarter')[param].max()
        ax.fill_between(quarterly_avg.index, quarterly_min.values, 
                        quarterly_max.values, alpha=0.2, color='#2E86AB',
                        label='Min-Max')
        
        ax.set_title(MAIN_PARAMS[param], fontsize=12, fontweight='bold')
        ax.set_xlabel('Thời gian', fontsize=10)
        ax.set_ylabel(MAIN_PARAMS[param], fontsize=10)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle('Xu hướng các thông số môi trường theo thời gian (2021-2024)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '1_time_series_main_params.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '1_time_series_main_params.png'}")
    plt.close()


def plot_station_comparison():
    """So sánh các trạm quan trắc"""
    print("\n2. Vẽ biểu đồ so sánh trạm...")
    
    # Lấy top 6 trạm có nhiều dữ liệu nhất
    station_counts = df['Station'].value_counts()
    top_stations = station_counts.head(6).index.tolist()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    params_to_plot = ['DO', 'Temperature', 'pH', 'Salinity']
    
    for idx, param in enumerate(params_to_plot):
        ax = axes[idx]
        
        # Lọc dữ liệu cho top stations
        df_filtered = df[df['Station'].isin(top_stations)][[param, 'Station']].copy()
        df_filtered[param] = pd.to_numeric(df_filtered[param], errors='coerce')
        
        # Box plot
        box_data = [df_filtered[df_filtered['Station'] == st][param].dropna().values 
                   for st in top_stations]
        
        bp = ax.boxplot(box_data, labels=top_stations, patch_artist=True)
        
        # Tô màu
        colors = plt.cm.Set3(np.linspace(0, 1, len(bp['boxes'])))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title(f'Phân bố {MAIN_PARAMS[param]} theo trạm', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel(MAIN_PARAMS[param], fontsize=10)
        ax.set_xlabel('Trạm quan trắc', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle('So sánh các thông số môi trường giữa các trạm quan trắc', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '2_station_comparison.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '2_station_comparison.png'}")
    plt.close()


def plot_correlation_heatmap():
    """Vẽ heatmap correlation matrix"""
    print("\n3. Vẽ heatmap correlation...")
    
    # Chọn các cột số để tính correlation
    numeric_cols = ['DO', 'Temperature', 'pH', 'Salinity', 'NH3', 'PO4', 
                   'TSS', 'Coliform', 'Transparency', 'COD', 'CN',
                   'As', 'Cd', 'Pb', 'Cu', 'Hg', 'Zn', 'Total_Cr',
                   'H2S', 'BOD5', 'Alkalinity']
    
    # Lọc các cột có trong dataframe
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    # Chuyển đổi tất cả các cột sang numeric, xử lý các giá trị không hợp lệ
    df_numeric = df[numeric_cols].copy()
    for col in numeric_cols:
        df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
    
    # Tính correlation
    corr_matrix = df_numeric.corr()
    
    # Vẽ heatmap
    fig, ax = plt.subplots(figsize=(14, 12))
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                cmap='coolwarm', center=0, square=True, 
                linewidths=0.5, cbar_kws={"shrink": 0.8},
                ax=ax, vmin=-1, vmax=1)
    
    ax.set_title('Ma trận tương quan giữa các thông số môi trường', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '3_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '3_correlation_heatmap.png'}")
    plt.close()


def plot_heavy_metals():
    """Vẽ biểu đồ kim loại nặng"""
    print("\n4. Vẽ biểu đồ kim loại nặng...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    metals_to_plot = ['As', 'Cd', 'Pb', 'Cu']
    
    for idx, metal in enumerate(metals_to_plot):
        if metal not in df.columns:
            continue
            
        ax = axes[idx]
        
        # Đảm bảo cột là numeric
        df_metal = df[[metal, 'Quarter']].copy()
        df_metal[metal] = pd.to_numeric(df_metal[metal], errors='coerce')
        
        # Tính trung bình theo quý
        quarterly_avg = df_metal.groupby('Quarter')[metal].mean()
        
        # Vẽ đường trung bình
        ax.plot(quarterly_avg.index, quarterly_avg.values, 
                linewidth=2.5, marker='o', markersize=6, 
                color='#C73E1D')
        
        # Vẽ min-max band
        quarterly_min = df_metal.groupby('Quarter')[metal].min()
        quarterly_max = df_metal.groupby('Quarter')[metal].max()
        ax.fill_between(quarterly_avg.index, quarterly_min.values, 
                        quarterly_max.values, alpha=0.2, color='#C73E1D')
        
        ax.set_title(f'{metal} (mg/L)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Thời gian', fontsize=10)
        ax.set_ylabel(f'{metal} (mg/L)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle('Xu hướng kim loại nặng theo thời gian (2021-2024)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '4_heavy_metals.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '4_heavy_metals.png'}")
    plt.close()


def plot_station_distribution():
    """Vẽ phân bố số lượng mẫu theo trạm"""
    print("\n5. Vẽ phân bố số lượng mẫu theo trạm...")
    
    station_counts = df['Station'].value_counts().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(station_counts)))
    bars = ax.barh(station_counts.index, station_counts.values, color=colors)
    
    # Thêm giá trị trên mỗi cột
    for i, (idx, val) in enumerate(zip(station_counts.index, station_counts.values)):
        ax.text(val + 0.5, i, f'{val}', va='center', fontsize=9)
    
    ax.set_xlabel('Số lượng mẫu', fontsize=11, fontweight='bold')
    ax.set_ylabel('Trạm quan trắc', fontsize=11, fontweight='bold')
    ax.set_title('Phân bố số lượng mẫu theo trạm quan trắc', 
                fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '5_station_distribution.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '5_station_distribution.png'}")
    plt.close()


def plot_quarterly_trends():
    """Vẽ xu hướng theo quý trong năm"""
    print("\n6. Vẽ xu hướng theo quý...")
    
    # Thêm cột quý
    df['Quarter_num'] = df['Quarter'].dt.quarter
    df['Year'] = df['Quarter'].dt.year
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    params_to_plot = ['DO', 'Temperature', 'pH', 'Salinity']
    
    for idx, param in enumerate(params_to_plot):
        ax = axes[idx]
        
        # Đảm bảo cột là numeric
        df_param = df[[param, 'Quarter_num']].copy()
        df_param[param] = pd.to_numeric(df_param[param], errors='coerce')
        
        # Tính trung bình theo quý (1-4) qua tất cả các năm
        quarterly_avg = df_param.groupby('Quarter_num')[param].mean()
        quarterly_std = df_param.groupby('Quarter_num')[param].std()
        
        quarters = [1, 2, 3, 4]
        means = [quarterly_avg.get(q, 0) for q in quarters]
        stds = [quarterly_std.get(q, 0) for q in quarters]
        
        ax.bar(quarters, means, yerr=stds, capsize=5, 
               color='#2E86AB', alpha=0.7, edgecolor='black', linewidth=1.5)
        
        ax.set_title(MAIN_PARAMS[param], fontsize=12, fontweight='bold')
        ax.set_xlabel('Quý', fontsize=10)
        ax.set_ylabel(MAIN_PARAMS[param], fontsize=10)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Giá trị trung bình các thông số môi trường theo quý (2021-2024)', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '6_quarterly_trends.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '6_quarterly_trends.png'}")
    plt.close()


def plot_summary_statistics():
    """Vẽ thống kê tổng quan"""
    print("\n7. Vẽ thống kê tổng quan...")
    
    # Chọn các thông số chính
    main_stats = ['DO', 'Temperature', 'pH', 'Salinity', 'NH3', 'PO4', 'TSS']
    main_stats = [col for col in main_stats if col in df.columns]
    
    # Tính thống kê
    stats_data = []
    for param in main_stats:
        df_param = df[[param]].copy()
        df_param[param] = pd.to_numeric(df_param[param], errors='coerce')
        stats_data.append({
            'Thông số': MAIN_PARAMS.get(param, param),
            'Min': df_param[param].min(),
            'Mean': df_param[param].mean(),
            'Max': df_param[param].max(),
            'Std': df_param[param].std()
        })
    
    stats_df = pd.DataFrame(stats_data)
    
    # Vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(stats_df))
    width = 0.2
    
    ax.bar(x - 1.5*width, stats_df['Min'], width, label='Min', color='#4A90E2', alpha=0.8)
    ax.bar(x - 0.5*width, stats_df['Mean'] - stats_df['Std'], width, 
           label='Mean - Std', color='#7ED321', alpha=0.8)
    ax.bar(x + 0.5*width, stats_df['Mean'], width, label='Mean', color='#F5A623', alpha=0.8)
    ax.bar(x + 1.5*width, stats_df['Max'], width, label='Max', color='#D0021B', alpha=0.8)
    
    ax.set_xlabel('Thông số', fontsize=11, fontweight='bold')
    ax.set_ylabel('Giá trị', fontsize=11, fontweight='bold')
    ax.set_title('Thống kê tổng quan các thông số môi trường', 
                fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(stats_df['Thông số'], rotation=45, ha='right')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '7_summary_statistics.png', dpi=300, bbox_inches='tight')
    print(f"   ✓ Đã lưu: {OUTPUT_DIR / '7_summary_statistics.png'}")
    plt.close()


def main():
    """Hàm chính"""
    print("=" * 60)
    print("VISUALIZE DỮ LIỆU QUẢNG NINH")
    print("=" * 60)
    
    # Tạo các biểu đồ
    plot_time_series()
    plot_station_comparison()
    plot_correlation_heatmap()
    plot_heavy_metals()
    plot_station_distribution()
    plot_quarterly_trends()
    plot_summary_statistics()
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print(f"Tất cả biểu đồ đã được lưu vào: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

