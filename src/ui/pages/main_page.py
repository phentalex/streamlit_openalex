import asyncio
import streamlit as st
import aiohttp  
from ui.utils.data_processing import check_authentication
from pagination import show_result_as_page

API_URL = "http://188.235.1.122:8000"

st.set_page_config(layout="wide")

async def search_articles(query, num_articles, min_year, max_year, min_score, match_type):
    params = {
        "query": query,
        "num_articles": num_articles,
        "min_year": min_year,
        "max_year": max_year,
        "min_score": min_score,
        "match_type": match_type  # Добавляем тип поиска
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/search", params=params) as response:
            if response.status == 200:
                return await response.json()
            return None

#@check_authentication
async def main():
    if "articles" not in st.session_state:
        st.session_state.articles = []
    if "total_articles" not in st.session_state:
        st.session_state.total_articles = 0
    if "query" not in st.session_state:
        st.session_state.query = ""

    # Фильтры поиска
    with st.sidebar:
        st.header("🔍 Фильтры поиска")
        num_articles = st.number_input("Количество статей", min_value=1, max_value=100, value=10, step=1)
        min_year = st.number_input("Минимальный год", min_value=1900, max_value=2025, value=2000, step=1)
        max_year = st.number_input("Максимальный год", min_value=1900, max_value=2025, value=2025, step=1)
        min_score = st.slider("Минимальный рейтинг", min_value=1.00, max_value=50.0, value=1.00, step=0.1)
        
        # Выбор типа поиска: Умный поиск или Дословное совпадение
        search_type = st.radio(
            "Тип поиска", 
            options=["Умный поиск", "Дословный поиск"], 
            index=0, 
            help="Выберите тип поиска: 'Умный поиск' для поиска по релевантным запросам или 'Дословный поиск' для поиска по ключевым словам."
        )

    st.write("#### Поиск статей:")

    container0 = st.container(border=True)

    with container0:
        col1, col2 = st.columns([9, 1])
        with col1:
            query = st.text_input(
                "Поиск",
                placeholder="Введите поисковый запрос...",
                help="Например: Deep Learning, NLP, Data Science",
                label_visibility="collapsed"
            )

        with col2:
            search_button = st.button("Искать", use_container_width=True)

        if search_button and query:
            st.session_state.query = query
            st.session_state.page = 1

            match_type = "relevant" if search_type == "Умный поиск" else "exact"

            with st.spinner("🔍 Выполняем поиск..."):
                results = await search_articles(st.session_state.query, num_articles, min_year, max_year, min_score, match_type)

                if results:
                    st.session_state.articles = results.get("hits", [])
                    st.session_state.total_articles = results.get("total", 0)
                st.rerun()
                    
        
    # Примеры запросов
    col1, col2, col3, col4 = st.columns([2, 3, 3, 3])
    with col1:
        st.write(f"#### Примеры запросов:")

    with col2:
        if st.button("Deep Learning", use_container_width=True):
            st.session_state.query = "Deep Learning"
            st.session_state.page = 1
            match_type = "relevant" if search_type == "Умный поиск" else "exact"
            with st.spinner("🔍 Выполняем поиск..."):
                results = await search_articles(st.session_state.query, num_articles, min_year, max_year, min_score, match_type)
                if results:
                    st.session_state.articles = results.get("hits", [])
                    st.session_state.total_articles = results.get("total", 0)
                st.rerun()

    with col3:
        if st.button("NLP", use_container_width=True):
            st.session_state.query = "NLP"
            st.session_state.page = 1
            match_type = "relevant" if search_type == "Умный поиск" else "exact"
            with st.spinner("🔍 Выполняем поиск..."):
                results = await search_articles(st.session_state.query, num_articles, min_year, max_year, min_score, match_type)
                if results:
                    st.session_state.articles = results.get("hits", [])
                    st.session_state.total_articles = results.get("total", 0)
                st.rerun()

    with col4:
        if st.button("Data Science", use_container_width=True):
            st.session_state.query = "Data Science"
            st.session_state.page = 1
            match_type = "relevant" if search_type == "Умный поиск" else "exact"
            with st.spinner("🔍 Выполняем поиск..."):
                results = await search_articles(st.session_state.query, num_articles, min_year, max_year, min_score, match_type)
                if results:
                    st.session_state.articles = results.get("hits", [])
                    st.session_state.total_articles = results.get("total", 0)
                st.rerun()

    if st.session_state.articles:
    # Если найдено хотя бы одно совпадение
        articles_list = [
        {
            "title": item['_source'].get('title', '') or item.get('title', ''),
            "doi": item['_source'].get('doi', '') or item.get('doi', ''),
            "authorships": ', '.join([author.get('name', '') for author in item.get('_source', {}).get('authorships', [])]),
            "keywords": ', '.join(item['_source'].get('keywords', []) or item.get('keywords', [])),
            "abstract_cut": item['_source'].get('abstract', '')[:300] + "..." if '_source' in item else '',
            "abstract": item['_source'].get('abstract', '') or item.get('abstract', ''),
            "publication_year": item['_source'].get('publication_year', '') or item.get('publication_year', ''),
            "type": item['_source'].get('type', '') or item.get('type', ''),
            "work_citation": item['_source'].get('cited_by_count', '') or item.get('cited_by_count', '')
        }
        for item in st.session_state.articles
    ]
        html_output = show_result_as_page(articles_list)

        container = st.container(border=True)
        with container:
            st.components.v1.html(html_output, height=600, scrolling=True)


if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной main()
