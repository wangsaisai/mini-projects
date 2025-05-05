# app.py

import streamlit as st
import fitz  # PyMuPDF
import io
import os

# --- PDF Extraction Logic (Adapted from previous example) ---
def extract_text_from_pdf_bytes(pdf_bytes, filename="Uploaded File"):
    """
    Uses PyMuPDF to extract text from PDF bytes.

    Args:
        pdf_bytes (bytes): The byte content of the PDF file.
        filename (str): The original name of the file (for error messages).

    Returns:
        str: Extracted text from all pages, separated by a separator.
             Returns None if an error occurs.
    """
    full_text = []
    try:
        # Open PDF from bytes
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            st.info(f"Processing '{filename}'...")
            st.write(f"Total pages: {len(doc)}")

            # Iterate through each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                full_text.append(text)
                # Optional: Update progress (can slow down for many pages)
                # st.progress((page_num + 1) / len(doc))

        st.success(f"Successfully extracted text from '{filename}'.")
        # Join pages with a clear separator
        return "\n\n--- Page Separator ---\n\n".join(full_text)

    except Exception as e:
        st.error(f"Error processing PDF '{filename}': {e}")
        # More specific error check for common PyMuPDF issues
        if "cannot open" in str(e).lower() or "format error" in str(e).lower():
             st.warning("The file might be corrupted, password-protected without providing a password, or not a valid PDF.")
        return None

# --- Streamlit App UI ---

st.set_page_config(page_title="PDF Text Extractor", layout="wide")

st.title("📄 PDF Text Extractor Service")
st.markdown("""
Upload a PDF file and this service will attempt to extract the text content using the PyMuPDF library.
*Note: Extraction accuracy depends on the PDF structure. Scanned images within PDFs require OCR (not included here).*
""")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # To read file as bytes:
    pdf_bytes = uploaded_file.getvalue()
    original_filename = uploaded_file.name

    st.markdown("---") # Visual separator

    # Display basic file info
    # st.write(f"**Filename:** {original_filename}")
    # st.write(f"**Size:** {len(pdf_bytes) / 1024:.2f} KB")

    # Process the file upon upload
    with st.spinner(f"Extracting text from '{original_filename}'... Please wait."):
        extracted_text = extract_text_from_pdf_bytes(pdf_bytes, original_filename)

    if extracted_text:
        st.markdown("---")
        st.subheader("Extracted Text:")

        # Display extracted text in a scrollable text area
        st.text_area("Text Content", extracted_text, height=400)

        st.markdown("---")
        st.subheader("Download Extracted Text")

        # Prepare filename for download
        txt_filename = os.path.splitext(original_filename)[0] + "_extracted.txt"

        # Provide download button
        st.download_button(
            label="Download as .txt",
            data=extracted_text.encode('utf-8'), # Encode text to bytes for download
            file_name=txt_filename,
            mime='text/plain',
        )
    elif extracted_text == "": # Handle case where PDF might have no text
         st.warning("The PDF was processed, but no text content was found. It might be an image-based PDF or empty.")
    # else: # Error message is already displayed by the extraction function
    #    pass

else:
    st.info("Please upload a PDF file to begin.")

st.markdown("""
---
*Powered by Streamlit & PyMuPDF*
""")


