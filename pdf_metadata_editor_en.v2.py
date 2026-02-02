import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os
import unicodedata
from datetime import datetime

class PDFMetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Metadata Editor")

        window_width = 350
        window_height = 320
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.input_pdf = ""
        self.output_pdf = ""
        self.creation_date = ""
        self.mod_date = ""
        self.existing_producer = "LibreOffice 7.4"
        self.existing_creator = "LibreOffice"
        self.pdf_version = ""
        self.identifier = ""
        self.info = ""
        self.description = ""

        button_font = ('Arial', 12)
        tk.Button(root, text="Open PDF", command=self.open_pdf, 
                 font=button_font, height=2, width=22).pack(pady=5)
        tk.Button(root, text="Show Metadata", command=self.show_metadata_window, 
                 font=button_font, height=2, width=22).pack(pady=5)
        tk.Button(root, text="Export Metadata", command=self.export_metadata, 
                 font=button_font, height=2, width=22).pack(pady=5)
        tk.Button(root, text="Edit Metadata", command=self.open_metadata_window, 
                 font=button_font, height=2, width=22).pack(pady=5)
        tk.Button(root, text="Exit", command=self.root.quit, 
                 font=button_font, height=2, width=22).pack(pady=5)

    def open_pdf(self):
        self.input_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.input_pdf:
            print(f"Selected PDF: {self.input_pdf}")
            if self.validate_pdf():
                self.load_metadata()
                messagebox.showinfo("Success", "PDF loaded successfully!")
            else:
                messagebox.showerror("Error", "The PDF file is corrupted or invalid.")

    def validate_pdf(self):
        try:
            with open(self.input_pdf, "rb") as file:
                reader = PdfReader(file)
                return not reader.is_encrypted
        except Exception as e:
            print(f"Error during PDF validation: {e}")
            return False

    def load_metadata(self):
        try:
            with open(self.input_pdf, "rb") as file:
                reader = PdfReader(file)
                metadata = reader.metadata or {}

                self.pdf_version = getattr(reader, 'pdf_header', 'Unknown')
                self.identifier = ""
                self.info = metadata.get('/Info', '')
                self.description = metadata.get('/Description', '')

                file_stats = os.stat(self.input_pdf)
                self.creation_date = datetime.fromtimestamp(file_stats.st_ctime).strftime("D:%Y%m%d%H%M%S")
                self.mod_date = datetime.fromtimestamp(file_stats.st_mtime).strftime("D:%Y%m%d%H%M%S")

                self.existing_producer = metadata.get('/Producer', 'LibreOffice 7.4')
                self.existing_creator = metadata.get('/Creator', 'LibreOffice')

        except Exception as e:
            print(f"Error loading metadata: {e}")
            messagebox.showerror("Error", f"Error loading metadata: {e}")

    def open_metadata_window(self):
        if not self.input_pdf:
            messagebox.showwarning("Warning", "Please open a PDF file first")
            return

        self.metadata_window = tk.Toplevel(self.root)
        self.metadata_window.title("Enter Metadata")
        self.metadata_window.geometry("950x750")

        label_width = 20
        entry_width = 45
        padx = 10
        pady = 3

        # Options for /Creator and /Producer
        creator_options = [
            "Adobe Acrobat", "Adobe InDesign CS2 (4.0)", "Adobe Illustrator", "AutoCAD",
            "Microsoft Word", "LaTeX", "PDF+Forms 2.0", "FrameMaker 7.0", "LibreOffice 7.4",
            "Apple Pages", "PDFCreator", "Ghostscript", "Scribus", "Canva", "Google Docs",
            "CorelDRAW", "PowerPoint", "Pandoc", "Apache OpenOffice Writer", "Affinity Publisher",
            "PrinceXML", "DocRaptor", "JasperReports", "Typora", "Chromium", "None of your business!"
        ]

        producer_options = {
            "Adobe Acrobat": "Adobe Acrobat",
            "Adobe InDesign CS2 (4.0)": "Adobe PDF Library 7.0",
            "Microsoft Word": "Microsoft Print to PDF",
            "Ghostscript": "Ghostscript",
            "LibreOffice 7.4": "LibreOffice",
            "PDFCreator": "PDFCreator",
            "Typora": "Typora, Electron",
            "Google Docs": "Google Docs",
            "Chromium": "Skia/PDF m80",
            "None of your business!": "None of your business!"
        }

        labels = [
            ("Title", "Document title"),
            ("Author", "Document author"),
            ("Subject", "Main subject or theme of the document"),
            ("Keywords", "Keywords associated with the document, used for search and indexing"),
            ("CreationDate", self.creation_date),
            ("ModDate", self.mod_date),
            ("Copyright", "© Copyright information for the document"),
            ("Description", self.description or "Brief description of the document"),
            ("Producer", self.existing_producer),
            ("Creator", self.existing_creator),
            ("Info", self.info or "Additional information")
        ]

        self.entries = {}
        for label, default in labels:
            frame = tk.Frame(self.metadata_window)
            frame.pack(pady=pady, fill=tk.X, padx=padx)
            tk.Label(frame, text=label, width=label_width, anchor='w').pack(side=tk.LEFT)
            if label == "Description":
                entry_frame = tk.Frame(frame)
                entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                entry = tk.Text(entry_frame, height=6, width=entry_width, wrap=tk.WORD)
                entry.insert("1.0", default if default else "")
                scrollbar = tk.Scrollbar(entry_frame, command=entry.yview)
                entry.config(yscrollcommand=scrollbar.set)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            elif label == "Creator":
                # Create OptionMenu for /Creator
                var = tk.StringVar(self.metadata_window)
                var.set(self.existing_creator)
                entry = tk.OptionMenu(frame, var, *creator_options)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.entries[label] = var
            elif label == "Producer":
                # Create OptionMenu for /Producer
                var = tk.StringVar(self.metadata_window)
                var.set(self.existing_producer)
                entry = tk.OptionMenu(frame, var, *producer_options.values())
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.entries[label] = var
            else:
                entry = tk.Entry(frame, width=entry_width)
                entry.insert(0, default if default else "")
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.entries[label] = entry

        ro_frame = tk.LabelFrame(self.metadata_window, text="Technical Information", padx=5, pady=5)
        ro_frame.pack(pady=10, padx=padx, fill=tk.X)
        tk.Label(ro_frame, text="PDF Version:", width=label_width, anchor='w').pack(anchor='w')
        tk.Label(ro_frame, text=self.pdf_version, relief='sunken', padx=5, pady=2).pack(fill=tk.X)
        tk.Label(ro_frame, text="Identifier:", width=label_width, anchor='w').pack(anchor='w')
        identifier_text = self.identifier if self.identifier else "Not available"
        tk.Label(ro_frame, text=identifier_text, relief='sunken', padx=5, pady=2).pack(fill=tk.X)

        button_frame = tk.Frame(self.metadata_window)
        button_frame.pack(pady=15)
        tk.Button(button_frame, text="Save Metadata", 
                 command=self.save_metadata, height=2, width=30, font=('Arial', 12)).pack()

    def save_metadata(self):
        metadata = {}
        for label, entry in self.entries.items():
            if label == "Description":
                metadata[label] = self.sanitize_metadata(entry.get("1.0", tk.END))
            elif label == "Creator":
                # Use StringVar associated with OptionMenu
                metadata[label] = self.sanitize_metadata(entry.get())  
            elif label == "Producer":
                # Use StringVar associated with OptionMenu
                metadata[label] = self.sanitize_metadata(entry.get())  
            else:
                metadata[label] = self.sanitize_metadata(entry.get())

        self.output_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF files", "*.pdf")],
            title="Save Modified PDF"
        )
        if self.output_pdf:
            self.update_pdf(metadata)

    def update_pdf(self, metadata):
        try:
            with open(self.input_pdf, 'rb') as file:
                reader = PdfReader(file)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                metadata_clean = {f"/{self.sanitize_key(k)}": v for k, v in metadata.items() if v}
                writer.add_metadata(metadata_clean)
                with open(self.output_pdf, 'wb') as output_file:
                    writer.write(output_file)
            messagebox.showinfo("Success", f"PDF updated successfully:\n{self.output_pdf}")
            self.metadata_window.destroy()
        except Exception as e:
            print(f"Error updating PDF: {e}")
            messagebox.showerror("Error", f"Error updating PDF: {e}")

    def show_metadata_window(self):
        if not self.input_pdf:
            messagebox.showwarning("Warning", "Please open a PDF file first")
            return

        window = tk.Toplevel(self.root)
        window.title("PDF Metadata")
        window.geometry("500x600")

        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(expand=True, fill=tk.BOTH)
        scrollbar.config(command=text.yview)

        try:
            with open(self.input_pdf, "rb") as file:
                reader = PdfReader(file)
                metadata = reader.metadata or {}
                for key, value in metadata.items():
                    key_str = key.replace("/", "")
                    text.insert(tk.END, f"{key_str}: {value}\n")
        except Exception as e:
            text.insert(tk.END, f"Error: {e}")

    def export_metadata(self):
        if not self.input_pdf:
            messagebox.showwarning("Warning", "Please open a PDF file first")
            return

        try:
            with open(self.input_pdf, "rb") as file:
                reader = PdfReader(file)
                metadata = reader.metadata or {}
            lines = []
            for key, value in metadata.items():
                key_str = key.replace("/", "").strip()
                val_str = str(value).strip()
                if key_str and val_str:
                    lines.append(f"InfoKey: {key_str}")
                    lines.append(f"InfoValue: {val_str}")
            export_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save metadata.txt"
            )
            if export_path:
                with open(export_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                messagebox.showinfo("Success", f"Metadata exported to:\n{export_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {e}")

    def sanitize_metadata(self, value):
        text = str(value)
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().strip()

    def sanitize_key(self, key):
        return key.strip().replace(" ", "_").replace("\n", "")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMetadataApp(root)
    root.mainloop()
