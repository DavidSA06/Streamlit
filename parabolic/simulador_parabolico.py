import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulador de movimiento parabólico",
    layout="centered"
)

st.title("Simulador de movimiento parabólico")

st.write(
    """
    Modifica los parámetros iniciales y observa cómo cambia la trayectoria
    de un proyectil sin resistencia del aire.
    """
)

# Controles
v0 = st.slider(
    "Velocidad inicial $v_0$ en m/s",
    min_value=5,
    max_value=60,
    value=20,
    step=1
)

theta_deg = st.slider(
    "Ángulo de lanzamiento en grados",
    min_value=5,
    max_value=85,
    value=45,
    step=1
)

g = st.slider(
    "Aceleración de la gravedad $g$ en m/s²",
    min_value=1.0,
    max_value=20.0,
    value=9.81,
    step=0.01
)

# Cálculos
theta = np.radians(theta_deg)

t_total = 2 * v0 * np.sin(theta) / g
alcance = v0**2 * np.sin(2 * theta) / g
altura_max = (v0**2 * np.sin(theta)**2) / (2 * g)

t = np.linspace(0, t_total, 300)

x = v0 * np.cos(theta) * t
y = v0 * np.sin(theta) * t - 0.5 * g * t**2

# Resultados numéricos
col1, col2, col3 = st.columns(3)

col1.metric("Tiempo de vuelo", f"{t_total:.2f} s")
col2.metric("Alcance", f"{alcance:.2f} m")
col3.metric("Altura máxima", f"{altura_max:.2f} m")

# Gráfica
fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(x, y)
ax.axhline(0, linewidth=1)
ax.set_xlabel("Distancia horizontal x (m)")
ax.set_ylabel("Altura y (m)")
ax.set_title("Trayectoria del proyectil")
ax.grid(True)

st.pyplot(fig)

# Fórmulas
st.subheader("Modelo matemático")

st.latex(r"x(t)=v_0\cos(\theta)t")

st.latex(r"y(t)=v_0\sin(\theta)t-\frac{1}{2}gt^2")

st.latex(r"R=\frac{v_0^2\sin(2\theta)}{g}")

st.latex(r"H_{\max}=\frac{v_0^2\sin^2(\theta)}{2g}")
