import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random
import time
import base64

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - الكتاب التفاعلي المتقدم",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تهيئة الجلسة ====================
if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())[:8]
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
    st.session_state.lesson_status = {}
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "certificates" not in st.session_state:
    st.session_state.certificates = []
if "language" not in st.session_state:
    st.session_state.language = "ar"
if "code_editor_content" not in st.session_state:
    st.session_state.code_editor_content = "print('Hello, World!')"
if "code_output" not in st.session_state:
    st.session_state.code_output = ""

# ==================== ملفات التخزين (Google Sheets API بديل) ====================
DATA_FOLDER = "student_progress"
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

# تحميل التقدم السابق للطالب
def load_student_progress():
    progress = load_progress()
    if st.session_state.student_id in progress:
        data = progress[st.session_state.student_id]
        st.session_state.lesson_status = data.get("lesson_status", {})
        st.session_state.total_score = data.get("total_score", 0)
        st.session_state.certificates = data.get("certificates", [])

def save_student_progress():
    progress = load_progress()
    progress[st.session_state.student_id] = {
        "student_name": st.session_state.student_name,
        "student_level": st.session_state.student_level,
        "lesson_status": st.session_state.lesson_status,
        "total_score": st.session_state.total_score,
        "certificates": st.session_state.certificates,
        "last_updated": datetime.now().isoformat()
    }
    save_progress(progress)

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "📚 Noor Al-Ma'rifa Advanced Interactive Book",
        "subtitle": "Learn Programming | Islamic Education | English | Mathematics",
        "welcome": "Welcome to Your Advanced Interactive Book",
        "student_name": "Student Name",
        "student_level": "Grade",
        "kg": "Kindergarten (KG)",
        "p1": "Primary 1",
        "p2": "Primary 2",
        "islamic": "🕌 Islamic Education",
        "english": "📖 English",
        "math": "🔢 Mathematics",
        "programming": "💻 Programming",
        "term": "📅 Term",
        "lessons": "📚 Lessons",
        "lesson": "Lesson",
        "read": "📖 Read",
        "code_editor": "💻 Code Editor",
        "practice": "✍️ Practice",
        "project": "🎯 Project",
        "quiz": "📝 Quiz",
        "run_code": "▶️ Run Code",
        "check": "✅ Check",
        "correct": "✅ Correct! Great job!",
        "wrong": "❌ Not quite. Try again!",
        "completed": "✅ Completed",
        "in_progress": "📖 In Progress",
        "not_started": "📚 Not Started",
        "score": "⭐ Score",
        "points": "points",
        "certificate": "🏆 Certificate",
        "project_desc": "🎯 **Project:** Complete the task below",
        "code_output": "📤 Output",
        "write_code": "✍️ Write your code here:"
    },
    "ar": {
        "title": "📚 نور المعرفة – الكتاب التفاعلي المتقدم",
        "subtitle": "تعلم البرمجة | تربية إسلامية | لغة إنجليزية | رياضيات",
        "welcome": "مرحباً بك في كتابك التفاعلي المتقدم",
        "student_name": "اسم الطالب",
        "student_level": "المرحلة",
        "kg": "رياض الأطفال (KG)",
        "p1": "الصف الأول",
        "p2": "الصف الثاني",
        "islamic": "🕌 التربية الإسلامية",
        "english": "📖 اللغة الإنجليزية",
        "math": "🔢 الرياضيات",
        "programming": "💻 البرمجة",
        "term": "📅 الفصل الدراسي",
        "lessons": "📚 الدروس",
        "lesson": "الدرس",
        "read": "📖 اقرأ",
        "code_editor": "💻 محرر الأكواد",
        "practice": "✍️ تدرب",
        "project": "🎯 مشروع",
        "quiz": "📝 اختبر نفسك",
        "run_code": "▶️ تشغيل الكود",
        "check": "✅ تحقق",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ إجابة خاطئة. حاول مرة أخرى!",
        "completed": "✅ مكتمل",
        "in_progress": "📖 قيد الدراسة",
        "not_started": "📚 لم يبدأ",
        "score": "⭐ درجتي",
        "points": "نقطة",
        "certificate": "🏆 شهادة إنجاز",
        "project_desc": "🎯 **المشروع:** أكمل المهمة التالية",
        "code_output": "📤 المخرجات",
        "write_code": "✍️ اكتب الكود هنا:"
    },
    "sw": {
        "title": "📚 Noor Al-Ma'rifa Advanced Interactive Book",
        "subtitle": "Jifunze Programu | Kiislamu | Kiingereza | Hisabati",
        "welcome": "Karibu Katika Kitabu Chako Cha Maingiliano",
        "student_name": "Jina la Mwanafunzi",
        "student_level": "Darasa",
        "kg": "Darasa la Awali (KG)",
        "p1": "Darasa la Kwanza",
        "p2": "Darasa la Pili",
        "islamic": "🕌 Elimu ya Kiislamu",
        "english": "📖 Kiingereza",
        "math": "🔢 Hisabati",
        "programming": "💻 Programu",
        "term": "📅 Muhula",
        "lessons": "📚 Masomo",
        "lesson": "Somo",
        "read": "📖 Soma",
        "code_editor": "💻 Kihariri cha Msimbo",
        "practice": "✍️ Fanya Mazoezi",
        "project": "🎯 Mradi",
        "quiz": "📝 Jaribu",
        "run_code": "▶️ Endesha Msimbo",
        "check": "✅ Angalia",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Jibu Sio Sahihi. Jaribu Tena!",
        "completed": "✅ Imekamilika",
        "in_progress": "📖 Inaendelea",
        "not_started": "📚 Haijaanza",
        "score": "⭐ Alama Yangu",
        "points": "alama",
        "certificate": "🏆 Cheti",
        "project_desc": "🎯 **Mradi:** Kamilisha kazi ifuatayo",
        "code_output": "📤 Matokeo",
        "write_code": "✍️ Andika msimbo wako hapa:"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== المحتوى التعليمي (موسع مع مشاريع برمجية) ====================
lessons_data = {
    "kg": {
        "islamic": {
            1: [
                {"title": "أنا مسلم", "text": "🌟 أنا مسلم. ربي الله. نبينا محمد ﷺ.\n\n📖 **سورة الفاتحة**\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ...", 
                 "practice": {"type": "choice", "question": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "answer": "محمد"},
                 "project": "ارسم مسجداً واكتب تحته: 'أنا مسلم'"},
                {"title": "دعاء الاستيقاظ", "text": "🤲 **دعاء الاستيقاظ**\nالْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", 
                 "practice": {"type": "choice", "question": "ماذا نقول عند الاستيقاظ؟", "options": ["بسم الله", "الحمد لله", "سبحان الله", "الله أكبر"], "answer": "الحمد لله"},
                 "project": "احفظ الدعاء وردده كل صباح لمدة أسبوع"}
            ]
        },
        "programming": {
            1: [
                {"title": "Hello, World!", "text": "💻 **أول برنامج لك**\n\nفي البرمجة، أول برنامج نتعلمه هو برنامج Hello, World!\n\n```python\nprint('Hello, World!')\n```\n\nهذا البرنامج يطبع كلمة Hello, World! على الشاشة.\n\n**جرب بنفسك في محرر الأكواد أدناه!**", 
                 "practice": {"type": "code", "task": "اطبع جملة 'Hello, World!'", "expected_output": "Hello, World!"},
                 "project": "اطبع اسمك 3 مرات باستخدام print()"},
                {"title": "المتغيرات", "text": "📦 **المتغيرات (Variables)**\n\nالمتغيرات是用来保存数据的.\n\n```python\nname = 'أحمد'\nage = 7\nprint(name)\nprint(age)\n```\n\n**جرب تغيير الاسم والعمر!**", 
                 "practice": {"type": "code", "task": "أنشئ متغيراً باسم 'city' واطبعه", "expected_output": "", "check_type": "variable"},
                 "project": "أنشئ متغيرات لاسمك، عمرك، مدينتك واطبعها"}
            ]
        }
    },
    "p1": {
        "programming": {
            1: [
                {"title": "العمليات الحسابية", "text": "➕ **العمليات الحسابية**\n\n```python\na = 5\nb = 3\nprint(a + b)  # جمع\nprint(a - b)  # طرح\nprint(a * b)  # ضرب\n```\n\n**جرب تغيير الأرقام!**", 
                 "practice": {"type": "code", "task": "احسب 10 + 5 واطبع الناتج", "expected_output": "15"},
                 "project": "اكتب برنامجاً يحسب مساحة المستطيل (الطول × العرض)"}
            ]
        }
    },
    "p2": {
        "programming": {
            1: [
                {"title": "الجمل الشرطية", "text": "⚡ **الجمل الشرطية (if/else)**\n\n```python\nage = 10\nif age >= 7:\n    print('يمكنك الذهاب إلى المدرسة')\nelse:\n    print('أنت صغير جداً')\n```\n\n**جرب تغيير العمر!**", 
                 "practice": {"type": "code", "task": "اكتب برنامجاً يطبع 'كبير' إذا كان العمر أكبر من 10، و'صغير' إذا كان أقل", "expected_output": "", "check_type": "conditional"},
                 "project": "اكتب برنامجاً يطلب رقمين ويطبع أكبرها"}
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
        save_student_progress()

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

def run_python_code(code):
    """تنفيذ كود بايثون بأمان"""
    try:
        # إعادة توجيه المخرجات
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        exec(code)
        
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        return output, None
    except Exception as e:
        return "", str(e)

def check_code_answer(user_code, expected_output):
    """التحقق من صحة الكود"""
    output, error = run_python_code(user_code)
    if error:
        return False, f"خطأ: {error}"
    if expected_output and expected_output.strip() != output.strip():
        return False, f"المخرج المتوقع: '{expected_output}'\nالمخرج الذي حصلت عليه: '{output}'"
    return True, "صحيح!"

# ==================== واجهة التطبيق ====================
# تصميم الكتاب المتقدم
st.markdown("""
<style>
    .book-cover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border-left: 5px solid #667eea;
    }
    .code-editor {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    .code-editor textarea {
        background: #1e1e1e;
        color: #d4d4d4;
        font-family: 'Courier New', monospace;
        border: none;
        width: 100%;
        height: 200px;
        padding: 10px;
    }
    .code-output {
        background: #2d2d2d;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-family: 'Courier New', monospace;
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
        border-left: 3px solid #667eea;
    }
    .project-box {
        background: #fff8e7;
        border: 2px dashed #f39c12;
        border-radius: 15px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .certificate-box {
        background: linear-gradient(135deg, #f9f3e3 0%, #fff5e6 100%);
        border: 10px double #e67e22;
        padding: 1.5rem;
        text-align: center;
        border-radius: 15px;
        margin: 1rem 0;
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
            load_student_progress()
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
        <p>🆔 معرف الطالب: {st.session_state.student_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
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
                save_student_progress()
                st.rerun()
        
        # اختيار المادة
        st.markdown(f"**📖 {t('islamic')} / {t('english')} / {t('math')} / 💻 {t('programming')}**")
        books = {"islamic": t("islamic"), "english": t("english"), "math": t("math"), "programming": t("programming")}
        for key, name in books.items():
            if st.button(name, use_container_width=True):
                st.session_state.current_book = key
                st.session_state.current_lesson = 0
                save_student_progress()
                st.rerun()
        
        # اختيار الفصل
        st.markdown(f"**📅 {t('term')}**")
        col1, col2, col3, col4 = st.columns(4)
        for i in range(1, 5):
            with [col1, col2, col3, col4][i-1]:
                if st.button(f"{i}", use_container_width=True):
                    st.session_state.current_term = i
                    st.session_state.current_lesson = 0
                    save_student_progress()
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
            
            lesson = lessons_data[st.session_state.student_level][st.session_state.current_book][st.session_state.current_term][i]
            lesson_title = lesson["title"][:25]
            
            if st.button(f"{icon} {lesson_title}", key=f"sidebar_lesson_{i}", use_container_width=True):
                st.session_state.current_lesson = i
                if status == "not_started":
                    update_lesson_status(lesson_key, "in_progress")
                save_student_progress()
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
                save_student_progress()
                st.rerun()
        with col2:
            if st.button("🇸🇦 AR", use_container_width=True):
                st.session_state.language = "ar"
                save_student_progress()
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
        
        # محرر الأكواد (للدروس البرمجية)
        if st.session_state.current_book == "programming" and "practice" in lesson and lesson["practice"].get("type") == "code":
            st.markdown(f"### 💻 {t('code_editor')}")
            st.markdown(f"<p>{t('write_code')}</p>", unsafe_allow_html=True)
            
            # محرر الكود
            code = st.text_area("", value=st.session_state.code_editor_content, height=200, key=f"code_editor_{lesson_key}", label_visibility="collapsed")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(t("run_code"), key=f"run_{lesson_key}"):
                    output, error = run_python_code(code)
                    if error:
                        st.session_state.code_output = f"❌ خطأ:\n{error}"
                    else:
                        st.session_state.code_output = output if output else "(لا يوجد مخرجات)"
                    st.rerun()
            
            # عرض المخرجات
            if st.session_state.code_output:
                st.markdown(f"**{t('code_output')}**")
                st.markdown(f"<div class='code-output'>{st.session_state.code_output}</div>", unsafe_allow_html=True)
            
            # زر التحقق من التمرين
            if "practice" in lesson and lesson["practice"].get("expected_output"):
                if st.button(t("check"), key=f"check_{lesson_key}"):
                    output, error = run_python_code(code)
                    expected = lesson["practice"]["expected_output"]
                    if error:
                        st.error(f"❌ {t('wrong')}\n{error}")
                    elif expected.strip() == output.strip():
                        st.success(f"✅ {t('correct')}")
                        st.balloons()
                        if current_status != "completed":
                            update_lesson_status(lesson_key, "completed")
                            save_student_progress()
                            st.rerun()
                    else:
                        st.error(f"❌ {t('wrong')}")
                        st.info(f"المخرج المتوقع: '{expected}'\nالمخرج الذي حصلت عليه: '{output}'")
        
        # التمرين العادي (اختيار من متعدد)
        elif "practice" in lesson and lesson["practice"].get("type") == "choice":
            st.markdown(f"### ✍️ {t('practice')}")
            ex = lesson["practice"]
            answer = st.radio(ex["question"], ex["options"], key=f"practice_{lesson_key}", index=None)
            if st.button(t("check"), key=f"check_{lesson_key}"):
                if answer == ex["answer"]:
                    st.success(f"✅ {t('correct')}")
                    st.balloons()
                    if current_status != "completed":
                        update_lesson_status(lesson_key, "completed")
                        save_student_progress()
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
                    save_student_progress()
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
                    save_student_progress()
                    st.rerun()
        with col2:
            if st.session_state.current_lesson < total_lessons - 1:
                if st.button(t("next"), use_container_width=True):
                    st.session_state.current_lesson += 1
                    save_student_progress()
                    st.rerun()
    
    else:
        st.info("📚 المزيد من الدروس قيد الإضافة...")
    
    # شهادة الإنجاز
    total_lessons_all = 0
    for level in lessons_data:
        for book in lessons_data[level]:
            for term in lessons_data[level][book]:
                total_lessons_all += len(lessons_data[level][book][term])
    
    completed_all = len([k for k, v in st.session_state.lesson_status.items() if v == "completed"])
    
    if completed_all >= total_lessons_all and total_lessons_all > 0:
        certificate_id = f"CERT-{st.session_state.student_id}-{datetime.now().strftime('%Y%m')}"
        
        if certificate_id not in st.session_state.certificates:
            st.session_state.certificates.append(certificate_id)
            save_student_progress()
        
        st.markdown(f"""
        <div class='certificate-box'>
            <h2>🏆 {t('certificate')}</h2>
            <h3>{t('certificate_earned')}</h3>
            <p>{st.session_state.student_name}</p>
            <p>{t('score')}: {st.session_state.total_score} {t('points')}</p>
            <p>📅 {datetime.now().strftime('%Y-%m-%d')}</p>
            <p>🔗 رابط التحقق: https://noor-knowledge.com/verify/{certificate_id}</p>
        </div>
        """, unsafe_allow_html=True)
