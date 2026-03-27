import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - الكتاب الإلكتروني التفاعلي",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تهيئة الجلسة ====================
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "student_level" not in st.session_state:
    st.session_state.student_level = "kg"
if "current_book" not in st.session_state:
    st.session_state.current_book = "islamic"
if "current_term" not in st.session_state:
    st.session_state.current_term = 1
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = 0
if "lesson_status" not in st.session_state:
    st.session_state.lesson_status = {}  # {"lesson_id": "not_started", "in_progress", "completed"}
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "language" not in st.session_state:
    st.session_state.language = "ar"

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "📚 Noor Al-Ma'rifa Interactive E-Book",
        "subtitle": "Islamic Education | English | Mathematics",
        "welcome": "Welcome to Your Interactive Book",
        "student_name": "Student Name",
        "student_level": "Grade",
        "kg": "Kindergarten (KG)",
        "p1": "Primary 1",
        "p2": "Primary 2",
        "islamic": "🕌 Islamic Education",
        "english": "📖 English",
        "math": "🔢 Mathematics",
        "term": "📅 Term",
        "lessons": "📚 Lessons",
        "lesson": "Lesson",
        "read": "📖 Read",
        "practice": "✍️ Practice",
        "project": "🎯 Project",
        "quiz": "📝 Quiz",
        "check": "✅ Check",
        "correct": "✅ Correct! Great job!",
        "wrong": "❌ Not quite. Try again!",
        "completed": "✅ Completed",
        "in_progress": "📖 In Progress",
        "not_started": "📚 Not Started",
        "score": "⭐ Score",
        "points": "points",
        "certificate": "🏆 Certificate",
        "project_desc": "🎯 **Project:** Complete the task below"
    },
    "ar": {
        "title": "📚 نور المعرفة – الكتاب الإلكتروني التفاعلي",
        "subtitle": "تربية إسلامية | لغة إنجليزية | رياضيات",
        "welcome": "مرحباً بك في كتابك التفاعلي",
        "student_name": "اسم الطالب",
        "student_level": "المرحلة",
        "kg": "رياض الأطفال (KG)",
        "p1": "الصف الأول",
        "p2": "الصف الثاني",
        "islamic": "🕌 التربية الإسلامية",
        "english": "📖 اللغة الإنجليزية",
        "math": "🔢 الرياضيات",
        "term": "📅 الفصل الدراسي",
        "lessons": "📚 الدروس",
        "lesson": "الدرس",
        "read": "📖 اقرأ",
        "practice": "✍️ تدرب",
        "project": "🎯 مشروع",
        "quiz": "📝 اختبر نفسك",
        "check": "✅ تحقق",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ إجابة خاطئة. حاول مرة أخرى!",
        "completed": "✅ مكتمل",
        "in_progress": "📖 قيد الدراسة",
        "not_started": "📚 لم يبدأ",
        "score": "⭐ درجتي",
        "points": "نقطة",
        "certificate": "🏆 شهادة إنجاز",
        "project_desc": "🎯 **المشروع:** أكمل المهمة التالية"
    },
    "sw": {
        "title": "📚 Noor Al-Ma'rifa Interactive E-Book",
        "subtitle": "Elimu ya Kiislamu | Kiingereza | Hisabati",
        "welcome": "Karibu Katika Kitabu Chako Shirikishi",
        "student_name": "Jina la Mwanafunzi",
        "student_level": "Darasa",
        "kg": "Darasa la Awali (KG)",
        "p1": "Darasa la Kwanza",
        "p2": "Darasa la Pili",
        "islamic": "🕌 Elimu ya Kiislamu",
        "english": "📖 Kiingereza",
        "math": "🔢 Hisabati",
        "term": "📅 Muhula",
        "lessons": "📚 Masomo",
        "lesson": "Somo",
        "read": "📖 Soma",
        "practice": "✍️ Fanya Mazoezi",
        "project": "🎯 Mradi",
        "quiz": "📝 Jaribu",
        "check": "✅ Angalia",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Jibu Sio Sahihi. Jaribu Tena!",
        "completed": "✅ Imekamilika",
        "in_progress": "📖 Inaendelea",
        "not_started": "📚 Haijaanza",
        "score": "⭐ Alama Yangu",
        "points": "alama",
        "certificate": "🏆 Cheti",
        "project_desc": "🎯 **Mradi:** Kamilisha kazi ifuatayo"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== المحتوى التعليمي (موسع) ====================
# هيكل: level -> book -> term -> lessons[]
lessons_data = {
    "kg": {
        "islamic": {
            1: [
                {"title": "أنا مسلم", "text": "🌟 أنا مسلم. ربي الله. نبينا محمد ﷺ.\n\n📖 **سورة الفاتحة**\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ...", 
                 "practice": {"type": "choice", "question": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "answer": "محمد"},
                 "project": "ارسم مسجداً واكتب تحته: 'أنا مسلم'"},
                {"title": "دعاء الاستيقاظ", "text": "🤲 **دعاء الاستيقاظ**\nالْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", 
                 "practice": {"type": "choice", "question": "ماذا نقول عند الاستيقاظ؟", "options": ["بسم الله", "الحمد لله", "سبحان الله", "الله أكبر"], "answer": "الحمد لله"},
                 "project": "احفظ الدعاء وردده كل صباح لمدة أسبوع"},
                {"title": "أركان الإسلام", "text": "🕋 **أركان الإسلام الخمسة**\n1. الشهادتان\n2. الصلاة\n3. الزكاة\n4. الصوم\n5. الحج", 
                 "practice": {"type": "choice", "question": "كم عدد أركان الإسلام؟", "options": ["3", "4", "5", "6"], "answer": "5"},
                 "project": "اكتب أركان الإسلام الخمسة في ورقة وعلقها في غرفتك"},
                {"title": "سورة الإخلاص", "text": "📖 **سورة الإخلاص**\nقُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", 
                 "practice": {"type": "choice", "question": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "answer": "4"},
                 "project": "اقرأ سورة الإخلاص 10 مرات واكتب فضلها"}
            ]
        },
        "english": {
            1: [
                {"title": "My Family", "text": "👨‍👩‍👧‍👦 **My Family**\n\nI have a father. 👨\nI have a mother. 👩\nI have brothers and sisters. 👧👦\n\n**New Words:** father, mother, brother, sister", 
                 "practice": {"type": "choice", "question": "Who is your father?", "options": ["My mother's husband", "My brother", "My teacher"], "answer": "My mother's husband"},
                 "project": "Draw your family and label each member in English"},
                {"title": "My Body", "text": "👁️ **My Body**\n\nI have eyes to see. 👁️\nI have ears to hear. 👂\nI have hands to clap. ✋\n\n**New Words:** eyes, ears, hands", 
                 "practice": {"type": "choice", "question": "What do we use to see?", "options": ["Ears", "Eyes", "Hands", "Feet"], "answer": "Eyes"},
                 "project": "Draw a person and label the body parts: eyes, ears, hands, feet"}
            ]
        },
        "math": {
            1: [
                {"title": "Counting 1-10", "text": "🔢 **Numbers 1 to 10**\n\n1️⃣ One\n2️⃣ Two\n3️⃣ Three\n4️⃣ Four\n5️⃣ Five\n6️⃣ Six\n7️⃣ Seven\n8️⃣ Eight\n9️⃣ Nine\n🔟 Ten", 
                 "practice": {"type": "choice", "question": "What number comes after 5?", "options": ["4", "6", "7", "8"], "answer": "6"},
                 "project": "Count 10 objects in your house (toys, spoons, books) and write their names"},
                {"title": "Addition", "text": "➕ **Addition**\n\n1 + 1 = 2\n2 + 2 = 4\n3 + 2 = 5\n\nAdding means putting together.", 
                 "practice": {"type": "choice", "question": "3 + 2 = ?", "options": ["4", "5", "6", "7"], "answer": "5"},
                 "project": "Use beans or stones to solve: 2+3, 4+1, 5+2"}
            ]
        }
    },
    "p1": {
        "islamic": {
            1: [
                {"title": "سورة الفاتحة", "text": "📖 **سورة الفاتحة**\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ...", 
                 "practice": {"type": "choice", "question": "كم عدد آيات سورة الفاتحة؟", "options": ["5", "6", "7", "8"], "answer": "7"},
                 "project": "اكتب سورة الفاتحة بخط جميل"}
            ]
        },
        "english": {
            1: [
                {"title": "Greetings", "text": "👋 **Greetings**\n\nGood morning! (صباح الخير)\nGood afternoon! (مساء الخير)\nGood evening! (مساء الخير)\nGood night! (تصبح على خير)", 
                 "practice": {"type": "choice", "question": "What do you say in the morning?", "options": ["Good night", "Good morning", "Goodbye", "Hello"], "answer": "Good morning"},
                 "project": "Practice greeting your family in English every morning"}
            ]
        },
        "math": {
            1: [
                {"title": "Numbers 1-50", "text": "🔢 **Numbers 1 to 50**\n\n1-10: 1 2 3 4 5 6 7 8 9 10\n11-20: 11 12 13 14 15 16 17 18 19 20...", 
                 "practice": {"type": "choice", "question": "What number comes after 29?", "options": ["28", "30", "31", "40"], "answer": "30"},
                 "project": "Write numbers from 1 to 50 in your notebook"}
            ]
        }
    },
    "p2": {
        "islamic": {
            1: [
                {"title": "سورة الكوثر", "text": "📖 **سورة الكوثر**\nإِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ\nفَصَلِّ لِرَبِّكَ وَانْحَرْ\nإِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", 
                 "practice": {"type": "choice", "question": "سورة الكوثر كم آية؟", "options": ["2", "3", "4", "5"], "answer": "3"},
                 "project": "احفظ سورة الكوثر واكتب معناها"}
            ]
        },
        "english": {
            1: [
                {"title": "My Day", "text": "⏰ **My Day**\n\nI wake up at 6 o'clock.\nI eat breakfast at 7 o'clock.\nI go to school at 8 o'clock.", 
                 "practice": {"type": "choice", "question": "What do you do in the morning?", "options": ["Sleep", "Wake up", "Play", "Eat dinner"], "answer": "Wake up"},
                 "project": "Write about your daily routine in English"}
            ]
        },
        "math": {
            1: [
                {"title": "Multiplication", "text": "✖️ **Multiplication Tables**\n\n2 × 1 = 2\n2 × 2 = 4\n2 × 3 = 6\n2 × 4 = 8\n2 × 5 = 10", 
                 "practice": {"type": "choice", "question": "3 × 4 = ?", "options": ["7", "10", "12", "15"], "answer": "12"},
                 "project": "Memorize multiplication tables for 2, 3, 4, 5"}
            ]
        }
    }
}

# ==================== دوال مساعدة ====================
def get_lesson_key(level, book, term, lesson_idx):
    return f"{level}_{book}_{term}_{lesson_idx}"

def get_lesson_status(lesson_key):
    return st.session_state.lesson_status.get(lesson_key, "not_started")

def update_lesson_status(lesson_key, status):
    st.session_state.lesson_status[lesson_key] = status
    if status == "completed":
        st.session_state.total_score += 10

def get_current_lesson():
    level = st.session_state.student_level
    book = st.session_state.current_book
    term = st.session_state.current_term
    lesson_idx = st.session_state.current_lesson
    
    try:
        lesson = lessons_data[level][book][term][lesson_idx]
        return lesson
    except (KeyError, IndexError):
        return None

def get_total_lessons():
    level = st.session_state.student_level
    book = st.session_state.current_book
    term = st.session_state.current_term
    try:
        return len(lessons_data[level][book][term])
    except (KeyError, IndexError):
        return 0

# ==================== واجهة التطبيق ====================
# تصميم الكتاب
st.markdown("""
<style>
    .book-cover {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .lesson-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-left: 5px solid #2ecc71;
    }
    .status-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    .sidebar-lesson {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .sidebar-lesson:hover {
        background: #f0f2f6;
    }
    .sidebar-lesson-active {
        background: #e8f5e9;
        border-left: 3px solid #2ecc71;
    }
    .project-box {
        background: #fff8e7;
        border: 2px dashed #f39c12;
        border-radius: 15px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# تسجيل الدخول
if not st.session_state.student_name:
    st.markdown(f"""
    <div class='book-cover'>
        <h1>📚 {t('title')}</h1>
        <p>{t('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(t("student_name"))
        level = st.selectbox(t("student_level"), ["kg", "p1", "p2"], format_func=lambda x: t(x))
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1674/1674083.png", width=150)
    
    if st.button("📖 افتح كتابي", type="primary", use_container_width=True):
        if name:
            st.session_state.student_name = name
            st.session_state.student_level = level
            st.rerun()
        else:
            st.warning("✏️ الرجاء إدخال اسم الطالب")

else:
    # رأس الكتاب
    st.markdown(f"""
    <div class='book-cover'>
        <h1>📚 {t('title')}</h1>
        <p>👋 {t('welcome')} {st.session_state.student_name}!</p>
        <p>⭐ {t('score')}: {st.session_state.total_score} {t('points')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي (الفهرس التفاعلي)
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.student_name}")
        st.markdown(f"**{t('score')}:** {st.session_state.total_score} ⭐")
        
        # اختيار المرحلة
        st.markdown(f"**📚 {t('student_level')}**")
        levels = {"kg": t("kg"), "p1": t("p1"), "p2": t("p2")}
        for key, name in levels.items():
            if st.button(name, use_container_width=True):
                st.session_state.student_level = key
                st.session_state.current_lesson = 0
                st.rerun()
        
        # اختيار المادة
        st.markdown(f"**📖 {t('islamic')} / {t('english')} / {t('math')}**")
        books = {"islamic": t("islamic"), "english": t("english"), "math": t("math")}
        for key, name in books.items():
            if st.button(name, use_container_width=True):
                st.session_state.current_book = key
                st.session_state.current_lesson = 0
                st.rerun()
        
        # اختيار الفصل
        st.markdown(f"**📅 {t('term')}**")
        col1, col2, col3, col4 = st.columns(4)
        for i in range(1, 5):
            with [col1, col2, col3, col4][i-1]:
                if st.button(f"{i}", use_container_width=True):
                    st.session_state.current_term = i
                    st.session_state.current_lesson = 0
                    st.rerun()
        
        st.markdown("---")
        st.markdown(f"### 📚 {t('lessons')}")
        
        # عرض قائمة الدروس مع الحالة
        total = get_total_lessons()
        for i in range(total):
            lesson_key = get_lesson_key(st.session_state.student_level, st.session_state.current_book, st.session_state.current_term, i)
            status = get_lesson_status(lesson_key)
            
            if status == "completed":
                icon = "✅"
            elif status == "in_progress":
                icon = "📖"
            else:
                icon = "📚"
            
            lesson_title = lessons_data[st.session_state.student_level][st.session_state.current_book][st.session_state.current_term][i]["title"][:20]
            
            # عرض الدرس في الشريط الجانبي
            if st.button(f"{icon} {lesson_title}", key=f"sidebar_lesson_{i}", use_container_width=True):
                st.session_state.current_lesson = i
                if status == "not_started":
                    update_lesson_status(lesson_key, "in_progress")
                st.rerun()
        
        # شريط التقدم
        st.markdown("---")
        completed = len([k for k, v in st.session_state.lesson_status.items() if v == "completed" and k.startswith(f"{st.session_state.student_level}_{st.session_state.current_book}_{st.session_state.current_term}_")])
        if total > 0:
            st.progress(completed / total)
            st.caption(f"{completed}/{total} {t('lessons')}")
        
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
    
    # عرض الدرس الحالي
    lesson = get_current_lesson()
    
    if lesson:
        lesson_key = get_lesson_key(st.session_state.student_level, st.session_state.current_book, st.session_state.current_term, st.session_state.current_lesson)
        current_status = get_lesson_status(lesson_key)
        
        # حالة الدرس
        status_text = {
            "completed": t("completed"),
            "in_progress": t("in_progress"),
            "not_started": t("not_started")
        }.get(current_status, t("not_started"))
        
        st.markdown(f"""
        <div class='lesson-card'>
            <h2>📖 {t('lesson')} {st.session_state.current_lesson + 1}: {lesson['title']}</h2>
            <p><span class='status-icon'>{'✅' if current_status == 'completed' else '📖'}</span> {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # عرض المحتوى
        st.markdown(f"### {t('read')}")
        st.markdown(f"<div style='background: #f0f2f6; padding: 1rem; border-radius: 10px;'>{lesson['text']}</div>", unsafe_allow_html=True)
        
        # التمرين
        if "practice" in lesson:
            st.markdown(f"### ✍️ {t('practice')}")
            ex = lesson["practice"]
            if ex["type"] == "choice":
                answer = st.radio(ex["question"], ex["options"], key=f"practice_{lesson_key}", index=None)
                if st.button(t("check"), key=f"check_{lesson_key}"):
                    if answer == ex["answer"]:
                        st.success(f"✅ {t('correct')}")
                        st.balloons()
                        if current_status != "completed":
                            update_lesson_status(lesson_key, "completed")
                            st.rerun()
                    else:
                        st.error(f"❌ {t('wrong')}")
                        st.info(f"💡 الإجابة الصحيحة: {ex['answer']}")
        
        # المشروع
        if "project" in lesson:
            st.markdown(f"""
            <div class='project-box'>
                {t('project_desc')}<br><br>
                📝 {lesson['project']}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ أكملت المشروع", key=f"project_{lesson_key}"):
                if current_status != "completed":
                    update_lesson_status(lesson_key, "completed")
                    st.success("🎉 أحسنت! لقد أكملت المشروع وحصلت على 10 نقاط!")
                    st.balloons()
                    st.rerun()
        
        # أزرار التنقل
        total_lessons = get_total_lessons()
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_lesson > 0:
                if st.button(t("prev"), use_container_width=True):
                    st.session_state.current_lesson -= 1
                    st.rerun()
        with col2:
            if st.session_state.current_lesson < total_lessons - 1:
                if st.button(t("next"), use_container_width=True):
                    st.session_state.current_lesson += 1
                    st.rerun()
    else:
        st.info("📚 المزيد من الدروس قيد الإضافة...")
    
    # شهادة الإنجاز
    total_lessons_all = sum([len(lessons_data[level][book][term]) for level in lessons_data for book in lessons_data[level] for term in lessons_data[level][book]])
    if len(st.session_state.lesson_status) >= total_lessons_all and all(v == "completed" for v in st.session_state.lesson_status.values()):
        st.markdown("---")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f9f3e3 0%, #fff5e6 100%); border: 10px double #e67e22; padding: 1.5rem; text-align: center; border-radius: 15px;'>
            <h2>🏆 {t('certificate')}</h2>
            <h3>{t('certificate_earned')}</h3>
            <p>{st.session_state.student_name}</p>
            <p>{t('score')}: {st.session_state.total_score} {t('points')}</p>
            <p>📅 {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)
