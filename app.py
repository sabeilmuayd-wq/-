import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - تعليم الأطفال",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"
if "level" not in st.session_state:
    st.session_state.level = "kg"
if "term" not in st.session_state:
    st.session_state.term = 1
if "subject" not in st.session_state:
    st.session_state.subject = "islamic"

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "📚 Noor Al-Ma'rifa",
        "subtitle": "Islamic Education | English | Mathematics",
        "select_level": "🎓 Select Grade",
        "kg": "🏫 Kindergarten (KG)",
        "p1": "📖 Primary 1",
        "p2": "📘 Primary 2",
        "select_subject": "📚 Subject",
        "islamic": "🕌 Islamic Education",
        "english": "📖 English",
        "math": "🔢 Mathematics",
        "term": "📅 Term",
        "term1": "Term 1",
        "term2": "Term 2",
        "term3": "Term 3",
        "term4": "Term 4",
        "lessons": "📚 Lessons",
        "quiz": "📝 Quiz",
        "my_score": "⭐ My Score",
        "correct": "✅ Correct!",
        "wrong": "❌ Wrong",
        "score": "Score",
        "out_of": "out of",
        "surah": "📖 Surah",
        "meaning": "Meaning",
        "dua": "🤲 Daily Dua"
    },
    "ar": {
        "title": "📚 نور المعرفة",
        "subtitle": "تربية إسلامية | لغة إنجليزية | رياضيات",
        "select_level": "🎓 اختر المرحلة",
        "kg": "🏫 رياض الأطفال (KG)",
        "p1": "📖 الصف الأول",
        "p2": "📘 الصف الثاني",
        "select_subject": "📚 المادة",
        "islamic": "🕌 التربية الإسلامية",
        "english": "📖 اللغة الإنجليزية",
        "math": "🔢 الرياضيات",
        "term": "📅 الفصل الدراسي",
        "term1": "الفصل الأول",
        "term2": "الفصل الثاني",
        "term3": "الفصل الثالث",
        "term4": "الفصل الرابع",
        "lessons": "📚 الدروس",
        "quiz": "📝 اختبار",
        "my_score": "⭐ درجتي",
        "correct": "✅ إجابة صحيحة!",
        "wrong": "❌ إجابة خاطئة",
        "score": "الدرجة",
        "out_of": "من",
        "surah": "📖 سورة",
        "meaning": "المعنى",
        "dua": "🤲 دعاء اليوم"
    },
    "sw": {
        "title": "📚 Noor Al-Ma'rifa",
        "subtitle": "Elimu ya Kiislamu | Kiingereza | Hisabati",
        "select_level": "🎓 Chagua Darasa",
        "kg": "🏫 Darasa la Awali (KG)",
        "p1": "📖 Darasa la Kwanza",
        "p2": "📘 Darasa la Pili",
        "select_subject": "📚 Somo",
        "islamic": "🕌 Elimu ya Kiislamu",
        "english": "📖 Kiingereza",
        "math": "🔢 Hisabati",
        "term": "📅 Muhula",
        "term1": "Muhula wa 1",
        "term2": "Muhula wa 2",
        "term3": "Muhula wa 3",
        "term4": "Muhula wa 4",
        "lessons": "📚 Masomo",
        "quiz": "📝 Mtihani",
        "my_score": "⭐ Alama Yangu",
        "correct": "✅ Jibu Sahihi!",
        "wrong": "❌ Jibu Sio Sahihi",
        "score": "Alama",
        "out_of": "kati ya",
        "surah": "📖 Surah",
        "meaning": "Maana",
        "dua": "🤲 Dua ya Leo"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== المحتوى التعليمي ====================
content = {
    "kg": {
        "islamic": {
            1: {
                "lessons": [
                    {"title": "أنا مسلم", "text": "أنا مسلم. ربي الله. نبينا محمد ﷺ. ديننا الإسلام."},
                    {"title": "سورة الفاتحة", "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\nالرَّحْمَٰنِ الرَّحِيمِ\nمَالِكِ يَوْمِ الدِّينِ\nإِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\nاهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\nصِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"},
                    {"title": "دعاء الاستيقاظ", "text": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ"}
                ],
                "quiz": [
                    {"q": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "a": "محمد"},
                    {"q": "كم عدد آيات سورة الفاتحة؟", "options": ["5", "6", "7", "8"], "a": "7"}
                ]
            },
            2: {
                "lessons": [
                    {"title": "أركان الإسلام", "text": "أركان الإسلام خمسة:\n1. الشهادتان\n2. إقام الصلاة\n3. إيتاء الزكاة\n4. صوم رمضان\n5. حج البيت"},
                    {"title": "سورة الإخلاص", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ"},
                    {"title": "دعاء دخول الخلاء", "text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ"}
                ],
                "quiz": [
                    {"q": "كم عدد أركان الإسلام؟", "options": ["3", "4", "5", "6"], "a": "5"},
                    {"q": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "a": "4"}
                ]
            },
            3: {
                "lessons": [
                    {"title": "أركان الإيمان", "text": "أركان الإيمان ستة:\n1. الإيمان بالله\n2. الإيمان بالملائكة\n3. الإيمان بالكتب\n4. الإيمان بالرسل\n5. الإيمان باليوم الآخر\n6. الإيمان بالقدر خيره وشره"},
                    {"title": "سورة الفلق", "text": "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ\nمِن شَرِّ مَا خَلَقَ\nوَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ\nوَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ\nوَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ"},
                    {"title": "دعاء الأكل", "text": "بِسْمِ اللَّهِ وَبَرَكَةِ اللَّهِ"}
                ],
                "quiz": [
                    {"q": "كم عدد أركان الإيمان؟", "options": ["4", "5", "6", "7"], "a": "6"},
                    {"q": "سورة الفلق تحمي من؟", "options": ["المرض", "الحسد", "الفقر", "الجهل"], "a": "الحسد"}
                ]
            },
            4: {
                "lessons": [
                    {"title": "الوضوء", "text": "خطوات الوضوء:\n1. نية الوضوء\n2. غسل الكفين\n3. المضمضة والاستنشاق\n4. غسل الوجه\n5. غسل اليدين إلى المرفقين\n6. مسح الرأس والأذنين\n7. غسل الرجلين إلى الكعبين"},
                    {"title": "سورة الناس", "text": "قُلْ أَعُوذُ بِرَبِّ النَّاسِ\nمَلِكِ النَّاسِ\nإِلَٰهِ النَّاسِ\nمِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ\nالَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ\nمِنَ الْجِنَّةِ وَالنَّاسِ"},
                    {"title": "دعاء النوم", "text": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا"}
                ],
                "quiz": [
                    {"q": "كم عدد فروض الوضوء؟", "options": ["4", "5", "6", "7"], "a": "6"},
                    {"q": "سورة الناس تحمي من؟", "options": ["المرض", "الوسواس", "الفقر", "الجهل"], "a": "الوسواس"}
                ]
            }
        },
        "english": {
            1: {
                "lessons": [
                    {"title": "My Family", "text": "I have a father. I have a mother. I have brothers and sisters."},
                    {"title": "My Body", "text": "I have eyes to see. I have ears to hear. I have hands to clap."}
                ],
                "quiz": [
                    {"q": "What do we use to see?", "options": ["Ears", "Eyes", "Hands", "Feet"], "a": "Eyes"}
                ]
            },
            2: {
                "lessons": [
                    {"title": "My School", "text": "I go to school. I have a teacher. I have friends."},
                    {"title": "Colors", "text": "Red, Blue, Yellow, Green, Black, White"}
                ],
                "quiz": [
                    {"q": "What color is grass?", "options": ["Red", "Blue", "Green", "Yellow"], "a": "Green"}
                ]
            },
            3: {
                "lessons": [
                    {"title": "Animals", "text": "Cow, Goat, Sheep, Chicken, Dog, Cat"},
                    {"title": "Fruits", "text": "Banana, Mango, Orange, Pineapple, Apple"}
                ],
                "quiz": [
                    {"q": "What animal gives milk?", "options": ["Chicken", "Cow", "Dog", "Cat"], "a": "Cow"}
                ]
            },
            4: {
                "lessons": [
                    {"title": "My Village", "text": "I live in Kiryandongo. There is a market. There is a school."},
                    {"title": "Weather", "text": "Sunny, Rainy, Cloudy, Windy, Hot, Cold"}
                ],
                "quiz": [
                    {"q": "Where do we pray?", "options": ["School", "Market", "Mosque", "Farm"], "a": "Mosque"}
                ]
            }
        },
        "math": {
            1: {
                "lessons": [
                    {"title": "Counting 1-10", "text": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"},
                    {"title": "Shapes", "text": "Circle, Square, Triangle, Rectangle"}
                ],
                "quiz": [
                    {"q": "What is after 5?", "options": ["4", "6", "7", "8"], "a": "6"}
                ]
            },
            2: {
                "lessons": [
                    {"title": "Addition 1-10", "text": "1+1=2, 2+2=4, 3+2=5"},
                    {"title": "Subtraction 1-10", "text": "2-1=1, 5-2=3, 7-3=4"}
                ],
                "quiz": [
                    {"q": "3 + 2 = ?", "options": ["4", "5", "6", "7"], "a": "5"}
                ]
            },
            3: {
                "lessons": [
                    {"title": "Numbers 11-20", "text": "11, 12, 13, 14, 15, 16, 17, 18, 19, 20"},
                    {"title": "Money", "text": "1000, 2000, 5000, 10000 shillings"}
                ],
                "quiz": [
                    {"q": "What is after 15?", "options": ["14", "16", "17", "18"], "a": "16"}
                ]
            },
            4: {
                "lessons": [
                    {"title": "Addition up to 20", "text": "10+5=15, 12+3=15, 14+2=16"},
                    {"title": "Subtraction up to 20", "text": "15-3=12, 18-4=14, 20-5=15"}
                ],
                "quiz": [
                    {"q": "12 + 5 = ?", "options": ["15", "16", "17", "18"], "a": "17"}
                ]
            }
        }
    },
    "p1": {"islamic": {}, "english": {}, "math": {}},
    "p2": {"islamic": {}, "english": {}, "math": {}}
}

# ==================== واجهة التطبيق ====================
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); border-radius: 20px; margin-bottom: 2rem; color: white;'>
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# اختيار المرحلة
st.markdown(f"### {t('select_level')}")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏫 " + t("kg"), use_container_width=True):
        st.session_state.level = "kg"
        st.rerun()
with col2:
    if st.button("📖 " + t("p1"), use_container_width=True):
        st.session_state.level = "p1"
        st.rerun()
with col3:
    if st.button("📘 " + t("p2"), use_container_width=True):
        st.session_state.level = "p2"
        st.rerun()

# اختيار المادة
st.markdown(f"### {t('select_subject')}")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🕌 " + t("islamic"), use_container_width=True):
        st.session_state.subject = "islamic"
        st.rerun()
with col2:
    if st.button("📖 " + t("english"), use_container_width=True):
        st.session_state.subject = "english"
        st.rerun()
with col3:
    if st.button("🔢 " + t("math"), use_container_width=True):
        st.session_state.subject = "math"
        st.rerun()

# اختيار الفصل
st.markdown(f"### {t('term')}")
col1, col2, col3, col4 = st.columns(4)
for i in range(1, 5):
    with [col1, col2, col3, col4][i-1]:
        if st.button(f"{t('term')} {i}", use_container_width=True):
            st.session_state.term = i
            st.rerun()

# عرض المحتوى
st.markdown(f"## {t('lessons')}")

try:
    level_data = content.get(st.session_state.level, {})
    subject_data = level_data.get(st.session_state.subject, {})
    term_data = subject_data.get(st.session_state.term, {})

    if term_data and "lessons" in term_data:
        for lesson in term_data["lessons"]:
            with st.expander(f"📖 {lesson['title']}"):
                st.markdown(lesson['text'])
    else:
        st.info("📚 المزيد من الدروس قيد الإضافة...")

    # اختبار
    st.markdown(f"## {t('quiz')}")
    if term_data and "quiz" in term_data:
        score = 0
        for i, q in enumerate(term_data["quiz"]):
            st.markdown(f"**{i+1}. {q['q']}**")
            answer = st.radio("", q['options'], key=f"q_{i}", index=None)
            if answer and answer == q['a']:
                st.markdown(f"<p style='color: green;'>✅ {t('correct')}</p>", unsafe_allow_html=True)
                score += 1
            elif answer:
                st.markdown(f"<p style='color: red;'>❌ {t('wrong')}</p>", unsafe_allow_html=True)
            st.markdown("---")
        st.markdown(f"### {t('my_score')}: {score}/{len(term_data['quiz'])} {t('out_of')} {len(term_data['quiz'])}")
        if score == len(term_data['quiz']):
            st.balloons()
    else:
        st.info("📝 اختبارات قريباً...")

except Exception as e:
    st.info("📚 اختر المرحلة والمادة والفصل")

# الشريط الجانبي
with st.sidebar:
    st.markdown(f"### 📚 {t('title')}")
    st.markdown(f"**{t('select_level')}:** {t(st.session_state.level)}")
    st.markdown(f"**{t('select_subject')}:** {t(st.session_state.subject)}")
    st.markdown(f"**{t('term')}:** {st.session_state.term}")
    st.markdown("---")
    st.markdown("### 🌍 Language")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.language = "en"
            st.rerun()
    with col2:
        if st.button("🇸🇦 العربية", use_container_width=True):
            st.session_state.language = "ar"
            st.rerun()
