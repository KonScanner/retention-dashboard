import streamlit as st
from utils.utils import get_data, hide_streamlit_style, option_handle, plot_bar
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Wallet Retention", page_icon="./img/retention.jpg", layout="wide"
)
st.markdown("# Wallet Retention", unsafe_allow_html=True)


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    """
    **Wallet/User Retention**: Is the ability of a network or DeFi protocol to retain its customers over some specified period of time.
    """
)

st.markdown(
    """
    **NOTE**: Do note that the last day,week,month is always incomplete as data is still being back-filled for that day, week, month.
    """
)
st.markdown(
    """
    All data is sourced from [FlipsideCrypto](https://flipsidecrypto.xyz/).
    """
)


option = st.sidebar.selectbox("View:", ("daily", "weekly", "monthly"), index=1)
option2 = st.sidebar.selectbox("Network:", ("Ethereum", "Polygon"), index=0)
option3 = option_handle(option=option2)
option4 = st.sidebar.selectbox("Type", ("Stacked", "Grouped", "Proportion"), index=0)


@st.cache(suppress_st_warning=True)
def load_data():
    return [
        get_data(trunc_date=option, network=option3, timeframe=j)
        for j in ["30", "90", "180", "365", "ALL"]
    ]


(data_30, data_90, data_180, data_365, data_all) = load_data()

fig_cols = st.columns(2)
with fig_cols[0]:
    # st.markdown("### Second Chart Title")
    fig = plot_bar(data=data_30, option4=option4)
    fig.update_layout(
        title_text=f"User Retention {option2.capitalize()} | Last 30 days | {option.capitalize()}"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

with fig_cols[1]:
    fig = plot_bar(data=data_90, option4=option4)
    fig.update_layout(
        title_text=f"User Retention {option2.capitalize()} | Last 90 days | {option.capitalize()}"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

st.markdown(
    """
        <hr>
    """,
    unsafe_allow_html=True,
)

fig_cols2 = st.columns(2)
with fig_cols2[0]:
    # st.markdown("### Second Chart Title")
    fig = plot_bar(data=data_180, option4=option4)
    fig.update_layout(
        title_text=f"User Retention {option2.capitalize()} | Last 180 days | {option.capitalize()}"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

with fig_cols2[1]:
    fig = plot_bar(data=data_365, option4=option4)

    fig.update_layout(
        title_text=f"User Retention {option2.capitalize()} | Last 365 days | {option.capitalize()}"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(autosize=True, width=800, height=600)
    st.write(fig)

st.markdown(
    """
        <hr>
    """,
    unsafe_allow_html=True,
)
fig = plot_bar(data=data_all, option4=option4)
fig.update_layout(
    title_text=f"User Retention {option2.capitalize()} | All-Time | {option.capitalize()}"
)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Count")
fig.update_layout(autosize=True, width=1500, height=800)
st.write(fig)
# st.markdown(
#     """
#         <iframe loading="lazy" src="https://velocity-app.flipsidecrypto.com/velocity/visuals/3ce232d2-3350-4539-8902-6cae1456fdbd/43fa7dee-c660-463b-8434-169c686584c9" width="100%" height="600"></iframe>
#     """,
#     unsafe_allow_html=True,
# )
