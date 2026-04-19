import streamlit as st
from markitdown import MarkItDown
import tempfile
import os

# Configuración visual
st.set_page_config(page_title="Convertidor MarkItDown", page_icon="📝")

st.title("📝 MarkItDown Local")
st.write("Sube tus archivos para convertirlos a Markdown automáticamente.")

# Inicializar MarkItDown
md = MarkItDown()

# Selector de archivos (Drag & Drop)
archivo_subido = st.file_uploader(
    "Arrastra aquí tus archivos (PDF, Word, Excel, etc.)", 
    type=["pdf", "docx", "pptx", "xlsx", "html", "txt", "jpg", "png"]
)

if archivo_subido:
    with st.spinner('Procesando...'):
        try:
            # Crear un archivo temporal para que MarkItDown lo lea
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{archivo_subido.name}") as tmp:
                tmp.write(archivo_subido.getvalue())
                ruta_temporal = tmp.name

            # Conversión
            resultado = md.convert(ruta_temporal)
            
            # Limpiar archivo temporal
            os.unlink(ruta_temporal)

            st.success("¡Listo!")

            # Vista previa
            st.text_area("Resultado en Markdown:", resultado.text_content, height=300)

            # Botón de descarga
            nombre_salida = f"{os.path.splitext(archivo_subido.name)[0]}.md"
            st.download_button(
                label="📥 Descargar archivo .md",
                data=resultado.text_content,
                file_name=nombre_salida,
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Error: {e}")