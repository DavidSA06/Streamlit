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
    resistance_warning_en,
    frequency_warning_en
)

st.set_page_config(
    page_title="555 Timer Calculator",
    page_icon="⚡",
    layout="wide"
)

apply_professional_style()

st.markdown(
    """
    <div class="main-title">⚡ 555 Timer Calculator</div>
    <div class="subtitle">
    Educational calculator for the 555 timer IC in astable and monostable modes.
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "The formulas are ideal approximations. For real circuit design, check the datasheet of the specific 555 timer model."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Astable Mode",
        "Astable Design",
        "Monostable Mode",
        "Monostable Design",
        "555 Notes"
    ]
)

# ============================================================
# Direct astable mode
# ============================================================

with tab1:
    st.header("Astable Mode")

    st.write(
        """
        In **astable mode**, the 555 timer generates a periodic signal without
        requiring an external trigger. It is useful for pulse generation,
        simple clock signals, tones, and square-wave-like signals.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        RA_val = st.number_input("RA", min_value=0.001, value=10.0, step=1.0, key="en_RA")
        RA_unit = st.selectbox("RA unit", ["Ω", "kΩ", "MΩ"], index=1, key="en_RA_unit")

    with col2:
        RB_val = st.number_input("RB", min_value=0.001, value=10.0, step=1.0, key="en_RB")
        RB_unit = st.selectbox("RB unit", ["Ω", "kΩ", "MΩ"], index=1, key="en_RB_unit")

    with col3:
        C_val = st.number_input("C", min_value=0.001, value=10.0, step=1.0, key="en_C")
        C_unit = st.selectbox("C unit", ["pF", "nF", "μF", "mF"], index=1, key="en_C_unit")

    astable_type = st.radio(
        "Connection type",
        [
            "Classic astable",
            "Astable with diode for duty cycle below 50%"
        ],
        key="en_astable_type"
    )

    RA = convert_resistance(RA_val, RA_unit)
    RB = convert_resistance(RB_val, RB_unit)
    C = convert_capacitance(C_val, C_unit)

    if astable_type == "Classic astable":
        result = astable_classic(RA, RB, C)
    else:
        result = astable_diode(RA, RB, C)

    st.subheader("Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("High time", format_time(result["t_high"]))
    col2.metric("Low time", format_time(result["t_low"]))
    col3.metric("Period", format_time(result["period"]))
    col4.metric("Frequency", format_frequency(result["frequency"]))

    st.metric("Duty cycle", f"{100*result['duty_cycle']:.2f} %")

    resistance_warning_en(RA, "RA")
    resistance_warning_en(RB, "RB")
    frequency_warning_en(result["frequency"])

    st.subheader("Approximate waveform")

    fig = plot_astable_signal(result["t_high"], result["t_low"])
    st.pyplot(fig)

    st.subheader("Formulas")

    if astable_type == "Classic astable":
        st.latex(r"t_{\text{high}}=0.693(R_A+R_B)C")
        st.latex(r"t_{\text{low}}=0.693R_BC")
        st.latex(r"T=0.693(R_A+2R_B)C")
        st.latex(r"f=\frac{1.44}{(R_A+2R_B)C}")
        st.latex(r"D=\frac{R_A+R_B}{R_A+2R_B}")
    else:
        st.latex(r"t_{\text{high}}=0.693R_AC")
        st.latex(r"t_{\text{low}}=0.693R_BC")
        st.latex(r"T=0.693(R_A+R_B)C")
        st.latex(r"f=\frac{1.44}{(R_A+R_B)C}")
        st.latex(r"D=\frac{R_A}{R_A+R_B}")


# ============================================================
# Inverse astable design
# ============================================================

with tab2:
    st.header("Astable Design from Frequency and Duty Cycle")

    st.write(
        """
        This section calculates approximate resistor values from a desired
        frequency, a desired duty cycle, and a selected capacitor value.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        f_val = st.number_input(
            "Desired frequency",
            min_value=0.001,
            value=1000.0,
            step=100.0,
            key="en_f_design"
        )
        f_unit = st.selectbox("Frequency unit", ["Hz", "kHz", "MHz"], index=0, key="en_f_unit")

    with col2:
        desired_duty = st.slider(
            "Desired duty cycle (%)",
            min_value=1.0,
            max_value=99.0,
            value=60.0,
            step=0.5,
            key="en_duty_design"
        )

    with col3:
        C_design_val = st.number_input(
            "Selected capacitor",
            min_value=0.001,
            value=10.0,
            step=1.0,
            key="en_C_design"
        )
        C_design_unit = st.selectbox(
            "Selected capacitor unit",
            ["pF", "nF", "μF", "mF"],
            index=1,
            key="en_C_design_unit"
        )

    design_mode = st.radio(
        "Design type",
        [
            "Classic astable",
            "Astable with diode"
        ],
        key="en_astable_design_mode"
    )

    target_frequency = convert_frequency(f_val, f_unit)
    C_design = convert_capacitance(C_design_val, C_design_unit)
    D = desired_duty / 100

    st.subheader("Calculated values")

    if design_mode == "Classic astable":
        if D <= 0.5:
            st.error(
                """
                In the classic astable configuration, the duty cycle normally
                cannot be less than or equal to 50%. For a duty cycle below
                50%, use the diode configuration.
                """
            )
        else:
            RA_calc, RB_calc = design_astable_classic(target_frequency, D, C_design)
            result = astable_classic(RA_calc, RB_calc, C_design)

            col1, col2, col3 = st.columns(3)

            col1.metric("Approximate RA", format_resistance(RA_calc))
            col2.metric("Approximate RB", format_resistance(RB_calc))
            col3.metric("Estimated frequency", format_frequency(result["frequency"]))

            st.metric("Estimated duty cycle", f"{100*result['duty_cycle']:.2f} %")

            resistance_warning_en(RA_calc, "Calculated RA")
            resistance_warning_en(RB_calc, "Calculated RB")
            frequency_warning_en(result["frequency"])

            fig = plot_astable_signal(result["t_high"], result["t_low"])
            st.pyplot(fig)

            st.latex(r"R_A=(R_A+2R_B)(2D-1)")
            st.latex(r"R_B=(R_A+2R_B)(1-D)")
            st.latex(r"R_A+2R_B=\frac{1.44}{fC}")

    else:
        RA_calc, RB_calc = design_astable_diode(target_frequency, D, C_design)
        result = astable_diode(RA_calc, RB_calc, C_design)

        col1, col2, col3 = st.columns(3)

        col1.metric("Approximate RA", format_resistance(RA_calc))
        col2.metric("Approximate RB", format_resistance(RB_calc))
        col3.metric("Estimated frequency", format_frequency(result["frequency"]))

        st.metric("Estimated duty cycle", f"{100*result['duty_cycle']:.2f} %")

        resistance_warning_en(RA_calc, "Calculated RA")
        resistance_warning_en(RB_calc, "Calculated RB")
        frequency_warning_en(result["frequency"])

        fig = plot_astable_signal(result["t_high"], result["t_low"])
        st.pyplot(fig)

        st.latex(r"R_A=D(R_A+R_B)")
        st.latex(r"R_B=(1-D)(R_A+R_B)")
        st.latex(r"R_A+R_B=\frac{1.44}{fC}")


# ============================================================
# Direct monostable mode
# ============================================================

with tab3:
    st.header("Monostable Mode")

    st.write(
        """
        In **monostable mode**, the 555 timer generates a single output pulse
        of fixed duration every time it receives a trigger.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        R_mono_val = st.number_input("R", min_value=0.001, value=10.0, step=1.0, key="en_R_mono")
        R_mono_unit = st.selectbox("R unit", ["Ω", "kΩ", "MΩ"], index=1, key="en_R_mono_unit")

    with col2:
        C_mono_val = st.number_input("C", min_value=0.001, value=100.0, step=1.0, key="en_C_mono")
        C_mono_unit = st.selectbox("C unit", ["pF", "nF", "μF", "mF"], index=2, key="en_C_mono_unit")

    R_mono = convert_resistance(R_mono_val, R_mono_unit)
    C_mono = convert_capacitance(C_mono_val, C_mono_unit)

    pulse_width = monostable(R_mono, C_mono)

    st.subheader("Result")

    st.metric("Pulse width", format_time(pulse_width))

    resistance_warning_en(R_mono, "R")

    fig = plot_monostable_signal(pulse_width)
    st.pyplot(fig)

    st.subheader("Formula")

    st.latex(r"t=1.1RC")


# ============================================================
# Inverse monostable design
# ============================================================

with tab4:
    st.header("Monostable Design")

    st.write(
        """
        This section calculates the required resistance to obtain a desired
        pulse width using a selected capacitor value.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        target_time_val = st.number_input(
            "Desired pulse width",
            min_value=0.001,
            value=1.0,
            step=0.1,
            key="en_target_time"
        )
        target_time_unit = st.selectbox("Time unit", ["μs", "ms", "s"], index=1, key="en_target_time_unit")

    with col2:
        C_target_val = st.number_input(
            "Selected capacitor",
            min_value=0.001,
            value=100.0,
            step=1.0,
            key="en_C_target"
        )
        C_target_unit = st.selectbox(
            "Selected capacitor unit",
            ["pF", "nF", "μF", "mF"],
            index=2,
            key="en_C_target_unit"
        )

    target_time = convert_time(target_time_val, target_time_unit)
    C_target = convert_capacitance(C_target_val, C_target_unit)

    required_R = design_monostable(target_time, C_target)

    st.subheader("Result")

    st.metric("Required resistance", format_resistance(required_R))

    resistance_warning_en(required_R, "Calculated R")

    fig = plot_monostable_signal(target_time)
    st.pyplot(fig)

    st.subheader("Rearranged formula")

    st.latex(r"t=1.1RC")
    st.latex(r"R=\frac{t}{1.1C}")


# ============================================================
# Notes
# ============================================================

with tab5:
    st.header("Practical Notes about the 555 Timer")

    st.subheader("Typical 555 pinout")

    st.markdown(
        """
        | Pin | Name | Function |
        |---:|---|---|
        | 1 | GND | Ground |
        | 2 | Trigger | Starts the timing cycle |
        | 3 | Output | Output signal |
        | 4 | Reset | Resets the timer |
        | 5 | Control Voltage | Adjusts internal threshold levels |
        | 6 | Threshold | Detects capacitor voltage |
        | 7 | Discharge | Discharges the timing capacitor |
        | 8 | VCC | Supply voltage |
        """
    )

    st.subheader("Practical recommendations")

    st.markdown(
        """
        - Use a decoupling capacitor of about **100 nF** between VCC and GND.
        - A small capacitor, often around **10 nF**, is commonly connected from pin 5 to ground.
        - Avoid very small resistor values because they increase current consumption.
        - Avoid very large resistor values because leakage currents may affect timing accuracy.
        - The classic bipolar 555 consumes more current than CMOS versions such as TLC555 or LMC555.
        - The formulas are approximations; real capacitors can have large tolerances.
        - For duty cycles below 50%, the diode configuration is usually more appropriate.
        """
    )

    st.subheader("Formula summary")

    st.markdown("### Classic astable mode")

    st.latex(r"t_{\text{high}}=0.693(R_A+R_B)C")
    st.latex(r"t_{\text{low}}=0.693R_BC")
    st.latex(r"T=0.693(R_A+2R_B)C")
    st.latex(r"f=\frac{1.44}{(R_A+2R_B)C}")
    st.latex(r"D=\frac{R_A+R_B}{R_A+2R_B}")

    st.markdown("### Astable mode with diode")

    st.latex(r"t_{\text{high}}=0.693R_AC")
    st.latex(r"t_{\text{low}}=0.693R_BC")
    st.latex(r"T=0.693(R_A+R_B)C")
    st.latex(r"f=\frac{1.44}{(R_A+R_B)C}")
    st.latex(r"D=\frac{R_A}{R_A+R_B}")

    st.markdown("### Monostable mode")

    st.latex(r"t=1.1RC")