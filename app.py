import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random
import time

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - التعليم بالذكاء الاصطناعي",
    page_icon="🤖",
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
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "🤖 Noor Al-Ma'rifa AI",
        "subtitle": "AI-Powered Learning | Islamic Education | English | Mathematics",
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
        "lesson": "📚 Lesson",
        "ai_tutor": "🤖 AI Tutor",
        "ask_me": "Ask me anything about the lesson",
        "your_answer": "Your answer",
        "check": "✅ Check Answer",
        "next": "➡️ Next Lesson",
        "prev": "⬅️ Previous Lesson",
        "correct": "✅ Correct! Great job!",
        "wrong": "❌ Not quite. Let me help you...",
        "explanation": "💡 Here's what you need to know:",
        "score": "⭐ Score",
        "points": "points",
        "well_done": "🎉 Well done! You completed the lesson!",
        "type_message": "Type your question here...",
        "send": "Send"
    },
    "ar": {
        "title": "🤖 نور المعرفة – التعليم بالذكاء الاصطناعي",
        "subtitle": "تعليم ذكي | تربية إسلامية | لغة إنجليزية | رياضيات",
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
        "lesson": "📚 الدرس",
        "ai_tutor": "🤖 المعلم الذكي",
        "ask_me": "اسألني أي شيء عن الدرس",
        "your_answer": "إجابتك",
        "check": "✅ تحقق من الإجابة",
        "next": "➡️ الدرس التالي",
        "prev": "⬅️ الدرس السابق",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ ليس صحيحاً. دعني أساعدك...",
        "explanation": "💡 إليك ما تحتاج معرفته:",
        "score": "⭐ درجتي",
        "points": "نقطة",
        "well_done": "🎉 ممتاز! لقد أكملت الدرس!",
        "type_message": "اكتب سؤالك هنا...",
        "send": "إرسال"
    },
    "sw": {
        "title": "🤖 Noor Al-Ma'rifa AI",
        "subtitle": "Kujifunza kwa Akili Bandia | Kiislamu | Kiingereza | Hisabati",
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
        "lesson": "📚 Somo",
        "ai_tutor": "🤖 Mwalimu wa AI",
        "ask_me": "Niulize chochote kuhusu somo",
        "your_answer": "Jibu lako",
        "check": "✅ Angalia Jibu",
        "next": "➡️ Somo Linalofuata",
        "prev": "⬅️ Somo Lililotangulia",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Sio sahihi. Hebu nikusaidie...",
        "explanation": "💡 Hiki ndicho unachohitaji kujua:",
        "score": "⭐ Alama Yangu",
        "points": "alama",
        "well_done": "🎉 Umefanya vizuri! Umemaliza somo!",
        "type_message": "Andika swali lako hapa...",
        "send": "Tuma"
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
                "text": """🌟 **الدرس الأول: أنا مسلم**

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
                "question": "من هو نبينا؟",
                "answer": "محمد",
                "hint": "هو خاتم الأنبياء والمرسلين، اسمه محمد بن عبد الله"
            },
            2: {
                "title": "أركان الإسلام وسورة الإخلاص",
                "text": """🕋 **أركان الإسلام الخمسة**

1. الشهادتان (أشهد أن لا إله إلا الله وأشهد أن محمداً رسول الله)
2. إقام الصلاة
3. إيتاء الزكاة
4. صوم رمضان
5. حج البيت لمن استطاع إليه سبيلاً

📖 **سورة الإخلاص**
قُلْ هُوَ اللَّهُ أَحَدٌ
اللَّهُ الصَّمَدُ
لَمْ يَلِدْ وَلَمْ يُولَدْ
وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ

🤲 **دعاء دخول الخلاء**
اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ""",
                "question": "كم عدد أركان الإسلام؟",
                "answer": "5",
                "hint": "هي خمسة: الشهادة، الصلاة، الزكاة، الصوم، الحج"
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
                "question": "كم عدد أركان الإيمان؟",
                "answer": "6",
                "hint": "هي ستة: الإيمان بالله، ملائكته، كتبه، رسله، اليوم الآخر، والقدر"
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
8. الترتيب

📖 **سورة الناس**
قُلْ أَعُوذُ بِرَبِّ النَّاسِ
مَلِكِ النَّاسِ
إِلَٰهِ النَّاسِ
مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ
الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ
مِنَ الْجِنَّةِ وَالنَّاسِ

🤲 **دعاء النوم**
بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا""",
                "question": "كم عدد فروض الوضوء؟",
                "answer": "6",
                "hint": "فروض الوضوء ستة: غسل الوجه، اليدين، مسح الرأس، غسل الرجلين، الترتيب، الموالاة"
            }
        },
        "english": {
            1: {"title": "My Family", "text": "I have a father. I have a mother. I have brothers and sisters.", "question": "Who is your father?", "answer": "My mother's husband", "hint": "He is the man in your family"},
            2: {"title": "My Body", "text": "I have eyes to see. I have ears to hear. I have hands to clap.", "question": "What do we use to see?", "answer": "Eyes", "hint": "We use them to look at things"},
            3: {"title": "Animals", "text": "Cow, Goat, Sheep, Chicken, Dog, Cat", "question": "What animal gives milk?", "answer": "Cow", "hint": "It gives us milk and meat"},
            4: {"title": "Fruits", "text": "Banana, Mango, Orange, Apple", "question": "What fruit is yellow?", "answer": "Banana", "hint": "Monkeys love it. It's long and yellow"}
        },
        "math": {
            1: {"title": "Counting 1-10", "text": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "question": "What is after 5?", "answer": "6", "hint": "Count: 1,2,3,4,5, then..."},
            2: {"title": "Addition", "text": "1+1=2, 2+2=4, 3+2=5", "question": "3 + 2 = ?", "answer": "5", "hint": "Count: 3, then add 2 more: 4,5"},
            3: {"title": "Numbers 11-20", "text": "11,12,13,14,15,16,17,18,19,20", "question": "What is after 15?", "answer": "16", "hint": "Count: 11,12,13,14,15, then..."},
            4: {"title": "Addition up to 20", "text": "10+5=15, 12+3=15", "question": "12 + 5 = ?", "answer": "17", "hint": "Count from 12: 13,14,15,16,17"}
        }
    },
    "p1": {"islamic": {}, "english": {}, "math": {}},
    "p2": {"islamic": {}, "english": {}, "math": {}}
}

# ==================== وظائف الذكاء الاصطناعي ====================
def ai_tutor_response(question, lesson_text, correct_answer, student_answer=None):
    """محاكاة ذكاء اصطناعي يشرح ويوجه"""
    responses = []
    
    if student_answer is not None:
        if student_answer.lower().strip() == correct_answer.lower():
            responses.append(f"✅ {t('correct')}")
            responses.append("🎉 ممتاز! أنت تفهم الدرس جيداً.")
            return responses
    
    # ردود عامة حسب السؤال
    if "محمد" in question or "نبينا" in question:
        responses.append("💡 نبينا هو محمد بن عبد الله ﷺ، خاتم الأنبياء والمرسلين.")
        responses.append("📖 ولد في مكة المكرمة، وبعثه الله للناس كافة.")
    elif "أركان الإسلام" in question or "5" in question:
        responses.append("🕋 أركان الإسلام خمسة:")
        responses.append("1. الشهادتان\n2. الصلاة\n3. الزكاة\n4. الصوم\n5. الحج")
    elif "أركان الإيمان" in question or "6" in question:
        responses.append("⭐ أركان الإيمان ستة:")
        responses.append("1. الإيمان بالله\n2. الإيمان بالملائكة\n3. الإيمان بالكتب\n4. الإيمان بالرسل\n5. الإيمان باليوم الآخر\n6. الإيمان بالقدر")
    elif "الوضوء" in question or "فروض" in question:
        responses.append("💧 فروض الوضوء ستة:")
        responses.append("1. غسل الوجه\n2. غسل اليدين إلى المرفقين\n3. مسح الرأس\n4. غسل الرجلين إلى الكعبين\n5. الترتيب\n6. الموالاة")
    elif "eyes" in question or "see" in question:
        responses.append("👁️ We use our EYES to see.")
        responses.append("We also have ears to hear, hands to touch, and nose to smell.")
    elif "cow" in question or "milk" in question:
        responses.append("🐄 The COW gives us milk.")
        responses.append("We also get milk from goats and camels.")
    elif "banana" in question or "yellow" in question:
        responses.append("🍌 The BANANA is yellow.")
        responses.append("It is long, sweet, and monkeys love it.")
    else:
        responses.append(f"💡 {t('explanation')}")
        responses.append(lesson_text[:200] + "...")
    
    if student_answer:
        responses.append(f"\n❌ إجابتك: '{student_answer}'")
        responses.append(f"✅ الإجابة الصحيحة: '{correct_answer}'")
    
    return responses

# ==================== واجهة التطبيق ====================
# العنوان
st.markdown(f"""
<div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 1rem; color: white;'>
    <h1>🤖 {t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### 📚 {t('title')}")
    
    # اختيار المرحلة
    st.markdown(f"**{t('select_level')}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("KG", use_container_width=True):
            st.session_state.level = "kg"
            st.session_state.current_lesson = 0
            st.session_state.score = 0
            st.rerun()
    with col2:
        if st.button("P1", use_container_width=True):
            st.session_state.level = "p1"
            st.session_state.current_lesson = 0
            st.rerun()
    with col3:
        if st.button("P2", use_container_width=True):
            st.session_state.level = "p2"
            st.session_state.current_lesson = 0
            st.rerun()
    
    # اختيار المادة
    st.markdown(f"**{t('select_subject')}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🕌 إسلامي", use_container_width=True):
            st.session_state.subject = "islamic"
            st.session_state.current_lesson = 0
            st.rerun()
    with col2:
        if st.button("📖 English", use_container_width=True):
            st.session_state.subject = "english"
            st.session_state.current_lesson = 0
            st.rerun()
    with col3:
        if st.button("🔢 Math", use_container_width=True):
            st.session_state.subject = "math"
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
    st.markdown(f"### {t('score')}")
    st.markdown(f"## {st.session_state.score} {t('points')}")
    
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

# ==================== عرض الدرس ====================
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
                    st.session_state.answered = False
                    st.rerun()
        with col3:
            if st.session_state.current_lesson < 3 and st.session_state.answered:
                if st.button(t('next'), use_container_width=True):
                    st.session_state.current_lesson += 1
                    st.session_state.answered = False
                    st.session_state.score += 10
                    st.rerun()
        
        # عرض الدرس الحالي
        st.markdown(f"## {t('lesson')} {st.session_state.current_lesson + 1}: {lesson_data.get('title', '')}")
        
        # عرض محتوى الدرس
        st.markdown(f"""
        <div style='background: #f0f2f6; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;'>
            {lesson_data.get('text', '')}
        </div>
        """, unsafe_allow_html=True)
        
        # المعلم الذكي (AI Tutor)
        st.markdown(f"### {t('ai_tutor')}")
        
        # منطقة الأسئلة التفاعلية
        with st.container():
            st.markdown(f"**📝 {lesson_data.get('question', '')}**")
            
            user_answer = st.text_input(t('your_answer'), key="answer_input")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(t('check'), use_container_width=True):
                    if user_answer:
                        st.session_state.answered = True
                        correct = lesson_data.get('answer', '')
                        
                        if user_answer.lower().strip() == correct.lower():
                            st.success(f"✅ {t('correct')}")
                            st.balloons()
                            if not st.session_state.answered:
                                st.session_state.score += 10
                        else:
                            st.error(f"❌ {t('wrong')}")
                            # المعلم الذكي يشرح
                            ai_response = ai_tutor_response(
                                lesson_data.get('question', ''),
                                lesson_data.get('text', ''),
                                correct,
                                user_answer
                            )
                            for msg in ai_response:
                                st.info(msg)
                    else:
                        st.warning("✏️ اكتب إجابتك أولاً")
            
            with col2:
                if st.button("💡 Hint", use_container_width=True):
                    st.info(f"💡 {lesson_data.get('hint', 'فكر في الدرس جيداً')}")
        
        # شريط التقدم
        st.progress((st.session_state.current_lesson + 1) / 4)
        
        if st.session_state.current_lesson == 3 and st.session_state.answered:
            st.success(f"🎉 {t('well_done')}")
    
    else:
        st.info("📚 المزيد من الدروس قيد الإضافة للمرحلة والمادة المختارة...")
        st.image("https://cdn-icons-png.flaticon.com/512/1674/1674083.png", width=100)
        
except Exception as e:
    st.info("🎓 اختر المرحلة والمادة والفصل لبدء التعلم")
    st.image("https://cdn-icons-png.flaticon.com/512/1674/1674083.png", width=100)

# ==================== محادثة المعلم الذكي ====================
with st.expander("💬 اسأل المعلم الذكي أي سؤال"):
    user_question = st.text_input(t('type_message'), key="ai_question")
    if st.button(t('send'), use_container_width=True):
        if user_question:
            with st.spinner("🤖 المعلم يفكر..."):
                time.sleep(1)
                response = ai_tutor_response(
                    user_question,
                    lesson_data.get('text', '') if lesson_data else "",
                    lesson_data.get('answer', '') if lesson_data else "",
                    None
                )
                for msg in response:
                    st.info(msg)
        else:
            st.warning("✏️ اكتب سؤالك أولاً")
