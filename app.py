import streamlit as st
from urllib.parse import urlparse

from rag.models import load_models
from rag.loader import load_wikipedia
from rag.vectorstore import create_vector_store
from rag.prompt import prompt
from rag.chain import get_response


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Wikipedia FAQ Bot",
    page_icon="📚"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "wiki_url" not in st.session_state:
    st.session_state.wiki_url = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# URL SCREEN
# --------------------------------------------------

if st.session_state.wiki_url is None:


    st.markdown(
        """
        <style>
        .url-container {
            max-width: 700px;
            margin: 80px auto;
        }

        .url-title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="url-container">
            <div class="url-title">
                Enter Wikipedia URL
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    url = st.text_input(
        " ",
        placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence"
    )

    if st.button("Continue"):

        parsed_url = urlparse(url)

        if (
            parsed_url.netloc == "en.wikipedia.org"
            and parsed_url.path.startswith("/wiki/")
        ):

            with st.spinner("Loading Wikipedia page..."):

                try:

                    # Load Wikipedia page
                    docs = load_wikipedia(url)

                    # Load embeddings
                    embeddings, chat_model = load_models()

                    # Create vector store
                    vector_store = create_vector_store(
                        docs,
                        embeddings
                    )

                    # Create retriever
                    retriever = vector_store.as_retriever(
                        search_kwargs={"k": 3}
                    )

                    # Store everything in session state
                    st.session_state.wiki_url = url
                    st.session_state.retriever = retriever
                    st.session_state.chat_model = chat_model

                    st.session_state.messages = []

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to load this Wikipedia page: {e}"
                    )

        else:

            st.error("Enter a valid Wikipedia URL")


# --------------------------------------------------
# CHATBOT SCREEN
# --------------------------------------------------

else:

    st.markdown(
        """
        <style>
        .chat-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 65px;
            background-color: transparent;
            z-index: 999999;
            display: flex;
            align-items: left;
            justify-content: center;
        }

        .chat-header h1 {
            margin: 0;
            font-size: 28px;
        }

        /* Push chat content below the fixed header */
        .main .block-container {
            padding-top: 90px;
        }
        </style>

        <div class="chat-header"  >
            <h1>Wikipedia FAQ Bot</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # DISPLAY PREVIOUS MESSAGES
    # --------------------------------------------------

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    margin: 10px 0;
                ">
                    <div style="
                        max-width: 70%;
                        padding: 10px 15px;
                        border-radius: 15px;
                        text-align: right;
                    ">
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    margin: 10px 0;
                ">
                    <div style="
                        max-width: 70%;
                        padding: 10px 15px;
                        border-radius: 15px;
                        text-align: left;
                    ">
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------
    # USER INPUT
    # --------------------------------------------------

    question = st.chat_input(
        "Ask something about this Wikipedia page..."
    )


    if question:

        # --------------------------------------------------
        # DISPLAY USER MESSAGE
        # --------------------------------------------------

        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin: 10px 0;
            ">
                <div style="
                    max-width: 70%;
                    padding: 10px 15px;
                    border-radius: 15px;
                    text-align: right;
                ">
                    {question}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # Save user message

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })


        # --------------------------------------------------
        # THINKING
        # --------------------------------------------------

        with st.spinner("Thinking..."):

            history = []

            for message in st.session_state.messages[:-1]:

                if message["role"] == "user":

                    history.append(
                        ("human", message["content"])
                    )

                else:

                    history.append(
                        ("ai", message["content"])
                    )


            # Get response

            response = get_response(
                question,
                st.session_state.retriever,
                prompt,
                st.session_state.chat_model,
                history
            )


        # --------------------------------------------------
        # DISPLAY AI RESPONSE
        # --------------------------------------------------

        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                margin: 10px 0;
            ">
                <div style="
                    max-width: 70%;
                    padding: 10px 15px;
                    border-radius: 15px;
                    text-align: left;
                ">
                    {response}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # Save AI response

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })