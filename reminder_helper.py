import re
from datetime import datetime, timedelta


def _parse_dosage_slots(dosage_str: str) -> tuple[list[tuple[int, int, str]], str]:
    """
    Parses Bangladeshi dosage notations like '1+0+1', '1+1+1', '0+0+1', '1+0+0'
    into (hour, minute, label_bn) slots and meal timing guidance.
    """
    raw = str(dosage_str or "").strip()

    # Determine meal timing from Bengali/English hints
    low = raw.lower()
    if any(k in low for k in ("আগে", "before", "খালি পেটে", "empty")):
        meal_timing = "খাওয়ার ৩০ মিনিট আগে (Before Meal)"
    else:
        meal_timing = "খাওয়ার পর (After Meal)"

    # Normalize Bengali digits to ASCII digits
    bn_to_en = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
    norm = raw.translate(bn_to_en)

    match = re.search(r"([0-9])\s*[\+\-\/]\s*([0-9])\s*[\+\-\/]\s*([0-9])", norm)
    slots = []
    if match:
        m_dose, n_dose, e_dose = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if m_dose > 0:
            slots.append((8, 0, "🌅 সকাল ৮:০০"))
        if n_dose > 0:
            slots.append((14, 0, "☀️ দুপুর ২:০০"))
        if e_dose > 0:
            slots.append((21, 0, "🌙 রাত ৯:০০"))

    # Default fallback if dosage is 'চলবে' or non-numeric
    if not slots:
        slots = [
            (8, 0, "🌅 সকাল ৮:০০"),
            (21, 0, "🌙 রাত ৯:০০"),
        ]

    return slots, meal_timing


def build_medicine_schedule(medicines: list[dict]) -> list[dict]:
    """Builds a human-readable daily reminder schedule for every detected medicine."""
    schedule = []
    for med in medicines:
        med_name = str(med.get("name", "অজানা ওষুধ")).strip()
        dosage = str(med.get("dosage", "")).strip()
        slots, meal_timing = _parse_dosage_slots(dosage)
        time_labels = " | ".join(label for _, _, label in slots)
        schedule.append({
            "medicine": med_name,
            "reminder_times": time_labels,
            "meal_timing": meal_timing,
        })
    return schedule


def generate_ics_calendar(medicines: list[dict], days: int = 7) -> str:
    """
    Generates a standard RFC 5545 .ics calendar file with daily recurring alarms
    that users can import directly into Android or iPhone Calendar.
    """
    now_utc = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    tomorrow = datetime.now().date() + timedelta(days=1)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Shasthobondhu AI//Medicine Reminder//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    for idx, med in enumerate(medicines, 1):
        med_name = str(med.get("name", "Medicine")).strip()
        dosage = str(med.get("dosage", "")).strip()
        usage = str(med.get("usage", "")).strip()
        slots, meal_timing = _parse_dosage_slots(dosage)

        for s_idx, (hour, minute, _) in enumerate(slots, 1):
            start_dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute, 0)
            end_dt = start_dt + timedelta(minutes=15)
            dt_start_str = start_dt.strftime("%Y%m%dT%H%M%S")
            dt_end_str = end_dt.strftime("%Y%m%dT%H%M%S")
            uid = f"shasthobondhu-{idx}-{s_idx}-{now_utc}@shasthobondhu.ai"

            desc = f"Dosage: {dosage} ({meal_timing}) | {usage}".replace("\n", " ")

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now_utc}",
                f"DTSTART:{dt_start_str}",
                f"DTEND:{dt_end_str}",
                f"RRULE:FREQ=DAILY;COUNT={max(1, int(days))}",
                f"SUMMARY:💊 ওষুধ সেবন: {med_name}",
                f"DESCRIPTION:{desc}",
                "BEGIN:VALARM",
                "TRIGGER:-PT0M",
                "ACTION:DISPLAY",
                f"DESCRIPTION:ওষুধ খাওয়ার সময় হয়েছে: {med_name}",
                "END:VALARM",
                "END:VEVENT",
            ])

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)
