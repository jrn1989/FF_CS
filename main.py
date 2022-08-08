import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from millify import millify

st.set_page_config(layout = "wide")
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df_final_long = pd.read_csv("clusters_final_all_vars_modified_with_cats.csv", encoding="utf-8")
df_final_long["datetime"] = df_final_long["date"].values + " " + df_final_long["hour"].astype("str").str.zfill(2) + ":00:00"

df1=df_final_long.query("date in ['14/02/2022','15/02/2022','16/02/2022','17/02/2022','18/02/2022','19/02/2022','20/02/2022']")
df2=df_final_long.query("date in ['21/02/2022','22/02/2022','23/02/2022','24/02/2022','25/02/2022','26/02/2022','27/02/2022'] ")

df1["date"] = pd.to_datetime(df1['date'] )#, format='%d/%m/%Y')
df1["datetime"] = pd.to_datetime(df1['datetime'])
df1["week"] = "7"


df2["date"] = pd.to_datetime(df2['date'])# , format='%d/%m/%Y')
df2["datetime"] = pd.to_datetime(df2['datetime'])
df2["week"] = "8"


#df_final_long["date"] = pd.to_datetime(df_final_long['date'], format='%d/%m/%Y')
#df_final_long["datetime"] = pd.to_datetime(df_final_long['datetime'])



#clist = df_final_long['cuisine_type'].unique()
#cuisine_type = st.sidebar.multiselect("Select a cuisine type:",clist)

st.header("FF-CS")
st.subheader('By José Robles')

range_time = st.sidebar.slider(
     "Time period",
     min_value = datetime(2022, 2, 21, 0, 0),
     max_value = datetime(2022, 2, 27, 23, 59),
     value=[datetime(2022, 2, 21, 0, 0),datetime(2022, 2, 27, 23, 59)],
     step = timedelta(hours=1),
     format="d"
     )
     #format="DD/MM/YY - hh:mm")

st.sidebar.write("Start date:", range_time[0])
st.sidebar.write("  End date:", range_time[1])

aggregation_type = st.sidebar.selectbox('View', ['cuisine_type','item_type'])

top = st.sidebar.radio(
     "Elements",
     ('Top 10', 'Top 5', 'Specific elements'))

#variable_type = st.sidebar.selectbox('Select variable', ['requested_orders','accepted_orders', 'completed_orders_ofo_state','total_eater_spend', 
#'first_time_orders', 'returning_orders'])

#operation_type = st.sidebar.selectbox('Select operation', ['sum','mean', 'count'])
#print(range_time[0])
#print(range_time[0]-timedelta(days=7))

fecha_ini_para_df1 = range_time[0]-timedelta(days=7)
fecha_fin_para_df1 = range_time[1]-timedelta(days=7)
fecha_ini_para_df2 = range_time[0]
fecha_fin_para_df2 = range_time[1]

print("XXXXXXXXXXXXXXXXXX")
print(fecha_ini_para_df1)
print(fecha_fin_para_df1)
print(fecha_ini_para_df2)
print(fecha_fin_para_df2)

tab_kpi, tab_otro = st.tabs(["Orders","Revenue"])


#print(type(datetime.strptime(str(range_time[0]), '%Y-%m-%d %H:%M:%S' )))
#xxx = df_final_long.query("datetime > @range_time[0] ")[["datetime","cuisine_type",variable_type]]

col1, col2, col3 = st.columns(3)

if aggregation_type == "cuisine_type":
    item_or_cuisine_list = df_final_long['cuisine_type'].unique()
    label_item_or_cuisine = "Select cuisine types:"
else:
    item_or_cuisine_list = df_final_long['item_type'].unique()
    label_item_or_cuisine = "Select item types:"

df1_filtrado_ini = df1[(df1['datetime']>=fecha_ini_para_df1) & (df1['datetime']<=fecha_fin_para_df1)].copy()
df2_filtrado_ini = df2[(df2['datetime']>=fecha_ini_para_df2) & (df2['datetime']<=fecha_fin_para_df2)].copy()
#print(df2_filtrado)
#print(df2_filtrado.columns)

if top != "Specific elements":
    item_or_cuisine_type_new_customer = st.sidebar.multiselect(label_item_or_cuisine,item_or_cuisine_list, default=[], disabled=True)
    if aggregation_type == "cuisine_type" and top == 'Top 10':
        #print("AQUI")
        item_or_cuisine_type_new_customer = df2_filtrado_ini[["cuisine_type", "first_time_orders"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="first_time_orders", ascending=False).head(10)["cuisine_type"].tolist()
        item_or_cuisine_type_completed_orders = df2_filtrado_ini[["cuisine_type", "completed_orders_ofo_state"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="completed_orders_ofo_state", ascending=False).head(10)["cuisine_type"].tolist()
        item_or_cuisine_type_revenue = df2_filtrado_ini[["cuisine_type", "total_eater_spend"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="total_eater_spend", ascending=False).head(10)["cuisine_type"].tolist()
        item_or_cuisine_type_req_orders = df2_filtrado_ini[["cuisine_type", "requested_orders"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="requested_orders", ascending=False).head(10)["cuisine_type"].tolist()
        #print(item_or_cuisine_type_new_customer)
    elif aggregation_type == "cuisine_type" and top == 'Top 5':
        print("AQUI2")
        item_or_cuisine_type_new_customer = df2_filtrado_ini[["cuisine_type", "first_time_orders"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="first_time_orders", ascending=False).head(5)["cuisine_type"].tolist()
        item_or_cuisine_type_completed_orders = df2_filtrado_ini[["cuisine_type", "completed_orders_ofo_state"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="completed_orders_ofo_state", ascending=False).head(5)["cuisine_type"].tolist()
        item_or_cuisine_type_revenue = df2_filtrado_ini[["cuisine_type", "total_eater_spend"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="total_eater_spend", ascending=False).head(5)["cuisine_type"].tolist()
        item_or_cuisine_type_req_orders = df2_filtrado_ini[["cuisine_type", "requested_orders"]].groupby([ "cuisine_type"]).sum().reset_index(drop=False).sort_values(by="requested_orders", ascending=False).head(5)["cuisine_type"].tolist()
    elif aggregation_type == "item_type" and top == 'Top 10':
        print("AQUI3")
        item_or_cuisine_type_new_customer = df2_filtrado_ini[["item_type", "first_time_orders"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="first_time_orders", ascending=False).head(10)["item_type"].tolist()
        item_or_cuisine_type_completed_orders = df2_filtrado_ini[["item_type", "completed_orders_ofo_state"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="completed_orders_ofo_state", ascending=False).head(10)["item_type"].tolist()
        item_or_cuisine_type_revenue = df2_filtrado_ini[["item_type", "total_eater_spend"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="total_eater_spend", ascending=False).head(10)["item_type"].tolist()
        item_or_cuisine_type_req_orders = df2_filtrado_ini[["item_type", "requested_orders"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="requested_orders", ascending=False).head(10)["item_type"].tolist()
    #elif aggregation_type == "item_type" and top == 'Top 5':
    else:
        print("AQUI4")
        item_or_cuisine_type_new_customer = df2_filtrado_ini[["item_type", "first_time_orders"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="first_time_orders", ascending=False).head(5)["item_type"].tolist()
        item_or_cuisine_type_completed_orders = df2_filtrado_ini[["item_type", "completed_orders_ofo_state"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="completed_orders_ofo_state", ascending=False).head(5)["item_type"].tolist()
        item_or_cuisine_type_revenue = df2_filtrado_ini[["item_type", "total_eater_spend"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="total_eater_spend", ascending=False).head(5)["item_type"].tolist()
        item_or_cuisine_type_req_orders = df2_filtrado_ini[["item_type", "requested_orders"]].groupby([ "item_type"]).sum().reset_index(drop=False).sort_values(by="requested_orders", ascending=False).head(5)["item_type"].tolist()
else:
    item_or_cuisine_type_new_customer = st.sidebar.multiselect(label_item_or_cuisine,item_or_cuisine_list, default=[], disabled=False)
    item_or_cuisine_type_completed_orders = item_or_cuisine_type_new_customer
    item_or_cuisine_type_revenue = item_or_cuisine_type_new_customer
    item_or_cuisine_type_req_orders = item_or_cuisine_type_new_customer
    
#if top == "Specific elements":
#    print("AQUI5")
#    item_or_cuisine_type_new_customer = st.sidebar.multiselect(label_item_or_cuisine,item_or_cuisine_list, default=[], disabled=False)
#else:
#    print("AQUI6")
    

#print("item_or_cuisine_type_new_customer:")
#print(item_or_cuisine_type_new_customer)

with tab_otro:
    # REVENUE
    
    col9, col10 = st.columns(2)      
    col11, col2 = st.columns(2)
           
    st.markdown("""---""")

    if aggregation_type == "cuisine_type":
        df1_filtrado=df1_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_revenue")
        df2_filtrado=df2_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_revenue")
        revenue_top = df2_filtrado[["cuisine_type","total_eater_spend"]].groupby(["cuisine_type"]).agg("sum").reset_index(drop=False).sort_values(by="total_eater_spend")
    else:
        df1_filtrado=df1_filtrado_ini.query("item_type in @item_or_cuisine_type_revenue")
        df2_filtrado=df2_filtrado_ini.query("item_type in @item_or_cuisine_type_revenue")
        revenue_top = df2_filtrado[["item_type","total_eater_spend"]].groupby(["item_type"]).agg("sum").reset_index(drop=False).sort_values(by="total_eater_spend")

        
    revenue = df2_filtrado["total_eater_spend"].sum()
    delta_revenue = (( df2_filtrado["total_eater_spend"].sum() - df1_filtrado["total_eater_spend"].sum() ) / df1_filtrado["total_eater_spend"].sum())*100
            
    if aggregation_type == "cuisine_type":
        fig2 = px.bar(revenue_top,  x="total_eater_spend",y="cuisine_type",orientation='h', title="Top elements")
    else:
        fig2 = px.bar(revenue_top,  x="total_eater_spend",y="item_type",orientation='h', title="Top elements")
    
    col9.markdown("<h3>Revenue</h3>", unsafe_allow_html=True)
    col9.metric("", millify(revenue, precision=2), delta=str(round(delta_revenue,2))+"%")
    
    #col7.plotly_chart(fig,use_container_width = True)
    with col11:
        revenue_radio=st.radio("  ",("By day of the week","By time of the day"), horizontal=True)
        if(revenue_radio=="By day of the week"):
            revenue_group1 = df1_filtrado[["date","week","total_eater_spend"]]
            revenue_group1 = revenue_group1.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
            revenue_group1["date"] = revenue_group1["date"] + timedelta(days=7)
        
            revenue_group2 = df2_filtrado[["date","week","total_eater_spend"]]
            revenue_group2 = revenue_group2.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
        
            revenue_group = pd.concat([revenue_group1, revenue_group2], axis=0)
            fig = px.bar(revenue_group, x="date",y="total_eater_spend", color="week",barmode = 'group', title='Comparison against previous week')
        else:
            revenue_group1 = df1_filtrado[["datetime","week","total_eater_spend"]]
            revenue_group1 = revenue_group1.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
            revenue_group1["datetime"] = revenue_group1["datetime"] + timedelta(days=7)
        
            revenue_group2 = df2_filtrado[["datetime","week","total_eater_spend"]]
            revenue_group2 = revenue_group2.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
        
            revenue_group = pd.concat([revenue_group1, revenue_group2], axis=0)
            fig = px.bar(revenue_group, x="datetime",y="total_eater_spend", color="week",barmode = 'group', title='Comparison against previous week')
        
        st.plotly_chart(fig,use_container_width = True)
    col2.text("")
    col2.text("")
    col2.text("")
    col2.text("")
    col2.text("")
    col2.plotly_chart(fig2,use_container_width = True)
    cola, colb= st.columns(2)
 
    if aggregation_type == "cuisine_type":
        df2_filtrado_tab2=df2_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_revenue")
        #df2_filtrado=df2_filtrado.query("cuisine_type in @item_or_cuisine_type_new_customer")
        #new_customers_top = df2_filtrado[["cuisine_type","first_time_orders"]].groupby(["cuisine_type"]).agg("sum").reset_index(drop=False).sort_values(by="first_time_orders")
        #print(new_customers_top)
    else:
        df2_filtrado_tab2=df2_filtrado_ini.query("item_type in @item_or_cuisine_type_revenue")
        #df2_filtrado=df2_filtrado.query("item_type in @item_or_cuisine_type_new_customer")
        #new_customers_top = df2_filtrado[["item_type","first_time_orders"]].groupby(["item_type"]).agg("sum").reset_index(drop=False).sort_values(by="first_time_orders")

    orders_tab2 = df2_filtrado_tab2["completed_orders_ofo_state"].sum()
    revenue_tab2 =  df2_filtrado_tab2["total_eater_spend"].sum()
    #delta_orders = (( df2_filtrado["completed_orders_ofo_state"].sum() - df1_filtrado["completed_orders_ofo_state"].sum() ) / df1_filtrado["completed_orders_ofo_state"].sum())*100
    #col3.metric("Completed Orders", millify(orders, precision=2), delta=str(round(delta_orders,2))+"%")
 
    if orders_tab2!=0:
        aov = revenue_tab2 / orders_tab2
        #aov_old = df1_filtrado["total_eater_spend"].sum() / df1_filtrado["completed_orders_ofo_state"].sum()
        #delta_aov = ( ( aov-aov_old ) / aov_old )*100
    else:
        aov = 0
        #delta_aov = 0
        
    #print(aov_week)
    with cola:
        st.markdown("<h3>Average order value</h3>", unsafe_allow_html=True)
        st.metric("_", millify(aov, precision=2))
    
        aov_radio=st.radio(". ",("By day of the week","By time of the day"), horizontal=True)
        if(aov_radio=="By day of the week"):
            aov_week = df2_filtrado_tab2[["date", "total_eater_spend","completed_orders_ofo_state"]].groupby(["date"]).agg("sum").reset_index(drop=False).copy()#.sort_values(by="first_time_orders")
            aov_week["average_order_value"] = aov_week["total_eater_spend"] / aov_week["completed_orders_ofo_state"]
            fig_tab2 = px.area(aov_week, x="date",y="average_order_value", title='Daily average order value')
        else:
            aov_week = df2_filtrado_tab2[["datetime", "total_eater_spend","completed_orders_ofo_state"]].groupby(["datetime"]).agg("sum").reset_index(drop=False).copy()#.sort_values(by="first_time_orders")
            aov_week["average_order_value"] = aov_week["total_eater_spend"] / aov_week["completed_orders_ofo_state"]
            fig_tab2 = px.area(aov_week, x="datetime",y="average_order_value", title='Daily average order value')
        st.plotly_chart(fig_tab2,use_container_width = False)

    st.markdown("""---""")
    bubble_radio = st.radio(".",("By day of the week","By time of the day"), horizontal=True)
    if(bubble_radio=="By day of the week" and aggregation_type == "cuisine_type"):
        df_bubble = df2_filtrado_tab2[["date", "cuisine_type","total_eater_spend","completed_orders_ofo_state"]].groupby(["date", "cuisine_type"]).agg("sum").reset_index(drop=False).copy()
        fig2_tab2 = px.scatter(df_bubble, x="date",y="total_eater_spend", size="completed_orders_ofo_state",color="cuisine_type", title='Revenue, Completed orders by cuisine_type')
        st.plotly_chart(fig2_tab2, use_container_width=False)
    elif (bubble_radio=="By time of the day" and aggregation_type == "cuisine_type"):
        df_bubble = df2_filtrado_tab2[["datetime", "cuisine_type","total_eater_spend","completed_orders_ofo_state"]].groupby(["datetime", "cuisine_type"]).agg("sum").reset_index(drop=False).copy()
        fig2_tab2 = px.scatter(df_bubble, x="datetime",y="total_eater_spend", size="completed_orders_ofo_state",color="cuisine_type", title='Revenue, Completed orders by cuisine_type')
        st.plotly_chart(fig2_tab2, use_container_width=False)
    elif (bubble_radio=="By day of the week" and aggregation_type == "item_type"):
        df_bubble = df2_filtrado_tab2[["date", "item_type","total_eater_spend","completed_orders_ofo_state"]].groupby(["date", "item_type"]).agg("sum").reset_index(drop=False).copy()
        fig2_tab2 = px.scatter(df_bubble, x="date",y="total_eater_spend", size="completed_orders_ofo_state",color="item_type", title='Revenue, Completed orders by item_type')
        st.plotly_chart(fig2_tab2, use_container_width=False)
    else:
        df_bubble = df2_filtrado_tab2[["datetime", "item_type","total_eater_spend","completed_orders_ofo_state"]].groupby(["datetime", "item_type"]).agg("sum").reset_index(drop=False).copy()
        fig2_tab2 = px.scatter(df_bubble, x="datetime",y="total_eater_spend", size="completed_orders_ofo_state",color="item_type", title='Revenue, Completed orders by item_type')
        st.plotly_chart(fig2_tab2, use_container_width=False)
    

with tab_kpi:
    
    ### NEW CUSTOMERS
    
    col1, col2 = st.columns(2)      
    col3, col4 = st.columns(2)
           
    st.markdown("""---""")

    if aggregation_type == "cuisine_type":
        df1_filtrado=df1_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_new_customer")
        df2_filtrado=df2_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_new_customer")
        new_customers_top = df2_filtrado[["cuisine_type","first_time_orders"]].groupby(["cuisine_type"]).agg("sum").reset_index(drop=False).sort_values(by="first_time_orders")
        #print(new_customers_top)
    else:
        df1_filtrado=df1_filtrado_ini.query("item_type in @item_or_cuisine_type_new_customer")
        df2_filtrado=df2_filtrado_ini.query("item_type in @item_or_cuisine_type_new_customer")
        new_customers_top = df2_filtrado[["item_type","first_time_orders"]].groupby(["item_type"]).agg("sum").reset_index(drop=False).sort_values(by="first_time_orders")

        
    new_customers = df2_filtrado["first_time_orders"].sum()
    delta_new_costumers = (( df2_filtrado["first_time_orders"].sum() - df1_filtrado["first_time_orders"].sum() ) / df1_filtrado["first_time_orders"].sum())*100
    
    if aggregation_type == "cuisine_type":
        fig2 = px.bar(new_customers_top,  x="first_time_orders",y="cuisine_type",orientation='h', title="Top elements")
    else:
        fig2 = px.bar(new_customers_top,  x="first_time_orders",y="item_type",orientation='h', title="Top elements")
        
    col1.markdown("<h3>New Customers</h3>", unsafe_allow_html=True)
    col1.metric("", millify(new_customers, precision=2), delta=str(round(delta_new_costumers,2))+"%")
    
    with col3:
        new_customers_radio=st.radio("",("By day of the week","By time of the day"), horizontal=True)
        if(new_customers_radio=="By day of the week"):
            new_customers_group1 = df1_filtrado[["date","week","first_time_orders"]]
            new_customers_group1 = new_customers_group1.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
            new_customers_group1["date"] = new_customers_group1["date"] + timedelta(days=7)
        
            new_customers_group2 = df2_filtrado[["date","week","first_time_orders"]]
            new_customers_group2 = new_customers_group2.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
        
            new_customers_group = pd.concat([new_customers_group1, new_customers_group2], axis=0)
            fig = px.bar(new_customers_group, x="date",y="first_time_orders", color="week",barmode = 'group', title='Comparison against previous week')
        else:
            new_customers_group1 = df1_filtrado[["datetime","week","first_time_orders"]]
            new_customers_group1 = new_customers_group1.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
            new_customers_group1["datetime"] = new_customers_group1["datetime"] + timedelta(days=7)
        
            new_customers_group2 = df2_filtrado[["datetime","week","first_time_orders"]]
            new_customers_group2 = new_customers_group2.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
        
            new_customers_group = pd.concat([new_customers_group1, new_customers_group2], axis=0)
            fig = px.bar(new_customers_group, x="datetime",y="first_time_orders", color="week",barmode = 'group', title='Comparison against previous week')
        
        st.plotly_chart(fig,use_container_width = True)
        
    col4.text("")
    col4.text("")
    col4.text("")
    col4.text("")
    col4.text("")
    col4.plotly_chart(fig2,use_container_width = True)
    
    ### COMPLETED ORDERS
    
    col5, col6 = st.columns(2)      
    col7, col8 = st.columns(2)
           
    st.markdown("""---""")

    if aggregation_type == "cuisine_type":
        df1_filtrado=df1_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_completed_orders")
        df2_filtrado=df2_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_completed_orders")
        completed_orders_top = df2_filtrado[["cuisine_type","completed_orders_ofo_state"]].groupby(["cuisine_type"]).agg("sum").reset_index(drop=False).sort_values(by="completed_orders_ofo_state")
    else:
        df1_filtrado=df1_filtrado_ini.query("item_type in @item_or_cuisine_type_completed_orders")
        df2_filtrado=df2_filtrado_ini.query("item_type in @item_or_cuisine_type_completed_orders")
        completed_orders_top = df2_filtrado[["item_type","completed_orders_ofo_state"]].groupby(["item_type"]).agg("sum").reset_index(drop=False).sort_values(by="completed_orders_ofo_state")

        
    orders = df2_filtrado["completed_orders_ofo_state"].sum()
    delta_orders = (( df2_filtrado["completed_orders_ofo_state"].sum() - df1_filtrado["completed_orders_ofo_state"].sum() ) / df1_filtrado["completed_orders_ofo_state"].sum())*100
            
    if aggregation_type == "cuisine_type":
        fig2 = px.bar(completed_orders_top,  x="completed_orders_ofo_state",y="cuisine_type",orientation='h', title="Top elements")
    else:
        fig2 = px.bar(completed_orders_top,  x="completed_orders_ofo_state",y="item_type",orientation='h', title="Top elements")
        
    col5.markdown("<h3>Completed orders</h3>", unsafe_allow_html=True)
    col5.metric("", millify(orders, precision=2), delta=str(round(delta_orders,2))+"%")
    
    #col7.plotly_chart(fig,use_container_width = True)
    with col7:
        completed_orders_radio=st.radio(" ",("By day of the week","By time of the day"), horizontal=True)
        if(completed_orders_radio=="By day of the week"):
            completed_orders_group1 = df1_filtrado[["date","week","completed_orders_ofo_state"]]
            completed_orders_group1 = completed_orders_group1.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
            completed_orders_group1["date"] = completed_orders_group1["date"] + timedelta(days=7)
        
            completed_orders_group2 = df2_filtrado[["date","week","completed_orders_ofo_state"]]
            completed_orders_group2 = completed_orders_group2.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
        
            completed_orders_group = pd.concat([completed_orders_group1, completed_orders_group2], axis=0)
            fig = px.bar(completed_orders_group, x="date",y="completed_orders_ofo_state", color="week",barmode = 'group', title='Comparison against previous week')
        else:
            completed_orders_group1 = df1_filtrado[["datetime","week","completed_orders_ofo_state"]]
            completed_orders_group1 = completed_orders_group1.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
            completed_orders_group1["datetime"] = completed_orders_group1["datetime"] + timedelta(days=7)
        
            completed_orders_group2 = df2_filtrado[["datetime","week","completed_orders_ofo_state"]]
            completed_orders_group2 = completed_orders_group2.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
        
            completed_orders_group = pd.concat([completed_orders_group1, completed_orders_group2], axis=0)
            fig = px.bar(completed_orders_group, x="datetime",y="completed_orders_ofo_state", color="week",barmode = 'group', title='Comparison against previous week')
        
        st.plotly_chart(fig,use_container_width = True)
    col8.text("")
    col8.text("")
    col8.text("")
    col8.text("")
    col8.text("")
    col8.plotly_chart(fig2,use_container_width = True)
    


    # REQUESTED ORDERS
    
    col13, col14 = st.columns(2)      
    col15, col16 = st.columns(2)
           
    st.markdown("""---""")

    if aggregation_type == "cuisine_type":
        df1_filtrado=df1_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_req_orders")
        df2_filtrado=df2_filtrado_ini.query("cuisine_type in @item_or_cuisine_type_req_orders")
        req_orders_top = df2_filtrado[["cuisine_type","requested_orders"]].groupby(["cuisine_type"]).agg("sum").reset_index(drop=False).sort_values(by="requested_orders")
    else:
        df1_filtrado=df1_filtrado_ini.query("item_type in @item_or_cuisine_type_req_orders")
        df2_filtrado=df2_filtrado_ini.query("item_type in @item_or_cuisine_type_req_orders")
        req_orders_top = df2_filtrado[["item_type","requested_orders"]].groupby(["item_type"]).agg("sum").reset_index(drop=False).sort_values(by="requested_orders")

        
    req_orders = df2_filtrado["requested_orders"].sum()
    delta_req_orders = (( df2_filtrado["requested_orders"].sum() - df1_filtrado["requested_orders"].sum() ) / df1_filtrado["requested_orders"].sum())*100
            
    if aggregation_type == "cuisine_type":
        fig2 = px.bar(req_orders_top,  x="requested_orders",y="cuisine_type",orientation='h', title="Top elements")
    else:
        fig2 = px.bar(req_orders_top,  x="requested_orders",y="item_type",orientation='h', title="Top elements")
    
    col13.markdown("<h3>Requested orders</h3>", unsafe_allow_html=True)
    col13.metric("", millify(req_orders, precision=2), delta=str(round(delta_req_orders,2))+"%")
    
    #col7.plotly_chart(fig,use_container_width = True)
    with col15:
        req_orders_radio=st.radio("   ",("By day of the week","By time of the day"), horizontal=True)
        if(req_orders_radio=="By day of the week"):
            req_orders_group1 = df1_filtrado[["date","week","requested_orders"]]
            req_orders_group1 = req_orders_group1.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
            req_orders_group1["date"] = req_orders_group1["date"] + timedelta(days=7)
        
            req_orders_group2 = df2_filtrado[["date","week","requested_orders"]]
            req_orders_group2 = req_orders_group2.groupby(["date", "week"]).agg("sum").reset_index(drop=False)
        
            req_orders_group = pd.concat([req_orders_group1, req_orders_group2], axis=0)
            fig = px.bar(req_orders_group, x="date",y="requested_orders", color="week",barmode = 'group', title='Comparison against previous week')
        else:
            req_orders_group1 = df1_filtrado[["datetime","week","requested_orders"]]
            req_orders_group1 = req_orders_group1.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
            req_orders_group1["datetime"] = req_orders_group1["datetime"] + timedelta(days=7)
        
            req_orders_group2 = df2_filtrado[["datetime","week","requested_orders"]]
            req_orders_group2 = req_orders_group2.groupby(["datetime", "week"]).agg("sum").reset_index(drop=False)
        
            req_orders_group = pd.concat([req_orders_group1, req_orders_group2], axis=0)
            fig = px.bar(req_orders_group, x="datetime",y="requested_orders", color="week",barmode = 'group', title='Comparison against previous week')
        
        st.plotly_chart(fig,use_container_width = True)
    col16.text("")
    col16.text("")
    col16.text("")
    col16.text("")
    col16.text("")
    col16.plotly_chart(fig2,use_container_width = True)     

    by_day = df_final_long[["date","cuisine_type","requested_orders"]]
    by_day = df_final_long.groupby(["date", "cuisine_type"]).agg("sum").reset_index(drop=False)
    fig = px.pie(by_day, names="cuisine_type",values="requested_orders", title="Overall participation")
    st.plotly_chart(fig, use_container_width=False)
