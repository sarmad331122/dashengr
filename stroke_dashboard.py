import streamlit as st
import requests
from datetime import datetime
import time

# ========== CONFIG ==========
API_KEY = "9d9d38293c1c436a9e5141950250305"  
CITY = "Vehari"
URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"

# ========== FUNCTIONS ==========
def get_weather():
    try:
        response = requests.get(URL).json()
        temp = response['current']['temp_c']
        humidity = response['current']['humidity']
        condition = response['current']['condition']['text']
        return temp, humidity, condition
    except:
        return None, None, "Error fetching data"

def assess_risk(temp, humidity):
    if temp is None:
        return "Error", "⚠️ ڈیٹا حاصل نہیں ہو سکا"

    if temp > 39 and humidity > 60:
        return (
            "زیادہ",
            """🌡️ شدید گرمی اور نمی کی صورت میں:
- ممکنہ ہیٹ اسٹروک کا خطرہ
- دھوپ میں کام سے گریز کریں
- روزے کی حالت میں پانی کی کمی سے بچیں
- ہلکے کپڑے پہنیں، پانی زیادہ پئیں، اور وقفے لیں
"""
        )
    elif temp > 37:
        return (
            "درمیانہ",
            """☀️ معتدل خطرہ:
- وقفے وقفے سے پانی پئیں
- دھوپ میں کام کم کریں
- سایہ دار یا ہوادار جگہ پر آرام کریں
- بلڈ پریشر یا دل کے مریض خاص احتیاط کریں
"""
        )
    else:
        return (
            "کم",
            """✅ موسم نارمل:
- پانی کا استعمال جاری رکھیں
- سن اسکرین یا ٹوپی استعمال کریں
- دھوپ میں غیر ضروری مشقت سے پرہیز کریں
"""
        )

def risk_color(risk_level):
    colors = {
        "زیادہ": "#ff4d4d",      # Red
        "درمیانہ": "#ffd11a",    # Yellow
        "کم": "#66cc66",         # Green
        "Error": "#999999"       # Grey
    }
    return colors.get(risk_level, "#cccccc")

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="ویہاری اسٹروک رسک", layout="centered")

st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    direction: rtl;
}
.urdu-box {
    border-radius: 15px;
    padding: 20px;
    color: white;
    font-size:18px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌡️ اینگرو فرٹیلائزرز - اسٹروک رسک ڈیش بورڈ")
st.write("📍 موجودہ موسم کی بنیاد پر اسٹروک سے بچاؤ کی معلومات")

temp, humidity, condition = get_weather()
risk, advice = assess_risk(temp, humidity)
color = risk_color(risk)

# ========== METRICS ==========
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ درجہ حرارت", f"{temp}°C" if temp else "N/A")
col2.metric("💧 نمی", f"{humidity}%" if humidity else "N/A")
col3.metric("🌤️ موسم", condition)

# ========== RISK BLOCK ==========
st.markdown(f"""
<div class="urdu-box" style="background-color:{color}">
<b>خطرے کی سطح:</b> {risk}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="urdu-box" style="background-color:#333333">
{advice}
</div>
""", unsafe_allow_html=True)

st.caption(f"⏰ تازہ کاری کا وقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ========== AUTO REFRESH ==========
time.sleep(600)  # 10 minutes
st.experimental_rerun()
