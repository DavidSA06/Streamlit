import streamlit as st

st.set_page_config(
    page_title="555 Timer Calculator",
    page_icon="⚡",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.15rem;
        color: #555;
        margin-bottom: 2rem;
    }

    .card {
        padding: 1.4rem;
        border-radius: 1rem;
        background-color: #f7f7f9;
        border: 1px solid #e3e3e8;
        margin-bottom: 1rem;
    }

    .small-note {
        font-size: 0.95rem;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">⚡ 555 Timer Calculator</div>
    <div class="subtitle">
    Interactive educational calculator for the 555 timer IC.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="card">
    <h3>Welcome / Bienvenido</h3>

    This app contains calculators for the 555 timer IC in:

    <ul>
        <li>Astable mode</li>
        <li>Monostable mode</li>
        <li>Inverse design from desired frequency, duty cycle, or pulse width</li>
        <li>Educational formulas and practical notes</li>
    </ul>

    Use the sidebar to choose the language page.

    <hr>

    Esta app contiene calculadoras para el temporizador 555 en:

    <ul>
        <li>Modo astable</li>
        <li>Modo monoestable</li>
        <li>Diseño inverso a partir de frecuencia, ciclo de trabajo o duración de pulso</li>
        <li>Fórmulas educativas y notas prácticas</li>
    </ul>

    Usa la barra lateral para elegir el idioma.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.info("🇲🇽 Go to **Español** in the sidebar.")

with col2:
    st.info("🇺🇸 Go to **English** in the sidebar.")

st.markdown(
    """
    <p class="small-note">
    Educational use only. For real circuit design, always check the datasheet
    of the specific 555 timer model you are using.
    </p>
    """,
    unsafe_allow_html=True
)