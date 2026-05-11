import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Заглавие
st.title("🧪 AI Анализатор на хранителни етикети")

st.write("""
Качи снимка на етикет или използвай камерата.
Приложението ще разпознае текста и ще открие вредни съставки.
""")

# Вредни съставки и Е-номера
harmful_ingredients = {
    "E407": "Карагенан – възпаления и храносмилателни проблеми",
    "E621": "Натриев глутамат – главоболие и алергии",
    "E262": "Натриев ацетат – дразни стомаха",
    "E300": "Аскорбинова киселина – в големи дози дразни стомаха",
    "E330": "Лимонена киселина – уврежда зъбния емайл",
    "E250": "Натриев нитрит – риск от онкологични заболявания",
    "E952": "Цикламат – изкуствен подсладител",
    "E471": "Емулгатор",
    "E472": "Емулгатор",
    "палмово масло": "Съдържа наситени мазнини",
    "palm oil": "Contains saturated fats",
    "aspartame": "Изкуствен подсладител",
}

# Качване на снимка
uploaded_file = st.file_uploader(
    "Качи изображение",
    type=["jpg", "jpeg", "png"]
)

# Снимка от камера
camera_image = st.camera_input("Или направи снимка")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

elif camera_image is not None:
    image = Image.open(camera_image)

# Ако има изображение
if image is not None:

    st.image(image, caption="Качено изображение", use_column_width=True)

    # Преобразуване към numpy масив
    img_array = np.array(image)

    # EasyOCR reader
    reader = easyocr.Reader(['bg', 'en'])

    with st.spinner("Разпознаване на текст..."):
        results = reader.readtext(img_array)

    # Събран текст
    detected_text = " ".join([res[1] for res in results])

    st.subheader("📄 Разпознат текст:")
    st.write(detected_text)

    # Търсене на вредни съставки
    found = []

    for ingredient, description in harmful_ingredients.items():
        if ingredient.lower() in detected_text.lower():
            found.append((ingredient, description))

    # Резултати
    st.subheader("⚠️ Открити съставки:")

    if found:
        for ingredient, description in found:
            st.error(f"{ingredient} → {description}")
    else:
        st.success("Не са открити вредни съставки.")
