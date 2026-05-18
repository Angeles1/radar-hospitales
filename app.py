import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Radar Hospitales",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Radar Hospitales")
st.write("Dashboard dinámico de evaluación de hospitales con GPT, Claude y revisión humana.")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Filtros")

    col_filtro1, col_filtro2 = st.columns(2)

    with col_filtro1:
        hospital = st.selectbox(
            "Hospital",
            sorted(df["hospital"].unique())
        )

    paises_disponibles = df[df["hospital"] == hospital]["pais"].unique()

    with col_filtro2:
        pais = st.selectbox(
            "País",
            sorted(paises_disponibles)
        )

    filtered = df[
        (df["hospital"] == hospital) &
        (df["pais"] == pais)
    ]

    columnas_dimensiones = ["dim1", "dim2", "dim3", "dim4", "dim5", "dim6"]

    nombres_dimensiones = [
        "Patient Access & Engagement",
        "Digital Care Delivery",
        "Data Platform & Interoperability",
        "Clinical Intelligence (CDS & AI)",
        "Leadership, Strategy & Innovation",
        "Compliance, Security & Accessibility"
    ]

    maximos_dimensiones = {
        "dim1": 16,
        "dim2": 20,
        "dim3": 32,
        "dim4": 12,
        "dim5": 20,
        "dim6": 14
    }

    st.subheader(f"Radar comparativo normalizado: {hospital}")

    col1, col2, col3 = st.columns(3)

    gpt_total = filtered.loc[filtered["modelo"] == "GPT", "Total"].sum()
    claude_total = filtered.loc[filtered["modelo"] == "Claude", "Total"].sum()
    humano_total = filtered.loc[filtered["modelo"] == "Humano", "Total"].sum()

    col1.metric("GPT Total", f"{int(gpt_total)} / 114")
    col2.metric("Claude Total", f"{int(claude_total)} / 114")
    col3.metric("Humano Total", f"{int(humano_total)} / 114")

    fig = go.Figure()

    colors = {
        "GPT": "#00A67E",
        "Claude": "#7B61FF",
        "Humano": "#FF4B4B"
    }

    for _, row in filtered.iterrows():
        modelo = row["modelo"]

        valores_normalizados = [
            row[d] / maximos_dimensiones[d] * 100
            for d in columnas_dimensiones
        ]

        valores_originales = [
            row[d]
            for d in columnas_dimensiones
        ]

        fig.add_trace(go.Scatterpolar(
            r=valores_normalizados,
            theta=nombres_dimensiones,
            fill="toself",
            name=modelo,
            line=dict(
                color=colors.get(modelo, "#000000"),
                width=3
            ),
            opacity=0.55,
            customdata=valores_originales,
            hovertemplate=(
                "<b>%{theta}</b><br>"
                "Puntuación: %{customdata}<br>"
                "Normalizado: %{r:.1f}%<br>"
                "<extra></extra>"
            )
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="#f5f5f5",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="%",
                tickfont=dict(size=12),
                gridcolor="lightgray"
            ),
            angularaxis=dict(
                tickfont=dict(size=12)
            )
        ),
        showlegend=True,
        template="plotly_white",
        height=750,
        margin=dict(
            l=120,
            r=180,
            t=80,
            b=80
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Datos filtrados")
    st.dataframe(filtered, use_container_width=True)

    # Footer
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center; color:#666; font-size:14px; margin-top:30px;">
            © 2026 Radar Hospitales. Todos los derechos reservados.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Partners colaboradores")

    col_logo1, col_logo2, col_logo3 = st.columns(3)

    with col_logo1:
        st.image("logos/logo1.png", width=180)

    with col_logo2:
        st.image("logos/logo2.png", width=180)

    with col_logo3:
        st.image("logos/logo3.png", width=180)

else:
    st.info("Sube un archivo Excel para empezar.")
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center; color:#666; font-size:14px; margin-top:30px;">
            © 2026 Radar Hospitales. Todos los derechos reservados.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Partners colaboradores")

    col_logo1, col_logo2, col_logo3 = st.columns(3)

    with col_logo1:
        st.image("logos/logo1.png", width=180)

    with col_logo2:
        st.image("logos/logo2.png", width=180)

    with col_logo3:
        st.image("logos/logo3.png", width=180)