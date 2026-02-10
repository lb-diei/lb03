#!/usr/bin/env python3
"""
DocGen GUI - Document Formatter with Graphical Interface

Select templates, customize styles, and format documents easily.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


class DocGenGUI:
    """GUI for Document Formatter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DocGen - Document Formatter")
        self.root.geometry("800x700")
        
        self.style_config = self.get_default_style()
        self.input_file = None
        
        # GUI state variables
        self.font_combos = {}
        self.bold_vars = {}
        self.align_vars = {}
        self.indent_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
    
    def get_default_style(self) -> dict:
        """Get default Chinese document style."""
        return {
            "document": {
                "margin_top": 3.7, "margin_bottom": 3.5,
                "margin_left": 2.8, "margin_right": 2.6,
                "line_spacing": 1.5,
                "font_family": "FangSong_GB2312", "font_size": 16
            },
            "title": {"font_family": "SimHei", "font_size": 22, "bold": True, "alignment": "center"},
            "heading1": {"font_family": "SimHei", "font_size": 16, "bold": True, "alignment": "left"},
            "heading2": {"font_family": "KaiTi_GB2312", "font_size": 15, "bold": False, "alignment": "left"},
            "body": {"font_family": "FangSong_GB2312", "font_size": 16, "bold": False, "alignment": "left", "first_line_indent": 2},
            "signature": {"font_family": "FangSong_GB2312", "font_size": 16, "bold": False, "alignment": "right"}
        }
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="DocGen - Document Formatter", font=('Microsoft YaHei', 18, 'bold'))
        title_label.pack(pady=10)
        
        # Template selection
        template_frame = ttk.LabelFrame(main_frame, text="Template Selection", padding="10")
        template_frame.pack(fill=tk.X, pady=5)
        
        self.template_var = tk.StringVar(value="default")
        templates = [("Default Document (GB/T 9704-2012)", "default"),
                     ("Formal Business Letter", "formal"),
                     ("Academic Paper Format", "academic"),
                     ("Custom", "custom")]
        
        for text, value in templates:
            rb = ttk.Radiobutton(template_frame, text=text, value=value, variable=self.template_var,
                                command=self.on_template_change)
            rb.pack(anchor=tk.W, pady=2)
        
        # Style customization
        style_frame = ttk.LabelFrame(main_frame, text="Style Customization", padding="10")
        style_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(style_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Document settings tab
        doc_tab = ttk.Frame(notebook)
        notebook.add(doc_tab, text="Page Setup")
        self.setup_document_tab(doc_tab)
        
        # Title tab
        title_tab = ttk.Frame(notebook)
        notebook.add(title_tab, text="Title")
        self.setup_element_tab(title_tab, "title")
        
        # Heading1 tab
        h1_tab = ttk.Frame(notebook)
        notebook.add(h1_tab, text="Heading 1")
        self.setup_element_tab(h1_tab, "heading1")
        
        # Body tab
        body_tab = ttk.Frame(notebook)
        notebook.add(body_tab, text="Body")
        self.setup_element_tab(body_tab, "body")
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.pack(side=tk.LEFT)
        
        btn_select = ttk.Button(file_frame, text="Select File", command=self.select_file)
        btn_select.pack(side=tk.RIGHT)
        
        btn_preview = ttk.Button(file_frame, text="Preview Config", command=self.preview_config)
        btn_preview.pack(side=tk.RIGHT, padx=5)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill=tk.X, pady=10)
        
        btn_format = ttk.Button(action_frame, text="Format Document", command=self.format_document)
        btn_format.pack(side=tk.RIGHT, padx=5)
        
        btn_reset = ttk.Button(action_frame, text="Reset Defaults", command=self.reset_styles)
        btn_reset.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def setup_document_tab(self, parent):
        """Setup document settings tab."""
        grid = ttk.Frame(parent)
        grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        row = 0
        ttk.Label(grid, text="Margins (cm):").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        # Margins
        margins = [("Top", "margin_top", 3.7), ("Bottom", "margin_bottom", 3.5),
                   ("Left", "margin_left", 2.8), ("Right", "margin_right", 2.6)]
        
        for col, (label, key, default) in enumerate(margins):
            ttk.Label(grid, text=label).grid(row=row, column=col*2+1, padx=2)
            spin = ttk.Spinbox(grid, from_=0.5, to=10, width=6,
                              command=lambda k=key, d=default: self.update_margin(k, d))
            spin.set(default)
            spin.grid(row=row, column=col*2+2, padx=5)
            setattr(self, f"spin_{key}", spin)
        
        row += 1
        ttk.Label(grid, text="Font Size:").grid(row=row, column=0, sticky=tk.W, pady=5)
        sizes = [str(i) for i in range(10, 26)]
        self.font_size_combo = ttk.Combobox(grid, values=sizes, width=6, state="readonly")
        self.font_size_combo.set("16")
        self.font_size_combo.grid(row=row, column=1, padx=5)
        self.font_size_combo.bind("<<ComboboxSelected>>", lambda e: self.update_style('document', 'font_size', 16))
        
        row += 1
        ttk.Label(grid, text="Line Spacing:").grid(row=row, column=0, sticky=tk.W, pady=5)
        spacings = [("Single", 1.0), ("1.5", 1.5), ("Double", 2.0)]
        self.spacing_var = tk.StringVar(value="1.5")
        for col, (label, val) in enumerate(spacings):
            rb = ttk.Radiobutton(grid, text=label, value=str(val), variable=self.spacing_var,
                                command=lambda v=val: self.update_style('document', 'line_spacing', v))
            rb.grid(row=row, column=col+1, padx=5)
    
    def setup_element_tab(self, parent, element_key):
        """Setup style tab for a specific element (title, heading1, body, etc.)."""
        grid = ttk.Frame(parent)
        grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        row = 0
        # Font family
        ttk.Label(grid, text="Font Family:").grid(row=row, column=0, sticky=tk.W, pady=5)
        fonts = ["SimHei", "KaiTi_GB2312", "FangSong_GB2312", "Microsoft YaHei", "Arial"]
        
        combo = ttk.Combobox(grid, values=fonts, width=15, state="readonly")
        default_font = self.style_config.get(element_key, {}).get("font_family", "SimHei")
        combo.set(default_font)
        combo.grid(row=row, column=1, padx=5, sticky=tk.W)
        combo.bind("<<ComboboxSelected>>", lambda e, k=element_key: self.update_font(k))
        self.font_combos[element_key] = {'family': combo}
        
        row += 1
        # Font size
        ttk.Label(grid, text="Font Size:").grid(row=row, column=0, sticky=tk.W, pady=5)
        sizes = [str(i) for i in range(8, 48)]
        combo = ttk.Combobox(grid, values=sizes, width=6, state="readonly")
        default_size = self.style_config.get(element_key, {}).get("font_size", 12)
        combo.set(str(default_size))
        combo.grid(row=row, column=1, padx=5, sticky=tk.W)
        combo.bind("<<ComboboxSelected>>", lambda e, k=element_key: self.update_size(k))
        self.font_combos[element_key]['size'] = combo
        
        row += 1
        # Bold
        self.bold_vars[element_key] = tk.BooleanVar(value=self.style_config.get(element_key, {}).get("bold", False))
        bold_cb = ttk.Checkbutton(grid, text="Bold", variable=self.bold_vars[element_key],
                                  command=lambda k=element_key: self.update_bold(k))
        bold_cb.grid(row=row, column=0, sticky=tk.W, pady=5)
        
        row += 1
        # Alignment
        ttk.Label(grid, text="Alignment:").grid(row=row, column=0, sticky=tk.W, pady=5)
        align_frame = ttk.Frame(grid)
        align_frame.grid(row=row, column=1, sticky=tk.W)
        
        self.align_vars[element_key] = tk.StringVar(
            value=self.style_config.get(element_key, {}).get("alignment", "left")
        )
        
        for align, label in [("left", "Left"), ("center", "Center"), ("right", "Right")]:
            rb = ttk.Radiobutton(align_frame, text=label, value=align,
                               variable=self.align_vars[element_key],
                               command=lambda k=element_key: self.update_alignment(k))
            rb.pack(side=tk.LEFT, padx=5)
        
        # Body specific: first line indent
        if element_key == "body":
            row += 1
            indent_cb = ttk.Checkbutton(grid, text="First Line Indent (2 chars)", variable=self.indent_var,
                                       command=self.update_indent)
            indent_cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def on_template_change(self):
        """Handle template selection change."""
        template = self.template_var.get()
        if template == "default":
            self.reset_styles()
        elif template == "formal":
            self.apply_formal_style()
        elif template == "academic":
            self.apply_academic_style()
    
    def update_margin(self, key, default):
        """Update margin setting."""
        try:
            value = float(getattr(self, f"spin_{key}").get())
            self.style_config["document"][key] = value
            self.status_var.set(f"Margin updated: {key} = {value}cm")
        except ValueError:
            pass
    
    def update_style(self, element, key, value):
        """Update a style setting."""
        self.style_config[element][key] = value
        self.template_var.set("custom")
        self.status_var.set(f"{element}.{key} = {value}")
    
    def update_font(self, element):
        """Update font family for element."""
        font = self.font_combos[element]['family'].get()
        self.style_config[element]["font_family"] = font
        self.template_var.set("custom")
    
    def update_size(self, element):
        """Update font size for element."""
        size = int(self.font_combos[element]['size'].get())
        self.style_config[element]["font_size"] = size
        self.template_var.set("custom")
    
    def update_bold(self, element):
        """Update bold setting for element."""
        bold = self.bold_vars[element].get()
        self.style_config[element]["bold"] = bold
        self.template_var.set("custom")
    
    def update_alignment(self, element):
        """Update alignment for element."""
        align = self.align_vars[element].get()
        self.style_config[element]["alignment"] = align
        self.template_var.set("custom")
    
    def update_indent(self):
        """Update first line indent."""
        self.style_config["body"]["first_line_indent"] = 2 if self.indent_var.get() else 0
        self.template_var.set("custom")
    
    def select_file(self):
        """Select input file."""
        filetypes = [("Word Document", "*.docx"), ("Markdown", "*.md"), ("Text File", "*.txt"), ("All Files", "*.*")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_file = filename
            self.file_label.config(text=Path(filename).name, foreground="black")
            self.status_var.set(f"Selected: {filename}")
    
    def preview_config(self):
        """Preview current style configuration."""
        preview = json.dumps(self.style_config, ensure_ascii=False, indent=2)
        
        top = tk.Toplevel(self.root)
        top.title("Current Configuration")
        top.geometry("500x600")
        
        text = tk.Text(top, wrap=tk.WORD, font=('Consolas', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, preview)
    
    def format_document(self):
        """Format the selected document."""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
        
        output_file = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")],
            initialfile=f"Formatted_{Path(self.input_file).stem}.docx"
        )
        
        if not output_file:
            return
        
        try:
            from doc_formatter import DocumentFormatter
            formatter = DocumentFormatter(self.style_config)
            
            if self.input_file.endswith('.docx'):
                formatter.format_word_document(self.input_file, output_file)
            else:
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                formatter.format_document(content, output_file)
            
            self.status_var.set(f"Formatting complete: {output_file}")
            messagebox.showinfo("Success", f"Document formatted successfully!\n\nOutput: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Formatting failed:\n{e}")
    
    def reset_styles(self):
        """Reset to default styles."""
        self.style_config = self.get_default_style()
        self.template_var.set("default")
        self.status_var.set("Reset to default styles")
        messagebox.showinfo("Reset", "Default styles restored")
    
    def apply_formal_style(self):
        """Apply formal business document style."""
        self.style_config = {
            "document": {"margin_top": 2.5, "margin_bottom": 2.5, "margin_left": 3.0,
                        "margin_right": 2.5, "line_spacing": 1.5, "font_family": "SimSun", "font_size": 14},
            "title": {"font_family": "SimHei", "font_size": 20, "bold": True, "alignment": "center"},
            "heading1": {"font_family": "SimHei", "font_size": 16, "bold": True, "alignment": "left"},
            "heading2": {"font_family": "SimSun", "font_size": 14, "bold": True, "alignment": "left"},
            "body": {"font_family": "SimSun", "font_size": 14, "bold": False, "alignment": "left", "first_line_indent": 2},
            "signature": {"font_family": "SimSun", "font_size": 14, "bold": False, "alignment": "right"}
        }
        self.status_var.set("Applied: Formal Business Letter style")
    
    def apply_academic_style(self):
        """Apply academic paper style."""
        self.style_config = {
            "document": {"margin_top": 2.5, "margin_bottom": 2.5, "margin_left": 3.0,
                        "margin_right": 2.5, "line_spacing": 2.0, "font_family": "SimSun", "font_size": 12},
            "title": {"font_family": "SimHei", "font_size": 18, "bold": True, "alignment": "center"},
            "heading1": {"font_family": "SimHei", "font_size": 15, "bold": True, "alignment": "left"},
            "heading2": {"font_family": "SimHei", "font_size": 14, "bold": True, "alignment": "left"},
            "body": {"font_family": "SimSun", "font_size": 12, "bold": False, "alignment": "justify", "first_line_indent": 2},
            "signature": {"font_family": "SimSun", "font_size": 12, "bold": False, "alignment": "right"}
        }
        self.status_var.set("Applied: Academic Paper style")


def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')
    
    app = DocGenGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
