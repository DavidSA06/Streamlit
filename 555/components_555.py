import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# Formatting functions
# ============================================================

def format_time(t):
    if t < 1e-6:
        return f"{t*1e9:.3f} ns"
    elif t < 1e-3:
        return f"{t*1e6:.3f} μs"
    elif t < 1:
        return f"{t*1e3:.3f} ms"
    else:
        return f"{t:.3f} s"


def format_frequency(f):
    if f < 1e3:
        return f"{f:.3f} Hz"
    elif f < 1e6:
        return f"{f/1e3:.3f} kHz"
    else:
        return f"{f/1e6:.3f} MHz"


def format_resistance(R):
    if R < 1e3:
        return f"{R:.2f} Ω"
    elif R < 1e6:
        return f"{R/1e3:.2f} kΩ"
    else:
        return f"{R/1e6:.2f} MΩ"


def format_capacitance(C):
    if C < 1e-9:
        return f"{C*1e12:.2f} pF"
    elif C < 1e-6:
        return f"{C*1e9:.2f} nF"
    elif C < 1e-3:
        return f"{C*1e6:.2f} μF"
    else:
        return f"{C*1e3:.2f} mF"


# ============================================================
# Unit conversion functions
# ============================================================

def convert_resistance(value, unit):
    factors = {
        "Ω": 1,
        "kΩ": 1e3,
        "MΩ": 1e6
    }
    return value * factors[unit]


def convert_capacitance(value, unit):
    factors = {
        "pF": 1e-12,
        "nF": 1e-9,
        "μF": 1e-6,
        "mF": 1e-3
    }
    return value * factors[unit]


def convert_frequency(value, unit):
    factors = {
        "Hz": 1,
        "kHz": 1e3,
        "MHz": 1e6
    }
    return value * factors[unit]


def convert_time(value, unit):
    factors = {
        "μs": 1e-6,
        "ms": 1e-3,
        "s": 1
    }
    return value * factors[unit]


# ============================================================
# 555 calculations
# ============================================================

def astable_classic(RA, RB, C):
    t_high = 0.693 * (RA + RB) * C
    t_low = 0.693 * RB * C
    period = t_high + t_low
    frequency = 1 / period
    duty_cycle = t_high / period

    return {
        "t_high": t_high,
        "t_low": t_low,
        "period": period,
        "frequency": frequency,
        "duty_cycle": duty_cycle
    }


def astable_diode(RA, RB, C):
    t_high = 0.693 * RA * C
    t_low = 0.693 * RB * C
    period = t_high + t_low
    frequency = 1 / period
    duty_cycle = t_high / period

    return {
        "t_high": t_high,
        "t_low": t_low,
        "period": period,
        "frequency": frequency,
        "duty_cycle": duty_cycle
    }


def monostable(R, C):
    return 1.1 * R * C


def design_astable_classic(frequency, duty_cycle, C):
    """
    Classic astable design.
    duty_cycle must be greater than 0.5.
    """
    S = 1.44 / (frequency * C)

    RA = S * (2 * duty_cycle - 1)
    RB = S * (1 - duty_cycle)

    return RA, RB


def design_astable_diode(frequency, duty_cycle, C):
    """
    Astable design with diode.
    """
    S = 1.44 / (frequency * C)

    RA = duty_cycle * S
    RB = (1 - duty_cycle) * S

    return RA, RB


def design_monostable(target_time, C):
    return target_time / (1.1 * C)


# ============================================================
# Plot functions
# ============================================================

def plot_astable_signal(t_high, t_low, cycles=3):
    period = t_high + t_low

    times = []
    output = []

    for n in range(cycles):
        t0 = n * period

        times.extend([
            t0,
            t0 + t_high,
            t0 + t_high,
            t0 + period
        ])

        output.extend([
            1,
            1,
            0,
            0
        ])

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.step(times, output, where="post")
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output")
    ax.set_title("Approximate output signal")
    ax.grid(True)

    return fig


def plot_monostable_signal(pulse_width):
    t = np.linspace(0, 2.5 * pulse_width, 400)
    y = np.where(t <= pulse_width, 1, 0)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.step(t, y, where="post")
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output")
    ax.set_title("Approximate output pulse")
    ax.grid(True)

    return fig


# ============================================================
# Warnings
# ============================================================

def resistance_warning_es(R, name):
    if R < 1e3:
        st.warning(
            f"{name} es menor que 1 kΩ. Puede exigir demasiada corriente al circuito."
        )
    elif R > 10e6:
        st.warning(
            f"{name} es mayor que 10 MΩ. El circuito puede volverse impreciso por fugas y ruido."
        )


def resistance_warning_en(R, name):
    if R < 1e3:
        st.warning(
            f"{name} is lower than 1 kΩ. This may cause excessive current in the circuit."
        )
    elif R > 10e6:
        st.warning(
            f"{name} is higher than 10 MΩ. The circuit may become inaccurate due to leakage currents and noise."
        )


def frequency_warning_es(f):
    if f > 100e3:
        st.warning(
            "La frecuencia es relativamente alta para un 555 bipolar clásico. "
            "Puede funcionar mejor con una versión CMOS, dependiendo del caso."
        )


def frequency_warning_en(f):
    if f > 100e3:
        st.warning(
            "The frequency is relatively high for a classic bipolar 555 timer. "
            "A CMOS version may be more suitable depending on the application."
        )


# ============================================================
# Page styling
# ============================================================

def apply_professional_style():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #555;
            margin-bottom: 1.8rem;
        }

        .section-card {
            padding: 1.2rem;
            background-color: #f7f7f9;
            border: 1px solid #e5e5ea;
            border-radius: 1rem;
            margin-bottom: 1rem;
        }

        .formula-note {
            color: #666;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )