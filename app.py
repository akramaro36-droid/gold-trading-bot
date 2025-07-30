import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from datetime import datetime
import feedparser
import time

# إعداد الواجهة
st.set_page_config(page_title="نظام تداول الذهب الذكي", layout="wide", page_icon="💰")

# تنسيق الصفحة
st.markdown("""
<style>
.header {
    font-size: 24px !important;
    color: #FFD700 !important;
}
.buy-signal {
    background-color: #4CAF50 !important;
    padding: 10px;
    border-radius: 5px;
}
.sell-signal {
    background-color: #F44336 !important;
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<p class="header">نظام التداول الآلي للذهب (XAU/USD)</p>', unsafe_allow_html=True)

# قسم التحليل
def analyze_market():
    with st.spinner("🔄 جاري تحليل بيانات السوق..."):
        try:
            # جلب البيانات
            data = yf.download("GC=F", period="1d", interval="5m")
            
            if not data.empty:
                # حساب المؤشرات
                data["RSI"] = ta.rsi(data["Close"], length=14)
                bb = ta.bbands(data["Close"], length=20, std=2)
                data = pd.concat([data, bb], axis=1)
                
                # تحليل الإشارة
                last = data.iloc[-1]
                signal = None
                if last['RSI'] < 30 and last['Close'] < last['BBL_20_2.0']:
                    signal = "شراء"
                elif last['RSI'] > 70 and last['Close'] > last['BBU_20_2.0']:
                    signal = "بيع"
                
                # عرض النتائج
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("السعر الحالي", f"{last['Close']:.2f} دولار")
                with col2:
                    st.metric("مؤشر RSI", f"{last['RSI']:.2f}")
                with col3:
                    st.metric("النطاق السعري", f"{last['BBL_20_2.0']:.2f} - {last['BBU_20_2.0']:.2f}")
                
                if signal:
                    if signal == "شراء":
                        st.markdown(f'<div class="buy-signal">إشارة {signal} قوية!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="sell-signal">إشارة {signal} تحذيرية!</div>', unsafe_allow_html=True)
                else:
                    st.info("لا توجد إشارة واضحة حالياً")
                
                # رسم بياني مبسط
                st.line_chart(data["Close"].tail(50))
                
            else:
                st.error("⚠️ تعذر جلب بيانات السوق. يرجى المحاولة لاحقاً")
            
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")

# قسم الأخبار
def show_news():
    st.header("📰 آخر الأخبار المؤثرة")
    try:
        news = feedparser.parse("https://news.google.com/rss/search?q=الذهب+OR+forex&hl=ar&gl=AE&ceid=AE:ar")
        for i, entry in enumerate(news.entries[:5], 1):
            st.write(f"{i}. [{entry.title}]({entry.link})")
            st.caption(entry.published)
    except:
        st.warning("تعذر تحميل الأخبار حالياً")

# الزر الرئيسي
if st.button("🔍 تحليل السوق الآن", type="primary"):
    analyze_market()
    show_news()

# التذييل
st.markdown("---")
st.caption("آخر تحديث: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))