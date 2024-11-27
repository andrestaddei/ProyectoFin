import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
import numpy as np

# Estilo global con CSS
def estilo_app():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        header, footer {
            visibility: hidden;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>input {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
# Función principal
def main():
    st.set_page_config(page_title="Finanzas Personales Pro", layout="wide")
    estilo_app()  # Aplicar el estilo

    st.sidebar.image("Imagen1.png", width=100)
    st.sidebar.title("Navegación")
    pages = {
        "🏠 Inicio": inicio,
        "💰 Datos Financieros": datos_financieros,
        "📊 Planeación Financiera": planeacion_financiera
    }
    choice = st.sidebar.radio("Elige una opción:", list(pages.keys()))
    pages[choice]()

# Página de inicio
def inicio():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Bienvenido a Finanzas Personales Pro</h1>", unsafe_allow_html=True)
    st.write("Esta app te ayudará a organizar tus finanzas, aprender a ahorrar y conocer opciones de inversión.")
    st.write("### ¿Listo para empezar? 🚀 Completa tus datos personales y ve al siguiente paso.")

    with st.form("form_datos_personales"):
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        edad = st.number_input("Edad", min_value=1, step=1)
        submit = st.form_submit_button("Continuar")

        if submit:
            if nombre and email:
                st.session_state["nombre"] = nombre
                st.session_state["email"] = email
                st.session_state["edad"] = edad
                st.success(f"¡Gracias, {nombre}! Ahora pasa a la sección de **Datos Financieros** en el menú de la izquierda.")
            else:
                st.error("Por favor, completa todos los campos antes de continuar.")

# Página de datos financieros
def datos_financieros():
    st.markdown("<h2 style='color: #4CAF50;'>💰 Tus Datos Financieros</h2>", unsafe_allow_html=True)
    st.write("Completa los siguientes datos para comenzar con tu planeación financiera.")

    # Registro de datos financieros
    with st.form("form_datos_financieros"):
        ingreso_mensual = st.number_input("Ingreso mensual", min_value=0.0, step=100.0)
        porcentaje_ahorro = st.slider("Porcentaje de ahorro", min_value=5, max_value=50, step=1)
        submit_finanzas = st.form_submit_button("Guardar Ingresos")

        if submit_finanzas:
            if ingreso_mensual > 0:
                st.session_state["ingreso_mensual"] = ingreso_mensual
                st.session_state["porcentaje_ahorro"] = porcentaje_ahorro
                st.success("¡Ingreso registrado exitosamente!")
            else:
                st.error("Por favor, ingresa un ingreso mensual válido.")


    # Registro de gastos
    with st.form("form_gastos", clear_on_submit=True):
        gasto_nombre = st.text_input("Nombre del gasto")
        gasto_monto = st.number_input("Monto del gasto", min_value=0.0, step=50.0)
        agregar_gasto = st.form_submit_button("Agregar gasto")

        if agregar_gasto:
            if gasto_nombre and gasto_monto > 0:
                if "gastos" not in st.session_state:
                    st.session_state["gastos"] = []
                st.session_state["gastos"].append({"nombre": gasto_nombre, "monto": gasto_monto})
                st.success(f"Gasto '{gasto_nombre}' agregado por ${gasto_monto:.2f}.")
            else:
                st.error("Por favor ingresa un nombre y un monto válido para el gasto.")

        
    # Mostrar gastos
    if "gastos" in st.session_state and st.session_state["gastos"]:
        st.write("### Lista de Gastos")
        gastos_df = pd.DataFrame(st.session_state["gastos"])
        st.dataframe(gastos_df)
    else:
        st.info("Aún no has registrado gastos.")

    with st.form("form_datos_financiero"):
        submit_finanzas = st.form_submit_button("Guardar datos financieros")
        if submit_finanzas:
            if ingreso_mensual > 0:
                st.session_state["ingreso_mensual"] = ingreso_mensual
                st.session_state["porcentaje_ahorro"] = porcentaje_ahorro
                st.success("¡Datos financieros guardados correctamente! Ahora pasa a **Planeación Financiera**.")
            else:
                st.error("Por favor, ingresa un ingreso mensual válido.")
    
# Página de planeación financiera
def planeacion_financiera():
    if "ingreso_mensual" not in st.session_state:
        st.warning("Primero completa tus datos financieros en la sección anterior.")
        return

    st.markdown("<h2 style='color: #4CAF50;'>📊 Planeación Financiera</h2>", unsafe_allow_html=True)

    ingreso_mensual = st.session_state["ingreso_mensual"]
    porcentaje_ahorro = st.session_state["porcentaje_ahorro"]
    gastos = st.session_state.get("gastos", [])

    # Cálculos financieros
    ahorro_obligatorio = ingreso_mensual * (porcentaje_ahorro / 100)
    total_gastos = sum(gasto["monto"] for gasto in gastos)
    excedente = ingreso_mensual - ahorro_obligatorio - total_gastos

    # Mostrar resultados
    st.write(f"- **Ingreso Mensual:** ${ingreso_mensual:.2f}")
    st.write(f"- **Ahorro Obligatorio:** ${ahorro_obligatorio:.2f}")
    st.write(f"- **Gastos Totales:** ${total_gastos:.2f}")
    st.write(f"- **Excedente Disponible:** ${excedente:.2f}")

    # Opciones de inversión
    st.write("### Opciones de inversión (ETFs reales)")
    etfs = {
        "SPY": "SPDR S&P 500 ETF Trust: Empresas líderes del S&P 500.",
        "QQQ": "Invesco QQQ Trust: Compañías tecnológicas del Nasdaq.",
        "VWO": "Vanguard Emerging Markets ETF: Mercados emergentes globales.",
        "IVV": "iShares Core S&P 500 ETF: Rastrea el índice S&P 500.",
        "DIA": "SPDR Dow Jones Industrial Average ETF Trust: Empresas del índice Dow Jones.",
        "IWM": "iShares Russell 2000 ETF: Compañías pequeñas de EE.UU.",
        "EFA": "iShares MSCI EAFE ETF: Mercados desarrollados fuera de EE.UU. y Canadá.",
        "AGG": "iShares Core U.S. Aggregate Bond ETF: Mercado de bonos de EE.UU.",
        "VNQ": "Vanguard Real Estate ETF: Sector inmobiliario de EE.UU.",
        "XLK": "Technology Select Sector SPDR Fund: Tecnológicas del S&P 500.",
        "XLE": "Energy Select Sector SPDR Fund: Sector energético del S&P 500.",
        "ARKK": "ARK Innovation ETF: Empresas innovadoras de tecnología.",
        "VOO": "Vanguard S&P 500 ETF: Inversión diversificada en el S&P 500.",
        "SCHD": "Schwab U.S. Dividend Equity ETF: Empresas con altos dividendos."
    }
    etf_seleccionado = st.selectbox("Elige un ETF:", list(etfs.keys()), format_func=lambda x: etfs[x])

    # Obtener datos del ETF seleccionado
    etf_data = yf.Ticker(etf_seleccionado)
    etf_hist = etf_data.history(period="1y")
    precios = etf_hist["Close"]
    precio_actual = precios.iloc[-1]
    retorno_anual = ((precio_actual / precios.iloc[0]) - 1) * 100
    volatilidad = precios.pct_change().std() * (252 ** 0.5) * 100

    st.write(f"**Precio actual:** ${precio_actual:.2f}")
    st.write(f"**Rentabilidad anual estimada:** {retorno_anual:.2f}%")
    st.write(f"**Volatilidad (riesgo) anualizada:** {volatilidad:.2f}%")

    

    # Simulación de inversión con anualidades vencidas
    meses = st.slider("Plazo de inversión (meses):", 1, 36, 12)
    tasa_mensual = retorno_anual / 100 / 12

    # Cálculo del crecimiento de la inversión
    valores_futuros_anualidad = [
        excedente * ((1 + tasa_mensual) ** i - 1) / tasa_mensual for i in range(1, meses + 1)
    ]

    # Creación de la tabla
    tabla_resultados = pd.DataFrame({
        "Mes": range(1, meses + 1),
        "Valor Futuro (MXN)": [f"{vf:.2f}" for vf in valores_futuros_anualidad]
    })

    # Mostrar tabla en Streamlit
    st.write("### Crecimiento de la inversión por anualidades vencidas")
    st.dataframe(tabla_resultados)

    # Gráfica de crecimiento
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, meses + 1), valores_futuros_anualidad, marker="o", color="green")
    plt.title("Proyección de Inversión con Anualidades Vencidas", fontsize=16)
    plt.xlabel("Meses", fontsize=12)
    plt.ylabel("Valor Futuro (MXN)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(plt)


    # Planeación de proyectos personales
    st.write("### Planeación de Proyectos Personales")
    st.markdown(
    """
    Define tus metas financieras y planea cuánto necesitas ahorrar mensualmente para alcanzarlas.
    ¡Comienza con tus sueños hoy! 🎯
    """
)
    with st.form("form_proyectos"):
        proyecto_nombre = st.text_input("📝 Nombre del proyecto (e.g., boda, vacaciones)")
        costo_proyecto = st.number_input("💰 Costo del proyecto", min_value=0.0, step=100.0)
        fecha_objetivo = st.date_input("📅 Fecha objetivo", min_value=datetime.date.today())
        calcular = st.form_submit_button("📊 Calcular Ahorro")
    
        if calcular:
            meses_restantes = (fecha_objetivo.year - datetime.date.today().year) * 12 + (fecha_objetivo.month - datetime.date.today().month)
            if meses_restantes > 0:
                ahorro_mensual_necesario = costo_proyecto / meses_restantes
                st.success(f"¡Meta calculada para '{proyecto_nombre}'! 🎉")
                st.write(f"- **Meses restantes:** {meses_restantes}")
                st.write(f"- **Ahorro mensual necesario:** ${ahorro_mensual_necesario:.2f}")
                ahorro_acumulado = [ahorro_mensual_necesario * i for i in range(1, meses_restantes + 1)]
                meses = list(range(1, meses_restantes + 1))
                sns.set(style="whitegrid")
                plt.figure(figsize=(10, 6))
                sns.lineplot(x=meses, y=ahorro_acumulado, marker="o", color="blue", label="Ahorro Acumulado")
                plt.axhline(costo_proyecto, color="red", linestyle="--", label="Meta del Proyecto")
                plt.title(f"Progreso de Ahorro para '{proyecto_nombre}'", fontsize=16)
                plt.xlabel("Meses", fontsize=12)
                plt.ylabel("Monto Ahorrado ($)", fontsize=12)
                plt.legend(fontsize=10)
                plt.tight_layout()
                st.pyplot(plt)
                st.markdown(
                    f"""
                    ### 🎯 ¡Estás a solo {meses_restantes} meses de alcanzar tu meta!
                    Si ahorras **${ahorro_mensual_necesario:.2f}** mensualmente, podrás financiar tu proyecto de **{proyecto_nombre}**.
                    """
                 )

            else:
                st.error("❌ La fecha objetivo debe estar en el futuro. Por favor, selecciona una fecha válida.")

    st.markdown(
        """
        ---
        ### Consejos para Alcanzar tus Metas:
        - 🔄 **Automatiza tu ahorro**: Configura transferencias automáticas para asegurar tu progreso.
        - 🛍️ **Controla tus gastos**: Revisa tu presupuesto para priorizar tu meta.
        - 📈 **Invierte tu ahorro**: Considera opciones de inversión para potenciar tu dinero.
        """
    )
if __name__ == "__main__":
    main()
