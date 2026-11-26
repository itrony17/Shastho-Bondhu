import streamlit as st
from offline_sync_engine import (
    preprocess_prescription_image,
    analyze_prescription,
    is_ollama_running,
)
from hospital_fetcher import (
    get_divisions,
    get_districts,
    get_hospitals_by_district,
    search_hospitals,
)
from reminder_helper import (
    build_medicine_schedule,
    generate_ics_calendar,
)
from diet_helper import (
    build_multi_disease_diet,
    generate_diet_pdf,
)

st.set_page_config(
    page_title="স্বাস্থ্যবন্ধু AI | Shasthobondhu AI",
    page_icon="🩺",
    layout="wide",
)

with st.sidebar:
    st.title("🩺 স্বাস্থ্যবন্ধু AI")
    st.caption("১০০% ফ্রি ও স্মার্ট ডিজিটাল স্বাস্থ্য সহায়ক")
    st.divider()

    st.subheader("⚙️ AI স্ট্যাটাস")
    if is_ollama_running():
        st.success("🟢 Cloud Vision AI সক্রিয়")
    else:
        st.warning("🟠 AI API Key সেট করা নেই")

    st.divider()
    st.error(
        "🚨 **জরুরি স্বাস্থ্য সেবা (২৪/৭):**\n"
        "- জাতীয় জরুরি সেবা: **999**\n"
        "- স্বাস্থ্য বাতায়ন: **16263**"
    )

st.title("🩺 স্বাস্থ্যবন্ধু AI (Shasthobondhu AI)")
st.markdown("প্রেসক্রিপশন থেকে ওষুধের নাম ও কাজ জানা, ডায়েট চার্ট এবং ৬৪ জেলার সরকারি হাসপাতালের তথ্য।")

tab1, tab2, tab3 = st.tabs([
    "📄 প্রেসক্রিপশন স্ক্যানার",
    "🥗 ডায়েট চার্ট তৈরি",
    "🏥 ৬৪ জেলার হাসপাতাল",
])

# ==========================================
# TAB 1: PRESCRIPTION SCANNER
# ==========================================
with tab1:
    st.subheader("প্রেসক্রিপশনের ছবি আপলোড করুন")
    uploaded_file = st.file_uploader(
        "স্পষ্ট প্রেসক্রিপশনের ছবি নির্বাচন করুন (JPG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded_file is not None:
        col_img, col_res = st.columns([1, 1.4])
        with col_img:
            st.image(uploaded_file, caption="আপলোডকৃত প্রেসক্রিপশন", width="stretch")

        with col_res:
            if st.button("🔍 প্রেসক্রিপশন বিশ্লেষণ করুন", type="primary", width="stretch"):
                with st.spinner("প্রেসক্রিপশন থেকে ওষুধের নাম ও কাজ পড়া হচ্ছে..."):
                    try:
                        img_bytes = preprocess_prescription_image(uploaded_file)
                        result, engine_used = analyze_prescription(img_bytes)
                        st.session_state["rx_result"] = result
                        st.session_state["rx_engine"] = engine_used
                    except Exception as e:
                        st.error(f"বিশ্লেষণে সমস্যা হয়েছে: {e}")

            if "rx_result" in st.session_state:
                data = st.session_state["rx_result"]
                st.caption(f"মডেল: **{st.session_state.get('rx_engine', '')}**")

                with st.container(border=True):
                    st.markdown(f"### 👨‍⚕️ {data.get('doctor_name', 'ডাক্তারের তথ্য')}")
                    st.write(f"**ডিগ্রি/পদবি:** {data.get('doctor_degree', 'উল্লেখ নেই')}")
                    st.write(f"**চেম্বার/হাসপাতাল:** {data.get('chamber_address', 'উল্লেখ নেই')}")
                    if data.get("diagnosis"):
                        st.write(f"**সম্ভাব্য রোগ:** {data.get('diagnosis')}")

                st.markdown("### 💊 ওষুধের তালিকা ও কার্যকারিতা")
                medicines = data.get("medicines", [])
                if medicines:
                    for idx, med in enumerate(medicines, 1):
                        with st.container(border=True):
                            st.markdown(f"**{idx}. {med.get('name', 'অজানা ওষুধ')}**")
                            st.write(f"🔹 **কী কাজে লাগে:** {med.get('usage', 'উল্লেখ নেই')}")
                            st.write(f"⏰ **খাবার নিয়ম:** {med.get('dosage', 'চিকিৎসকের পরামর্শ অনুযায়ী')}")

                    st.markdown("### ⏰ দৈনিক ওষুধের রিমাইন্ডার সূচি")
                    schedule = build_medicine_schedule(medicines)
                    for item in schedule:
                        with st.container(border=True):
                            st.markdown(f"**💊 {item['medicine']}**")
                            st.write(f"🕒 **সময়:** {item['reminder_times']} | 🍽️ **{item['meal_timing']}**")

                    reminder_days = st.slider("কত দিনের জন্য ফোনে রিমাইন্ডার অ্যালার্ম সেট করবেন?", 1, 30, 7)
                    ics_data = generate_ics_calendar(medicines, days=reminder_days)
                    st.download_button(
                        label="📅 মোবাইলে অ্যালার্ম সেট করতে ক্যালেন্ডার ফাইল (.ics) ডাউনলোড করুন",
                        data=ics_data,
                        file_name="shasthobondhu_medicine_reminder.ics",
                        mime="text/calendar",
                        width="stretch",
                    )
                else:
                    st.warning("ছবি থেকে ওষুধের নাম স্পষ্টভাবে পড়া যায়নি। অনুগ্রহ করে আরও কাছ থেকে পরিষ্কার ছবি আপলোড করুন।")

                if data.get("summary"):
                    st.info(f"**সহজ সারাংশ:** {data['summary']}")

                st.warning("⚠️ সতর্কতা: এটি কেবল তথ্যগত সহায়তার জন্য। যেকোনো ওষুধ সেবনের আগে নিবন্ধিত চিকিৎসকের পরামর্শ নিন।")
# ==========================================
# TAB 2: DIET CHART GENERATOR (FEET/INCH + MULTI-DISEASE + PDF)
# ==========================================
with tab2:
    st.subheader("🥗 ব্যক্তিগত বাংলাদেশি ডায়েট চার্ট ও PDF রিপোর্ট")
    with st.form("diet_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            p_name = st.text_input("রোগীর নাম (ইংরেজি বা বাংলায়)", value="Rahim Uddin")
            p_age = st.number_input("বয়স (বছর)", min_value=1, max_value=120, value=42)
        with c2:
            p_gender = st.selectbox("লিঙ্গ", ["পুরুষ", "মহিলা"])
            p_weight = st.number_input("ওজন (কেজি)", min_value=10.0, max_value=250.0, value=72.0)
        with c3:
            h_col1, h_col2 = st.columns(2)
            with h_col1:
                p_feet = st.number_input("উচ্চতা (Feet)", min_value=1, max_value=8, value=5)
            with h_col2:
                p_inch = st.number_input("ইঞ্চি (Inch)", min_value=0, max_value=11, value=6)
            extra_note = st.text_input("অতিরিক্ত কোনো তথ্য (ঐচ্ছিক)", placeholder="যেমন: গর্ভবতী, অ্যালার্জি ইত্যাদি")

        st.markdown("**🩺 রোগ নির্বাচন করুন (একাধিক রোগে টিক চিহ্ন দিতে পারেন):**")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            chk_dm = st.checkbox("ডায়াবেটিস (Diabetes)", value=True)
            chk_bp = st.checkbox("উচ্চ রক্তচাপ (High BP)", value=True)
            chk_gastric = st.checkbox("গ্যাস্ট্রিক / আলসার (Gastric/GERD)")
        with d_col2:
            chk_kidney = st.checkbox("কিডনি সমস্যা (Kidney Disease)")
            chk_lipid = st.checkbox("ফ্যাটি লিভার / কোলেস্টেরল (Fatty Liver/Cholesterol)")
        with d_col3:
            chk_thyroid = st.checkbox("থাইরয়েড (Thyroid)")
            chk_heart = st.checkbox("হৃদরোগ (Heart Disease)")

        submitted = st.form_submit_button("📋 ডায়েট চার্ট ও PDF তৈরি করুন", type="primary", width="stretch")

    if submitted:
        selected_diseases = []
        if chk_dm:
            selected_diseases.append("ডায়াবেটিস (Diabetes)")
        if chk_bp:
            selected_diseases.append("উচ্চ রক্তচাপ (High BP)")
        if chk_gastric:
            selected_diseases.append("গ্যাস্ট্রিক / আলসার (Gastric/GERD)")
        if chk_kidney:
            selected_diseases.append("কিডনি সমস্যা (Kidney Disease)")
        if chk_lipid:
            selected_diseases.append("ফ্যাটি লিভার / কোলেস্টেরল (Fatty Liver/Cholesterol)")
        if chk_thyroid:
            selected_diseases.append("থাইরয়েড (Thyroid)")
        if chk_heart:
            selected_diseases.append("হৃদরোগ (Heart Disease)")

        metrics, diet_data = build_multi_disease_diet(
            name=p_name,
            age=p_age,
            gender=p_gender,
            weight_kg=p_weight,
            feet=int(p_feet),
            inches=int(p_inch),
            diseases=selected_diseases,
            extra_notes=extra_note,
        )
        pdf_bytes = generate_diet_pdf(
            patient_name=p_name,
            age=int(p_age),
            gender=p_gender,
            weight_kg=float(p_weight),
            metrics=metrics,
            diet=diet_data,
        )
        st.session_state["diet_metrics"] = metrics
        st.session_state["diet_result"] = diet_data
        st.session_state["diet_pdf"] = pdf_bytes
        st.session_state["diet_patient_name"] = p_name

    if "diet_result" in st.session_state:
        d = st.session_state["diet_result"]
        m = st.session_state["diet_metrics"]
        patient_name = st.session_state.get("diet_patient_name", "Patient")

        st.success(
            f"**উচ্চতা:** {m['height_str']} | **BMI:** {m['bmi']} ({m['bmi_cat']}) | "
            f"**নির্বাচিত রোগ:** {m['diseases_str']}"
        )
        st.info(f"**দৈনিক পুষ্টি লক্ষ্য:** {d.get('daily_calorie_target', '')}")

        m1, m2 = st.columns(2)
        with m1:
            with st.container(border=True):
                st.markdown("#### 🌅 ভোরে (খালি পেটে)")
                st.write(d.get("early_morning", "-"))
            with st.container(border=True):
                st.markdown("#### 🍳 সকালের নাস্তা")
                st.write(d.get("breakfast", "-"))
            with st.container(border=True):
                st.markdown("#### 🍎 সকাল ১১টার নাস্তা")
                st.write(d.get("mid_morning_snack", "-"))
        with m2:
            with st.container(border=True):
                st.markdown("#### 🍛 দুপুরের খাবার")
                st.write(d.get("lunch", "-"))
            with st.container(border=True):
                st.markdown("#### ☕ বিকালের নাস্তা")
                st.write(d.get("evening_snack", "-"))
            with st.container(border=True):
                st.markdown("#### 🍽️ রাতের খাবার")
                st.write(d.get("dinner", "-"))

        col_avoid, col_adv = st.columns(2)
        with col_avoid:
            with st.container(border=True):
                st.markdown("#### 🚫 যেসব খাবার বর্জন করবেন")
                for food in d.get("foods_to_avoid", []):
                    st.write(f"❌ {food}")
        with col_adv:
            with st.container(border=True):
                st.markdown("#### 💡 বিশেষ পরামর্শ")
                st.write(d.get("special_advice", "-"))

        if "diet_pdf" in st.session_state:
            safe_file = "".join(c if c.isalnum() else "_" for c in patient_name) or "Patient"
            st.download_button(
                label="📄 সুন্দর PDF ফরম্যাটে ডায়েট চার্ট ডাউনলোড করুন (.pdf)",
                data=st.session_state["diet_pdf"],
                file_name=f"Shasthobondhu_Diet_{safe_file}.pdf",
                mime="application/pdf",
                type="primary",
                width="stretch",
            )

# ==========================================
# TAB 3: 64 DISTRICT HOSPITAL FINDER
# ==========================================
with tab3:
    st.subheader("🏥 বাংলাদেশের ৬৪ জেলার সরকারি ও মেডিকেল কলেজ হাসপাতাল")

    search_query = st.text_input("🔎 সরাসরি জেলা বা হাসপাতালের নাম লিখে খুঁজুন (যেমন: Dhaka, Bogura, Sylhet, Cumilla)")

    if search_query.strip():
        matches = search_hospitals(search_query)
        st.write(f"**'{search_query}'** এর জন্য **{len(matches)}টি** হাসপাতাল পাওয়া গেছে:")
        for h in matches:
            with st.container(border=True):
                c_info, c_btn = st.columns((3, 1))
                with c_info:
                    st.markdown(f"### {h['name']}")
                    st.write(f"📍 **জেলা:** {h['district']} | **ধরন:** {h['type']}")
                    st.write(f"🏠 **ঠিকানা:** {h['address']} | 📞 **ফোন:** `{h['phone']}`")
                with c_btn:
                    st.link_button("🗺️ Google Maps", h["maps_url"], width="stretch")
    else:
        col_div, col_dist = st.columns(2)
        with col_div:
            selected_div = st.selectbox("বিভাগ নির্বাচন করুন", get_divisions())
        with col_dist:
            selected_dist = st.selectbox("জেলা নির্বাচন করুন", get_districts(selected_div))

        hospitals = get_hospitals_by_district(selected_div, selected_dist)
        st.markdown(f"### {selected_dist} জেলার প্রধান হাসপাতালসমূহ ({len(hospitals)}টি)")
        for h in hospitals:
            with st.container(border=True):
                c_info, c_btn = st.columns((3, 1))
                with c_info:
                    st.markdown(f"#### 🏥 {h['name']}")
                    st.write(f"**ধরন:** {h['type']} | **ঠিকানা:** {h['address']}")
                    st.write(f"📞 **জরুরি যোগাযোগ:** `{h['phone']}`")
                with c_btn:
                    st.link_button("🗺️ ম্যাপে দেখুন", h["maps_url"], width="stretch")
