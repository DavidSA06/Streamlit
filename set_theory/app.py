import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib_venn import venn2
from itertools import product


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="Set Theory Explorer",
    page_icon="∈",
    layout="wide"
)


# ============================================================
# Text dictionary
# ============================================================

TEXT = {
    "es": {
        "language": "Idioma",
        "title": "∈ Explorador de teoría de conjuntos",
        "subtitle": "Recurso interactivo para estudiar conjuntos, operaciones y producto cartesiano.",
        "sidebar_title": "Conjuntos de trabajo",
        "universe": "Conjunto universal U",
        "set_a": "Conjunto A",
        "set_b": "Conjunto B",
        "input_help": "Escribe los elementos separados por comas. Ejemplo: 1, 2, 3, 4",
        "warning_universe": "Algunos elementos de A o B no estaban en U. Se agregaron automáticamente al conjunto universal para poder calcular complementos.",
        "tabs": ["Conceptos", "Calculadora", "Diagramas de Venn", "Producto cartesiano", "Ejercicios"],
        "current_sets": "Conjuntos actuales",
        "concepts_intro": """
        Un **conjunto** es una colección bien definida de objetos llamados **elementos**. 
        Los conjuntos suelen representarse con letras mayúsculas, como \(A\), \(B\) o \(U\).
        """,
        "notation_title": "Notación básica",
        "operations_title": "Operaciones principales",
        "calculator_title": "Calculadora de operaciones",
        "properties_title": "Propiedades entre conjuntos",
        "venn_title": "Diagrama de Venn",
        "select_operation": "Selecciona la operación a visualizar",
        "cartesian_title": "Producto cartesiano",
        "practice_title": "Ejercicios rápidos",
        "show_answer": "Mostrar respuesta",
        "operation": "Operación",
        "result": "Resultado",
        "description": "Descripción",
        "cardinality": "Cardinalidad",
        "true": "Verdadero",
        "false": "Falso",
        "empty": "∅",
        "outside": "Elementos fuera de A y B",
        "region_elements": "Elementos por región",
        "too_many_pairs": "Hay demasiados pares ordenados. Se muestran solo los primeros.",
        "ordered_pairs": "Pares ordenados",
        "show_bxa": "Mostrar también B × A",
        "exercise_type": "Tipo de ejercicio",
        "exercise_operation": "Calcular una operación",
        "exercise_cardinality": "Calcular cardinalidad",
        "exercise_relation": "Analizar relación entre conjuntos",
        "choose_operation": "Operación",
        "educational_note": "Esta app está pensada como recurso educativo. Los elementos se tratan como texto, por lo que 1 y 01 se consideran elementos diferentes.",
        "venn_note": "El diagrama representa las regiones de A y B dentro del conjunto universal U.",
    },
    "en": {
        "language": "Language",
        "title": "∈ Set Theory Explorer",
        "subtitle": "Interactive resource for studying sets, operations, and Cartesian products.",
        "sidebar_title": "Working sets",
        "universe": "Universal set U",
        "set_a": "Set A",
        "set_b": "Set B",
        "input_help": "Enter elements separated by commas. Example: 1, 2, 3, 4",
        "warning_universe": "Some elements of A or B were not in U. They were automatically added to the universal set so complements can be computed.",
        "tabs": ["Concepts", "Calculator", "Venn Diagrams", "Cartesian Product", "Exercises"],
        "current_sets": "Current sets",
        "concepts_intro": """
        A **set** is a well-defined collection of objects called **elements**. 
        Sets are usually denoted by uppercase letters, such as \(A\), \(B\), or \(U\).
        """,
        "notation_title": "Basic notation",
        "operations_title": "Main operations",
        "calculator_title": "Operations calculator",
        "properties_title": "Set relationships",
        "venn_title": "Venn diagram",
        "select_operation": "Select the operation to visualize",
        "cartesian_title": "Cartesian product",
        "practice_title": "Quick exercises",
        "show_answer": "Show answer",
        "operation": "Operation",
        "result": "Result",
        "description": "Description",
        "cardinality": "Cardinality",
        "true": "True",
        "false": "False",
        "empty": "∅",
        "outside": "Elements outside A and B",
        "region_elements": "Elements by region",
        "too_many_pairs": "There are too many ordered pairs. Only the first ones are shown.",
        "ordered_pairs": "Ordered pairs",
        "show_bxa": "Also show B × A",
        "exercise_type": "Exercise type",
        "exercise_operation": "Compute an operation",
        "exercise_cardinality": "Compute cardinality",
        "exercise_relation": "Analyze a set relationship",
        "choose_operation": "Operation",
        "educational_note": "This app is intended as an educational resource. Elements are treated as text, so 1 and 01 are considered different elements.",
        "venn_note": "The diagram represents the regions of A and B inside the universal set U.",
    }
}


# ============================================================
# Helper functions
# ============================================================

def parse_set(text):
    """
    Converts a comma-separated string into a Python set of strings.
    """
    if text.strip() == "":
        return set()

    return {
        item.strip()
        for item in text.split(",")
        if item.strip() != ""
    }


def sort_items(s):
    return sorted(s, key=lambda x: str(x).lower())


def format_set(s):
    if len(s) == 0:
        return "∅"
    return "{" + ", ".join(sort_items(s)) + "}"


def format_region_label(s, max_items=6):
    """
    Short label for Venn diagram regions.
    """
    if len(s) == 0:
        return "∅"

    items = sort_items(s)

    if len(items) <= max_items:
        return "\n".join(items)

    visible = items[:max_items]
    remaining = len(items) - max_items

    return "\n".join(visible) + f"\n+{remaining}"


def set_to_table(s):
    return [{"Elemento": item} for item in sort_items(s)]


def operation_dict(A, B, U, lang):
    if lang == "es":
        return {
            "A ∪ B": {
                "value": A | B,
                "description": "Elementos que pertenecen a A, a B o a ambos."
            },
            "A ∩ B": {
                "value": A & B,
                "description": "Elementos que pertenecen simultáneamente a A y a B."
            },
            "A - B": {
                "value": A - B,
                "description": "Elementos que pertenecen a A pero no a B."
            },
            "B - A": {
                "value": B - A,
                "description": "Elementos que pertenecen a B pero no a A."
            },
            "A Δ B": {
                "value": A ^ B,
                "description": "Elementos que pertenecen a exactamente uno de los dos conjuntos."
            },
            "Aᶜ": {
                "value": U - A,
                "description": "Elementos del conjunto universal que no pertenecen a A."
            },
            "Bᶜ": {
                "value": U - B,
                "description": "Elementos del conjunto universal que no pertenecen a B."
            },
        }

    return {
        "A ∪ B": {
            "value": A | B,
            "description": "Elements that belong to A, to B, or to both."
        },
        "A ∩ B": {
            "value": A & B,
            "description": "Elements that belong to both A and B."
        },
        "A - B": {
            "value": A - B,
            "description": "Elements that belong to A but not to B."
        },
        "B - A": {
            "value": B - A,
            "description": "Elements that belong to B but not to A."
        },
        "A Δ B": {
            "value": A ^ B,
            "description": "Elements that belong to exactly one of the two sets."
        },
        "Aᶜ": {
            "value": U - A,
            "description": "Elements in the universal set that do not belong to A."
        },
        "Bᶜ": {
            "value": U - B,
            "description": "Elements in the universal set that do not belong to B."
        },
    }


def draw_venn(A, B, U, selected_operation, lang):
    """
    Draws a two-set Venn diagram and highlights the selected operation.
    """
    A_only = A - B
    B_only = B - A
    both = A & B
    outside = U - (A | B)

    if selected_operation in ["Aᶜ", "Bᶜ"]:
        return draw_complement_diagram(A, B, U, selected_operation, lang)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    if len(A | B) == 0:
        ax.text(
            0.5,
            0.5,
            "A = ∅, B = ∅",
            ha="center",
            va="center",
            fontsize=16
        )
        ax.axis("off")
        return fig

    v = venn2(
        subsets=(len(A_only), len(B_only), len(both)),
        set_labels=("A", "B"),
        ax=ax
    )

    region_sets = {
        "10": A_only,
        "01": B_only,
        "11": both
    }

    for region_id, region_set in region_sets.items():
        label = v.get_label_by_id(region_id)
        if label is not None:
            label.set_text(format_region_label(region_set))

    for region_id in ["10", "01", "11"]:
        patch = v.get_patch_by_id(region_id)
        if patch is not None:
            patch.set_alpha(0.25)
            patch.set_edgecolor("black")
            patch.set_linewidth(1.2)

    highlight_map = {
        "A ∪ B": ["10", "01", "11"],
        "A ∩ B": ["11"],
        "A - B": ["10"],
        "B - A": ["01"],
        "A Δ B": ["10", "01"],
        "Ninguna": [],
        "None": [],
    }

    for region_id in highlight_map.get(selected_operation, []):
        patch = v.get_patch_by_id(region_id)
        if patch is not None:
            patch.set_alpha(0.75)

    if lang == "es":
        title = f"Operación seleccionada: {selected_operation}"
        outside_text = f"U - (A ∪ B) = {format_set(outside)}"
    else:
        title = f"Selected operation: {selected_operation}"
        outside_text = f"U - (A ∪ B) = {format_set(outside)}"

    ax.set_title(title, fontsize=14)
    ax.text(
        0.5,
        -0.12,
        outside_text,
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=10
    )

    return fig


def draw_complement_diagram(A, B, U, selected_operation, lang):
    """
    Custom diagram for complements relative to U.
    """
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    rect = Rectangle(
        (0.5, 0.5),
        9,
        5,
        linewidth=1.5,
        edgecolor="black",
        facecolor="lightgray",
        alpha=0.45
    )
    ax.add_patch(rect)

    circle_A = Circle(
        (4, 3),
        1.7,
        linewidth=1.5,
        edgecolor="black",
        facecolor="white" if selected_operation == "Aᶜ" else "lightgray",
        alpha=0.85
    )

    circle_B = Circle(
        (6, 3),
        1.7,
        linewidth=1.5,
        edgecolor="black",
        facecolor="white" if selected_operation == "Bᶜ" else "lightgray",
        alpha=0.85
    )

    ax.add_patch(circle_A)
    ax.add_patch(circle_B)

    ax.text(1, 5.2, "U", fontsize=14, weight="bold")
    ax.text(3.2, 4.55, "A", fontsize=14, weight="bold")
    ax.text(6.65, 4.55, "B", fontsize=14, weight="bold")

    if selected_operation == "Aᶜ":
        result_set = U - A
    else:
        result_set = U - B

    if lang == "es":
        title = f"Complemento seleccionado: {selected_operation}"
        explanation = f"{selected_operation} = {format_set(result_set)}"
    else:
        title = f"Selected complement: {selected_operation}"
        explanation = f"{selected_operation} = {format_set(result_set)}"

    ax.set_title(title, fontsize=14)
    ax.text(
        5,
        0.15,
        explanation,
        ha="center",
        va="center",
        fontsize=10
    )

    ax.axis("off")

    return fig


def cartesian_product_table(A, B, limit=100):
    pairs = list(product(sort_items(A), sort_items(B)))

    rows = []
    for i, pair in enumerate(pairs[:limit], start=1):
        rows.append(
            {
                "#": i,
                "Primer elemento / First element": pair[0],
                "Segundo elemento / Second element": pair[1],
                "Par ordenado / Ordered pair": f"({pair[0]}, {pair[1]})"
            }
        )

    return rows, len(pairs)


def boolean_text(value, lang):
    if lang == "es":
        return "Verdadero" if value else "Falso"
    return "True" if value else "False"


# ============================================================
# Style
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.55rem;
        font-weight: 850;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }

    .soft-card {
        padding: 1.1rem 1.2rem;
        border-radius: 1rem;
        border: 1px solid #e6e6ea;
        background-color: #f8f8fb;
        margin-bottom: 1rem;
    }

    .small-note {
        color: #666;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Language selector
# ============================================================

language_name = st.sidebar.selectbox(
    "Idioma / Language",
    ["Español", "English"]
)

lang = "es" if language_name == "Español" else "en"
T = TEXT[lang]


# ============================================================
# Sidebar inputs
# ============================================================

st.sidebar.header(T["sidebar_title"])

default_U = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
default_A = "2, 4, 6, 8, 10"
default_B = "3, 6, 9"

U_text = st.sidebar.text_input(
    T["universe"],
    value=default_U,
    help=T["input_help"]
)

A_text = st.sidebar.text_input(
    T["set_a"],
    value=default_A,
    help=T["input_help"]
)

B_text = st.sidebar.text_input(
    T["set_b"],
    value=default_B,
    help=T["input_help"]
)

U = parse_set(U_text)
A = parse_set(A_text)
B = parse_set(B_text)

missing_from_U = (A | B) - U

if len(missing_from_U) > 0:
    U = U | A | B
    st.sidebar.warning(T["warning_universe"])


# ============================================================
# Header
# ============================================================

st.markdown(
    f"""
    <div class="main-title">{T["title"]}</div>
    <div class="subtitle">{T["subtitle"]}</div>
    """,
    unsafe_allow_html=True
)

st.info(T["educational_note"])


# ============================================================
# Current sets summary
# ============================================================

with st.expander(T["current_sets"], expanded=True):
    col1, col2, col3 = st.columns(3)

    col1.metric("U", format_set(U))
    col2.metric("A", format_set(A))
    col3.metric("B", format_set(B))

    col1.metric("|U|", len(U))
    col2.metric("|A|", len(A))
    col3.metric("|B|", len(B))


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(T["tabs"])


# ============================================================
# Tab 1: Concepts
# ============================================================

with tab1:
    st.header(T["concepts_intro"])

    st.subheader(T["notation_title"])

    if lang == "es":
        notation_rows = [
            {"Símbolo": r"x ∈ A", "Significado": "x pertenece al conjunto A"},
            {"Símbolo": r"x ∉ A", "Significado": "x no pertenece al conjunto A"},
            {"Símbolo": r"∅", "Significado": "conjunto vacío"},
            {"Símbolo": r"U", "Significado": "conjunto universal"},
            {"Símbolo": r"A ⊆ B", "Significado": "A es subconjunto de B"},
            {"Símbolo": r"|A|", "Significado": "cardinalidad de A, es decir, número de elementos de A"},
        ]
    else:
        notation_rows = [
            {"Symbol": r"x ∈ A", "Meaning": "x belongs to set A"},
            {"Symbol": r"x ∉ A", "Meaning": "x does not belong to set A"},
            {"Symbol": r"∅", "Meaning": "empty set"},
            {"Symbol": r"U", "Meaning": "universal set"},
            {"Symbol": r"A ⊆ B", "Meaning": "A is a subset of B"},
            {"Symbol": r"|A|", "Meaning": "cardinality of A, that is, the number of elements in A"},
        ]

    st.table(notation_rows)

    st.subheader(T["operations_title"])

    if lang == "es":
        operation_rows = [
            {
                "Operación": "A ∪ B",
                "Nombre": "Unión",
                "Idea": "Todo lo que está en A o en B."
            },
            {
                "Operación": "A ∩ B",
                "Nombre": "Intersección",
                "Idea": "Lo que está al mismo tiempo en A y en B."
            },
            {
                "Operación": "A - B",
                "Nombre": "Diferencia",
                "Idea": "Lo que está en A pero no en B."
            },
            {
                "Operación": "A Δ B",
                "Nombre": "Diferencia simétrica",
                "Idea": "Lo que está en A o en B, pero no en ambos."
            },
            {
                "Operación": "Aᶜ",
                "Nombre": "Complemento",
                "Idea": "Lo que está en U pero no en A."
            },
            {
                "Operación": "A × B",
                "Nombre": "Producto cartesiano",
                "Idea": "Conjunto de todos los pares ordenados (a, b), con a ∈ A y b ∈ B."
            },
        ]
    else:
        operation_rows = [
            {
                "Operation": "A ∪ B",
                "Name": "Union",
                "Idea": "Everything that is in A or in B."
            },
            {
                "Operation": "A ∩ B",
                "Name": "Intersection",
                "Idea": "Everything that is in both A and B."
            },
            {
                "Operation": "A - B",
                "Name": "Difference",
                "Idea": "Everything that is in A but not in B."
            },
            {
                "Operation": "A Δ B",
                "Name": "Symmetric difference",
                "Idea": "Everything that is in A or in B, but not in both."
            },
            {
                "Operation": "Aᶜ",
                "Name": "Complement",
                "Idea": "Everything that is in U but not in A."
            },
            {
                "Operation": "A × B",
                "Name": "Cartesian product",
                "Idea": "Set of all ordered pairs (a, b), with a ∈ A and b ∈ B."
            },
        ]

    st.table(operation_rows)

    st.subheader("Fórmulas / Formulas")

    col1, col2 = st.columns(2)

    with col1:
        st.latex(r"A \cup B=\{x:x\in A \text{ or } x\in B\}")
        st.latex(r"A \cap B=\{x:x\in A \text{ and } x\in B\}")
        st.latex(r"A-B=\{x:x\in A \text{ and } x\notin B\}")

    with col2:
        st.latex(r"A^c=U-A")
        st.latex(r"A\triangle B=(A-B)\cup(B-A)")
        st.latex(r"A\times B=\{(a,b):a\in A,\ b\in B\}")


# ============================================================
# Tab 2: Calculator
# ============================================================

with tab2:
    st.header(T["calculator_title"])

    ops = operation_dict(A, B, U, lang)

    rows = []

    for name, data in ops.items():
        value = data["value"]
        rows.append(
            {
                T["operation"]: name,
                T["result"]: format_set(value),
                T["cardinality"]: len(value),
                T["description"]: data["description"]
            }
        )

    st.table(rows)

    st.subheader(T["properties_title"])

    if lang == "es":
        property_rows = [
            {"Propiedad": "A ⊆ B", "Valor": boolean_text(A <= B, lang)},
            {"Propiedad": "B ⊆ A", "Valor": boolean_text(B <= A, lang)},
            {"Propiedad": "A = B", "Valor": boolean_text(A == B, lang)},
            {"Propiedad": "A y B son disjuntos", "Valor": boolean_text(len(A & B) == 0, lang)},
            {"Propiedad": "(A ∪ B)ᶜ = Aᶜ ∩ Bᶜ", "Valor": boolean_text(U - (A | B) == (U - A) & (U - B), lang)},
            {"Propiedad": "(A ∩ B)ᶜ = Aᶜ ∪ Bᶜ", "Valor": boolean_text(U - (A & B) == (U - A) | (U - B), lang)},
        ]
    else:
        property_rows = [
            {"Property": "A ⊆ B", "Value": boolean_text(A <= B, lang)},
            {"Property": "B ⊆ A", "Value": boolean_text(B <= A, lang)},
            {"Property": "A = B", "Value": boolean_text(A == B, lang)},
            {"Property": "A and B are disjoint", "Value": boolean_text(len(A & B) == 0, lang)},
            {"Property": "(A ∪ B)ᶜ = Aᶜ ∩ Bᶜ", "Value": boolean_text(U - (A | B) == (U - A) & (U - B), lang)},
            {"Property": "(A ∩ B)ᶜ = Aᶜ ∪ Bᶜ", "Value": boolean_text(U - (A & B) == (U - A) | (U - B), lang)},
        ]

    st.table(property_rows)


# ============================================================
# Tab 3: Venn diagrams
# ============================================================

with tab3:
    st.header(T["venn_title"])

    st.write(T["venn_note"])

    none_label = "Ninguna" if lang == "es" else "None"

    operation_options = [
        none_label,
        "A ∪ B",
        "A ∩ B",
        "A - B",
        "B - A",
        "A Δ B",
        "Aᶜ",
        "Bᶜ",
    ]

    selected_operation = st.selectbox(
        T["select_operation"],
        operation_options
    )

    fig = draw_venn(A, B, U, selected_operation, lang)
    st.pyplot(fig)

    st.subheader(T["region_elements"])

    A_only = A - B
    B_only = B - A
    both = A & B
    outside = U - (A | B)

    if lang == "es":
        region_rows = [
            {"Región": "Solo A", "Elementos": format_set(A_only), "Cardinalidad": len(A_only)},
            {"Región": "Solo B", "Elementos": format_set(B_only), "Cardinalidad": len(B_only)},
            {"Región": "A ∩ B", "Elementos": format_set(both), "Cardinalidad": len(both)},
            {"Región": "U - (A ∪ B)", "Elementos": format_set(outside), "Cardinalidad": len(outside)},
        ]
    else:
        region_rows = [
            {"Region": "Only A", "Elements": format_set(A_only), "Cardinality": len(A_only)},
            {"Region": "Only B", "Elements": format_set(B_only), "Cardinality": len(B_only)},
            {"Region": "A ∩ B", "Elements": format_set(both), "Cardinality": len(both)},
            {"Region": "U - (A ∪ B)", "Elements": format_set(outside), "Cardinality": len(outside)},
        ]

    st.table(region_rows)


# ============================================================
# Tab 4: Cartesian product
# ============================================================

with tab4:
    st.header(T["cartesian_title"])

    if lang == "es":
        st.write(
            """
            El **producto cartesiano** \(A \\times B\) es el conjunto de todos los pares ordenados
            \((a,b)\), donde \(a \\in A\) y \(b \\in B\).
            """
        )
    else:
        st.write(
            """
            The **Cartesian product** \(A \\times B\) is the set of all ordered pairs
            \((a,b)\), where \(a \\in A\) and \(b \\in B\).
            """
        )

    st.latex(r"A\times B=\{(a,b):a\in A,\ b\in B\}")
    st.latex(r"|A\times B|=|A||B|")

    rows, total_pairs = cartesian_product_table(A, B, limit=100)

    col1, col2, col3 = st.columns(3)

    col1.metric("|A|", len(A))
    col2.metric("|B|", len(B))
    col3.metric("|A × B|", total_pairs)

    if total_pairs > 100:
        st.warning(T["too_many_pairs"])

    st.subheader("A × B")
    st.dataframe(rows, use_container_width=True)

    show_bxa = st.checkbox(T["show_bxa"])

    if show_bxa:
        rows_ba, total_pairs_ba = cartesian_product_table(B, A, limit=100)

        st.subheader("B × A")
        st.dataframe(rows_ba, use_container_width=True)

        if lang == "es":
            st.info(
                "Observa que, en general, A × B no es igual a B × A, porque los pares ordenados dependen del orden."
            )
        else:
            st.info(
                "Notice that, in general, A × B is not equal to B × A because ordered pairs depend on order."
            )


# ============================================================
# Tab 5: Exercises
# ============================================================

with tab5:
    st.header(T["practice_title"])

    exercise_type = st.selectbox(
        T["exercise_type"],
        [
            T["exercise_operation"],
            T["exercise_cardinality"],
            T["exercise_relation"]
        ]
    )

    if exercise_type == T["exercise_operation"]:
        ops = operation_dict(A, B, U, lang)

        chosen_op = st.selectbox(
            T["choose_operation"],
            list(ops.keys())
        )

        if lang == "es":
            st.markdown(
                f"""
                **Ejercicio.** Con los conjuntos actuales, calcula:

                \[
                {chosen_op}
                \]
                """
            )
        else:
            st.markdown(
                f"""
                **Exercise.** Using the current sets, compute:

                \[
                {chosen_op}
                \]
                """
            )

        if st.checkbox(T["show_answer"], key="answer_operation"):
            st.success(f"{chosen_op} = {format_set(ops[chosen_op]['value'])}")

    elif exercise_type == T["exercise_cardinality"]:
        selected_expr = st.selectbox(
            T["choose_operation"],
            ["|A|", "|B|", "|A ∪ B|", "|A ∩ B|", "|A × B|"]
        )

        values = {
            "|A|": len(A),
            "|B|": len(B),
            "|A ∪ B|": len(A | B),
            "|A ∩ B|": len(A & B),
            "|A × B|": len(A) * len(B),
        }

        if lang == "es":
            st.markdown(
                f"""
                **Ejercicio.** Calcula la cardinalidad:

                \[
                {selected_expr}
                \]
                """
            )
        else:
            st.markdown(
                f"""
                **Exercise.** Compute the cardinality:

                \[
                {selected_expr}
                \]
                """
            )

        if st.checkbox(T["show_answer"], key="answer_cardinality"):
            st.success(f"{selected_expr} = {values[selected_expr]}")

    else:
        relation = st.selectbox(
            T["choose_operation"],
            ["A ⊆ B", "B ⊆ A", "A = B", "A ∩ B = ∅"]
        )

        relation_values = {
            "A ⊆ B": A <= B,
            "B ⊆ A": B <= A,
            "A = B": A == B,
            "A ∩ B = ∅": len(A & B) == 0,
        }

        if lang == "es":
            st.markdown(
                f"""
                **Ejercicio.** Determina si la siguiente afirmación es verdadera o falsa:

                \[
                {relation}
                \]
                """
            )
        else:
            st.markdown(
                f"""
                **Exercise.** Determine whether the following statement is true or false:

                \[
                {relation}
                \]
                """
            )

        if st.checkbox(T["show_answer"], key="answer_relation"):
            answer = boolean_text(relation_values[relation], lang)
            st.success(f"{relation}: {answer}")