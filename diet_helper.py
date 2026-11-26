import io
from fpdf import FPDF


def feet_inch_to_cm(feet: int, inches: int) -> float:
    """Converts Feet and Inches to centimeters."""
    total_inches = (feet * 12) + inches
    return round(total_inches * 2.54, 1)


def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    """Calculates BMI and returns (bmi_value, bengali_category)."""
    if height_cm <= 0:
        return 22.0, "স্বাভাবিক ওজন (Normal)"
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m * height_m), 1)
    if bmi < 18.5:
        cat = "ওজন কম (Underweight)"
    elif bmi < 25.0:
        cat = "স্বাভাবিক ওজন (Normal)"
    elif bmi < 30.0:
        cat = "অতিরিক্ত ওজন (Overweight)"
    else:
        cat = "স্থূলতা (Obese)"
    return bmi, cat


def build_multi_disease_diet(
    name: str,
    age: int,
    gender: str,
    weight_kg: float,
    feet: int,
    inches: int,
    diseases: list[str],
    extra_notes: str = "",
) -> tuple[dict, dict]:
    """
    Generates a clinical Bangladeshi diet chart tailored to multiple selected diseases,
    BMI, and height in Feet/Inches.
    """
    height_cm = feet_inch_to_cm(feet, inches)
    bmi, bmi_cat = calculate_bmi(weight_kg, height_cm)

    base_kcal = 1900 if gender == "পুরুষ" else 1650
    if bmi >= 25.0:
        base_kcal -= 300
    elif bmi < 18.5:
        base_kcal += 300
    if age > 55:
        base_kcal -= 150

    d_set = set(diseases)
    has_dm = "ডায়াবেটিস (Diabetes)" in d_set
    has_bp = "উচ্চ রক্তচাপ (High BP)" in d_set
    has_gastric = "গ্যাস্ট্রিক / আলসার (Gastric/GERD)" in d_set
    has_kidney = "কিডনি সমস্যা (Kidney Disease)" in d_set
    has_lipid = "ফ্যাটি লিভার / কোলেস্টেরল (Fatty Liver/Cholesterol)" in d_set
    has_thyroid = "থাইরয়েড (Thyroid)" in d_set
    has_heart = "হৃদরোগ (Heart Disease)" in d_set

    water_liters = "১.৫ - ২.০ লিটার (চিকিৎসকের পরামর্শ অনুযায়ী মেপে)" if has_kidney else "২.৫ - ৩.০ লিটার (৮-১০ গ্লাস)"

    early_morning = "১ গ্লাস কুসুম গরম পানি ও ১ চা চামচ ভেজানো চিয়া সিড বা মেথি"
    breakfast = "২টি লাল আটার রুটি, ১ বাটি সবজি ভাজি (কম তেলে) ও ১টি সিদ্ধ ডিম"
    mid_morning = "১টি মৌসুমি ফল (পেয়ারা, আপেল বা আমলকী) অথবা ১ কাপ গ্রিন টি"
    lunch = "১.৫ কাপ ভাত (লাল চাল হলে ভালো), ১ টুকরো মাছ বা মুরগি, ১ বাটি পাতলা ডাল ও শাকসবজি"
    evening_snack = "১ মুঠো ভাজা ছোলা বা মুড়ি (তেল-চানাচুর ছাড়া) এবং চিনি ছাড়া লাল চা"
    dinner = "২টি লাল আটার রুটি, ১ বাটি সবজি ও ১ টুকরো মাছ বা ডাল (ঘুমানোর ২ ঘণ্টা আগে)"

    avoid = ["অতিরিক্ত তেল-চর্বিযুক্ত ভাজাপোড়া ও ফাস্টফুড", "কোমল পানীয় ও প্যাকেটজাত জুস"]
    advice_notes = ["প্রতিদিন অন্তত ৩০ মিনিট হালকা ব্যায়াম বা হাঁটাহাঁটি করুন এবং পর্যাপ্ত ঘুমান।"]

    if has_dm:
        breakfast = "২টি পাতলা লাল আটার রুটি, সবজি ভাজি ও ১টি সিদ্ধ ডিমের সাদা অংশ"
        mid_morning = "১টি কম মিষ্টি ফল (পেয়ারা, জাম্বুরা বা সবুজ আপেল)"
        lunch = "১ কাপ লাল চালের ভাত, ১ টুকরো মাছ, পাতলা ডাল ও প্রচুর সবুজ শাকসবজি"
        avoid.extend(["চিনি, মিষ্টি, গুড়, পায়েস ও মিষ্টি পানীয়", "অতিরিক্ত সাদা ভাত, আলু ও পাকা আম-কলা"])
        advice_notes.append("ডায়াবেটিস নিয়ন্ত্রণে প্রতি ২-৩ ঘণ্টা পরপর অল্প পরিমাণে খাবার খান; একসাথে পেট ভরে খাবেন না।")

    if has_bp or has_heart:
        avoid.extend(["খাবারে কাঁচা লবণ (আলগা লবণ) ও সস", "আচার, চানাচুর, নোনা ইলিশ ও প্রক্রিয়াজাত খাবার"])
        advice_notes.append("উচ্চ রক্তচাপ ও হার্ট ভালো রাখতে রান্নায় লবণ ও তেলের পরিমাণ অর্ধেকে নামিয়ে আনুন।")

    if has_gastric:
        early_morning = "১ গ্লাস স্বাভাবিক বা হালকা কুসুম গরম পানি (খালি পেটে চা/কফি বর্জনীয়)"
        evening_snack = "২-৩টি নোনতা বিস্কুট বা শুকনো মুড়ি এবং হালকা আদা চা"
        avoid.extend(["অতিরিক্ত ঝাল-মসলাযুক্ত খাবার, ভাজাপোড়া ও টক ফল", "খালি পেটে চা-কফি এবং রাত জাগা"])
        advice_notes.append("খাবার খাওয়ার পরপরই শুয়ে পড়বেন না; অন্তত ১.৫-২ ঘণ্টা পর ঘুমাতে যান।")

    if has_kidney:
        lunch = "১ কাপ ভাত, পরিমিত প্রোটিন (১ ছোট টুকরো মাছ বা ডিমের সাদা অংশ) ও কম পটাশিয়ামযুক্ত সবজি (পটল, ঝিঙা, লাউ)"
        dinner = "২টি রুটি, লাউ/পটল/পেঁপের তরকারি (ডাল ও অতিরিক্ত মাছ-মাংস সীমিত)"
        avoid.extend(["অতিরিক্ত ডাল, বাদাম, বিচি জাতীয় খাবার ও লাল মাংস (গরু/খাসি)", "ডাবের পানি, কলা, টমেটো ও পালং শাক (উচ্চ পটাশিয়ামযুক্ত খাবার)"])
        advice_notes.append("কিডনির সুরক্ষায় প্রোটিন ও পানি অবশ্যই নেফ্রোলজিস্টের নির্ধারিত মাপ অনুযায়ী গ্রহণ করুন।")

    if has_lipid or has_heart:
        breakfast = "২টি লাল আটার রুটি, তেলছাড়া সবজি ও ১টি সিদ্ধ ডিমের সাদা অংশ (কুসুম বাদে)"
        avoid.extend(["গরু-খাসির মাংস, মগজ, কলিজা, চিংড়ি ও ডিমের কুসুম", "ঘি, মাখন, ডালডা ও নারকেল দুধ"])
        advice_notes.append("ওমেগা-৩ সমৃদ্ধ সামুদ্রিক মাছ বা দেশি ছোট মাছ খান এবং রান্নায় অলিভ অয়েল বা সরিষার তেল অল্প ব্যবহার করুন।")

    if has_thyroid:
        avoid.extend(["অতিরিক্ত বাঁধাকপি, ফুলকপি ও সয়াবিন জাতীয় খাবার কাঁচা খাওয়া", "অতিরিক্ত প্রক্রিয়াজাত চিনি ও ময়দার খাবার"])
        advice_notes.append("থাইরয়েডের ওষুধ সকালে খালি পেটে খাওয়ার অন্তত ৩০-৪৫ মিনিট পর সকালের নাস্তা করবেন।")

    if extra_notes.strip():
        advice_notes.append(f"রোগীর বিশেষ নোট: {extra_notes.strip()}")

    metrics = {
        "bmi": bmi,
        "bmi_cat": bmi_cat,
        "height_str": f"{feet} ফুট {inches} ইঞ্চি ({height_cm} সেমি)",
        "estimated_kcal": base_kcal,
        "water_liters": water_liters,
        "diseases_str": ", ".join(diseases) if diseases else "সাধারণ স্বাস্থ্য সুরক্ষা",
    }

    diet_plan = {
        "daily_calorie_target": f"{base_kcal - 100} - {base_kcal + 100} ক্যালরি | পানি: {water_liters}",
        "early_morning": early_morning,
        "breakfast": breakfast,
        "mid_morning_snack": mid_morning,
        "lunch": lunch,
        "evening_snack": evening_snack,
        "dinner": dinner,
        "foods_to_avoid": list(dict.fromkeys(avoid)),
        "special_advice": " ".join(advice_notes),
    }
    return metrics, diet_plan

import os
from datetime import datetime


def _find_nikosh_font() -> str:
    """Finds Nikosh Unicode font inside the 'font/' directory (or root folder)."""
    search_dirs = ("font", "fonts", ".")
    preferred_names = (
        "Nikosh.ttf",
        "nikosh.ttf",
        "NikoshBAN.ttf",
        "nikoshban.ttf",
        "NikoshGrameen.ttf",
    )
    for folder in search_dirs:
        if not os.path.isdir(folder):
            continue
        for fname in preferred_names:
            full_path = os.path.join(folder, fname)
            if os.path.exists(full_path):
                return full_path
        for f in os.listdir(folder):
            if "nikosh" in f.lower() and f.lower().endswith(".ttf"):
                return os.path.join(folder, f)
    return ""


def generate_diet_pdf(
    patient_name: str,
    age: int,
    gender: str,
    weight_kg: float,
    metrics: dict,
    diet: dict,
) -> bytes:
    """
    Generates a Bengali Unicode PDF diet chart using Nikosh font from the main folder
    and automatically saves it inside the 'report/' directory.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    font_path = _find_nikosh_font()
    has_bn_font = bool(font_path)

    if has_bn_font:
        pdf.add_font("Nikosh", style="", fname=font_path)
        pdf.set_text_shaping(use_shaping_engine=True)
        font_family = "Nikosh"
    else:
        font_family = "Helvetica"

    # Header Banner
    pdf.set_fill_color(13, 110, 110)
    pdf.rect(0, 0, 210, 32, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font(font_family, "", 18)
    pdf.set_xy(12, 8)
    title_txt = "স্বাস্থ্যবন্ধু AI - ব্যক্তিগত বাংলাদেশি ডায়েট চার্ট" if has_bn_font else "SHASTHOBONDHU AI - DIET PLAN"
    pdf.cell(0, 8, title_txt, ln=True)

    pdf.set_font(font_family, "", 10.5)
    pdf.set_x(12)
    sub_txt = "রোগীর শারীরিক অবস্থা ও নির্বাচিত রোগ অনুযায়ী সুষম খাদ্যতালিকা" if has_bn_font else "Personalized Meal Chart"
    pdf.cell(0, 6, sub_txt, ln=True)

    # Patient Summary Box
    pdf.set_text_color(30, 30, 30)
    pdf.set_xy(12, 38)
    pdf.set_fill_color(240, 248, 248)
    pdf.set_draw_color(180, 210, 210)
    pdf.rect(12, 38, 186, 32, "DF")

    if has_bn_font:
        pdf.set_font(font_family, "", 11.5)
        pdf.set_xy(16, 41)
        pdf.cell(95, 6, f"রোগীর নাম: {patient_name} ({age} বছর, {gender})")
        pdf.cell(85, 6, f"ওজন: {weight_kg} কেজি | উচ্চতা: {metrics['height_str']}", ln=True)

        pdf.set_font(font_family, "", 10.5)
        pdf.set_x(16)
        pdf.cell(95, 6, f"BMI: {metrics['bmi']} ({metrics['bmi_cat']})")
        pdf.cell(85, 6, f"দৈনিক ক্যালরি: ~{metrics['estimated_kcal']} kcal", ln=True)

        pdf.set_text_color(160, 30, 30)
        pdf.set_x(16)
        pdf.multi_cell(178, 6, f"নির্বাচিত রোগ: {metrics['diseases_str']}")
    else:
        safe_name = patient_name.encode("latin-1", "ignore").decode("latin-1").strip() or "Patient"
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(16, 41)
        pdf.cell(0, 6, f"Patient: {safe_name} ({age} yrs) | Weight: {weight_kg} kg | BMI: {metrics['bmi']}", ln=True)

    # Meal Schedule Section
    pdf.set_xy(12, 75)
    pdf.set_text_color(13, 110, 110)
    pdf.set_font(font_family, "", 13.5)
    sec_title = "দৈনিক খাবারের সময়সূচি ও তালিকা" if has_bn_font else "Daily Meal Schedule"
    pdf.cell(0, 8, sec_title, ln=True)

    meals_bn = (
        ("ভোরে (খালি পেটে)", diet.get("early_morning", "-")),
        ("সকালের নাস্তা", diet.get("breakfast", "-")),
        ("সকাল ১১টার নাস্তা", diet.get("mid_morning_snack", "-")),
        ("দুপুরের খাবার", diet.get("lunch", "-")),
        ("বিকালের নাস্তা", diet.get("evening_snack", "-")),
        ("রাতের খাবার", diet.get("dinner", "-")),
    )

    for meal_time, desc in meals_bn:
        pdf.set_x(12)
        start_y = pdf.get_y()
        pdf.set_fill_color(247, 250, 250)
        pdf.set_text_color(20, 80, 80)
        pdf.set_font(font_family, "", 10.5)
        pdf.multi_cell(48, 7, f" {meal_time}", border=1, fill=True)
        end_y_left = pdf.get_y()

        pdf.set_xy(60, start_y)
        pdf.set_text_color(40, 40, 40)
        text_val = desc if has_bn_font else desc.encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(138, 7, f" {text_val}", border=1)
        end_y_right = pdf.get_y()
        pdf.set_y(max(end_y_left, end_y_right))

    # Foods to Avoid Section
    pdf.ln(4)
    pdf.set_x(12)
    pdf.set_text_color(170, 30, 30)
    pdf.set_font(font_family, "", 12.5)
    avoid_title = "যেসব খাবার অবশ্যই বর্জন করবেন:" if has_bn_font else "Foods to Strictly Avoid:"
    pdf.cell(0, 8, avoid_title, ln=True)

    pdf.set_text_color(50, 50, 50)
    pdf.set_font(font_family, "", 10.5)
    for food in diet.get("foods_to_avoid", []):
        pdf.set_x(16)
        f_txt = food if has_bn_font else food.encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(180, 6, f"• {f_txt}")

    # Special Advice
    pdf.ln(3)
    pdf.set_x(12)
    pdf.set_text_color(13, 110, 110)
    pdf.set_font(font_family, "", 11.5)
    adv_title = "বিশেষ পরামর্শ:" if has_bn_font else "Special Advice:"
    pdf.cell(0, 7, adv_title, ln=True)

    pdf.set_x(16)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font(font_family, "", 10)
    adv_txt = diet.get("special_advice", "-") if has_bn_font else ""
    pdf.multi_cell(180, 6, adv_txt)

    # Footer Disclaimer
    pdf.ln(4)
    pdf.set_x(12)
    pdf.set_font(font_family, "", 9)
    pdf.set_text_color(110, 110, 110)
    disc_txt = (
        "সতর্কতা: এই ডায়েট চার্টটি স্বাস্থ্যবন্ধু AI দ্বারা তৈরি প্রাথমিক নির্দেশিকা। যেকোনো বড় খাদ্য পরিবর্তন বা জটিল রোগের ক্ষেত্রে নিবন্ধিত চিকিৎসক বা পুষ্টিবিদের পরামর্শ নিন।"
        if has_bn_font
        else "Disclaimer: Consult a registered physician or nutritionist before major dietary changes."
    )
    pdf.multi_cell(186, 5, disc_txt)

    pdf_bytes = bytes(pdf.output())

    # Auto-save inside 'report/' directory
    os.makedirs("report", exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in patient_name).strip("_") or "Patient"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join("report", f"Diet_Chart_{safe_name}_{timestamp}.pdf")
    with open(save_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_bytes
