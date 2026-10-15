from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title='AInote Log',page_icon='📝',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>header[data-testid="stHeader"]{display:none} .block-container{padding:0!important;max-width:100%!important} iframe{display:block} [data-testid="stAppViewContainer"]{background:#111827}</style>''',unsafe_allow_html=True)
components.html(Path(__file__).parent.joinpath('frontend/index.html').read_text(encoding='utf-8'),height=900,scrolling=False)
