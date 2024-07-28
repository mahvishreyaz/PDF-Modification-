import fitz  # PyMuPDF
import re

def add_logo(pdf_document, logo_path, logo_position):
    # Open the image file
    logo_image = fitz.Pixmap(logo_path)
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Define the position where the logo will be added 
        x, y, width, height = logo_position
        
        # Insert the logo into the page
        page.insert_image(fitz.Rect(x, y, x + width, y + height), pixmap=logo_image)
    
def remove_sensitive_info(pdf_document):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    phone_pattern = re.compile(r'\b(?:\+?\d{1,3})?[-. (]?\d{3}[-. )]?\d{3}[-. ]?\d{4}\b') 

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")

        # Find all phone numbers and email addresses in the text
        sensitive_info = phone_pattern.findall(text) + email_pattern.findall(text)

        # Redact the found phone numbers and email addresses
        for info in sensitive_info:
            redaction_areas = page.search_for(info)
            for area in redaction_areas:
                page.add_redact_annot(area, fill=(1, 1, 1))  # Redact with white color

        page.apply_redactions()

def main():
    pdf_path = r'C:\Mahvish NMIMS\INTERNSHIP\E4\pdf_task\pdftesting.pdf'
    logo_path = r'C:\Mahvish NMIMS\INTERNSHIP\E4\pdf_task\logotesting.png'
    final_output_path = 'final_output.pdf'
    
    logo_position = (60, 50, 100, 100) 


    pdf_document = fitz.open(pdf_path)

    add_logo(pdf_document, logo_path, logo_position)
    
    remove_sensitive_info(pdf_document)
    
    # Save the updated PDF to the final output path
    pdf_document.save(final_output_path)

    print("PDF editing completed.")

if __name__ == "__main__":
    main()
