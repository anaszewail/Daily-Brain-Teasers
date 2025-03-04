import streamlit as st
import random
from datetime import date
import requests

# بيانات PayPal Sandbox
PAYPAL_CLIENT_ID = "AQd5IZObL6YTejqYpN0LxADLMtqbeal1ahbgNNrDfFLcKzMl6goF9BihgMw2tYnb4suhUfprhI-Z8eoC"
PAYPAL_SECRET = "EPk46EBw3Xm2W-R0Uua8sLsoDLJytgSXqIzYLbbXCk_zSOkdzFx8jEbKbKxhjf07cnJId8gt6INzm6_V"
PAYPAL_API = "https://api-m.sandbox.paypal.com"

# قائمة ألغاز بسيطة وممتعة
teasers = [
    {"riddle": "What has keys but can’t open locks?", "answer": "A piano!"},
    {"riddle": "I’m tall when I’m young, and short when I’m old. What am I?", "answer": "A candle!"},
    {"riddle": "What can run but never walks?", "answer": "Water!"},
    {"riddle": "What has a head, a tail, but no body?", "answer": "A coin!"},
    {"riddle": "What gets wetter the more it dries?", "answer": "A towel!"},
    {"riddle": "What has one eye but can’t see?", "answer": "A needle!"},
    {"riddle": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "The letter M!"}
]

# لغز مجاني ثابت كمعاينة
free_teaser = {"riddle": "What has hands but can’t clap?", "answer": "A clock!"}

# واجهة جذابة
st.title("Daily Brain Teasers")
st.write("Get a free teaser below, but subscribe for just $1/month to unlock daily riddles and answers!")

# عرض اللغز المجاني
st.subheader("Free Teaser of the Day")
st.write(f"Riddle: {free_teaser['riddle']}")
st.info("Want the answer? Subscribe to unlock it and get a new teaser every day!")

# الحصول على رمز الوصول من PayPal
def get_paypal_token():
    url = f"{PAYPAL_API}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET), data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

# حالة الاشتراك
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# التحقق من الاشتراك
if not st.session_state.subscribed:
    st.warning("🧠 Daily teasers and answers are exclusive to members! Subscribe now.")
    st.info("Join for only $1/month – just 3 cents a day for brain-busting fun!")
    if st.button("Subscribe Now for $1/month"):
        token = get_paypal_token()
        if token:
            st.session_state.subscribed = True
            st.success("Payment successful! Welcome to Daily Brain Teasers!")
            st.balloons()
        else:
            st.error("Payment failed. Try again!")
    st.markdown("[Pay $1/month via PayPal Sandbox](https://www.sandbox.paypal.com) - Use a test account to subscribe!")
else:
    # عرض اللغز المجاني مع الإجابة للمشتركين
    st.subheader("Your Free Teaser (with Answer)")
    st.write(f"Riddle: {free_teaser['riddle']}")
    st.write(f"Answer: {free_teaser['answer']}")

    # عرض اللغز اليومي الإضافي للمشتركين
    today = date.today().day
    teaser_index = today % len(teasers)
    daily_teaser = teasers[teaser_index]
    st.success(f"Your Daily Brain Teaser: {daily_teaser['riddle']}")
    
    # زر لعرض الإجابة
    if st.button("Show Answer"):
        st.write(f"Answer: {daily_teaser['answer']}")
        st.warning("🧩 Solved it? Come back tomorrow for a new one!")
    
    # روابط المشاركة
    share_text = f"Here’s a brain teaser from Daily Brain Teasers: {daily_teaser['riddle']} - Join at yourapp.streamlit.app!"
    whatsapp_link = f"https://wa.me/?text={share_text}"
    telegram_link = f"https://t.me/share/url?url=yourapp.streamlit.app&text={share_text}"
    twitter_link = f"https://twitter.com/intent/tweet?text={share_text}"
    
    st.subheader("Share the Fun!")
    st.markdown(f"[Share on WhatsApp]({whatsapp_link}) | [Share on Telegram]({telegram_link}) | [Share on Twitter]({twitter_link})")
    st.info("🎉 You’re a teaser master! Invite friends to join the challenge!")

# تنبيه إضافي
if st.session_state.subscribed:
    st.info("🌟 VIP Member Alert: Enjoy your exclusive daily teaser and more!")
