import urllib.parse

BANGLADESH_HOSPITALS = {
    "Dhaka (ঢাকা বিভাগ)": {
        "Dhaka (ঢাকা)": [
            {"name": "Dhaka Medical College Hospital (DMCH)", "type": "Govt. Medical College", "address": "Secretariat Road, Shahbag, Dhaka", "phone": "02-55165088"},
            {"name": "Shaheed Suhrawardy Medical College Hospital", "type": "Govt. Medical College", "address": "Sher-e-Bangla Nagar, Dhaka", "phone": "02-9130800"},
            {"name": "Sir Salimullah Medical College (Mitford) Hospital", "type": "Govt. Medical College", "address": "Mitford Road, Dhaka", "phone": "02-7319002"},
            {"name": "National Institute of Cardiovascular Diseases (NICVD)", "type": "Govt. Specialized", "address": "Sher-e-Bangla Nagar, Dhaka", "phone": "02-9122560"},
        ],
        "Gazipur (গাজীপুর)": [
            {"name": "Shaheed Tajuddin Ahmad Medical College Hospital", "type": "Govt. Medical College", "address": "Joydebpur, Gazipur", "phone": "02-9263422"},
            {"name": "Tongi 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Tongi, Gazipur", "phone": "01730-324775"},
        ],
        "Narayanganj (নারায়ণগঞ্জ)": [
            {"name": "Narayanganj 300 Bedded Hospital", "type": "Govt. General Hospital", "address": "Khanpur, Narayanganj", "phone": "02-7648440"},
            {"name": "Narayanganj General (Victoria) Hospital", "type": "Govt. Sadar Hospital", "address": "New Metro Hall Road, Narayanganj", "phone": "02-7630420"},
        ],
        "Narsingdi (নরসিংদী)": [
            {"name": "Narsingdi 100 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Basail, Narsingdi", "phone": "01730-324782"},
            {"name": "Narsingdi Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Narsingdi", "phone": "02-9462244"},
        ],
        "Manikganj (মানিকগঞ্জ)": [
            {"name": "Colonel Malek Medical College Hospital", "type": "Govt. Medical College", "address": "Manikganj Sadar, Manikganj", "phone": "01730-324778"},
            {"name": "Manikganj 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Manikganj Sadar", "phone": "02-7710244"},
        ],
        "Munshiganj (মুন্সীগঞ্জ)": [
            {"name": "Munshiganj 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Munshiganj", "phone": "01730-324779"},
        ],
        "Tangail (টাঙ্গাইল)": [
            {"name": "Sheikh Hasina Medical College Hospital, Tangail", "type": "Govt. Medical College", "address": "Kodalia, Tangail", "phone": "0921-62411"},
            {"name": "Tangail 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Tangail", "phone": "01730-324785"},
        ],
        "Kishoreganj (কিশোরগঞ্জ)": [
            {"name": "Shaheed Syed Nazrul Islam Medical College Hospital", "type": "Govt. Medical College", "address": "Jashodal, Kishoreganj", "phone": "0941-61770"},
            {"name": "Kishoreganj 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Station Road, Kishoreganj", "phone": "01730-324776"},
        ],
        "Faridpur (ফরিদপুর)": [
            {"name": "Bangabandhu Sheikh Mujib Medical College Hospital", "type": "Govt. Medical College", "address": "West Khabaspur, Faridpur", "phone": "0631-63442"},
            {"name": "Faridpur General Hospital", "type": "Govt. General Hospital", "address": "Mujib Sarak, Faridpur", "phone": "01730-324774"},
        ],
        "Gopalganj (গোপালগঞ্জ)": [
            {"name": "Sheikh Sayera Khatun Medical College Hospital", "type": "Govt. Medical College", "address": "Gopalganj Sadar", "phone": "02-6685234"},
            {"name": "Gopalganj 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Gopalganj", "phone": "01730-324777"},
        ],
        "Madaripur (মাদারীপুর)": [
            {"name": "Madaripur 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Madaripur", "phone": "01730-324780"},
        ],
        "Rajbari (রাজবাড়ী)": [
            {"name": "Rajbari 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Rajbari", "phone": "01730-324783"},
        ],
        "Shariatpur (শরীয়তপুর)": [
            {"name": "Shariatpur 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Palong, Shariatpur", "phone": "01730-324784"},
        ],
    },
    "Chattogram (চট্টগ্রাম বিভাগ)": {
        "Chattogram (চট্টগ্রাম)": [
            {"name": "Chattogram Medical College Hospital (CMCH)", "type": "Govt. Medical College", "address": "K.B. Fazlul Kader Road, Panchlaish", "phone": "031-619400"},
            {"name": "Chattogram 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Andarkilla, Chattogram", "phone": "031-611407"},
        ],
        "Cox's Bazar (কক্সবাজার)": [
            {"name": "Cox's Bazar 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Cox's Bazar", "phone": "01730-324792"},
            {"name": "Cox's Bazar Medical College Hospital", "type": "Govt. Medical College", "address": "Jhilongja, Cox's Bazar", "phone": "0341-52411"},
        ],
        "Cumilla (কুমিল্লা)": [
            {"name": "Cumilla Medical College Hospital", "type": "Govt. Medical College", "address": "Kuchaitoli, Cumilla", "phone": "081-65562"},
            {"name": "Cumilla General Hospital", "type": "Govt. General Hospital", "address": "Kandirpar, Cumilla", "phone": "01730-324791"},
        ],
        "Brahmanbaria (ব্রাহ্মণবাড়িয়া)": [
            {"name": "Brahmanbaria 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Kumarshil More, Brahmanbaria", "phone": "01730-324789"},
        ],
        "Chandpur (চাঁদপুর)": [
            {"name": "Chandpur 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Chandpur", "phone": "01730-324790"},
        ],
        "Noakhali (নোয়াখালী)": [
            {"name": "250 Bedded General Hospital, Noakhali", "type": "Govt. General Hospital", "address": "Maijdee Court, Noakhali", "phone": "01730-324796"},
        ],
        "Feni (ফেনী)": [
            {"name": "Feni 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Sadar Hospital Road, Feni", "phone": "01730-324793"},
        ],
        "Lakshmipur (লক্ষ্মীপুর)": [
            {"name": "Lakshmipur 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Lakshmipur", "phone": "01730-324795"},
        ],
        "Rangamati (রাঙ্গামাটি)": [
            {"name": "Rangamati General Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Rangamati", "phone": "01730-324797"},
        ],
        "Khagrachhari (খাগড়াছড়ি)": [
            {"name": "Khagrachhari District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Khagrachhari", "phone": "01730-324794"},
        ],
        "Bandarban (বান্দরবান)": [
            {"name": "Bandarban District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Bandarban Sadar", "phone": "01730-324788"},
        ],
    },
    "Rajshahi (রাজশাহী বিভাগ)": {
        "Rajshahi (রাজশাহী)": [
            {"name": "Rajshahi Medical College Hospital (RMCH)", "type": "Govt. Medical College", "address": "Laxmipur, Rajshahi", "phone": "0721-772150"},
        ],
        "Bogura (বগুড়া)": [
            {"name": "Shaheed Ziaur Rahman Medical College Hospital", "type": "Govt. Medical College", "address": "Silimpur, Bogura", "phone": "051-69965"},
            {"name": "Mohammad Ali 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Sherpur Road, Bogura", "phone": "01730-324808"},
        ],
        "Pabna (পাবনা)": [
            {"name": "Pabna 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Pabna", "phone": "01730-324812"},
        ],
        "Sirajganj (সিরাজগঞ্জ)": [
            {"name": "Shaheed M. Monsur Ali Medical College Hospital", "type": "Govt. Medical College", "address": "Shialkol, Sirajganj", "phone": "0751-62411"},
            {"name": "Sirajganj 250 Bedded Bangamata Sheikh Fazilatunnesa Mujib General Hospital", "type": "Govt. General Hospital", "address": "Sirajganj Sadar", "phone": "01730-324814"},
        ],
        "Naogaon (নওগাঁ)": [
            {"name": "Naogaon 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Naogaon", "phone": "01730-324810"},
        ],
        "Natore (নাটোর)": [
            {"name": "Natore 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Natore", "phone": "01730-324811"},
        ],
        "Chapainawabganj (চাঁপাইনবাবগঞ্জ)": [
            {"name": "250 Bedded District Hospital, Chapainawabganj", "type": "Govt. District Hospital", "address": "Hospital Road, Chapainawabganj", "phone": "01730-324809"},
        ],
        "Joypurhat (জয়পুরহাট)": [
            {"name": "Joypurhat 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Joypurhat", "phone": "01730-324813"},
        ],
    },
    "Khulna (খুলনা বিভাগ)": {
        "Khulna (খুলনা)": [
            {"name": "Khulna Medical College Hospital", "type": "Govt. Medical College", "address": "Boyra, Khulna", "phone": "041-761535"},
            {"name": "Khulna 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Khulna", "phone": "01730-324801"},
        ],
        "Jashore (যশোর)": [
            {"name": "Jashore 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Jashore", "phone": "01730-324800"},
        ],
        "Kushtia (কুষ্টিয়া)": [
{"name": "Kushtia 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Court Para, Kushtia", "phone": "01730-324802"},
],
"Satkhira (সাতক্ষীরা)": [
{"name": "Satkhira Medical College Hospital", "type": "Govt. Medical College", "address": "Bakal, Satkhira", "phone": "0471-62411"},
{"name": "Satkhira District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Satkhira Sadar", "phone": "01730-324806"},
],
"Bagerhat (বাগেরহাট)": [
{"name": "Bagerhat 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Bagerhat", "phone": "01730-324798"},
],
"Jhenaidah (ঝিনাইদহ)": [
{"name": "Jhenaidah 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Jhenaidah", "phone": "01730-324803"},
],
"Chuadanga (চুয়াডাঙ্গা)": [
{"name": "Chuadanga 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Chuadanga", "phone": "01730-324799"},
],
"Magura (মাগুরা)": [
{"name": "Magura 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Magura", "phone": "01730-324804"},
],
"Meherpur (মেহেরপুর)": [
{"name": "Meherpur 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Meherpur", "phone": "01730-324805"},
],
"Narail (নড়াইল)": [
{"name": "Narail District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Narail", "phone": "01730-324807"},
],
},
"Sylhet (সিলেট বিভাগ)": {
"Sylhet (সিলেট)": [
{"name": "Sylhet MAG Osmani Medical College Hospital", "type": "Govt. Medical College", "address": "Medical Road, Kajolshah, Sylhet", "phone": "0821-713667"},
{"name": "Sylhet Shahid Shamsuddin Ahmed District Hospital", "type": "Govt. District Hospital", "address": "Chouhatta, Sylhet", "phone": "01730-324822"},
],
"Moulvibazar (মৌলভীবাজার)": [
{"name": "Moulvibazar 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Moulvibazar", "phone": "01730-324820"},
],
"Habiganj (হবিগঞ্জ)": [
{"name": "Habiganj 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Habiganj", "phone": "01730-324819"},
],
"Sunamganj (সুনামগঞ্জ)": [
{"name": "Sunamganj 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Sunamganj", "phone": "01730-324821"},
],
},
"Barishal (বরিশাল বিভাগ)": {
"Barishal (বরিশাল)": [
{"name": "Sher-e-Bangla Medical College Hospital (SBMCH)", "type": "Govt. Medical College", "address": "Band Road, Barishal", "phone": "0431-2173547"},
{"name": "Barishal General (Sadar) Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Barishal", "phone": "01730-324768"},
],
"Patuakhali (পটুয়াখালী)": [
{"name": "Patuakhali Medical College Hospital", "type": "Govt. Medical College", "address": "Hospital Road, Patuakhali", "phone": "01730-324771"},
],
"Bhola (ভোলা)": [
{"name": "Bhola 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Bhola", "phone": "01730-324769"},
],
"Pirojpur (পিরোজপুর)": [
{"name": "Pirojpur District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Pirojpur", "phone": "01730-324772"},
],
"Barguna (বরগুনা)": [
{"name": "Barguna District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Barguna", "phone": "01730-324767"},
],
"Jhalokati (ঝালকাঠি)": [
{"name": "Jhalokati District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Jhalokati", "phone": "01730-324770"},
],
},
"Rangpur (রংপুর বিভাগ)": {
"Rangpur (রংপুর)": [
{"name": "Rangpur Medical College Hospital (RpMCH)", "type": "Govt. Medical College", "address": "Medical East Gate, Rangpur", "phone": "0521-63388"},
],
"Dinajpur (দিনাজপুর)": [
{"name": "M Abdur Rahim Medical College Hospital", "type": "Govt. Medical College", "address": "Sadar, Dinajpur", "phone": "0531-64787"},
{"name": "Dinajpur 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Dinajpur", "phone": "01730-324815"},
],
"Gaibandha (গাইবান্ধা)": [
{"name": "Gaibandha 250 Bedded District Hospital", "type": "Govt. District Hospital", "address": "Hospital Road, Gaibandha", "phone": "01730-324816"},
],
"Kurigram (কুড়িগ্রাম)": [
{"name": "Kurigram 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Kurigram", "phone": "01730-324817"},
],
"Nilphamari (নীলফামারী)": [
{"name": "Nilphamari 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Nilphamari", "phone": "01730-324818"},
],
"Lalmonirhat (লালমনিরহাট)": [
{"name": "Lalmonirhat 100 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Lalmonirhat", "phone": "01730-324823"},
],
"Panchagarh (পঞ্চগড়)": [
{"name": "Panchagarh District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Panchagarh", "phone": "01730-324824"},
],
"Thakurgaon (ঠাকুরগাঁও)": [
{"name": "Thakurgaon 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Thakurgaon", "phone": "01730-324825"},
],
},
"Mymensingh (ময়মনসিংহ বিভাগ)": {
"Mymensingh (ময়মনসিংহ)": [
{"name": "Mymensingh Medical College Hospital (MMCH)", "type": "Govt. Medical College", "address": "Charpara, Mymensingh", "phone": "091-66063"},
],
"Jamalpur (জামালপুর)": [
{"name": "Sheikh Hasina Medical College Hospital, Jamalpur", "type": "Govt. Medical College", "address": "Jamalpur Sadar", "phone": "0981-63411"},
{"name": "Jamalpur 250 Bedded General Hospital", "type": "Govt. General Hospital", "address": "Hospital Road, Jamalpur", "phone": "01730-324786"},
],
"Netrokona (নেত্রকোণা)": [
{"name": "Netrokona District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Netrokona", "phone": "01730-324787"},
],
"Sherpur (শেরপুর)": [
{"name": "Sherpur 250 Bedded District Sadar Hospital", "type": "Govt. Sadar Hospital", "address": "Hospital Road, Sherpur", "phone": "01730-324781"},
],
},
}
def get_divisions() -> list[str]:
    return list(BANGLADESH_HOSPITALS.keys())


def get_districts(division: str) -> list[str]:
    return list(BANGLADESH_HOSPITALS.get(division, {}).keys())


def get_hospitals_by_district(division: str, district: str) -> list[dict]:
    hospitals = BANGLADESH_HOSPITALS.get(division, {}).get(district, [])
    maps_base = "https://google.com" + "/maps/search/?api=1&query="
    enriched = []
    for h in hospitals:
        query = urllib.parse.quote(f"{h['name']} {h['address']}")
        item = h.copy()
        item["maps_url"] = f"{maps_base}{query}"
        enriched.append(item)
    return enriched


def search_hospitals(keyword: str) -> list[dict]:
    """Searches across all 64 districts by district name or hospital name."""
    kw = keyword.strip().lower()
    maps_base = "https://google.com" + "/maps/search/?api=1&query="
    results = []
    for div, districts in BANGLADESH_HOSPITALS.items():
        for dist, hosp_list in districts.items():
            for h in hosp_list:
                if kw in dist.lower() or kw in h["name"].lower() or kw in h["address"].lower():
                    query = urllib.parse.quote(f"{h['name']} {h['address']}")
                    item = h.copy()
                    item["district"] = dist
                    item["division"] = div
                    item["maps_url"] = f"{maps_base}{query}"
                    results.append(item)
    return results
