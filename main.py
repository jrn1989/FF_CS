import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime
from datetime import timedelta

st.set_page_config(layout = "wide")
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df_final_long = pd.read_csv("clusters_final_all_vars_modified_with_cats.csv", encoding="utf-8")
df_final_long["datetime"] = df_final_long["date"].values + " " + df_final_long["hour"].astype("str").str.zfill(2) + ":00:00"

df_final_long["date"] = pd.to_datetime(df_final_long['date'])
df_final_long["datetime"] = pd.to_datetime(df_final_long['datetime'])

#clist = df_final_long['cuisine_type'].unique()
#cuisine_type = st.sidebar.multiselect("Select a cuisine type:",clist)

st.header("FF-CS")
st.subheader('By José Robles')

aggregation_type = st.sidebar.selectbox('Select aggregation level', ['cuisine_type','item_type'])
variable_type = st.sidebar.selectbox('Select variable', ['requested_orders','accepted_orders', 'completed_orders_ofo_state','total_eater_spend', 
'first_time_orders', 'returning_orders'])

#range_time = st.sidebar.slider(
#     "When do you start?",
#     min_value = datetime(2022, 2, 14, 16, 0),
#     max_value = datetime(2022, 2, 28, 2, 0),
#     value=[datetime(2022, 2, 14, 16, 0),datetime(2022, 2, 28, 2, 0)],
#     step = timedelta(hours=1),
#     format="DD/MM/YY - hh:mm")



if aggregation_type == "cuisine_type":
    item_or_cuisine_list = df_final_long['cuisine_type'].unique()
    label_item_or_cuisine = "Select a cuisine type:"
else:
    item_or_cuisine_list = df_final_long['item_type'].unique()
    label_item_or_cuisine = "Select a item type:"

item_or_cuisine_type = st.sidebar.multiselect(label_item_or_cuisine,item_or_cuisine_list, default=item_or_cuisine_list)




#st.sidebar.subheader("Plot filters")
#time_type = st.sidebar.selectbox("Period:",["By time of day", "By day of week"])
#time_type = st.sidebar.selectbox("Period:",["By time of day", "By day of week"])


col1, col2 = st.columns(2)
with st.container():
    if aggregation_type == "cuisine_type":
        #by_time = df_final_long.query("datetime > @range_time[0] & datetime< @range_time[1]")[["datetime","cuisine_type",variable_type]]
        by_time = df_final_long[["datetime","cuisine_type",variable_type]]
        by_time = df_final_long.groupby(["datetime", "cuisine_type"]).sum().reset_index(drop=False)
        fig = px.line(by_time.query("cuisine_type in @item_or_cuisine_type"), x="datetime",y=variable_type, color="cuisine_type")
        col1.plotly_chart(fig,use_container_width = True)

        by_day = df_final_long[["date","cuisine_type",variable_type]]
        by_day = df_final_long.groupby(["date", "cuisine_type"]).sum().reset_index(drop=False)
        fig = px.line(by_day.query("cuisine_type in @item_or_cuisine_type"), x="date",y=variable_type, color="cuisine_type")
        col2.plotly_chart(fig,use_container_width = True)
    else:
        by_time = df_final_long[["datetime","item_type",variable_type]]
        by_time = df_final_long.groupby(["datetime", "item_type"]).sum().reset_index(drop=False)
        fig = px.line(by_time.query("item_type in @item_or_cuisine_type"), x="datetime",y=variable_type, color="item_type")
        col1.plotly_chart(fig,use_container_width = True)

        by_day = df_final_long[["date","item_type",variable_type]]
        by_day = df_final_long.groupby(["date", "item_type"]).sum().reset_index(drop=False)
        fig = px.line(by_day.query("item_type in @item_or_cuisine_type"), x="date",y=variable_type, color="item_type")
        col2.plotly_chart(fig,use_container_width = True)
        
        
col3, col4 = st.columns(2)
with st.container():
    if aggregation_type == "cuisine_type":
        by_time = df_final_long[["datetime","cuisine_type",variable_type]]
        by_time = df_final_long.groupby(["datetime", "cuisine_type"]).sum().reset_index(drop=False)   
        by_time2 = df_final_long.groupby(["cuisine_type"]).sum().reset_index(drop=False)
        
        fig = px.bar(by_time2, y=variable_type, x='cuisine_type', text_auto='.2s')#, title="Default: various text sizes, positions and angles")
        col3.plotly_chart(fig,use_container_width = True)

        fig = px.pie(by_day.query("cuisine_type in @item_or_cuisine_type"), names="cuisine_type",values=variable_type)
        col4.plotly_chart(fig,use_container_width = True)
    else:
        by_time = df_final_long[["datetime","item_type",variable_type]]
        by_time = df_final_long.groupby(["datetime", "item_type"]).sum().reset_index(drop=False)   
        by_time2 = df_final_long.groupby(["item_type"]).sum().reset_index(drop=False)
        
        fig = px.bar(by_time2, y=variable_type, x='item_type', text_auto='.2s')#, title="Default: various text sizes, positions and angles")
        col3.plotly_chart(fig,use_container_width = True)

        fig = px.pie(by_day.query("item_type in @item_or_cuisine_type"), names="item_type",values=variable_type)
        col4.plotly_chart(fig,use_container_width = True)

        
#if variable_type == 'requested_orders':
#    print("ok")
#    col1, col2 = st.columns(2)
#    
#elif page == "total_eater_spend":
#    print("wait")
#else:
#    print("ELSE")

#if(time_type=="By hour"):
#    print("POR HORA")
#    xx = df_final_long[["datetime","cuisine_type","requested_orders"]]
#    xx = df_final_long.groupby(["datetime", "cuisine_type"]).sum().reset_index(drop=False)
#    fig = px.line(xx.query("cuisine_type in @cuisine_type"), x="datetime",y="requested_orders", color="cuisine_type")
#else:
#
#    yy = df_final_long[["date","cuisine_type","requested_orders"]]
#    yy = df_final_long.groupby(["date", "cuisine_type"]).sum().reset_index(drop=False)
#
#    fig = px.line(yy.query("cuisine_type in @cuisine_type"), x="date",y="requested_orders", color="cuisine_type")


# Plot!
#st.plotly_chart(fig, use_container_width=True)