import streamlit as st
import numpy as np

# streamlitのメソッドでmarkdown形式で表示
st.write(
    """
    # My first app
    Hello *world!*
    """
    )

# 適当なデータ作成
data = np.arange(0, 10, 0.1)

# streamlitのメソッドでデータを直線グラフに
st.line_chart(data)