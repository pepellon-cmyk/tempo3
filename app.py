# app.py
import streamlit as st
import pandas as pd
import sqlite3
import datetime
import numpy as np

st.set_page_config(page_title="Kite for Life - Avaliação de Desempenho", layout="wide")
st.title("Kite for Life — Avaliação de Desempenho")

DB_PATH = "evaluations.db"

# Inicializa DB
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projeto TEXT,
        nome TEXT,
        cargo TEXT,
        data TEXT,
        lideranca REAL,
        assiduidade REAL,
        flexibilidade REAL,
        teoria REAL,
        comando REAL,
        controle REAL,
        badydrag_esq_dir REAL,
        water_start REAL,
        prancha_esq_dir REAL,
        contra_vento REAL,
        nota_media REAL,
        comentarios TEXT
    )
    """
)
conn.commit()

# Helper: map possible column names in uploaded CSV to DB columns
def map_row_to_criteria(row):
    def pick(*names):
        for n in names:
            if n in row and pd.notna(row[n]):
                return row[n]
        return None

    projeto = pick("projeto", "PROJETO", "Projeto") or "KITE FOR LIFE"
    nome = pick("nome", "Nome", "NOME") or ""
    cargo = pick("cargo", "Cargo", "CARGO") or ""
    data = pick("data", "Data", "DATA") or ""
    comentarios = pick("comentarios", "Comentários", "Comentarios", "COMENTARIOS") or ""

    # criteria mapping with common variants, accents, slashes and spacing
    lideranca = pick("liderança", "lideranca", "LIDERANÇA", "LIDERANCA", "Liderança", "LIDERANÇA")
    assiduidade = pick("assiduidade", "Assiduidade", "ASSIDUIDADE")
    flexibilidade = pick("flexibilidade", "Flexibilidade", "FLEXIBILIDADE")
    teoria = pick("teoria", "Teoria", "TEORIA")
    comando = pick("comando", "Comando", "COMANDO")
    controle = pick("controle", "Controle", "CONTROLE")
    badydrag = pick("badydrag esq/dir", "badydrag_esq_dir", "badydrag", "BADYDRAG ESQ/DIR", "BADYDRAG_ESQ_DIR", "Badydrag")
    water_start = pick("water start", "water_start", "Water Start", "WATER START", "water-start")
    prancha = pick("prancha esq/dir", "prancha_esq_dir", "PRANCHA ESQ/DIR", "PRANCHA_ESQ_DIR", "Prancha")
    contra_vento = pick("contra vento", "contra_vento", "contra-vento", "Contra vento", "CONTRA VENTO")

    def to_float(x):
        try:
            return float(x)
        except:
            return None

    return {
        "projeto": projeto,
        "nome": nome,
        "cargo": cargo,
        "data": data,
        "lideranca": to_float(lideranca),
        "assiduidade": to_float(assiduidade),
        "flexibilidade": to_float(flexibilidade),
        "teoria": to_float(teoria),
        "comando": to_float(comando),
        "controle": to_float(controle),
        "badydrag_esq_dir": to_float(badydrag),
        "water_start": to_float(water_start),
        "prancha_esq_dir": to_float(prancha),
        "contra_vento": to_float(contra_vento),
        "comentarios": comentarios,
    }

# Sidebar: Upload CSV
st.sidebar.header("Importar / Exportar")
uploaded_file = st.sidebar.file_uploader("Faça upload de um arquivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Erro ao ler CSV: {e}")
        df = None

    if df is not None:
        st.sidebar.markdown("Visualizar e editar CSV")
        edited = st.experimental_data_editor(df, num_rows="dynamic")
        if st.sidebar.button("Salvar CSV editado (local)"):
            edited.to_csv("uploaded_saved.csv", index=False)
            st.sidebar.success("CSV salvo como uploaded_saved.csv")
        if st.sidebar.button("Importar linhas do CSV para o banco de avaliações"):
            count = 0
            for _, row in edited.iterrows():
                mapped = map_row_to_criteria(row)
                criteria_vals = [
                    mapped["lideranca"], mapped["assiduidade"], mapped["flexibilidade"],
                    mapped["teoria"], mapped["comando"], mapped["controle"],
                    mapped["badydrag_esq_dir"], mapped["water_start"], mapped["prancha_esq_dir"],
                    mapped["contra_vento"]
                ]
                valid = [v for v in criteria_vals if v is not None]
                nota_media = float(np.mean(valid)) if len(valid) > 0 else None
                try:
                    c.execute(
                        """
                        INSERT INTO evaluations
                        (projeto, nome, cargo, data, lideranca, assiduidade, flexibilidade, teoria, comando, controle, badydrag_esq_dir, water_start, prancha_esq_dir, contra_vento, nota_media, comentarios)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            mapped["projeto"], mapped["nome"], mapped["cargo"], mapped["data"],
                            mapped["lideranca"], mapped["assiduidade"], mapped["flexibilidade"],
                            mapped["teoria"], mapped["comando"], mapped["controle"], mapped["badydrag_esq_dir"],
                            mapped["water_start"], mapped["prancha_esq_dir"], mapped["contra_vento"],
                            nota_media, mapped["comentarios"]
                        ),
                    )
                    count += 1
                except Exception as e:
                    st.warning(f"Não foi possível importar linha: {e}")
            conn.commit()
            st.sidebar.success(f"{count} linhas importadas para o banco de avaliações.")

# Formulário para adicionar nova avaliação com critérios
st.header("Adicionar nova avaliação")
with st.form("add_eval"):
    col1, col2, col3 = st.columns(3)
    projeto = col1.text_input("Projeto", value="KITE FOR LIFE")
    nome = col2.text_input("Nome do avaliado")
    cargo = col3.text_input("Cargo")
    col4, col5 = st.columns(2)
    data_av = col4.date_input("Data", value=datetime.date.today())

    st.markdown("### Notas por critério (0-100)")
    # layout dos sliders
    s1, s2, s3 = st.columns(3)
    lideranca = s1.slider("LIDERANÇA", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    assiduidade = s2.slider("ASSIDUIDADE", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    flexibilidade = s3.slider("FLEXIBILIDADE", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

    s4, s5, s6 = st.columns(3)
    teoria = s4.slider("TEORIA", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    comando = s5.slider("COMANDO", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    controle = s6.slider("CONTROLE", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

    s7, s8, s9 = st.columns(3)
    badydrag_esq_dir = s7.slider("BADYDRAG ESQ/DIR", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    water_start = s8.slider("WATER START", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    prancha_esq_dir = s9.slider("PRANCHA ESQ/DIR", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

    contra_vento = st.slider("CONTRA VENTO", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

    comentarios = st.text_area("Comentários", height=100)
    submitted = st.form_submit_button("Salvar avaliação")

if submitted:
    nota_media = float(np.mean([
        lideranca, assiduidade, flexibilidade, teoria, comando, controle,
        badydrag_esq_dir, water_start, prancha_esq_dir, contra_vento
    ]))
    c.execute(
        """
        INSERT INTO evaluations
        (projeto, nome, cargo, data, lideranca, assiduidade, flexibilidade, teoria, comando, controle, badydrag_esq_dir, water_start, prancha_esq_dir, contra_vento, nota_media, comentarios)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            projeto, nome, cargo, data_av.isoformat(), float(lideranca), float(assiduidade), float(flexibilidade),
            float(teoria), float(comando), float(controle), float(badydrag_esq_dir),
            float(water_start), float(prancha_esq_dir), float(contra_vento),
            nota_media, comentarios
        ),
    )
    conn.commit()
    st.success("Avaliação salva com sucesso.")

# Mostrar avaliações existentes
st.header("Avaliações registradas")
df_db = pd.read_sql_query("SELECT * FROM evaluations ORDER BY id DESC", conn)
st.dataframe(df_db)

# Estatísticas básicas
st.header("Resumo")
if not df_db.empty:
    criteria = ["lideranca","assiduidade","flexibilidade","teoria","comando","controle","badydrag_esq_dir","water_start","prancha_esq_dir","contra_vento"]
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Número de avaliações", len(df_db))
        st.metric("Média das notas (nota_media)", round(df_db["nota_media"].astype(float).mean(), 2))
        st.write("Média por critério (global)")
        mean_criteria = {c: round(df_db[c].astype(float).mean(), 2) for c in criteria}
        st.table(pd.DataFrame.from_dict(mean_criteria, orient="index", columns=["média"]).reset_index().rename(columns={"index":"critério"}))
    with col_b:
        st.write("Média por cargo (nota_media)")
        mean_by_cargo = df_db.groupby("cargo")["nota_media"].mean().reset_index().sort_values("nota_media", ascending=False)
        st.table(mean_by_cargo)

    st.write("Médias por cargo e por critério")
    by_cargo = df_db.groupby("cargo")[criteria + ["nota_media"]].mean().reset_index()
    st.dataframe(by_cargo)
else:
    st.info("Nenhuma avaliação registrada ainda.")

# Exportar banco para CSV
st.header("Exportar dados")
csv_export = df_db.to_csv(index=False)
st.download_button("Baixar todas as avaliações (CSV)", data=csv_export, file_name="avaliacoes_kite_for_life.csv", mime="text/csv")

# Botão para resetar DB (cuidado)
if st.button("Resetar banco (apagar todas avaliações)"):
    c.execute("DROP TABLE IF EXISTS evaluations")
    conn.commit()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto TEXT,
            nome TEXT,
            cargo TEXT,
            data TEXT,
            lideranca REAL,
            assiduidade REAL,
            flexibilidade REAL,
            teoria REAL,
            comando REAL,
            controle REAL,
            badydrag_esq_dir REAL,
            water_start REAL,
            prancha_esq_dir REAL,
            contra_vento REAL,
            nota_media REAL,
            comentarios TEXT
        )
        """
    )
    conn.commit()
    st.warning("Banco reiniciado. Todas as avaliações apagadas.")