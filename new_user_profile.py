import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="BuzzTalent | New Talent Profile", layout="centered")
st.title("📋 New Talent Profile Page")

with st.form("profile_form"):
    st.subheader("👤 Basic Details")
    name = st.text_input("Talent Name")
    city = st.text_input("City")
    photo = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"])

    st.subheader("📧 Manager Info")
    manager_name = st.text_input("Manager Name")
    manager_email = st.text_input("Manager Email")

    st.subheader("🔗 Social Media Handles")
    ig = st.text_input("Instagram")
    yt = st.text_input("YouTube")
    twitter = st.text_input("X / Twitter")

    st.subheader("🏷️ Category & Preferences")
    profession = st.selectbox("Profession", ["Select", "Actor", "Influencer", "Sportsman", "RJ", "Other"])
    preferred_categories = st.multiselect("Preferred Brand Categories", ["Fashion", "Tech", "Wellness", "Finance", "Entertainment"])
    endorsement_fee = st.slider("Expected Endorsement Fee ($)", 500, 20000, (1000, 5000), step=500)
    preferred_brands = st.text_area("Preferred Brands (comma separated)")
    past_brands = st.text_area("Brands Endorsed Before (comma separated)")

    st.subheader("🎯 Category-Specific Fields")
    extra = {}
    if profession == "Sportsman":
        extra["Height"] = st.text_input("Height (in cm)")
        extra["Fitness Level"] = st.selectbox("Fitness Level", ["High", "Moderate", "Low"])
        extra["Languages"] = st.text_input("Languages Known")
        extra["Hobbies"] = st.text_input("Hobbies")
    elif profession == "Actor":
        extra["Languages Comfortable With"] = st.text_input("Languages Comfortable With")
    elif profession == "Influencer":
        extra["Genre"] = st.text_input("Genre / Niche")
        extra["Language Comfort"] = st.text_input("Primary Language")
    elif profession == "RJ":
        extra["Primary Language"] = st.text_input("Primary Language")
        extra["Genre"] = st.text_input("Genre")

    st.subheader("🎨 Profile Customization")
    upload_logo = st.file_uploader("Upload Your Logo (Optional)", type=["jpg", "jpeg", "png"])
    theme_color = st.color_picker("Choose Theme Color", "#00aaff")

    submitted = st.form_submit_button("Save Profile")

    if submitted:
        profile_data = {
            "Talent Name": name,
            "City": city,
            "Manager Name": manager_name,
            "Manager Email": manager_email,
            "Instagram": ig,
            "YouTube": yt,
            "Twitter": twitter,
            "Profession": profession,
            "Preferred Categories": preferred_categories,
            "Endorsement Fee": endorsement_fee,
            "Preferred Brands": preferred_brands,
            "Past Brands": past_brands,
            "Custom Fields": extra,
            "Theme Color": theme_color
        }
        st.success("✅ Profile saved successfully!")
        st.json(profile_data)
        with open("saved_talent_profile.json", "w") as f:
            json.dump(profile_data, f, indent=4)
