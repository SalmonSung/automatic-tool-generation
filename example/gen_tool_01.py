import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.seasonal import STL
from langchain_core.tools import tool

def load_csv_with_datetime(file_path, parse_dates=['SNAPSHOT_TIME'], index_col='SNAPSHOT_TIME'):
    """Load CSV file, parse date columns, and set index."""
    return pd.read_csv(file_path, parse_dates=parse_dates, index_col=index_col)

@tool
def analyze_data(file_path):
    """Load data from CSV file and compute summary statistics (mean, median, std) for numeric columns."""
    df = load_csv_with_datetime(file_path)
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    summary_stats = df[numerical_cols].agg(['mean', 'median', 'std'])
    return summary_stats

@tool
def detect_anomalies_zscore(file_path, window=10, threshold=3):
    """Detect anomalies in selected columns ('PING_MS', 'CPU', 'CONNS') using rolling window Z-score method."""
    df = load_csv_with_datetime(file_path)
    anomalies = {}
    for column in ['PING_MS', 'CPU', 'CONNS']:
        if column in df.columns:
            rolling_mean = df[column].rolling(window=window).mean()
            rolling_std = df[column].rolling(window=window).std().replace(0, np.nan)
            z_scores = (df[column] - rolling_mean) / rolling_std
            anomalies[column] = z_scores.abs() > threshold
    return anomalies

@tool
def analyze_time_series(file_path):
    """Perform autocorrelation analysis and seasonal decomposition on system metrics."""
    df = load_csv_with_datetime(file_path)
    columns = ['PING_MS', 'CPU', 'USED_GB', 'CONNS', 'TRANS', 'WAIT_THR', 'BUSY_SQL', 'PEND_SESS', 'D_WR_MBPS']
    autocorr_results = {}
    seasonal_results = {}
    for col in columns:
        series = df[col].dropna()
        autocorr_results[col] = acf(series, nlags=30, fft=False)
        try:
            stl = STL(series, period=7, robust=True).fit()
            seasonal_results[col] = {'trend': stl.trend,
                                     'seasonal': stl.seasonal,
                                     'resid': stl.resid}
        except:
            seasonal_results[col] = None
    return {'autocorrelations': autocorr_results, 'seasonal_decomposition': seasonal_results}

@tool
def analyze_peak_periods(file_path, freq='H'):
    """Resample data to detect peak periods for activity metrics."""
    df = load_csv_with_datetime(file_path)
    resampled = df.resample(freq).agg({
        'CONNS': ['max', 'mean'],
        'TRANS': ['max', 'mean'],
        'BUSY_SQL': ['max', 'mean']
    })
    resampled.columns = ['_'.join(col).strip() for col in resampled.columns]
    return resampled

@tool
def analyze_correlations(file_path):
    """Compute correlation matrix for system metrics."""
    df = load_csv_with_datetime(file_path)
    selected_cols = ['CPU', 'PING_MS', 'USED_GB', 'SWAP_MB', 'CONNS', 'TRANS', 'WAIT_THR', 'BUSY_SQL', 'PEND_SESS', 'D_WR_MBPS', 'DOWN_EVENT']
    corr_matrix = df[selected_cols].corr()
    return corr_matrix

@tool
def cluster_system_snapshots(file_path, n_clusters=3):
    """Cluster snapshots based on performance metrics to identify similar system states."""
    df = load_csv_with_datetime(file_path)
    features = ['PING_MS', 'CPU', 'USED_GB', 'SWAP_MB', 'CONNS', 'TRANS', 'WAIT_THR', 'BUSY_SQL', 'PEND_SESS', 'D_WR_MBPS', 'DOWN_EVENT']
    data = df[features].fillna(0)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(scaled_data)
    return df[['HOST', 'PORT', 'Cluster']], kmeans, scaler

@tool
def detect_time_series_anomalies(file_path, columns=['PING_MS', 'CPU', 'CONNS'], window=20, threshold=3):
    """Detect anomalies in specified columns using rolling window Z-score method."""
    df = load_csv_with_datetime(file_path)
    anomalies = {}
    for col in columns:
        if col in df.columns:
            rolling_mean = df[col].rolling(window=window).mean()
            rolling_std = df[col].rolling(window=window).std().replace(0, np.nan)
            z_scores = (df[col] - rolling_mean) / rolling_std
            anomalies[col] = z_scores.abs() > threshold
    return anomalies

@tool
def analyze_correlation_pairs(file_path, column_pairs):
    """Compute correlation coefficients for specific pairs of columns."""
    df = load_csv_with_datetime(file_path)
    correlations = {}
    for col1, col2 in column_pairs:
        if col1 in df.columns and col2 in df.columns:
            corr_value = df[[col1, col2]].corr().iloc[0,1]
            correlations[f'{col1} vs {col2}'] = corr_value
        else:
            correlations[f'{col1} vs {col2}'] = 'Column not found'
    return correlations