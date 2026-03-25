import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="منصة تعليم الأطفال - أوغندا",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PWA Support ====================
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#2ecc71">
<meta name="apple-mobile-web-app-capable" content="yes">
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js');
}
</script>
<style>
    .main-header {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .level-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s;
        border: 2px solid #2ecc71;
    }
    .level-card:hover {
        transform: scale(1.02);
        background: #f0fff0;
    }
    .lesson-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 5px solid #2ecc71;
    }
    .quiz-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #ddd;
    }
    .correct { color: #2ecc71; font-weight: bold; }
    .wrong { color: #e74c3c; font-weight: bold; }
    .islamic-card {
        background: #fef9e6;
        border-left: 5px solid #f39c12;
    }
    .dua-card {
        background: #e8f4fd;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"
if "level" not in st.session_state:
    st.session_state.level = "kg"  # kg, p1, p2
if "term" not in st.session_state:
    st.session_state.term = 1
if "subject" not in st.session_state:
    st.session_state.subject = "islamic"
if "score" not in st.session_state:
    st.session_state.score = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# ==================== الترجمة ====================
lang_text = {
    "en": {
        "title": "📚 Kids Education Platform",
        "subtitle": "Islamic Education | English | Mathematics",
        "select_level": "🎓 Select Grade",
        "kg": "🏫 Kindergarten (KG)",
        "p1": "📖 Primary 1 (P1)",
        "p2": "📘 Primary 2 (P2)",
        "select_subject": "📚 Select Subject",
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
        "check_answer": "✅ Check Answer",
        "next_lesson": "➡️ Next Lesson",
        "prev_lesson": "⬅️ Previous Lesson",
        "correct": "✅ Correct! Well done!",
        "wrong": "❌ Wrong. Try again!",
        "score": "Score",
        "out_of": "out of",
        "surah": "📖 Surah",
        "meaning": "Meaning",
        "dua": "🤲 Daily Dua",
        "pillars_of_islam": "🕋 Pillars of Islam",
        "pillars_of_faith": "⭐ Pillars of Faith",
        "wudu": "💧 Wudu (Ablution)",
        "prayer": "🕌 Prayer Times"
    },
    "ar": {
        "title": "📚 منصة تعليم الأطفال",
        "subtitle": "تربية إسلامية | لغة إنجليزية | رياضيات",
        "select_level": "🎓 اختر المرحلة",
        "kg": "🏫 رياض الأطفال (KG)",
        "p1": "📖 الصف الأول الابتدائي (P1)",
        "p2": "📘 الصف الثاني الابتدائي (P2)",
        "select_subject": "📚 اختر المادة",
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
        "check_answer": "✅ تحقق من الإجابة",
        "next_lesson": "➡️ الدرس التالي",
        "prev_lesson": "⬅️ الدرس السابق",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ إجابة خاطئة. حاول مرة أخرى!",
        "score": "الدرجة",
        "out_of": "من",
        "surah": "📖 سورة",
        "meaning": "المعنى",
        "dua": "🤲 دعاء اليوم",
        "pillars_of_islam": "🕋 أركان الإسلام",
        "pillars_of_faith": "⭐ أركان الإيمان",
        "wudu": "💧 الوضوء",
        "prayer": "🕌 أوقات الصلاة"
    },
    "sw": {
        "title": "📚 Jukwaa la Elimu ya Watoto",
        "subtitle": "Elimu ya Kiislamu | Kiingereza | Hisabati",
        "select_level": "🎓 Chagua Darasa",
        "kg": "🏫 Darasa la Awali (KG)",
        "p1": "📖 Darasa la Kwanza (P1)",
        "p2": "📘 Darasa la Pili (P2)",
        "select_subject": "📚 Chagua Somo",
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
        "check_answer": "✅ Angalia Jibu",
        "next_lesson": "➡️ Somo Linalofuata",
        "prev_lesson": "⬅️ Somo Lililotangulia",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Jibu Sio Sahihi. Jaribu Tena!",
        "score": "Alama",
        "out_of": "kati ya",
        "surah": "📖 Surah",
        "meaning": "Maana",
        "dua": "🤲 Dua ya Leo",
        "pillars_of_islam": "🕋 Nguzo za Uislamu",
        "pillars_of_faith": "⭐ Nguzo za Imani",
        "wudu": "💧 Udhu",
        "prayer": "🕌 Wakati wa Swala"
    }
}

def t(key):
    return lang_text[st.session_state.language].get(key, key)

# ==================== المنهج الكامل (تربية إسلامية + لغة + رياضيات) ====================
CURRICULUM = {
    "kg": {
        "name": t("kg"),
        "terms": {
            1: {
                "title": t("term1"),
                "islamic": {
                    "lessons": [
                        {"title": "أنا مسلم", "content": "أنا مسلم. ربي الله. نبينا محمد ﷺ. ديننا الإسلام.", "keywords": ["الله", "محمد", "إسلام"]},
                        {"title": "سورة الفاتحة", "content": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\nالرَّحْمَٰنِ الرَّحِيمِ\nمَالِكِ يَوْمِ الدِّينِ\nإِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\nاهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\nصِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", "translation": "الحمد لله رب العالمين...", "audio": True},
                        {"title": "دعاء الاستيقاظ", "content": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", "meaning": "الحمد لله الذي أحيانا بعد ما أماتنا وإليه النشور"}
                    ],
                    "quiz": [
                        {"question": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "answer": "محمد"},
                        {"question": "سورة الفاتحة كم آية؟", "options": ["5", "6", "7", "8"], "answer": "7"},
                        {"question": "ماذا نقول عند الاستيقاظ؟", "options": ["بسم الله", "الحمد لله", "اللهم صل على محمد", "اللهم اغفر لي"], "answer": "الحمد لله"}
                    ]
                },
                "english": {
                    "lessons": [
                        {"title": "My Family", "content": "I have a father. I have a mother. I have brothers and sisters. We live together.", "vocab": ["father", "mother", "brother", "sister"]},
                        {"title": "My Body", "content": "I have eyes to see. I have ears to hear. I have hands to clap. I have feet to walk.", "vocab": ["eyes", "ears", "hands", "feet"]}
                    ],
                    "quiz": [
                        {"question": "Who is your father?", "options": ["My mother's husband", "My brother", "My teacher", "My friend"], "answer": "My mother's husband"},
                        {"question": "What do we use to see?", "options": ["Ears", "Eyes", "Hands", "Feet"], "answer": "Eyes"}
                    ]
                },
                "math": {
                    "lessons": [
                        {"title": "Counting 1-10", "content": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "practice": "عد إلى 10"},
                        {"title": "Shapes", "content": "Circle, Square, Triangle, Rectangle", "practice": "تعرف على الأشكال"}
                    ],
                    "quiz": [
                        {"question": "ما هو العدد بعد 5؟", "options": ["4", "6", "7", "8"], "answer": "6"},
                        {"question": "What shape has 4 equal sides?", "options": ["Circle", "Square", "Triangle", "Rectangle"], "answer": "Square"}
                    ]
                }
            },
            2: {
                "title": t("term2"),
                "islamic": {
                    "lessons": [
                        {"title": "أركان الإسلام", "content": "1. الشهادتان\n2. إقام الصلاة\n3. إيتاء الزكاة\n4. صوم رمضان\n5. حج البيت", "keywords": ["شهادة", "صلاة", "زكاة", "صوم", "حج"]},
                        {"title": "سورة الإخلاص", "content": "قُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", "translation": "قل هو الله أحد..."},
                        {"title": "دعاء دخول الخلاء", "content": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ", "meaning": "اللهم إني أعوذ بك من الخبث والخبائث"}
                    ],
                    "quiz": [
                        {"question": "كم عدد أركان الإسلام؟", "options": ["3", "4", "5", "6"], "answer": "5"},
                        {"question": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "answer": "4"},
                        {"question": "ماذا نقول عند دخول الخلاء؟", "options": ["بسم الله", "اللهم إني أعوذ بك", "سبحان الله", "الحمد لله"], "answer": "اللهم إني أعوذ بك"}
                    ]
                },
                "english": {
                    "lessons": [
                        {"title": "My School", "content": "I go to school. I have a teacher. I have friends. I learn many things.", "vocab": ["school", "teacher", "friend", "learn"]},
                        {"title": "Colors", "content": "Red, Blue, Yellow, Green, Black, White", "vocab": ["red", "blue", "yellow", "green"]}
                    ],
                    "quiz": [
                        {"question": "Who teaches you?", "options": ["Friend", "Teacher", "Mother", "Father"], "answer": "Teacher"},
                        {"question": "What color is grass?", "options": ["Red", "Blue", "Green", "Yellow"], "answer": "Green"}
                    ]
                },
                "math": {
                    "lessons": [
                        {"title": "Addition 1-10", "content": "1+1=2, 2+2=4, 3+2=5, 4+3=7", "practice": "اجمع الأعداد"},
                        {"title": "Subtraction 1-10", "content": "2-1=1, 5-2=3, 7-3=4, 9-4=5", "practice": "اطرح الأعداد"}
                    ],
                    "quiz": [
                        {"question": "3 + 2 = ?", "options": ["4", "5", "6", "7"], "answer": "5"},
                        {"question": "5 - 2 = ?", "options": ["2", "3", "4", "5"], "answer": "3"}
                    ]
                }
            },
            3: {
                "title": t("term3"),
                "islamic": {
                    "lessons": [
                        {"title": "أركان الإيمان", "content": "1. الإيمان بالله\n2. الإيمان بالملائكة\n3. الإيمان بالكتب\n4. الإيمان بالرسل\n5. الإيمان باليوم الآخر\n6. الإيمان بالقدر خيره وشره", "keywords": ["الله", "ملائكة", "كتب", "رسل", "يوم الآخر", "قدر"]},
                        {"title": "سورة الفلق", "content": "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ\nمِن شَرِّ مَا خَلَقَ\nوَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ\nوَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ\nوَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ", "translation": "قل أعوذ برب الفلق..."},
                        {"title": "دعاء الأكل", "content": "بِسْمِ اللَّهِ وَبَرَكَةِ اللَّهِ", "meaning": "بسم الله وبركة الله"}
                    ],
                    "quiz": [
                        {"question": "كم عدد أركان الإيمان؟", "options": ["4", "5", "6", "7"], "answer": "6"},
                        {"question": "سورة الفلق تحمي من؟", "options": ["المرض", "الحسد", "الفقر", "الجهل"], "answer": "الحسد"}
                    ]
                },
                "english": {
                    "lessons": [
                        {"title": "Animals", "content": "Cow, Goat, Sheep, Chicken, Dog, Cat", "vocab": ["cow", "goat", "sheep", "chicken"]},
                        {"title": "Fruits", "content": "Banana, Mango, Orange, Pineapple, Apple", "vocab": ["banana", "mango", "orange", "apple"]}
                    ],
                    "quiz": [
                        {"question": "What animal gives milk?", "options": ["Chicken", "Cow", "Dog", "Cat"], "answer": "Cow"},
                        {"question": "What fruit is yellow?", "options": ["Apple", "Orange", "Banana", "Mango"], "answer": "Banana"}
                    ]
                },
                "math": {
                    "lessons": [
                        {"title": "Numbers 11-20", "content": "11, 12, 13, 14, 15, 16, 17, 18, 19, 20", "practice": "عد إلى 20"},
                        {"title": "Money (UGX)", "content": "1000 shillings, 2000 shillings, 5000 shillings, 10000 shillings", "practice": "تعرف على العملات"}
                    ],
                    "quiz": [
                        {"question": "ما هو العدد بعد 15؟", "options": ["14", "16", "17", "18"], "answer": "16"},
                        {"question": "1000 + 1000 = ?", "options": ["1000", "1500", "2000", "2500"], "answer": "2000"}
                    ]
                }
            },
            4: {
                "title": t("term4"),
                "islamic": {
                    "lessons": [
                        {"title": "الوضوء", "content": "1. نية الوضوء\n2. غسل الكفين\n3. المضمضة والاستنشاق\n4. غسل الوجه\n5. غسل اليدين إلى المرفقين\n6. مسح الرأس والأذنين\n7. غسل الرجلين إلى الكعبين\n8. الترتيب", "keywords": ["نية", "غسل", "مسح", "ترتيب"]},
                        {"title": "سورة الناس", "content": "قُلْ أَعُوذُ بِرَبِّ النَّاسِ\nمَلِكِ النَّاسِ\nإِلَٰهِ النَّاسِ\nمِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ\nالَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ\nمِنَ الْجِنَّةِ وَالنَّاسِ", "translation": "قل أعوذ برب الناس..."},
                        {"title": "دعاء النوم", "content": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "meaning": "باسمك اللهم أموت وأحيا"}
                    ],
                    "quiz": [
                        {"question": "كم عدد فروض الوضوء؟", "options": ["4", "5", "6", "7"], "answer": "6"},
                        {"question": "سورة الناس تحمي من؟", "options": ["المرض", "الوسواس", "الفقر", "الجهل"], "answer": "الوسواس"}
                    ]
                },
                "english": {
                    "lessons": [
                        {"title": "My Village", "content": "I live in Kiryandongo. There is a market. There is a school. There is a mosque. There are many farms.", "vocab": ["village", "market", "mosque", "farm"]},
                        {"title": "Weather", "content": "Sunny, Rainy, Cloudy, Windy, Hot, Cold", "vocab": ["sunny", "rainy", "hot", "cold"]}
                    ],
                    "quiz": [
                        {"question": "Where do we pray?", "options": ["School", "Market", "Mosque", "Farm"], "answer": "Mosque"},
                        {"question": "What is the weather when it rains?", "options": ["Sunny", "Rainy", "Cloudy", "Windy"], "answer": "Rainy"}
                    ]
                },
                "math": {
                    "lessons": [
                        {"title": "Addition up to 20", "content": "10+5=15, 12+3=15, 14+2=16, 11+8=19", "practice": "اجمع حتى 20"},
                        {"title": "Subtraction up to 20", "content": "15-3=12, 18-4=14, 20-5=15, 17-7=10", "practice": "اطرح حتى 20"}
                    ],
                    "quiz": [
                        {"question": "12 + 5 = ?", "options": ["15", "16", "17", "18"], "answer": "17"},
                        {"question": "18 - 6 = ?", "options": ["10", "11", "12", "13"], "answer": "12"}
                    ]
                }
            }
        }
    },
    "p1": {
        "name": t("p1"),
        "terms": {
            1: {"title": t("term1"), "lessons": [{"title": "مقدمة", "content": "نفس هيكل KG لكن بمستوى أعلى"}]},
            2: {"title": t("term2"), "lessons": []},
            3: {"title": t("term3"), "lessons": []},
            4: {"title": t("term4"), "lessons": []}
        }
    },
    "p2": {
        "name": t("p2"),
        "terms": {
            1: {"title": t("term1"), "lessons": []},
            2: {"title": t("term2"), "lessons": []},
            3: {"title": t("term3"), "lessons": []},
            4: {"title": t("term4"), "lessons": []}
        }
    }
}

# ==================== واجهة التطبيق ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== اختيار المرحلة ====================
st.markdown(f"### {t('select_level')}")
col1, col2, col3 = st.columns(3)
levels = {"kg": t("kg"), "p1": t("p1"), "p2": t("p2")}
for i, (key, name) in enumerate(levels.items()):
    with [col1, col2, col3][i]:
        if st.button(name, use_container_width=True):
            st.session_state.level = key
            st.session_state.term = 1
            st.session_state.subject = "islamic"
            st.rerun()

# ==================== اختيار المادة والفصل ====================
st.markdown(f"### {t('select_subject')}")
col1, col2, col3 = st.columns(3)
subjects = {"islamic": t("islamic"), "english": t("english"), "math": t("math")}
for i, (key, name) in enumerate(subjects.items()):
    with [col1, col2, col3][i]:
        if st.button(name, use_container_width=True):
            st.session_state.subject = key
            st.rerun()

st.markdown(f"### {t('term')}")
col1, col2, col3, col4 = st.columns(4)
for i in range(1, 5):
    with [col1, col2, col3, col4][i-1]:
        if st.button(f"{t('term')} {i}", use_container_width=True):
            st.session_state.term = i
            st.rerun()

# ==================== عرض المحتوى ====================
st.markdown(f"## 📚 {t('lessons')} - {levels[st.session_state.level]} - {subjects[st.session_state.subject]} - {t('term')} {st.session_state.term}")

try:
    level_data = CURRICULUM[st.session_state.level]
    term_data = level_data["terms"][st.session_state.term]
    subject_data = term_data[st.session_state.subject]
    
    if "lessons" in subject_data and subject_data["lessons"]:
        for i, lesson in enumerate(subject_data["lessons"]):
            with st.expander(f"📖 {lesson['title']}"):
                st.markdown(lesson['content'])
                if "vocab" in lesson:
                    st.markdown("**📝 Vocabulary:** " + ", ".join(lesson['vocab']))
                if "keywords" in lesson:
                    st.markdown("**🔑 Keywords:** " + ", ".join(lesson['keywords']))
                if "translation" in lesson:
                    st.markdown(f"**📖 {t('meaning')}:** {lesson['translation']}")
                if "practice" in lesson:
                    st.markdown(f"**✏️ Practice:** {lesson['practice']}")
    else:
        st.info("📚 المزيد من الدروس قيد الإضافة...")
    
    # عرض الاختبار
    st.markdown(f"## 📝 {t('quiz')}")
    if "quiz" in subject_data and subject_data["quiz"]:
        if f"quiz_{st.session_state.level}_{st.session_state.subject}_{st.session_state.term}" not in st.session_state:
            st.session_state[f"quiz_{st.session_state.level}_{st.session_state.subject}_{st.session_state.term}"] = {}
        
        score = 0
        for i, q in enumerate(subject_data["quiz"]):
            st.markdown(f"**{i+1}. {q['question']}**")
            answer = st.radio("", q['options'], key=f"q_{i}", index=None)
            if answer:
                if answer == q['answer']:
                    st.markdown(f"<p class='correct'>✅ {t('correct')}</p>", unsafe_allow_html=True)
                    score += 1
                else:
                    st.markdown(f"<p class='wrong'>❌ {t('wrong')}</p>", unsafe_allow_html=True)
            st.markdown("---")
        
        st.markdown(f"### {t('my_score')}: {score}/{len(subject_data['quiz'])} {t('out_of')} {len(subject_data['quiz'])}")
        
        if score == len(subject_data['quiz']):
            st.balloons()
            st.success("🎉 ممتاز! أكملت الاختبار بنجاح!")
    else:
        st.info("📝 اختبارات قريباً...")
        
except KeyError:
    st.info("📚 المحتوى قيد الإعداد للمرحلة والفصل المختار...")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### 📚 {t('title')}")
    st.markdown(f"**{t('select_level')}:** {levels[st.session_state.level]}")
    st.markdown(f"**{t('select_subject')}:** {subjects[st.session_state.subject]}")
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
    
    st.markdown("---")
    st.markdown("### 📖 Short Surahs")
    st.markdown("- Al-Fatihah\n- Al-Ikhlas\n- Al-Falaq\n- An-Nas\n- Al-Kawthar")
    
    st.markdown("---")
    st.markdown("### 🤲 Daily Duas")
    st.markdown("- Upon waking up\n- Before eating\n- After eating\n- Entering toilet\n- Leaving toilet\n- Before sleeping")
