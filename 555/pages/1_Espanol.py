import streamlit as st

from components_555 import (
    apply_professional_style,
    convert_resistance,
    convert_capacitance,
    convert_frequency,
    convert_time,
    format_time,
    format_frequency,
    format_resistance,
    astable_classic,
    astable_diode,
    monostable,
    design_astable_classic,
    design_astable_diode,
    design_monostable,
    plot_astable_signal,
    plot_monostable_signal,
    resistance_warning_es,
    frequency_warning_es
)

st.set_page_config(
    page_title="Calculadora 555",
    page_icon="⚡",
    layout="wide"
)

apply_professional_style()

st.markdown(
    """
    <div class="main-title">⚡ Calculadora para temporizador 555</div>
    <div class="subtitle">
    Calculadora educativa para el chip 555 en modo astable y monoestable.
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Las fórmulas son aproximaciones ideales. Para diseño real, revisa la hoja de datos del modelo específico del 555."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Astable",
        "Diseño astable",
        "Monoestable",
        "Diseño monoestable",
        "Notas del 555"
    ]
)

# ============================================================
# Astable directo
# ============================================================

with tab1:
    st.header("Modo astable")

    st.write(
        """
        En modo **astable**, el 555 genera una señal periódica sin necesidad de
        disparos externos. Es útil para generar pulsos, relojes simples, tonos
        y señales cuadradas aproximadas.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        RA_val = st.number_input("RA", min_value=0.001, value=10.0, step=1.0, key="es_RA")
        RA_unit = st.selectbox("Unidad de RA", ["Ω", "kΩ", "MΩ"], index=1, key="es_RA_unit")

    with col2:
        RB_val = st.number_input("RB", min_value=0.001, value=10.0, step=1.0, key="es_RB")
        RB_unit = st.selectbox("Unidad de RB", ["Ω", "kΩ", "MΩ"], index=1, key="es_RB_unit")

    with col3:
        C_val = st.number_input("C", min_value=0.001, value=10.0, step=1.0, key="es_C")
        C_unit = st.selectbox("Unidad de C", ["pF", "nF", "μF", "mF"], index=1, key="es_C_unit")

    tipo_astable = st.radio(
        "Tipo de conexión",
        [
            "Astable clásico",
            "Astable con diodo para duty menor a 50%"
        ],
        key="es_tipo_astable"
    )

    RA = convert_resistance(RA_val, RA_unit)
    RB = convert_resistance(RB_val, RB_unit)
    C = convert_capacitance(C_val, C_unit)

    if tipo_astable == "Astable clásico":
        result = astable_classic(RA, RB, C)
    else:
        result = astable_diode(RA, RB, C)

    st.subheader("Resultados")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Tiempo alto", format_time(result["t_high"]))
    col2.metric("Tiempo bajo", format_time(result["t_low"]))
    col3.metric("Periodo", format_time(result["period"]))
    col4.metric("Frecuencia", format_frequency(result["frequency"]))

    st.metric("Ciclo de trabajo", f"{100*result['duty_cycle']:.2f} %")

    resistance_warning_es(RA, "RA")
    resistance_warning_es(RB, "RB")
    frequency_warning_es(result["frequency"])

    st.subheader("Gráfica aproximada")

    fig = plot_astable_signal(result["t_high"], result["t_low"])
    st.pyplot(fig)

    st.subheader("Fórmulas")

    if tipo_astable == "Astable clásico":
        st.latex(r"t_{\text{alto}}=0.693(R_A+R_B)C")
        st.latex(r"t_{\text{bajo}}=0.693R_BC")
        st.latex(r"T=0.693(R_A+2R_B)C")
        st.latex(r"f=\frac{1.44}{(R_A+2R_B)C}")
        st.latex(r"D=\frac{R_A+R_B}{R_A+2R_B}")
    else:
        st.latex(r"t_{\text{alto}}=0.693R_AC")
        st.latex(r"t_{\text{bajo}}=0.693R_BC")
        st.latex(r"T=0.693(R_A+R_B)C")
        st.latex(r"f=\frac{1.44}{(R_A+R_B)C}")
        st.latex(r"D=\frac{R_A}{R_A+R_B}")


# ============================================================
# Diseño astable inverso
# ============================================================

with tab2:
    st.header("Diseño astable a partir de frecuencia y ciclo de trabajo")

    st.write(
        """
        Esta sección calcula valores aproximados de resistencias a partir de una
        frecuencia deseada, un ciclo de trabajo deseado y una capacitancia elegida.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        f_val = st.number_input(
            "Frecuencia deseada",
            min_value=0.001,
            value=1000.0,
            step=100.0,
            key="es_f_design"
        )
        f_unit = st.selectbox("Unidad de frecuencia", ["Hz", "kHz", "MHz"], index=0, key="es_f_unit")

    with col2:
        duty_deseado = st.slider(
            "Ciclo de trabajo deseado (%)",
            min_value=1.0,
            max_value=99.0,
            value=60.0,
            step=0.5,
            key="es_duty_design"
        )

    with col3:
        C_dis_val = st.number_input(
            "Capacitor elegido",
            min_value=0.001,
            value=10.0,
            step=1.0,
            key="es_C_design"
        )
        C_dis_unit = st.selectbox(
            "Unidad del capacitor",
            ["pF", "nF", "μF", "mF"],
            index=1,
            key="es_C_design_unit"
        )

    modo_diseno = st.radio(
        "Tipo de diseño",
        [
            "Astable clásico",
            "Astable con diodo"
        ],
        key="es_modo_diseno_astable"
    )

    f_obj = convert_frequency(f_val, f_unit)
    C_dis = convert_capacitance(C_dis_val, C_dis_unit)
    D = duty_deseado / 100

    st.subheader("Valores calculados")

    if modo_diseno == "Astable clásico":
        if D <= 0.5:
            st.error(
                """
                En el astable clásico, el ciclo de trabajo normalmente no puede
                ser menor o igual a 50 %. Para duty menor a 50 %, usa la configuración con diodo.
                """
            )
        else:
            RA_calc, RB_calc = design_astable_classic(f_obj, D, C_dis)
            result = astable_classic(RA_calc, RB_calc, C_dis)

            col1, col2, col3 = st.columns(3)

            col1.metric("RA aproximada", format_resistance(RA_calc))
            col2.metric("RB aproximada", format_resistance(RB_calc))
            col3.metric("Frecuencia estimada", format_frequency(result["frequency"]))

            st.metric("Duty estimado", f"{100*result['duty_cycle']:.2f} %")

            resistance_warning_es(RA_calc, "RA calculada")
            resistance_warning_es(RB_calc, "RB calculada")
            frequency_warning_es(result["frequency"])

            fig = plot_astable_signal(result["t_high"], result["t_low"])
            st.pyplot(fig)

            st.latex(r"R_A=(R_A+2R_B)(2D-1)")
            st.latex(r"R_B=(R_A+2R_B)(1-D)")
            st.latex(r"R_A+2R_B=\frac{1.44}{fC}")

    else:
        RA_calc, RB_calc = design_astable_diode(f_obj, D, C_dis)
        result = astable_diode(RA_calc, RB_calc, C_dis)

        col1, col2, col3 = st.columns(3)

        col1.metric("RA aproximada", format_resistance(RA_calc))
        col2.metric("RB aproximada", format_resistance(RB_calc))
        col3.metric("Frecuencia estimada", format_frequency(result["frequency"]))

        st.metric("Duty estimado", f"{100*result['duty_cycle']:.2f} %")

        resistance_warning_es(RA_calc, "RA calculada")
        resistance_warning_es(RB_calc, "RB calculada")
        frequency_warning_es(result["frequency"])

        fig = plot_astable_signal(result["t_high"], result["t_low"])
        st.pyplot(fig)

        st.latex(r"R_A=D(R_A+R_B)")
        st.latex(r"R_B=(1-D)(R_A+R_B)")
        st.latex(r"R_A+R_B=\frac{1.44}{fC}")


# ============================================================
# Monoestable directo
# ============================================================

with tab3:
    st.header("Modo monoestable")

    st.write(
        """
        En modo **monoestable**, el 555 genera un solo pulso de duración
        determinada cada vez que recibe un disparo.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        R_mono_val = st.number_input("R", min_value=0.001, value=10.0, step=1.0, key="es_R_mono")
        R_mono_unit = st.selectbox("Unidad de R", ["Ω", "kΩ", "MΩ"], index=1, key="es_R_mono_unit")

    with col2:
        C_mono_val = st.number_input("C", min_value=0.001, value=100.0, step=1.0, key="es_C_mono")
        C_mono_unit = st.selectbox("Unidad de C", ["pF", "nF", "μF", "mF"], index=2, key="es_C_mono_unit")

    R_mono = convert_resistance(R_mono_val, R_mono_unit)
    C_mono = convert_capacitance(C_mono_val, C_mono_unit)

    t_pulso = monostable(R_mono, C_mono)

    st.subheader("Resultado")

    st.metric("Duración del pulso", format_time(t_pulso))

    resistance_warning_es(R_mono, "R")

    fig = plot_monostable_signal(t_pulso)
    st.pyplot(fig)

    st.subheader("Fórmula")

    st.latex(r"t=1.1RC")


# ============================================================
# Diseño monoestable inverso
# ============================================================

with tab4:
    st.header("Diseño monoestable")

    st.write(
        """
        Esta sección calcula la resistencia necesaria para obtener una duración
        de pulso deseada usando un capacitor elegido.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        t_obj_val = st.number_input("Tiempo deseado", min_value=0.001, value=1.0, step=0.1, key="es_t_obj")
        t_obj_unit = st.selectbox("Unidad del tiempo", ["μs", "ms", "s"], index=1, key="es_t_obj_unit")

    with col2:
        C_obj_val = st.number_input("Capacitor elegido", min_value=0.001, value=100.0, step=1.0, key="es_C_obj")
        C_obj_unit = st.selectbox("Unidad del capacitor", ["pF", "nF", "μF", "mF"], index=2, key="es_C_obj_unit")

    t_obj = convert_time(t_obj_val, t_obj_unit)
    C_obj = convert_capacitance(C_obj_val, C_obj_unit)

    R_necesaria = design_monostable(t_obj, C_obj)

    st.subheader("Resultado")

    st.metric("Resistencia necesaria", format_resistance(R_necesaria))

    resistance_warning_es(R_necesaria, "R calculada")

    fig = plot_monostable_signal(t_obj)
    st.pyplot(fig)

    st.subheader("Fórmula despejada")

    st.latex(r"t=1.1RC")
    st.latex(r"R=\frac{t}{1.1C}")


# ============================================================
# Notas
# ============================================================

with tab5:
    st.header("Notas prácticas sobre el temporizador 555")

    st.subheader("Pines típicos del 555")

    st.markdown(
        """
        | Pin | Nombre | Función |
        |---:|---|---|
        | 1 | GND | Tierra |
        | 2 | Trigger | Disparo |
        | 3 | Output | Salida |
        | 4 | Reset | Reinicio |
        | 5 | Control Voltage | Control de voltaje |
        | 6 | Threshold | Umbral |
        | 7 | Discharge | Descarga |
        | 8 | VCC | Alimentación |
        """
    )

    st.subheader("Recomendaciones prácticas")

    st.markdown(
        """
        - Usa un capacitor de desacoplo de aproximadamente **100 nF** entre VCC y GND.
        - En el pin 5 suele colocarse un capacitor pequeño, por ejemplo **10 nF**, hacia tierra.
        - Evita resistencias demasiado pequeñas, porque aumentan el consumo de corriente.
        - Evita resistencias demasiado grandes, porque las fugas pueden afectar el tiempo.
        - El 555 bipolar clásico consume más corriente que versiones CMOS como TLC555 o LMC555.
        - Las fórmulas son aproximadas; los capacitores reales pueden tener tolerancias grandes.
        - Para ciclos de trabajo menores a 50 %, conviene usar la configuración con diodo.
        """
    )

    st.subheader("Resumen de fórmulas")

    st.markdown("### Astable clásico")

    st.latex(r"t_{\text{alto}}=0.693(R_A+R_B)C")
    st.latex(r"t_{\text{bajo}}=0.693R_BC")
    st.latex(r"T=0.693(R_A+2R_B)C")
    st.latex(r"f=\frac{1.44}{(R_A+2R_B)C}")
    st.latex(r"D=\frac{R_A+R_B}{R_A+2R_B}")

    st.markdown("### Astable con diodo")

    st.latex(r"t_{\text{alto}}=0.693R_AC")
    st.latex(r"t_{\text{bajo}}=0.693R_BC")
    st.latex(r"T=0.693(R_A+R_B)C")
    st.latex(r"f=\frac{1.44}{(R_A+R_B)C}")
    st.latex(r"D=\frac{R_A}{R_A+R_B}")

    st.markdown("### Monoestable")

    st.latex(r"t=1.1RC")