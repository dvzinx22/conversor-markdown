import streamlit as st
from markitdown import MarkItDown
import tempfile
import os

# Configuración de la página
st.set_page_config(page_title="MarkItDown Universal", page_icon="📝")

st.title("📝 Conversor MarkItDown")

# Inicializar MarkItDown
md = MarkItDown()

# Crear pestañas para organizar la interfaz
tab1, tab2 = st.tabs(["📁 Subir Archivo", "✍️ Escribir Texto"])

# --- PESTAÑA 1: ARCHIVOS ---
with tab1:
    archivo_subido = st.file_uploader(
        "Arrastra PDF, Word, Excel, etc.", 
        type=["pdf", "docx", "pptx", "xlsx", "html", "txt", "jpg", "png"]
    )

    if archivo_subido:
        with st.spinner('Procesando archivo...'):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{archivo_subido.name}") as tmp:
                    tmp.write(archivo_subido.getvalue())
                    ruta_temporal = tmp.name
                
                resultado = md.convert(ruta_temporal)
                os.unlink(ruta_temporal)
                
                st.text_area("Resultado Markdown:", resultado.text_content, height=300, key="res_file")
                st.download_button("📥 Descargar .md", resultado.text_content, f"{archivo_subido.name}.md")
            except Exception as e:
                st.error(f"Error: {e}")

# --- PESTAÑA 2: TEXTO DIRECTO ---
with tab2:
    texto_usuario = st.text_area("Pega o escribe tu texto aquí:", height=300, placeholder="Escribe algo...")
    
    if texto_usuario:
        # Para texto plano, MarkItDown lo procesa creando un archivo temporal de texto
        with st.spinner('Formateando...'):
            try:
                with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as tmp:
                    tmp.write(texto_usuario)
                    ruta_txt = tmp.name
                
                resultado_txt = md.convert(ruta_txt)
                os.unlink(ruta_txt)
                
                st.markdown("### Vista Previa:")
                st.info("Aquí tienes tu texto convertido a formato limpio:")
                st.code(resultado_txt.text_content, language="markdown")
                
                st.download_button("📥 Descargar este texto como .md", resultado_txt.text_content, "texto_convertido.md")
            except Exception as e:
                st.error(f"Error al procesar texto: {e}")