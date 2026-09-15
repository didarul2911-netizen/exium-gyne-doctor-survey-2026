# Exium MUPS — GERD and Pregnancy Survey Portal (2026)
### Nationwide Digital Survey & Clinical Opinion Collection Platform
**Live URL:** [https://didarul2911-netizen.github.io/exium-gyne-doctor-survey-2026/](https://didarul2911-netizen.github.io/exium-gyne-doctor-survey-2026/)

A lightweight, mobile-first, enterprise-grade clinical survey application designed for Medical Information Officers (MIOs) across Bangladesh to conduct on-the-spot surveys with Obstetricians & Gynaecologists on GERD management during pregnancy.

---

## 🌟 Key Highlights & Architecture

1. **Nationwide Real-Time Cloud Sync (Google Sheets Backend)**:
   - **Instant Push**: Every mobile submission from field personnel immediately syncs asynchronously to a central Google Sheet.
   - **Offline Resilience**: Automatically caches responses in `localStorage` if cellular signal is weak in hospital chambers and auto-syncs when back online.
   - **Nationwide Aggregation**: Admin and Field Force dashboards pull live data from the cloud so Head Office, Zonal Heads, Regional Heads, and MIOs view up-to-the-minute coverage across all 1,869 territories.

2. **Full English Professional UI**:
   - Zero Bengali text throughout all screens, alerts, modals, and export files.
   - Polite, doctor-focused clinical presentation for rapid (<30 seconds) survey completion.

3. **Field Force Hierarchy & Submission Reports**:
   - **MIO Level**: Real-time list of surveyed doctors, RPL IDs, answers, and timestamps for any selected territory.
   - **Regional Head (RH) Level**: Territory-by-territory completion matrix, coverage percentage, and regional doctor list.
   - **Zonal Head (ZH) Level**: Zone-wide summary, regional breakdown, and completion KPIs.
   - Open access for field managers without requiring passwords.

4. **Central Admin & Analytics Control**:
   - Territory Submission Explorer with quick search and cascading Zone -> Region -> Territory filters.
   - Live Question 1 & Question 2 visual analytics breakdown.
   - Dynamic In-App Question & Answer choice editor.
   - Client-side Master Excel (.xlsx) and CSV exports.

---

## 📂 Project Structure

```
G:\Exium\2026\3Q'26\Survey (Gyne Doctor)\
│
├── index.html                               # Production Web Portal (Hosted on GitHub Pages)
├── Survey_Gyne_Doctor_Portal.html           # Standalone offline-capable backup
├── google_apps_script.js                    # Google Sheet sync engine backend
│
├── questions_config.json                    # Survey questions & answer choices config
├── territories.json                         # Parsed hierarchy of 1,869 territories
├── FF list.xlsx                             # Source Field Force dataset
├── Exium MUPS Logo.png                      # Brand header logo
│
├── Exium_Gyne_Doctor_Survey_Master_2026.xlsx# Master Excel template & dataset
├── generate_webapp.py                       # Python compiler for the web application
├── sync_excel.py                            # Offline Excel synchronizer
└── README.md                                # Official documentation
```

---

## ☁️ Google Sheets Real-Time Sync Setup Guide

To connect your own Google Sheet for central real-time data collection:

1. **Create Google Sheet**:
   - Go to Google Drive and create a new Google Sheet named `Exium_Gyne_Doctor_Survey_2026`.
   - Rename the first tab to `Survey_Responses`.

2. **Add Apps Script**:
   - In the Google Sheet, open menu: **Extensions > Apps Script**.
   - Copy and paste the entire content of [`google_apps_script.js`](google_apps_script.js) into `Code.gs`.

3. **Deploy as Web App**:
   - Click **Deploy > New Deployment**.
   - Select type: **Web app**.
   - Description: `Exium Gyne Survey Backend v1`.
   - Execute as: **Me** (`your_email@gmail.com`).
   - Who has access: **Anyone** (allows mobile MIO devices across Bangladesh to submit).
   - Click **Deploy** and authorize permissions when prompted.
   - Copy the generated **Web App URL** (e.g. `https://script.google.com/macros/s/.../exec`).

4. **Link to Web Portal**:
   - Open your portal: [https://didarul2911-netizen.github.io/exium-gyne-doctor-survey-2026/](https://didarul2911-netizen.github.io/exium-gyne-doctor-survey-2026/).
   - Click ⚙️ (Central Admin) in top-right.
   - Password: `admin` or `Exium MUPS`.
   - Under **Real-Time Google Sheet Cloud Sync**, paste the URL into the input field and click **Save Cloud URL 💾**.
   - Click **Test Connection 🔌** to verify connectivity!

---

## 📱 Survey Workflow

```
[ 1. MIO Setup ]
   │
   ▼
Quick Search (by Code/Name) or Select Zone ➔ Region ➔ Territory
   │
   ▼
[ 2. Doctor Information ]
   │
   ▼
Enter Doctor Name & 6-Digit RPL ID ➔ Proceed to Doctor's Survey ➡️
   │
   ▼
[ 3. Clinical Survey ]
   │
   ▼
Doctor selects Question 1 (Trimester) & Question 2 (GERD Symptoms) ➔ Submit Survey ✅
   │
   ▼
[ 4. Thank You Screen ]
   │
   ▼
"Back to Doctor's Entry ➡️" ➔ Instant Cloud Sync & Ready for Next Doctor!
```

---

## 🔒 Passwords & Security

- **Admin Control Panel**: `admin` or `Exium MUPS`
- **Field Reports (MIO / RH / ZH)**: Open access (No password required)