import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, timedelta
import random
import time
import base64
from PIL import Image
import io

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="نور المعرفة - الكتاب الإلكتروني",
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
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "completed_pages" not in st.session_state:
    st.session_state.completed_pages = []
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "language" not in st.session_state:
    st.session_state.language = "ar"

# ==================== الترجمة ====================
lang = {
    "en": {
        "title": "📚 Noor Al-Ma'rifa E-Book",
        "subtitle": "Interactive Islamic Education | English | Mathematics",
        "welcome": "Welcome to Your Digital School",
        "student_name": "Student Name",
        "student_level": "Grade Level",
        "kg": "Kindergarten (KG)",
        "p1": "Primary 1",
        "p2": "Primary 2",
        "islamic": "🕌 Islamic Education",
        "english": "📖 English",
        "math": "🔢 Mathematics",
        "term": "📅 Term",
        "term1": "Term 1",
        "term2": "Term 2",
        "term3": "Term 3",
        "term4": "Term 4",
        "page": "📖 Page",
        "read": "📖 Read",
        "practice": "✍️ Practice",
        "exercise": "📝 Exercise",
        "color": "🎨 Color",
        "quiz": "📝 Quiz",
        "next": "➡️ Next Page",
        "prev": "⬅️ Previous Page",
        "check": "✅ Check Answer",
        "correct": "✅ Correct! Great job!",
        "wrong": "❌ Not quite. Try again!",
        "score": "⭐ Score",
        "points": "points",
        "completed": "✅ Completed",
        "certificate": "🏆 Certificate"
    },
    "ar": {
        "title": "📚 نور المعرفة – الكتاب الإلكتروني",
        "subtitle": "تعليم تفاعلي | تربية إسلامية | لغة إنجليزية | رياضيات",
        "welcome": "مرحباً بك في مدرستك الرقمية",
        "student_name": "اسم الطالب",
        "student_level": "المرحلة الدراسية",
        "kg": "رياض الأطفال (KG)",
        "p1": "الصف الأول الابتدائي",
        "p2": "الصف الثاني الابتدائي",
        "islamic": "🕌 التربية الإسلامية",
        "english": "📖 اللغة الإنجليزية",
        "math": "🔢 الرياضيات",
        "term": "📅 الفصل الدراسي",
        "term1": "الفصل الأول",
        "term2": "الفصل الثاني",
        "term3": "الفصل الثالث",
        "term4": "الفصل الرابع",
        "page": "📖 الصفحة",
        "read": "📖 اقرأ",
        "practice": "✍️ تدرب",
        "exercise": "📝 تمرين",
        "color": "🎨 لوّن",
        "quiz": "📝 اختبر نفسك",
        "next": "➡️ الصفحة التالية",
        "prev": "⬅️ الصفحة السابقة",
        "check": "✅ تحقق من الإجابة",
        "correct": "✅ إجابة صحيحة! أحسنت!",
        "wrong": "❌ إجابة خاطئة. حاول مرة أخرى!",
        "score": "⭐ درجتي",
        "points": "نقطة",
        "completed": "✅ مكتمل",
        "certificate": "🏆 شهادة إنجاز"
    },
    "sw": {
        "title": "📚 Noor Al-Ma'rifa E-Book",
        "subtitle": "Elimu Shirikishi | Kiislamu | Kiingereza | Hisabati",
        "welcome": "Karibu Shule Yako ya Dijitali",
        "student_name": "Jina la Mwanafunzi",
        "student_level": "Kiwango cha Mwanafunzi",
        "kg": "Darasa la Awali (KG)",
        "p1": "Darasa la Kwanza",
        "p2": "Darasa la Pili",
        "islamic": "🕌 Elimu ya Kiislamu",
        "english": "📖 Kiingereza",
        "math": "🔢 Hisabati",
        "term": "📅 Muhula",
        "term1": "Muhula wa 1",
        "term2": "Muhula wa 2",
        "term3": "Muhula wa 3",
        "term4": "Muhula wa 4",
        "page": "📖 Ukurasa",
        "read": "📖 Soma",
        "practice": "✍️ Fanya Mazoezi",
        "exercise": "📝 Zoezi",
        "color": "🎨 Rangi",
        "quiz": "📝 Jaribu",
        "next": "➡️ Ukurasa Unaofuata",
        "prev": "⬅️ Ukurasa Ulioletangulia",
        "check": "✅ Angalia Jibu",
        "correct": "✅ Jibu Sahihi! Hongera!",
        "wrong": "❌ Jibu Sio Sahihi. Jaribu Tena!",
        "score": "⭐ Alama Yangu",
        "points": "alama",
        "completed": "✅ Imekamilika",
        "certificate": "🏆 Cheti"
    }
}

def t(key):
    return lang[st.session_state.language].get(key, key)

# ==================== محتوى الكتاب الإلكتروني الكامل ====================
# كل صفحة تحتوي على: عنوان، نص تعليمي، صورة، تمرين، إجابة
def get_page_content(level, book, term, page):
    """محتوى الكتاب الإلكتروني حسب المرحلة والمادة والفصل والصفحة"""
    
    # ==================== رياض الأطفال (KG) ====================
    if level == "kg":
        # التربية الإسلامية
        if book == "islamic":
            pages = {
                1: {
                    "title": "أنا مسلم",
                    "text": "🌟 **أنا مسلم**\n\nأنا مسلم. ربي الله.\nنبينا محمد ﷺ.\nديننا الإسلام.\n\n📖 **سورة الفاتحة**\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\nالرَّحْمَٰنِ الرَّحِيمِ\nمَالِكِ يَوْمِ الدِّينِ\nإِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\nاهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\nصِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
                    "image": "🕌",
                    "exercise": {"type": "choice", "question": "من هو نبينا؟", "options": ["موسى", "عيسى", "محمد", "إبراهيم"], "answer": "محمد"}
                },
                2: {
                    "title": "دعاء الاستيقاظ",
                    "text": "🤲 **دعاء الاستيقاظ من النوم**\n\nالْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ\n\n**المعنى:** الحمد لله الذي أحيانا بعد ما أماتنا وإليه النشور.\n\n**متى نقوله؟**\nعند الاستيقاظ من النوم صباحاً.",
                    "image": "🌅",
                    "exercise": {"type": "choice", "question": "ماذا نقول عند الاستيقاظ؟", "options": ["بسم الله", "الحمد لله", "سبحان الله", "الله أكبر"], "answer": "الحمد لله"}
                },
                3: {
                    "title": "أركان الإسلام",
                    "text": "🕋 **أركان الإسلام الخمسة**\n\n1. **الشهادتان**: أشهد أن لا إله إلا الله وأشهد أن محمداً رسول الله\n2. **إقام الصلاة**: الصلوات الخمس في اليوم والليلة\n3. **إيتاء الزكاة**: إخراج جزء من المال للفقراء\n4. **صوم رمضان**: الصيام في شهر رمضان المبارك\n5. **حج البيت**: لمن استطاع إليه سبيلاً",
                    "image": "🕋",
                    "exercise": {"type": "choice", "question": "كم عدد أركان الإسلام؟", "options": ["3", "4", "5", "6"], "answer": "5"}
                },
                4: {
                    "title": "سورة الإخلاص",
                    "text": "📖 **سورة الإخلاص**\n\nقُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ\n\n**المعنى:** قل هو الله أحد، الله الصمد، لم يلد ولم يولد، ولم يكن له كفواً أحد.",
                    "image": "📖",
                    "exercise": {"type": "choice", "question": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "answer": "4"}
                },
                5: {
                    "title": "أركان الإيمان",
                    "text": "⭐ **أركان الإيمان الستة**\n\n1. الإيمان بالله\n2. الإيمان بالملائكة\n3. الإيمان بالكتب\n4. الإيمان بالرسل\n5. الإيمان باليوم الآخر\n6. الإيمان بالقدر خيره وشره",
                    "image": "⭐",
                    "exercise": {"type": "choice", "question": "كم عدد أركان الإيمان؟", "options": ["4", "5", "6", "7"], "answer": "6"}
                },
                6: {
                    "title": "سورة الفلق",
                    "text": "📖 **سورة الفلق**\n\nقُلْ أَعُوذُ بِرَبِّ الْفَلَقِ\nمِن شَرِّ مَا خَلَقَ\nوَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ\nوَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ\nوَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ\n\n**المعنى:** قل أعوذ برب الفلق من شر ما خلق...",
                    "image": "🌙",
                    "exercise": {"type": "choice", "question": "سورة الفلق تحمي من؟", "options": ["المرض", "الحسد", "الفقر", "الجهل"], "answer": "الحسد"}
                },
                7: {
                    "title": "الوضوء",
                    "text": "💧 **خطوات الوضوء**\n\n1. **النية** في القلب\n2. **غسل الكفين** ثلاث مرات\n3. **المضمضة والاستنشاق** ثلاث مرات\n4. **غسل الوجه** ثلاث مرات\n5. **غسل اليدين إلى المرفقين** ثلاث مرات\n6. **مسح الرأس والأذنين** مرة واحدة\n7. **غسل الرجلين إلى الكعبين** ثلاث مرات\n8. **الترتيب** كما ذكر",
                    "image": "💧",
                    "exercise": {"type": "choice", "question": "كم عدد فروض الوضوء؟", "options": ["4", "5", "6", "7"], "answer": "6"}
                },
                8: {
                    "title": "سورة الناس",
                    "text": "📖 **سورة الناس**\n\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ\nمَلِكِ النَّاسِ\nإِلَٰهِ النَّاسِ\nمِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ\nالَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ\nمِنَ الْجِنَّةِ وَالنَّاسِ\n\n**المعنى:** قل أعوذ برب الناس، ملك الناس، إله الناس...",
                    "image": "🤲",
                    "exercise": {"type": "choice", "question": "سورة الناس تحمي من؟", "options": ["المرض", "الوسواس", "الفقر", "الجهل"], "answer": "الوسواس"}
                }
            }
            return pages.get(page, None)
        
        # اللغة الإنجليزية
        elif book == "english":
            pages = {
                1: {"title": "My Family", "text": "👨‍👩‍👧‍👦 **My Family**\n\nI have a father.\nI have a mother.\nI have brothers and sisters.\nWe love each other.\n\n**New Words:**\n- Father 👨\n- Mother 👩\n- Brother 👦\n- Sister 👧", "image": "👨‍👩‍👧‍👦", "exercise": {"type": "choice", "question": "Who is your father?", "options": ["My mother's husband", "My brother", "My teacher"], "answer": "My mother's husband"}},
                2: {"title": "My Body", "text": "👁️ **My Body**\n\nI have eyes to see. 👁️\nI have ears to hear. 👂\nI have hands to clap. ✋\nI have feet to walk. 🦶\n\n**New Words:**\n- Eyes 👁️\n- Ears 👂\n- Hands ✋\n- Feet 🦶", "image": "👧", "exercise": {"type": "choice", "question": "What do we use to see?", "options": ["Ears", "Eyes", "Hands", "Feet"], "answer": "Eyes"}},
                3: {"title": "Animals", "text": "🐄 **Animals**\n\nCow 🐄 gives us milk.\nGoat 🐐 gives us meat.\nSheep 🐑 gives us wool.\nChicken 🐔 gives us eggs.\n\n**New Words:**\n- Cow 🐄\n- Goat 🐐\n- Sheep 🐑\n- Chicken 🐔", "image": "🐄", "exercise": {"type": "choice", "question": "What animal gives milk?", "options": ["Chicken", "Cow", "Dog", "Cat"], "answer": "Cow"}},
                4: {"title": "Fruits", "text": "🍎 **Fruits**\n\nBanana 🍌 is yellow.\nApple 🍎 is red.\nMango 🥭 is sweet.\nOrange 🍊 is orange.\n\n**New Words:**\n- Banana 🍌\n- Apple 🍎\n- Mango 🥭\n- Orange 🍊", "image": "🍎", "exercise": {"type": "choice", "question": "What fruit is yellow?", "options": ["Apple", "Orange", "Banana", "Mango"], "answer": "Banana"}},
                5: {"title": "Colors", "text": "🎨 **Colors**\n\nRed 🔴\nBlue 🔵\nYellow 🟡\nGreen 🟢\n\nThe sky is blue.\nThe grass is green.\nThe sun is yellow.\nThe apple is red.", "image": "🎨", "exercise": {"type": "choice", "question": "What color is the sky?", "options": ["Red", "Blue", "Yellow", "Green"], "answer": "Blue"}},
                6: {"title": "Weather", "text": "☀️ **Weather**\n\nSunny ☀️ - The sun is shining.\nRainy 🌧️ - It is raining.\nCloudy ☁️ - Clouds in the sky.\nWindy 🌬️ - The wind is blowing.", "image": "☀️", "exercise": {"type": "choice", "question": "What is the weather when it rains?", "options": ["Sunny", "Rainy", "Cloudy", "Windy"], "answer": "Rainy"}},
                7: {"title": "My School", "text": "🏫 **My School**\n\nI go to school.\nI have a teacher.\nI have friends.\nI learn many things.\n\nI learn to read and write.\nI learn math and science.", "image": "🏫", "exercise": {"type": "choice", "question": "Who teaches you at school?", "options": ["Friend", "Teacher", "Mother", "Father"], "answer": "Teacher"}},
                8: {"title": "Transportation", "text": "🚗 **Transportation**\n\nCar 🚗\nBus 🚌\nBicycle 🚲\nAirplane ✈️\nBoat 🚢\n\nWe ride cars and buses.\nWe fly in airplanes.\nWe sail in boats.", "image": "🚗", "exercise": {"type": "choice", "question": "What do you ride to school?", "options": ["Airplane", "Boat", "Car", "Rocket"], "answer": "Car"}}
            }
            return pages.get(page, None)
        
        # الرياضيات
        elif book == "math":
            pages = {
                1: {"title": "Counting 1-10", "text": "🔢 **Counting Numbers 1 to 10**\n\n1 2 3 4 5 6 7 8 9 10\n\nLet's count together:\n1️⃣ One\n2️⃣ Two\n3️⃣ Three\n4️⃣ Four\n5️⃣ Five\n6️⃣ Six\n7️⃣ Seven\n8️⃣ Eight\n9️⃣ Nine\n🔟 Ten", "image": "🔢", "exercise": {"type": "choice", "question": "What number comes after 5?", "options": ["4", "6", "7", "8"], "answer": "6"}},
                2: {"title": "Addition", "text": "➕ **Addition**\n\nAdding means putting together.\n\n1 + 1 = 2\n2 + 2 = 4\n3 + 2 = 5\n4 + 3 = 7\n5 + 4 = 9\n\nCount on your fingers!", "image": "➕", "exercise": {"type": "choice", "question": "3 + 2 = ?", "options": ["4", "5", "6", "7"], "answer": "5"}},
                3: {"title": "Subtraction", "text": "➖ **Subtraction**\n\nSubtracting means taking away.\n\n2 - 1 = 1\n5 - 2 = 3\n7 - 3 = 4\n9 - 4 = 5\n10 - 5 = 5", "image": "➖", "exercise": {"type": "choice", "question": "5 - 2 = ?", "options": ["2", "3", "4", "5"], "answer": "3"}},
                4: {"title": "Shapes", "text": "◯ **Shapes**\n\nCircle ◯\nSquare ◻️\nTriangle ▲\nRectangle ▭\n\nA ball is a circle.\nA box is a square.\nA roof is a triangle.\nA door is a rectangle.", "image": "◯", "exercise": {"type": "choice", "question": "What shape has 4 equal sides?", "options": ["Circle", "Square", "Triangle", "Rectangle"], "answer": "Square"}},
                5: {"title": "Numbers 11-20", "text": "🔢 **Numbers 11 to 20**\n\n11 Eleven\n12 Twelve\n13 Thirteen\n14 Fourteen\n15 Fifteen\n16 Sixteen\n17 Seventeen\n18 Eighteen\n19 Nineteen\n20 Twenty", "image": "🔢", "exercise": {"type": "choice", "question": "What number comes after 15?", "options": ["14", "16", "17", "18"], "answer": "16"}},
                6: {"title": "Money (UGX)", "text": "💰 **Ugandan Money**\n\n1,000 Shillings (One Thousand)\n2,000 Shillings (Two Thousand)\n5,000 Shillings (Five Thousand)\n10,000 Shillings (Ten Thousand)\n\nWe use money to buy things.", "image": "💰", "exercise": {"type": "choice", "question": "1000 + 1000 = ?", "options": ["1000", "1500", "2000", "2500"], "answer": "2000"}},
                7: {"title": "Addition up to 20", "text": "➕ **Addition up to 20**\n\n10 + 5 = 15\n12 + 3 = 15\n14 + 2 = 16\n11 + 8 = 19\n13 + 6 = 19", "image": "➕", "exercise": {"type": "choice", "question": "12 + 5 = ?", "options": ["15", "16", "17", "18"], "answer": "17"}},
                8: {"title": "Subtraction up to 20", "text": "➖ **Subtraction up to 20**\n\n15 - 3 = 12\n18 - 4 = 14\n20 - 5 = 15\n17 - 7 = 10\n19 - 9 = 10", "image": "➖", "exercise": {"type": "choice", "question": "18 - 6 = ?", "options": ["10", "11", "12", "13"], "answer": "12"}}
            }
            return pages.get(page, None)
    
    # ==================== الصف الأول (P1) ====================
    elif level == "p1":
        if book == "islamic":
            pages = {
                1: {"title": "سورة الفاتحة", "text": "📖 **سورة الفاتحة**\n\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\nالرَّحْمَٰنِ الرَّحِيمِ\nمَالِكِ يَوْمِ الدِّينِ\nإِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\nاهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\nصِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ\n\n**تفسير مبسط:**\nالفاتحة هي أم القرآن، نقرأها في كل صلاة. فيها نحمد الله ونطلب منه الهداية.", "image": "📖", "exercise": {"type": "choice", "question": "كم عدد آيات سورة الفاتحة؟", "options": ["5", "6", "7", "8"], "answer": "7"}},
                2: {"title": "أركان الإسلام", "text": "🕋 **أركان الإسلام الخمسة**\n\n1. **الشهادتان** (أشهد أن لا إله إلا الله وأشهد أن محمداً رسول الله)\n2. **الصلاة** (5 صلوات في اليوم والليلة)\n3. **الزكاة** (إخراج جزء من المال للفقراء)\n4. **الصوم** (صيام شهر رمضان)\n5. **الحج** (زيارة بيت الله الحرام لمن استطاع)", "image": "🕋", "exercise": {"type": "choice", "question": "ما هو الركن الثاني من أركان الإسلام؟", "options": ["الصلاة", "الزكاة", "الصوم", "الحج"], "answer": "الصلاة"}},
                3: {"title": "سورة الإخلاص", "text": "📖 **سورة الإخلاص**\n\nقُلْ هُوَ اللَّهُ أَحَدٌ\nاللَّهُ الصَّمَدُ\nلَمْ يَلِدْ وَلَمْ يُولَدْ\nوَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ\n\n**تفسير مبسط:**\nسورة الإخلاص تخبرنا أن الله واحد أحد، ليس له ولد ولا والد، ولا يشبهه أحد.", "image": "📖", "exercise": {"type": "choice", "question": "سورة الإخلاص كم آية؟", "options": ["2", "3", "4", "5"], "answer": "4"}},
                4: {"title": "أركان الإيمان", "text": "⭐ **أركان الإيمان الستة**\n\n1. الإيمان بالله\n2. الإيمان بالملائكة\n3. الإيمان بالكتب\n4. الإيمان بالرسل\n5. الإيمان باليوم الآخر\n6. الإيمان بالقدر خيره وشره", "image": "⭐", "exercise": {"type": "choice", "question": "كم عدد أركان الإيمان؟", "options": ["4", "5", "6", "7"], "answer": "6"}}
            }
            return pages.get(page, None)
        elif book == "english":
            pages = {
                1: {"title": "Greetings", "text": "👋 **Greetings**\n\nGood morning! (صباح الخير)\nGood afternoon! (مساء الخير)\nGood evening! (مساء الخير)\nGood night! (تصبح على خير)\n\n**Practice:**\nSay \"Good morning\" to your teacher.", "image": "👋", "exercise": {"type": "choice", "question": "What do you say in the morning?", "options": ["Good night", "Good morning", "Goodbye", "Hello"], "answer": "Good morning"}},
                2: {"title": "My School", "text": "🏫 **My School**\n\nI go to school every day.\nI have a teacher. 👩‍🏫\nI have friends. 👧👦\nI learn many things.\n\nI learn to read and write.\nI learn math and science.", "image": "🏫", "exercise": {"type": "choice", "question": "Who teaches you at school?", "options": ["Friend", "Teacher", "Mother", "Father"], "answer": "Teacher"}},
                3: {"title": "Colors", "text": "🎨 **Colors**\n\nRed 🔴\nBlue 🔵\nYellow 🟡\nGreen 🟢\nBlack ⚫\nWhite ⚪\n\n**Examples:**\nThe apple is red.\nThe sky is blue.\nThe sun is yellow.\nThe grass is green.", "image": "🎨", "exercise": {"type": "choice", "question": "What color is the grass?", "options": ["Red", "Blue", "Yellow", "Green"], "answer": "Green"}},
                4: {"title": "Weather", "text": "☀️ **Weather**\n\nSunny ☀️ - The sun is shining.\nRainy 🌧️ - It is raining.\nCloudy ☁️ - Clouds in the sky.\nWindy 🌬️ - The wind is blowing.\n\nWhat is the weather today?", "image": "☀️", "exercise": {"type": "choice", "question": "What is the weather when it rains?", "options": ["Sunny", "Rainy", "Cloudy", "Windy"], "answer": "Rainy"}}
            }
            return pages.get(page, None)
        elif book == "math":
            pages = {
                1: {"title": "Numbers 1-50", "text": "🔢 **Numbers 1 to 50**\n\n1-10: 1 2 3 4 5 6 7 8 9 10\n11-20: 11 12 13 14 15 16 17 18 19 20\n21-30: 21 22 23 24 25 26 27 28 29 30\n31-40: 31 32 33 34 35 36 37 38 39 40\n41-50: 41 42 43 44 45 46 47 48 49 50", "image": "🔢", "exercise": {"type": "choice", "question": "What number comes after 29?", "options": ["28", "30", "31", "40"], "answer": "30"}},
                2: {"title": "Addition", "text": "➕ **Addition up to 20**\n\nAdding means putting together.\n\n10 + 5 = 15\n12 + 3 = 15\n14 + 2 = 16\n11 + 8 = 19\n13 + 6 = 19\n\n**Practice:**\n15 + 4 = 19", "image": "➕", "exercise": {"type": "choice", "question": "14 + 5 = ?", "options": ["18", "19", "20", "21"], "answer": "19"}},
                3: {"title": "Subtraction", "text": "➖ **Subtraction up to 20**\n\nSubtracting means taking away.\n\n15 - 3 = 12\n18 - 4 = 14\n20 - 5 = 15\n17 - 7 = 10\n19 - 9 = 10\n\n**Practice:**\n16 - 4 = 12", "image": "➖", "exercise": {"type": "choice", "question": "18 - 6 = ?", "options": ["10", "11", "12", "13"], "answer": "12"}},
                4: {"title": "Multiplication", "text": "✖️ **Multiplication Tables**\n\n2 × 1 = 2\n2 × 2 = 4\n2 × 3 = 6\n2 × 4 = 8\n2 × 5 = 10\n\n3 × 1 = 3\n3 × 2 = 6\n3 × 3 = 9\n3 × 4 = 12\n3 × 5 = 15", "image": "✖️", "exercise": {"type": "choice", "question": "3 × 4 = ?", "options": ["7", "10", "12", "15"], "answer": "12"}}
            }
            return pages.get(page, None)
    
    # ==================== الصف الثاني (P2) ====================
    elif level == "p2":
        if book == "islamic":
            pages = {
                1: {"title": "سورة الكوثر", "text": "📖 **سورة الكوثر**\n\nإِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ\nفَصَلِّ لِرَبِّكَ وَانْحَرْ\nإِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ\n\n**تفسير مبسط:**\nالله أعطى النبي ﷺ خيراً كثيراً، فأمره أن يصلي ويذبح لله.", "image": "📖", "exercise": {"type": "choice", "question": "سورة الكوثر كم آية؟", "options": ["2", "3", "4", "5"], "answer": "3"}},
                2: {"title": "الصلاة", "text": "🕌 **الصلاة**\n\nالصلاة هي عمود الدين.\nالصلوات الخمس:\n1. الفجر (ركعتان)\n2. الظهر (أربع ركعات)\n3. العصر (أربع ركعات)\n4. المغرب (ثلاث ركعات)\n5. العشاء (أربع ركعات)", "image": "🕌", "exercise": {"type": "choice", "question": "كم عدد الصلوات المفروضة في اليوم؟", "options": ["3", "4", "5", "6"], "answer": "5"}},
                3: {"title": "الزكاة", "text": "💰 **الزكاة**\n\nالزكاة هي الركن الثالث من أركان الإسلام.\nنسبة الزكاة: 2.5% من المال.\n\n**مصارف الزكاة:**\n- الفقراء والمساكين\n- العاملين عليها\n- المؤلفة قلوبهم\n- في الرقاب\n- الغارمين\n- في سبيل الله\n- ابن السبيل", "image": "💰", "exercise": {"type": "choice", "question": "كم نسبة الزكاة؟", "options": ["1%", "2.5%", "5%", "10%"], "answer": "2.5%"}},
                4: {"title": "الصوم", "text": "🌙 **الصوم**\n\nالصوم هو الركن الرابع من أركان الإسلام.\nنصوم شهر رمضان المبارك.\n\n**أركان الصوم:**\n- النية\n- الإمساك عن الطعام والشراب من الفجر إلى المغرب\n\n**مفطرات الصوم:**\n- الأكل والشرب عمداً\n- الجماع\n- إنزال المني\n- الحيض والنفاس", "image": "🌙", "exercise": {"type": "choice", "question": "متى يبدأ وقت الصوم؟", "options": ["من طلوع الشمس", "من أذان الفجر", "من الظهر", "من المغرب"], "answer": "من أذان الفجر"}}
            }
            return pages.get(page, None)
        elif book == "english":
            pages = {
                1: {"title": "My Day", "text": "⏰ **My Day**\n\nI wake up at 6 o'clock.\nI eat breakfast at 7 o'clock.\nI go to school at 8 o'clock.\nI play with friends at 4 o'clock.\nI eat dinner at 7 o'clock.\nI go to bed at 9 o'clock.", "image": "⏰", "exercise": {"type": "choice", "question": "What do you do in the morning?", "options": ["Sleep", "Wake up", "Play", "Eat dinner"], "answer": "Wake up"}},
                2: {"title": "My Village", "text": "🏘️ **My Village**\n\nI live in Kiryandongo.\nThere is a market. 🏪\nThere is a school. 🏫\nThere is a mosque. 🕌\nThere are many farms. 🌾\nThe people are friendly.", "image": "🏘️", "exercise": {"type": "choice", "question": "Where do we pray?", "options": ["School", "Market", "Mosque", "Farm"], "answer": "Mosque"}},
                3: {"title": "Transportation", "text": "🚗 **Transportation**\n\nCar 🚗\nBus 🚌\nBicycle 🚲\nMotorcycle 🏍️\nAirplane ✈️\nBoat 🚢\n\nWe use transportation to go places.", "image": "🚗", "exercise": {"type": "choice", "question": "What do you ride to school?", "options": ["Airplane", "Boat", "Car", "Rocket"], "answer": "Car"}},
                4: {"title": "Jobs", "text": "👨‍🏫 **Jobs**\n\nTeacher 👨‍🏫 - teaches students\nDoctor 👩‍⚕️ - helps sick people\nFarmer 👨‍🌾 - grows food\nPolice 👮‍♂️ - keeps us safe\nDriver 🚗 - drives vehicles", "image": "👨‍🏫", "exercise": {"type": "choice", "question": "Who helps sick people?", "options": ["Teacher", "Doctor", "Farmer", "Police"], "answer": "Doctor"}}
            }
            return pages.get(page, None)
        elif book == "math":
            pages = {
                1: {"title": "Numbers 1-100", "text": "🔢 **Numbers 1 to 100**\n\n1-10: 1 2 3 4 5 6 7 8 9 10\n11-20: 11 12 13 14 15 16 17 18 19 20\n21-30: 21 22 23 24 25 26 27 28 29 30\n... and so on up to 100", "image": "🔢", "exercise": {"type": "choice", "question": "What number comes after 49?", "options": ["48", "50", "51", "60"], "answer": "50"}},
                2: {"title": "Addition up to 50", "text": "➕ **Addition up to 50**\n\n25 + 15 = 40\n32 + 18 = 50\n20 + 25 = 45\n35 + 10 = 45\n40 + 8 = 48", "image": "➕", "exercise": {"type": "choice", "question": "25 + 15 = ?", "options": ["30", "35", "40", "45"], "answer": "40"}},
                3: {"title": "Subtraction up to 50", "text": "➖ **Subtraction up to 50**\n\n45 - 20 = 25\n50 - 30 = 20\n38 - 15 = 23\n42 - 12 = 30\n35 - 10 = 25", "image": "➖", "exercise": {"type": "choice", "question": "45 - 20 = ?", "options": ["20", "25", "30", "35"], "answer": "25"}},
                4: {"title": "Multiplication Tables", "text": "✖️ **Multiplication Tables**\n\n2 × 1 = 2\n2 × 2 = 4\n2 × 3 = 6\n2 × 4 = 8\n2 × 5 = 10\n\n3 × 1 = 3\n3 × 2 = 6\n3 × 3 = 9\n3 × 4 = 12\n3 × 5 = 15\n\n4 × 1 = 4\n4 × 2 = 8\n4 × 3 = 12\n4 × 4 = 16\n4 × 5 = 20\n\n5 × 1 = 5\n5 × 2 = 10\n5 × 3 = 15\n5 × 4 = 20\n5 × 5 = 25", "image": "✖️", "exercise": {"type": "choice", "question": "3 × 4 = ?", "options": ["7", "10", "12", "15"], "answer": "12"}}
            }
            return pages.get(page, None)
    
    return None

# ==================== واجهة الكتاب الإلكتروني ====================
def render_book_page():
    """عرض صفحة الكتاب الإلكتروني"""
    page_data = get_page_content(
        st.session_state.student_level,
        st.session_state.current_book,
        st.session_state.current_term,
        st.session_state.current_page + 1
    )
    
    if page_data:
        # عنوان الصفحة
        st.markdown(f"## 📖 {t('page')} {st.session_state.current_page + 1}: {page_data['title']}")
        
        # محتوى الصفحة (نص + صورة)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style='background: #fff8e7; padding: 1.5rem; border-radius: 15px; border-left: 5px solid #e67e22; font-size: 1.1rem; line-height: 1.8;'>
                {page_data['text']}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='text-align: center; font-size: 5rem; padding: 1rem; background: #f0f2f6; border-radius: 15px;'>
                {page_data['image']}
            </div>
            """, unsafe_allow_html=True)
        
        # التمرين
        if "exercise" in page_data:
            st.markdown("---")
            st.markdown(f"### ✍️ {t('exercise')}")
            
            ex = page_data["exercise"]
            page_id = f"{st.session_state.student_level}_{st.session_state.current_book}_{st.session_state.current_term}_{st.session_state.current_page}"
            
            if ex["type"] == "choice":
                answer = st.radio(ex["question"], ex["options"], key=f"ex_{page_id}", index=None)
                if st.button(t("check"), key=f"check_{page_id}"):
                    if answer == ex["answer"]:
                        st.success(f"✅ {t('correct')}")
                        st.balloons()
                        if page_id not in st.session_state.completed_pages:
                            st.session_state.completed_pages.append(page_id)
                            st.session_state.total_score += 10
                    else:
                        st.error(f"❌ {t('wrong')}")
                        st.info(f"💡 الإجابة الصحيحة: {ex['answer']}")
    
    else:
        st.info("📚 هذه الصفحة قيد الإعداد...")

# ==================== واجهة التطبيق ====================
# تصميم الكتاب
st.markdown("""
<style>
    .book-cover {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .page-nav {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
    .progress-bar {
        background: #f0f2f6;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
    }
    .progress-fill {
        background: #2ecc71;
        border-radius: 10px;
        height: 100%;
        width: 0%;
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
        <p>👋 {t('welcome')} {st.session_state.student_name}</p>
        <p>⭐ {t('score')}: {st.session_state.total_score} {t('points')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.student_name}")
        st.markdown(f"**{t('score')}:** {st.session_state.total_score} ⭐")
        
        # اختيار المرحلة
        st.markdown(f"**{t('student_level')}**")
        levels = {"kg": t("kg"), "p1": t("p1"), "p2": t("p2")}
        for key, name in levels.items():
            if st.button(name, use_container_width=True):
                st.session_state.student_level = key
                st.session_state.current_page = 0
                st.session_state.completed_pages = []
                st.rerun()
        
        # اختيار المادة
        st.markdown(f"**{t('islamic')} / {t('english')} / {t('math')}**")
        books = {"islamic": t("islamic"), "english": t("english"), "math": t("math")}
        for key, name in books.items():
            if st.button(name, use_container_width=True):
                st.session_state.current_book = key
                st.session_state.current_page = 0
                st.rerun()
        
        # اختيار الفصل
        st.markdown(f"**{t('term')}**")
        col1, col2, col3, col4 = st.columns(4)
        for i in range(1, 5):
            with [col1, col2, col3, col4][i-1]:
                if st.button(f"{i}", use_container_width=True):
                    st.session_state.current_term = i
                    st.session_state.current_page = 0
                    st.rerun()
        
        # شريط التقدم
        st.markdown("---")
        st.markdown(f"### 📊 {t('progress')}")
        total_pages = 8  # 8 صفحات لكل فصل
        completed = len([p for p in st.session_state.completed_pages if f"{st.session_state.student_level}_{st.session_state.current_book}_{st.session_state.current_term}_" in p])
        st.progress(completed / total_pages)
        st.caption(f"{completed}/{total_pages} {t('page')}")
        
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
    
    # عرض الكتاب
    render_book_page()
    
    # أزرار التنقل
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_page > 0:
            if st.button(t("prev"), use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
    with col3:
        if st.session_state.current_page < 7:
            if st.button(t("next"), use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
    
    # شهادة الإنجاز
    if len(st.session_state.completed_pages) >= 8 * 4 * 3:  # 8 صفحات × 4 فصول × 3 مواد
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
