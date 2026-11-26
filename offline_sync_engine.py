import io
import os
import re
import json
import streamlit as st
from PIL import Image, ImageOps
from google import genai
from google.genai import types


def _get_gemini_client():
    """Retrieves Gemini API key from Streamlit Secrets or Environment Variables."""
    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")

    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def is_ollama_running() -> bool:
    """Checks if Cloud Gemini AI is configured and ready (keeps compatibility with app.py)."""
    return _get_gemini_client() is not None


def preprocess_prescription_image(image_file, max_size: int = 1600) -> bytes:
    """Keeps natural, high-resolution handwriting intact."""
    img = Image.open(image_file)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def _extract_json(raw_text: str) -> dict:
    """Safely extracts JSON from AI response."""
    cleaned = raw_text.strip().replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    cleaned = re.sub(r",\s*([\}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def analyze_prescription(image_bytes: bytes) -> tuple[dict, str]:
    """
    Analyzes handwritten or printed Bangladeshi prescriptions using Google Gemini 2.5 Flash.
    Extracts doctor info, exact medicine brand names, dosages, and Bengali medical usage.
    """
    client = _get_gemini_client()
    if not client:
        raise RuntimeError(
            "Gemini API Key সেট করা নেই। Streamlit Dashboard -> Settings -> Secrets-এ GEMINI_API_KEY যুক্ত করুন।"
        )

    prompt = """
    You are an expert Bangladeshi pharmacist and medical OCR assistant.
    Analyze this prescription image carefully and extract all details in valid JSON format.

    Instructions:
    1. Read the doctor's name, degrees, and chamber/hospital address from the header. If unclear or missing, write "উল্লেখ নেই".
    2. Transcribe ALL handwritten or printed medicines accurately using their exact Bangladeshi brand names and strengths (e.g., Tab. Pantonix 20, Cap. Rivacap 3, Tab. Jovia Silver, Tab. Napa Extra). Do NOT replace brand names with generic names.
    3. Extract the dosage schedule (e.g., "1+0+1", "১+০+১", "0+0+1 সকালে/রাতে খাবার পর"). If unreadable, write "চিকিৎসকের পরামর্শ অনুযায়ী".
    4. For each medicine, write its true medical usage/indication in 1 simple, clear Bengali sentence (বাংলায়).
    5. Provide a brief 1-2 sentence summary in Bengali.

    Return ONLY raw JSON matching this exact structure:
    {
      "doctor_name": "string",
      "doctor_degree": "string",
      "chamber_address": "string",
      "diagnosis": "string",
      "medicines": [
        {
          "name": "Brand Name & Strength",
          "usage": "কী কাজে লাগে (বাংলায়)",
          "dosage": "খাবার নিয়ম"
        }
      ],
      "summary": "সহজ সারাংশ (বাংলায়)"
    }
    """

    model_name = "gemini-2.5-flash"
    response = client.models.generate_content(
        model=model_name,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt,
        ],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    data = _extract_json(response.text)
    medicines = data.get("medicines", [])

    result = {
        "doctor_name": data.get("doctor_name") or "উল্লেখ নেই",
        "doctor_degree": data.get("doctor_degree") or "উল্লেখ নেই",
        "chamber_address": data.get("chamber_address") or "উল্লেখ নেই",
        "diagnosis": data.get("diagnosis") or "প্রেসক্রিপশন অনুযায়ী",
        "medicines": medicines,
        "summary": data.get("summary")
        or f"প্রেসক্রিপশন থেকে মোট {len(medicines)}টি ওষুধের নাম ও কার্যকারিতা পড়া হয়েছে।",
    }

    return result, f"Cloud Vision AI ({model_name})"


def _fallback_clinical_diet(patient_data: dict) -> dict:
    """Clinical Bangladeshi diet chart generator."""
    disease = patient_data.get("disease", "").lower()
    bmi = patient_data.get("bmi", 22.0)

    is_diabetic = any(w in disease for w in ["ডায়াবেটিস", "diabetes", "sugar", "সুগার"])
    is_bp = any(w in disease for w in ["প্রেসার", "রক্তচাপ", "pressure", "hypertension", "bp"])

    calories = "১৪০০ - ১৬০০ ক্যালরি" if bmi >= 25 or is_diabetic else "১৮০০ - ২০০০ ক্যালরি"
    avoid = ["অতিরিক্ত তেল-চর্বিযুক্ত ভাজাপোড়া ও ফাস্টফুড", "কোমল পানীয় ও প্যাকেটজাত জুস"]
    if is_diabetic:
        avoid.extend(["চিনি, মিষ্টি, গুড় ও অতিরিক্ত মিষ্টি ফল", "সাদা ভাত ও ময়দার তৈরি খাবার অতিরিক্ত খাওয়া"])
    if is_bp:
        avoid.extend(["খাবারে কাঁচা লবণ (আলগা লবণ)", "আচার, চানাচুর ও অতিরিক্ত লবণাক্ত শুঁটকি"])
    if not is_diabetic and not is_bp:
        avoid.append("অতিরিক্ত চিনি ও প্রক্রিয়াজাত খাবার")

    return {
        "daily_calorie_target": f"{calories} এবং দৈনিক ৮-১০ গ্লাস বিশুদ্ধ পানি",
        "early_morning": "১ গ্লাস কুসুম গরম পানি ও ভেজানো মেথি বা চিয়া সিড (১ চা চামচ)",
        "breakfast": "২টি লাল আটার রুটি, ১ বাটি সবজি ভাজি (কম তেলে) ও ১টি সিদ্ধ ডিমের সাদা অংশ",
        "mid_morning_snack": "১টি মৌসুমি কম মিষ্টি ফল (পেয়ারা, আমলকী বা আপেল) অথবা ১ কাপ গ্রিন টি",
        "lunch": "১ থেকে ১.৫ কাপ ভাত (লাল চাল হলে ভালো), ১ টুকরো মাছ বা চামড়া ছাড়া মুরগি, ১ বাটি পাতলা ডাল ও পর্যাপ্ত শাকসবজি",
        "evening_snack": "১ মুঠো ভাজা ছোলা বা মুড়ি (তেল/চানাচুর ছাড়া) এবং চিনি ছাড়া লাল চা",
        "dinner": "২টি লাল আটার রুটি, ১ বাটি সবজি ও ১ টুকরো মাছ বা ডাল (ঘুমানোর অন্তত ২ ঘণ্টা আগে)",
        "foods_to_avoid": avoid,
        "special_advice": "প্রতিদিন অন্তত ৩০-৪০ মিনিট দ্রুত হাঁটুন, পর্যাপ্ত ঘুমান এবং নিয়মিত চিকিৎসকের পরামর্শ অনুযায়ী ওষুধ সেবন করুন।",
    }


def generate_diet_chart(patient_data: dict) -> tuple[dict, str]:
    """Generates Bangladeshi diet chart via Clinical Nutrition Engine."""
    return _fallback_clinical_diet(patient_data), "Clinical Nutrition Engine (Bangladeshi Diet)"
