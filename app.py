import streamlit as st
from Model import BertLinear, predict, predict_one
from PreprocessText import URLParser
import pandas as pd

st.set_page_config(page_title="Furniture Extractor", layout="wide")

st.title("Furniture Product Extractor")
st.markdown("Введите URL магазина мебели")

if 'raw_results' not in st.session_state:
    st.session_state['raw_results'] = []

# cache
@st.cache_resource
def load_my_model():
    model = BertLinear()
    model.load_weight()

    parser = URLParser()
    return model, parser


model, parser = load_my_model()

with st.sidebar:
    st.header("Настройки модели")
    threshold = st.slider("Порог уверенности (Precision)", 0.5, 0.95, 0.5)
    st.info("Чем выше порог, тем меньше мусора, но меньше товаров.")

urls = st.text_area(
    "Список URL:",
    placeholder="https://ikea.com/...\nhttps://hoff.ru/...",
    height=150
)

if st.button("Начать парсинг"):
    urls = [url.strip() for url in urls.split('\n') if url.strip()]
    if urls:
        all_results = []
        progress_bar = st.progress(0)

        for idx, url in enumerate(urls):
            with st.status(f"Обработка {url}...", expanded=False) as status:
                try:
                    input_texts = parser.parse_one(url)
                    if not input_texts:
                        st.warning(f"Текст не найден на {url}")
                        continue

                    outputs = predict_one(input_texts, model, True)

                    for name, output in zip(input_texts, outputs):
                        prob = float(output[1])
                        all_results.append({
                            "URL": url,
                            "name": name,
                            "proba": prob
                        })
                    status.update(label=f"Завершено: {url}", state="complete")
                except Exception as e:
                    st.error(f"Ошибка при обработке {url}: {e}")
                    status.update(label=f"Ошибка: {url}", state="error")

            progress_bar.progress((idx + 1) / len(urls))

        st.session_state['raw_results'] = all_results
    else:
        st.warning("Пожалуйста, введите URL.")

# --- ВЫВОД РЕЗУЛЬТАТОВ ---
if st.session_state['raw_results']:
    # 1. Фильтруем данные из памяти по текущему значению слайдера
    full_data = pd.DataFrame(st.session_state['raw_results'])
    filtered_df = full_data[full_data['proba'] > threshold].copy()

    if not filtered_df.empty:
        st.success(f"Найдено товаров: {len(filtered_df)}")

        styled_df = filtered_df.style.background_gradient(
            subset=['proba'], cmap='YlGn').format({'Proba': "{:.2%}"})

        tab1, tab2 = st.tabs(["Общая таблица", "Группировка"])
        with tab1:
            st.dataframe(styled_df, width='stretch', height=500)
        with tab2:
            for source_url in filtered_df['URL'].unique():
                with st.expander(f"Источник: {source_url}"):
                    sub = filtered_df[filtered_df['URL'] == source_url][['name', 'proba']]
                    st.table(sub.style.background_gradient(subset=['proba'], cmap='YlGn'))
    else:
        st.warning("Нет товаров с такой уверенностью. Попробуйте снизить порог.")


st.divider()
st.caption("""
    Classification Report:
    
                        precision    recall  f1-score   support
        Not Furniture     0.9265    0.9403    0.9333        67
        Furniture         0.8400    0.8077    0.8235        26
        
        accuracy                              0.9032        93
        macro avg         0.8832    0.8740    0.8784        93
        weighted avg      0.9023    0.9032    0.9026        93
""")