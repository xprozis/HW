import streamlit as st


def single_space():
    st.markdown("")

def double_space():
    st.markdown("")
    st.markdown("")

def page_header(title, description):
    """
    Gera um cabeçalho identico para todos
    
    """
    st.title(title,help=description)
    single_space()
    st.image("./pages/shared/Logo_Prozis.png")
    st.markdown(
    """
    <style>
        img {
            position: fixed;
            padding-top: 25rem;
            opacity: 30%;
        }

    </style>
    """,
    unsafe_allow_html=True
)


