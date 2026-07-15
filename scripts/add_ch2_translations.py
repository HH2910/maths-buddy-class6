# -*- coding: utf-8 -*-
import json
import re

PATH = "content/sanskrit2_qa.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

# --- Section 0: concept intro — hand-written translations, keyed by exact q text ---
CONCEPT_EN = {
    "संयुक्त-व्यञ्जनानि कथं भवन्ति?": (
        "How are conjunct consonants formed?",
        "Conjunct consonants are formed by joining two or more consonant letters together. "
        "They are not new letters — just a special way of writing separate consonants combined. "
        "The vowel that follows is not merged inside the conjunct itself."
    ),
    "क्ष इति संयुक्त-व्यञ्जनं कथं बनति? उदाहरणेन स्पष्टीकुर्वन्तु (कक्षा)।": (
        "How is the conjunct 'क्ष' formed? Explain with the example कक्षा.",
        "क्ष = क् + ष् + अ\nकक्षा (class/classroom) = क् + अ + क् + ष् + आ"
    ),
    "त्र इति संयुक्त-व्यञ्जनं कथं बनति? उदाहरणेन स्पष्टीकुर्वन्तु (पत्रम्)।": (
        "How is the conjunct 'त्र' formed? Explain with the example पत्रम्.",
        "त्र = त् + र् + अ\nपत्रम् (letter/leaf) = प् + अ + त् + र् + अ + म्"
    ),
    "ज्ञ इति संयुक्त-व्यञ्जनं कथं बनति? उदाहरणेन स्पष्टीकुर्वन्तु (ज्ञानम्)।": (
        "How is the conjunct 'ज्ञ' formed? Explain with the example ज्ञानम्.",
        "ज्ञ = ज् + ञ् + अ\nज्ञानम् (knowledge) = ज् + ञ् + आ + न् + अ + म्"
    ),
    "द्य इति संयुक्त-व्यञ्जनं कथं बनति? उदाहरणेन स्पष्टीकुर्वन्तु (विद्या)।": (
        "How is the conjunct 'द्य' formed? Explain with the example विद्या.",
        "द्य = द् + य् + अ\nविद्या (knowledge/learning) = व् + इ + द् + य् + आ"
    ),
    "किमर्थं संयुक्त-व्यञ्जनानि 'नवीनाः वर्णाः' न कथ्यन्ते?": (
        "Why are conjunct consonants not called 'new letters'?",
        "Because they are just a special writing style of pre-existing, separate consonants — not new, "
        "independent letters. E.g. क्ष = क्+ष् (simply क् and ष् together, not a brand-new letter)."
    ),
    "चाणक्यः, क्रमः, पद्मम्, अर्णवः, मन्त्रः, इन्द्रः, ओष्ठ्यः, उष्ट्रः, सन्ध्या – एतेषु शब्देषु के के संयुक्त-व्यञ्जनाः सन्ति?": (
        "In the words चाणक्यः (Chanakya), क्रमः (sequence), पद्मम् (lotus), अर्णवः (ocean), मन्त्रः (mantra), "
        "इन्द्रः (Indra), ओष्ठ्यः (labial), उष्ट्रः (camel), सन्ध्या (evening/twilight) — which conjunct consonant is in each?",
        "चाणक्यः → क्य\nक्रमः → क्र\nपद्मम् → द्म\nअर्णवः → र्ण\nमन्त्रः → न्त्र\nइन्द्रः → न्द्र\nओष्ठ्यः → ष्ठ्य\nउष्ट्रः → ष्ट्र\nसन्ध्या → न्ध्य"
    ),
}

# --- Word glosses for the drill sections ---
GLOSS = {
    "अजः": "goat", "रामः": "Rama (name)", "हरिः": "Hari/Vishnu (name)", "सीता": "Sita (name)",
    "गुरुः": "teacher", "वधूः": "bride", "ऋषिः": "sage", "मातॄणम्": "of mothers",
    "कॢप्तम्": "supposed", "देवाः": "gods", "एकैकः": "each one", "ओम्": "the sacred syllable Om",
    "औषधम्": "medicine", "वाक्यम्": "sentence", "मूर्धन्यः": "cerebral (sound)",
    "तालव्यः": "palatal (sound)", "बाह्यम्": "external", "क्रीडा": "play/game",
    "ग्रहणम्": "taking/holding", "वज्रः": "thunderbolt/diamond", "द्रष्टा": "seer/spectator",
    "प्रगतिः": "progress", "ब्रह्म": "the Supreme Being", "ब्रह्मचारी": "celibate student",
    "जाह्नवी": "the river Ganga", "ध्वनिः": "sound", "सरस्वती": "Saraswati (goddess)",
    "वर्णः": "letter", "कर्म": "action/deed", "सप्तर्षिः": "the Seven Sages", "ढक्का": "drum",
    "वित्तम्": "wealth", "सिद्धार्थः": "Siddhartha (name)", "पद्मम्": "lotus", "शब्दः": "word/sound",
    "पङ्कजम्": "lotus", "व्यञ्जनम्": "consonant", "कण्ठः": "throat", "सन्धिः": "joining (of letters)",
    "प्रारम्भः": "beginning", "सँस्कर्ता": "one who performs a rite", "कस्मिँश्चिद्": "in some/somewhere",
    "संयमः": "self-control", "संवादः": "dialogue", "हंसः": "swan", "दुःखम्": "sorrow",
    "प्रातःकालः": "morning", "इन्द्रः": "Indra (king of gods)",
    # वर्ण-संयोगः answers
    "दाशरथिः": "son of Dasharatha (Rama)", "हिमालयः": "the Himalayas", "कृष्णः": "Krishna (name)",
    "नरेन्द्रः": "king", "मञ्जुलः": "lovely", "पुष्करः": "lotus", "कुक्कुटः": "rooster",
    "स्वस्तिकः": "auspicious symbol", "शिक्षकः": "teacher", "सङ्गणकम्": "computer",
    "कन्दुकः": "ball", "मन्त्री": "minister", "राष्ट्रम्": "nation", "कण्ठ्यः": "guttural (sound)",
    "दन्त्यः": "dental (sound)", "मत्स्यः": "fish", "ओष्ठ्यः": "labial (sound)",
    "सन्ध्यक्षरम्": "compound-vowel letter", "संस्कृतम्": "Sanskrit", "धार्ष्ट्यम्": "audacity",
    "कार्त्स्न्यम्": "entirety",
}

def gloss_for(word):
    w = word.strip()
    return GLOSS.get(w, "")

vieyoga_re = re.compile(r"^(\S+) इत्यस्य वर्ण-वियोगः कुर्वन्तु।$")
sanyoga_re = re.compile(r"^(.+) → कः शब्दः बनति\?$")
vocab_re = re.compile(r"^(\S+) इत्यस्य अर्थः कः\?$")
english_re = re.compile(r"English:\s*([^)]+)\)")

for section in data:
    name = section["section"]
    for q in section["questions"]:
        qt = q["q"]

        if name == "संयुक्त-व्यञ्जनानि – परिचयः":
            en = CONCEPT_EN.get(qt)
            if en:
                q["qEn"], q["aEn"] = en
            continue

        m = vieyoga_re.match(qt)
        if m:
            word = m.group(1)
            g = gloss_for(word)
            suffix = f" (= {g})" if g else ""
            q["qEn"] = f"Break '{word}'{suffix} into its constituent letters."
            q["aEn"] = f"Letters: {q['a'].split('=', 1)[1].strip()}"
            continue

        m = sanyoga_re.match(qt)
        if m:
            q["qEn"] = "Which word do these letters spell?"
            g = gloss_for(q["a"])
            suffix = f" (= {g})" if g else ""
            q["aEn"] = f"{q['a']}{suffix}"
            continue

        m = vocab_re.match(qt)
        if m:
            word = m.group(1)
            q["qEn"] = f"What is the meaning of {word}?"
            em = english_re.search(q["a"])
            q["aEn"] = em.group(1).strip() if em else ""
            continue

        raise SystemExit(f"Unmatched question, needs manual translation: {qt!r}")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = sum(len(s["questions"]) for s in data)
missing = [q["q"] for s in data for q in s["questions"] if not q.get("qEn") or not q.get("aEn")]
print(f"Wrote {PATH}: {len(data)} sections, {total} questions, missing translations: {len(missing)}")
if missing:
    print(missing[:10])
