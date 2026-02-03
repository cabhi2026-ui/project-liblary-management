# -*- coding: utf-8 -*-
"""
Enhanced Advanced Library Management System 
With Modern UI, Auto-Email Features, Course-Based Book View,
Web Portal, AI Recommendations, Financial Management, and AI Chatbot
Author: Dhruv Kailash Singh Chauhan
"""

import sys
import subprocess
import sqlite3
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter import filedialog
import os
import threading
import webbrowser
import json
from collections import defaultdict
import numpy as np
import re
import random
from difflib import SequenceMatcher

# ================== AUTO-INSTALL MODULES ==================
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import qrcode
except ModuleNotFoundError:
    install("qrcode[pil]")
    import qrcode

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    install("Pillow")
    from PIL import Image, ImageTk

# Check and install matplotlib with specific backend configuration
try:
    import matplotlib
    # Try to use TkAgg backend which works with Tkinter
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ModuleNotFoundError:
    try:
        install("matplotlib")
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.font_manager as fm
        MATPLOTLIB_AVAILABLE = True
    except Exception as e:
        print(f"Matplotlib installation/import failed: {e}")
        MATPLOTLIB_AVAILABLE = False
except Exception as e:
    print(f"Matplotlib import error: {e}")
    MATPLOTLIB_AVAILABLE = False

# Install NLTK for chatbot
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ModuleNotFoundError:
    try:
        install("nltk")
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        NLTK_AVAILABLE = True
    except Exception as e:
        print(f"NLTK installation failed: {e}")
        NLTK_AVAILABLE = False
except Exception as e:
    print(f"NLTK import error: {e}")
    NLTK_AVAILABLE = False

# Try to install flask for web portal
try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
except ModuleNotFoundError:
    try:
        install("flask")
        from flask import Flask, render_template, request, jsonify
        FLASK_AVAILABLE = True
    except Exception as e:
        print(f"Flask installation failed: {e}")
        FLASK_AVAILABLE = False

# ================== MODERN COLOR SCHEME ==================
COLORS = {
    "primary": "#2C3E50",      # Dark blue-gray
    "secondary": "#3498DB",    # Bright blue
    "accent": "#E74C3C",       # Red accent
    "success": "#27AE60",      # Green
    "warning": "#F39C12",      # Orange
    "light_bg": "#ECF0F1",     # Light gray background
    "dark_bg": "#1A252F",      # Very dark blue
    "card_bg": "#FFFFFF",      # White card background
    "sidebar": "#34495E",      # Sidebar blue
    "highlight": "#2980B9",    # Highlight blue,
}

# ================== MODERN STYLES ==================
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "button": ("Segoe UI", 10, "bold"),
}

# ================== FIXED LOGIN SCREEN ==================
def login_screen():
    login = Tk()
    login.title("🔐 Login - Library Management System")
    login.geometry("500x400")
    login.config(bg=COLORS['light_bg'])
    login.resizable(False, False)
    
    # Center window
    login.update_idletasks()
    width = 500
    height = 400
    x = (login.winfo_screenwidth() // 2) - (width // 2)
    y = (login.winfo_screenheight() // 2) - (height // 2)
    login.geometry(f'{width}x{height}+{x}+{y}')
    
    # Header Frame
    header_frame = Frame(login, bg=COLORS['primary'], height=100)
    header_frame.pack(fill=X)
    header_frame.pack_propagate(False)
    
    Label(header_frame, 
          text="📚 Library Management System", 
          bg=COLORS['primary'], 
          fg="white",
          font=FONTS['title']).pack(expand=True, pady=20)
    
    # Main container with proper spacing
    container = Frame(login, bg=COLORS['light_bg'])
    container.pack(fill=BOTH, expand=True, padx=40, pady=20)
    
    # Login Card
    card = Frame(container, bg=COLORS['card_bg'], relief="flat", bd=2, 
                highlightbackground="#DDDDDD", highlightthickness=1)
    card.pack(fill=BOTH, expand=True)
    
    # Card content with proper padding
    content = Frame(card, bg=COLORS['card_bg'], padx=30, pady=20)
    content.pack(expand=True, fill=BOTH)
    
    Label(content, 
          text="Welcome Back!", 
          bg=COLORS['card_bg'],
          font=FONTS['heading']).pack(pady=(10, 20))
    
    # Username Section
    username_frame = Frame(content, bg=COLORS['card_bg'])
    username_frame.pack(fill=X, pady=(0, 10))
    
    Label(username_frame, text="Username", bg=COLORS['card_bg'],
          font=FONTS['subheading']).pack(anchor="w")
    
    username_entry = Entry(username_frame, font=FONTS['body'], 
                          relief="solid", bd=1, highlightthickness=0)
    username_entry.pack(fill=X, pady=(5, 0), ipady=5)
    
    # Password Section
    password_frame = Frame(content, bg=COLORS['card_bg'])
    password_frame.pack(fill=X, pady=(10, 20))
    
    Label(password_frame, text="Password", bg=COLORS['card_bg'],
          font=FONTS['subheading']).pack(anchor="w")
    
    password_entry = Entry(password_frame, font=FONTS['body'], 
                          relief="solid", bd=1, highlightthickness=0,
                          show="●")
    password_entry.pack(fill=X, pady=(5, 0), ipady=5)
    
    def show_splash():
        splash = Tk()
        splash.overrideredirect(True)
        splash.configure(bg=COLORS['dark_bg'])
        w, h = 700, 450
        x = (splash.winfo_screenwidth() // 2) - (w // 2)
        y = (splash.winfo_screenheight() // 2) - (h // 2)
        splash.geometry(f"{w}x{h}+{x}+{y}")
        
        try:
            img = Image.open("rgc_logo.png")
            img = img.resize((650, 400))
            logo = ImageTk.PhotoImage(img)
            lbl = Label(splash, image=logo, bg=COLORS['dark_bg'])
            lbl.image = logo
            lbl.pack(expand=True)
        except:
            Label(
                splash,
                text="RAJIV GANDHI COLLEGE\nLIBRARY MANAGEMENT SYSTEM",
                fg="white", 
                bg=COLORS['dark_bg'],
                font=("Segoe UI", 24, "bold"),
                justify=CENTER
            ).pack(expand=True)
            
            Label(
                splash,
                text="Loading...",
                fg=COLORS['warning'],
                bg=COLORS['dark_bg'],
                font=("Segoe UI", 14),
            ).pack(pady=20)
        
        # Loading bar
        progress = ttk.Progressbar(splash, mode='indeterminate', length=300)
        progress.pack(pady=20)
        progress.start()
        
        splash.after(2500, splash.destroy)
        splash.mainloop()

    def check_login():
        # GET VALUES DIRECTLY FROM ENTRY WIDGETS
        username = username_entry.get()
        password = password_entry.get()
        
        # Check credentials - TRIM WHITESPACE
        if username.strip() == "dhruv" and password.strip() == "1234":
            login.destroy()
            show_splash()
            start_lms()
        else:
            mb.showerror("Login Failed", "Invalid Username or Password\n\nUsername: dhruv\nPassword: 1234")
            # Shake animation
            for _ in range(3):
                login.geometry(f"{width}x{height}+{x+5}+{y}")
                login.update()
                login.after(50)
                login.geometry(f"{width}x{height}+{x-5}+{y}")
                login.update()
                login.after(50)
                login.geometry(f"{width}x{height}+{x}+{y}")
    
    # Login Button Frame
    button_frame = Frame(content, bg=COLORS['card_bg'])
    button_frame.pack(fill=X, pady=(10, 0))
    
    # Login Button
    login_btn = Button(button_frame, 
                      text="Login →", 
                      command=check_login,
                      bg=COLORS['success'],
                      fg="white",
                      font=("Segoe UI", 12, "bold"),
                      padx=30,
                      pady=10,
                      relief="flat",
                      cursor="hand2")
    login_btn.pack(fill=X, pady=(10, 0))
    
    # Add hover effect to button
    def on_enter(e):
        login_btn['bg'] = COLORS['warning']
    def on_leave(e):
        login_btn['bg'] = COLORS['success']
    
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)
    
    # Footer
    footer = Frame(login, bg=COLORS['light_bg'])
    footer.pack(side=BOTTOM, fill=X, pady=10)
    Label(footer, 
          text="© 2024 Rajiv Gandhi College Library",
          bg=COLORS['light_bg'],
          fg="#666666",
          font=("Segoe UI", 9)).pack()
    
    # Set focus and bind Enter key
    username_entry.focus_set()
    login.bind('<Return>', lambda e: check_login())
    
    login.mainloop()

# ================== LMS MAIN ==================
def start_lms():
    global connector, cursor, web_portal, financial_manager, dropdown_listbox
    connector = sqlite3.connect("library.db")
    cursor = connector.cursor()

    # ===== CREATE TABLES =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Library (
        BK_NAME TEXT,
        BK_ID TEXT PRIMARY KEY,
        AUTHOR_NAME TEXT,
        BK_STATUS TEXT,
        CARD_ID TEXT,
        DUE_DATE TEXT,
        FINE_PER_DAY INTEGER,
        QUANTITY INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        STUDENT_ID TEXT PRIMARY KEY,
        NAME TEXT,
        CLASS TEXT,
        CONTACT TEXT,
        LIBRARY_JOINING_DATE TEXT,
        ADMISSION_YEAR TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FineHistory (
        STUDENT_ID TEXT,
        BK_ID TEXT,
        AMOUNT INTEGER,
        PAYMENT_DATE TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Wishlist (
        STUDENT_ID TEXT,
        BOOK_ID TEXT,
        BOOK_NAME TEXT,
        ADDED_DATE TEXT,
        PRIMARY KEY (STUDENT_ID, BOOK_ID)
    )
    """)
    
    # ===== ADD MISSING COLUMNS IF THEY DON'T EXIST =====
    try:
        cursor.execute("SELECT LIBRARY_JOINING_DATE FROM Students LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE Students ADD COLUMN LIBRARY_JOINING_DATE TEXT")
    
    try:
        cursor.execute("SELECT ADMISSION_YEAR FROM Students LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE Students ADD COLUMN ADMISSION_YEAR TEXT")
    
    connector.commit()

    # ===== UTILITIES =====
    def calculate_fine(due, fine_per_day=5):
        if not due or due == "N/A":
            return 0
        try:
            d = datetime.strptime(due, "%Y-%m-%d").date()
            days = (datetime.now().date() - d).days
            return max(0, days * fine_per_day)
        except:
            return 0

    def update_book_issued_count(book_id):
        """Update the issued count for a specific book"""
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Library 
            WHERE BK_ID=? AND BK_STATUS='Issued'
        """, (book_id,))
        issued_count = cursor.fetchone()[0]
        return issued_count

    def get_issue_date(book_id, student_id):
        """Get the issue date for a specific book-student combination"""
        try:
            if student_id == "N/A" or not student_id:
                return "N/A"
            
            cursor.execute("""
                SELECT DUE_DATE FROM Library 
                WHERE BK_ID=? AND CARD_ID=? AND BK_STATUS='Issued'
            """, (book_id, student_id))
            result = cursor.fetchone()
            
            if result and result[0] and result[0] != "N/A":
                try:
                    # Calculate issue date (14 days before due date)
                    due_date = datetime.strptime(result[0], "%Y-%m-%d")
                    issue_date = due_date - timedelta(days=14)
                    
                    # Always return the actual date (YYYY-MM-DD format)
                    return issue_date.strftime("%Y-%m-%d")
                except:
                    return "N/A"
            return "N/A"
        except:
            return "N/A"

    def update_status():
        total = cursor.execute("SELECT SUM(QUANTITY) FROM Library").fetchone()[0] or 0
        issued = cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Issued'").fetchone()[0]
        fine_res = cursor.execute("SELECT DUE_DATE, FINE_PER_DAY FROM Library WHERE BK_STATUS='Issued'").fetchall()
        fine = sum(calculate_fine(d[0], d[1]) for d in fine_res)
        
        # Get books with multiple copies issued
        cursor.execute("""
            SELECT COUNT(DISTINCT BK_ID) 
            FROM Library 
            WHERE BK_STATUS='Issued'
            GROUP BY BK_ID
            HAVING COUNT(*) > 1
        """)
        multiple_copies = cursor.fetchall()
        multiple_count = len(multiple_copies)
        
        # Update stats labels if they exist
        if 'total_books_label' in globals():
            total_books_label.config(text=f"📚 {total}")
        if 'issued_books_label' in globals():
            issued_books_label.config(text=f"📖 {issued}")
        if 'fine_label' in globals():
            fine_label.config(text=f"💰 ₹{fine}")
        
        # Update status bar with issued books info
        status_text = f"📊 Library Status | Total Books: {total} | Issued: {issued}"
        if multiple_count > 0:
            status_text += f" | 📚 Books with multiple copies issued: {multiple_count}"
        if fine > 0:
            status_text += f" | 📌 Pending Fines: ₹{fine}"
        status_bar.config(text=status_text)

    # ================== NEW REPORT FEATURE ==================
    def generate_library_report():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("PDF files", "*.pdf"), ("Excel files", "*.xlsx")],
            initialfile=f"Library_Report_{datetime.now().strftime('%Y-%m-%d')}.csv"
        )
        if not file_path:
            return
        try:
            cursor.execute("""
                SELECT L.BK_ID, L.BK_NAME, L.AUTHOR_NAME, L.BK_STATUS, 
                       L.CARD_ID, S.NAME, L.DUE_DATE, L.QUANTITY 
                FROM Library L 
                LEFT JOIN Students S ON L.CARD_ID = S.STUDENT_ID
            """)
            rows = cursor.fetchall()
            headers = ["Book ID", "Book Name", "Author", "Status", "Borrower ID", "Borrower Name", "Due Date", "Current Stock"]
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["LIBRARY STATUS REPORT"])
                writer.writerow([f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                writer.writerow([f"Total Records: {len(rows)}"])
                writer.writerow([])
                writer.writerow(headers)
                writer.writerows(rows)
            mb.showinfo("Success", f"✅ Report generated successfully!\nSaved to: {file_path}")
        except Exception as e:
            mb.showerror("Error", f"❌ Failed to generate report: {e}")

    # ================== EMAIL LOGIC ==================
    def send_issue_email(student_id, book_name, book_id, due_date):
        S_EMAIL = "abhimanyuchauhan897@gmail.com"
        S_PW = "ldcc ytgs boda qmih" 
        R_EMAIL = "abhimanyuchauhan897@gmail.com"

        cursor.execute("SELECT NAME FROM Students WHERE STUDENT_ID=?", (student_id,))
        res = cursor.fetchone()
        s_name = res[0] if res else "Unknown Student"

        subject = f"Library Alert: Book Issued to {s_name}"
        body = f"""
        Dear Librarian/Admin,

        A book has been issued in the system:

        STUDENT DETAILS:
        - ID: {student_id}
        - Name: {s_name}

        BOOK DETAILS:
        - Book Name: {book_name}
        - Book ID: {book_id}
        - Due Date: {due_date}

        Sent via LMS Auto-Notifier.
        """
        
        msg = MIMEMultipart()
        msg['From'] = S_EMAIL
        msg['To'] = R_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(S_EMAIL, S_PW)
                server.send_message(msg)
            print("✅ Issue confirmation email sent!")
        except Exception as e:
            print(f"❌ Error sending issue email: {e}")

    def send_return_email(student_id, book_name, book_id):
        S_EMAIL = "abhimanyuchauhan897@gmail.com"
        S_PW = "ldcc ytgs boda qmih" 
        R_EMAIL = "abhimanyuchauhan897@gmail.com"

        cursor.execute("SELECT NAME FROM Students WHERE STUDENT_ID=?", (student_id,))
        res = cursor.fetchone()
        s_name = res[0] if res else "Unknown Student"

        subject = f"Library Confirmation: Book Returned by {s_name}"
        body = f"""
        Dear Librarian/Admin,

        A book has been successfully returned to the library:

        STUDENT DETAILS:
        - ID: {student_id}
        - Name: {s_name}

        BOOK DETAILS:
        - Book Name: {book_name}
        - Book ID: {book_id}
        - Return Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        The book stock has been increased and status updated.
        """
        
        msg = MIMEMultipart()
        msg['From'] = S_EMAIL
        msg['To'] = R_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(S_EMAIL, S_PW)
                server.send_message(msg)
            print("✅ Return confirmation email sent!")
        except Exception as e:
            print(f"❌ Error sending return email: {e}")

    # ===== STUDENT FUNCTIONS =====
    def issuer_card():
        win = Toplevel(root)
        win.title("📝 Issue Book")
        win.geometry("400x250")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 400
        height = 250
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        card = Frame(win, bg=COLORS['card_bg'], relief="flat", bd=2, 
                    highlightbackground="#DDDDDD", highlightthickness=1)
        card.pack(pady=30, padx=30, fill="both", expand=True)
        
        Label(card, text="Enter Student ID", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=20)
        
        sid_entry = Entry(card, font=FONTS['body'], width=25, relief="solid", bd=1)
        sid_entry.pack(pady=10)
        sid_entry.focus_set()
        
        result = {"sid": None}
        
        def check_and_close():
            sid = sid_entry.get().strip()
            if not sid:
                mb.showerror("Error", "Please enter Student ID")
                return
            
            cursor.execute("SELECT * FROM Students WHERE STUDENT_ID=?", (sid,))
            if cursor.fetchone():
                result["sid"] = sid
                win.destroy()
            else:
                mb.showerror("Error", "❌ Student not found in database")
        
        btn_frame = Frame(card, bg=COLORS['card_bg'])
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="Cancel", 
               command=win.destroy,
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=5).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Confirm", 
               command=check_and_close,
               bg=COLORS['success'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=5).pack(side=LEFT, padx=5)
        
        win.bind('<Return>', lambda e: check_and_close())
        win.grab_set()
        win.wait_window()
        
        return result["sid"]

    def add_student():
        win = Toplevel(root)
        win.title("➕ Add New Student")
        win.geometry("450x550")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 450
        height = 550
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['secondary'], height=60)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="➕ Add New Student", 
              bg=COLORS['secondary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=10)
        
        form_frame = Frame(win, bg=COLORS['card_bg'], relief="flat", bd=2,
                          highlightbackground="#DDDDDD", highlightthickness=1)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Create entry fields
        student_id_var = StringVar()
        name_var = StringVar()
        contact_var = StringVar()
        library_date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        admission_year_var = StringVar(value=str(datetime.now().year))
        
        fields = [
            ("Student ID:", student_id_var),
            ("Name:", name_var),
            ("Contact:", contact_var),
            ("Library Joining Date:", library_date_var),
            ("Admission Year:", admission_year_var),
        ]
        
        for i, (label, var) in enumerate(fields):
            Label(form_frame, text=label, bg=COLORS['card_bg'],
                  font=FONTS['subheading']).grid(row=i, column=0, sticky=W, pady=(20 if i==0 else 10), padx=20)
            entry = Entry(form_frame, textvariable=var, font=FONTS['body'], width=30, relief="solid", bd=1)
            entry.grid(row=i, column=1, pady=(20 if i==0 else 10), padx=20)
            
            if label == "Library Joining Date:":
                Label(form_frame, text="(YYYY-MM-DD)", bg=COLORS['card_bg'],
                      font=("Segoe UI", 8), fg="#7F8C8D").grid(row=i, column=2, sticky=W, padx=(0, 20))
        
        # Class dropdown
        Label(form_frame, text="Class:", bg=COLORS['card_bg'],
              font=FONTS['subheading']).grid(row=5, column=0, sticky=W, pady=10, padx=20)
        class_var = StringVar(value="1st Year")
        class_options = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        class_menu = ttk.Combobox(form_frame, textvariable=class_var, 
                                 values=class_options, state="readonly", width=28,
                                 font=FONTS['body'])
        class_menu.grid(row=5, column=1, pady=10, padx=20)
        
        def save():
            if not (student_id_var.get() and name_var.get() and contact_var.get() and class_var.get()):
                mb.showerror("Error", "Student ID, Name, Contact, and Class are required")
                return
            
            try:
                if library_date_var.get():
                    datetime.strptime(library_date_var.get(), "%Y-%m-%d")
                
                if admission_year_var.get():
                    year = int(admission_year_var.get())
                    if year < 2000 or year > datetime.now().year:
                        mb.showerror("Error", "Admission year should be between 2000 and current year")
                        return
            except ValueError:
                mb.showerror("Error", "Invalid date format. Use YYYY-MM-DD for dates")
                return
            
            try:
                cursor.execute("INSERT INTO Students (STUDENT_ID, NAME, CLASS, CONTACT, LIBRARY_JOINING_DATE, ADMISSION_YEAR) VALUES (?,?,?,?,?,?)",
                               (student_id_var.get().strip(), 
                                name_var.get().strip(), 
                                class_var.get(), 
                                contact_var.get().strip(),
                                library_date_var.get().strip() if library_date_var.get() else datetime.now().strftime("%Y-%m-%d"),
                                admission_year_var.get().strip() if admission_year_var.get() else str(datetime.now().year)))
                connector.commit()
                mb.showinfo("Success", "✅ Student Added Successfully")
                win.destroy()
                update_status()
            except sqlite3.IntegrityError:
                mb.showerror("Error", "❌ Student ID already exists")
            except Exception as e:
                mb.showerror("Error", f"❌ Error: {e}")
        
        btn_frame = Frame(form_frame, bg=COLORS['card_bg'])
        btn_frame.grid(row=6, column=0, columnspan=2, pady=30)
        
        Button(btn_frame, text="Cancel", 
               command=win.destroy,
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Save Student", 
               command=save,
               bg=COLORS['success'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(side=LEFT, padx=10)
        
        # Set focus to first field
        win.after(100, lambda: form_frame.winfo_children()[1].focus_set())

    def view_students():
        win = Toplevel(root)
        win.title("🎓 Student Records")
        win.geometry("1000x600")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 1000
        height = 600
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="🎓 STUDENT RECORDS", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        tree_frame = Frame(win, bg=COLORS['card_bg'])
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        tree2 = ttk.Treeview(tree_frame, columns=("ID","Name","Class","Contact","Library Join","Admission Year"), 
                            show="headings", yscrollcommand=scrollbar.set,
                            height=15)
        
        style = ttk.Style()
        style.configure("Treeview", font=FONTS['body'], rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        columns = ["ID","Name","Class","Contact","Library Join","Admission Year"]
        widths = [100, 180, 100, 120, 110, 110]
        
        for col, width in zip(columns, widths):
            tree2.heading(col, text=col)
            tree2.column(col, width=width, anchor=CENTER)
        
        tree2.pack(fill=BOTH, expand=True)
        scrollbar.config(command=tree2.yview)
        
        # Load students with new columns
        try:
            students = cursor.execute("SELECT STUDENT_ID, NAME, CLASS, CONTACT, LIBRARY_JOINING_DATE, ADMISSION_YEAR FROM Students").fetchall()
        except sqlite3.OperationalError:
            # If columns don't exist yet, use basic query
            cursor.execute("SELECT STUDENT_ID, NAME, CLASS, CONTACT FROM Students")
            basic_students = cursor.fetchall()
            students = []
            for student in basic_students:
                students.append((student[0], student[1], student[2], student[3], "N/A", "N/A"))
        
        for s in students:
            formatted_student = list(s)
            if s[4] and s[4] != "N/A":
                try:
                    date_obj = datetime.strptime(s[4], "%Y-%m-%d")
                    formatted_student[4] = date_obj.strftime("%d-%b-%Y")
                except:
                    formatted_student[4] = s[4]
            if not formatted_student[5] or formatted_student[5] == "N/A":
                formatted_student[5] = "N/A"
            tree2.insert("", END, values=formatted_student)
        
        def show_student_details(event):
            """Show detailed student information when double-clicked"""
            selected_item = tree2.selection()
            if not selected_item:
                return
            
            item = tree2.item(selected_item[0])
            student_data = item["values"]
            
            if not student_data:
                return
            
            # Get full data from database
            try:
                cursor.execute("SELECT * FROM Students WHERE STUDENT_ID=?", (student_data[0],))
                full_data = cursor.fetchone()
            except sqlite3.OperationalError:
                # Use basic columns if new ones don't exist
                cursor.execute("SELECT STUDENT_ID, NAME, CLASS, CONTACT FROM Students WHERE STUDENT_ID=?", (student_data[0],))
                full_data = cursor.fetchone()
                if full_data:
                    full_data = full_data + ("N/A", "N/A")  # Add missing columns
            
            if not full_data:
                return
            
            # Get books issued to this student
            cursor.execute("""
                SELECT BK_NAME, BK_ID, DUE_DATE, FINE_PER_DAY 
                FROM Library 
                WHERE CARD_ID=? AND BK_STATUS='Issued'
            """, (student_data[0],))
            issued_books = cursor.fetchall()
            
            # Calculate total fines
            total_fine = 0
            for book in issued_books:
                fine = calculate_fine(book[2], book[3])
                total_fine += fine
            
            # Create details window
            details_win = Toplevel(win)
            details_win.title(f"👤 Student Details: {student_data[1]}")
            details_win.geometry("600x500")
            details_win.config(bg=COLORS['light_bg'])
            
            details_win.update_idletasks()
            width = 600
            height = 500
            x = (details_win.winfo_screenwidth() // 2) - (width // 2)
            y = (details_win.winfo_screenheight() // 2) - (height // 2)
            details_win.geometry(f'{width}x{height}+{x}+{y}')
            
            # Header
            header = Frame(details_win, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text=f"👤 STUDENT DETAILS", 
                  bg=COLORS['primary'], fg="white",
                  font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Main content
            content_frame = Frame(details_win, bg=COLORS['card_bg'], relief="flat", bd=2,
                                highlightbackground="#DDDDDD", highlightthickness=1)
            content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # Student information section
            info_frame = Frame(content_frame, bg=COLORS['card_bg'])
            info_frame.pack(fill=X, padx=20, pady=20)
            
            details = [
                ("🎯 Student ID:", student_data[0]),
                ("👤 Name:", student_data[1]),
                ("🏫 Class:", student_data[2]),
                ("📞 Contact:", student_data[3]),
                ("📅 Library Joining Date:", student_data[4]),
                ("🎓 Admission Year:", student_data[5] if student_data[5] != "N/A" else "N/A"),
            ]
            
            for i, (label, value) in enumerate(details):
                row_frame = Frame(info_frame, bg=COLORS['card_bg'])
                row_frame.pack(fill=X, pady=8)
                
                Label(row_frame, text=label, bg=COLORS['card_bg'],
                      font=("Segoe UI", 10, "bold"), width=25, anchor="w").pack(side=LEFT)
                
                Label(row_frame, text=value, bg=COLORS['card_bg'],
                      font=("Segoe UI", 10), anchor="w").pack(side=LEFT, padx=(10, 0))
            
            # Calculate duration in library
            if full_data[4] and full_data[4] != "N/A":
                try:
                    join_date = datetime.strptime(full_data[4], "%Y-%m-%d")
                    today = datetime.now()
                    duration = (today - join_date).days
                    
                    duration_frame = Frame(info_frame, bg=COLORS['card_bg'])
                    duration_frame.pack(fill=X, pady=(15, 10))
                    
                    Label(duration_frame, text="📊 Duration in Library:", bg=COLORS['card_bg'],
                          font=("Segoe UI", 10, "bold"), width=25, anchor="w").pack(side=LEFT)
                    
                    years = duration // 365
                    months = (duration % 365) // 30
                    days = (duration % 365) % 30
                    
                    duration_text = f"{years} years, {months} months, {days} days"
                    Label(duration_frame, text=duration_text, bg=COLORS['card_bg'],
                          font=("Segoe UI", 10), anchor="w").pack(side=LEFT, padx=(10, 0))
                except:
                    pass
            
            # Books issued section
            books_frame = Frame(content_frame, bg=COLORS['light_bg'])
            books_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
            
            Label(books_frame, text=f"📚 Books Currently Issued ({len(issued_books)})", 
                  bg=COLORS['light_bg'], font=("Segoe UI", 11, "bold")).pack(anchor=W, pady=(0, 10))
            
            if issued_books:
                books_tree_frame = Frame(books_frame, bg=COLORS['card_bg'])
                books_tree_frame.pack(fill=BOTH, expand=True)
                
                books_scrollbar = Scrollbar(books_tree_frame)
                books_scrollbar.pack(side=RIGHT, fill=Y)
                
                books_tree = ttk.Treeview(books_tree_frame,
                                         columns=("Book Name", "Book ID", "Due Date", "Fine"),
                                         show="headings",
                                         yscrollcommand=books_scrollbar.set,
                                         height=min(5, len(issued_books)))
                
                for col in ["Book Name", "Book ID", "Due Date", "Fine"]:
                    books_tree.heading(col, text=col)
                    books_tree.column(col, width=120, anchor=CENTER)
                
                books_tree.pack(fill=BOTH, expand=True)
                books_scrollbar.config(command=books_tree.yview)
                
                for book in issued_books:
                    fine = calculate_fine(book[2], book[3])
                    books_tree.insert("", END, values=(book[0], book[1], book[2], f"₹{fine}"))
                
                if total_fine > 0:
                    fine_frame = Frame(books_frame, bg=COLORS['light_bg'])
                    fine_frame.pack(fill=X, pady=(10, 0))
                    
                    Label(fine_frame, text="💰 Total Pending Fine:", bg=COLORS['light_bg'],
                          font=("Segoe UI", 10, "bold")).pack(side=LEFT)
                    
                    Label(fine_frame, text=f"₹{total_fine}", bg=COLORS['light_bg'],
                          font=("Segoe UI", 10, "bold"), fg=COLORS['accent']).pack(side=LEFT, padx=(10, 0))
            else:
                Label(books_frame, text="✅ No books currently issued", 
                      bg=COLORS['light_bg'], font=("Segoe UI", 10), fg=COLORS['success']).pack(expand=True)
        
        # Bind double-click event
        tree2.bind("<Double-1>", show_student_details)
        
        # Add instruction label
        instruction_frame = Frame(win, bg=COLORS['light_bg'])
        instruction_frame.pack(pady=(0, 10))
        
        Label(instruction_frame, 
              text="💡 Double-click on any student to view detailed information",
              bg=COLORS['light_bg'], font=("Segoe UI", 9), fg=COLORS['primary']).pack()
        
        def generate_student_qr_from_table():
            selected = tree2.focus()
            if not selected:
                mb.showerror("Error","Select a student")
                return
            student_data = tree2.item(selected)["values"]
            if not student_data:
                mb.showerror("Error","No data found")
                return

            sid = student_data[0]
            cursor.execute("SELECT COUNT(*) FROM Library WHERE CARD_ID=? AND BK_STATUS='Issued'", (sid,))
            issued_count = cursor.fetchone()[0]
            cursor.execute("SELECT BK_NAME, BK_ID, DUE_DATE FROM Library WHERE CARD_ID=? AND BK_STATUS='Issued'", (sid,))
            books = cursor.fetchall()
            books_info = "; ".join([f"{b[0]}({b[1]})Due:{b[2]}" for b in books]) or "No books issued"

            info = (f"Student ID:{student_data[0]};Name:{student_data[1]};Class:{student_data[2]};"
                    f"Contact:{student_data[3]};Library Join:{student_data[4] if len(student_data) > 4 else 'N/A'};"
                    f"Admission Year:{student_data[5] if len(student_data) > 5 else 'N/A'};"
                    f"Books Issued:{issued_count};Issued Books:{books_info}")

            qr = qrcode.QRCode(version=None,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
            qr.add_data(info)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            popup = Toplevel()
            popup.title(f"QR Code for {student_data[1]}")
            img_tk = ImageTk.PhotoImage(img)
            lbl = Label(popup, image=img_tk)
            lbl.image = img_tk
            lbl.pack(padx=10,pady=10)

            def save_qr():
                file = filedialog.asksaveasfilename(defaultextension=".png", 
                                                   filetypes=[("PNG files","*.png")])
                if file:
                    img.save(file)
                    mb.showinfo("Saved",f"QR Code saved as {file}")
            
            Button(popup, text="Save QR", command=save_qr, 
                   bg="#28a745", fg="white", font=FONTS['button']).pack(pady=5)
        
        btn_frame = Frame(win, bg=COLORS['light_bg'])
        btn_frame.pack(pady=(0, 10))
        
        Button(btn_frame, text="Generate QR Code",
               command=generate_student_qr_from_table,
               bg=COLORS['secondary'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Close",
               command=win.destroy,
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(side=LEFT, padx=5)

    def update_student_details():
        """Update library joining date and admission year for existing students"""
        win = Toplevel(root)
        win.title("🔄 Update Student Details")
        win.geometry("500x400")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 500
        height = 400
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="🔄 UPDATE STUDENT DETAILS", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        content_frame = Frame(win, bg=COLORS['card_bg'], relief="flat", bd=2,
                             highlightbackground="#DDDDDD", highlightthickness=1)
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        Label(content_frame, text="Select Student:", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(10, 5))
        
        student_var = StringVar()
        cursor.execute("SELECT STUDENT_ID, NAME FROM Students")
        students = cursor.fetchall()
        student_options = ["Select Student"] + [f"{sid} - {name}" for sid, name in students]
        student_menu = ttk.Combobox(content_frame, textvariable=student_var, 
                                   values=student_options, state="readonly", width=40,
                                   font=FONTS['body'])
        student_menu.pack(pady=(0, 20))
        
        Label(content_frame, text="Library Joining Date:", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(10, 5))
        
        library_date_var = StringVar()
        library_date_entry = Entry(content_frame, textvariable=library_date_var, 
                                  font=FONTS['body'], width=40)
        library_date_entry.pack(pady=(0, 10))
        Label(content_frame, text="(Format: YYYY-MM-DD, e.g., 2024-01-21)", 
              bg=COLORS['card_bg'], font=("Segoe UI", 8), fg="#7F8C8D").pack()
        
        Label(content_frame, text="Admission Year:", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(10, 5))
        
        admission_year_var = StringVar()
        admission_year_entry = Entry(content_frame, textvariable=admission_year_var, 
                                    font=FONTS['body'], width=40)
        admission_year_entry.pack(pady=(0, 10))
        
        def update_student():
            if student_var.get() == "Select Student":
                mb.showerror("Error", "Please select a student")
                return
            
            student_id = student_var.get().split(" - ")[0]
            
            try:
                update_fields = []
                values = []
                
                if library_date_var.get():
                    datetime.strptime(library_date_var.get(), "%Y-%m-%d")
                    update_fields.append("LIBRARY_JOINING_DATE = ?")
                    values.append(library_date_var.get())
                
                if admission_year_var.get():
                    year = int(admission_year_var.get())
                    if year < 2000 or year > datetime.now().year:
                        mb.showerror("Error", "Admission year should be between 2000 and current year")
                        return
                    update_fields.append("ADMISSION_YEAR = ?")
                    values.append(admission_year_var.get())
                
                if not update_fields:
                    mb.showerror("Error", "No fields to update")
                    return
                
                values.append(student_id)
                
                query = f"UPDATE Students SET {', '.join(update_fields)} WHERE STUDENT_ID = ?"
                cursor.execute(query, values)
                connector.commit()
                
                mb.showinfo("Success", "✅ Student details updated successfully!")
                win.destroy()
                
            except ValueError:
                mb.showerror("Error", "Invalid date format. Use YYYY-MM-DD for dates")
            except Exception as e:
                mb.showerror("Error", f"Failed to update student: {e}")
        
        Button(content_frame, text="Update Details", 
               command=update_student,
               bg=COLORS['success'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=10).pack(pady=20)

    def delete_student():
        sid = sd.askstring("Delete Student","Enter Student ID:")
        if not sid:
            return
        sid = sid.strip()
        cursor.execute("SELECT * FROM Students WHERE STUDENT_ID=?", (sid,))
        if not cursor.fetchone():
            mb.showerror("Error","Student not found")
            return
        if mb.askyesno("Confirm","Are you sure you want to delete this student?"):
            cursor.execute("DELETE FROM Students WHERE STUDENT_ID=?", (sid,))
            connector.commit()
            mb.showinfo("Success","Student deleted successfully")
            update_status()

    def add_record():
        if not (bk_name.get() and bk_id.get() and fine_per_day.get()):
            mb.showerror("Error","Book Name, ID and Fine per Day are required")
            return
        try:
            cursor.execute("INSERT INTO Library VALUES (?,?,?,?,?,?,?,?)",
                (bk_name.get().strip(), 
                 bk_id.get().strip(), 
                 author.get().strip() if author.get() else "Unknown",
                 "Available", 
                 "N/A", 
                 "N/A", 
                 int(fine_per_day.get()), 
                 10))  # Fixed quantity of 10 units
            connector.commit()
            mb.showinfo("Success", "✅ Book added successfully with 10 units stock.")
            # Clear fields
            bk_name.set("")
            bk_id.set("")
            author.set("")
            fine_per_day.set("5")
            update_status()
        except sqlite3.IntegrityError:
            mb.showerror("Error","❌ Book ID already exists")
        except ValueError:
            mb.showerror("Error","❌ Fine per Day must be a number")

    # ================== ENHANCED SEARCH WITH DROPDOWN ==================
    def setup_search_dropdown(search_entry):
        """Setup dropdown list for search suggestions with issued book indication"""
        global search_var, dropdown_listbox, book_suggestions
        
        search_var = StringVar()
        search_entry.config(textvariable=search_var)
        
        # Create dropdown listbox
        dropdown_listbox = Listbox(root, height=8, font=FONTS['body'], 
                                   bg='white', fg=COLORS['primary'],
                                   selectbackground=COLORS['secondary'],
                                   selectforeground='white',
                                   relief='solid', bd=1)
        dropdown_listbox.place_forget()  # Hide initially
        
        # Store book data for suggestions
        book_suggestions = []
        
        def update_suggestions(*args):
            """Update dropdown suggestions based on input"""
            search_text = search_var.get().strip().lower()
            
            if not search_text:
                dropdown_listbox.place_forget()
                return
            
            # Clear previous suggestions
            dropdown_listbox.delete(0, END)
            book_suggestions.clear()
            
            # Get all books from database
            cursor.execute("""
                SELECT L.BK_NAME, L.AUTHOR_NAME, L.BK_STATUS, 
                       L.BK_ID, L.CARD_ID, S.NAME as STUDENT_NAME
                FROM Library L
                LEFT JOIN Students S ON L.CARD_ID = S.STUDENT_ID
                ORDER BY L.BK_NAME
            """)
            all_books = cursor.fetchall()
            
            # Filter books that match search text
            matches = []
            for book in all_books:
                book_name = book[0]
                author = book[1]
                status = book[2]
                book_id = book[3]
                student_id = book[4]
                student_name = book[5]
                
                # Check if search text matches book name or author
                if (search_text in book_name.lower() or 
                    search_text in author.lower() or
                    search_text in book_id.lower()):
                    
                    # Determine display text with status indicator
                    if status == 'Issued':
                        display_text = f"📖 {book_name} - {author} (Issued to: {student_name or student_id})"
                    else:
                        display_text = f"✅ {book_name} - {author} (Available)"
                    
                    matches.append((display_text, book_name, author, status, book_id))
            
            # Sort matches by relevance (starting with search text)
            matches.sort(key=lambda x: (
                not x[1].lower().startswith(search_text),  # Books starting with search text first
                not search_text in x[1].lower(),  # Then books containing search text
                x[1]  # Alphabetical order
            ))
            
            # Add to dropdown (limit to 10 suggestions)
            for i, (display_text, book_name, author, status, book_id) in enumerate(matches[:10]):
                dropdown_listbox.insert(END, display_text)
                book_suggestions.append((book_name, author, status, book_id))
            
            if matches:
                # Position dropdown below search entry
                x = search_entry.winfo_rootx() - root.winfo_rootx()
                y = search_entry.winfo_rooty() - root.winfo_rooty() + search_entry.winfo_height()
                width = search_entry.winfo_width()
                
                dropdown_listbox.place(x=x, y=y, width=width)
                dropdown_listbox.lift()
            else:
                dropdown_listbox.place_forget()
        
        def select_suggestion(event):
            """Handle selection from dropdown"""
            selection = dropdown_listbox.curselection()
            if selection:
                index = selection[0]
                if index < len(book_suggestions):
                    book_name, author, status, book_id = book_suggestions[index]
                    
                    # Set search text to the selected book's name
                    search_var.set(book_name)
                    
                    # Hide dropdown
                    dropdown_listbox.place_forget()
                    
                    # Focus back to search entry and select all text
                    search_entry.focus_set()
                    search_entry.select_range(0, END)
        
        def hide_dropdown(event):
            """Hide dropdown when focus leaves"""
            if (event.widget != dropdown_listbox and 
                event.widget != search_entry):
                dropdown_listbox.place_forget()
        
        def perform_search(event=None):
            """Perform search and hide dropdown"""
            dropdown_listbox.place_forget()
            display_records(search_var.get())
        
        def navigate_dropdown(event):
            if not dropdown_listbox.winfo_ismapped():
                return
            
            if event.keysym == 'Down':
                if dropdown_listbox.size() > 0:
                    current = dropdown_listbox.curselection()
                    if not current:
                        dropdown_listbox.selection_set(0)
                    else:
                        next_index = (current[0] + 1) % dropdown_listbox.size()
                        dropdown_listbox.selection_clear(0, END)
                        dropdown_listbox.selection_set(next_index)
                        dropdown_listbox.activate(next_index)
            
            elif event.keysym == 'Up':
                if dropdown_listbox.size() > 0:
                    current = dropdown_listbox.curselection()
                    if not current:
                        dropdown_listbox.selection_set(dropdown_listbox.size() - 1)
                    else:
                        prev_index = (current[0] - 1) % dropdown_listbox.size()
                        dropdown_listbox.selection_clear(0, END)
                        dropdown_listbox.selection_set(prev_index)
                        dropdown_listbox.activate(prev_index)
            
            elif event.keysym == 'Escape':
                dropdown_listbox.place_forget()
                search_entry.focus_set()
            
            elif event.keysym == 'Return':
                if dropdown_listbox.winfo_ismapped():
                    select_suggestion(event)
                else:
                    perform_search()
        
        # Bind events
        search_var.trace('w', update_suggestions)  # Update suggestions on typing
        dropdown_listbox.bind('<Double-Button-1>', select_suggestion)
        dropdown_listbox.bind('<Return>', select_suggestion)
        
        # Bind Enter key in search entry to perform search
        search_entry.bind('<Return>', perform_search)
        
        # Bind focus out events
        search_entry.bind('<FocusOut>', hide_dropdown)
        dropdown_listbox.bind('<FocusOut>', hide_dropdown)
        
        # Bind navigation keys
        search_entry.bind('<Down>', navigate_dropdown)
        search_entry.bind('<Up>', navigate_dropdown)
        search_entry.bind('<Escape>', navigate_dropdown)
        
        return search_var

    def display_records(search=""):
        if 'tree' not in globals():
            return
        
        # Clear existing records
        tree.delete(*tree.get_children())
        
        if search.strip() == "": 
            # Show EMPTY dashboard when search is empty
            status_bar.config(text="🔍 Enter book name or author name to search")
            return
        else:
            # Search by book name OR author name
            search_term = f"%{search.strip()}%"
            rows = cursor.execute("""
                SELECT L.*, S.NAME as STUDENT_NAME 
                FROM Library L 
                LEFT JOIN Students S ON L.CARD_ID = S.STUDENT_ID
                WHERE UPPER(L.BK_NAME) LIKE UPPER(?) 
                   OR UPPER(L.AUTHOR_NAME) LIKE UPPER(?)
                ORDER BY L.BK_NAME
                """, (search_term, search_term)).fetchall()
            
            if len(rows) == 0:
                status_bar.config(text=f"🔍 No books found for: '{search.strip()}'")
            else:
                status_bar.config(text=f"🔍 Search results for: '{search.strip()}' | Found: {len(rows)} records")
            
            # Add records to treeview with issued count and issue date
            for r in rows: 
                # Calculate issued count for this book
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM Library 
                    WHERE BK_ID=? AND BK_STATUS='Issued'
                """, (r[1],))  # r[1] is BK_ID
                issued_count = cursor.fetchone()[0]
                
                # Calculate issue date if book is issued
                issue_date = get_issue_date(r[1], r[4])
                
                # Get student name if book is issued
                student_name = r[8] if len(r) > 8 else "Unknown"
                
                # Create new row with issued count and issue date
                # New column order: Name, ID, Author, Status, Student ID, Issue Date, Due Date, Fine/Day, Quantity, Issued Count
                new_row = [
                    r[0],  # Name
                    r[1],  # ID
                    r[2],  # Author
                    r[3],  # Status
                    r[4],  # Student ID
                    issue_date,  # Issue Date
                    r[5],  # Due Date
                    r[6],  # Fine/Day
                    r[7],  # Quantity
                    issued_count  # Issued Count
                ]
                
                # Insert with tag for highlighting
                item_id = tree.insert("", END, values=tuple(new_row))
                
                # Apply highlighting based on status
                if r[3] == 'Issued':  # BK_STATUS
                    tree.tag_configure('issued', background='#FFF0F0', foreground='#C41E3A')
                    tree.item(item_id, tags=('issued',))
                else:
                    tree.tag_configure('available', background='#F0FFF0', foreground='#228B22')
                    tree.item(item_id, tags=('available',))
            
            update_status()

    def view_books():
        win = Toplevel(root)
        win.title("📚 Library Books")
        win.geometry("1300x600")  # Increased width for new column
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 1300
        height = 600
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="📚 LIBRARY BOOKS", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        # Stats frame at the top
        stats_frame = Frame(win, bg=COLORS['light_bg'], padx=20, pady=10)
        stats_frame.pack(fill=X)
        
        def update_view_stats():
            # Get total issued count
            cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Issued'")
            total_issued = cursor.fetchone()[0] or 0
            
            # Get books with multiple copies issued
            cursor.execute("""
                SELECT BK_NAME, BK_ID, 
                       (SELECT COUNT(*) FROM Library L2 
                        WHERE L2.BK_ID = L.BK_ID AND L2.BK_STATUS='Issued') as issued_count,
                       QUANTITY
                FROM Library L
                WHERE BK_STATUS='Issued'
                GROUP BY BK_ID
                HAVING issued_count > 0
            """)
            multiple_issued = cursor.fetchall()
            
            # Update stats labels
            total_issued_label.config(text=f"📖 Total Issued Books: {total_issued}")
            
            if multiple_issued:
                popular_books = ", ".join([f"{book[0]} ({book[2]})" for book in multiple_issued[:2]])
                multiple_label.config(text=f"🔥 {len(multiple_issued)} books have multiple copies issued")
            else:
                multiple_label.config(text="✅ All issued books are single copies")
        
        total_issued_label = Label(stats_frame, text="📖 Total Issued Books: 0", 
                                  bg=COLORS['light_bg'], font=("Segoe UI", 10, "bold"),
                                  fg=COLORS['primary'])
        total_issued_label.pack(side=LEFT, padx=(0, 20))
        
        multiple_label = Label(stats_frame, text="", 
                              bg=COLORS['light_bg'], font=("Segoe UI", 10),
                              fg=COLORS['warning'])
        multiple_label.pack(side=LEFT)
        
        tree_frame = Frame(win, bg=COLORS['card_bg'])
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # UPDATED: ADDED NEW COLUMN: "Issue Date" after "Student ID"
        tree3 = ttk.Treeview(tree_frame, 
                            columns=("Name","ID","Author","Status","Student ID","Issue Date","Due Date","Fine/Day","Quantity","Issued Count"), 
                            show="headings", 
                            yscrollcommand=scrollbar.set)
        
        style = ttk.Style()
        style.configure("Treeview", font=FONTS['body'], rowheight=28)
        
        # Updated columns with new "Issue Date"
        columns = ["Name","ID","Author","Status","Student ID","Issue Date","Due Date","Fine/Day","Quantity","Issued Count"]
        widths = [180, 90, 130, 90, 90, 100, 100, 80, 80, 100]  # Adjusted widths
        
        for col, width in zip(columns, widths):
            tree3.heading(col, text=col)
            tree3.column(col, width=width, anchor=CENTER)
        
        tree3.pack(fill=BOTH, expand=True)
        scrollbar.config(command=tree3.yview)
        
        def refresh_tree():
            try:
                # Check if the treeview still exists
                if not tree3.winfo_exists():
                    return
                    
                for i in tree3.get_children(): 
                    tree3.delete(i)
                
                # Get all books
                rows = cursor.execute("SELECT * FROM Library").fetchall()
                
                for r in rows: 
                    # Calculate issued count for this book
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM Library 
                        WHERE BK_ID=? AND BK_STATUS='Issued'
                    """, (r[1],))  # r[1] is BK_ID
                    issued_count = cursor.fetchone()[0]
                    
                    # Calculate issue date if book is issued
                    issue_date = get_issue_date(r[1], r[4])
                    
                    # Create new row with issued count and issue date
                    # Column order: Name, ID, Author, Status, Student ID, Issue Date, Due Date, Fine/Day, Quantity, Issued Count
                    new_row = [
                        r[0],  # Name
                        r[1],  # ID
                        r[2],  # Author
                        r[3],  # Status
                        r[4],  # Student ID
                        issue_date,  # Issue Date
                        r[5],  # Due Date
                        r[6],  # Fine/Day
                        r[7],  # Quantity
                        issued_count  # Issued Count
                    ]
                    
                    tree3.insert("", END, values=tuple(new_row))
                
                # Update stats
                update_view_stats()
                # Apply highlighting
                highlight_issued_books()
                
            except Exception as e:
                print(f"Refresh tree error: {e}")
        
        refresh_tree()
        
        # Function to highlight rows based on issued count
        def highlight_issued_books():
            for item in tree3.get_children():
                values = tree3.item(item)['values']
                if values and len(values) > 9:  # Check if we have issued count
                    issued_count = values[9]
                    if issued_count > 0:
                        # Highlight rows with issued books
                        tree3.tag_configure('issued', background='#FFF3CD')  # Light yellow
                        tree3.item(item, tags=('issued',))
                    if issued_count > 1:
                        # Highlight rows with multiple copies issued
                        tree3.tag_configure('multiple', background='#F8D7DA')  # Light red
                        tree3.item(item, tags=('multiple',))
        
        # Apply highlighting
        highlight_issued_books()
        
        def edit_book_details():
            try:
                selected = tree3.focus()
                if not selected:
                    mb.showerror("Error", "Select a book to edit")
                    return
                
                values = tree3.item(selected)["values"]
                
                # Create edit window
                edit_win = Toplevel(win)
                edit_win.title("✏️ Edit Book Details")
                edit_win.geometry("500x500")
                edit_win.config(bg=COLORS['light_bg'])
                
                edit_win.update_idletasks()
                width = 500
                height = 500
                x = (edit_win.winfo_screenwidth() // 2) - (width // 2)
                y = (edit_win.winfo_screenheight() // 2) - (height // 2)
                edit_win.geometry(f'{width}x{height}+{x}+{y}')
                
                # Header
                header = Frame(edit_win, bg=COLORS['primary'], height=70)
                header.pack(fill=X)
                header.pack_propagate(False)
                
                Label(header, text="✏️ EDIT BOOK DETAILS", 
                      bg=COLORS['primary'], fg="white",
                      font=FONTS['heading']).pack(expand=True, pady=15)
                
                # Form frame
                form_frame = Frame(edit_win, bg=COLORS['card_bg'], relief="flat", bd=2,
                                  highlightbackground="#DDDDDD", highlightthickness=1)
                form_frame.pack(pady=20, padx=30, fill="both", expand=True)
                
                # Book ID (cannot be edited)
                Label(form_frame, text="Book ID (cannot be changed):", 
                      bg=COLORS['card_bg'], font=FONTS['subheading']).grid(row=0, column=0, 
                                                                            sticky=W, pady=20, padx=20)
                book_id_label = Label(form_frame, text=values[1], bg=COLORS['card_bg'], 
                                     font=FONTS['body'], fg=COLORS['primary'])
                book_id_label.grid(row=0, column=1, pady=20, padx=20, sticky=W)
                
                # Book Name
                Label(form_frame, text="Book Name:", bg=COLORS['card_bg'], 
                      font=FONTS['subheading']).grid(row=1, column=0, sticky=W, pady=15, padx=20)
                book_name_var = StringVar(value=values[0])
                book_name_entry = Entry(form_frame, textvariable=book_name_var, 
                                       font=FONTS['body'], width=30, relief="solid", bd=1)
                book_name_entry.grid(row=1, column=1, pady=15, padx=20)
                
                # Author
                Label(form_frame, text="Author:", bg=COLORS['card_bg'], 
                      font=FONTS['subheading']).grid(row=2, column=0, sticky=W, pady=15, padx=20)
                author_var = StringVar(value=values[2])
                author_entry = Entry(form_frame, textvariable=author_var, 
                                    font=FONTS['body'], width=30, relief="solid", bd=1)
                author_entry.grid(row=2, column=1, pady=15, padx=20)
                
                # Fine per Day
                Label(form_frame, text="Fine per Day (₹):", bg=COLORS['card_bg'], 
                      font=FONTS['subheading']).grid(row=3, column=0, sticky=W, pady=15, padx=20)
                fine_var = StringVar(value=str(values[7]))
                fine_entry = Entry(form_frame, textvariable=fine_var, 
                                  font=FONTS['body'], width=30, relief="solid", bd=1)
                fine_entry.grid(row=3, column=1, pady=15, padx=20)
                
                # Quantity (Fixed at 10, can't be changed)
                Label(form_frame, text="Quantity (Fixed at 10):", bg=COLORS['card_bg'], 
                      font=FONTS['subheading']).grid(row=4, column=0, sticky=W, pady=15, padx=20)
                quantity_label = Label(form_frame, text="10", bg=COLORS['card_bg'], 
                                      font=FONTS['body'], fg=COLORS['primary'])
                quantity_label.grid(row=4, column=1, pady=15, padx=20, sticky=W)
                
                def save_changes():
                    try:
                        # Validate inputs
                        if not book_name_var.get().strip():
                            mb.showerror("Error", "Book name is required")
                            return
                        
                        fine_per_day_val = int(fine_var.get())
                        
                        if fine_per_day_val < 0:
                            mb.showerror("Error", "Fine per day cannot be negative")
                            return
                        
                        # Update the database (quantity is fixed at 10)
                        cursor.execute("""
                            UPDATE Library 
                            SET BK_NAME=?, AUTHOR_NAME=?, FINE_PER_DAY=?, QUANTITY=10
                            WHERE BK_ID=?
                        """, (
                            book_name_var.get().strip(),
                            author_var.get().strip(),
                            fine_per_day_val,
                            values[1]  # Original book ID
                        ))
                        
                        connector.commit()
                        
                        # Update the treeview if it still exists
                        if tree3.winfo_exists():
                            # Get updated issued count
                            cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_ID=? AND BK_STATUS='Issued'", (values[1],))
                            issued_count = cursor.fetchone()[0]
                            
                            # Get updated issue date
                            updated_issue_date = get_issue_date(values[1], values[4])
                            
                            tree3.item(selected, values=(
                                book_name_var.get().strip(),
                                values[1],  # Original book ID
                                author_var.get().strip(),
                                values[3],  # Original status
                                values[4],  # Original student ID
                                updated_issue_date,  # Updated issue date
                                values[6],  # Original due date
                                fine_per_day_val,
                                10,  # Fixed quantity of 10
                                issued_count  # Updated issued count
                            ))
                        
                        mb.showinfo("Success", "✅ Book details updated successfully!")
                        edit_win.destroy()
                        refresh_tree()
                        update_status()
                        
                    except ValueError:
                        mb.showerror("Error", "❌ Fine per Day must be a number")
                    except Exception as e:
                        mb.showerror("Error", f"❌ Failed to update book: {e}")
                
                # Buttons frame
                btn_frame = Frame(form_frame, bg=COLORS['card_bg'])
                btn_frame.grid(row=5, column=0, columnspan=2, pady=30)
                
                Button(btn_frame, text="Cancel", 
                       command=edit_win.destroy,
                       bg="#95A5A6",
                       fg="white",
                       font=FONTS['button'],
                       padx=20,
                       pady=8).pack(side=LEFT, padx=10)
                
                Button(btn_frame, text="Save Changes", 
                       command=save_changes,
                       bg=COLORS['success'],
                       fg="white",
                       font=FONTS['button'],
                       padx=20,
                       pady=8).pack(side=LEFT, padx=10)
                
                # Set focus to first editable field
                book_name_entry.focus_set()
                book_name_entry.select_range(0, END)
                
            except Exception as e:
                mb.showerror("Error", f"Failed to open edit window: {e}")
        
        def issue_selected_book():
            try:
                selected = tree3.focus()
                if not selected:
                    mb.showerror("Error","Select a book")
                    return
                values = tree3.item(selected)["values"]
                book_id_to_issue = values[1]

                sid = issuer_card()
                if not sid: 
                    return
                
                due = (datetime.now()+timedelta(days=14)).strftime("%Y-%m-%d")
                
                cursor.execute("UPDATE Library SET BK_STATUS='Issued', CARD_ID=?, DUE_DATE=? WHERE BK_ID=?", 
                               (sid, due, book_id_to_issue))
                connector.commit()
                
                send_issue_email(sid, values[0], values[1], due)
                mb.showinfo("Success",f"✅ Book '{values[0]}' issued to student {sid}. Stock remains at 10 units.")
                
                # Refresh only if treeview exists
                if tree3.winfo_exists():
                    refresh_tree()
                update_status()
                
            except Exception as e:
                mb.showerror("Error", f"Failed to issue book: {e}")

        def return_selected_book():
            try:
                selected = tree3.focus()
                if not selected:
                    mb.showerror("Error", "Select a book to return")
                    return
                values = tree3.item(selected)["values"]
                if values[3] == "Available" and values[4] == "N/A": 
                    mb.showinfo("Info", "This book is already available")
                    return
                
                student_id_returning = values[4] 
                book_name_returning = values[0]
                book_id_returning = values[1]

                cursor.execute("UPDATE Library SET BK_STATUS='Available', CARD_ID='N/A', DUE_DATE='N/A' WHERE BK_ID=?", 
                               (book_id_returning,))
                connector.commit()
                
                send_return_email(student_id_returning, book_name_returning, book_id_returning)
                mb.showinfo("Success", f"✅ Book '{book_name_returning}' returned. Stock remains at 10 units.")
                
                # Refresh only if treeview exists
                if tree3.winfo_exists():
                    refresh_tree()
                update_status()
                
            except Exception as e:
                mb.showerror("Error", f"Failed to return book: {e}")

        def pay_selected_fine():
            try:
                selected = tree3.focus()
                if not selected: 
                    return
                values = tree3.item(selected)["values"]
                fine = calculate_fine(values[6], int(values[7]) if values[7] else 5)
                if fine == 0: 
                    mb.showinfo("Info", "No fine pending for this book")
                    return
                if mb.askyesno("Confirm Payment",f"Fine Amount: ₹{fine}\nDo you want to pay this fine?"):
                    cursor.execute("INSERT INTO FineHistory VALUES (?,?,?,?)", 
                                  (values[4], values[1], fine, datetime.now().strftime("%Y-%m-%d")))
                    cursor.execute("UPDATE Library SET DUE_DATE=? WHERE BK_ID=?", 
                                  (datetime.now().strftime("%Y-%m-%d"), values[1]))
                    connector.commit()
                    
                    # Refresh only if treeview exists
                    if tree3.winfo_exists():
                        refresh_tree()
                    update_status()
                    mb.showinfo("Success", f"✅ Fine of ₹{fine} paid successfully")
                    
            except Exception as e:
                mb.showerror("Error", f"Failed to process fine: {e}")

        def delete_selected_book():
            try:
                selected = tree3.focus()
                if not selected: 
                    return
                bid = tree3.item(selected)["values"][1]
                book_name = tree3.item(selected)["values"][0]
                if mb.askyesno("Confirm Delete", f"Are you sure you want to delete '{book_name}'?"):
                    cursor.execute("DELETE FROM Library WHERE BK_ID=?", (bid,))
                    connector.commit()
                    
                    # Refresh only if treeview exists
                    if tree3.winfo_exists():
                        refresh_tree()
                    update_status()
                    mb.showinfo("Success", f"Book '{book_name}' deleted successfully")
                    
            except Exception as e:
                mb.showerror("Error", f"Failed to delete book: {e}")

        # Function to view book issue details
        def view_book_issue_details():
            selected = tree3.focus()
            if not selected:
                mb.showerror("Error", "Select a book to view issue details")
                return
            
            values = tree3.item(selected)["values"]
            book_id = values[1]
            book_name = values[0]
            
            # Create details window
            details_win = Toplevel(win)
            details_win.title(f"📖 Issue Details: {book_name}")
            details_win.geometry("600x400")
            details_win.config(bg=COLORS['light_bg'])
            
            details_win.update_idletasks()
            width = 600
            height = 400
            x = (details_win.winfo_screenwidth() // 2) - (width // 2)
            y = (details_win.winfo_screenheight() // 2) - (height // 2)
            details_win.geometry(f'{width}x{height}+{x}+{y}')
            
            # Header
            header = Frame(details_win, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text=f"📖 {book_name} - Issue Details", 
                  bg=COLORS['primary'], fg="white",
                  font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Get all issued copies of this book with issue dates
            cursor.execute("""
                SELECT CARD_ID, DUE_DATE, FINE_PER_DAY 
                FROM Library 
                WHERE BK_ID=? AND BK_STATUS='Issued'
            """, (book_id,))
            issued_copies = cursor.fetchall()
            
            if not issued_copies:
                # Show message if no copies are issued
                no_issues_frame = Frame(details_win, bg=COLORS['card_bg'])
                no_issues_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                
                Label(no_issues_frame, 
                      text="✅ No copies of this book are currently issued.",
                      bg=COLORS['card_bg'], font=FONTS['subheading'],
                      fg=COLORS['success']).pack(expand=True)
                
                # Show total quantity (always 10)
                Label(no_issues_frame, 
                      text=f"📚 Total copies available: 10 (Fixed)",
                      bg=COLORS['card_bg'], font=FONTS['body']).pack(pady=10)
            else:
                # Create table for issued copies
                table_frame = Frame(details_win, bg=COLORS['card_bg'])
                table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                
                # Summary
                summary_frame = Frame(table_frame, bg=COLORS['light_bg'], relief="solid", bd=1)
                summary_frame.pack(fill=X, pady=(0, 10))
                
                total_copies = len(issued_copies)
                Label(summary_frame, 
                      text=f"📊 {total_copies} copy(ies) currently issued out of 10 total copies",
                      bg=COLORS['light_bg'], font=FONTS['subheading']).pack(pady=10)
                
                # Create table
                scrollbar = Scrollbar(table_frame)
                scrollbar.pack(side=RIGHT, fill=Y)
                
                issue_tree = ttk.Treeview(table_frame,
                                         columns=("Copy #", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Status"),
                                         show="headings",
                                         yscrollcommand=scrollbar.set,
                                         height=8)
                
                for col, width in zip(["Copy #", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Status"], 
                                     [70, 100, 100, 100, 80, 100]):
                    issue_tree.heading(col, text=col)
                    issue_tree.column(col, width=width, anchor=CENTER)
                
                issue_tree.pack(fill=BOTH, expand=True)
                scrollbar.config(command=issue_tree.yview)
                
                # Add issued copies to table with issue dates
                for i, (student_id, due_date, fine_per_day) in enumerate(issued_copies, 1):
                    # Calculate issue date (14 days before due date)
                    if due_date != "N/A":
                        try:
                            due = datetime.strptime(due_date, "%Y-%m-%d")
                            issue = due - timedelta(days=14)
                            display_issue_date = issue.strftime("%Y-%m-%d")
                        except:
                            display_issue_date = "N/A"
                    else:
                        display_issue_date = "N/A"
                    
                    # Calculate fine if overdue
                    fine_amount = calculate_fine(due_date, fine_per_day)
                    status = "✅ On Time" if fine_amount == 0 else f"⚠️ Overdue (₹{fine_amount})"
                    
                    issue_tree.insert("", END, values=(
                        f"Copy {i}",
                        student_id,
                        display_issue_date,
                        due_date,
                        f"₹{fine_per_day}",
                        status
                    ))
                
                # Get student names for issued copies
                student_info = []
                for student_id, _, _ in issued_copies:
                    cursor.execute("SELECT NAME FROM Students WHERE STUDENT_ID=?", (student_id,))
                    student_name = cursor.fetchone()
                    if student_name:
                        student_info.append(f"• {student_name[0]} ({student_id})")
                
                if student_info:
                    info_frame = Frame(table_frame, bg=COLORS['card_bg'])
                    info_frame.pack(fill=X, pady=10)
                    
                    Label(info_frame, text="👨‍🎓 Issued to:", 
                          bg=COLORS['card_bg'], font=FONTS['body'], 
                          fg=COLORS['primary']).pack(anchor=W)
                    
                    for info in student_info:
                        Label(info_frame, text=info, 
                              bg=COLORS['card_bg'], font=("Segoe UI", 9)).pack(anchor=W)
            
            # Close button
            Button(details_win, text="Close",
                   command=details_win.destroy,
                   bg="#95A5A6",
                   fg="white",
                   font=FONTS['button'],
                   padx=20,
                   pady=8).pack(pady=10)

        # ===== ENHANCED FEATURE: VIEW BOOKS BY COURSE WITH PRE-DEFINED BOOKS =====
        def view_books_by_course():
            course_win = Toplevel(win)
            course_win.title("📚 Books by Course & Year")
            course_win.geometry("1200x600")
            course_win.config(bg=COLORS['light_bg'])
            
            course_win.update_idletasks()
            width = 1200
            height = 600
            x = (course_win.winfo_screenwidth() // 2) - (width // 2)
            y = (course_win.winfo_screenheight() // 2) - (height // 2)
            course_win.geometry(f'{width}x{height}+{x}+{y}')
            
            # Header
            header = Frame(course_win, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text="📚 BOOKS BY COURSE & YEAR", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Course selection frame
            course_frame = Frame(course_win, bg=COLORS['light_bg'], padx=20, pady=10)
            course_frame.pack(fill=X)
            
            Label(course_frame, text="Select Course:", bg=COLORS['light_bg'],
                  font=FONTS['subheading']).pack(side=LEFT, padx=(0, 10))
            
            # Course selection
            course_var = StringVar(value="Select Course")
            courses = ["Select Course", "BCA", "BSC", "B.COM", "BA", "BBA", "Other"]
            course_menu = ttk.Combobox(course_frame, textvariable=course_var, 
                                      values=courses, state="readonly", width=15,
                                      font=FONTS['body'])
            course_menu.pack(side=LEFT, padx=(0, 20))
            
            # Year selection
            Label(course_frame, text="Select Year:", bg=COLORS['light_bg'],
                  font=FONTS['subheading']).pack(side=LEFT, padx=(0, 10))
            
            year_var = StringVar(value="Select Year")
            years = ["Select Year", "1st Year", "2nd Year", "3rd Year", "4th Year"]
            year_menu = ttk.Combobox(course_frame, textvariable=year_var, 
                                    values=years, state="readonly", width=12,
                                    font=FONTS['body'])
            year_menu.pack(side=LEFT)
            
            # Search entry
            search_course_var = StringVar()
            Label(course_frame, text="Search:", bg=COLORS['light_bg'],
                  font=FONTS['subheading']).pack(side=LEFT, padx=(40, 10))
            
            search_entry = Entry(course_frame, textvariable=search_course_var, 
                                font=FONTS['body'], width=30, relief="solid", bd=1)
            search_entry.pack(side=LEFT, padx=(0, 10))
            
            # ===== PRE-DEFINED BOOKS DATABASE =====
            predefined_books = {
                "BCA": {
                    "1st Year": [
                        ["Introduction to Computers", "BCA101", "P.K. Sinha", 5, 10],
                        ["Programming in C", "BCA102", "E. Balagurusamy", 5, 10],
                        ["Digital Electronics", "BCA103", "Morris Mano", 5, 10],
                        ["Mathematics for Computing", "BCA104", "R.D. Sharma", 5, 10],
                        ["Business Communication", "BCA105", "R.K. Madhukar", 5, 10]
                    ],
                    "2nd Year": [
                        ["Data Structures", "BCA201", "Seymour Lipschutz", 5, 10],
                        ["Object Oriented Programming with C++", "BCA202", "Robert Lafore", 5, 10],
                        ["Database Management Systems", "BCA203", "Raghu Ramakrishnan", 5, 10],
                        ["Operating Systems", "BCA204", "Silberschatz", 5, 10],
                        ["Web Technologies", "BCA205", "Achyut Godbole", 5, 10]
                    ],
                    "3rd Year": [
                        ["Software Engineering", "BCA301", "Roger Pressman", 5, 10],
                        ["Computer Networks", "BCA302", "Andrew Tanenbaum", 5, 10],
                        ["Java Programming", "BCA303", "Herbert Schildt", 5, 10],
                        ["Python Programming", "BCA304", "Mark Lutz", 5, 10],
                        ["Cloud Computing", "BCA305", "Rajkumar Buyya", 5, 10]
                    ]
                },
                "BSC": {
                    "1st Year": [
                        ["Fundamentals of computer- I", "BSC101", "E. Balagurusam", 5, 10],
                        ["Data Structure- I", "BSC102", "Donald Knuth", 5, 10],
                        ["RDBMS - I", "BSC103", "Edgar F. Codd", 5, 10],
                        ["web tech", "BSC104", "Achyut S. Godbole", 5, 10],
                        ["C Programming", "BSC105", "Dennis Ritchie", 5, 10]
                    ],
                    "2nd Year": [
                        ["Software testing- II", "BSC201", " Ron Patton", 5, 10],
                        ["windows Programming- II", "BSC202", "Charles Petzold", 5, 10],
                        ["Python - II", "BSC203", "Mark Lutz", 5, 10],
                        ["Statistics", "BSC204", "Karl Pearson", 5, 10],
                        ["java", "BSC205", "Herbert Schildt", 5, 10]
                    ],
                    "3rd Year": [
                        ["image processing", "BSC301", "Rafael C.Gonzalez", 5, 10],
                        ["SPM", "BSC302", "Mike Cotterell", 5, 10],
                        ["Android Studio", "BSC303", "Neil Smyth", 5, 10],
                        ["Machine learning", "BSC304", "Tom Mitchell", 5, 10],
                        ["Research Methodology", "BSC305", "C.R. Kothari", 5, 10]
                    ]
                },
                "B.COM": {
                    "1st Year": [
                        ["Financial Accounting", "BCOM101", "S.N. Maheshwari", 5, 10],
                        ["Business Economics", "BCOM102", "H.L. Ahuja", 5, 10],
                        ["Business Law", "BCOM103", "N.D. Kapoor", 5, 10],
                        ["Business Mathematics", "BCOM104", "J.K. Thukral", 5, 10],
                        ["Principles of Management", "BCOM105", "Prasad & Prasad", 5, 10]
                    ],
                    "2nd Year": [
                        ["Cost Accounting", "BCOM201", "Jain & Narang", 5, 10],
                        ["Corporate Accounting", "BCOM202", "S.P. Iyengar", 5, 10],
                        ["Income Tax", "BCOM203", "V.K. Singhania", 5, 10],
                        ["Business Statistics", "BCOM204", "S.P. Gupta", 5, 10],
                        ["Marketing Management", "BCOM205", "Philip Kotler", 5, 10]
                    ],
                    "3rd Year": [
                        ["Auditing", "BCOM301", "D.K. Mittal", 5, 10],
                        ["Management Accounting", "BCOM302", "Khan & Jain", 5, 10],
                        ["Financial Management", "BCOM303", "I.M. Pandey", 5, 10],
                        ["Indian Economy", "BCOM304", "Mishra & Puri", 5, 10],
                        ["Entrepreneurship", "BCOM305", "Robert Hisrich", 5, 10]
                    ]
                },
                "BA": {
                    "1st Year": [
                        ["English Literature - I", "BA101", "William Shakespeare", 5, 10],
                        ["History of India - I", "BA102", "Romila Thapar", 5, 10],
                        ["Political Theory", "BA103", "O.P. Gauba", 5, 10],
                        ["Sociology - I", "BA104", "Haralambos & Holborn", 5, 10],
                        ["Psychology - I", "BA105", "Morgan & King", 5, 10]
                    ],
                    "2nd Year": [
                        ["English Literature - II", "BA201", "Jane Austen", 5, 10],
                        ["History of India - II", "BA202", "Bipin Chandra", 5, 10],
                        ["Indian Constitution", "BA203", "D.D. Basu", 5, 10],
                        ["Sociology - II", "BA204", "Anthony Giddens", 5, 10],
                        ["Psychology - II", "BA205", "Baron & Misra", 5, 10]
                    ],
                    "3rd Year": [
                        ["Modern English Literature", "BA301", "T.S. Eliot", 5, 10],
                        ["World History", "BA302", "H.G. Wells", 5, 10],
                        ["International Relations", "BA303", "Palmer & Perkins", 5, 10],
                        ["Social Anthropology", "BA304", "E.E. Evans-Pritchard", 5, 10],
                        ["Clinical Psychology", "BA305", "Barlow & Durand", 5, 10]
                    ]
                },
                "BBA": {
                    "1st Year": [
                        ["Principles of Management", "BBA101", "Koontz & O'Donnell", 5, 10],
                        ["Business Economics", "BBA102", "P.N. Chopra", 5, 10],
                        ["Financial Accounting", "BBA103", "Mukherjee & Hanif", 5, 10],
                        ["Business Mathematics", "BBA104", "Qazi Zameeruddin", 5, 10],
                        ["Organizational Behavior", "BBA105", "Stephen Robbins", 5, 10]
                    ],
                    "2nd Year": [
                        ["Human Resource Management", "BBA201", "Gary Dessler", 5, 10],
                        ["Marketing Management", "BBA202", "Philip Kotler", 5, 10],
                        ["Financial Management", "BBA203", "Prasanna Chandra", 5, 10],
                        ["Business Statistics", "BBA204", "S.P. Gupta", 5, 10],
                        ["Production Management", "BBA205", "Buffa & Sarin", 5, 10]
                    ],
                    "3rd Year": [
                        ["Strategic Management", "BBA301", "Fred David", 5, 10],
                        ["International Business", "BBA302", "Charles Hill", 5, 10],
                        ["Management Information Systems", "BBA303", "James O'Brien", 5, 10],
                        ["Business Research Methods", "BBA304", "William Zikmund", 5, 10],
                        ["Entrepreneurship Development", "BBA305", "Robert Hisrich", 5, 10]
                    ]
                }
            }
            
            def filter_books():
                course = course_var.get()
                year = year_var.get()
                search_text = search_course_var.get().strip().upper()
                
                # Clear tree
                for i in tree_course.get_children():
                    tree_course.delete(i)
                
                # Check if both course and year are selected
                if course == "Select Course" or year == "Select Year":
                    status_label.config(text="⚠️ Please select both Course and Year to view predefined books")
                    return
                
                # Check if we have predefined books for this course and year
                if course in predefined_books and year in predefined_books[course]:
                    # Add predefined books for this course and year
                    books = predefined_books[course][year]
                    for book in books:
                        book_name = book[0]
                        book_id = book[1]
                        author_name = book[2]
                        fine_per_day = book[3]
                        quantity = 10  # Always 10
                        
                        # Apply search filter if any
                        if search_text:
                            if (search_text not in book_name.upper() and 
                                search_text not in book_id.upper() and 
                                search_text not in author_name.upper()):
                                continue
                        
                        # Check if book exists in actual library database
                        cursor.execute("SELECT BK_STATUS, CARD_ID, DUE_DATE FROM Library WHERE BK_ID=?", (book_id,))
                        db_book = cursor.fetchone()
                        
                        if db_book:
                            # Book exists in database, get actual status
                            status = db_book[0]
                            card_id = db_book[1]
                            due_date = db_book[2]
                            # Get issue date
                            issue_date = get_issue_date(book_id, card_id)
                        else:
                            # Book not in database, show predefined values
                            status = "Available"
                            card_id = "N/A"
                            due_date = "N/A"
                            issue_date = "N/A"
                        
                        # Get issued count for this book
                        cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_ID=? AND BK_STATUS='Issued'", (book_id,))
                        issued_count = cursor.fetchone()[0]
                        
                        # Insert book into treeview with issue date and issued count
                        tree_course.insert("", END, values=[
                            book_name,
                            book_id,
                            author_name,
                            status,
                            card_id,
                            issue_date,  # Issue Date
                            due_date,
                            fine_per_day,
                            10,  # Always 10
                            issued_count  # Add issued count as last column
                        ])
                    
                    status_label.config(text=f"📚 Showing {len(books)} predefined books for {course} - {year}")
                
                else:
                    status_label.config(text=f"⚠️ No predefined books found for {course} - {year}")
            
            # Add "Add to Library" button
            def add_predefined_to_library():
                course = course_var.get()
                year = year_var.get()
                
                if course == "Select Course" or year == "Select Year":
                    mb.showerror("Error", "Please select both Course and Year")
                    return
                
                if course not in predefined_books or year not in predefined_books[course]:
                    mb.showerror("Error", f"No predefined books found for {course} - {year}")
                    return
                
                # Get all books for this course and year
                books = predefined_books[course][year]
                
                # Add to database
                added_count = 0
                already_exists_count = 0
                
                for book in books:
                    book_name = book[0]
                    book_id = book[1]
                    author_name = book[2]
                    fine_per_day = book[3]
                    quantity = 10  # Always 10
                    
                    try:
                        # Check if book already exists
                        cursor.execute("SELECT * FROM Library WHERE BK_ID=?", (book_id,))
                        if cursor.fetchone():
                            already_exists_count += 1
                        else:
                            # Add to database
                            cursor.execute("INSERT INTO Library VALUES (?,?,?,?,?,?,?,?)",
                                (book_name, book_id, author_name, "Available", "N/A", "N/A", fine_per_day, 10))  # Quantity fixed at 10
                            added_count += 1
                    except Exception as e:
                        print(f"Error adding book {book_id}: {e}")
                
                connector.commit()
                
                # Show summary
                if added_count > 0 or already_exists_count > 0:
                    message = ""
                    if added_count > 0:
                        message += f"✅ Successfully added {added_count} new books to the library database (each with 10 units).\n\n"
                    if already_exists_count > 0:
                        message += f"⚠️ {already_exists_count} books were already in the database (not duplicated)."
                    
                    mb.showinfo("Add to Library", message)
                    
                    # Refresh the tree to show newly added books
                    filter_books()
                    # Also refresh the main book view if it exists
                    if 'tree' in globals() and tree.winfo_exists():
                        display_records("")
                    update_status()
                else:
                    mb.showinfo("Info", "No books were added to the library.")
            
            # Filter button
            filter_btn = Button(course_frame, text="🔍 Filter", 
                               command=filter_books,
                               bg=COLORS['secondary'],
                               fg="white",
                               font=FONTS['button'],
                               padx=15,
                               pady=3)
            filter_btn.pack(side=LEFT, padx=(5, 10))
            
            # Add to Library button
            add_to_lib_btn = Button(course_frame, text="➕ Add to Library", 
                                   command=add_predefined_to_library,
                                   bg=COLORS['success'],
                                   fg="white",
                                   font=FONTS['button'],
                                   padx=10,
                                   pady=3)
            add_to_lib_btn.pack(side=LEFT, padx=5)
            
            # Treeview frame
            tree_frame_course = Frame(course_win, bg=COLORS['card_bg'])
            tree_frame_course.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            # Scrollbars
            v_scroll = Scrollbar(tree_frame_course)
            v_scroll.pack(side=RIGHT, fill=Y)
            
            h_scroll = Scrollbar(tree_frame_course, orient=HORIZONTAL)
            h_scroll.pack(side=BOTTOM, fill=X)
            
            # Course treeview with Issue Date and Issued Count columns
            tree_course = ttk.Treeview(tree_frame_course,
                                      columns=("Name","ID","Author","Status","Student ID","Issue Date","Due Date","Fine/Day","Quantity","Issued Count"), 
                                      show="headings",
                                      yscrollcommand=v_scroll.set,
                                      xscrollcommand=h_scroll.set,
                                      height=15)
            
            columns = ["Name","ID","Author","Status","Student ID","Issue Date","Due Date","Fine/Day","Quantity","Issued Count"]
            widths = [200, 90, 120, 90, 90, 100, 100, 80, 80, 100]
            
            for col, width in zip(columns, widths):
                tree_course.heading(col, text=col)
                tree_course.column(col, width=width, anchor=CENTER)
            
            tree_course.pack(fill=BOTH, expand=True)
            v_scroll.config(command=tree_course.yview)
            h_scroll.config(command=tree_course.xview)
            
            # Status label
            status_label = Label(course_win, text="📚 Select course and year to view predefined books",
                                bg=COLORS['light_bg'], font=("Segoe UI", 10))
            status_label.pack(pady=(5, 10))
            
            # Action buttons frame
            action_frame = Frame(course_win, bg=COLORS['light_bg'])
            action_frame.pack(pady=(0, 15))
            
            # Function to check if treeview exists
            def course_tree_exists():
                return tree_course.winfo_exists() if 'tree_course' in locals() else False
            
            # Issue Book for course view
            def issue_course_book():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected:
                    mb.showerror("Error","Select a book")
                    return
                
                values = tree_course.item(selected)["values"]
                
                # Check if book exists in actual database
                cursor.execute("SELECT * FROM Library WHERE BK_ID=?", (values[1],))
                db_book = cursor.fetchone()
                
                if db_book:
                    # Book exists in database, proceed with issue
                    pass
                else:
                    # Book is predefined but not in database
                    mb.showerror("Error", "This book is not yet added to the library. Please add it first.")
                    return
                
                sid = issuer_card()
                if not sid: 
                    return
                
                due = (datetime.now()+timedelta(days=14)).strftime("%Y-%m-%d")
                
                cursor.execute("UPDATE Library SET BK_STATUS='Issued', CARD_ID=?, DUE_DATE=? WHERE BK_ID=?", 
                               (sid, due, values[1]))
                connector.commit()
                
                send_issue_email(sid, values[0], values[1], due)
                mb.showinfo("Success",f"✅ Book '{values[0]}' issued to student {sid}. Stock remains at 10 units.")
                filter_books()  # Refresh the filtered view
                if 'tree' in globals() and tree.winfo_exists():
                    display_records("")  # Refresh main view
                update_status()
            
            # Return Book for course view
            def return_course_book():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected:
                    mb.showerror("Error", "Select a book to return")
                    return
                values = tree_course.item(selected)["values"]
                
                # Check if book exists in database
                cursor.execute("SELECT * FROM Library WHERE BK_ID=?", (values[1],))
                db_book = cursor.fetchone()
                
                if not db_book:
                    mb.showerror("Error", "This book is not in the library database")
                    return
                
                if values[3] == "Available" and values[4] == "N/A": 
                    mb.showinfo("Info", "This book is already available")
                    return
                
                student_id_returning = values[4] 
                book_name_returning = values[0]
                book_id_returning = values[1]

                cursor.execute("UPDATE Library SET BK_STATUS='Available', CARD_ID='N/A', DUE_DATE='N/A' WHERE BK_ID=?", 
                               (book_id_returning,))
                connector.commit()
                
                send_return_email(student_id_returning, book_name_returning, book_id_returning)
                mb.showinfo("Success", f"✅ Book '{book_name_returning}' returned. Stock remains at 10 units.")
                filter_books()  # Refresh the filtered view
                if 'tree' in globals() and tree.winfo_exists():
                    display_records("")  # Refresh main view
                update_status()
            
            # Pay Fine for course view
            def pay_course_fine():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected: 
                    return
                values = tree_course.item(selected)["values"]
                fine = calculate_fine(values[6], int(values[7]) if values[7] else 5)
                if fine == 0: 
                    mb.showinfo("Info", "No fine pending for this book")
                    return
                if mb.askyesno("Confirm Payment",f"Fine Amount: ₹{fine}\nDo you want to pay this fine?"):
                    cursor.execute("INSERT INTO FineHistory VALUES (?,?,?,?)", 
                                  (values[4], values[1], fine, datetime.now().strftime("%Y-%m-%d")))
                    cursor.execute("UPDATE Library SET DUE_DATE=? WHERE BK_ID=?", 
                                  (datetime.now().strftime("%Y-%m-%d"), values[1]))
                    connector.commit()
                    filter_books()  # Refresh the filtered view
                    if 'tree' in globals() and tree.winfo_exists():
                        display_records("")  # Refresh main view
                    update_status()
                    mb.showinfo("Success", f"✅ Fine of ₹{fine} paid successfully")
            
            # Edit Book for course view
            def edit_course_book():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected:
                    mb.showerror("Error", "Select a book to edit")
                    return
                
                values = tree_course.item(selected)["values"]
                
                # Check if book exists in database
                cursor.execute("SELECT * FROM Library WHERE BK_ID=?", (values[1],))
                db_book = cursor.fetchone()
                
                if not db_book:
                    mb.showerror("Error", "This book is not in the library database. Please add it first.")
                    return
                
                # Reuse the existing edit_book_details functionality from main view
                edit_book_details()
            
            # Delete Book for course view
            def delete_course_book():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected: 
                    return
                bid = tree_course.item(selected)["values"][1]
                book_name = tree_course.item(selected)["values"][0]
                if mb.askyesno("Confirm Delete", f"Are you sure you want to delete '{book_name}'?"):
                    cursor.execute("DELETE FROM Library WHERE BK_ID=?", (bid,))
                    connector.commit()
                    filter_books()  # Refresh the filtered view
                    if 'tree' in globals() and tree.winfo_exists():
                        display_records("")  # Refresh main view
                    update_status()
                    mb.showinfo("Success", f"Book '{book_name}' deleted successfully")
            
            # View Issue Details for course view
            def view_course_issue_details():
                if not course_tree_exists():
                    return
                selected = tree_course.focus()
                if not selected:
                    mb.showerror("Error", "Select a book to view issue details")
                    return
                
                values = tree_course.item(selected)["values"]
                book_id = values[1]
                book_name = values[0]
                
                # Create details window
                details_win = Toplevel(course_win)
                details_win.title(f"📖 Issue Details: {book_name}")
                details_win.geometry("600x400")
                details_win.config(bg=COLORS['light_bg'])
                
                details_win.update_idletasks()
                width = 600
                height = 400
                x = (details_win.winfo_screenwidth() // 2) - (width // 2)
                y = (details_win.winfo_screenheight() // 2) - (height // 2)
                details_win.geometry(f'{width}x{height}+{x}+{y}')
                
                # Header
                header = Frame(details_win, bg=COLORS['primary'], height=70)
                header.pack(fill=X)
                header.pack_propagate(False)
                
                Label(header, text=f"📖 {book_name} - Issue Details", 
                      bg=COLORS['primary'], fg="white",
                      font=FONTS['heading']).pack(expand=True, pady=15)
                
                # Get all issued copies of this book
                cursor.execute("""
                    SELECT CARD_ID, DUE_DATE, FINE_PER_DAY 
                    FROM Library 
                    WHERE BK_ID=? AND BK_STATUS='Issued'
                """, (book_id,))
                issued_copies = cursor.fetchall()
                
                if not issued_copies:
                    # Show message if no copies are issued
                    no_issues_frame = Frame(details_win, bg=COLORS['card_bg'])
                    no_issues_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                    
                    Label(no_issues_frame, 
                          text="✅ No copies of this book are currently issued.",
                          bg=COLORS['card_bg'], font=FONTS['subheading'],
                          fg=COLORS['success']).pack(expand=True)
                    
                    # Show total quantity (always 10)
                    Label(no_issues_frame, 
                          text=f"📚 Total copies available: 10 (Fixed)",
                          bg=COLORS['card_bg'], font=FONTS['body']).pack(pady=10)
                else:
                    # Create table for issued copies
                    table_frame = Frame(details_win, bg=COLORS['card_bg'])
                    table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                    
                    # Summary
                    summary_frame = Frame(table_frame, bg=COLORS['light_bg'], relief="solid", bd=1)
                    summary_frame.pack(fill=X, pady=(0, 10))
                    
                    total_copies = len(issued_copies)
                    Label(summary_frame, 
                          text=f"📊 {total_copies} copy(ies) currently issued out of 10 total copies",
                          bg=COLORS['light_bg'], font=FONTS['subheading']).pack(pady=10)
                    
                    # Create table
                    scrollbar = Scrollbar(table_frame)
                    scrollbar.pack(side=RIGHT, fill=Y)
                    
                    issue_tree = ttk.Treeview(table_frame,
                                             columns=("Copy #", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Status"),
                                             show="headings",
                                             yscrollcommand=scrollbar.set,
                                             height=8)
                    
                    for col, width in zip(["Copy #", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Status"], 
                                         [70, 100, 100, 100, 80, 100]):
                        issue_tree.heading(col, text=col)
                        issue_tree.column(col, width=width, anchor=CENTER)
                    
                    issue_tree.pack(fill=BOTH, expand=True)
                    scrollbar.config(command=issue_tree.yview)
                    
                    # Add issued copies to table
                    for i, (student_id, due_date, fine_per_day) in enumerate(issued_copies, 1):
                        # Calculate issue date (14 days before due date)
                        if due_date != "N/A":
                            try:
                                due = datetime.strptime(due_date, "%Y-%m-%d")
                                issue = due - timedelta(days=14)
                                display_issue_date = issue.strftime("%Y-%m-%d")
                            except:
                                display_issue_date = "N/A"
                        else:
                            display_issue_date = "N/A"
                        
                        # Calculate fine if overdue
                        fine_amount = calculate_fine(due_date, fine_per_day)
                        status = "✅ On Time" if fine_amount == 0 else f"⚠️ Overdue (₹{fine_amount})"
                        
                        issue_tree.insert("", END, values=(
                            f"Copy {i}",
                            student_id,
                            display_issue_date,
                            due_date,
                            f"₹{fine_per_day}",
                            status
                        ))
                    
                    # Get student names for issued copies
                    student_info = []
                    for student_id, _, _ in issued_copies:
                        cursor.execute("SELECT NAME FROM Students WHERE STUDENT_ID=?", (student_id,))
                        student_name = cursor.fetchone()
                        if student_name:
                            student_info.append(f"• {student_name[0]} ({student_id})")
                    
                    if student_info:
                        info_frame = Frame(table_frame, bg=COLORS['card_bg'])
                        info_frame.pack(fill=X, pady=10)
                        
                        Label(info_frame, text="👨‍🎓 Issued to:", 
                              bg=COLORS['card_bg'], font=FONTS['body'], 
                              fg=COLORS['primary']).pack(anchor=W)
                        
                        for info in student_info:
                            Label(info_frame, text=info, 
                                  bg=COLORS['card_bg'], font=("Segoe UI", 9)).pack(anchor=W)
                
                # Close button
                Button(details_win, text="Close",
                       command=details_win.destroy,
                       bg="#95A5A6",
                       fg="white",
                       font=FONTS['button'],
                       padx=20,
                       pady=8).pack(pady=10)
            
            # Action buttons (similar to main view)
            Button(action_frame, text="📖 View Issue Details",
                   command=view_course_issue_details,
                   bg="#17a2b8",
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Issue Book",
                   command=issue_course_book,
                   bg=COLORS['success'],
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Return Book",
                   command=return_course_book,
                   bg="#17a2b8",
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Pay Fine",
                   command=pay_course_fine,
                   bg=COLORS['warning'],
                   fg="black",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Edit Book",
                   command=edit_course_book,
                   bg="#9B59B6",
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Delete Book",
                   command=delete_course_book,
                   bg=COLORS['accent'],
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Refresh",
                   command=filter_books,
                   bg="#95A5A6",
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            Button(action_frame, text="Close",
                   command=course_win.destroy,
                   bg="#7F8C8D",
                   fg="white",
                   font=FONTS['button'],
                   padx=12,
                   pady=6).pack(side=LEFT, padx=3)
            
            # Load all books initially
            filter_books()
            
            # Bind Enter key to search
            search_entry.bind('<Return>', lambda e: filter_books())
            search_entry.focus_set()

        # Buttons frame (ADD THE NEW BUTTONS HERE)
        btn_frame = Frame(win, bg=COLORS['light_bg'])
        btn_frame.pack(pady=(0, 10))
        
        # Add the new "View Issue Details" button FIRST
        Button(btn_frame, text="📖 View Issue Details",
               command=view_book_issue_details,
               bg="#17a2b8",  # Teal color for distinction
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        # Add the "View by Course" button
        Button(btn_frame, text="📚 View by Course",
               command=view_books_by_course,
               bg="#2ECC71",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        # Existing buttons
        Button(btn_frame, text="Issue Book",
               command=issue_selected_book,
               bg=COLORS['success'],
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Return Book",
               command=return_selected_book,
               bg="#17a2b8",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Pay Fine",
               command=pay_selected_fine,
               bg=COLORS['warning'],
               fg="black",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Edit Book",
               command=edit_book_details,
               bg="#9B59B6",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Delete Book",
               command=delete_selected_book,
               bg=COLORS['accent'],
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Refresh",
               command=lambda: [refresh_tree(), highlight_issued_books()],
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Close",
               command=win.destroy,
               bg="#7F8C8D",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=5)
        
        # Handle window close event
        def on_closing():
            win.destroy()
        
        win.protocol("WM_DELETE_WINDOW", on_closing)

    def view_issued_history():
        win = Toplevel(root)
        win.title("📖 Issued Book History")
        win.geometry("950x400")  # Increased width for issue date column
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 950
        height = 400
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="📖 ISSUED BOOK HISTORY", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        tree_frame = Frame(win, bg=COLORS['card_bg'])
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Updated to include Issue Date column
        tree_hist = ttk.Treeview(tree_frame,
                                columns=("Book Name","Book ID","Student ID","Issue Date","Due Date","Status"), 
                                show="headings",
                                yscrollcommand=scrollbar.set)
        
        for col, width in zip(["Book Name","Book ID","Student ID","Issue Date","Due Date","Status"], 
                             [250, 100, 100, 100, 100, 100]):
            tree_hist.heading(col, text=col)
            tree_hist.column(col, width=width, anchor=CENTER)
        
        tree_hist.pack(fill=BOTH, expand=True)
        scrollbar.config(command=tree_hist.yview)
        
        # Get issued books with issue dates
        for r in cursor.execute("SELECT BK_NAME,BK_ID,CARD_ID,DUE_DATE,BK_STATUS FROM Library WHERE CARD_ID!='N/A'").fetchall():
            # Calculate issue date from due date
            if r[3] != "N/A":
                try:
                    due_date = datetime.strptime(r[3], "%Y-%m-%d")
                    issue_date = (due_date - timedelta(days=14)).strftime("%Y-%m-%d")
                    display_issue_date = issue_date
                except:
                    display_issue_date = "N/A"
            else:
                display_issue_date = "N/A"
            
            # Create row with issue date
            row_with_issue = (r[0], r[1], r[2], display_issue_date, r[3], r[4])
            tree_hist.insert("", END, values=row_with_issue)
        
        Button(win, text="Close",
               command=win.destroy,
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(pady=10)

    def view_student_books():
        win = Toplevel(root)
        win.title("🎓 Student + Issued Books Info")
        win.geometry("1050x450")  # Increased width for issue date column
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 1050
        height = 450
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="🎓 STUDENT + ISSUED BOOKS", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        tree_frame = Frame(win, bg=COLORS['card_bg'])
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Updated to include Issue Date column
        tree_sb = ttk.Treeview(tree_frame, 
                              columns=("Student ID","Name","Class","Contact","Book Name","Book ID","Issue Date","Due Date","Fine/Day"), 
                              show="headings",
                              yscrollcommand=scrollbar.set)
        
        cols = ["Student ID","Name","Class","Contact","Book Name","Book ID","Issue Date","Due Date","Fine/Day"]
        widths = [100, 150, 80, 120, 200, 100, 100, 100, 80]
        
        for col, width in zip(cols, widths):
            tree_sb.heading(col, text=col)
            tree_sb.column(col, width=width, anchor=CENTER)
        
        tree_sb.pack(fill=BOTH, expand=True)
        scrollbar.config(command=tree_sb.yview)
        
        rows = cursor.execute("""
            SELECT S.STUDENT_ID, S.NAME, S.CLASS, S.CONTACT,
                   L.BK_NAME, L.BK_ID, L.DUE_DATE, L.FINE_PER_DAY 
            FROM Students S 
            LEFT JOIN Library L ON S.STUDENT_ID = L.CARD_ID AND L.BK_STATUS = 'Issued'
            ORDER BY S.STUDENT_ID
        """).fetchall()
        
        for r in rows: 
            # Calculate issue date from due date
            if r[6] != "N/A" and r[6]:
                try:
                    due_date = datetime.strptime(r[6], "%Y-%m-%d")
                    issue_date = (due_date - timedelta(days=14)).strftime("%Y-%m-%d")
                    display_issue_date = issue_date
                except:
                    display_issue_date = "N/A"
            else:
                display_issue_date = "N/A"
            
            # Create row with issue date
            row_with_issue = (r[0], r[1], r[2], r[3], r[4], r[5], display_issue_date, r[6], r[7])
            tree_sb.insert("", END, values=row_with_issue)
        
        Button(win, text="Close",
               command=win.destroy,
               bg="#95A5A6",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(pady=10)

    def show_pie_chart():
        total = cursor.execute("SELECT SUM(QUANTITY) FROM Library").fetchone()[0] or 0
        issued = cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Issued'").fetchone()[0]
        
        if total == 0:
            mb.showinfo("Info", "Library database is empty.")
            return
        
        if not MATPLOTLIB_AVAILABLE:
            # Show text-based statistics if matplotlib is not available
            if issued == 0:
                message = f"📊 Library Statistics\n\nAll books are available\n\n📚 Total Books: {total}\n📖 Issued Books: 0\n📈 Available: 100%"
            else:
                available = total - issued
                issued_percent = (issued / total) * 100
                available_percent = (available / total) * 100
                
                message = f"""📊 Library Statistics

📚 Total Books: {total}
📖 Issued Books: {issued} ({issued_percent:.1f}%)
📈 Available Books: {available} ({available_percent:.1f}%)

📊 Status Summary:
- Issued: {'█' * int(issued_percent/10)}{'░' * (10 - int(issued_percent/10))} {issued_percent:.1f}%
- Available: {'█' * int(available_percent/10)}{'░' * (10 - int(available_percent/10))} {available_percent:.1f}%"""
            
            mb.showinfo("Library Statistics", message)
            return
        
        try:
            # Create a new window for the chart
            chart_window = Toplevel(root)
            chart_window.title("📊 Library Analytics")
            chart_window.geometry("800x600")
            chart_window.config(bg=COLORS['light_bg'])
            
            # Center the chart window
            chart_window.update_idletasks()
            width = 800
            height = 600
            x = (chart_window.winfo_screenwidth() // 2) - (width // 2)
            y = (chart_window.winfo_screenheight() // 2) - (height // 2)
            chart_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Header
            header = Frame(chart_window, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text="📊 LIBRARY ANALYTICS", 
                  bg=COLORS['primary'], fg="white",
                  font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Create figure for pie chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            
            # Pie Chart
            if issued == 0:
                labels = ['Available']
                sizes = [total]
                colors = ['#4ECDC4']
                explode = (0,)
                ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=140)
            else:
                labels = ['Issued', 'Available']
                sizes = [issued, total - issued]
                colors = ['#FF6B6B', '#4ECDC4']
                explode = (0.1, 0)
                ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=140)
            
            ax1.set_title('Book Status Distribution', fontweight='bold')
            ax1.axis('equal')
            
            # Bar Chart for additional stats
            categories = ['Total', 'Issued', 'Available']
            values = [total, issued, total - issued]
            colors_bar = ['#3498DB', '#E74C3C', '#27AE60']
            
            bars = ax2.bar(categories, values, color=colors_bar)
            ax2.set_title('Book Counts', fontweight='bold')
            ax2.set_ylabel('Number of Books')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{value}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            # Embed the chart in Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # Add statistics text
            stats_frame = Frame(chart_window, bg=COLORS['light_bg'])
            stats_frame.pack(fill=X, padx=20, pady=(0, 20))
            
            if issued == 0:
                stats_text = f"📚 All {total} books are available in the library."
            else:
                available = total - issued
                issued_percent = (issued / total) * 100
                available_percent = (available / total) * 100
                stats_text = f"📚 Total: {total} | 📖 Issued: {issued} ({issued_percent:.1f}%) | 📈 Available: {available} ({available_percent:.1f}%)"
            
            Label(stats_frame, text=stats_text, bg=COLORS['light_bg'],
                  font=("Segoe UI", 12, "bold")).pack()
            
            # Close button
            Button(chart_window, text="Close",
                   command=chart_window.destroy,
                   bg=COLORS['accent'],
                   fg="white",
                   font=FONTS['button'],
                   padx=20,
                   pady=8).pack(pady=(0, 20))
            
        except Exception as e:
            # Fallback to text display if chart fails
            print(f"Chart error: {e}")
            if issued == 0:
                message = f"📊 Library Statistics\n\nAll books are available\n\n📚 Total Books: {total}\n📖 Issued Books: 0\n📈 Available: 100%"
            else:
                available = total - issued
                issued_percent = (issued / total) * 100
                available_percent = (available / total) * 100
                
                message = f"""📊 Library Statistics

📚 Total Books: {total}
📖 Issued Books: {issued} ({issued_percent:.1f}%)
📈 Available Books: {available} ({available_percent:.1f}%)

📊 Status Summary:
- Issued: {'█' * int(issued_percent/10)}{'░' * (10 - int(issued_percent/10))} {issued_percent:.1f}%
- Available: {'█' * int(available_percent/10)}{'░' * (10 - int(available_percent/10))} {available_percent:.1f}%"""
            
            mb.showinfo("Library Statistics", message)

    # ================== AI/ML RECOMMENDATION SYSTEM WITH CHATBOT ==================
    class BookRecommender:
        def __init__(self, connector):
            self.conn = connector
            self.cursor = connector.cursor()
            self.load_data()
            self.setup_nltk()
            self.setup_knowledge_base()
            
        def setup_nltk(self):
            """Download required NLTK data"""
            if NLTK_AVAILABLE:
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('stopwords', quiet=True)
                except:
                    print("NLTK download failed, using fallback methods")
        
        def setup_knowledge_base(self):
            """Setup knowledge base for chatbot responses"""
            self.knowledge_base = {
                # Library information
                "library_hours": {
                    "patterns": ["timing", "hours", "open", "close", "time", "schedule"],
                    "response": "📚 Library Hours:\n• Monday-Friday: 9:00 AM - 8:00 PM\n• Saturday: 10:00 AM - 6:00 PM\n• Sunday: 10:00 AM - 4:00 PM\n• Holidays: Closed"
                },
                "library_contact": {
                    "patterns": ["contact", "phone", "email", "address", "location", "reach"],
                    "response": "📞 Library Contact Information:\n• Address: Rajiv Gandhi College Library, College Campus\n• Phone: +91-XXX-XXX-XXXX\n• Email: library@rgcollege.edu\n• Librarian: Dr. S. Sharma"
                },
                "membership": {
                    "patterns": ["membership", "join", "register", "sign up", "card", "id card"],
                    "response": "🎫 Library Membership:\n• Free for all college students\n• Student ID required\n• Can borrow up to 3 books at a time\n• Membership valid for academic year"
                },
                "rules": {
                    "patterns": ["rules", "policy", "regulation", "fine", "penalty", "late"],
                    "response": "📋 Library Rules:\n• Borrowing period: 14 days\n• Fine: ₹5 per day after due date\n• Maximum books: 3 per student\n• Lost books: 2x book price\n• No food/drinks allowed"
                },
                "services": {
                    "patterns": ["service", "facility", "available", "what can i do", "offer"],
                    "response": "🔧 Library Services:\n• Book borrowing\n• Reading room\n• Computer access\n• Printing/Photocopy\n• Reference assistance\n• Book recommendations\n• E-resources access"
                },
                
                # Book-related queries
                "available_books": {
                    "patterns": ["available books", "which books are available", "books in stock", "what books do you have"],
                    "response": "You can check available books by:\n1. Using the search feature\n2. Viewing 'View Books' section\n3. Checking 'View by Course' for subject-specific books\n\nCurrently we have books across: BCA, BSC, B.COM, BA, BBA"
                },
                "popular_books": {
                    "patterns": ["popular books", "best books", "most read", "trending books", "famous books"],
                    "response": "📈 Popular Books in our library:\n• Programming in C by E. Balagurusamy\n• Financial Accounting by S.N. Maheshwari\n• English Literature by William Shakespeare\n• Software Engineering by Roger Pressman\n\nUse 'AI Recommendations' for personalized suggestions!"
                },
                "new_books": {
                    "patterns": ["new books", "recent arrivals", "latest books", "new arrivals"],
                    "response": "📚 New Arrivals (This Month):\n• Python Programming by Mark Lutz\n• Machine Learning by Tom Mitchell\n• Cloud Computing by Rajkumar Buyya\n• Digital Marketing by Philip Kotler\n\nCheck 'View Books' for complete catalog!"
                },
                
                # Help queries
                "help": {
                    "patterns": ["help", "what can you do", "features", "capabilities", "assist"],
                    "response": "🤖 I can help you with:\n\n📚 **Book Information:**\n• Find books by name/author\n• Check availability\n• Get recommendations\n\n📋 **Library Info:**\n• Timings and contact\n• Rules and policies\n• Membership details\n\n🎯 **Assistance:**\n• Answer questions about library\n• Suggest books based on course\n• Help with borrowing process\n\n💡 Just ask me anything about the library!"
                },
                "greeting": {
                    "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "greetings"],
                    "responses": [
                        "Hello! 👋 How can I assist you with the library today?",
                        "Hi there! 📚 What would you like to know about our library?",
                        "Greetings! I'm your library assistant. How can I help?",
                        "Welcome to Rajiv Gandhi College Library! How may I assist you?"
                    ]
                },
                "thanks": {
                    "patterns": ["thanks", "thank you", "appreciate", "grateful"],
                    "responses": [
                        "You're welcome! 😊 Let me know if you need anything else.",
                        "Happy to help! 📚",
                        "Glad I could assist! Don't hesitate to ask if you have more questions.",
                        "Anytime! Feel free to ask if you need more information."
                    ]
                },
                "bye": {
                    "patterns": ["bye", "goodbye", "see you", "exit", "quit"],
                    "responses": [
                        "Goodbye! 👋 Happy reading!",
                        "See you soon! 📚",
                        "Take care! Don't forget to return your books on time!",
                        "Goodbye! Visit the library soon!"
                    ]
                }
            }
        
        def load_data(self):
            # Load borrowing history
            self.cursor.execute("""
                SELECT S.STUDENT_ID, S.CLASS, L.BK_ID, L.BK_NAME, L.AUTHOR_NAME
                FROM Library L
                JOIN Students S ON L.CARD_ID = S.STUDENT_ID
                WHERE L.BK_STATUS = 'Issued'
            """)
            self.borrowing_history = self.cursor.fetchall()
            
            # Load all books
            self.cursor.execute("SELECT BK_ID, BK_NAME, AUTHOR_NAME FROM Library")
            self.all_books = self.cursor.fetchall()
            
            # Create student profiles
            self.student_profiles = defaultdict(set)
            for student_id, student_class, book_id, book_name, author in self.borrowing_history:
                self.student_profiles[student_id].add((book_id, book_name, author))
            
            # Load book database for chatbot
            self.book_database = {}
            for book_id, book_name, author in self.all_books:
                self.book_database[book_id.lower()] = {
                    'name': book_name,
                    'author': author,
                    'id': book_id
                }
        
        def preprocess_text(self, text):
            """Clean and preprocess text for matching"""
            if not NLTK_AVAILABLE:
                # Simple fallback preprocessing
                text = text.lower()
                text = re.sub(r'[^\w\s]', '', text)
                return text.split()
            
            try:
                # Convert to lowercase
                text = text.lower()
                
                # Remove punctuation
                text = re.sub(r'[^\w\s]', '', text)
                
                # Tokenize
                tokens = word_tokenize(text)
                
                # Remove stopwords
                stop_words = set(stopwords.words('english'))
                tokens = [word for word in tokens if word not in stop_words]
                
                return tokens
            except:
                # Fallback
                return text.lower().split()
        
        def calculate_similarity(self, text1, text2):
            """Calculate similarity between two texts"""
            return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        def find_best_match(self, user_input):
            """Find the best matching intent from knowledge base"""
            user_input_lower = user_input.lower()
            best_match = None
            best_score = 0
            
            for intent, data in self.knowledge_base.items():
                patterns = data.get("patterns", []) + data.get("responses", [])
                for pattern in patterns:
                    score = self.calculate_similarity(user_input_lower, pattern)
                    if score > best_score and score > 0.4:  # Threshold for matching
                        best_score = score
                        best_match = intent
            
            return best_match, best_score
        
        def search_book_in_query(self, query):
            """Extract book-related information from query"""
            query_lower = query.lower()
            
            # Check for specific book IDs
            book_id_pattern = r'book\s*(id\s*)?(\w+\d+\w*)'
            match = re.search(book_id_pattern, query_lower)
            if match:
                book_id = match.group(2)
                if book_id.lower() in self.book_database:
                    return self.book_database[book_id.lower()]
            
            # Check for book names
            for book_id, book_info in self.book_database.items():
                book_name_lower = book_info['name'].lower()
                author_lower = book_info['author'].lower()
                
                # Check if book name or author is mentioned in query
                if book_name_lower in query_lower or \
                   any(word in query_lower for word in book_name_lower.split() if len(word) > 3):
                    return book_info
                
                if author_lower in query_lower or \
                   any(word in query_lower for word in author_lower.split() if len(word) > 3):
                    return book_info
            
            return None
        
        def get_book_status(self, book_id):
            """Get current status of a book"""
            try:
                self.cursor.execute("""
                    SELECT BK_STATUS, QUANTITY, CARD_ID, DUE_DATE 
                    FROM Library 
                    WHERE BK_ID = ? OR UPPER(BK_NAME) LIKE UPPER(?)
                """, (book_id, f"%{book_id}%"))
                result = self.cursor.fetchone()
                
                if result:
                    status, quantity, card_id, due_date = result
                    if status == "Available":
                        return f"✅ Available (10 copies in stock - Fixed quantity)"
                    else:
                        # Get issue date
                        issue_date = get_issue_date(book_id, card_id)
                        return f"📖 Currently Issued\n• Borrower ID: {card_id}\n• Issue Date: {issue_date}\n• Due Date: {due_date}\n• Return to make available"
                return "❌ Book not found in database"
            except:
                return "⚠️ Could not fetch book status"
        
        def process_query(self, user_input):
            """Process user query and generate response"""
            if not user_input or not user_input.strip():
                return "🤔 Please ask a question about books or library services."
            
            user_input = user_input.strip()
            
            # Check for book-specific queries
            book_info = self.search_book_in_query(user_input)
            if book_info:
                # Get book status
                status = self.get_book_status(book_info['id'])
                
                response = f"📚 **Book Information:**\n"
                response += f"• **Title:** {book_info['name']}\n"
                response += f"• **Author:** {book_info['author']}\n"
                response += f"• **Book ID:** {book_info['id']}\n"
                response += f"• **Status:** {status}\n\n"
                
                # Add related books
                self.cursor.execute("""
                    SELECT BK_NAME, AUTHOR_NAME, BK_STATUS 
                    FROM Library 
                    WHERE AUTHOR_NAME LIKE ? AND BK_ID != ?
                    LIMIT 3
                """, (f"%{book_info['author'].split()[0]}%", book_info['id']))
                
                related_books = self.cursor.fetchall()
                if related_books:
                    response += "📖 **Related Books by Same Author:**\n"
                    for book in related_books:
                        status_icon = "✅" if book[2] == "Available" else "📖"
                        response += f"• {status_icon} {book[0]} by {book[1]}\n"
                
                return response
            
            # Check for specific intents in knowledge base
            intent, score = self.find_best_match(user_input)
            
            if intent:
                data = self.knowledge_base[intent]
                
                if "responses" in data:  # For greetings, thanks, etc.
                    return random.choice(data["responses"])
                elif "response" in data:  # For informational responses
                    return data["response"]
            
            # Check for course-based queries
            course_keywords = {
                'bca': 'BCA',
                'bsc': 'BSC', 
                'bcom': 'B.COM',
                'ba': 'BA',
                'bba': 'BBA',
                'computer': 'BCA',
                'science': 'BSC',
                'commerce': 'B.COM',
                'arts': 'BA',
                'business': 'BBA'
            }
            
            for keyword, course in course_keywords.items():
                if keyword in user_input.lower():
                    # Count books for this course
                    self.cursor.execute("SELECT COUNT(*) FROM Library WHERE UPPER(BK_NAME) LIKE UPPER(?)", 
                                      (f"%{course}%",))
                    count = self.cursor.fetchone()[0]
                    
                    return f"📚 **{course} Course Books:**\n• We have {count} books for {course} course\n• Each book has 10 fixed copies\n• Use 'View by Course' feature to see all books\n• Check 'AI Recommendations' for personalized suggestions"
            
            # Check for availability queries
            if any(word in user_input.lower() for word in ['available', 'in stock', 'have you got', 'do you have']):
                return "📚 To check book availability:\n1. Use the search bar above\n2. Enter book name or author\n3. Check status in the table\n\nNote: All books have 10 fixed copies. Quantity doesn't change when issued/returned."
            
            # Check for borrowing queries
            if any(word in user_input.lower() for word in ['borrow', 'issue', 'lend', 'take book', 'get book']):
                return "📖 **How to borrow a book:**\n1. Search for the book\n2. Select it from the table\n3. Click 'Issue Book'\n4. Enter student ID\n\n📌 **Note:** Book quantity is fixed at 10 copies. It doesn't decrease when issued."
            
            # Check for return queries
            if any(word in user_input.lower() for word in ['return', 'give back', 'submit']):
                return "📚 **Book Return Process:**\n1. Select the issued book from 'View Books'\n2. Click 'Return Book'\n3. System will update status automatically\n4. Any fines will be calculated\n\n⚠️ Late returns incur ₹5 per day fine\nNote: Book quantity remains at 10 copies (fixed)."
            
            # Check for fine queries
            if any(word in user_input.lower() for word in ['fine', 'penalty', 'late fee', 'charge']):
                self.cursor.execute("SELECT SUM(FINE_PER_DAY) FROM Library WHERE BK_STATUS='Issued'")
                total_fines = self.cursor.fetchone()[0] or 0
                
                return f"💰 **Fine Information:**\n• Late return fine: ₹5 per day\n• Current pending fines in system: ₹{total_fines}\n• Pay fines via 'Pay Fine' button\n• Check 'View Books' for individual book fines"
            
            # Default response for unknown queries
            suggestions = [
                "Try asking about:\n• Library timings and contact\n• Book availability\n• Borrowing rules\n• Course-specific books\n• New arrivals",
                "I can help with:\n• Finding books\n• Library information\n• Borrowing process\n• Book recommendations\n• Fine details",
                "Need help? Try:\n• 'What are the library hours?'\n• 'How do I borrow a book?'\n• 'Show me BCA books'\n• 'What is the fine for late return?'"
            ]
            
            return f"🤔 I'm not sure I understand that question about the library.\n\n💡 {random.choice(suggestions)}\n\nOr type 'help' to see what I can do!"
        
        def collaborative_filtering(self, student_id, top_n=5):
            """
            Collaborative filtering based on similar students
            """
            if not self.borrowing_history:
                return self.popular_books(top_n)
            
            if student_id not in self.student_profiles:
                return self.course_based_recommendations(student_id, top_n)
            
            # Find similar students (same class or similar borrowing patterns)
            target_books = self.student_profiles[student_id]
            
            # Get student's class
            self.cursor.execute("SELECT CLASS FROM Students WHERE STUDENT_ID=?", (student_id,))
            student_class_result = self.cursor.fetchone()
            student_class = student_class_result[0] if student_class_result else None
            
            # Find similar students
            similar_students = []
            for sid, books in self.student_profiles.items():
                if sid == student_id:
                    continue
                
                # Check if same class for better recommendations
                self.cursor.execute("SELECT CLASS FROM Students WHERE STUDENT_ID=?", (sid,))
                other_class_result = self.cursor.fetchone()
                other_class = other_class_result[0] if other_class_result else None
                
                similarity = len(books.intersection(target_books))
                if student_class and other_class and student_class == other_class:
                    similarity *= 2  # Weight higher for same class
                
                if similarity > 0:
                    similar_students.append((sid, similarity, books))
            
            # Sort by similarity
            similar_students.sort(key=lambda x: x[1], reverse=True)
            
            # Get books from similar students that target student hasn't borrowed
            recommended_books = set()
            for sid, similarity, books in similar_students[:3]:  # Top 3 similar students
                for book in books:
                    if book not in target_books:
                        recommended_books.add(book)
            
            # If not enough recommendations, add popular books
            if len(recommended_books) < top_n:
                recommended_books.update(self.popular_books(top_n - len(recommended_books)))
            
            return list(recommended_books)[:top_n]
        
        def course_based_recommendations(self, student_id, top_n=5):
            """
            Recommend books based on student's course/year
            """
            self.cursor.execute("SELECT CLASS FROM Students WHERE STUDENT_ID=?", (student_id,))
            result = self.cursor.fetchone()
            
            if not result:
                return self.popular_books(top_n)
            
            student_class = result[0]
            
            # Extract course and year from class (e.g., "BCA 3rd Year")
            course_keywords = {
                'BCA': ['computer', 'programming', 'software', 'database'],
                'BSC': ['science', 'math', 'physics', 'chemistry'],
                'B.COM': ['commerce', 'accounting', 'finance', 'business'],
                'BA': ['arts', 'history', 'literature', 'psychology'],
                'BBA': ['business', 'management', 'marketing', 'finance']
            }
            
            # Find matching keywords
            recommended = []
            for book_id, book_name, author in self.all_books:
                book_lower = book_name.lower()
                for keyword in student_class.upper().split():
                    if keyword in course_keywords:
                        for course_word in course_keywords[keyword]:
                            if course_word in book_lower:
                                recommended.append((book_id, book_name, author))
                                break
            
            # If still not enough, add popular books
            if len(recommended) < top_n:
                recommended.extend(self.popular_books(top_n - len(recommended)))
            
            return recommended[:top_n]
        
        def popular_books(self, top_n=5):
            """
            Recommend most frequently borrowed books
            """
            # Count book borrowings
            book_counts = defaultdict(int)
            for _, _, book_id, _, _ in self.borrowing_history:
                book_counts[book_id] += 1
            
            # Sort by popularity
            popular_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Get book details
            recommendations = []
            for book_id, count in popular_books[:top_n]:
                self.cursor.execute("SELECT BK_ID, BK_NAME, AUTHOR_NAME FROM Library WHERE BK_ID=?", (book_id,))
                book = self.cursor.fetchone()
                if book:
                    recommendations.append(book)
            
            return recommendations
        
        def trending_books(self, days=30, top_n=5):
            """
            Recommend recently popular books
            """
            recent_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            self.cursor.execute("""
                SELECT L.BK_ID, COUNT(*) as recent_borrows
                FROM Library L
                WHERE L.BK_STATUS = 'Issued' 
                AND L.DUE_DATE > ?
                GROUP BY L.BK_ID
                ORDER BY recent_borrows DESC
                LIMIT ?
            """, (recent_date, top_n))
            
            trending = self.cursor.fetchall()
            
            recommendations = []
            for book_id, count in trending:
                self.cursor.execute("SELECT BK_ID, BK_NAME, AUTHOR_NAME FROM Library WHERE BK_ID=?", (book_id,))
                book = self.cursor.fetchone()
                if book:
                    recommendations.append(book)
            
            return recommendations
        
        def get_recommendations(self, student_id, method='hybrid', top_n=5):
            """
            Get recommendations using specified method
            """
            if method == 'collaborative':
                return self.collaborative_filtering(student_id, top_n)
            elif method == 'course':
                return self.course_based_recommendations(student_id, top_n)
            elif method == 'popular':
                return self.popular_books(top_n)
            elif method == 'trending':
                return self.trending_books(top_n=top_n)
            else:  # hybrid approach
                all_recs = []
                all_recs.extend(self.collaborative_filtering(student_id, top_n))
                all_recs.extend(self.course_based_recommendations(student_id, top_n))
                all_recs.extend(self.trending_books(top_n=top_n))
                
                # Remove duplicates while preserving order
                seen = set()
                unique_recs = []
                for rec in all_recs:
                    if rec not in seen:
                        seen.add(rec)
                        unique_recs.append(rec)
                
                return unique_recs[:top_n]

    def show_ai_recommendations():
        win = Toplevel(root)
        win.title("🤖 AI Book Recommendations")
        win.geometry("800x600")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 800
        height = 600
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="🤖 AI BOOK RECOMMENDATIONS", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        # Student selection frame
        selection_frame = Frame(win, bg=COLORS['light_bg'], padx=20, pady=15)
        selection_frame.pack(fill=X)
        
        Label(selection_frame, text="Select Student:", bg=COLORS['light_bg'],
              font=FONTS['subheading']).pack(side=LEFT, padx=(0, 10))
        
        student_var = StringVar()
        cursor.execute("SELECT STUDENT_ID, NAME FROM Students")
        students = cursor.fetchall()
        student_options = ["Select Student"] + [f"{sid} - {name}" for sid, name in students]
        student_menu = ttk.Combobox(selection_frame, textvariable=student_var, 
                                   values=student_options, state="readonly", width=30,
                                   font=FONTS['body'])
        student_menu.pack(side=LEFT, padx=(0, 20))
        
        # Recommendation method
        Label(selection_frame, text="Method:", bg=COLORS['light_bg'],
              font=FONTS['subheading']).pack(side=LEFT, padx=(0, 10))
        
        method_var = StringVar(value="Hybrid")
        method_menu = ttk.Combobox(selection_frame, textvariable=method_var, 
                                   values=["Hybrid", "Collaborative Filtering", "Course-Based", 
                                          "Popular", "Trending"], state="readonly", width=20,
                                   font=FONTS['body'])
        method_menu.pack(side=LEFT)
        
        # Generate button
        def generate_recommendations():
            student_info = student_var.get()
            if student_info == "Select Student":
                mb.showerror("Error", "Please select a student")
                return
            
            student_id = student_info.split(" - ")[0]
            method_map = {
                "Hybrid": "hybrid",
                "Collaborative Filtering": "collaborative",
                "Course-Based": "course",
                "Popular": "popular",
                "Trending": "trending"
            }
            
            method = method_map[method_var.get()]
            
            # Initialize recommender
            recommender = BookRecommender(connector)
            
            try:
                recommendations = recommender.get_recommendations(student_id, method=method, top_n=10)
                
                # Clear previous recommendations
                for widget in results_frame.winfo_children():
                    widget.destroy()
                
                if not recommendations:
                    Label(results_frame, text="⚠️ No recommendations available. Try different method.",
                          bg=COLORS['card_bg'], font=FONTS['body'], fg=COLORS['warning']).pack(pady=50)
                    return
                
                # Display recommendations
                Label(results_frame, text=f"📚 Recommended Books for {student_info.split(' - ')[1]}:",
                      bg=COLORS['card_bg'], font=FONTS['subheading'], fg=COLORS['primary']).pack(pady=(0, 20))
                
                for i, (book_id, book_name, author) in enumerate(recommendations, 1):
                    rec_frame = Frame(results_frame, bg=COLORS['light_bg'], relief="flat", bd=1,
                                     highlightbackground="#DDDDDD", highlightthickness=1)
                    rec_frame.pack(fill=X, pady=5, padx=5)
                    
                    # Number badge
                    Label(rec_frame, text=str(i), bg=COLORS['secondary'], fg="white",
                          font=("Segoe UI", 10, "bold"), width=3).pack(side=LEFT, padx=(10, 15), pady=10)
                    
                    # Book info
                    info_frame = Frame(rec_frame, bg=COLORS['light_bg'])
                    info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
                    
                    Label(info_frame, text=book_name, bg=COLORS['light_bg'],
                          font=("Segoe UI", 10, "bold"), anchor="w").pack(anchor="w")
                    
                    Label(info_frame, text=f"Author: {author} | ID: {book_id}", 
                          bg=COLORS['light_bg'], font=("Segoe UI", 9), anchor="w").pack(anchor="w")
                    
                    # Action buttons
                    btn_frame = Frame(rec_frame, bg=COLORS['light_bg'])
                    btn_frame.pack(side=RIGHT, padx=10)
                    
                    Button(btn_frame, text="📖 Issue", 
                           command=lambda bid=book_id: quick_issue_book(bid, student_id),
                           bg=COLORS['success'],
                           fg="white",
                           font=("Segoe UI", 9),
                           padx=10,
                           pady=2).pack(pady=2)
                    
                    Button(btn_frame, text="➕ Add to List", 
                           command=lambda bid=book_id, bname=book_name: add_to_wishlist(student_id, bid, bname),
                           bg=COLORS['secondary'],
                           fg="white",
                           font=("Segoe UI", 9),
                           padx=10,
                           pady=2).pack(pady=2)
                
            except Exception as e:
                mb.showerror("Error", f"Failed to generate recommendations: {e}")
        
        def quick_issue_book(book_id, student_id):
            try:
                # Check if book exists (don't check quantity since it's always 10)
                cursor.execute("SELECT BK_NAME FROM Library WHERE BK_ID=?", (book_id,))
                result = cursor.fetchone()
                
                if not result:
                    mb.showerror("Error", "Book not found")
                    return False
                
                book_name = result[0]
                
                # Check if student exists
                cursor.execute("SELECT * FROM Students WHERE STUDENT_ID=?", (student_id,))
                if not cursor.fetchone():
                    mb.showerror("Error", "Student not found")
                    return False
                
                # Issue book (don't change quantity)
                due = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                
                cursor.execute("""
                    UPDATE Library 
                    SET BK_STATUS='Issued', CARD_ID=?, DUE_DATE=? 
                    WHERE BK_ID=?
                """, (student_id, due, book_id))
                
                connector.commit()
                
                # Send email notification
                send_issue_email(student_id, book_name, book_id, due)
                
                mb.showinfo("Success", f"✅ Book '{book_name}' issued successfully! (Stock remains at 10)")
                
                # Refresh views
                if 'tree' in globals() and tree.winfo_exists():
                    display_records(search_var.get())
                update_status()
                
                return True
                
            except Exception as e:
                mb.showerror("Error", f"Failed to issue book: {e}")
                return False
        
        def add_to_wishlist(student_id, book_id, book_name):
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO Wishlist VALUES (?,?,?,?)
                """, (student_id, book_id, book_name, datetime.now().strftime("%Y-%m-%d")))
                
                connector.commit()
                mb.showinfo("Success", f"✅ '{book_name}' added to wishlist!")
            except Exception as e:
                mb.showerror("Error", f"Failed to add to wishlist: {e}")
        
        Button(selection_frame, text="🤖 Generate Recommendations", 
               command=generate_recommendations,
               bg="#9B59B6",
               fg="white",
               font=FONTS['button'],
               padx=15,
               pady=8).pack(side=LEFT, padx=(20, 0))
        
        # Results frame
        results_container = Frame(win, bg=COLORS['light_bg'])
        results_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Scrollable results
        results_canvas = Canvas(results_container, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = Scrollbar(results_container, orient="vertical", command=results_canvas.yview)
        scrollable_frame = Frame(results_canvas, bg=COLORS['card_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=RIGHT, fill=Y)
        results_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Safe mousewheel binding with error handling
        def on_mousewheel(event):
            try:
                # Handle different event types for cross-platform compatibility
                if hasattr(event, 'delta'):
                    # Windows/MacOS
                    scroll_amount = int(-1 * (event.delta / 120))
                elif event.num == 4:
                    # Linux scroll up
                    scroll_amount = -1
                elif event.num == 5:
                    # Linux scroll down
                    scroll_amount = 1
                else:
                    return
                
                results_canvas.yview_scroll(scroll_amount, "units")
            except Exception:
                # Ignore mousewheel errors if widget is destroyed
                pass
        
        # Bind mousewheel events with error handling
        try:
            results_canvas.bind_all("<MouseWheel>", on_mousewheel)
            results_canvas.bind_all("<Button-4>", on_mousewheel)
            results_canvas.bind_all("<Button-5>", on_mousewheel)
        except:
            pass
        
        global results_frame
        results_frame = scrollable_frame
        
        # Add placeholder text
        Label(results_frame, text="🎯 Select a student and click 'Generate Recommendations' to see AI-powered suggestions.",
              bg=COLORS['card_bg'], font=FONTS['body'], fg="#7F8C8D").pack(pady=50)

    # ================== LIBRARY CHATBOT FEATURE ==================
    def show_library_chatbot():
        """Show AI-powered library chatbot interface"""
        win = Toplevel(root)
        win.title("🤖 Library Assistant Chatbot")
        win.geometry("700x600")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 700
        height = 600
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="🤖 LIBRARY ASSISTANT CHATBOT", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        # Subtitle
        subtitle = Frame(win, bg=COLORS['light_bg'], height=40)
        subtitle.pack(fill=X)
        subtitle.pack_propagate(False)
        
        Label(subtitle, 
              text="Ask me anything about books, library services, or borrowing process!",
              bg=COLORS['light_bg'], font=("Segoe UI", 10), fg="#7F8C8D").pack(expand=True, pady=10)
        
        # Main chat container
        main_chat_container = Frame(win, bg=COLORS['card_bg'])
        main_chat_container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Create a frame for chat display with scrollbar
        chat_display_frame = Frame(main_chat_container, bg=COLORS['card_bg'])
        chat_display_frame.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Create Canvas and Scrollbar for chat
        chat_canvas = Canvas(chat_display_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = Scrollbar(chat_display_frame, orient="vertical", command=chat_canvas.yview)
        
        # Create scrollable frame
        chat_frame = Frame(chat_canvas, bg=COLORS['card_bg'])
        
        # Configure the canvas
        chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=RIGHT, fill=Y)
        chat_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Add the chat frame to the canvas
        chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw", width=chat_canvas.winfo_reqwidth())
        
        # Configure scrolling
        def configure_scroll_region(event):
            chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
            # Auto-scroll to bottom
            chat_canvas.yview_moveto(1.0)
        
        chat_frame.bind("<Configure>", configure_scroll_region)
        
        # Input frame (at the bottom)
        input_frame = Frame(main_chat_container, bg=COLORS['card_bg'])
        input_frame.pack(fill=X, pady=(10, 0))
        
        # Create chat history list
        chat_history = []
        
        def add_message(sender, message, is_bot=False):
            """Add a message to the chat"""
            message_container = Frame(chat_frame, bg=COLORS['card_bg'])
            message_container.pack(fill=X, padx=10, pady=5, anchor="w" if is_bot else "e")
            
            # Main message frame
            msg_frame = Frame(message_container, bg=COLORS['card_bg'])
            msg_frame.pack(side=LEFT if is_bot else RIGHT, padx=5)
            
            # Avatar
            avatar_frame = Frame(msg_frame, bg=COLORS['card_bg'])
            avatar_frame.pack(side=LEFT, padx=(0, 10))
            
            if is_bot:
                avatar = Label(avatar_frame, text="🤖", bg=COLORS['card_bg'], 
                              font=("Segoe UI", 20))
                bubble_color = "#E3F2FD"
                text_color = COLORS['primary']
            else:
                avatar = Label(avatar_frame, text="👤", bg=COLORS['card_bg'], 
                              font=("Segoe UI", 20))
                bubble_color = "#E8F5E9"
                text_color = "#2E7D32"
            
            avatar.pack()
            
            # Message bubble
            bubble_frame = Frame(msg_frame, bg=bubble_color, relief="flat", 
                                bd=1, highlightbackground="#DDDDDD", highlightthickness=1)
            bubble_frame.pack(side=LEFT, fill=BOTH, expand=True)
            
            # Message text with word wrapping
            message_text = Text(bubble_frame, height=1, width=40, wrap=WORD, bg=bubble_color, 
                               fg=text_color, font=("Segoe UI", 10), relief="flat", 
                               bd=0, padx=15, pady=10)
            message_text.insert(END, message)
            message_text.config(state=DISABLED)  # Make it read-only
            message_text.pack(fill=BOTH, expand=True)
            
            # Adjust text widget height based on content
            lines = len(message.split('\n')) + sum([len(line) // 40 for line in message.split('\n')])
            message_text.config(height=min(max(lines, 1), 10))
            
            # Timestamp
            timestamp_frame = Frame(message_container, bg=COLORS['card_bg'])
            timestamp_frame.pack(side=LEFT if is_bot else RIGHT, padx=5)
            
            timestamp = datetime.now().strftime("%H:%M")
            time_label = Label(timestamp_frame, text=timestamp, bg=COLORS['card_bg'],
                              font=("Segoe UI", 8), fg="#95A5A6")
            time_label.pack(pady=5)
            
            # Store in history
            chat_history.append({
                'sender': sender,
                'message': message,
                'is_bot': is_bot,
                'timestamp': timestamp
            })
            
            # Update scroll region
            chat_frame.update_idletasks()
            chat_canvas.config(scrollregion=chat_canvas.bbox("all"))
            chat_canvas.yview_moveto(1.0)
        
        # Initialize chatbot
        chatbot = BookRecommender(connector)
        
        # Add welcome message
        welcome_msg = """Hello! I'm your Library Assistant. 🤖

I can help you with:
• 📚 Finding books and checking availability
• 📋 Library information and rules
• 🎓 Course-specific book suggestions
• ⏰ Library timings and contact details
• 💰 Fine and borrowing information

Note: All books have 10 fixed copies. Quantity doesn't change when issued/returned.

What would you like to know?"""
        
        add_message("Bot", welcome_msg, is_bot=True)
        
        # Input field and send button
        input_var = StringVar()
        
        # Create input frame with border
        input_entry_frame = Frame(input_frame, bg="#DDDDDD", relief="solid", bd=1)
        input_entry_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        input_entry = Entry(input_entry_frame, textvariable=input_var, 
                           font=FONTS['body'], bg="white", fg=COLORS['primary'],
                           relief="flat", bd=0)
        input_entry.pack(fill=BOTH, expand=True, padx=10, pady=10)
        input_entry.focus_set()
        
        def send_message():
            """Send user message and get bot response"""
            message = input_var.get().strip()
            if not message:
                return
            
            # Add user message
            add_message("You", message, is_bot=False)
            
            # Clear input
            input_var.set("")
            
            # Get bot response
            response = chatbot.process_query(message)
            
            # Add bot response after a short delay (simulate thinking)
            win.after(500, lambda: add_message("Bot", response, is_bot=True))
        
        # Send button
        send_btn = Button(input_frame, text="Send",
                         command=send_message,
                         bg=COLORS['secondary'],
                         fg="white",
                         font=FONTS['button'],
                         padx=25,
                         pady=10,
                         relief="flat",
                         cursor="hand2")
        send_btn.pack(side=LEFT)
        
        # Quick suggestions frame
        suggestions_frame = Frame(win, bg=COLORS['light_bg'])
        suggestions_frame.pack(fill=X, padx=20, pady=(0, 10))
        
        Label(suggestions_frame, text="💡 Quick questions:", 
              bg=COLORS['light_bg'], font=("Segoe UI", 9)).pack(anchor=W, pady=(0, 5))
        
        quick_questions = [
            "Library hours?",
            "How to borrow?",
            "BCA books?",
            "Late fine?",
            "New books?"
        ]
        
        q_frame = Frame(suggestions_frame, bg=COLORS['light_bg'])
        q_frame.pack(fill=X, pady=5)
        
        for question in quick_questions:
            btn = Button(q_frame, text=question,
                        command=lambda q=question: [input_var.set(q), send_message()],
                        bg=COLORS['light_bg'],
                        fg=COLORS['primary'],
                        font=("Segoe UI", 9),
                        relief="flat",
                        cursor="hand2",
                        padx=10,
                        pady=5)
            btn.pack(side=LEFT, padx=2)
            
            # Add hover effect
            def on_enter(e, btn=btn):
                btn['bg'] = COLORS['secondary']
                btn['fg'] = "white"
            
            def on_leave(e, btn=btn):
                btn['bg'] = COLORS['light_bg']
                btn['fg'] = COLORS['primary']
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Function to save chat history
        def save_chat_history():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")],
                initialfile=f"Chat_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("LIBRARY CHATBOT HISTORY\n")
                        f.write("=" * 50 + "\n\n")
                        
                        for entry in chat_history:
                            sender = "Bot" if entry['is_bot'] else "You"
                            f.write(f"[{entry['timestamp']}] {sender}: {entry['message']}\n\n")
                        
                        f.write("\n" + "=" * 50 + "\n")
                        f.write(f"End of conversation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    mb.showinfo("Success", f"✅ Chat history saved to:\n{file_path}")
                except Exception as e:
                    mb.showerror("Error", f"Failed to save chat history: {e}")
        
        # Example queries button
        def show_example_queries():
            examples_win = Toplevel(win)
            examples_win.title("💡 Chatbot Examples")
            examples_win.geometry("500x400")
            examples_win.config(bg=COLORS['light_bg'])
            
            examples_win.update_idletasks()
            width = 500
            height = 400
            x = (examples_win.winfo_screenwidth() // 2) - (width // 2)
            y = (examples_win.winfo_screenheight() // 2) - (height // 2)
            examples_win.geometry(f'{width}x{height}+{x}+{y}')
            
            # Header
            header = Frame(examples_win, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text="💡 CHATBOT EXAMPLE QUERIES", 
                  bg=COLORS['primary'], fg="white",
                  font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Create scrollable content
            container = Frame(examples_win, bg=COLORS['light_bg'])
            container.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            canvas = Canvas(container, bg=COLORS['light_bg'], highlightthickness=0)
            scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg=COLORS['light_bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side=RIGHT, fill=Y)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            
            # Example categories
            categories = {
                "📚 Book Information": [
                    "Do you have Programming in C book?",
                    "Is Introduction to Computers available?",
                    "Find books by E. Balagurusamy",
                    "What is the status of book BCA101?",
                    "Show me books about Python programming"
                ],
                "🏫 Library Information": [
                    "What are the library hours?",
                    "Library contact information",
                    "Library rules and policies",
                    "How do I get library membership?",
                    "What services does the library offer?"
                ],
                "🎓 Course-based Queries": [
                    "Show me BCA course books",
                    "What books are available for BSC?",
                    "Books for 3rd year B.COM",
                    "Computer science books",
                    "Commerce department books"
                ],
                "📖 Borrowing Process": [
                    "How do I borrow a book?",
                    "What is the borrowing period?",
                    "How many books can I borrow?",
                    "How to return a book?",
                    "What if I lose a book?"
                ],
                "💰 Fines and Fees": [
                    "What is the fine for late return?",
                    "How much is the library membership fee?",
                    "How to pay fines?",
                    "What happens if I don't return books?"
                ],
                "🔍 General Help": [
                    "Help me find a book",
                    "What can you do?",
                    "New book arrivals",
                    "Most popular books",
                    "Book recommendations"
                ]
            }
            
            row = 0
            for category, queries in categories.items():
                # Category label
                cat_frame = Frame(scrollable_frame, bg=COLORS['card_bg'], relief="flat", bd=1,
                                 highlightbackground="#DDDDDD", highlightthickness=1)
                cat_frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
                cat_frame.grid_columnconfigure(0, weight=1)
                
                Label(cat_frame, text=category, bg=COLORS['card_bg'],
                      font=("Segoe UI", 11, "bold"), fg=COLORS['primary']).pack(pady=10)
                
                row += 1
                
                # Queries
                for query in queries:
                    query_frame = Frame(scrollable_frame, bg=COLORS['light_bg'])
                    query_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=20)
                    
                    # Clickable query
                    def create_query_click(q=query):
                        def query_click():
                            examples_win.destroy()
                            input_var.set(q)
                            send_message()
                        return query_click
                    
                    query_btn = Button(query_frame, text=f"• {query}",
                                      command=create_query_click(query),
                                      bg=COLORS['light_bg'],
                                      fg="#2C3E50",
                                      font=("Segoe UI", 9),
                                      anchor="w",
                                      relief="flat",
                                      cursor="hand2")
                    query_btn.pack(fill=X, padx=10, pady=3)
                    
                    # Hover effect
                    def on_enter(e, btn=query_btn):
                        btn['bg'] = COLORS['secondary']
                        btn['fg'] = "white"
                    
                    def on_leave(e, btn=query_btn):
                        btn['bg'] = COLORS['light_bg']
                        btn['fg'] = "#2C3E50"
                    
                    query_btn.bind("<Enter>", on_enter)
                    query_btn.bind("<Leave>", on_leave)
                    
                    row += 1
            
            # Update scroll region
            scrollable_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
            # Close button
            Button(examples_win, text="Close",
                   command=examples_win.destroy,
                   bg="#95A5A6",
                   fg="white",
                   font=FONTS['button'],
                   padx=20,
                   pady=8).pack(pady=10)
        
        # Bottom buttons frame
        bottom_buttons_frame = Frame(win, bg=COLORS['light_bg'])
        bottom_buttons_frame.pack(fill=X, padx=20, pady=(0, 10))
        
        # Example queries button
        example_btn = Button(bottom_buttons_frame, text="💡 Example Queries",
                            command=show_example_queries,
                            bg=COLORS['warning'],
                            fg="white",
                            font=FONTS['button'],
                            padx=15,
                            pady=8)
        example_btn.pack(side=LEFT, padx=(0, 10))
        
        # Save chat button
        save_btn = Button(bottom_buttons_frame, text="💾 Save Chat",
                         command=save_chat_history,
                         bg="#95A5A6",
                         fg="white",
                         font=FONTS['button'],
                         padx=15,
                         pady=8)
        save_btn.pack(side=LEFT)
        
        # Bind Enter key to send
        input_entry.bind('<Return>', lambda e: send_message())

    # ================== WEB PORTAL INTEGRATION ==================
    def setup_web_portal_files():
        # Create directories if they don't exist
        os.makedirs('templates', exist_ok=True)
        os.makedirs('static/css', exist_ok=True)
        os.makedirs('static/js', exist_ok=True)
        
        # Create HTML template
        index_html = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Library Management Portal</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body { background-color: #f8f9fa; }
            .navbar { background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%); }
            .card { border: none; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .btn-primary { background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%); border: none; }
            .search-box { max-width: 500px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <i class="fas fa-book"></i> Library Portal
                </a>
                <div class="navbar-text text-light">
                    Rajiv Gandhi College Library
                </div>
            </div>
        </nav>

        <!-- Main Container -->
        <div class="container mt-4">
            <!-- Search Bar -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="input-group search-box">
                        <input type="text" id="searchInput" class="form-control" 
                               placeholder="Search books by name or author...">
                        <button class="btn btn-primary" onclick="searchBooks()">
                            <i class="fas fa-search"></i> Search
                        </button>
                    </div>
                </div>
            </div>

            <!-- Statistics Cards -->
            <div class="row mb-4" id="statsSection">
                <div class="col-md-3 mb-3">
                    <div class="card stat-card p-3">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 id="totalBooks">0</h3>
                                <p class="mb-0">Total Books</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-book fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card p-3">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 id="issuedBooks">0</h3>
                                <p class="mb-0">Issued Books</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-book-reader fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card p-3">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 id="totalStudents">0</h3>
                                <p class="mb-0">Students</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-users fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card p-3">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h3 id="pendingFines">₹0</h3>
                                <p class="mb-0">Pending Fines</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-rupee-sign fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Books Section -->
            <div class="row">
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0"><i class="fas fa-books"></i> Book Collection</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Book Name</th>
                                            <th>Author</th>
                                            <th>Status</th>
                                            <th>Issue Date</th>
                                            <th>Due Date</th>
                                            <th>Quantity</th>
                                            <th>Issued Count</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="booksTable">
                                        <!-- Books will be loaded here -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Issue Book Form -->
                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0"><i class="fas fa-handshake"></i> Issue Book</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">Student ID</label>
                                <input type="text" id="studentId" class="form-control" placeholder="Enter student ID">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Book ID</label>
                                <input type="text" id="bookId" class="form-control" placeholder="Enter book ID">
                            </div>
                            <button class="btn btn-success w-100" onclick="issueBook()">
                                <i class="fas fa-paper-plane"></i> Issue Book
                            </button>
                        </div>
                    </div>

                    <!-- Students List -->
                    <div class="card mt-3">
                        <div class="card-header bg-info text-white">
                            <h5 class="mb-0"><i class="fas fa-user-graduate"></i> Recent Students</h5>
                        </div>
                        <div class="card-body">
                            <div id="studentsList">
                                <!-- Students will be loaded here -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- JavaScript -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Load statistics on page load
            document.addEventListener('DOMContentLoaded', function() {
                loadStatistics();
                loadBooks();
                loadStudents();
            });

            async function loadStatistics() {
                try {
                    const response = await fetch('/api/statistics');
                    const data = await response.json();
                    
                    if (data.success) {
                        const stats = data.statistics;
                        document.getElementById('totalBooks').textContent = stats.total_books;
                        document.getElementById('issuedBooks').textContent = stats.issued_books;
                        document.getElementById('totalStudents').textContent = stats.total_students;
                        document.getElementById('pendingFines').textContent = '₹' + stats.pending_fines;
                    }
                } catch (error) {
                    console.error('Error loading statistics:', error);
                }
            }

            async function loadBooks() {
                try {
                    const response = await fetch('/api/books');
                    const data = await response.json();
                    
                    if (data.success) {
                        const booksTable = document.getElementById('booksTable');
                        booksTable.innerHTML = '';
                        
                        data.books.forEach(book => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${book.name}</td>
                                <td>${book.author}</td>
                                <td>
                                    <span class="badge ${book.status === 'Available' ? 'bg-success' : 'bg-danger'}">
                                        ${book.status}
                                    </span>
                                </td>
                                <td>${book.issue_date}</td>
                                <td>${book.due_date}</td>
                                <td>${book.quantity} (Fixed)</td>
                                <td>
                                    <span class="badge ${book.issued_count > 0 ? 'bg-warning' : 'bg-secondary'}">
                                        ${book.issued_count} issued
                                    </span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-primary" onclick="selectBook('${book.id}')">
                                        <i class="fas fa-hand-pointer"></i> Select
                                    </button>
                                </td>
                            `;
                            booksTable.appendChild(row);
                        });
                    }
                } catch (error) {
                    console.error('Error loading books:', error);
                }
            }

            async function loadStudents() {
                try {
                    const response = await fetch('/api/students');
                    const data = await response.json();
                    
                    if (data.success) {
                        const studentsList = document.getElementById('studentsList');
                        studentsList.innerHTML = '';
                        
                        // Show only 5 recent students
                        data.students.slice(0, 5).forEach(student => {
                            const studentDiv = document.createElement('div');
                            studentDiv.className = 'mb-2 p-2 border rounded';
                            studentDiv.innerHTML = `
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <strong>${student.name}</strong><br>
                                        <small class="text-muted">ID: ${student.id} | ${student.class}</small>
                                    </div>
                                    <div>
                                        <span class="badge bg-info">${student.books_issued} books</span>
                                    </div>
                                </div>
                            `;
                            studentsList.appendChild(studentDiv);
                        });
                    }
                } catch (error) {
                    console.error('Error loading students:', error);
                }
            }

            async function searchBooks() {
                const query = document.getElementById('searchInput').value;
                if (!query.trim()) {
                    loadBooks();
                    return;
                }

                try {
                    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                    const data = await response.json();
                    
                    if (data.success) {
                        const booksTable = document.getElementById('booksTable');
                        booksTable.innerHTML = '';
                        
                        data.books.forEach(book => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${book.name}</td>
                                <td>${book.author}</td>
                                <td>
                                    <span class="badge ${book.status === 'Available' ? 'bg-success' : 'bg-danger'}">
                                        ${book.status}
                                    </span>
                                </td>
                                <td>${book.issue_date}</td>
                                <td>${book.due_date}</td>
                                <td>${book.quantity} (Fixed)</td>
                                <td>
                                    <span class="badge ${book.issued_count > 0 ? 'bg-warning' : 'bg-secondary'}">
                                        ${book.issued_count} issued
                                    </span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-primary" onclick="selectBook('${book.id}')">
                                        <i class="fas fa-hand-pointer"></i> Select
                                    </button>
                                </td>
                            `;
                            booksTable.appendChild(row);
                        });
                    }
                } catch (error) {
                    console.error('Error searching books:', error);
                }
            }

            function selectBook(bookId) {
                document.getElementById('bookId').value = bookId;
            }

            async function issueBook() {
                const studentId = document.getElementById('studentId').value;
                const bookId = document.getElementById('bookId').value;
                
                if (!studentId || !bookId) {
                    alert('Please enter both Student ID and Book ID');
                    return;
                }

                try {
                    const response = await fetch('/api/issue', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            student_id: studentId,
                            book_id: bookId
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        alert('Book issued successfully! (Stock remains at 10)');
                        document.getElementById('studentId').value = '';
                        document.getElementById('bookId').value = '';
                        loadStatistics();
                        loadBooks();
                        loadStudents();
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    console.error('Error issuing book:', error);
                    alert('Failed to issue book. Please try again.');
                }
            }

            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadStatistics();
            }, 30000);

            // Enter key for search
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchBooks();
                }
            });
        </script>
    </body>
    </html>'''
        
        # Write HTML file
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        # Create CSS file
        css_content = '''
        /* Additional custom styles */
        .badge {
            padding: 0.5em 0.8em;
            font-weight: 600;
        }
        
        .table-hover tbody tr:hover {
            background-color: rgba(52, 152, 219, 0.1);
        }
        
        .card-header {
            border-radius: 15px 15px 0 0 !important;
        }
        
        .form-control:focus {
            border-color: #3498DB;
            box-shadow: 0 0 0 0.25rem rgba(52, 152, 219, 0.25);
        }
        '''
        
        with open('static/css/style.css', 'w') as f:
            f.write(css_content)

    # Create web portal files
    setup_web_portal_files()

    class WebPortal:
        def __init__(self):
            if not FLASK_AVAILABLE:
                self.app = None
                print("Flask not available. Web portal feature disabled.")
                return
                
            try:
                from flask import Flask, render_template, request, jsonify
                self.app = Flask(__name__, 
                                static_folder='static',
                                template_folder='templates')
                self.app.secret_key = 'library_secret_key_2024'
                self.setup_routes()
                self.portal_thread = None
                self.portal_running = False
            except ImportError:
                self.app = None
                print("Flask not available. Web portal feature disabled.")
        
        def setup_routes(self):
            if not self.app:
                return
                
            @self.app.route('/')
            def home():
                return render_template('index.html')
            
            @self.app.route('/api/books')
            def get_books():
                try:
                    with sqlite3.connect("library.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, DUE_DATE, QUANTITY FROM Library")
                        books = cursor.fetchall()
                        result = []
                        for book in books:
                            # Get issued count for each book
                            cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_ID=? AND BK_STATUS='Issued'", (book[1],))
                            issued_count = cursor.fetchone()[0]
                            
                            # Get issue date
                            issue_date = get_issue_date(book[1], book[4]) if book[4] != "N/A" else "N/A"
                            
                            result.append({
                                'name': book[0],
                                'id': book[1],
                                'author': book[2],
                                'status': book[3],
                                'issue_date': issue_date,
                                'due_date': book[5],
                                'quantity': book[6],
                                'issued_count': issued_count
                            })
                        return jsonify({'success': True, 'books': result})
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
            
            @self.app.route('/api/search')
            def search_books():
                query = request.args.get('q', '')
                try:
                    with sqlite3.connect("library.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, DUE_DATE, QUANTITY 
                            FROM Library 
                            WHERE UPPER(BK_NAME) LIKE UPPER(?) 
                            OR UPPER(AUTHOR_NAME) LIKE UPPER(?)
                        """, (f'%{query}%', f'%{query}%'))
                        books = cursor.fetchall()
                        result = []
                        for book in books:
                            # Get issued count for each book
                            cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_ID=? AND BK_STATUS='Issued'", (book[1],))
                            issued_count = cursor.fetchone()[0]
                            
                            # Get issue date
                            issue_date = get_issue_date(book[1], book[4]) if book[4] != "N/A" else "N/A"
                            
                            result.append({
                                'name': book[0],
                                'id': book[1],
                                'author': book[2],
                                'status': book[3],
                                'issue_date': issue_date,
                                'due_date': book[5],
                                'quantity': book[6],
                                'issued_count': issued_count
                            })
                        return jsonify({'success': True, 'books': result})
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
            
            @self.app.route('/api/students')
            def get_students():
                try:
                    with sqlite3.connect("library.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT STUDENT_ID, NAME, CLASS, CONTACT FROM Students")
                        students = cursor.fetchall()
                        result = []
                        for student in students:
                            cursor.execute("""
                                SELECT COUNT(*) FROM Library 
                                WHERE CARD_ID=? AND BK_STATUS='Issued'
                            """, (student[0],))
                            issued_count = cursor.fetchone()[0]
                            
                            result.append({
                                'id': student[0],
                                'name': student[1],
                                'class': student[2],
                                'contact': student[3],
                                'books_issued': issued_count
                            })
                        return jsonify({'success': True, 'students': result})
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
            
            @self.app.route('/api/issue', methods=['POST'])
            def issue_book():
                data = request.json
                student_id = data.get('student_id')
                book_id = data.get('book_id')
                
                try:
                    with sqlite3.connect("library.db") as conn:
                        cursor = conn.cursor()
                        
                        # Check if student exists
                        cursor.execute("SELECT * FROM Students WHERE STUDENT_ID=?", (student_id,))
                        if not cursor.fetchone():
                            return jsonify({'success': False, 'error': 'Student not found'})
                        
                        # Issue book (don't change quantity)
                        due = (datetime.now()+timedelta(days=14)).strftime("%Y-%m-%d")
                        
                        cursor.execute("""
                            UPDATE Library 
                            SET BK_STATUS='Issued', CARD_ID=?, DUE_DATE=?
                            WHERE BK_ID=?
                        """, (student_id, due, book_id))
                        conn.commit()
                        
                        # Send email
                        send_issue_email(student_id, "Book", book_id, due)
                        
                        return jsonify({'success': True, 'message': 'Book issued successfully (Stock remains at 10)'})
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
            
            @self.app.route('/api/statistics')
            def get_statistics():
                try:
                    with sqlite3.connect("library.db") as conn:
                        cursor = conn.cursor()
                        
                        # Total books
                        cursor.execute("SELECT SUM(QUANTITY) FROM Library")
                        total = cursor.fetchone()[0] or 0
                        
                        # Issued books
                        cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Issued'")
                        issued = cursor.fetchone()[0]
                        
                        # Students count
                        cursor.execute("SELECT COUNT(*) FROM Students")
                        students = cursor.fetchone()[0]
                        
                        # Fines
                        cursor.execute("SELECT DUE_DATE, FINE_PER_DAY FROM Library WHERE BK_STATUS='Issued'")
                        fine_res = cursor.fetchall()
                        fine = sum(calculate_fine(d[0], d[1]) for d in fine_res)
                        
                        return jsonify({
                            'success': True,
                            'statistics': {
                                'total_books': total,
                                'issued_books': issued,
                                'total_students': students,
                                'pending_fines': fine,
                                'available_books': total - issued
                            }
                        })
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
        
        def start_portal(self):
            if not self.app:
                mb.showerror("Error", "Flask not installed. Web portal feature unavailable.")
                return
                
            def run_flask():
                self.portal_running = True
                self.app.run(debug=False, port=5000, use_reloader=False)
            
            self.portal_thread = threading.Thread(target=run_flask, daemon=True)
            self.portal_thread.start()
            
            # Open browser after short delay
            threading.Timer(1.5, lambda: webbrowser.open('http://localhost:5000')).start()
            mb.showinfo("Web Portal", "🌐 Web portal started at http://localhost:5000\n\nThe portal will open in your browser.")
        
        def stop_portal(self):
            self.portal_running = False

    # Initialize web portal
    web_portal = WebPortal()

    def launch_web_portal():
        if web_portal.app is None:
            mb.showerror("Error", "Web portal is not available. Flask might not be installed.")
            return
        web_portal.start_portal()

    # ================== FINANCIAL MANAGEMENT SYSTEM ==================
    class FinancialManager:
        def __init__(self, connector):
            self.conn = connector
            self.cursor = connector.cursor()
            self.setup_financial_tables()
        
        def setup_financial_tables(self):
            # Fee Structure table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS FeeStructure (
                    FEE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FEE_TYPE TEXT,
                    AMOUNT REAL,
                    DUE_DATE TEXT,
                    APPLICABLE_TO TEXT,  -- 'All', 'Course:Year', 'Individual'
                    ACADEMIC_YEAR TEXT
                )
            """)
            
            # Fee Payments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS FeePayments (
                    PAYMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    STUDENT_ID TEXT,
                    FEE_TYPE TEXT,
                    AMOUNT_PAID REAL,
                    PAYMENT_DATE TEXT,
                    PAYMENT_MODE TEXT,
                    TRANSACTION_ID TEXT,
                    STATUS TEXT,
                    FOREIGN KEY (STUDENT_ID) REFERENCES Students(STUDENT_ID)
                )
            """)
            
            # Budget table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Budget (
                    BUDGET_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CATEGORY TEXT,
                    ALLOCATED_AMOUNT REAL,
                    SPENT_AMOUNT REAL DEFAULT 0,
                    FISCAL_YEAR TEXT,
                    START_DATE TEXT,
                    END_DATE TEXT
                )
            """)
            
            # Expenses table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Expenses (
                    EXPENSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CATEGORY TEXT,
                    AMOUNT REAL,
                    DESCRIPTION TEXT,
                    EXPENSE_DATE TEXT,
                    PAYMENT_MODE TEXT,
                    RECEIPT_NO TEXT,
                    APPROVED_BY TEXT
                )
            """)
            
            # Donations table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Donations (
                    DONATION_ID INTEGER PRIMARY KEY AUTOINcrement,
                    DONOR_NAME TEXT,
                    AMOUNT REAL,
                    DONATION_DATE TEXT,
                    PURPOSE TEXT,
                    PAYMENT_MODE TEXT,
                    RECEIPT_NO TEXT,
                    NOTES TEXT
                )
            """)
            
            self.conn.commit()
        
        def add_fee_structure(self, fee_type, amount, due_date, applicable_to="All", academic_year=None):
            if not academic_year:
                academic_year = datetime.now().strftime("%Y")
            
            try:
                self.cursor.execute("""
                    INSERT INTO FeeStructure (FEE_TYPE, AMOUNT, DUE_DATE, APPLICABLE_TO, ACADEMIC_YEAR)
                    VALUES (?,?,?,?,?)
                """, (fee_type, amount, due_date, applicable_to, academic_year))
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error adding fee structure: {e}")
                return False
        
        def record_fee_payment(self, student_id, fee_type, amount_paid, payment_mode="Cash", transaction_id=None):
            try:
                self.cursor.execute("""
                    INSERT INTO FeePayments (STUDENT_ID, FEE_TYPE, AMOUNT_PAID, PAYMENT_DATE, 
                                            PAYMENT_MODE, TRANSACTION_ID, STATUS)
                    VALUES (?,?,?,?,?,?,?)
                """, (student_id, fee_type, amount_paid, datetime.now().strftime("%Y-%m-%d"),
                     payment_mode, transaction_id, "Completed"))
                self.conn.commit()
                
                # Update student's library access if applicable
                if fee_type == "Library Membership":
                    self.cursor.execute("""
                        UPDATE Students SET LIBRARY_ACCESS = 'Active' WHERE STUDENT_ID = ?
                    """, (student_id,))
                    self.conn.commit()
                
                return True
            except Exception as e:
                print(f"Error recording fee payment: {e}")
                return False
        
        def add_expense(self, category, amount, description, payment_mode="Cash", receipt_no=None, approved_by="Admin"):
            try:
                self.cursor.execute("""
                    INSERT INTO Expenses (CATEGORY, AMOUNT, DESCRIPTION, EXPENSE_DATE, 
                                        PAYMENT_MODE, RECEIPT_NO, APPROVED_BY)
                    VALUES (?,?,?,?,?,?,?)
                """, (category, amount, description, datetime.now().strftime("%Y-%m-%d"),
                     payment_mode, receipt_no, approved_by))
                
                # Update budget spent amount
                self.cursor.execute("""
                    UPDATE Budget 
                    SET SPENT_AMOUNT = SPENT_AMOUNT + ? 
                    WHERE CATEGORY = ? AND FISCAL_YEAR = ?
                """, (amount, category, datetime.now().strftime("%Y")))
                
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error adding expense: {e}")
                return False
        
        def record_donation(self, donor_name, amount, purpose, payment_mode="Cash", notes=""):
            try:
                self.cursor.execute("""
                    INSERT INTO Donations (DONOR_NAME, AMOUNT, DONATION_DATE, PURPOSE, 
                                          PAYMENT_MODE, RECEIPT_NO, NOTES)
                    VALUES (?,?,?,?,?,?,?)
                """, (donor_name, amount, datetime.now().strftime("%Y-%m-%d"), purpose,
                     payment_mode, f"DON-{datetime.now().strftime('%Y%m%d%H%M%S')}", notes))
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Error recording donation: {e}")
                return False
        
        def get_financial_report(self, start_date=None, end_date=None):
            try:
                if not start_date:
                    start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
                if not end_date:
                    end_date = datetime.now().strftime("%Y-%m-%d")
                
                # Fee collection summary
                self.cursor.execute("""
                    SELECT 
                        SUM(AMOUNT_PAID) as total_fees,
                        COUNT(*) as payment_count,
                        FEE_TYPE,
                        STATUS
                    FROM FeePayments
                    WHERE PAYMENT_DATE BETWEEN ? AND ?
                    GROUP BY FEE_TYPE, STATUS
                """, (start_date, end_date))
                fee_summary = self.cursor.fetchall()
                
                # Expense summary
                self.cursor.execute("""
                    SELECT 
                        SUM(AMOUNT) as total_expenses,
                        COUNT(*) as expense_count,
                        CATEGORY
                    FROM Expenses
                    WHERE EXPENSE_DATE BETWEEN ? AND ?
                    GROUP BY CATEGORY
                """, (start_date, end_date))
                expense_summary = self.cursor.fetchall()
                
                # Donation summary
                self.cursor.execute("""
                    SELECT 
                        SUM(AMOUNT) as total_donations,
                        COUNT(*) as donation_count
                    FROM Donations
                    WHERE DONATION_DATE BETWEEN ? AND ?
                """, (start_date, end_date))
                donation_summary = self.cursor.fetchone()
                
                # Budget summary
                self.cursor.execute("""
                    SELECT 
                        CATEGORY,
                        ALLOCATED_AMOUNT,
                        SPENT_AMOUNT,
                        (ALLOCATED_AMOUNT - SPENT_AMOUNT) as remaining
                    FROM Budget
                    WHERE FISCAL_YEAR = ?
                """, (datetime.now().strftime("%Y"),))
                budget_summary = self.cursor.fetchall()
                
                return {
                    'fee_summary': fee_summary,
                    'expense_summary': expense_summary,
                    'donation_summary': donation_summary,
                    'budget_summary': budget_summary,
                    'period': (start_date, end_date)
                }
            except Exception as e:
                print(f"Error generating financial report: {e}")
                return None

    def show_financial_management():
        win = Toplevel(root)
        win.title("💰 Financial Management")
        win.geometry("1000x700")
        win.config(bg=COLORS['light_bg'])
        
        win.update_idletasks()
        width = 1000
        height = 700
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = Frame(win, bg=COLORS['primary'], height=70)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="💰 FINANCIAL MANAGEMENT", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
        
        # Create Notebook for tabs
        notebook = ttk.Notebook(win)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Initialize financial manager
        financial_manager = FinancialManager(connector)
        
        # ===== TAB 1: FEE MANAGEMENT =====
        fee_frame = Frame(notebook, bg=COLORS['light_bg'])
        notebook.add(fee_frame, text="🎫 Fee Management")
        
        # Fee payment form
        fee_form_frame = Frame(fee_frame, bg=COLORS['card_bg'], relief="flat", bd=2,
                              highlightbackground="#DDDDDD", highlightthickness=1)
        fee_form_frame.pack(fill=X, padx=20, pady=20)
        
        Label(fee_form_frame, text="💳 Record Fee Payment", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(15, 10))
        
        # Form fields
        fields_frame = Frame(fee_form_frame, bg=COLORS['card_bg'])
        fields_frame.pack(pady=10, padx=20)
        
        # Student ID
        Label(fields_frame, text="Student ID:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=0, column=0, sticky=W, pady=5)
        student_id_var = StringVar()
        Entry(fields_frame, textvariable=student_id_var, font=FONTS['body'], width=30).grid(row=0, column=1, pady=5, padx=10)
        
        # Fee Type
        Label(fields_frame, text="Fee Type:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=1, column=0, sticky=W, pady=5)
        fee_type_var = StringVar(value="Library Membership")
        fee_types = ["Library Membership", "Late Fee", "Book Damage", "Other"]
        ttk.Combobox(fields_frame, textvariable=fee_type_var, values=fee_types, 
                     state="readonly", width=28).grid(row=1, column=1, pady=5, padx=10)
        
        # Amount
        Label(fields_frame, text="Amount (₹):", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=2, column=0, sticky=W, pady=5)
        amount_var = StringVar()
        Entry(fields_frame, textvariable=amount_var, font=FONTS['body'], width=30).grid(row=2, column=1, pady=5, padx=10)
        
        # Payment Mode
        Label(fields_frame, text="Payment Mode:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=3, column=0, sticky=W, pady=5)
        payment_mode_var = StringVar(value="Cash")
        modes = ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"]
        ttk.Combobox(fields_frame, textvariable=payment_mode_var, values=modes, 
                     state="readonly", width=28).grid(row=3, column=1, pady=5, padx=10)
        
        def record_fee_payment():
            if not (student_id_var.get() and amount_var.get()):
                mb.showerror("Error", "Student ID and Amount are required")
                return
            
            try:
                amount = float(amount_var.get())
                if financial_manager.record_fee_payment(
                    student_id_var.get(),
                    fee_type_var.get(),
                    amount,
                    payment_mode_var.get()
                ):
                    mb.showinfo("Success", "✅ Fee payment recorded successfully!")
                    
                    # Clear form
                    student_id_var.set("")
                    amount_var.set("")
                else:
                    mb.showerror("Error", "Failed to record fee payment")
            except ValueError:
                mb.showerror("Error", "Amount must be a number")
        
        Button(fee_form_frame, text="💳 Record Payment", 
               command=record_fee_payment,
               bg=COLORS['success'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(pady=15)
        
        # Fee history table
        Label(fee_frame, text="📋 Recent Fee Payments", bg=COLORS['light_bg'],
              font=FONTS['subheading']).pack(pady=(20, 10))
        
        # Create fee history table
        fee_history_frame = Frame(fee_frame, bg=COLORS['card_bg'])
        fee_history_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = Scrollbar(fee_history_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        fee_tree = ttk.Treeview(fee_history_frame,
                               columns=("Payment ID", "Student ID", "Fee Type", "Amount", "Date", "Mode", "Status"),
                               show="headings",
                               yscrollcommand=scrollbar.set)
        
        for col in ["Payment ID", "Student ID", "Fee Type", "Amount", "Date", "Mode", "Status"]:
            fee_tree.heading(col, text=col)
            fee_tree.column(col, width=100, anchor=CENTER)
        
        fee_tree.pack(fill=BOTH, expand=True)
        scrollbar.config(command=fee_tree.yview)
        
        # Load fee payments
        def load_fee_payments():
            for item in fee_tree.get_children():
                fee_tree.delete(item)
            
            cursor.execute("""
                SELECT PAYMENT_ID, STUDENT_ID, FEE_TYPE, AMOUNT_PAID, PAYMENT_DATE, 
                       PAYMENT_MODE, STATUS
                FROM FeePayments
                ORDER BY PAYMENT_DATE DESC
                LIMIT 100
            """)
            
            for payment in cursor.fetchall():
                fee_tree.insert("", END, values=payment)
        
        load_fee_payments()
        
        # ===== TAB 2: EXPENSE TRACKING =====
        expense_frame = Frame(notebook, bg=COLORS['light_bg'])
        notebook.add(expense_frame, text="💸 Expense Tracking")
        
        # Expense form
        expense_form_frame = Frame(expense_frame, bg=COLORS['card_bg'], relief="flat", bd=2,
                                  highlightbackground="#DDDDDD", highlightthickness=1)
        expense_form_frame.pack(fill=X, padx=20, pady=20)
        
        Label(expense_form_frame, text="💸 Record Expense", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(15, 10))
        
        # Expense form fields
        exp_fields_frame = Frame(expense_form_frame, bg=COLORS['card_bg'])
        exp_fields_frame.pack(pady=10, padx=20)
        
        # Category
        Label(exp_fields_frame, text="Category:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=0, column=0, sticky=W, pady=5)
        category_var = StringVar(value="Books")
        categories = ["Books", "Stationery", "Maintenance", "Utilities", "Salaries", "Other"]
        ttk.Combobox(exp_fields_frame, textvariable=category_var, values=categories, 
                     state="readonly", width=28).grid(row=0, column=1, pady=5, padx=10)
        
        # Amount
        Label(exp_fields_frame, text="Amount (₹):", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=1, column=0, sticky=W, pady=5)
        exp_amount_var = StringVar()
        Entry(exp_fields_frame, textvariable=exp_amount_var, font=FONTS['body'], width=30).grid(row=1, column=1, pady=5, padx=10)
        
        # Description
        Label(exp_fields_frame, text="Description:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=2, column=0, sticky=W, pady=5)
        description_var = StringVar()
        Entry(exp_fields_frame, textvariable=description_var, font=FONTS['body'], width=30).grid(row=2, column=1, pady=5, padx=10)
        
        def record_expense():
            if not (exp_amount_var.get() and description_var.get()):
                mb.showerror("Error", "Amount and Description are required")
                return
            
            try:
                amount = float(exp_amount_var.get())
                if financial_manager.add_expense(
                    category_var.get(),
                    amount,
                    description_var.get(),
                    "Cash"
                ):
                    mb.showinfo("Success", "✅ Expense recorded successfully!")
                    
                    # Clear form
                    exp_amount_var.set("")
                    description_var.set("")
                    load_expenses()
                else:
                    mb.showerror("Error", "Failed to record expense")
            except ValueError:
                mb.showerror("Error", "Amount must be a number")
        
        Button(expense_form_frame, text="➕ Record Expense", 
               command=record_expense,
               bg=COLORS['warning'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(pady=15)
        
        # Expense table
        Label(expense_frame, text="📊 Recent Expenses", bg=COLORS['light_bg'],
              font=FONTS['subheading']).pack(pady=(20, 10))
        
        expense_table_frame = Frame(expense_frame, bg=COLORS['card_bg'])
        expense_table_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        exp_scrollbar = Scrollbar(expense_table_frame)
        exp_scrollbar.pack(side=RIGHT, fill=Y)
        
        expense_tree = ttk.Treeview(expense_table_frame,
                                   columns=("ID", "Category", "Amount", "Description", "Date"),
                                   show="headings",
                                   yscrollcommand=exp_scrollbar.set)
        
        for col in ["ID", "Category", "Amount", "Description", "Date"]:
            expense_tree.heading(col, text=col)
            expense_tree.column(col, width=120, anchor=CENTER)
        
        expense_tree.pack(fill=BOTH, expand=True)
        exp_scrollbar.config(command=expense_tree.yview)
        
        def load_expenses():
            for item in expense_tree.get_children():
                expense_tree.delete(item)
            
            cursor.execute("""
                SELECT EXPENSE_ID, CATEGORY, AMOUNT, DESCRIPTION, EXPENSE_DATE
                FROM Expenses
                ORDER BY EXPENSE_DATE DESC
                LIMIT 100
            """)
            
            for expense in cursor.fetchall():
                expense_tree.insert("", END, values=expense)
        
        load_expenses()
        
        # ===== TAB 3: FINANCIAL REPORTS =====
        report_frame = Frame(notebook, bg=COLORS['light_bg'])
        notebook.add(report_frame, text="📈 Reports")
        
        def generate_financial_report():
            report = financial_manager.get_financial_report()
            
            if not report:
                mb.showerror("Error", "Failed to generate report")
                return
            
            # Create report window
            report_win = Toplevel(win)
            report_win.title("📊 Financial Report")
            report_win.geometry("900x600")
            report_win.config(bg=COLORS['light_bg'])
            
            # Header
            header = Frame(report_win, bg=COLORS['primary'], height=70)
            header.pack(fill=X)
            header.pack_propagate(False)
            
            Label(header, text="📊 FINANCIAL REPORT", 
              bg=COLORS['primary'], fg="white",
              font=FONTS['heading']).pack(expand=True, pady=15)
            
            # Report period
            period_frame = Frame(report_win, bg=COLORS['light_bg'])
            period_frame.pack(fill=X, padx=20, pady=10)
            
            Label(period_frame, 
                  text=f"Report Period: {report['period'][0]} to {report['period'][1]}",
                  bg=COLORS['light_bg'], font=FONTS['subheading']).pack()
            
            # Create notebook for report sections
            report_notebook = ttk.Notebook(report_win)
            report_notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # Summary tab
            summary_frame = Frame(report_notebook, bg=COLORS['light_bg'])
            report_notebook.add(summary_frame, text="📋 Summary")
            
            # Calculate totals
            total_fees = sum(fee[0] for fee in report['fee_summary'] if fee[0])
            total_expenses = sum(exp[0] for exp in report['expense_summary'] if exp[0])
            total_donations = report['donation_summary'][0] if report['donation_summary'][0] else 0
            
            # Summary statistics
            stats_frame = Frame(summary_frame, bg=COLORS['card_bg'], relief="flat", bd=2,
                               highlightbackground="#DDDDDD", highlightthickness=1)
            stats_frame.pack(pady=20, padx=20, fill=X)
            
            stats = [
                ("💰 Total Fees Collected", f"₹{total_fees:,.2f}"),
                ("💸 Total Expenses", f"₹{total_expenses:,.2f}"),
                ("🎁 Total Donations", f"₹{total_donations:,.2f}"),
                ("📊 Net Balance", f"₹{total_fees + total_donations - total_expenses:,.2f}")
            ]
            
            for i, (label, value) in enumerate(stats):
                stat_frame = Frame(stats_frame, bg=COLORS['card_bg'])
                stat_frame.pack(fill=X, padx=20, pady=10)
                
                Label(stat_frame, text=label, bg=COLORS['card_bg'],
                      font=FONTS['body']).pack(side=LEFT)
                
                Label(stat_frame, text=value, bg=COLORS['card_bg'],
                      font=("Segoe UI", 12, "bold"), fg=COLORS['primary']).pack(side=RIGHT)
            
            # Budget status
            budget_frame = Frame(summary_frame, bg=COLORS['card_bg'], relief="flat", bd=2,
                                highlightbackground="#DDDDDD", highlightthickness=1)
            budget_frame.pack(pady=20, padx=20, fill=X)
            
            Label(budget_frame, text="📅 Budget Status", bg=COLORS['card_bg'],
                  font=FONTS['subheading']).pack(pady=(10, 15))
            
            for category, allocated, spent, remaining in report['budget_summary']:
                budget_item = Frame(budget_frame, bg=COLORS['card_bg'])
                budget_item.pack(fill=X, padx=10, pady=5)
                
                # Progress bar
                progress = spent / allocated * 100 if allocated > 0 else 0
                
                Label(budget_item, text=category, bg=COLORS['card_bg'],
                      font=FONTS['body'], width=20, anchor=W).pack(side=LEFT)
                
                progress_frame = Frame(budget_item, bg=COLORS['light_bg'], height=20)
                progress_frame.pack(side=LEFT, fill=X, expand=True, padx=10)
                
                progress_bar = Frame(progress_frame, bg='green' if progress < 80 else 'orange' if progress < 100 else 'red',
                                    height=20, width=progress)
                progress_bar.pack(side=LEFT)
                
                Label(budget_item, text=f"₹{spent:,.2f} / ₹{allocated:,.2f}",
                      bg=COLORS['card_bg'], font=FONTS['body']).pack(side=RIGHT)
            
            # Export button
            def export_report():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("PDF files", "*.pdf")],
                    initialfile=f"Financial_Report_{datetime.now().strftime('%Y%m%d')}.csv"
                )
                
                if file_path:
                    try:
                        with open(file_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(["FINANCIAL REPORT"])
                            writer.writerow([f"Period: {report['period'][0]} to {report['period'][1]}"])
                            writer.writerow([f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                            writer.writerow([])
                            writer.writerow(["SUMMARY"])
                            writer.writerow(["Total Fees Collected", f"₹{total_fees:,.2f}"])
                            writer.writerow(["Total Expenses", f"₹{total_expenses:,.2f}"])
                            writer.writerow(["Total Donations", f"₹{total_donations:,.2f}"])
                            writer.writerow(["Net Balance", f"₹{total_fees + total_donations - total_expenses:,.2f}"])
                            writer.writerow([])
                            writer.writerow(["BUDGET STATUS"])
                            writer.writerow(["Category", "Allocated", "Spent", "Remaining", "Utilization %"])
                            for category, allocated, spent, remaining in report['budget_summary']:
                                utilization = (spent / allocated * 100) if allocated > 0 else 0
                                writer.writerow([category, allocated, spent, remaining, f"{utilization:.1f}%"])
                        
                        mb.showinfo("Success", f"✅ Report exported to {file_path}")
                    except Exception as e:
                        mb.showerror("Error", f"Failed to export report: {e}")
            
            Button(report_win, text="📄 Export Report", 
                   command=export_report,
                   bg=COLORS['secondary'],
                   fg="white",
                   font=FONTS['button'],
                   padx=20,
                   pady=8).pack(pady=20)
        
        Button(report_frame, text="📈 Generate Financial Report", 
               command=generate_financial_report,
               bg=COLORS['primary'],
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=12).pack(expand=True)
        
        # ===== TAB 4: DONATIONS =====
        donation_frame = Frame(notebook, bg=COLORS['light_bg'])
        notebook.add(donation_frame, text="🎁 Donations")
        
        # Donation form
        donation_form_frame = Frame(donation_frame, bg=COLORS['card_bg'], relief="flat", bd=2,
                                   highlightbackground="#DDDDDD", highlightthickness=1)
        donation_form_frame.pack(fill=X, padx=20, pady=20)
        
        Label(donation_form_frame, text="🎁 Record Donation", bg=COLORS['card_bg'],
              font=FONTS['subheading']).pack(pady=(15, 10))
        
        # Donation form fields
        don_fields_frame = Frame(donation_form_frame, bg=COLORS['card_bg'])
        don_fields_frame.pack(pady=10, padx=20)
        
        # Donor Name
        Label(don_fields_frame, text="Donor Name:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=0, column=0, sticky=W, pady=5)
        donor_var = StringVar()
        Entry(don_fields_frame, textvariable=donor_var, font=FONTS['body'], width=30).grid(row=0, column=1, pady=5, padx=10)
        
        # Amount
        Label(don_fields_frame, text="Amount (₹):", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=1, column=0, sticky=W, pady=5)
        don_amount_var = StringVar()
        Entry(don_fields_frame, textvariable=don_amount_var, font=FONTS['body'], width=30).grid(row=1, column=1, pady=5, padx=10)
        
        # Purpose
        Label(don_fields_frame, text="Purpose:", bg=COLORS['card_bg'],
              font=FONTS['body']).grid(row=2, column=0, sticky=W, pady=5)
        purpose_var = StringVar(value="Books")
        purposes = ["Books", "Infrastructure", "Scholarship", "General", "Other"]
        ttk.Combobox(don_fields_frame, textvariable=purpose_var, values=purposes, 
                     state="readonly", width=28).grid(row=2, column=1, pady=5, padx=10)
        
        def record_donation():
            if not (donor_var.get() and don_amount_var.get()):
                mb.showerror("Error", "Donor Name and Amount are required")
                return
            
            try:
                amount = float(don_amount_var.get())
                if financial_manager.record_donation(
                    donor_var.get(),
                    amount,
                    purpose_var.get()
                ):
                    mb.showinfo("Success", "✅ Donation recorded successfully!")
                    
                    # Clear form
                    donor_var.set("")
                    don_amount_var.set("")
                    load_donations()
                else:
                    mb.showerror("Error", "Failed to record donation")
            except ValueError:
                mb.showerror("Error", "Amount must be a number")
        
        Button(donation_form_frame, text="💝 Record Donation", 
               command=record_donation,
               bg="#E74C3C",
               fg="white",
               font=FONTS['button'],
               padx=20,
               pady=8).pack(pady=15)
        
        # Donations table
        Label(donation_frame, text="📋 Recent Donations", bg=COLORS['light_bg'],
              font=FONTS['subheading']).pack(pady=(20, 10))
        
        donation_table_frame = Frame(donation_frame, bg=COLORS['card_bg'])
        donation_table_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        don_scrollbar = Scrollbar(donation_table_frame)
        don_scrollbar.pack(side=RIGHT, fill=Y)
        
        donation_tree = ttk.Treeview(donation_table_frame,
                                    columns=("ID", "Donor", "Amount", "Purpose", "Date"),
                                    show="headings",
                                    yscrollcommand=don_scrollbar.set)
        
        for col in ["ID", "Donor", "Amount", "Purpose", "Date"]:
            donation_tree.heading(col, text=col)
            donation_tree.column(col, width=120, anchor=CENTER)
        
        donation_tree.pack(fill=BOTH, expand=True)
        don_scrollbar.config(command=donation_tree.yview)
        
        def load_donations():
            for item in donation_tree.get_children():
                donation_tree.delete(item)
            
            cursor.execute("""
                SELECT DONATION_ID, DONOR_NAME, AMOUNT, PURPOSE, DONATION_DATE
                FROM Donations
                ORDER BY DONATION_DATE DESC
                LIMIT 100
            """)
            
            for donation in cursor.fetchall():
                donation_tree.insert("", END, values=donation)
        
        load_donations()

    # Initialize financial manager
    financial_manager = FinancialManager(connector)

    # ===== MAIN APPLICATION WINDOW =====
    global root, total_books_label, issued_books_label, fine_label, status_bar, tree
    root = Tk()
    root.title("📚 Library Management System")
    root.geometry("1400x750")  # Increased width for new columns
    root.config(bg=COLORS['light_bg'])
    
    # Center window
    root.update_idletasks()
    width = 1400
    height = 750
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # ===== HEADER =====
    header_frame = Frame(root, bg=COLORS['primary'], height=100)
    header_frame.pack(fill=X)
    header_frame.pack_propagate(False)
    
    title_frame = Frame(header_frame, bg=COLORS['primary'])
    title_frame.pack(expand=True)
    
    Label(title_frame, text="📚 ", bg=COLORS['primary'], fg="white",
          font=("Segoe UI", 32)).pack(side=LEFT)
    
    Label(title_frame, text="LIBRARY MANAGEMENT SYSTEM", 
          bg=COLORS['primary'], fg="white",
          font=FONTS['title']).pack(side=LEFT)
    
    Label(header_frame, 
          text="Rajiv Gandhi College | Advanced Book Tracking & Management",
          bg=COLORS['primary'], fg="#BDC3C7",
          font=("Segoe UI", 11)).pack(pady=(0, 10))
    
    # ===== STATS BAR ===== (COMPACT VERSION)
    stats_frame = Frame(root, bg=COLORS['secondary'], height=45)  # Reduced from 60 to 45
    stats_frame.pack(fill=X, pady=(5, 0))  # Reduced vertical padding
    stats_frame.pack_propagate(False)

    # Create stat frames
    stat_frames = []
    for i in range(3):
        stat = Frame(stats_frame, bg=COLORS['secondary'])
        stat.pack(side=LEFT, expand=True, fill=Y)
        stat_frames.append(stat)

    # Total Books
    total_books_label = Label(stat_frames[0], text="📚 0", 
                             bg=COLORS['secondary'], fg="white",
                             font=("Segoe UI", 14, "bold"))  # Reduced from 18 to 14
    total_books_label.pack(pady=(1, 2))  # Reduced padding
    Label(stat_frames[0], text="Total Books", bg=COLORS['secondary'], fg="#ECF0F1",
          font=("Segoe UI", 8)).pack()  # Smaller font

    # Issued Books
    issued_books_label = Label(stat_frames[1], text="📖 0", 
                              bg=COLORS['secondary'], fg="white",
                              font=("Segoe UI", 14, "bold"))  # Reduced from 18 to 14
    issued_books_label.pack(pady=(1, 2))  # Reduced padding
    Label(stat_frames[1], text="Issued Books", bg=COLORS['secondary'], fg="#ECF0F1",
          font=("Segoe UI", 8)).pack()  # Smaller font

    # Pending Fines
    fine_label = Label(stat_frames[2], text="💰 ₹0", 
                      bg=COLORS['secondary'], fg="white",
                      font=("Segoe UI", 14, "bold"))  # Reduced from 18 to 14
    fine_label.pack(pady=(1, 2))  # Reduced padding
    Label(stat_frames[2], text="Pending Fines", bg=COLORS['secondary'], fg="#ECF0F1",
          font=("Segoe UI", 8)).pack()  # Smaller font
    
    # ===== MAIN CONTENT =====
    main_frame = Frame(root, bg=COLORS['light_bg'])
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)  # Reduced pady from 20 to 15
    
    # ===== LEFT SIDEBAR WITH SCROLLBAR =====
    sidebar_container = Frame(main_frame, bg=COLORS['sidebar'], width=350)
    sidebar_container.pack(side=LEFT, fill=Y)
    sidebar_container.pack_propagate(False)
    
    # Create Canvas and Scrollbar
    sidebar_canvas = Canvas(sidebar_container, bg=COLORS['sidebar'], highlightthickness=0)
    sidebar_scrollbar = Scrollbar(sidebar_container, orient="vertical", command=sidebar_canvas.yview)
    
    # Create scrollable frame
    sidebar = Frame(sidebar_canvas, bg=COLORS['sidebar'])
    
    # Configure the canvas
    sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
    
    # Pack scrollbar and canvas
    sidebar_scrollbar.pack(side=RIGHT, fill=Y)
    sidebar_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Add the sidebar frame to the canvas
    sidebar_window = sidebar_canvas.create_window((0, 0), window=sidebar, anchor="nw")
    
    # Configure scrolling
    def configure_scroll_region(event):
        sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
    
    sidebar.bind("<Configure>", configure_scroll_region)
    
    # Safe mousewheel binding for sidebar
    def on_sidebar_mousewheel(event):
        try:
            # Handle different event types for cross-platform compatibility
            if hasattr(event, 'delta'):
                # Windows/MacOS
                scroll_amount = int(-1 * (event.delta / 120))
            elif event.num == 4:
                # Linux scroll up
                scroll_amount = -1
            elif event.num == 5:
                # Linux scroll down
                scroll_amount = 1
            else:
                return
            
            sidebar_canvas.yview_scroll(scroll_amount, "units")
        except Exception:
            # Ignore mousewheel errors if widget is destroyed
            pass
    
    # Bind mousewheel events with error handling
    try:
        sidebar_canvas.bind_all("<MouseWheel>", on_sidebar_mousewheel)
        sidebar_canvas.bind_all("<Button-4>", on_sidebar_mousewheel)
        sidebar_canvas.bind_all("<Button-5>", on_sidebar_mousewheel)
    except:
        pass
    
    sidebar_header = Frame(sidebar, bg=COLORS['dark_bg'], height=50)
    sidebar_header.pack(fill=X)
    sidebar_header.pack_propagate(False)
    
    Label(sidebar_header, text="📋 Operations", 
          bg=COLORS['dark_bg'], fg="white",
          font=FONTS['subheading']).pack(expand=True, pady=10)
    
    # Book Entry Section
    entry_section = Frame(sidebar, bg=COLORS['sidebar'], padx=15, pady=15)
    entry_section.pack(fill=X, pady=(0, 10))
    
    Label(entry_section, text="📝 Add New Book", 
          bg=COLORS['sidebar'], fg="#BDC3C7",
          font=("Segoe UI", 11, "bold")).pack(anchor=W, pady=(0, 10))
    
    # Create StringVars
    global bk_name, bk_id, author, fine_per_day
    bk_name = StringVar()
    bk_id = StringVar()
    author = StringVar()
    fine_per_day = StringVar(value="5")
    
    # Book Name
    Label(entry_section, text="Book Name:", bg=COLORS['sidebar'], 
          fg="white", font=("Segoe UI", 9)).pack(anchor=W)
    Entry(entry_section, textvariable=bk_name, font=("Segoe UI", 9),
          bg="white", fg=COLORS['primary'], relief="solid", bd=1).pack(fill=X, pady=(2, 8))
    
    # Book ID
    Label(entry_section, text="Book ID:", bg=COLORS['sidebar'], 
          fg="white", font=("Segoe UI", 9)).pack(anchor=W)
    Entry(entry_section, textvariable=bk_id, font=("Segoe UI", 9),
          bg="white", fg=COLORS['primary'], relief="solid", bd=1).pack(fill=X, pady=(2, 8))
    
    # Author
    Label(entry_section, text="Author:", bg=COLORS['sidebar'], 
          fg="white", font=("Segoe UI", 9)).pack(anchor=W)
    Entry(entry_section, textvariable=author, font=("Segoe UI", 9),
          bg="white", fg=COLORS['primary'], relief="solid", bd=1).pack(fill=X, pady=(2, 8))
    
    # Fine per Day
    Label(entry_section, text="Fine per Day (₹):", bg=COLORS['sidebar'], 
          fg="white", font=("Segoe UI", 9)).pack(anchor=W)
    Entry(entry_section, textvariable=fine_per_day, font=("Segoe UI", 9),
          bg="white", fg=COLORS['primary'], relief="solid", bd=1).pack(fill=X, pady=(2, 15))
    
    # Add Book Button
    Button(entry_section, text="➕ Add Book", 
           command=add_record,
           bg=COLORS['success'],
           fg="white",
           font=("Segoe UI", 10, "bold"),
           padx=20,
           pady=8,
           relief="flat",
           cursor="hand2").pack(fill=X, pady=(5, 20))
    
    # Operations Buttons Section
    operations_label = Frame(sidebar, bg=COLORS['dark_bg'], height=40)
    operations_label.pack(fill=X, pady=(5, 0))
    operations_label.pack_propagate(False)
    
    Label(operations_label, text="🚀 Quick Actions", 
          bg=COLORS['dark_bg'], fg="white",
          font=("Segoe UI", 11, "bold")).pack(expand=True, pady=8)
    
    operations_frame = Frame(sidebar, bg=COLORS['sidebar'], padx=15, pady=10)
    operations_frame.pack(fill=X, pady=(0, 15))
    
    operations = [
        ("👁️ View Books", view_books, COLORS['secondary']),
        ("🎓 Add Student", add_student, "#9B59B6"),
        ("📋 View Students", view_students, "#3498DB"),
        ("🔄 Update Student Details", update_student_details, "#3498DB"),
        ("🗑️ Delete Student", delete_student, COLORS['accent']),
        ("📖 Issued History", view_issued_history, "#F39C12"),
        ("👨‍🎓 Student + Books", view_student_books, "#1ABC9C"),
        ("📊 Show Analytics", show_pie_chart, "#E74C3C"),
        ("📄 Generate Report", generate_library_report, COLORS['primary']),
        # NEW PHASE 3 FEATURES
        ("🤖 AI Recommendations", show_ai_recommendations, "#9B59B6"),
        ("💬 Library Chatbot", show_library_chatbot, "#E74C3C"),
        ("💰 Financial Management", show_financial_management, "#27AE60"),
        ("🌐 Web Portal", launch_web_portal, "#3498DB"),
        ("🔍 Clear Search", lambda: [search_var.set(""), display_records("")], "#95A5A6"),
    ]
    
    for text, command, color in operations:
        btn = Button(operations_frame, 
                    text=text,
                    command=command,
                    bg=color,
                    fg="white",
                    font=("Segoe UI", 10),
                    anchor="w",
                    padx=20,
                    pady=12,
                    relief="flat",
                    cursor="hand2")
        btn.pack(fill=X, pady=5)
        
        # Add hover effect
        def make_hover(btn, color):
            def on_enter(e):
                btn['bg'] = COLORS['highlight']
            def on_leave(e):
                btn['bg'] = color
            return on_enter, on_leave
        
        on_enter, on_leave = make_hover(btn, color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    # Update scroll region after all widgets are added
    sidebar.update_idletasks()
    sidebar_canvas.config(scrollregion=sidebar_canvas.bbox("all"))
    
    # ===== RIGHT PANEL =====
    right_panel = Frame(main_frame, bg=COLORS['card_bg'], 
                       relief="flat", bd=2,
                       highlightbackground="#DDDDDD", 
                       highlightthickness=1)
    right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=(20, 0))
    
    # ===== ENHANCED SEARCH SECTION WITH DROPDOWN =====
    search_frame = Frame(right_panel, bg=COLORS['card_bg'], pady=15, padx=15)
    search_frame.pack(fill=X)
    
    Label(search_frame, text="🔍 Search Books (by Name or Author):", 
          bg=COLORS['card_bg'],
          font=FONTS['subheading']).pack(side=LEFT)
    
    # Search entry with dropdown
    search_entry = Entry(search_frame, font=FONTS['body'], width=40,
                        relief="solid", bd=1)
    search_entry.pack(side=LEFT, padx=10, fill=X, expand=True, ipady=3)
    
    # Setup dropdown search
    setup_search_dropdown(search_entry)
    
    # Search button
    Button(search_frame, text="Search",
           command=lambda: display_records(search_var.get()),
           bg=COLORS['secondary'],
           fg="white",
           font=FONTS['button'],
           padx=15,
           pady=5).pack(side=LEFT, padx=(5, 0))
    
    # Clear search button
    Button(search_frame, text="Clear",
           command=lambda: [search_var.set(""), display_records("")],
           bg="#95A5A6",
           fg="white",
           font=FONTS['button'],
           padx=15,
           pady=5).pack(side=LEFT, padx=(5, 0))
    
    # Table Section
    table_frame = Frame(right_panel, bg=COLORS['card_bg'])
    table_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))
    
    # Scrollbars
    v_scrollbar = Scrollbar(table_frame)
    v_scrollbar.pack(side=RIGHT, fill=Y)
    
    h_scrollbar = Scrollbar(table_frame, orient=HORIZONTAL)
    h_scrollbar.pack(side=BOTTOM, fill=X)
    
    # Treeview with Issue Date and Issued Count columns
    tree = ttk.Treeview(table_frame, 
                       columns=("Name", "ID", "Author", "Status", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Quantity", "Issued Count"), 
                       show="headings",
                       yscrollcommand=v_scrollbar.set,
                       xscrollcommand=h_scrollbar.set,
                       height=18)
    
    style = ttk.Style()
    style.configure("Treeview", 
                   font=FONTS['body'],
                   rowheight=28,
                   fieldbackground=COLORS['card_bg'])
    style.configure("Treeview.Heading",
                   font=("Segoe UI", 10, "bold"),
                   background=COLORS['light_bg'])
    
    col_widths = [180, 90, 130, 90, 90, 100, 100, 80, 80, 100]  # Added Issue Date column width
    columns = ("Name", "ID", "Author", "Status", "Student ID", "Issue Date", "Due Date", "Fine/Day", "Quantity", "Issued Count")
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=CENTER)
    
    tree.pack(fill=BOTH, expand=True)
    
    v_scrollbar.config(command=tree.yview)
    h_scrollbar.config(command=tree.xview)
    
    # ===== STATUS BAR =====
    status_bar = Label(root, text="🔍 Enter book name or author name to search", 
                      bg=COLORS['dark_bg'], fg="white",
                      font=("Segoe UI", 10),
                      anchor=W, padx=20)
    status_bar.pack(side=BOTTOM, fill=X)
    
    # ===== FINAL INITIALIZATION =====
    # Start with EMPTY dashboard (no books shown initially)
    # The treeview will be empty until user searches
    
    # Clear any existing records from tree
    if tree.winfo_exists():
        tree.delete(*tree.get_children())
    
    update_status()
    
    # Set minimum window size
    root.minsize(1300, 700)
    
    # Bind Enter key to search
    search_entry.bind('<Return>', lambda e: display_records(search_var.get()))
    
    # Set focus to search entry
    search_entry.focus_set()
    
    root.mainloop()

# Start the application
if __name__ == "__main__":
    login_screen()