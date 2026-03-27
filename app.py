import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, timedelta
import random
import time
import base64

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - المدرسة الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تهيئة الجلسة ====================
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "student_age" not in st.session_state:
    st.session_state.student_age = ""
if "level" not in st.session_state:
    st.session_state.level = "kg"
if "term" not in st.session_state:
    st.session_state.term = 1
if "subject" not in st.session_state:
    st.session_state.subject = "islamic"
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = 0
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []
if "weekly_test_score" not in st.session_state:
    st.session_state.weekly_test_score = 0
if "certificates" not in st.session_state:
    st.session_state.certificates = []
if "language" not in st.session_state:
    st.session_state.language = "ar"
if "activity_completed" not in st.session_state:
    st.session_state.activity_completed = False

# ==================== ملفات التخزين ====================
DATA_FOLDER = "student_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PROGRESS_FILE = os.path.join(DATA_FOLDER, "progress.json")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "🎓 Noor Al-Ma'rifa Smart School",
        "subtitle": "Interactive Learning | Islamic Education | English | Mathematics",
        "welcome": "👋 Welcome! Let's start learning",
        "student_name": "Student Name",
        "student_age": "Age",
        "start": "🚀 Start Learning",
        "select_level": "📚 Select Grade",
        "kg": "🏫 Kindergarten (KG)",
        "p1": "📖 Primary 1",
        "p2": "📘 Primary 2",
        "select_subject": "📖 Subject",
        "islamic": "🕌 Islamic Education",
        "english": "📖 English",
        "math": "🔢 Mathematics",
        "term": "📅 Term",
        "term1": "Term 1",
        "term2": "Term 2",
        "term3": "Term 3",
        "term4": "Term 4",
        "lesson": "📚 Lesson",
        "activity": "🎨 Activity",
        "quiz": "📝 Quiz",
        "weekly_test": "📊 Weekly Test",
        "certificate": "🏆 Certificate",
        "my_progress": "📈 My Progress",
        "score": "⭐ Score",
        "points": "points",
        "correct": "✅ Correct! Great job!",
        "wrong": "❌ Not quite. Try again!",
        "well_done": "🎉 Well done! You completed the lesson!",
        "certificate_earned": "🏆 Congratulations! You earned a certificate!",
        "download_certificate": "📥 Download Certificate",
        "activity_coloring": "🎨 Coloring Activity",
        "activity_counting": "🔢 Counting Activity",
        "activity_writing": "✍️ Writing Practice",
        "story_time": "📖 Story Time"
    },
    "ar": {
        "title": "🎓 نور المعرفة – المدرسة الذكية",
        "subtitle": "تعليم تفاعلي | تربية إسلامية | لغة إنجليزية | رياضيات",
        "welcome": "👋 مرحباً! دعنا نبدأ التعلم",
        "student_name": "اسم الطالب",
        "student_age": "العمر",
        "start": "🚀 ابدأ التعلم",
        "select_level": "📚 اختر المرحلة",
        "kg": "🏫 رياض الأطفال (KG)",
        "p1": "📖 الصف الأول",
        "p2": "📘 الصف الثاني",
        "select_subject": "📖 المادة",
        "islamic": "🕌 التربية الإسلامية",
        "english": "📖 اللغة الإنجليزية",
        "math": "🔢 الرياضيات",
        "term": "📅 الفصل الدراسي",
        "term1": "الفصل الأول",
        "term2": "الفصل الثاني",
        "term3": "الفصل الثالث",
        "term4": "الفصل الرابع",
        "lesson": "📚 الدرس",
        "activity": "🎨 نشاط",
        "quiz": "📝 اختبار",
        "weekly_test": "📊 اختبار أسبوعي",
        "certificate": "🏆 شهادة",
        "my_progress": "📈 تقدمي",
        "score": "⭐ درجتي",
        "points": "نقطة",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ إجابة خاطئة. حاول مرة أخرى!",
        "well_done": "🎉 ممتاز! لقد أكملت الدرس!",
        "certificate_earned": "🏆 مبروك! حصلت على شهادة!",
        "download_certificate": "📥 تحميل الشهادة",
        "activity_coloring": "🎨 نشاط تلوين",
        "activity_counting": "🔢 نشاط عد",
        "activity_writing": "✍️ تدريب الكتابة",
        "story_time": "📖 وقت القصة"
    },
    "sw": {
        "title": "🎓 Noor Al-Ma'rifa Smart School",
        "subtitle": "Kujifunza Shirikishi | Kiislamu | Kiingereza | Hisabati",
        "welcome": "👋 Karibu! Tuanze kujifunza",
        "student_name": "Jina la Mwanafunzi",
        "student_age": "Umri",
        "start": "🚀 Anza Kujifunza",
        "select_level": "📚 Chagua Darasa",
        "kg": "🏫 Darasa la Awali (KG)",
        "p1": "📖 Darasa la Kwanza",
        "p2": "📘 Darasa la Pili",
        "select_subject": "📖 Somo",
        "islamic": "🕌 Elimu ya Kiislamu",
        "english": "📖 Kiingereza",
        "math": "🔢 Hisabati",
        "term": "📅 Muhula",
        "term1": "Muhula wa 1",
        "term2": "Muhula wa 2",
        "term3": "Muhula wa 3",
        "term4": "Muhula wa 4",
        "lesson": "📚 Somo",
        "activity": "🎨 Shughuli",
        "quiz": "📝 Mtihani",
        "weekly_test": "📊 Mtihani wa Wiki",
        "certificate": "🏆 Cheti",
        "my_progress": "📈 Maendeleo Yangu",
        "score": "⭐ Alama Yangu",
        "points": "alama",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Jibu Sio Sahihi. Jaribu Tena!",
        "well_done": "🎉 Umefanya Vizuri! Umemaliza somo!",
        "certificate_earned": "🏆 Hongera! Umepata cheti!",
        "download_certificate": "📥 Pakua Cheti",
        "activity_coloring": "🎨 Shughuli ya Kupaka Rangi",
        "activity_counting": "🔢 Shughuli ya Kuhesabu",
        "activity_writing": "✍️ Mazoezi ya Kuandika",
        "story_time": "📖 Wakati wa Hadithi"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== المحتوى التعليمي الكامل ====================
content = {
    "kg": {
        "islamic": {
            1: {
                "title": "أنا مسلم وسورة الفاتحة",
                "text": """🌟 **أنا مسلم**

أنا مسلم. ربي الله. نبينا محمد ﷺ. ديننا الإسلام.

📖 **سورة الفاتحة**
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
الرَّحْمَٰنِ الرَّحِيمِ
مَالِكِ يَوْمِ الدِّينِ
إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ
صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ

🤲 **دعاء الاستيقاظ**
الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ""",
                "quiz": [
                    {"q": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "a": "محمد"},
                    {"q": "كم عدد آيات سورة الفاتحة؟", "options": ["5", "6", "7", "8"], "a": "7"},
                    {"q": "ماذا نقول عند الاستيقاظ؟", "options": ["بسم الله", "الحمد لله", "سبحان الله", "الله أكبر"], "a": "الحمد لله"}
                ]
            },
            2: {
                "title": "أركان الإسلام وسورة الإخلاص",
                "text": """🕋 **أركان الإسلام الخمسة**

1. الشهادتان
2. إقام الصلاة
3. إيتاء الزكاة
4. صوم رمضان
5. حج البيت

📖 **سورة الإخلاص**
قُلْ هُوَ اللَّهُ أَحَدٌ
اللَّهُ الصَّمَدُ
لَمْ يَلِدْ وَلَمْ يُولَدْ
وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ

🤲 **دعاء دخول الخلاء**
اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ""",
                "quiz": [
                    {"q": "كم عدد أركان الإسلام؟", "options": ["3", "4", "5", "6"], "a": "5"},
                    {"q": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "a": "4"},
                    {"q": "ما هو الركن الثالث من أركان الإسلام؟", "options": ["الصلاة", "الزكاة", "الصوم", "الحج"], "a": "الزكاة"}
                ]
            },
            3: {
                "title": "أركان الإيمان وسورة الفلق",
                "text": """⭐ **أركان الإيمان الستة**

1. الإيمان بالله
2. الإيمان بالملائكة
3. الإيمان بالكتب
4. الإيمان بالرسل
5. الإيمان باليوم الآخر
6. الإيمان بالقدر خيره وشره

📖 **سورة الفلق**
قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ
مِن شَرِّ مَا خَلَقَ
وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ
وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ
وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ

🤲 **دعاء الأكل**
بِسْمِ اللَّهِ وَبَرَكَةِ اللَّهِ""",
                "quiz": [
                    {"q": "كم عدد أركان الإيمان؟", "options": ["4", "5", "6", "7"], "a": "6"},
                    {"q": "سورة الفلق تحمي من؟", "options": ["المرض", "الحسد", "الفقر", "الجهل"], "a": "الحسد"},
                    {"q": "ماذا نقول قبل الأكل؟", "options": ["الحمد لله", "بسم الله", "سبحان الله", "الله أكبر"], "a": "بسم الله"}
                ]
            },
            4: {
                "title": "الوضوء وسورة الناس",
                "text": """💧 **خطوات الوضوء**

1. نية الوضوء
2. غسل الكفين
3. المضمضة والاستنشاق
4. غسل الوجه
5. غسل اليدين إلى المرفقين
6. مسح الرأس والأذنين
7. غسل الرجلين إلى الكعبين

📖 **سورة الناس**
قُلْ أَعُوذُ بِرَبِّ النَّاسِ
مَلِكِ النَّاسِ
إِلَٰهِ النَّاسِ
مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ
الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ
مِنَ الْجِنَّةِ وَالنَّاسِ

🤲 **دعاء النوم**
بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا""",
                "quiz": [
                    {"q": "كم عدد فروض الوضوء؟", "options": ["4", "5", "6", "7"], "a": "6"},
                    {"q": "سورة الناس تحمي من؟", "options": ["المرض", "الوسواس", "الفقر", "الجهل"], "a": "الوسواس"},
                    {"q": "ماذا نقول عند النوم؟", "options": ["بسم الله", "اللهم إني أعوذ بك", "باسمك اللهم أموت وأحيا", "الحمد لله"], "a": "باسمك اللهم أموت وأحيا"}
                ]
            }
        },
        "english": {
            1: {"title": "My Family", "text": "I have a father. I have a mother. I have brothers and sisters.", "quiz": [{"q": "Who is your father?", "options": ["My mother's husband", "My brother", "My teacher", "My friend"], "a": "My mother's husband"}]},
            2: {"title": "My Body", "text": "I have eyes to see. I have ears to hear. I have hands to clap.", "quiz": [{"q": "What do we use to see?", "options": ["Ears", "Eyes", "Hands", "Feet"], "a": "Eyes"}]},
            3: {"title": "Animals", "text": "Cow, Goat, Sheep, Chicken, Dog, Cat", "quiz": [{"q": "What animal gives milk?", "options": ["Chicken", "Cow", "Dog", "Cat"], "a": "Cow"}]},
            4: {"title": "Fruits", "text": "Banana, Mango, Orange, Apple", "quiz": [{"q": "What fruit is yellow?", "options": ["Apple", "Orange", "Banana", "Mango"], "a": "Banana"}]}
        },
        "math": {
            1: {"title": "Counting 1-10", "text": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "quiz": [{"q": "What is after 5?", "options": ["4", "6", "7", "8"], "a": "6"}]},
            2: {"title": "Addition", "text": "1+1=2, 2+2=4, 3+2=5", "quiz": [{"q": "3 + 2 = ?", "options": ["4", "5", "6", "7"], "a": "5"}]},
            3: {"title": "Numbers 11-20", "text": "11,12,13,14,15,16,17,18,19,20", "quiz": [{"q": "What is after 15?", "options": ["14", "16", "17", "18"], "a": "16"}]},
            4: {"title": "Addition up to 20", "text": "10+5=15, 12+3=15", "quiz": [{"q": "12 + 5 = ?", "options": ["15", "16", "17", "18"], "a": "17"}]}
        }
    },
    "p1": {"islamic": {}, "english": {}, "math": {}},
    "p2": {"islamic": {}, "english": {}, "math": {}}
}

# ==================== أنشطة تفاعلية ====================
def coloring_activity():
    st.markdown("### 🎨 " + t("activity_coloring"))
    st.markdown("📝 ارسم ولوّن الشكل التالي:")
    st.markdown("""
    <div style='border: 2px dashed #2ecc71; padding: 2rem; text-align: center; background: #f9f9f9; border-radius: 15px;'>
        <h1 style='font-size: 5rem;'>☀️</h1>
        <p>🌞 ارسم شمساً جميلة</p>
        <p>🎨 لوّنها باللون الأصفر</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✅ أنجزت النشاط", use_container_width=True):
        st.session_state.activity_completed = True
        st.success("🎨 أحسنت! نشاط التلوين مكتمل!")
        st.balloons()

def counting_activity():
    st.markdown("### 🔢 " + t("activity_counting"))
    st.markdown("🔢 عدّ الأشياء التالية:")
    
    items = ["🍎", "🍌", "🍊", "🍇", "🍒"]
    random.shuffle(items)
    
    for i, item in enumerate(items[:3]):
        st.markdown(f"{item} {item} {item}")
    
    answer = st.number_input("كم عدد التفاح؟", min_value=0, max_value=10, step=1)
    if st.button("تحقق"):
        if answer == 3:
            st.success("✅ إجابة صحيحة! 3 تفاحات")
            st.session_state.activity_completed = True
        else:
            st.error("❌ حاول مرة أخرى. عدّ التفاحات")

def writing_activity():
    st.markdown("### ✍️ " + t("activity_writing"))
    st.markdown("📝 اكتب الكلمة التالية:")
    
    words = ["الله", "محمد", "أمي", "أبي", "شمس", "قمر"]
    word = random.choice(words)
    
    st.markdown(f"<h1 style='text-align: center;'>{word}</h1>", unsafe_allow_html=True)
    st.text_area("اكتب الكلمة هنا:", key="writing_input", height=100)
    if st.button("تحقق من الكتابة"):
        st.success("✍️ أحسنت! واصل التدريب")

def story_time():
    st.markdown("### 📖 " + t("story_time"))
    
    stories = [
        {"title": "قصة النبي محمد ﷺ", "content": "ولد النبي محمد ﷺ في مكة المكرمة. كان صادقاً أميناً. دعا الناس إلى عبادة الله الواحد الأحد."},
        {"title": "قصة إبراهيم عليه السلام", "content": "كان إبراهيم عليه السلام يبحث عن الله. رأى نجماً فقال: هذا ربي. فلما أفل قال: لا أحب الآفلين."},
        {"title": "قصة موسى عليه السلام", "content": "ولد موسى عليه السلام في زمن فرعون. ألقته أمه في اليم فالتقطه آل فرعون."}
    ]
    
    story = random.choice(stories)
    st.markdown(f"### {story['title']}")
    st.markdown(f"<div style='background: #f0f2f6; padding: 1rem; border-radius: 15px;'>{story['content']}</div>", unsafe_allow_html=True)

# ==================== واجهة التطبيق ====================
# تصميم مدرسي
st.markdown("""
<style>
    .school-board {
        background: #2c3e50;
        padding: 2rem;
        border-radius: 15px;
        color: #f1c40f;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Courier New', monospace;
    }
    .notebook {
        background: #fff8e7;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #e67e22;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .certificate {
        background: linear-gradient(135deg, #f9f3e3 0%, #fff5e6 100%);
        border: 10px double #e67e22;
        padding: 1.5rem;
        text-align: center;
        border-radius: 15px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# تسجيل الدخول (تسجيل الطالب)
if not st.session_state.student_name:
    st.markdown(f"""
    <div class='school-board'>
        <h1>🎓 {t('title')}</h1>
        <p>{t('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(t("student_name"))
        age = st.text_input(t("student_age"))
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1674/1674083.png", width=150)
    
    if st.button(t("start"), type="primary", use_container_width=True):
        if name:
            st.session_state.student_name = name
            st.session_state.student_age = age
            # تحميل التقدم السابق
            progress = load_progress()
            if name in progress:
                st.session_state.total_score = progress[name].get("score", 0)
                st.session_state.completed_lessons = progress[name].get("completed", [])
            st.rerun()
        else:
            st.warning("✏️ الرجاء إدخال اسم الطالب")

else:
    # الواجهة الرئيسية
    st.markdown(f"""
    <div class='school-board'>
        <h1>🎓 {t('title')}</h1>
        <p>👋 {t('welcome')} {st.session_state.student_name}!</p>
        <p>⭐ {t('score')}: {st.session_state.total_score} {t('points')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.student_name}")
        st.markdown(f"**{t('score')}:** {st.session_state.total_score} ⭐")
        
        # اختيار المرحلة
        st.markdown(f"**{t('select_level')}**")
        levels = {"kg": "KG", "p1": "P1", "p2": "P2"}
        for key, name in levels.items():
            if st.button(name, use_container_width=True):
                st.session_state.level = key
                st.session_state.current_lesson = 0
                st.rerun()
        
        # اختيار المادة
        st.markdown(f"**{t('select_subject')}**")
        subjects = {"islamic": "🕌", "english": "📖", "math": "🔢"}
        for key, icon in subjects.items():
            if st.button(f"{icon} {t(key)}", use_container_width=True):
                st.session_state.subject = key
                st.session_state.current_lesson = 0
                st.rerun()
        
        # اختيار الفصل
        st.markdown(f"**{t('term')}**")
        col1, col2, col3, col4 = st.columns(4)
        for i in range(1, 5):
            with [col1, col2, col3, col4][i-1]:
                if st.button(f"{i}", use_container_width=True):
                    st.session_state.term = i
                    st.session_state.current_lesson = 0
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🌍 Language")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬🇧 EN", use_container_width=True):
                st.session_state.language = "en"
                st.rerun()
        with col2:
            if st.button("🇸🇦 AR", use_container_width=True):
                st.session_state.language = "ar"
                st.rerun()
        
        # شريط التقدم
        st.markdown("---")
        st.markdown(f"### {t('my_progress')}")
        progress_percent = (len(st.session_state.completed_lessons) / 16) * 100 if st.session_state.completed_lessons else 0
        st.progress(progress_percent / 100)
        st.caption(f"{len(st.session_state.completed_lessons)}/16 {t('lessons')}")
    
    # المحتوى الرئيسي
    try:
        level_data = content.get(st.session_state.level, {})
        subject_data = level_data.get(st.session_state.subject, {})
        lesson_data = subject_data.get(st.session_state.term, {})
        
        if lesson_data:
            # أزرار التنقل
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.session_state.current_lesson > 0:
                    if st.button(t('prev'), use_container_width=True):
                        st.session_state.current_lesson -= 1
                        st.rerun()
            with col3:
                if st.session_state.current_lesson < 3:
                    if st.button(t('next'), use_container_width=True):
                        st.session_state.current_lesson += 1
                        st.rerun()
            
            # عرض الدرس (بشكل كراسة)
            st.markdown(f"""
            <div class='notebook'>
                <h2>📚 {t('lesson')} {st.session_state.current_lesson + 1}: {lesson_data.get('title', '')}</h2>
                <div style='font-size: 1.1rem; line-height: 1.8;'>
                    {lesson_data.get('text', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # اختبار الدرس
            if "quiz" in lesson_data:
                st.markdown(f"### 📝 {t('quiz')}")
                
                lesson_id = f"{st.session_state.level}_{st.session_state.subject}_{st.session_state.term}_{st.session_state.current_lesson}"
                lesson_completed = lesson_id in st.session_state.completed_lessons
                
                if not lesson_completed:
                    score = 0
                    for i, q in enumerate(lesson_data["quiz"]):
                        st.markdown(f"**{i+1}. {q['q']}**")
                        answer = st.radio("", q['options'], key=f"q_{i}_{st.session_state.current_lesson}", index=None)
                        if answer and answer == q['a']:
                            st.markdown(f"<p style='color: green;'>✅ {t('correct')}</p>", unsafe_allow_html=True)
                            score += 1
                        elif answer:
                            st.markdown(f"<p style='color: red;'>❌ {t('wrong')}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                    
                    if st.button("📝 إنهاء الاختبار", use_container_width=True):
                        if score == len(lesson_data["quiz"]):
                            st.success(f"🎉 {t('well_done')}")
                            st.balloons()
                            st.session_state.total_score += 10
                            st.session_state.completed_lessons.append(lesson_id)
                            # حفظ التقدم
                            progress = load_progress()
                            progress[st.session_state.student_name] = {
                                "score": st.session_state.total_score,
                                "completed": st.session_state.completed_lessons,
                                "date": datetime.now().isoformat()
                            }
                            save_progress(progress)
                            st.rerun()
                        else:
                            st.warning("📚 حاول مرة أخرى. أعد قراءة الدرس ثم اختبر نفسك")
                else:
                    st.success("✅ لقد أكملت هذا الدرس بالفعل!")
            
            # أنشطة تفاعلية
            st.markdown("---")
            tab1, tab2, tab3, tab4 = st.tabs([t("activity"), t("quiz"), t("weekly_test"), t("story_time")])
            
            with tab1:
                activity_type = random.choice(["coloring", "counting", "writing"])
                if activity_type == "coloring":
                    coloring_activity()
                elif activity_type == "counting":
                    counting_activity()
                else:
                    writing_activity()
            
            with tab2:
                st.markdown("### 📝 " + t("quiz"))
                if "quiz" in lesson_data:
                    st.info("📝 الاختبار موجود في أعلى الصفحة")
                else:
                    st.info("📝 اختبارات قريباً...")
            
            with tab3:
                st.markdown(f"### 📊 {t('weekly_test')}")
                st.info("📊 اختبار أسبوعي: يجمع كل دروس الفصل")
                if st.button("بدء الاختبار الأسبوعي", use_container_width=True):
                    st.warning("📝 قريباً...")
            
            with tab4:
                story_time()
            
            # شهادة إنجاز
            if len(st.session_state.completed_lessons) >= 16:
                st.markdown("---")
                st.markdown(f"""
                <div class='certificate'>
                    <h2>🏆 {t('certificate')}</h2>
                    <h3>{t('certificate_earned')}</h3>
                    <p>{st.session_state.student_name}</p>
                    <p>{t('score')}: {st.session_state.total_score} {t('points')}</p>
                    <p>📅 {datetime.now().strftime('%Y-%m-%d')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(t("download_certificate"), use_container_width=True):
                    st.success("📥 تم تحميل الشهادة (سيتم تفعيلها قريباً)")
        
        else:
            st.info("📚 المزيد من الدروس قيد الإضافة...")
            
    except Exception as e:
        st.info("🎓 اختر المرحلة والمادة والفصل لبدء التعلم")
