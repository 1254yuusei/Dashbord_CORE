import streamlit as st
import numpy as np
import pandas as pd
import oura
import datetime
import plotly.graph_objects as go
st.title('概日リズム可視化アプリ')

# 時間取得
import datetime
now = datetime.datetime.now()
dt_now = now.strftime('%Y-%m-%d')
yd = now - datetime.timedelta(days=1)
dt_yd = yd.strftime('%Y-%m-%d')
dby = now - datetime.timedelta(days=2)
dt_dby = dby.strftime('%Y-%m-%d')


#ouraアクセストークン
access_token="QVRKWLEC4P6F7OICXAPUDX5WIVRHANEV"

client = oura.client_pandas.OuraClientDataFrame(personal_access_token=access_token)

#期間を指定（全期間が欲しい場合はこのままでOKです。）
start_text = dt_yd
end_text = dt_now

start_text_yd = dt_dby
end_text_yd = dt_yd
# start_text = '2022-11-16'
# end_text = '2022-11-17'

#Sleepデータをdataframeに格納
data_oura = client.sleep_df(start=start_text, end=end_text)
data_oura_yd = client.sleep_df(start=start_text_yd, end=end_text_yd)

# datetime Oura
date_start =pd.to_datetime(data_oura['bedtime_start_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')
date_end =pd.to_datetime(data_oura['bedtime_end_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')

#COREのデータ取得
df = pd.read_csv('data/CORE_data.csv', sep = ';', header = 1,)
data = pd.to_datetime(df.iloc[:,0])
y = df.iloc[:,1]
plot_data = pd.DataFrame(data)
plot_data['Temp'] = y

# COREの前日データ取得
df_yd = pd.read_csv('data/CORE_data_yd.csv', sep = ';', header = 1,)
data_yd = pd.to_datetime(df_yd.iloc[:,0])
y_yd = df_yd.iloc[:,1]
plot_data_yd = pd.DataFrame(data_yd)
plot_data_yd['Temp'] = y_yd

# CORE温度差判定







# CORE,Ouraプロット
fig = go.Figure()
fig.add_trace(go.Scatter(x=plot_data['DateTime'],
                         y=plot_data['Temp'],
                         mode='lines',
                         name='深部体温',
                        ),
                )
fig.add_shape(type="line",
                        x0=data_oura['bedtime_start_dt_adjusted'][0], y0=36,
                        x1=data_oura['bedtime_start_dt_adjusted'][0], y1=38,
                        line=dict(color="Red",width=3)
                )
fig.add_shape(type="line",
                        x0=data_oura['bedtime_end_dt_adjusted'][0], y0=36,
                        x1=data_oura['bedtime_end_dt_adjusted'][0], y1=38,
                        line=dict(color="Red",width=3)
                )

fig.update_layout(
        legend=dict(
                        x=0.015,
                        y=0.96,
                        orientation='h'),
                        showlegend=True,
                        margin=dict(
                        t=0,
                        b=30,
                        l=25,
                        r=0
                ),
        height = 200,
        # showlegend=True,
        yaxis=dict(
         # range=(y_min, y_max),
        # title='深部体温'
                                    ),
        xaxis=dict(
        # range=(x_min, x_max),
        # title='時間'
                                    
                                    )
                )          
st.subheader('今日の概日リズム')                                                
st.plotly_chart(fig,use_container_width=True) 



# CORE,Ouraプロット
fig_yd = go.Figure()
fig_yd.add_trace(go.Scatter(x=plot_data_yd['DateTime'],
                         y=plot_data_yd['Temp'],
                         mode='lines',
                         name='深部体温',
                        ),
                )
fig_yd.add_shape(type="line",
                        x0=data_oura_yd['bedtime_start_dt_adjusted'][0], y0=36,
                        x1=data_oura_yd['bedtime_start_dt_adjusted'][0], y1=38,
                        line=dict(color="Red",width=3)
                )
fig_yd.add_shape(type="line",
                        x0=data_oura_yd['bedtime_end_dt_adjusted'][0], y0=36,
                        x1=data_oura_yd['bedtime_end_dt_adjusted'][0], y1=38,
                        line=dict(color="Red",width=3)
                )

fig_yd.update_layout(
        legend=dict(
                        x=0.015,
                        y=0.96,
                        orientation='h'),
                        showlegend=True,
                        margin=dict(
                        t=0,
                        b=30,
                        l=25,
                        r=0
                ),
        height = 200,
        # showlegend=True,
        yaxis=dict(
         # range=(y_min, y_max),
        # title='深部体温'
                                    ),
        xaxis=dict(
        # range=(x_min, x_max),
        # title='時間'
                                    
                                    )
                )          
st.subheader('昨日の概日リズム')                           
st.plotly_chart(fig_yd,use_container_width=True) 
