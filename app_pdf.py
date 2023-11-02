import streamlit as st
from PyPDF2 import PdfMerger
import os
import tempfile
import threading

# Configuración de la página
st.set_page_config(page_title="Web Para unir pdf", page_icon="🗂", layout="wide")

# Función para unir PDFs
def unir_pdfs(documents):
    merger = PdfMerger()
    for document in documents:
        merger.append(document)
    return merger

# Función para eliminar archivos temporales
def cleanup_temp_file(path):
    os.remove(path)

# Frontend
st.image("asset/combine-pdf.png")
st.header("Unir PDF")
st.subheader("Adjuntar pdfs para unir")

pdf_files = st.file_uploader("Arrastra tus archivos PDF aquí o haz clic para buscar", accept_multiple_files=True, type=['pdf'])

if st.button("Unir PDFs"):
    if len(pdf_files) <= 1:
        st.warning("Debes adjuntar más de un pdf para unir.")
    else:
        merger = unir_pdfs(pdf_files)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            merger.write(temp_file.name)
            merger.close()
            with open(temp_file.name, "rb") as file:
                st.download_button(label="Descargar PDF unido", data=file, file_name="pdf_unido.pdf", mime="application/pdf")
            # Programar la eliminación del archivo temporal después de un tiempo razonable
            threading.Timer(300, cleanup_temp_file, args=[temp_file.name]).start()
