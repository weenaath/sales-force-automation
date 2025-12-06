# 🚀 Sales Force Automation (SFA) System

A production-grade, full-stack Field Sales Management platform designed to bridge the gap between headquarters and field representatives. Features real-time GPS tracking, Digital Invoicing, and Interactive Analytics. Built with Django and modern Vanilla JS.

## 📖 Overview

The Sales Force Automation System is a full-stack web application tailored for distribution companies. It solves the challenge of real-time field data collection by providing:

1. For Management (HQ): A "Mission Control" dashboard with live revenue tracking, route performance heatmaps, and staff target monitoring. 

2. For Field Reps: A streamlined mobile interface to record sales, track inventory, and generate PDF invoices on the spot. 

This project focuses on User Experience (UX) and Data Visualization, moving away from clunky enterprise software to a clean, "SaaS-style" aesthetic.

## ✨ Key Features

### 🏢 HQ Admin Dashboard

- Visual Analytics: Interactive charts powered by Chart.js.

- GPS Location Stamping: Automatically captures Latitude/Longitude upon sale submission to verify rep location.

- Digital Invoicing: Generates professional PDF receipts instantly for customers using xhtml2pdf.

- Personal Performance: Real-time "Target vs. Actual" progress bars and 30-day performance trend charts.

- KPI Tiles: Real-time calculation of Total Revenue, Active Transactions, and Growth metrics.

- Data Management: Full control over Routes, Shops, and Products via the secure Django Admin panel.

### 🧢 Field Rep Dashboard (Mobile)

- Mobile-First Design: Large touch targets and simplified navigation for use on the go.

- Quick Entry: AJAX-powered "Add Sale" form allowing dynamic row addition for multiple products.

- Personal Stats: Instant view of "Today's Sales" and "Total Visits" to track personal targets.

### 🔐 Security & Architecture

- Role-Based Access Control (RBAC): Automatically routes users to the correct dashboard (Admin vs. Rep) upon login.

- Scalable Database: Uses PostgreSQL for production-grade data integrity (configured for SQLite in dev).

- Modern UI: Implements Glassmorphism, Mesh Gradients, and Phosphor Icons for a premium feel.

## 🛠️ Tech Stack

- Backend: Python 3, Django 5

- Database: PostgreSQL (Prod) / SQLite (Dev)

- Frontend: HTML5, CSS3 (Custom SaaS Theme), JavaScript (ES6)

- Visualization: Chart.js

- Icons: Phosphor Icons

- Deployment: Ready for PythonAnywhere / Heroku / AWS

## 🚀 Installation & Setup

Follow these steps to run the project locally.

Prerequisites

- Python 3.10 or higher

- Git

1. Clone the Repository

```git clone [https://github.com/YOUR_USERNAME/sales-force-automation.git](https://github.com/YOUR_USERNAME/sales-force-automation.git)
cd sales-force-automation
```


2. Create Virtual Environment

```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Setup Database

```
# Apply migrations to create the database file
python manage.py makemigrations
python manage.py migrate
```

5. Create Admin User

```
# Create the HQ account
python manage.py createsuperuser
```

6. Run the Server

```
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## 🧪 Usage Guide

Logging In

- Admin Access: Log in with the superuser account created above. You will be redirected to the Analytics Console.

- Rep Access: Create a standard user via the Django Admin panel (/admin). Log in with this account to see the Field Dashboard.

Adding Data

- Go to the Django Admin panel (http://127.0.0.1:8000/admin).

- Add Routes (e.g., "Downtown", "Suburbs").

- Add Products (e.g., "Item A", "Item B") with prices.

- Add Shops and assign them to Routes.

## 📂 Project Structure
```
sales-force-automation/
├── config/                     # Main project settings & URLs
├── sales_automation/           # The core app
│   ├── migrations/             # Database migration files
│   ├── static/                 # CSS, JS, Images
│   ├── templates/              # HTML files
│   │   └── sales_automation/
│   │       ├── base.html             # Master layout
│   │       ├── dashboard_admin.html  # HQ view
│   │       ├── dashboard_rep.html    # Field view
│   │       ├── add_sale.html         # Data entry
│   │       └── login.html            # Auth page
│   ├── admin.py                # Admin panel config
│   ├── models.py               # Database schema
│   ├── views.py                # Business logic & Charts
│   └── urls.py                 # App routing
├── manage.py                   # Django CLI
├── requirements.txt            # Dependencies
└── db.sqlite3                  # Local database 
```

## 📝 License

Copyright (c) 2025 Sakindu Weenath 

All Rights Reserved.

## 👤 Author

Sakindu Weenath

- LinkedIn: [www.linkedin.com/in/sakindu/](https://www.linkedin.com/in/sakindu/)

- GitHub: [www.github.com/weenaath](https://github.com/weenaath)
