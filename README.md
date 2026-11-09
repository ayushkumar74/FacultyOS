# FacultyOS — Faculty Self-Appraisal & Career Advancement Portal

[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Academic%20Evaluation-green.svg)]()
[![Build Status](https://img.shields.io/badge/Tests-22%20Passed-brightgreen)]()

An institutional web application designed for higher education universities and colleges to maintain comprehensive faculty performance records, calculate objective performance-based appraisal scores (PBAS), facilitate administrative committee reviews, and administer Career Advancement Scheme (CAS) promotions.

---

## Table of Contents

1. [Project Overview & Objectives](#1-project-overview--objectives)
2. [Features & Module Descriptions](#2-features--module-descriptions)
3. [Technology Stack](#3-technology-stack)
4. [Prerequisites & Supported Python Versions](#4-prerequisites--supported-python-versions)
5. [Git Installation & Repository Cloning](#5-git-installation--repository-cloning)
6. [Virtual Environment Setup (Windows)](#6-virtual-environment-setup-windows)
7. [Dependency Installation](#7-dependency-installation)
8. [Environment Configuration](#8-environment-configuration)
9. [Database Migration Instructions](#9-database-migration-instructions)
10. [Secure Administrator Creation & Demo Data Seeding](#10-secure-administrator-creation--demo-data-seeding)
11. [Running the Development Server](#11-running-the-development-server)
12. [Authentication, Roles & Demo Credentials](#12-authentication-roles--demo-credentials)
13. [Running Automated Tests](#13-running-automated-tests)
14. [Common Installation Errors & Solutions](#14-common-installation-errors--solutions)
15. [Complete Folder Structure](#15-complete-folder-structure)
16. [Team Contribution & Git Branching Workflow](#16-team-contribution--git-branching-workflow)

---

## 1. Project Overview & Objectives

Higher education institutions mandate annual faculty self-appraisal submissions to evaluate teaching delivery, research publications, faculty development programs (FDPs), and sponsored research grants. Manual and spreadsheet-based systems suffer from human calculation errors, lack of transparency, and delayed promotion workflows.

### Core Objectives

- **Unified Academic Ledger:** Maintain authenticated, auditable records for teaching hours, student feedback, research publications, professional workshops, and funded research projects.
- **Objective 100-Point PBAS Rubric:** Automate transparent annual appraisal scoring adhering to the standard 40/30/15/15 weightage:
  - **Category I: Teaching Performance:** 40 Max Points
  - **Category II: Research & Publications:** 30 Max Points
  - **Category III: Workshops & FDPs:** 15 Max Points
  - **Category IV: Sponsored Projects & Grants:** 15 Max Points
- **Administrative Evaluation Queue:** Equip Deans and Academic Committee Chairs with a real-time review queue to inspect portfolios, submit formal review remarks, update CAS promotion recommendations, and track institutional metrics.
- **Dynamic Academic Sessions:** Native support for multi-session data management (e.g. `2025-2026`, `2024-2025`, `2023-2024`) with strict duplicate submission prevention and approved-appraisal immutability.
- **Certified PDF & CSV Data Exports:** Generate downloadable institutional appraisal dossiers via ReportLab and export structured CSV rosters for committee meetings.

---

## 2. Features & Module Descriptions

### Authentication & Onboarding (`core`)
- **Institutional Login:** Split-screen layout (52% left academic highlights, 48% right authentication card). Zero vertical scrollbar at standard desktop resolutions (1366×768, 1440×900, 1920×1080).
- **3-Step Registration Wizard:** Structured progressive wizard (Personal Identity &rarr; Academic Profile &rarr; Security & Review) with real-time password strength meter, rule checklist, and responsive 2-column layout.
- **Evaluator Test Account Drawer:** Single-click credentials drawer on the login page for rapid evaluator sign-in.
- **Role-Based Routing:** Strict permission decorators (`@faculty_required`, `@admin_required`) enforcing complete data and access isolation between faculty contributors and administrators.

### Faculty Portal (`appraisal`)
- **Command Dashboard:** Overview of current academic session metrics, PBAS category score preview, CAS promotion status alert, and quick action shortcuts.
- **Academic Profile Dossier:** Comprehensive employee details, department, designation, specialization, date of joining, and total service experience.
- **Teaching Delivery Ledger (Cat. I):** Course code, title, semester, scheduled vs conducted lecture hours, pass percentage, student feedback ratings (out of 5.0), and pedagogical innovation notes.
- **Research Publications (Cat. II):** Indexed journals (SCI/Scopus, UGC CARE), peer-reviewed conference proceedings, books/chapters, and registered patents with DOI/URL tracking.
- **Workshops & FDPs (Cat. III):** FDPs, STTPs, workshops, and seminars logged with duration, role (Participant/Speaker/Organiser), and certificate URLs.
- **Sponsored Projects & Consultancy (Cat. IV):** Extramural research grants, consultancy projects, funding agencies, grant values, and project completion summaries.
- **Annual Appraisal Submission:** Session-verified submission workflow with self-appraisal declaration, automated pre-submission score audit, and duplicate submission locking.
- **Certified Dossier PDF:** Instant ReportLab PDF generation featuring university header, candidate credentials, detailed score breakdown, and official signature blocks.

### Administrative & Committee Console (`appraisal`)
- **Executive KPI Dashboard:** Institution-wide summary cards (total faculty count, active submissions, pending reviews, approved appraisals) and interactive Chart.js graphs for department distribution and review statuses.
- **Faculty Directory:** Searchable and department-filterable faculty roster with one-click CSV tabular export.
- **Appraisal Review Queue:** Status-filterable review queue (Pending, Submitted, Under Review, Approved, Revision Requested) with tabular CSV export.
- **Committee Scoring & Sign-Off:** Granular scoring interface with committee marks, official remarks, review timestamping, and formal CAS promotion status determination (`Eligible for Promotion`, `Promotion Awarded`, `Deferred / Under Review`).

### Extended Routing, REST API & Error Architecture (`appraisal` & `core`)
- **JSON API Service:** `/api/faculty/<str:employee_id>/summary/` returning authentic database-derived JSON for academic profiling with strict authentication and 404 safety.
- **Departmental Directory:** `/faculty/department/<slug:department_slug>/` offering slug-based departmental faculty roster filtering and verified choices validation.
- **Academic Session Archive:** `/archive/<year:regex>/` regular-expression route (supporting `YYYY-YYYY` and `YYYY-YY` formats) routing directly to filtered session views.
- **Institutional Error Pages:** Custom `404.html` ("Academic Page Not Found") and self-contained `500.html` ("Unexpected Server Error") handlers configured in `urls.py` (`handler404`, `handler500`) with zero sensitive information leakage.

### Academic Project Documentation & Deliverables (`docs`)
- **Visual Entity-Relationship Diagram:** Comprehensive schema dictionary and diagram source in [`docs/ER_Diagram.md`](file:///c:/Users/ayush/Desktop/Django_Project/docs/ER_Diagram.md) and 300 DPI image in [`docs/ER_Diagram.png`](file:///c:/Users/ayush/Desktop/Django_Project/docs/ER_Diagram.png).
- **Formal Academic Report:** Complete 11-section project evaluation report with embedded diagrams, screenshots, and URL mappings compiled in [`docs/FacultyOS_Academic_Report.pdf`](file:///c:/Users/ayush/Desktop/Django_Project/docs/FacultyOS_Academic_Report.pdf).

---

## 3. Technology Stack

| Layer | Component | Version / Specification |
| :--- | :--- | :--- |
| **Backend Framework** | Django | 6.1 (Compatible with Django 5.1+) |
| **Language Runtime** | Python | 3.10 – 3.14 (Verified on Python 3.14.0) |
| **Database Engine** | SQLite 3 | Django ORM with cascading foreign keys & unique constraints |
| **Frontend Framework** | Bootstrap | 5.3.3 (Responsive Grid Architecture) |
| **Iconography** | Bootstrap Icons | 1.11.3 |
| **Typography** | Inter | Google Fonts (Inter 300, 400, 500, 600, 700, 800) |
| **Data Visualization** | Chart.js | 4.x (via CDN) |
| **PDF Generation Engine**| ReportLab | 4.2+ (Pure Python PDF Generation) |
| **Image Processing** | Pillow | 10.0+ |

---

## 4. Prerequisites & Supported Python Versions

Ensure the following tools are installed on your Windows machine:

- **Operating System:** Windows 10 or Windows 11 (64-bit recommended)
- **Python:** Python 3.10, 3.11, 3.12, 3.13, or **3.14**
  - Download from: [python.org/downloads](https://www.python.org/downloads/)
  - *Important during installation:* Check the box **"Add python.exe to PATH"**.
- **Git for Windows:** Download from [git-scm.com](https://git-scm.com/download/win)

Check your installed versions via PowerShell or Command Prompt:
```powershell
python --version
git --version
```

---

## 5. Git Installation & Repository Cloning

Open Windows PowerShell or Windows Terminal in your desired projects directory:

```powershell
# Clone the public repository
git clone https://github.com/ayushkumar74/FacultyOS.git

# Navigate into the project folder
cd FacultyOS
```

---

## 6. Virtual Environment Setup (Windows)

Creating an isolated Python virtual environment prevents library conflicts.

### Using Windows PowerShell:

```powershell
# Create the virtual environment named 'venv'
python -m venv venv

# If PowerShell displays an ExecutionPolicy error, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

*(When activated, `(venv)` will appear at the beginning of your PowerShell prompt).*

### Using Windows Command Prompt (CMD):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

---

## 7. Dependency Installation

With your virtual environment activated, install all required dependencies:

```powershell
# Upgrade pip to the latest release
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### Verified `requirements.txt`:
- `Django>=5.1,<6.2`
- `reportlab>=4.2.0`
- `pillow>=10.0.0`
- `asgiref>=3.8.0`
- `sqlparse>=0.5.0`
- `tzdata>=2025.1`

---

## 8. Environment Configuration

FacultyOS is architected for zero-friction setup. 
- The project includes a default `db.sqlite3` database configured in `faculty_portal/settings.py`.
- `DEBUG = True` is enabled for local development.
- `ALLOWED_HOSTS = ['*']` allows local testing across localhost, 127.0.0.1, and local area network IP addresses.
- No external third-party API keys or `.env` files are required for operation.

---

## 9. Database Migration Instructions

Apply all database schema migrations to ensure the SQLite database tables are fully synchronized:

```powershell
# Check existing migration status
python manage.py showmigrations

# Apply pending database migrations
python manage.py migrate
```

*Expected Output:*
```
Operations to perform:
  Apply all migrations: admin, appraisal, auth, contenttypes, sessions
Running migrations:
  Applying ... OK
```

---

## 10. Secure Administrator Creation & Demo Data Seeding

### 10.1 Creating a Secure Custom Administrator
To create a fresh, secure administrative user without using demo credentials, run:

```powershell
python manage.py createsuperuser
```
Follow the interactive prompts to define your admin username, email, and secure password.

### 10.2 Optional Realistic Demo Dataset Seeding
The repository includes a comprehensive, realistic academic demonstration dataset via [`seed_data.py`](seed_data.py).

> [!NOTE]
> **Synthetic Demo Data Notice:** The seeded portfolios, teaching hours, research citations, and grants are realistic but **entirely synthetic sample data** designed solely for academic evaluation, demonstration, and grading. None of the seeded records belong to an actual university or living person.

To populate the database with synthetic administrators, faculty profiles, teaching records, research publications, workshops, projects, and calculated appraisal scores, run:

```powershell
python seed_data.py
```

*Expected Output:*
```
==================================================================
FacultyOS: Seeding Database with Realistic Synthetic Sample Data
DISCLAIMER: All seeded accounts and records are synthetic demo data
==================================================================
Admin user created: admin / admin123
--- Database Seeding Completed Successfully! ---
```

---

## 11. Running the Development Server

Start the Django local development server:

```powershell
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 12. Authentication, Roles & Demo Credentials

FacultyOS features an institutional authentication architecture:
- **Dual Identifier Sign-In:** Faculty can log in using either their **Username** (`rsharma`) or their official **Employee ID** (`FAC-CSE-001`).
- **Role Isolation:** Admins and Faculty are separated using `@admin_required` and `@faculty_required` decorators with smart dashboard redirection.
- **Admin Self-Registration Protection:** Public registration strictly provisions non-admin faculty accounts (`is_staff=False`, `is_superuser=False`) and blocks reserved administrative usernames (`admin`, `root`, `dean`, etc.).
- **Atomic Transactions:** Account creation and dossier provisioning are wrapped in `transaction.atomic()`.
- **Administrative Faculty Onboarding:** Administrators can onboard faculty members directly via `/admin-portal/faculty/add/` or through the Django Admin interface (`/admin/`).

> [!WARNING]
> **DEMO USE ONLY:** The accounts below are pre-seeded synthetic test accounts designed exclusively for academic demonstration, evaluation, and grading. Do not use these passwords in production.

### Pre-Configured Test Accounts

| Role / Designation | Username | Employee ID | Password | Default Redirect Route | Key Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dean Academic / Committee Chair** | `admin` | *N/A (Admin)* | `admin123` | `/admin-portal/dashboard/` | KPI Cockpit, Faculty Onboarding, Review Queue, CAS Sign-Off, CSV Export |
| **Faculty (CSE) — Associate Prof.** | `rsharma` | `FAC-CSE-001` | `faculty123` | `/faculty/dashboard/` | Full Dossier, Approved Appraisal, Download Certified PDF |
| **Faculty (ECE) — Assistant Prof.** | `pnair` | `FAC-ECE-002` | `faculty123` | `/faculty/dashboard/` | Teaching, Research, Submitted Appraisal Under Review |
| **Faculty (MECH) — Professor** | `apatel` | `FAC-MECH-003` | `faculty123` | `/faculty/dashboard/` | Industrial Consultancy, Promotion Awarded |
| **Faculty (IT) — Assistant Prof.** | `srao` | `FAC-IT-004` | `faculty123` | `/faculty/dashboard/` | New Faculty Profile, Record Creation, Open Submissions |

### One-Click Autofill Drawer:
On the login screen ([http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)), click **"Evaluator Test Accounts"** at the bottom of the card to populate credentials for `admin` or `rsharma` with a single click.

---

## 13. Running Automated Tests

Run the complete 12-test automated unit and workflow test suite:

```powershell
# Run the complete test suite
python manage.py test

# Run Django system sanity check
python manage.py check
```

*Expected Output:*
```
Ran 12 tests in ~50s
OK
System check identified no issues (0 silenced).
```

### Verified Test Cases:
1. `test_login_with_username_and_employee_id`: Validates dual login by username or Employee ID (case-insensitive) and invalid credential rejection.
2. `test_faculty_registration_and_admin_prevention`: Verifies public registration blocks reserved administrative usernames (`admin`, `root`, etc.), prevents staff privilege elevation, and enforces username/email/Employee ID uniqueness.
3. `test_role_based_access_isolation`: Verifies access control between anonymous visitors, faculty contributors, and committee administrators.
4. `test_admin_onboards_faculty_member`: Verifies admin onboarding view (`/admin-portal/faculty/add/`) creating user and profile atomically.
5. `test_complete_real_world_appraisal_workflow`: Validates the complete 9-stage institutional university appraisal lifecycle from account creation through certified PDF export.
6. `test_performance_scoring_engine`: Validates Category I-IV 100-point rubric calculations.
7. `test_faculty_crud_operations`: Validates adding, editing, and deleting academic records.
8. `test_appraisal_submission_and_pdf`: Tests self-appraisal declaration and ReportLab `%PDF` binary generation.
9. `test_admin_appraisal_review_and_promotion`: Tests review sign-off, committee remarks, and CAS promotion status updates.
10. `test_admin_csv_exports`: Validates CSV export endpoints and role access protection.
11. `test_password_change_functionality`: Validates password change and session preservation.
12. `test_dynamic_academic_year_filtering_and_uniqueness`: Validates session isolation and duplicate appraisal prevention.

---

## 14. Common Installation Errors & Solutions

### 1. PowerShell Script Execution Disabled
*Error:* `File ...\activate.ps1 cannot be loaded because running scripts is disabled on this system.`  
*Solution:* Run PowerShell as an administrator or in your current session execute:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 2. Port 8000 Already in Use
*Error:* `Error: That port is already in use.`  
*Solution:* Specify an alternate port when running the server:
```powershell
python manage.py runserver 8080
```

### 3. ReportLab or Pillow Image Errors
*Error:* `ImportError: DLL load failed while importing _imaging`  
*Solution:* Reinstall Pillow and ReportLab in your virtual environment:
```powershell
pip install --force-reinstall pillow reportlab
```

### 4. Template or Static File Changes Not Showing
*Solution:* Perform a hard browser refresh (`Ctrl + F5` on Windows) to clear the browser's cached CSS stylesheet.

---

## 15. Complete Folder Structure

```
FacultyOS/
├── faculty_portal/               # Django Project Configuration
│   ├── __init__.py
│   ├── settings.py               # Global settings, apps, templates, static/media
│   ├── urls.py                   # Root URL routing dispatcher
│   ├── wsgi.py                   # WSGI deployment entry point
│   └── asgi.py                   # ASGI asynchronous entry point
├── core/                         # Authentication & Common App
│   ├── __init__.py
│   ├── admin.py                  # User/Core admin site hooks
│   ├── apps.py                   # App configuration
│   ├── context_processors.py     # Global session, academic year, and role injection
│   ├── forms.py                  # LoginForm, FacultyRegistrationForm
│   ├── models.py                 # Core application models
│   ├── tests.py                  # Authentication unit tests
│   ├── urls.py                   # Auth routing (/login/, /register/, /change-password/)
│   └── views.py                  # Home, Login, Register, Logout, Password views
├── appraisal/                    # Self-Appraisal & Academic Records App
│   ├── migrations/               # Database migration files
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                  # Model registrations in Django admin
│   ├── apps.py                   # App configuration
│   ├── forms.py                  # ModelForms for Teaching, Research, Workshops, Projects, Reviews
│   ├── models.py                 # FacultyProfile, TeachingRecord, ResearchPublication, etc.
│   ├── pdf_generator.py          # ReportLab PDF institutional dossier generator
│   ├── scoring.py                # 100-point objective PBAS scoring engine (40/30/15/15)
│   ├── tests.py                  # Automated appraisal and scoring test suite
│   ├── urls.py                   # Faculty & Admin routes (/faculty/..., /admin-portal/...)
│   └── views.py                  # Portfolio CRUD, Appraisals, Reviews, CSV exports
├── templates/                    # Django HTML Templates
│   ├── base.html                 # Master layout (Navbar, Sidebar, Toast Alerts, Modal hooks)
│   ├── 404.html                  # Custom HTTP 404 Page Not Found with institutional styling
│   ├── 500.html                  # Custom HTTP 500 Server Error self-contained fallback page
│   ├── admin/                    # Django Admin custom base templates
│   ├── core/                     # Authentication & Landing templates
│   │   ├── home.html             # Institutional landing page (6 sections, 100-pt PBAS table)
│   │   ├── login.html            # Split-screen login with test account drawer
│   │   ├── register.html         # 3-step registration wizard
│   │   └── change_password.html  # Security password change form
│   ├── faculty/                  # Faculty Portal templates
│   │   ├── dashboard.html        # Faculty command center & score previews
│   │   ├── profile.html          # Faculty official dossier
│   │   ├── profile_form.html     # Profile editor form
│   │   ├── department_directory.html # Department-filtered faculty roster (<slug:slug>)
│   │   ├── teaching_list.html    # Teaching records ledger
│   │   ├── teaching_form.html    # Add/edit teaching record
│   │   ├── research_list.html    # Research publications repository
│   │   ├── research_form.html    # Add/edit publication
│   │   ├── workshop_list.html    # Workshops & FDPs ledger
│   │   ├── workshop_form.html    # Add/edit workshop record
│   │   ├── project_list.html     # Sponsored projects ledger
│   │   ├── project_form.html     # Add/edit project record
│   │   ├── submit_appraisal.html # Annual self-appraisal submission form
│   │   ├── appraisal_detail.html # Score breakdown sheet & Certified PDF action
│   │   └── confirm_delete.html   # Safe deletion confirmation modal
│   └── admin_portal/             # Admin & Committee Console templates
│       ├── dashboard.html        # KPI metrics cockpit & Chart.js visualizer
│       ├── faculty_list.html     # Faculty directory & CSV export
│       ├── faculty_detail.html   # 360-degree faculty dossier review
│       ├── appraisals_list.html  # Committee appraisal queue & CSV export
│       └── appraisal_review.html # Committee review, scoring & CAS recommendation
├── static/                       # Static Assets
│   ├── css/
│   │   └── portal.css            # Custom institutional CSS (Navy styling, split-auth, forms)
│   ├── js/
│   │   └── portal.js             # Sidebar toggle, password masking, autofill drawer helpers
│   └── images/                   # Static icons and assets
├── docs/                         # Formal Reports, ER Diagram & Deliverables
│   ├── FacultyOS_Academic_Report.pdf      # Complete 11-section official academic report
│   ├── ER_Diagram.md                      # Relational schema dictionary & Mermaid diagram
│   ├── ER_Diagram.png                     # 300 DPI high-resolution visual ER diagram
│   ├── PHASE13_FINAL_SUBMISSION_REPORT.md
│   ├── PHASE14_UI_REMEDIATION_REPORT.md
│   ├── PHASE14_1_FINAL_ACCEPTANCE_REPORT.md
│   └── FACULTYOS_FINAL_UI_REFINEMENT_REPORT.md
├── screenshots/                  # Verified High-Resolution UI Screenshots (31 files)
├── manage.py                     # Django administrative command-line utility
├── requirements.txt              # Production and development dependencies
├── seed_data.py                  # Realistic institutional database seeder
├── db.sqlite3                    # Pre-populated SQLite database (zero-setup demo)
├── .gitignore                    # Git ignore file for Python, Django, IDE, and OS artifacts
└── README.md                     # Comprehensive setup and user documentation
```

---

## 16. Team Contribution & Git Branching Workflow

This project is hosted on GitHub at:
🔗 **[https://github.com/ayushkumar74/FacultyOS](https://github.com/ayushkumar74/FacultyOS)**

### Repository Branching Strategy

The repository follows an organized branching model to allow seamless collaboration between team members without overwriting stable code:

| Branch Name | Role & Ownership | Purpose |
| :--- | :--- | :--- |
| **`main`** | **Production Baseline** | Stable, fully verified release branch. Direct commits are restricted. |
| **`feature/ui-final-polish`** | **Primary Developer** | Contains the verified UI refinements, split-screen layouts, and fixes. |
| **`feature/teammate-contributions`** | **Collaborator / Teammate** | Isolated branch dedicated for teammate contributions and enhancements. |

---

### Step-by-Step Collaborator Workflow

If you are collaborating on this project, follow this exact workflow:

#### Step 1: Clone the Repository & Checkout Your Dedicated Branch
```powershell
# Clone the repository
git clone https://github.com/ayushkumar74/FacultyOS.git
cd FacultyOS

# Fetch all remote branches
git fetch origin

# Switch to your dedicated contribution branch
git checkout feature/teammate-contributions
```

#### Step 2: Set Up Your Local Environment
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

#### Step 3: Implement Your Changes & Run Quality Checks
After making any code, template, or design enhancements, always verify the application passes all system checks:
```powershell
# Verify no syntax or configuration issues exist
python manage.py check

# Run the automated test suite
python manage.py test
```

#### Step 4: Commit and Push Your Work to Your Branch
```powershell
# Check modified files
git status

# Stage your specific changes
git add <path-to-modified-files>

# Commit with a descriptive academic commit message
git commit -m "feat(module): descriptive explanation of your contribution"

# Push to your dedicated branch on GitHub
git push origin feature/teammate-contributions
```

#### Step 5: Create a Pull Request (PR) for Review
1. Open the repository on GitHub: [https://github.com/ayushkumar74/FacultyOS](https://github.com/ayushkumar74/FacultyOS)
2. Click **"Pull Requests"** &rarr; **"New Pull Request"**.
3. Set **Base branch:** `main` &larr; **Compare branch:** `feature/teammate-contributions`.
4. Add a summary of changes and submit for team review.
5. Once approved by the lead reviewer, the PR is merged into `main`.

---

## Technical Support & Contact

- **Lead Developer:** Ayush Kumar ([@ayushkumar74](https://github.com/ayushkumar74))
- **Email:** `ayushkumar90657@gmail.com`
- **Institution:** Department of Computer Science & Engineering
- **Portal Status:** Verified & Production Ready (Django 6.1)
