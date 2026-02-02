# PDF-Metadata-Editor
Simple graphical PDF metadata editing application developed with Tkinter in Python.

![PDF File Icon](https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/200px-PDF_file_icon.svg.png)


## Files:

    - `pdf_metadata_editor_en.v2.py`

        Main python version in English

    - `pdf_metadata_editor.v2.py`

        python version in French        

    - `pdf_metadata_editor.v2.exe`

        Complied and optimised (<mark>only 12 Mo</mark>) executable in French.


## **Module to install**

  - **pypdf** 

  `pip install pypdf`
  
## Main features :

1. **Simple user interface with 5 main buttons** :
  
    - Open a PDF file
    
    - View existing metadata
    
    - Export metadata to a text file
    
    - Edit metadata
    
    - Exit the application
    
2. **Handling PDF metadata via the pypdf library** :
  
    - Reading existing metadata (title, author, subject, keywords, etc.)
    
    - Complete modification of metadata fields
    
    - Preservation of the original PDF content
    
3. **Specific features**:
  
    - Validation of PDF files (verifies that they are not encrypted)
    
    - Editing interface with drop-down menus for Creator/Producer
    
    - Support for common software (LibreOffice, Adobe, Microsoft, etc.)
    
    - Automatic cleaning of special characters (Unicode → ASCII)
    
    - Export of metadata in text format compatible with other tools
    
4. **Managed metadata fields** :
  
    - Title, Author, Subject, Keywords
    
    - CreationDate, ModDate (based on file system dates)
    
    - Copyright, Description
    
    - Producer, Creator (with predefined choices)
    
    - Info (custom field)
    

This application is useful for organizing, archiving or standardizing the metadata of PDF documents.
