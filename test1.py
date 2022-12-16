import streamlit as st
import numpy as np
import pandas as pd
import oura
import datetime
import plotly.graph_objects as go
st.title('概日リズム可視化アプリ')

# 時間取得
dt_now = datetime.datetime.now()
dt_yd = dt_now - datetime.timedelta(days=1)


#ouraアクセストークン
access_token="QVRKWLEC4P6F7OICXAPUDX5WIVRHANEV"

client = oura.client_pandas.OuraClientDataFrame(personal_access_token=access_token)

#期間を指定（全期間が欲しい場合はこのままでOKです。）
start_text="2022-11-16"
end_text="2022-11-17"

#上からそれぞれ、Sleepデータ、Activityデータ、Readinessデータをdataframeに格納しています。
data_oura=client.sleep_df(start=start_text, end=end_text)

# datetime Oura
date_start =pd.to_datetime(data_oura['bedtime_start_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')
date_end =pd.to_datetime(data_oura['bedtime_end_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')

#COREのデータ取得
df = pd.read_csv('data/CORE_TEMP_1117.csv', sep = ';', header = 1,)
data = pd.to_datetime(df.iloc[:,0])
y = df.iloc[:,1]
plot_data = pd.DataFrame(data)
plot_data['Temp'] = y


# CORE,Ouraプロット
fig = go.Figure()
fig.add_trace(go.Scatter(x=plot_data['DateTime'],
                         y=plot_data['Temp'],
                         mode='lines',
                         name='深部体温',
                        ),
                )
fig.add_shape(type="line",
                        x0=data_oura['bedtime_start_dt_adjusted'][0], y0=35,
                        x1=data_oura['bedtime_start_dt_adjusted'][0], y1=40,
                        line=dict(color="Red",width=3)
                )
fig.add_shape(type="line",
                        x0=data_oura['bedtime_end_dt_adjusted'][0], y0=35,
                        x1=data_oura['bedtime_end_dt_adjusted'][0], y1=40,
                        line=dict(color="Red",width=3)
                )

fig.update_layout(
                        # showlegend=True,
                        yaxis=dict(
                                    # range=(y_min, y_max),
                                    title='Oura'
                                    ),
                        xaxis=dict(
                                    # range=(x_min, x_max),
                                    title='時間'
                                    
                                    )
                )                                          
st.plotly_chart(fig, use_container_width=True) 