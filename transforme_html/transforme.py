import streamlit as st
from io import BytesIO
import os
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from html import escape
import pdfplumber
from docx.oxml.ns import qn
from docx.table import _Cell

st.set_page_config(page_title="Conversor DOCX/PDF → HTML", layout="wide")

CSS_STYLE = """
<style>
    html{
        margin: 0;
    }
    .center { 
        margin: 5px 5% 0; 
        font-family: Times New Roman, serif;
        text-align: justify; 
        font-size: 14px; 
    }
    
    .tabela-centralizada {
        width: 100%;
        margin: 5px auto;
        border-collapse: collapse;
        border: 1px solid black; /* borda externa da tabela */
    }
    
    .tabela-centralizada th,
    .tabela-centralizada td {
        border: 1px solid black; /* borda das células */
        padding: 5px;
    }
</style>
"""

# ---------------- Funções do DOCX/PDF ----------------
def format_runs(paragraph):
    html = ""
    current_style = None
    buffer = []

    def flush_buffer():
        nonlocal html, buffer, current_style
        if buffer:
            text = "".join(buffer)
            if current_style == "bold":
                html += f"<b>{text}</b>"
            elif current_style == "italic":
                html += f"<i>{text}</i>"
            elif current_style == "underline":
                html += f"<u>{text}</u>"
            else:
                html += text
        buffer = []
        current_style = None

    for run in paragraph.runs:
        if not run.text:
            continue
        text = escape(run.text)
        style = "bold" if run.bold else "italic" if run.italic else "underline" if run.underline else None
        if style == current_style:
            buffer.append(text)
        else:
            flush_buffer()
            buffer.append(text)
            current_style = style
    flush_buffer()
    return html

def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def get_colspan(cell):
    tcPr = cell._tc.tcPr
    if tcPr is None:
        return 1
    gridSpan = tcPr.find(qn('w:gridSpan'))
    if gridSpan is not None:
        try:
            return int(gridSpan.val)
        except Exception:
            return 1
    return 1

def is_vmerge_continuation(cell):
    tcPr = cell._tc.tcPr
    if tcPr is None:
        return False
    vMerge = tcPr.find(qn('w:vMerge'))
    if vMerge is None:
        return False
    return vMerge.val is None or vMerge.val == "continue"

def docx_table_to_html(table):
    rows_html = []
    row_html = ["  <tbody>"]
    for row in table._tbl.tr_lst:
        row_html = ["  <tr>"]
        for tc in row.tc_lst:
            c = _Cell(tc, table)
            if is_vmerge_continuation(c):
                continue
            texts = [format_runs(p) for p in c.paragraphs if p.text.strip()]
            cell_text = " ".join(texts).strip()
            colspan = get_colspan(c)
            colspan_attr = f' colspan="{colspan}"' if colspan > 1 else ""
            row_html.append(f"    <td{colspan_attr}>{cell_text}</td>")
        row_html.append("  </tr>")
        rows_html.append(" </tbody> \n".join(row_html))
    return "<table>\n" + "\n".join(rows_html) + "\n</table>"

def docx_to_html(file_bytes):
    doc = Document(file_bytes)
    html = [CSS_STYLE, '<div class="center">']

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            if not block.text.strip():
                continue
            if block.style and block.style.name.startswith("Heading"):
                level = block.style.name[-1] if block.style.name[-1].isdigit() else "1"
                html.append(f"<h{level}>{escape(block.text)}</h{level}>")
            else:
                html.append(f"<p>{format_runs(block)}</p>")
        elif isinstance(block, Table):
            html.append(docx_table_to_html(block))

    html.append("</div></html>")
    return "\n".join(html)

def pdf_to_html(file_bytes):
    html = [CSS_STYLE, '<div class="center">']
    with pdfplumber.open(file_bytes) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                html.append(f"<h2>Página {page_num}</h2>")
                for line in text.split("\n"):
                    html.append(f"<p>{escape(line)}</p>")
    html.append("</div></html>")
    return "\n".join(html)

def convert_to_html(file_bytes, ext):
    ext = ext.lower()
    if ext == ".docx":
        return docx_to_html(file_bytes)
    elif ext == ".pdf":
        return pdf_to_html(file_bytes)
    else:
        raise ValueError("Formato não suportado. Use .docx ou .pdf")

# ---------------- Streamlit Interface ----------------
st.title("Conversor DOCX/PDF → HTML")

uploaded_file = st.file_uploader("Escolha um arquivo DOCX ou PDF", type=["docx","pdf"])

if uploaded_file is not None:
    try:
        file_bytes = BytesIO(uploaded_file.read())
        ext = os.path.splitext(uploaded_file.name)[1]
        html_content = convert_to_html(file_bytes, ext)

        st.subheader("Pré-visualização do HTML")
        st.code(html_content, language='html')

        # Botão para download
        st.download_button(
            label="Baixar HTML",
            data=html_content,
            file_name=os.path.splitext(uploaded_file.name)[0] + ".html",
            mime="text/html"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
