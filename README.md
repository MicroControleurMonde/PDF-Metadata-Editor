# PDF-Metadata-Editor
Simple graphical PDF metadata editing application developed with Tkinter in Python.


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
