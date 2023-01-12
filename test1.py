import streamlit as st
import numpy as np
import pandas as pd
import oura
import datetime
import time
import plotly.graph_objects as go
import pytz
import math
import matplotlib.pyplot as plt


tz = pytz.timezone('UTC')

st.title('概日リズム可視化アプリ')

# 時間取得
import datetime
now = datetime.datetime.now()
dt_now = now.strftime('%Y-%m-%d')
yd = now - datetime.timedelta(days=1)
dt_yd = yd.strftime('%Y-%m-%d')
dby = now - datetime.timedelta(days=2)
dt_dby = dby.strftime('%Y-%m-%d')
days_ago_3 = now - datetime.timedelta(days=3)
dt_days_ago_3 = days_ago_3.strftime('%Y-%m-%d')


#ouraアクセストークン
access_token="QVRKWLEC4P6F7OICXAPUDX5WIVRHANEV"

client = oura.client_pandas.OuraClientDataFrame(personal_access_token=access_token)

#期間を指定（全期間が欲しい場合はこのままでOKです。）
start_text = dt_yd
end_text = dt_now

start_text_yd = dt_dby
end_text_yd = dt_yd
# start_text = '2023-01-04'# 18日の寝た時間19日の朝起きた時間
# end_text = '2023-01-04' # 19日の寝た時間20日の朝起きた時間 こっちはもし19日ならまだjsonデータがない

#Sleepデータをdataframeに格納
data_oura = client.sleep_df(start=start_text, end=end_text)
# data_oura_yd = client.sleep_df(start=start_text_yd, end=end_text_yd)

# datetime Oura
date_start =pd.to_datetime(data_oura['bedtime_start_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')
date_start = date_start.dt.tz_localize(None)
date_end =pd.to_datetime(data_oura['bedtime_end_dt_adjusted'], format='%Y-%m-%d %H:%M:%S')
date_end = date_end.dt.tz_localize(None)
sleep_score = data_oura['score_total'][0]
duration_in_hrs = data_oura['duration_in_hrs'][0]

print(sleep_score)
print(duration_in_hrs)


#COREのデータ取得
df = pd.read_csv('data/CORE_data.csv', sep = ';', header = 1,)
# df = pd.read_csv('data/CORE_data_1219.csv', sep = ';', header = 1,)
data = pd.to_datetime(df.iloc[:,0], format = '%d.%m.%Y %H:%M:%S')

y = df.iloc[:,1]
plot_data = pd.DataFrame(data)
plot_data['Temp'] = y


# COREの前日データ取得
df_yd = pd.read_csv('data/CORE_data_yd.csv', sep = ';', header = 1,)
data_yd = pd.to_datetime(df_yd.iloc[:,0], format = '%d.%m.%Y %H:%M:%S')

y_yd = df_yd.iloc[:,1]
plot_data_yd = pd.DataFrame(data_yd)
plot_data_yd['Temp'] = y_yd
new_datetime_yd = plot_data_yd['DateTime'] + datetime.timedelta(days=1)


# COREの一昨日のデータ
df_dby = pd.read_csv('data/CORE_data_dby.csv', sep = ';', header = 1)
data_dby = pd.to_datetime(df_dby.iloc[:,0], format = '%d.%m.%Y %H:%M:%S')

y_dby = df_dby.iloc[:,1]
plot_data_dby = pd.DataFrame(data_dby)
plot_data_dby['Temp'] = y_dby
new_datetime_dby = plot_data_dby['DateTime'] + datetime.timedelta(days=2)

print(new_datetime_dby)
print(plot_data_dby['Temp'])




# CORE,Ouraプロット
fig = go.Figure()
f1 = go.Scatter(x=plot_data['DateTime'],
                         y=plot_data['Temp'],
                         mode='lines',
                         name='今日の深部体温',
                        )
f2 = go.Scatter(x=new_datetime_yd,
                         y=plot_data_yd['Temp'],
                         mode='lines',
                         name='昨日の深部体温'
                        )

f3 = go.Scatter(x=new_datetime_dby,
                         y=plot_data_dby['Temp'],
                         mode='lines',
                         name='一昨日のの深部体温'
                        )
# 表示グラフ選択
x_choice = st.radio("", ("今日", "昨日","一昨日"), horizontal=True, args=[1, 0])

if x_choice == "今日":
        fig.add_traces((f1))
elif x_choice == "昨日":
        fig.add_traces((f1,f2))
elif x_choice == "一昨日":
        fig.add_traces((f1,f2,f3))


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
        #  range=(y_min, y_max),
        # title='深部体温'
                                    ),
        xaxis=dict(
        # range=(x_min, x_max),
        # title='時間'
                                    
                                    )
                )          
st.subheader('今日の概日リズム')                                                
st.plotly_chart(fig,use_container_width=True) 


# COREの30分前との変化率取得
chang_rate = plot_data['Temp'].pct_change(30, axis=0)
plot_data['diff30m'] = chang_rate
plot_data['diff30m'][plot_data['diff30m']==np.NaN] = 0
df_cr = pd.DataFrame(chang_rate)
df_cr['DateTime'] = data


# DataFrame Get up Change Rate
df_gucr = df_cr.query('Temp > 0.003')
subset_df = df_gucr[df_gucr['DateTime'] > date_start[0] + datetime.timedelta(minutes=30)]
df_getup = subset_df.iloc[1,1]

# DataFrame Fall Asleep Change Rate
df_facr = df_cr.query('Temp < -0.0045')
facr_df = df_facr[df_facr['DateTime'] > date_start[0]]
df_fall_asleep = facr_df.iloc[1,1]

# 睡眠スコア
ss1 = '睡眠スコアは'
ss2 = sleep_score
ss3 = 'でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))

# 睡眠時間

# 小数点切り捨て
n = 1
m = duration_in_hrs
new_duration_in_hrs = math.floor(m * 10 ** n) / (10 ** n)

ss1 = '睡眠時間は'
ss2 = new_duration_in_hrs
ss3 = '時間でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))



# 起床時刻と体温上がり初めの差異
rhythm_delay = df_getup.strftime('%H時%M分%S秒')
a = 'あなたの眠ってから体温が上がり始めた時刻は'
b = 'です'
c = rhythm_delay
st.markdown("{0}{1}{2}".format(a,c,b))
st.caption("深部体温は正常なリズムの場合，入眠と共に低下し，眠っている間は低い状態がキープされ，目覚めに向けて再度上昇していきます．")
st.caption("深部体温が上昇することで体が活動できるように変化していきます．起床するとさらに深部体温が上昇します．深部体温が上昇し始めるよりも先に起床してしまうのは良い目覚めとは言えません．")


# 就寝時刻と体温下がり始めの差異
rhythm_delay_fa = df_fall_asleep - date_start[0]
a = 'あなたの眠ってから体温が下がり始めるまでの時間は'
b = 'です'
c = rhythm_delay_fa
st.markdown("{0}{1}{2}".format(a,c,b))
st.caption("正常なリズムの場合，入眠と共に深部体温は低下していきます．低下しない場合，良い睡眠は得られません．体温の最高値と最低値の差は健康な場合1°C程度です．")

# 変化率のグラフ

# fig_cr = go.Figure()
# fig_cr.add_trace(go.Scatter(x=plot_data['DateTime'],
#                         y=plot_data['diff30m'],
#                         mode='lines',
#                         ))

# fig_cr.update_layout(
#         legend=dict(
#                         x=0.015,
#                         y=0.96,
#                         orientation='h'),
#                         showlegend=True,
#                         margin=dict(
#                         t=0,
#                         b=30,
#                         l=25,
#                         r=0
#                 ),
#         height = 200,
#         # showlegend=True,
#         yaxis=dict(
#         # range=(, y_max),
#         # title='深部体温'
#                                     ),
#         xaxis=dict(
#         # range=(dt_dby, dt_yd),
#         # title='時間'
                                    
#                                     )
#                 )          
# st.subheader('変化率') 
# st.plotly_chart(fig_cr,use_container_width=True) 