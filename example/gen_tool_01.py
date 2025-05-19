from langchain_core.tools import tool, Tool
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import IsolationForest
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

def load_and_prepare_data(file_path):
    """Load CSV data, parse dates, and set index."""
    df = pd.read_csv(file_path)
    df['SNAPSHOT_TIME'] = pd.to_datetime(df['SNAPSHOT_TIME'])
    df.set_index('SNAPSHOT_TIME', inplace=True)
    return df

@tool
def analyze_time_series_full(file_path: str) -> dict:
    """Load data and perform seasonal decomposition on PING_MS, CPU, and USED_GB columns."""
    df = load_and_prepare_data(file_path)
    columns = ['PING_MS', 'CPU', 'USED_GB']
    decompositions = {}
    for col in columns:
        if col in df.columns:
            try:
                # Interpolate missing values
                ts = df[col].interpolate()
                # Decompose with period=12 (adjust based on data frequency)
                result = sm.tsa.seasonal_decompose(ts, model='additive', period=12)
                decompositions[col] = result
            except Exception as e:
                decompositions[col] = str(e)
        else:
            decompositions[col] = 'Column not found'
    return decompositions

@tool
def analyze_correlations_full(file_path: str) -> dict:
    """Calculate and return the top 3 correlated metrics with CONNS and TRANS."""
    df = load_and_prepare_data(file_path)
    relevant_cols = ['CONNS', 'TRANS', 'PING_MS', 'CPU', 'USED_GB', 'SWAP_MB', 'WAIT_THR', 'BUSY_SQL', 'PEND_SESS', 'D_WR_MBPS']
    df_numeric = df[relevant_cols].dropna()
    corr_matrix = df_numeric.corr()
    results = {}
    for target in ['CONNS', 'TRANS']:
        correlations = corr_matrix[target].drop(labels=[target])
        top3 = correlations.abs().sort_values(ascending=False).head(3)
        results[f'top_correlated_with_{target}'] = top3.to_dict()
    return results

@tool
def detect_anomalies_full(file_path: str, metrics: list=['PING_MS', 'CPU', 'BUSY_SQL'], window_size: int=30, threshold: float=3):
    """Detect anomalies using Z-score method over rolling window."""
    df = pd.read_csv(file_path, index_col='SNAPSHOT_TIME', parse_dates=True)
    df_anomaly = df.copy()
    for metric in metrics:
        if metric not in df.columns:
            continue
        # Rolling mean and std
        rolling_mean = df[metric].rolling(window=window_size, min_periods=1).mean()
        rolling_std = df[metric].rolling(window=window_size, min_periods=1).std()
        # Avoid division by zero
        safe_std = rolling_std.replace(0, 1e-9)
        z_score = (df[metric] - rolling_mean) / safe_std
        # Flag anomalies
        df_anomaly[f'{metric}_anomaly'] = abs(z_score) > threshold
    return df_anomaly

@tool
def analyze_temporal_patterns_full(file_path: str) -> dict:
    """Analyze multiple temporal patterns and detect anomalies for given metrics."""
    df = load_and_prepare_data(file_path)
    metrics = ['CPU', 'USED_GB', 'SWAP_MB', 'CONNS', 'TRANS', 'WAIT_THR', 'BUSY_SQL', 'PEND_SESS', 'D_WR_MBPS', 'DOWN_EVENT']
    results = {}
    for metric in metrics:
        if metric not in df.columns:
            continue
        series = df[metric].dropna()
        # Moving average for trend
        window_size = max(1, len(series)//10)
        moving_avg = series.rolling(window=window_size, min_periods=1).mean()
        # Seasonal decomposition
        try:
            decomposition = seasonal_decompose(series, model='additive', period=12)
            seasonal = decomposition.seasonal
            trend = decomposition.trend
            residual = decomposition.resid
        except Exception:
            seasonal = trend = residual = pd.Series([np.nan] * len(series), index=series.index)
        # Anomaly detection with Isolation Forest
        reshaped = series.values.reshape(-1,1)
        clf = IsolationForest(contamination='auto', random_state=42)
        clf.fit(reshaped)
        preds = clf.predict(reshaped)
        anomalies_idx = series.index[preds == -1]
        results[metric] = {
            'moving_avg': moving_avg,
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'anomalies': anomalies_idx
        }
    return results

tools = [analyze_time_series_full, analyze_correlations_full, detect_anomalies_full, analyze_temporal_patterns_full]