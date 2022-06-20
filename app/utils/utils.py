import requests as rq
import pandas as pd
import plotly.express as px
import json
import matplotlib.dates as mpl_dates


def request_data(url: str, return_df=True):
    response = rq.get(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        },
    )
    if response.status_code == 200:
        return pd.DataFrame(response.json()) if return_df else response.json()
    return pd.DataFrame([])


def read_config(fname: str = "config.json") -> dict:
    with open(fname, "r") as f:
        config = json.loads(f.read())
    return config


def get_maker_dao(trunc_date="daily", normal_df=True) -> pd.DataFrame:
    urls = read_config()
    urs = urls["FLIPSIDE"]["DAILY"]
    df = request_data(url=urs, return_df=True)
    df.columns = df.columns.str.capitalize()
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True)
    df = trunc_by(data=df, by=trunc_date)

    if not normal_df:
        df = further_processing(data=df)
    return df


def get_data(
    trunc_date: str = "daily", network: str = "ETH", timeframe: str = "30"
) -> pd.DataFrame:
    urls = read_config()
    url = urls["FLIPSIDE"][network][trunc_date.upper()][timeframe]
    df = request_data(url=url, return_df=True)
    df.columns = df.columns.str.capitalize()
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True)
    return df


def option_handle(option: str):
    return "ETH" if option == "Ethereum" else "MATIC"


def trunc_by(data: pd.DataFrame, by: str = "W-MON") -> pd.DataFrame:
    if by == "daily":
        return data[:-1]
    if by == "monthly":
        by_change = "MS"
    elif by == "weekly":
        by_change = "W-MON"
    return (
        data.resample(by_change, label="left", closed="left", on="Date")
        .sum()
        .reset_index()
        .sort_values(by="Date")
    )


def get_date_truncations(self, data: pd.DataFrame) -> dict:
    """
    Creates Weekly and Monthly  dict.

    Args:
        data (pd.DataFrame): Dataframe of Daily data.

    Returns:
            dict: Daily, Weekly and Monthly  dataframes.
    """
    weekly = trunc_by(data=data, by="W")
    monthly = trunc_by(data=data, by="M")
    return {"daily": data, "weekly": weekly, "monthly": monthly}


def plot_vlines_mkr(fig, color: str = "black"):
    """
    WHEN date >= '2021-06-21' AND date <= '2021-07-19' THEN 'Reduced stability fee'
    WHEN date >= '2021-07-19' AND date <= '2021-11-10' THEN 'Reduced stability fee'
    WHEN date >= '2022-01-25' THEN 'Reduced stability fee'
    ELSE 'Increased stability fee'
    """
    fig.add_vline(
        x=pd.to_datetime("2021-06-21").timestamp() * 1_000,
        line_width=2,
        line_dash="dash",
        line_color=color,
        annotation_text=" Reduced stability fee",
        annotation_position="top right",
    )
    fig.add_vline(
        x=pd.to_datetime("2021-07-19").timestamp() * 1_000,
        line_width=2,
        line_dash="dash",
        line_color=color,
        annotation_text=" Increased stability fee",
        annotation_position="bottom right",
    )
    fig.add_vline(
        x=pd.to_datetime("2022-01-25").timestamp() * 1_000,
        line_width=2,
        line_dash="dash",
        line_color=color,
        annotation_text=" Reduced stability fee",
        annotation_position="top right",
    )


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
