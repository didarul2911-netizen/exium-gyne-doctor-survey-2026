import os
import json
import base64

def get_base64_image(file_path):
    if not os.path.exists(file_path):
        return ""
    ext = os.path.splitext(file_path)[1].lower().replace(".", "")
    if ext == "jpg": ext = "jpeg"
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{encoded}"

def build():
    folder = r"G:\Exium\2026\3Q'26\Survey (Gyne Doctor)"
    
    # 1. Load logo
    logo_path = os.path.join(folder, "Exium MUPS Logo.png")
    logo_b64 = get_base64_image(logo_path)
    print("Logo encoded:", len(logo_b64), "bytes")

    # 2. Load questions config
    with open(os.path.join(folder, "questions_config.json"), "r", encoding="utf-8") as f:
        questions_config = json.load(f)

    # 3. Load territories
    with open(os.path.join(folder, "territories.json"), "r", encoding="utf-8") as f:
        territories = json.load(f)
    print(f"Loaded {len(territories)} territories.")

    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Exium MUPS — GERD and Pregnancy Survey</title>
  <link rel="icon" type="image/png" href="{logo_b64}">
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <!-- SheetJS for Client-Side Excel Export -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

  <style>
    :root {{
      --primary: #0284c7;
      --primary-dark: #0369a1;
      --primary-light: #e0f2fe;
      --accent: #10b981;
      --accent-dark: #059669;
      --accent-light: #d1fae5;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --danger: #ef4444;
      --warning: #f59e0b;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 12px rgba(2, 132, 199, 0.08);
      --shadow-lg: 0 10px 25px -5px rgba(2, 132, 199, 0.15);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      background: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 0;
      overflow-x: hidden;
    }}

    /* Main Container for Mobile First */
    .app-container {{
      width: 100%;
      max-width: 540px;
      min-height: 100vh;
      background: var(--card-bg);
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 0 30px rgba(0,0,0,0.05);
    }}

    @media (min-width: 600px) {{
      body {{
        padding: 24px 12px;
        background: #f1f5f9;
      }}
      .app-container {{
        min-height: auto;
        border-radius: var(--radius-lg);
        overflow: hidden;
        margin-bottom: 30px;
        border: 1px solid var(--border);
      }}
    }}

    /* App Header (2-Line Responsive Layout) */
    .app-header {{
      background: linear-gradient(135deg, #0f172a 0%, #0369a1 100%);
      color: white;
      padding: 12px 16px;
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
    }}

    /* Line 1: Brand Logo & Title */
    .header-brand-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .brand-logo {{
      height: 38px;
      max-width: 130px;
      object-fit: contain;
      background: white;
      padding: 3px 8px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      flex-shrink: 0;
    }}

    .header-title-box {{
      flex: 1;
      min-width: 0;
    }}

    .header-title-box h1 {{
      font-size: 15px;
      font-weight: 700;
      letter-spacing: -0.2px;
      color: #ffffff;
      line-height: 1.25;
      margin: 0;
    }}

    /* Line 2: Actions Bar (Reports & Admin) */
    .header-actions-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.1);
      padding: 5px 8px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}

    .btn-header-report {{
      flex: 1;
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: white;
      border-radius: 8px;
      padding: 0 12px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 700;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .btn-header-report:hover {{
      background: rgba(255, 255, 255, 0.25);
    }}

    .btn-icon {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: white;
      border-radius: 8px;
      width: 38px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
      flex-shrink: 0;
    }}

    .btn-icon:hover {{
      background: rgba(255, 255, 255, 0.25);
    }}

    .btn-icon {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: white;
      border-radius: 8px;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.2s;
    }}

    .btn-icon:hover {{
      background: rgba(255, 255, 255, 0.25);
    }}

    .btn-header-report {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: white;
      border-radius: 8px;
      padding: 0 10px;
      height: 32px;
      display: flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 700;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .btn-header-report:hover {{
      background: rgba(255, 255, 255, 0.25);
    }}

    /* Hierarchy Modal & Tabs */
    #reportsModal .modal-card {{
      max-width: 680px;
    }}

    .report-tabs {{
      display: flex;
      gap: 4px;
      margin-bottom: 12px;
      background: #f1f5f9;
      padding: 4px;
      border-radius: var(--radius-sm);
    }}

    .report-tab-btn {{
      flex: 1;
      padding: 8px 6px;
      border: none;
      background: transparent;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
    }}

    .report-tab-btn.active {{
      background: #ffffff;
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }}

    .data-table-container {{
      width: 100%;
      overflow-x: auto;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: #ffffff;
      margin-top: 8px;
      max-height: 240px;
    }}

    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
    }}

    .data-table th {{
      background: #f8fafc;
      color: #475569;
      font-weight: 700;
      padding: 8px 10px;
      border-bottom: 1.5px solid var(--border);
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 1;
    }}

    .data-table td {{
      padding: 8px 10px;
      border-bottom: 1px solid var(--border);
      color: #0f172a;
      white-space: nowrap;
    }}

    .data-table tr:hover td {{
      background: #f8fafc;
    }}

    .badge-status {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 700;
    }}

    .badge-completed {{
      background: #d1fae5;
      color: #065f46;
    }}

    .badge-pending {{
      background: #fef3c7;
      color: #92400e;
    }}

    /* Active Session Bar */
    .session-bar {{
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(8px);
      border-radius: 8px;
      padding: 6px 12px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}

    .session-info {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: #e2e8f0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .session-info strong {{
      color: #38bdf8;
    }}

    .btn-switch {{
      background: transparent;
      border: none;
      color: #fdba74;
      font-size: 11px;
      cursor: pointer;
      font-weight: 600;
      text-decoration: underline;
      padding: 2px 4px;
    }}

    /* App Content */
    .app-content {{
      padding: 20px 18px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    /* Screen Views */
    .screen {{
      display: none;
      flex-direction: column;
      gap: 18px;
      animation: fadeIn 0.25s ease-out;
    }}

    .screen.active {{
      display: flex;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Cards */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
    }}

    .card-header {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
    }}

    .card-step {{
      background: var(--primary);
      color: white;
      font-weight: 800;
      font-size: 12px;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .card-title {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .card-subtitle {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    .form-control.is-invalid {{
      border-color: var(--danger) !important;
      background-color: #fef2f2 !important;
    }}

    .form-control.is-invalid:focus {{
      box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15) !important;
    }}

    .search-feedback {{
      display: none;
      align-items: center;
      gap: 5px;
      margin-top: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--danger);
      animation: fadeIn 0.2s ease-out;
    }}

    /* Form Elements */
    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
    }}

    .form-label {{
      font-size: 13px;
      font-weight: 600;
      color: #334155;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .form-label .required {{
      color: var(--danger);
      font-weight: 800;
    }}

    .form-control {{
      width: 100%;
      padding: 12px 14px;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 14px;
      color: var(--text-main);
      background: #fff;
      transition: all 0.2s;
      outline: none;
    }}

    .form-control:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}

    .hint-text {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    select.form-control {{
      appearance: none;
      background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
      background-repeat: no-repeat;
      background-position: right 12px center;
      background-size: 16px;
      padding-right: 36px;
    }}

    /* Info Badge Box */
    .info-summary-box {{
      background: #f8fafc;
      border: 1.5px dashed #cbd5e1;
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      margin-top: 8px;
      display: none;
    }}

    .info-summary-box.active {{
      display: block;
    }}

    .info-row {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      padding: 3px 0;
      border-bottom: 1px dotted #e2e8f0;
    }}

    .info-row:last-child {{
      border-bottom: none;
    }}

    .info-label {{
      color: var(--text-muted);
      font-weight: 500;
    }}

    .info-val {{
      font-weight: 700;
      color: var(--text-main);
      text-align: right;
    }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 14px 20px;
      border-radius: var(--radius-md);
      font-size: 15px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
      box-shadow: var(--shadow-sm);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
      color: white;
    }}

    .btn-primary:active {{
      transform: scale(0.98);
      background: var(--primary-dark);
    }}

    .btn-primary:disabled {{
      background: #94a3b8;
      cursor: not-allowed;
      box-shadow: none;
    }}

    .btn-accent {{
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: white;
      font-size: 16px;
      padding: 16px;
    }}

    .btn-accent:active {{
      transform: scale(0.98);
    }}

    .btn-outline {{
      background: white;
      border: 1.5px solid var(--border);
      color: var(--text-main);
    }}

    .btn-outline:hover {{
      background: #f8fafc;
    }}

    /* Doctor View Styles (Clean English Only - No Icons) */
    .doctor-welcome {{
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: white;
      border-radius: var(--radius-md);
      padding: 18px 20px;
      box-shadow: var(--shadow-md);
    }}

    .doctor-welcome h2 {{
      font-size: 18px;
      font-weight: 800;
      margin-bottom: 4px;
    }}

    .doctor-welcome p {{
      font-size: 13px;
      color: #bae6fd;
      line-height: 1.4;
    }}

    .question-card {{
      background: white;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .q-number-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #e0f2fe;
      color: #0369a1;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 20px;
      align-self: flex-start;
    }}

    .q-title {{
      font-size: 15px;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.4;
    }}

    /* Options List - Clean Text Without Icons */
    .options-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 4px;
    }}

    .option-item {{
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 15px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.2s;
      background: #ffffff;
      user-select: none;
    }}

    .option-item:active {{
      transform: scale(0.98);
    }}

    .option-item.selected {{
      border-color: #0284c7;
      background: #f0f9ff;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.12);
    }}

    .option-radio {{
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 2px solid #cbd5e1;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.2s;
    }}

    .option-item.selected .option-radio {{
      border-color: #0284c7;
      background: #0284c7;
    }}

    .option-radio::after {{
      content: '';
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: white;
      opacity: 0;
      transition: opacity 0.2s;
    }}

    .option-item.selected .option-radio::after {{
      opacity: 1;
    }}

    .option-content {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      flex: 1;
    }}

    .option-text-en {{
      font-size: 14.5px;
      font-weight: 600;
      color: #1e293b;
      line-height: 1.35;
    }}

    /* Thank You Screen */
    .thank-you-box {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 36px 20px;
      gap: 16px;
    }}

    .checkmark-circle {{
      width: 76px;
      height: 76px;
      background: #d1fae5;
      color: #059669;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
      box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2);
    }}

    .thank-you-box h2 {{
      font-size: 22px;
      font-weight: 800;
      color: #0f172a;
    }}

    .thank-you-box p {{
      font-size: 14px;
      color: #475569;
      line-height: 1.5;
    }}

    .return-alert {{
      background: #fff7ed;
      border: 1.5px solid #ffedd5;
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      width: 100%;
    }}

    .return-alert-icon {{
      font-size: 28px;
    }}

    .return-alert strong {{
      color: #c2410c;
      font-size: 15px;
    }}

    .return-alert span {{
      color: #9a3412;
      font-size: 13px;
    }}

    /* Admin Modal */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}

    .modal-backdrop.active {{
      display: flex;
    }}

    .modal-card {{
      background: white;
      width: 100%;
      max-width: 600px;
      max-height: 90vh;
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: modalPop 0.25s ease-out;
    }}

    @keyframes modalPop {{
      from {{ transform: scale(0.94); opacity: 0; }}
      to {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-header {{
      background: #0f172a;
      color: white;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .modal-body {{
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    /* Stat Cards */
    .stat-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }}

    .stat-card {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 12px;
      text-align: center;
    }}

    .stat-val {{
      font-size: 22px;
      font-weight: 800;
      color: var(--primary);
    }}

    .stat-label {{
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Progress bar for analytics */
    .analytics-group {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .chart-bar-item {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      font-size: 12px;
    }}

    .chart-bar-header {{
      display: flex;
      justify-content: space-between;
      font-weight: 600;
      color: #334155;
    }}

    .bar-track {{
      height: 10px;
      background: #e2e8f0;
      border-radius: 5px;
      overflow: hidden;
    }}

    .bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #0284c7, #38bdf8);
      border-radius: 5px;
      transition: width 0.3s ease;
    }}

    /* Option Editor in Admin Panel */
    .admin-opt-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }}

    .admin-opt-code {{
      width: 28px;
      height: 28px;
      background: #e0f2fe;
      color: #0369a1;
      font-weight: 800;
      font-size: 12px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}

    .btn-opt-del {{
      background: #fee2e2;
      border: 1px solid #fecaca;
      color: #b91c1c;
      border-radius: 6px;
      width: 28px;
      height: 28px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      flex-shrink: 0;
    }}

    .btn-opt-del:hover {{
      background: #fca5a5;
    }}

    .btn-opt-add {{
      background: #f1f5f9;
      border: 1px dashed #cbd5e1;
      color: #334155;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
      width: fit-content;
    }}

    .btn-opt-add:hover {{
      background: #e2e8f0;
    }}

    /* Cloud Sync Badge */
    .btn-cloud-sync {{
      font-size: 11px;
      font-weight: 700;
      padding: 0 10px;
      height: 32px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: rgba(255, 255, 255, 0.15);
      color: #ffffff;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .btn-cloud-sync:hover {{
      background: #f1f5f9;
      border-color: #94a3b8;
    }}
    .btn-cloud-sync.connected {{
      border-color: #a7f3d0;
      background: #ecfdf5;
      color: #065f46;
    }}
    .btn-cloud-sync.syncing {{
      border-color: #bae6fd;
      background: #f0f9ff;
      color: #0369a1;
    }}
    .btn-cloud-sync.offline {{
      border-color: #fed7aa;
      background: #fff7ed;
      color: #9a3412;
    }}
    .status-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      display: inline-block;
      background: #94a3b8;
    }}
    .status-dot.connected {{
      background: #10b981;
      box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
    }}
    .status-dot.syncing {{
      background: #0284c7;
      animation: pulse 1s infinite;
    }}
    .status-dot.offline {{
      background: #f97316;
    }}

    /* Toast Notification */
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #0f172a;
      color: white;
      padding: 12px 20px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
      z-index: 200;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      opacity: 0;
      white-space: nowrap;
    }}

    .toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
    }}
    .badge-primary {{ background: var(--primary-light); color: var(--primary-dark); }}
    .badge-accent {{ background: var(--accent-light); color: var(--accent-dark); }}
  </style>
</head>
<body>

  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <!-- Line 1: Logo and Title -->
      <div class="header-brand-row">
        <img src="{logo_b64}" alt="Exium MUPS" class="brand-logo">
        <div class="header-title-box">
          <h1>GERD and Pregnancy Survey</h1>
        </div>
      </div>

      <!-- Line 2: Actions Bar (Reports & Admin) -->
      <div class="header-actions-row">
        <button class="btn-header-report" id="btnReportsOpen" title="Survey Submission Report">📊 Survey Submission Report</button>
        <button class="btn-icon" id="btnAdminOpen" title="Central Admin">⚙️</button>
      </div>

      <!-- Active Session Status Bar -->
      <div class="session-bar" id="sessionBar" style="display: none;">
        <div class="session-info">
          <span>👤 <strong id="sessMioName">MIO Name</strong> (<span id="sessTerritory">Territory</span>)</span>
        </div>
        <button class="btn-switch" id="btnSwitchTerritory">Switch</button>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="app-content">

      <!-- ============================================== -->
      <!-- SCREEN 1: MIO LOGIN & TERRITORY SETUP          -->
      <!-- ============================================== -->
      <div class="screen active" id="screenLogin">
        <div class="card">
          <div class="card-header">
            <div class="card-step">1</div>
            <div>
              <div class="card-title">MIO Territory Login</div>
              <div class="card-subtitle">Select Territory</div>
            </div>
          </div>

          <!-- Quick Search -->
          <div class="form-group">
            <label class="form-label">🔍 Quick Search</label>
            <input type="text" id="searchInput" class="form-control" placeholder="Search by MIO Code, Area Code, Name..." autocomplete="off">
            <div id="searchFeedback" class="search-feedback">
              <span>⚠️ Not Found</span>
            </div>
          </div>

          <div style="text-align: center; font-size: 12px; color: var(--text-muted); margin: -4px 0 10px;">— OR SELECT FROM HIERARCHY —</div>

          <!-- Zone Selection -->
          <div class="form-group">
            <label class="form-label">Zone <span class="required">*</span></label>
            <select id="zoneSelect" class="form-control">
              <option value="">-- Select Zone (35 Zones) --</option>
            </select>
          </div>

          <!-- Region Selection -->
          <div class="form-group">
            <label class="form-label">Region <span class="required">*</span></label>
            <select id="regionSelect" class="form-control" disabled>
              <option value="">-- First Select Zone --</option>
            </select>
          </div>

          <!-- Territory Selection -->
          <div class="form-group">
            <label class="form-label">Territory <span class="required">*</span></label>
            <select id="terrSelect" class="form-control" disabled>
              <option value="">-- First Select Region --</option>
            </select>
          </div>

          <!-- MIO Details Card (Auto-filled) -->
          <div class="info-summary-box" id="mioInfoBox">
            <div class="info-row">
              <span class="info-label">MIO / Sr. MIO Name:</span>
              <span class="info-val" id="dispMioName">-</span>
            </div>
            <div class="info-row">
              <span class="info-label">SAP MIO Code:</span>
              <span class="info-val" id="dispMioCode">-</span>
            </div>
            <div class="info-row">
              <span class="info-label">SAP Area Code:</span>
              <span class="info-val" id="dispAreaCode">-</span>
            </div>
            <div class="info-row">
              <span class="info-label">Regional Head:</span>
              <span class="info-val" id="dispRhName">-</span>
            </div>
            <div class="info-row">
              <span class="info-label">Zonal Head:</span>
              <span class="info-val" id="dispZhName">-</span>
            </div>
          </div>

          <button class="btn btn-primary" id="btnLoginProceed" style="margin-top: 14px;" disabled>
            <span>Proceed to Doctor Entry</span> ➡️
          </button>
        </div>
      </div>


      <!-- ============================================== -->
      <!-- SCREEN 2: DOCTOR INFO ENTRY (MIO PHASE)         -->
      <!-- ============================================== -->
      <div class="screen" id="screenDoctorInfo">
        <div class="card">
          <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div class="card-step">2</div>
              <div>
                <div class="card-title">Doctor's Information</div>
                <div class="card-subtitle">Fill in Doctor Details</div>
              </div>
            </div>
            <button type="button" class="btn btn-outline" id="btnQuickViewMyDoctors" style="font-size: 11px; padding: 5px 10px; width: auto; display: flex; align-items: center; gap: 4px; border-color: var(--primary); color: var(--primary);" title="View doctors surveyed in this territory">
              📋 View (<strong id="mySurveyCountBadge">0</strong>)
            </button>
          </div>

          <div class="form-group">
            <label class="form-label">Doctor's Full Name <span class="required">*</span></label>
            <input type="text" id="docName" class="form-control" placeholder="e.g. Prof. / Dr. Sabrina Parveen">
          </div>

          <div class="form-group">
            <label class="form-label">Doctor RPL ID (6-digit code) <span class="required">*</span></label>
            <input type="text" inputmode="numeric" pattern="\\d{{6}}" maxlength="6" id="docRplId" class="form-control" placeholder="e.g. 465737 (Strictly 6 numeric digits)">
            <span class="hint-text">⚠️ 6 numeric digits required (e.g. 465737)</span>
          </div>

          <button class="btn btn-primary" id="btnHandoverDoctor" style="width: 100%; margin-top: 14px; font-size: 16px; padding: 16px;">
            <span>Proceed to Doctor's Survey ➡️</span>
          </button>
        </div>
      </div>


      <!-- ============================================== -->
      <!-- SCREEN 3: DOCTOR QUESTIONNAIRE (DOCTOR PHASE)   -->
      <!-- ============================================== -->
      <div class="screen" id="screenDoctorSurvey">
        <div class="doctor-welcome">
          <h2>Welcome, Respected Doctor!</h2>
          <p>Dear <strong id="surveyDocWelcomeName">Doctor</strong>, please share your valued clinical opinion on the following 2 questions:</p>
        </div>

        <!-- Question 1 -->
        <div class="question-card" id="qCard1">
          <div class="q-number-badge">Question 1 of 2</div>
          <div class="q-title" id="q1TitleEn">Loading question 1...</div>

          <div class="options-list" id="q1OptionsContainer">
            <!-- Options dynamically rendered (Clean text without icons) -->
          </div>
        </div>

        <!-- Question 2 -->
        <div class="question-card" id="qCard2">
          <div class="q-number-badge">Question 2 of 2</div>
          <div class="q-title" id="q2TitleEn">Loading question 2...</div>

          <div class="options-list" id="q2OptionsContainer">
            <!-- Options dynamically rendered (Clean text without icons) -->
          </div>
        </div>

        <button class="btn btn-accent" id="btnSubmitSurvey" style="margin-top: 8px;">
          <span>Submit Survey ✅</span>
        </button>
      </div>


      <!-- ============================================== -->
      <!-- SCREEN 4: THANK YOU & HANDBACK (COMPLETION)    -->
      <!-- ============================================== -->
      <div class="screen" id="screenThankYou">
        <div class="card thank-you-box">
          <div class="checkmark-circle">✓</div>
          <h2>Thank You, Doctor!</h2>
          <p>Your clinical feedback has been successfully recorded.<br>Thank you for prescribing <strong>Exium MUPS</strong>.</p>

          <div style="margin-top: 24px; width: 100%;">
            <button class="btn btn-outline" id="btnMioUnlock" style="font-size: 15px; padding: 16px;">
              <span>Back to Doctor's Entry ➡️</span>
            </button>
          </div>
        </div>
      </div>

    </main>

    <!-- ============================================== -->
    <!-- MODAL: HIERARCHY REPORTS (MIO, RH, ZH)         -->
    <!-- ============================================== -->
    <div class="modal-backdrop" id="reportsModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3 style="font-size: 16px; font-weight: 700;">📊 Survey Submission Report</h3>
          <div style="display: flex; align-items: center; gap: 8px;">
            <button class="btn btn-outline" id="btnReportLiveRefresh" style="font-size: 11px; padding: 4px 8px; width: auto; border-color: var(--primary); color: var(--primary);" title="Pull latest survey responses from Google Sheet">🔄 Sync Live Data</button>
            <button class="btn-icon" id="btnReportsClose" style="width: 28px; height: 28px;">✕</button>
          </div>
        </div>

        <div class="modal-body">
          <!-- Role Tabs -->
          <div class="report-tabs">
            <button class="report-tab-btn active" id="tabBtnMio" data-tab="mioTab">👤 MIO (Territory)</button>
            <button class="report-tab-btn" id="tabBtnRh" data-tab="rhTab">👔 Regional Head</button>
            <button class="report-tab-btn" id="tabBtnZh" data-tab="zhTab">🏛️ Zonal Head</button>
          </div>

          <!-- TAB 1: MIO VIEW -->
          <div class="tab-content" id="mioTab">
            <!-- Quick Search for Territory/MIO -->
            <div class="form-group" style="margin-bottom: 8px;">
              <label class="form-label" style="font-size: 12px;">Quick Search Territory / MIO</label>
              <input type="text" id="reportMioQuickSearch" class="form-control" placeholder="Search by MIO Code, Terr Code, Name..." style="font-size: 13px; padding: 8px 12px;">
              <div id="reportMioSearchFeedback" class="search-feedback" style="font-size: 11px; margin-top: 4px;">
                <span>⚠️ Not Found</span>
              </div>
            </div>

            <!-- Hierarchy Dropdown Filters (Zone & Region) -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Zone (Filter)</label>
                <select id="reportMioZoneFilter" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
              </div>
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Region (Filter)</label>
                <select id="reportMioRegionFilter" class="form-control" style="font-size: 13px; padding: 8px 12px;" disabled></select>
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 10px;">
              <label class="form-label" style="font-size: 12px;">Select Territory / MIO</label>
              <select id="reportMioTerrSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
            </div>

            <!-- MIO KPI Stats -->
            <div class="stat-grid" style="margin-bottom: 10px;">
              <div class="stat-card">
                <div class="stat-val" id="mioStatTotalDocs">0</div>
                <div class="stat-label">Doctors Surveyed</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="mioStatTerrName" style="font-size: 13px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">-</div>
                <div class="stat-label">Territory Name</div>
              </div>
            </div>

            <!-- Doctor List Table -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
              <h4 style="font-size: 13px; font-weight: 700;">Doctor Clinical Records</h4>
              <button class="btn btn-outline" id="btnExportMioExcel" style="font-size: 11px; padding: 4px 8px; width: auto;">Export Excel</button>
            </div>
            <div class="data-table-container">
              <table class="data-table" id="tableMioDocs">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor Name</th>
                    <th>RPL ID</th>
                    <th>Trimester (Q1)</th>
                    <th>GERD Symptom (Q2)</th>
                    <th>Date & Time</th>
                  </tr>
                </thead>
                <tbody id="tbodyMioDocs">
                  <tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 16px;">No doctor surveys recorded yet in this territory</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- TAB 2: REGIONAL HEAD VIEW -->
          <div class="tab-content" id="rhTab" style="display: none;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px;">
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Zone</label>
                <select id="reportRhZoneSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
              </div>
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Region</label>
                <select id="reportRhRegionSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
              </div>
            </div>

            <!-- Regional Head Info Bar -->
            <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px 12px; font-size: 12px; margin-bottom: 10px;">
              Regional Head: <strong id="dispReportRhName" style="color: var(--primary);">-</strong>
            </div>

            <!-- Regional KPIs -->
            <div class="stat-grid" style="margin-bottom: 10px;">
              <div class="stat-card">
                <div class="stat-val" id="rhStatTotalDocs">0</div>
                <div class="stat-label">Doctors Surveyed</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="rhStatCompletedTerrs">0</div>
                <div class="stat-label">Completed Terrs</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="rhStatTotalTerrs">0</div>
                <div class="stat-label">Total Terrs</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="rhStatCoverage">0%</div>
                <div class="stat-label">Coverage</div>
              </div>
            </div>

            <!-- Region Tables: Territory Breakdown & Doctor Details -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
              <h4 style="font-size: 13px; font-weight: 700;">Territory Performance</h4>
              <button class="btn btn-outline" id="btnExportRhExcel" style="font-size: 11px; padding: 4px 8px; width: auto;">Export Region Excel</button>
            </div>
            <div class="data-table-container" style="max-height: 180px;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Territory</th>
                    <th>MIO Name</th>
                    <th>Status</th>
                    <th>Doctors Surveyed</th>
                  </tr>
                </thead>
                <tbody id="tbodyRhTerritories"></tbody>
              </table>
            </div>

            <h4 style="font-size: 13px; font-weight: 700; margin-top: 12px;">Doctor Records in Region</h4>
            <div class="data-table-container" style="max-height: 200px;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor Name</th>
                    <th>RPL ID</th>
                    <th>Territory</th>
                    <th>MIO Name</th>
                    <th>Trimester (Q1)</th>
                    <th>Symptom (Q2)</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody id="tbodyRhDoctors"></tbody>
              </table>
            </div>
          </div>

          <!-- TAB 3: ZONAL HEAD VIEW -->
          <div class="tab-content" id="zhTab" style="display: none;">
            <div class="form-group" style="margin-bottom: 10px;">
              <label class="form-label" style="font-size: 12px;">Select Zone</label>
              <select id="reportZhZoneSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
            </div>

            <!-- Zonal Head Info Bar -->
            <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px 12px; font-size: 12px; margin-bottom: 10px;">
              Zonal Head: <strong id="dispReportZhName" style="color: var(--primary);">-</strong>
            </div>

            <!-- Zonal KPIs -->
            <div class="stat-grid" style="margin-bottom: 10px;">
              <div class="stat-card">
                <div class="stat-val" id="zhStatTotalDocs">0</div>
                <div class="stat-label">Doctors Surveyed</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="zhStatCompletedTerrs">0</div>
                <div class="stat-label">Completed Terrs</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="zhStatTotalTerrs">0</div>
                <div class="stat-label">Total Terrs</div>
              </div>
              <div class="stat-card">
                <div class="stat-val" id="zhStatCoverage">0%</div>
                <div class="stat-label">Coverage</div>
              </div>
            </div>

            <!-- Regional Performance Matrix in this Zone -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
              <h4 style="font-size: 13px; font-weight: 700;">Regional Breakdown</h4>
              <button class="btn btn-outline" id="btnExportZhExcel" style="font-size: 11px; padding: 4px 8px; width: auto;">Export Zone Excel</button>
            </div>
            <div class="data-table-container" style="max-height: 180px;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Region</th>
                    <th>Regional Head</th>
                    <th>Territories</th>
                    <th>Completed</th>
                    <th>Doctors Surveyed</th>
                    <th>Coverage</th>
                  </tr>
                </thead>
                <tbody id="tbodyZhRegions"></tbody>
              </table>
            </div>

            <h4 style="font-size: 13px; font-weight: 700; margin-top: 12px;">Doctor Records in Zone</h4>
            <div class="data-table-container" style="max-height: 200px;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor Name</th>
                    <th>RPL ID</th>
                    <th>Region</th>
                    <th>Territory</th>
                    <th>MIO Name</th>
                    <th>Trimester (Q1)</th>
                    <th>Symptom (Q2)</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody id="tbodyZhDoctors"></tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- ============================================== -->
    <!-- MODAL: ADMIN & ANALYTICS DASHBOARD             -->
    <!-- ============================================== -->
    <div class="modal-backdrop" id="adminModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3 style="font-size: 16px; font-weight: 700;">⚙️ Central Survey Admin</h3>
          <button class="btn-icon" id="btnAdminClose" style="width: 28px; height: 28px;">✕</button>
        </div>

        <!-- Admin Login Form (if not logged in) -->
        <div class="modal-body" id="adminLoginBody">
          <div class="form-group">
            <label class="form-label">Admin Password</label>
            <input type="password" id="adminPassInput" class="form-control" placeholder="Enter password">
          </div>
          <button class="btn btn-primary" id="btnAdminAuth">Unlock Dashboard 🔓</button>
        </div>

        <!-- Admin Dashboard Content (Unlocked) -->
        <div class="modal-body" id="adminDashboardBody" style="display: none;">
          <!-- Stats Grid -->
          <div class="stat-grid">
            <div class="stat-card">
              <div class="stat-val" id="statTotalSurveys">0</div>
              <div class="stat-label">Total Surveys</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" id="statUniqueTerritories">0</div>
              <div class="stat-label">Territories Covered</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" id="statSyncCount">0</div>
              <div class="stat-label">Cloud Synced</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" id="statPendingCount">0</div>
              <div class="stat-label">Offline Cached</div>
            </div>
          </div>

          <!-- Question 1 Live Chart -->
          <div class="card" style="padding: 14px;">
            <h4 style="font-size: 13px; margin-bottom: 8px; color: var(--primary-dark);">📊 Question 1 Response Distribution</h4>
            <div class="analytics-group" id="q1AnalyticsContainer">
              <!-- Rendered via JS -->
            </div>
          </div>

          <!-- Question 2 Live Chart -->
          <div class="card" style="padding: 14px;">
            <h4 style="font-size: 13px; margin-bottom: 8px; color: var(--primary-dark);">📊 Question 2 Response Distribution</h4>
            <div class="analytics-group" id="q2AnalyticsContainer">
              <!-- Rendered via JS -->
            </div>
          </div>

          <!-- TERRITORY SUBMISSION EXPLORER (ADMIN) -->
          <div class="card" style="padding: 16px; background: #ffffff; border: 1.5px solid var(--border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
              <div>
                <h4 style="font-size: 14px; font-weight: 800; color: #0f172a;">🔍 Territory Submission Explorer</h4>
                <p style="font-size: 11px; color: var(--text-muted);">Check if a territory has submitted survey data</p>
              </div>
              <span class="badge badge-primary" id="adminTerrStatusBadge">Select Territory</span>
            </div>

            <!-- Quick Search Input -->
            <div class="form-group" style="margin-bottom: 8px;">
              <label class="form-label" style="font-size: 12px;">Quick Search (MIO Code, Terr Code, Name)</label>
              <input type="text" id="adminQuickSearch" class="form-control" placeholder="Type MIO Code, Terr Code, or Name..." style="font-size: 13px; padding: 8px 12px;">
              <div id="adminSearchFeedback" class="search-feedback" style="font-size: 11px; margin-top: 4px;">
                <span>⚠️ Not Found</span>
              </div>
            </div>

            <!-- Hierarchy Dropdowns (Zone & Region & Territory) -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Zone</label>
                <select id="adminZoneSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
              </div>
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 12px;">Region</label>
                <select id="adminRegionSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;" disabled></select>
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 10px;">
              <label class="form-label" style="font-size: 12px;">Territory</label>
              <select id="adminTerrSelect" class="form-control" style="font-size: 13px; padding: 8px 12px;"></select>
            </div>

            <!-- Territory Submission Summary Box -->
            <div id="adminTerrSummaryBox" style="background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; margin-bottom: 10px; display: none;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <strong id="adminDispTerrName" style="font-size: 13px; color: var(--primary);">-</strong>
                <span id="adminDispStatusBadge" class="badge-status">-</span>
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12px; color: var(--text-muted);">
                <div>MIO: <strong id="adminDispMioName" style="color: var(--text-main);">-</strong></div>
                <div>MIO Code: <code id="adminDispMioCode">-</code></div>
                <div>Region: <span id="adminDispRegName" style="color: var(--text-main); font-weight: 600;">-</span></div>
                <div>Doctors Submitted: <strong id="adminDispDocCount" style="color: var(--primary); font-size: 14px;">0</strong></div>
              </div>
            </div>

            <!-- Doctor Submissions Table -->
            <div class="data-table-container" style="max-height: 180px;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor Name</th>
                    <th>RPL ID</th>
                    <th>Trimester (Q1)</th>
                    <th>Symptom (Q2)</th>
                    <th>Date & Time</th>
                  </tr>
                </thead>
                <tbody id="tbodyAdminDocs">
                  <tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 14px;">Select or search a territory to inspect submissions</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- REAL-TIME GOOGLE SHEET CLOUD SYNC CONFIGURATION -->
          <div class="card" style="padding: 14px; background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">☁️</span>
                <div>
                  <h4 style="font-size: 13px; font-weight: 800; color: #166534;">Real-Time Google Sheet Cloud Sync</h4>
                  <p style="font-size: 11px; color: #15803d;">All 1,869 MIO mobile entries sync live to your central Google Sheet</p>
                </div>
              </div>
              <span class="badge" id="adminCloudStatusPill" style="background: #dcfce7; color: #15803d; border: 1px solid #86efac; font-size: 11px;">Ready</span>
            </div>

            <div class="form-group" style="margin-bottom: 8px;">
              <label class="form-label" style="font-size: 11px; font-weight: 700; color: #166534;">Google Apps Script Web App URL</label>
              <input type="url" id="adminCloudUrlInput" class="form-control" placeholder="https://script.google.com/macros/s/.../exec" style="font-size: 12px; font-family: monospace;">
            </div>

            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
              <button type="button" class="btn btn-primary" id="btnSaveCloudUrl" style="font-size: 12px; padding: 7px 12px; width: auto; background: #16a34a; border-color: #16a34a;">Save Cloud URL 💾</button>
              <button type="button" class="btn btn-outline" id="btnTestCloudConn" style="font-size: 12px; padding: 7px 12px; width: auto; border-color: #16a34a; color: #166534;">Test Connection 🔌</button>
              <button type="button" class="btn btn-outline" id="btnAdminPullCloud" style="font-size: 12px; padding: 7px 12px; width: auto; border-color: var(--primary); color: var(--primary);">Pull Live Data 📥</button>
              <button type="button" class="btn btn-outline" id="btnAdminPushCloud" style="font-size: 12px; padding: 7px 12px; width: auto; border-color: #f59e0b; color: #b45309;">Push Local Records ⬆️</button>
            </div>

            <div id="adminCloudMsg" style="font-size: 11px; padding: 6px 10px; border-radius: 6px; display: none;"></div>
          </div>

          <!-- DYNAMIC QUESTION & ANSWER CUSTOMIZER IN ADMIN PANEL -->
          <div class="card" style="padding: 16px; background: #fafafa; border: 1.5px solid #cbd5e1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <div>
                <h4 style="font-size: 14px; font-weight: 800; color: #0f172a;">✏️ Question & Answer Editor</h4>
                <p style="font-size: 11px; color: var(--text-muted);">Edit questions and answer choices directly</p>
              </div>
              <button class="badge badge-primary" id="btnResetDefaultQuestions" style="border: none; cursor: pointer; padding: 4px 10px;">Reset to Default</button>
            </div>

            <!-- Question 1 Editor -->
            <div style="background: white; border: 1px solid var(--border); border-radius: 10px; padding: 12px; margin-bottom: 12px;">
              <div class="form-group" style="margin-bottom: 10px;">
                <label class="form-label" style="font-size: 12px; font-weight: 700; color: var(--primary-dark);">Question 1 Title</label>
                <textarea id="editQ1En" class="form-control" rows="2" style="font-size: 13px;"></textarea>
              </div>
              <label class="form-label" style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Question 1 Answer Choices</label>
              <div id="q1AdminOptionsContainer"></div>
              <button type="button" class="btn-opt-add" id="btnAddQ1Option">+ Add Option to Q1</button>
            </div>

            <!-- Question 2 Editor -->
            <div style="background: white; border: 1px solid var(--border); border-radius: 10px; padding: 12px; margin-bottom: 14px;">
              <div class="form-group" style="margin-bottom: 10px;">
                <label class="form-label" style="font-size: 12px; font-weight: 700; color: var(--primary-dark);">Question 2 Title</label>
                <textarea id="editQ2En" class="form-control" rows="2" style="font-size: 13px;"></textarea>
              </div>
              <label class="form-label" style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Question 2 Answer Choices</label>
              <div id="q2AdminOptionsContainer"></div>
              <button type="button" class="btn-opt-add" id="btnAddQ2Option">+ Add Option to Q2</button>
            </div>

            <button class="btn btn-primary" id="btnSaveQuestions" style="font-size: 14px; padding: 12px;">Save Questions & Answers 💾</button>
          </div>

          <!-- Export Actions -->
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <button class="btn btn-primary" id="btnExportExcel">📥 Export Master Excel (.xlsx)</button>
            <button class="btn btn-outline" id="btnExportCSV">📥 Export CSV File</button>
            <button class="btn btn-outline" id="btnClearData" style="color: var(--danger); border-color: #fca5a5; font-weight: 700; background: #fff5f5;">🗑️ Delete All Survey Data (Local & Google Sheet)</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast" id="appToast">Notification Message</div>
  </div>

  <!-- Embedded Data & Application Logic -->
  <script>
    // Embedded Territories Data ({len(territories)} records)
    const TERRITORIES = {json.dumps(territories, ensure_ascii=False)};

    // Default Questions Configuration
    const DEFAULT_QUESTIONS = {json.dumps(questions_config, ensure_ascii=False)};

    // App State
    let currentMio = null;
    let currentDoctor = null;
    let selectedQ1 = null;
    let selectedQ2 = null;
    let activeQuestions = null;
    let isAdminLoggedIn = false;

    // Local Storage Keys
    const LS_SURVEYS = "EXIUM_GYNE_SURVEYS_2026";
    const LS_MIO = "EXIUM_ACTIVE_MIO_SESSION";
    const LS_QUESTIONS = "EXIUM_SURVEY_QUESTIONS_CONFIG_V3";
    const LS_CLOUD_URL = "EXIUM_GYNE_CLOUD_URL_2026";
    const DEFAULT_CLOUD_URL = "https://script.google.com/macros/s/AKfycbyNC2sDd7cN0286cA51r8vUxRrsxePn51wnjRsK0HQcsBEqa1EQKmMNTeE_Eeia5YNigA/exec";
    let cloudApiUrl = localStorage.getItem(LS_CLOUD_URL) || DEFAULT_CLOUD_URL;

    // Initialize Application
    document.addEventListener("DOMContentLoaded", () => {{
      loadQuestionsConfig();
      initHierarchy();
      initReportHierarchy();
      initAdminTerritoryExplorer();
      checkExistingSession();
      renderQuestions();
      setupEventListeners();
      updateMySurveyCountBadge();
      initCloudSync();
    }});

    // 1. Load Questions Config (LocalStorage or Default)
    function loadQuestionsConfig() {{
      const saved = localStorage.getItem(LS_QUESTIONS);
      if (saved) {{
        try {{
          activeQuestions = JSON.parse(saved);
        }} catch(e) {{
          activeQuestions = JSON.parse(JSON.stringify(DEFAULT_QUESTIONS));
        }}
      }} else {{
        activeQuestions = JSON.parse(JSON.stringify(DEFAULT_QUESTIONS));
      }}
    }}

    function resetHierarchySelection() {{
      const zoneSelect = document.getElementById("zoneSelect");
      const regionSelect = document.getElementById("regionSelect");
      const terrSelect = document.getElementById("terrSelect");
      const infoBox = document.getElementById("mioInfoBox");
      const btnProceed = document.getElementById("btnLoginProceed");

      if (zoneSelect) zoneSelect.value = "";
      if (regionSelect) {{
        regionSelect.innerHTML = '<option value="">-- First Select Zone --</option>';
        regionSelect.disabled = true;
      }}
      if (terrSelect) {{
        terrSelect.innerHTML = '<option value="">-- First Select Region --</option>';
        terrSelect.disabled = true;
      }}

      const elMio = document.getElementById("dispMioName");
      const elMioCode = document.getElementById("dispMioCode");
      const elArea = document.getElementById("dispAreaCode");
      const elRh = document.getElementById("dispRhName");
      const elZh = document.getElementById("dispZhName");

      if (elMio) elMio.textContent = "-";
      if (elMioCode) elMioCode.textContent = "-";
      if (elArea) elArea.textContent = "-";
      if (elRh) elRh.textContent = "-";
      if (elZh) elZh.textContent = "-";

      if (infoBox) infoBox.classList.remove("active");
      if (btnProceed) btnProceed.disabled = true;
      currentMio = null;
    }}

    function showSearchNotFound() {{
      const searchInput = document.getElementById("searchInput");
      const feedback = document.getElementById("searchFeedback");
      if (searchInput) searchInput.classList.add("is-invalid");
      if (feedback) feedback.style.display = "flex";
    }}

    function clearSearchFeedback() {{
      const searchInput = document.getElementById("searchInput");
      const feedback = document.getElementById("searchFeedback");
      if (searchInput) searchInput.classList.remove("is-invalid");
      if (feedback) feedback.style.display = "none";
    }}

    // 2. Initialize Hierarchy Dropdowns
    function initHierarchy() {{
      const zoneSelect = document.getElementById("zoneSelect");
      const uniqueZones = [...new Set(TERRITORIES.map(t => t.zone_name))].filter(Boolean).sort();
      
      zoneSelect.innerHTML = '<option value="">-- Select Zone (35 Zones) --</option>';
      uniqueZones.forEach(z => {{
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        zoneSelect.appendChild(opt);
      }});

      // Quick Search input listener
      const searchInput = document.getElementById("searchInput");
      searchInput.addEventListener("input", (e) => {{
        const term = e.target.value.trim().toLowerCase();

        // If user clears the input or it is empty -> restore default state!
        if (!term) {{
          clearSearchFeedback();
          resetHierarchySelection();
          return;
        }}

        // Priority 1: Exact match for MIO code or Territory code
        let match = TERRITORIES.find(t => 
          (t.mio_code && t.mio_code.toLowerCase() === term) ||
          (t.terr_code && t.terr_code.toLowerCase() === term)
        );

        // Priority 2: Starts-with match
        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().startsWith(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().startsWith(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().startsWith(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().startsWith(term))
          );
        }}

        // Priority 3: Substring match
        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().includes(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().includes(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().includes(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().includes(term))
          );
        }}

        if (match) {{
          clearSearchFeedback();
          selectTerritoryDirectly(match);
        }} else {{
          showSearchNotFound();
          resetHierarchySelection();
        }}
      }});
    }}

    function selectTerritoryDirectly(t) {{
      const zoneSelect = document.getElementById("zoneSelect");
      zoneSelect.value = t.zone_name;
      triggerZoneChange(t.zone_name, t.region_name, t.terr_code);
    }}

    function triggerZoneChange(zoneName, targetRegion = null, targetTerr = null) {{
      const regionSelect = document.getElementById("regionSelect");
      const terrSelect = document.getElementById("terrSelect");
      
      regionSelect.innerHTML = '<option value="">-- Select Region --</option>';
      terrSelect.innerHTML = '<option value="">-- First Select Region --</option>';
      terrSelect.disabled = true;

      if (!zoneName) {{
        clearSearchFeedback();
        resetHierarchySelection();
        return;
      }}

      const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === zoneName).map(t => t.region_name))].sort();
      regions.forEach(r => {{
        const opt = document.createElement("option");
        opt.value = r;
        opt.textContent = r;
        regionSelect.appendChild(opt);
      }});
      regionSelect.disabled = false;

      if (targetRegion) {{
        regionSelect.value = targetRegion;
        triggerRegionChange(zoneName, targetRegion, targetTerr);
      }}
    }}

    function triggerRegionChange(zoneName, regName, targetTerr = null) {{
      const terrSelect = document.getElementById("terrSelect");
      terrSelect.innerHTML = '<option value="">-- Select Territory --</option>';

      if (!regName) {{
        terrSelect.disabled = true;
        return;
      }}

      const terrs = TERRITORIES.filter(t => t.zone_name === zoneName && t.region_name === regName);
      terrs.forEach(t => {{
        const opt = document.createElement("option");
        opt.value = t.terr_code;
        opt.textContent = `${{t.terr_name}} (${{t.terr_code}}) — ${{t.mio_name}}`;
        terrSelect.appendChild(opt);
      }});
      terrSelect.disabled = false;

      if (targetTerr) {{
        terrSelect.value = targetTerr;
        onTerritorySelected(targetTerr);
      }}
    }}

    function onTerritorySelected(terrCode) {{
      const match = TERRITORIES.find(t => t.terr_code === terrCode);
      const infoBox = document.getElementById("mioInfoBox");
      const btnProceed = document.getElementById("btnLoginProceed");

      if (match) {{
        document.getElementById("dispMioName").textContent = match.mio_name || "Vacant";
        document.getElementById("dispMioCode").textContent = match.mio_code || "N/A";
        document.getElementById("dispAreaCode").textContent = `${{match.terr_name}} (${{match.terr_code}})`;
        document.getElementById("dispRhName").textContent = match.rh_name || "N/A";
        document.getElementById("dispZhName").textContent = match.zh_name || "N/A";

        infoBox.classList.add("active");
        btnProceed.disabled = false;
        currentMio = match;
      }} else {{
        infoBox.classList.remove("active");
        btnProceed.disabled = true;
        currentMio = null;
      }}
    }}

    // Check existing MIO session
    function checkExistingSession() {{
      const saved = localStorage.getItem(LS_MIO);
      if (saved) {{
        try {{
          currentMio = JSON.parse(saved);
          updateSessionBar();
          showScreen("screenDoctorInfo");
        }} catch(e) {{
          currentMio = null;
        }}
      }}
    }}

    function updateSessionBar() {{
      const bar = document.getElementById("sessionBar");
      if (currentMio) {{
        document.getElementById("sessMioName").textContent = currentMio.mio_name;
        document.getElementById("sessTerritory").textContent = currentMio.terr_name;
        bar.style.display = "flex";
      }} else {{
        bar.style.display = "none";
      }}
    }}

    // Screen Switching
    function showScreen(screenId) {{
      document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
      const target = document.getElementById(screenId);
      if (target) {{
        target.classList.add("active");
        window.scrollTo({{ top: 0, behavior: 'smooth' }});

        if (screenId === "screenDoctorInfo") {{
          updateMySurveyCountBadge();
          setTimeout(() => {{
            const dn = document.getElementById("docName");
            if (dn) dn.focus();
          }}, 150);
        }} else if (screenId === "screenLogin") {{
          setTimeout(() => {{
            const si = document.getElementById("searchInput");
            if (si) si.focus();
          }}, 150);
        }}
      }}
    }}

    // Render Questions in Doctor View (CLEAN TEXT - NO ICONS)
    function renderQuestions() {{
      const q1 = activeQuestions.questions[0];
      const q2 = activeQuestions.questions[1];

      document.getElementById("q1TitleEn").textContent = q1.title_en;
      document.getElementById("q2TitleEn").textContent = q2.title_en;

      const q1Container = document.getElementById("q1OptionsContainer");
      const q2Container = document.getElementById("q2OptionsContainer");
      q1Container.innerHTML = "";
      q2Container.innerHTML = "";

      // Options Q1 - Clean text without icons
      q1.options.forEach(opt => {{
        const item = document.createElement("div");
        item.className = "option-item" + (selectedQ1 === opt.code ? " selected" : "");
        item.setAttribute("tabindex", "0");
        item.innerHTML = `
          <div class="option-radio"></div>
          <div class="option-content">
            <div class="option-text-en">${{opt.text_en}}</div>
          </div>
        `;
        const selectOpt1 = () => {{
          selectedQ1 = opt.code;
          q1Container.querySelectorAll(".option-item").forEach(el => el.classList.remove("selected"));
          item.classList.add("selected");
          if (!selectedQ2) {{
            const q2Card = document.getElementById("qCard2");
            if (q2Card) {{
              q2Card.scrollIntoView({{ behavior: "smooth", block: "center" }});
            }}
          }}
        }};
        item.addEventListener("click", selectOpt1);
        item.addEventListener("keydown", (ev) => {{
          if (ev.key === "Enter" || ev.key === " ") {{
            ev.preventDefault();
            selectOpt1();
          }}
        }});
        q1Container.appendChild(item);
      }});

      // Options Q2 - Clean text without icons
      q2.options.forEach(opt => {{
        const item = document.createElement("div");
        item.className = "option-item" + (selectedQ2 === opt.code ? " selected" : "");
        item.setAttribute("tabindex", "0");
        item.innerHTML = `
          <div class="option-radio"></div>
          <div class="option-content">
            <div class="option-text-en">${{opt.text_en}}</div>
          </div>
        `;
        const selectOpt2 = () => {{
          selectedQ2 = opt.code;
          q2Container.querySelectorAll(".option-item").forEach(el => el.classList.remove("selected"));
          item.classList.add("selected");
        }};
        item.addEventListener("click", selectOpt2);
        item.addEventListener("keydown", (ev) => {{
          if (ev.key === "Enter" || ev.key === " ") {{
            ev.preventDefault();
            selectOpt2();
          }}
        }});
        q2Container.appendChild(item);
      }});
    }}

    // Setup All Event Listeners
    function setupEventListeners() {{
      // Zone change
      document.getElementById("zoneSelect").addEventListener("change", (e) => {{
        triggerZoneChange(e.target.value);
      }});

      // Region change
      document.getElementById("regionSelect").addEventListener("change", (e) => {{
        const zone = document.getElementById("zoneSelect").value;
        triggerRegionChange(zone, e.target.value);
      }});

      // Territory change
      document.getElementById("terrSelect").addEventListener("change", (e) => {{
        onTerritorySelected(e.target.value);
      }});

      // Switch Territory / Logout MIO
      document.getElementById("btnSwitchTerritory").addEventListener("click", () => {{
        if (confirm("Are you sure you want to switch territory / MIO?")) {{
          localStorage.removeItem(LS_MIO);
          currentMio = null;
          updateSessionBar();
          resetHierarchySelection();
          clearSearchFeedback();
          const searchInput = document.getElementById("searchInput");
          if (searchInput) searchInput.value = "";
          showScreen("screenLogin");
        }}
      }});

      // Login Proceed (NO PASSWORD REQUIRED)
      document.getElementById("btnLoginProceed").addEventListener("click", () => {{
        if (!currentMio) return;

        localStorage.setItem(LS_MIO, JSON.stringify(currentMio));
        updateSessionBar();
        showScreen("screenDoctorInfo");
        showToast(`✅ Selected: ${{currentMio.terr_name}} (${{currentMio.mio_name}})`);
      }});

      // Strict real-time formatting for RPL ID (digits only, max 6)
      const rplInput = document.getElementById("docRplId");
      rplInput.addEventListener("input", (e) => {{
        e.target.value = e.target.value.replace(/\\D/g, '').slice(0, 6);
      }});

      // Proceed to Doctor's Survey (Validation for Doctor Name & MANDATORY 6-DIGIT RPL ID)
      document.getElementById("btnHandoverDoctor").addEventListener("click", () => {{
        const docName = document.getElementById("docName").value.trim();
        if (!docName) {{
          showToast("⚠️ Please enter Doctor's Full Name.");
          document.getElementById("docName").focus();
          return;
        }}

        const docRplId = document.getElementById("docRplId").value.trim();
        if (!docRplId) {{
          showToast("⚠️ Doctor RPL ID is required.");
          document.getElementById("docRplId").focus();
          return;
        }}

        if (!/^\\d{{6}}$/.test(docRplId)) {{
          showToast("⚠️ Doctor RPL ID must be exactly 6 digits (e.g. 465737).");
          document.getElementById("docRplId").focus();
          return;
        }}

        currentDoctor = {{
          name: docName,
          rpl_id: docRplId
        }};

        document.getElementById("surveyDocWelcomeName").textContent = currentDoctor.name;
        selectedQ1 = null;
        selectedQ2 = null;
        renderQuestions();

        // Switch to Doctor Screen
        showScreen("screenDoctorSurvey");
        showToast("📱 Doctor View Activated!");
      }});

      // Doctor Submits Questionnaire
      document.getElementById("btnSubmitSurvey").addEventListener("click", () => {{
        if (!selectedQ1) {{
          showToast("⚠️ Please answer Question 1 before submitting.");
          document.getElementById("qCard1").scrollIntoView({{ behavior: "smooth" }});
          return;
        }}
        if (!selectedQ2) {{
          showToast("⚠️ Please answer Question 2 before submitting.");
          document.getElementById("qCard2").scrollIntoView({{ behavior: "smooth" }});
          return;
        }}

        // Save Response
        saveSurveyResponse();
        showScreen("screenThankYou");
      }});

      // MIO Next Doctor Button
      document.getElementById("btnMioUnlock").addEventListener("click", () => {{
        // Reset doctor fields for next survey
        document.getElementById("docName").value = "";
        document.getElementById("docRplId").value = "";
        currentDoctor = null;
        selectedQ1 = null;
        selectedQ2 = null;

        showScreen("screenDoctorInfo");
        showToast("Ready for next doctor entry 📝");
      }});

      // Open Hierarchy Reports Modal from Header
      document.getElementById("btnReportsOpen").addEventListener("click", () => {{
        document.getElementById("reportsModal").classList.add("active");
        document.getElementById("tabBtnMio").click();
        const searchInput = document.getElementById("reportMioQuickSearch");
        if (searchInput) {{
          searchInput.value = "";
          searchInput.classList.remove("is-invalid");
        }}
        const feedback = document.getElementById("reportMioSearchFeedback");
        if (feedback) feedback.style.display = "none";

        if (currentMio) {{
          selectReportMioTerritory(currentMio.terr_code);
        }} else {{
          renderMioReport(document.getElementById("reportMioTerrSelect").value);
        }}
      }});

      // Quick View from Step 2 (Doctor Entry Screen)
      document.getElementById("btnQuickViewMyDoctors").addEventListener("click", () => {{
        document.getElementById("reportsModal").classList.add("active");
        document.getElementById("tabBtnMio").click();
        const searchInput = document.getElementById("reportMioQuickSearch");
        if (searchInput) {{
          searchInput.value = "";
          searchInput.classList.remove("is-invalid");
        }}
        const feedback = document.getElementById("reportMioSearchFeedback");
        if (feedback) feedback.style.display = "none";

        if (currentMio) {{
          selectReportMioTerritory(currentMio.terr_code);
        }}
      }});

      // Close Hierarchy Reports Modal
      document.getElementById("btnReportsClose").addEventListener("click", () => {{
        document.getElementById("reportsModal").classList.remove("active");
      }});

      // Export buttons in reports
      document.getElementById("btnExportMioExcel").addEventListener("click", exportMioExcel);
      document.getElementById("btnExportRhExcel").addEventListener("click", exportRhExcel);
      document.getElementById("btnExportZhExcel").addEventListener("click", exportZhExcel);

      // Admin Modal Open
      document.getElementById("btnAdminOpen").addEventListener("click", () => {{
        document.getElementById("adminModal").classList.add("active");
      }});

      // Admin Modal Close
      document.getElementById("btnAdminClose").addEventListener("click", () => {{
        document.getElementById("adminModal").classList.remove("active");
      }});

      // Admin Auth
      document.getElementById("btnAdminAuth").addEventListener("click", () => {{
        const pass = document.getElementById("adminPassInput").value.trim();
        if (pass === "Exium MUPS" || pass === "admin") {{
          isAdminLoggedIn = true;
          document.getElementById("adminLoginBody").style.display = "none";
          document.getElementById("adminDashboardBody").style.display = "flex";
          populateAdminCloudSettings();
          refreshAdminStats();
          loadQuestionEditor();
          initAdminTerritoryExplorer();
          // Silently pull live cloud data upon admin unlock
          pullCloudData(false);
        }} else {{
          showToast("❌ Incorrect Admin Password!");
        }}
      }});



      // Report Live Refresh Button Click
      const btnReportLiveRefresh = document.getElementById("btnReportLiveRefresh");
      if (btnReportLiveRefresh) {{
        btnReportLiveRefresh.addEventListener("click", () => {{
          pullCloudData(true);
        }});
      }}

      // Admin Cloud URL Save
      const btnSaveCloudUrl = document.getElementById("btnSaveCloudUrl");
      if (btnSaveCloudUrl) {{
        btnSaveCloudUrl.addEventListener("click", () => {{
          saveAdminCloudUrl();
        }});
      }}

      // Admin Test Cloud Connection
      const btnTestCloudConn = document.getElementById("btnTestCloudConn");
      if (btnTestCloudConn) {{
        btnTestCloudConn.addEventListener("click", () => {{
          testCloudConnection();
        }});
      }}

      // Admin Pull Live Data
      const btnAdminPullCloud = document.getElementById("btnAdminPullCloud");
      if (btnAdminPullCloud) {{
        btnAdminPullCloud.addEventListener("click", () => {{
          pullCloudData(true);
        }});
      }}

      // Admin Push Local Records
      const btnAdminPushCloud = document.getElementById("btnAdminPushCloud");
      if (btnAdminPushCloud) {{
        btnAdminPushCloud.addEventListener("click", () => {{
          pushAllPendingToCloud(true);
        }});
      }}

      // Add option buttons in Admin
      document.getElementById("btnAddQ1Option").addEventListener("click", () => {{
        addOptionRow("q1AdminOptionsContainer");
      }});
      document.getElementById("btnAddQ2Option").addEventListener("click", () => {{
        addOptionRow("q2AdminOptionsContainer");
      }});

      // Save Edited Questions & Answers
      document.getElementById("btnSaveQuestions").addEventListener("click", () => {{
        const q1Title = document.getElementById("editQ1En").value.trim();
        const q2Title = document.getElementById("editQ2En").value.trim();

        if (!q1Title || !q2Title) {{
          showToast("⚠️ Both Question titles are required.");
          return;
        }}

        // Collect Q1 options
        const q1Opts = collectOptionsFromContainer("q1AdminOptionsContainer");
        if (q1Opts.length < 2) {{
          showToast("⚠️ Question 1 must have at least 2 options.");
          return;
        }}

        // Collect Q2 options
        const q2Opts = collectOptionsFromContainer("q2AdminOptionsContainer");
        if (q2Opts.length < 2) {{
          showToast("⚠️ Question 2 must have at least 2 options.");
          return;
        }}

        activeQuestions.questions[0].title_en = q1Title;
        activeQuestions.questions[0].options = q1Opts;

        activeQuestions.questions[1].title_en = q2Title;
        activeQuestions.questions[1].options = q2Opts;

        localStorage.setItem(LS_QUESTIONS, JSON.stringify(activeQuestions));
        renderQuestions();
        refreshAdminStats();
        loadQuestionEditor();
        showToast("✅ Questions & Options updated successfully!");
      }});

      // Reset to default questions & answers
      document.getElementById("btnResetDefaultQuestions").addEventListener("click", () => {{
        if (confirm("Reset all questions and answer choices to default?")) {{
          activeQuestions = JSON.parse(JSON.stringify(DEFAULT_QUESTIONS));
          localStorage.removeItem(LS_QUESTIONS);
          renderQuestions();
          refreshAdminStats();
          loadQuestionEditor();
          showToast("🔄 Reset to default questions & answers.");
        }}
      }});

      // Export Excel
      document.getElementById("btnExportExcel").addEventListener("click", exportExcelFile);

      // Export CSV
      document.getElementById("btnExportCSV").addEventListener("click", exportCSVFile);

      // Clear All Survey Data (Local Storage & Google Sheet Backend)
      document.getElementById("btnClearData").addEventListener("click", async () => {{
        if (confirm(`⚠️ WARNING: This will permanently delete ALL survey responses from BOTH Local Storage and your connected Google Sheet (including submissions from all field personnel nationwide).\n\nAre you sure you want to proceed?`)) {{
          if (confirm("FINAL CONFIRMATION: This action CANNOT be undone. Delete all survey records everywhere?")) {{
            // 1. Clear local storage
            localStorage.removeItem(LS_SURVEYS);

            // 2. Clear Google Sheet backend
            const targetUrl = cloudApiUrl || DEFAULT_CLOUD_URL;
            if (targetUrl && targetUrl.startsWith("http")) {{
              try {{
                await fetch(targetUrl, {{
                  method: "POST",
                  mode: "no-cors",
                  keepalive: true,
                  headers: {{ "Content-Type": "text/plain;charset=utf-8" }},
                  body: JSON.stringify({{ action: "clear_all" }})
                }});
                console.log("[Cloud] Clear all command dispatched to Google Sheet.");
              }} catch (err) {{
                console.warn("[Cloud Clear Error]:", err);
              }}
            }}

            // 3. Reset UI state & stats
            refreshAdminStats();
            updateMySurveyCountBadge();
            const tbodyDocs = document.getElementById("tbodyAdminDocs");
            if (tbodyDocs) {{
              tbodyDocs.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 14px;">Select or search a territory to inspect submissions</td></tr>';
            }}
            showToast("🗑️ All survey data deleted from Local & Google Sheet.");
          }}
        }}
      }});

      // ==============================================
      // KEYBOARD NAVIGATION / ENTER KEY ADVANCE
      // ==============================================

      // 1. Quick Search Enter key: proceed if valid territory selected, else show message
      const searchInput = document.getElementById("searchInput");
      searchInput.addEventListener("keydown", (e) => {{
        if (e.key === "Enter") {{
          e.preventDefault();
          const btnLoginProceed = document.getElementById("btnLoginProceed");
          if (currentMio && btnLoginProceed && !btnLoginProceed.disabled) {{
            btnLoginProceed.click();
          }} else {{
            const term = searchInput.value.trim();
            if (!term) {{
              showToast("⚠️ Please select a territory first.");
            }} else {{
              showToast("⚠️ Not Found — Please enter a valid code or name.");
            }}
          }}
        }}
      }});

      // 2. Dropdowns Enter key: proceed if selected
      ["zoneSelect", "regionSelect", "terrSelect"].forEach(id => {{
        const el = document.getElementById(id);
        if (el) {{
          el.addEventListener("keydown", (e) => {{
            if (e.key === "Enter") {{
              const btnLoginProceed = document.getElementById("btnLoginProceed");
              if (btnLoginProceed && !btnLoginProceed.disabled) {{
                e.preventDefault();
                btnLoginProceed.click();
              }}
            }}
          }});
        }}
      }});

      // 3. Doctor Name Enter key: advances to RPL ID
      const docName = document.getElementById("docName");
      const docRplId = document.getElementById("docRplId");
      docName.addEventListener("keydown", (e) => {{
        if (e.key === "Enter") {{
          e.preventDefault();
          if (!docName.value.trim()) {{
            showToast("⚠️ Please enter Doctor's Full Name.");
          }} else if (docRplId.value.trim().length === 6) {{
            document.getElementById("btnHandoverDoctor").click();
          }} else {{
            docRplId.focus();
          }}
        }}
      }});

      // 4. Doctor RPL ID Enter key: triggers proceed to Doctor Survey
      docRplId.addEventListener("keydown", (e) => {{
        if (e.key === "Enter") {{
          e.preventDefault();
          document.getElementById("btnHandoverDoctor").click();
        }}
      }});

      // 5. Admin Password Enter key: unlocks admin panel
      document.getElementById("adminPassInput").addEventListener("keydown", (e) => {{
        if (e.key === "Enter") {{
          e.preventDefault();
          document.getElementById("btnAdminAuth").click();
        }}
      }});

      // 6. Global Enter Key Navigation for Screen Transitions
      document.addEventListener("keydown", (e) => {{
        if (e.key !== "Enter") return;

        // If Admin Modal or Reports Modal is open, don't trigger background survey navigation
        const adminModal = document.getElementById("adminModal");
        if (adminModal && adminModal.classList.contains("active")) {{
          return;
        }}
        const reportsModal = document.getElementById("reportsModal");
        if (reportsModal && reportsModal.classList.contains("active")) {{
          return;
        }}

        const activeScreen = document.querySelector(".screen.active");
        if (!activeScreen) return;

        if (activeScreen.id === "screenLogin") {{
          const activeEl = document.activeElement;
          if (activeEl !== searchInput && 
              activeEl !== document.getElementById("zoneSelect") &&
              activeEl !== document.getElementById("regionSelect") &&
              activeEl !== document.getElementById("terrSelect")) {{
            const btnLoginProceed = document.getElementById("btnLoginProceed");
            if (btnLoginProceed && !btnLoginProceed.disabled) {{
              e.preventDefault();
              btnLoginProceed.click();
            }}
          }}
        }} else if (activeScreen.id === "screenDoctorInfo") {{
          const activeEl = document.activeElement;
          if (activeEl !== docName && activeEl !== docRplId) {{
            e.preventDefault();
            document.getElementById("btnHandoverDoctor").click();
          }}
        }} else if (activeScreen.id === "screenDoctorSurvey") {{
          e.preventDefault();
          document.getElementById("btnSubmitSurvey").click();
        }} else if (activeScreen.id === "screenThankYou") {{
          e.preventDefault();
          document.getElementById("btnMioUnlock").click();
        }}
      }});
    }}

    // Load Question and Answer Options Editor in Admin
    function loadQuestionEditor() {{
      const q1 = activeQuestions.questions[0];
      const q2 = activeQuestions.questions[1];

      document.getElementById("editQ1En").value = q1.title_en;
      document.getElementById("editQ2En").value = q2.title_en;

      renderAdminOptions("q1AdminOptionsContainer", q1.options);
      renderAdminOptions("q2AdminOptionsContainer", q2.options);
    }}

    function renderAdminOptions(containerId, options) {{
      const container = document.getElementById(containerId);
      container.innerHTML = "";
      options.forEach((opt, idx) => {{
        const code = String.fromCharCode(65 + idx); // A, B, C...
        const row = document.createElement("div");
        row.className = "admin-opt-row";
        row.innerHTML = `
          <div class="admin-opt-code">${{code}}</div>
          <input type="text" class="form-control admin-opt-text" value="${{escapeHtml(opt.text_en)}}" placeholder="Option text" style="padding: 6px 10px; font-size: 13px;">
          <button type="button" class="btn-opt-del" title="Delete option">✕</button>
        `;
        row.querySelector(".btn-opt-del").addEventListener("click", () => {{
          if (container.querySelectorAll(".admin-opt-row").length <= 2) {{
            showToast("⚠️ Must have at least 2 options.");
            return;
          }}
          row.remove();
          reindexAdminOptions(containerId);
        }});
        container.appendChild(row);
      }});
    }}

    function addOptionRow(containerId) {{
      const container = document.getElementById(containerId);
      const idx = container.querySelectorAll(".admin-opt-row").length;
      if (idx >= 8) {{
        showToast("⚠️ Maximum 8 options allowed.");
        return;
      }}
      const code = String.fromCharCode(65 + idx);
      const row = document.createElement("div");
      row.className = "admin-opt-row";
      row.innerHTML = `
        <div class="admin-opt-code">${{code}}</div>
        <input type="text" class="form-control admin-opt-text" value="" placeholder="New option text..." style="padding: 6px 10px; font-size: 13px;">
        <button type="button" class="btn-opt-del" title="Delete option">✕</button>
      `;
      row.querySelector(".btn-opt-del").addEventListener("click", () => {{
        if (container.querySelectorAll(".admin-opt-row").length <= 2) {{
          showToast("⚠️ Must have at least 2 options.");
          return;
        }}
        row.remove();
        reindexAdminOptions(containerId);
      }});
      container.appendChild(row);
      row.querySelector(".admin-opt-text").focus();
    }}

    function reindexAdminOptions(containerId) {{
      const container = document.getElementById(containerId);
      container.querySelectorAll(".admin-opt-row").forEach((row, idx) => {{
        row.querySelector(".admin-opt-code").textContent = String.fromCharCode(65 + idx);
      }});
    }}

    function collectOptionsFromContainer(containerId) {{
      const container = document.getElementById(containerId);
      const options = [];
      container.querySelectorAll(".admin-opt-row").forEach((row, idx) => {{
        const text = row.querySelector(".admin-opt-text").value.trim();
        if (text) {{
          options.push({{
            code: String.fromCharCode(65 + idx),
            text_en: text
          }});
        }}
      }});
      return options;
    }}

    function escapeHtml(text) {{
      return String(text || "").replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }}

    // Save Survey Response to LocalStorage
    function saveSurveyResponse() {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");

      const q1Config = activeQuestions.questions[0];
      const q2Config = activeQuestions.questions[1];
      const q1SelectedObj = q1Config.options.find(o => o.code === selectedQ1);
      const q2SelectedObj = q2Config.options.find(o => o.code === selectedQ2);

      const record = {{
        id: "SURV_" + Date.now() + "_" + Math.floor(Math.random()*1000),
        timestamp: new Date().toISOString(),
        formatted_time: new Date().toLocaleString(),
        zone: currentMio ? currentMio.zone_name : "",
        region: currentMio ? currentMio.region_name : "",
        sap_region_code: currentMio ? currentMio.sap_reg : "",
        regional_head: currentMio ? currentMio.rh_name : "",
        zonal_head: currentMio ? currentMio.zh_name : "",
        sap_territory_code: currentMio ? currentMio.terr_code : "",
        territory: currentMio ? currentMio.terr_name : "",
        sap_mio_code: currentMio ? currentMio.mio_code : "",
        mio_name: currentMio ? currentMio.mio_name : "",
        doctor_name: currentDoctor ? currentDoctor.name : "",
        doctor_rpl_id: currentDoctor ? currentDoctor.rpl_id : "",
        q1_code: selectedQ1,
        q1_answer_en: q1SelectedObj ? q1SelectedObj.text_en : "",
        q2_code: selectedQ2,
        q2_answer_en: q2SelectedObj ? q2SelectedObj.text_en : "",
        synced: false
      }};

      surveys.push(record);
      localStorage.setItem(LS_SURVEYS, JSON.stringify(surveys));
      updateMySurveyCountBadge();
      console.log("Survey saved locally:", record);
      // Immediately push to Google Cloud Sheet
      pushSurveyToCloud(record);
    }}

    // Update Doctor count badge on Step 2
    function updateMySurveyCountBadge() {{
      const badge = document.getElementById("mySurveyCountBadge");
      if (!badge) return;
      if (!currentMio) {{
        badge.textContent = "0";
        return;
      }}
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const count = surveys.filter(s => s.sap_territory_code === currentMio.terr_code).length;
      badge.textContent = count;
    }}

    function populateReportMioTerrSelect(terrs, selectedTerrCode = "") {{
      const mioSelect = document.getElementById("reportMioTerrSelect");
      mioSelect.innerHTML = '<option value="">-- Choose Territory / MIO --</option>';
      const sortedTerrs = [...terrs].sort((a, b) => (a.terr_name || "").localeCompare(b.terr_name || ""));
      sortedTerrs.forEach(t => {{
        const opt = document.createElement("option");
        opt.value = t.terr_code;
        opt.textContent = `${{t.terr_name}} (${{t.terr_code}}) — ${{t.mio_name}}`;
        if (t.terr_code === selectedTerrCode) opt.selected = true;
        mioSelect.appendChild(opt);
      }});
      if (selectedTerrCode) mioSelect.value = selectedTerrCode;
    }}

    function selectReportMioTerritory(terrCode) {{
      const match = TERRITORIES.find(t => t.terr_code === terrCode);
      if (!match) return;

      const zoneFilter = document.getElementById("reportMioZoneFilter");
      const regFilter = document.getElementById("reportMioRegionFilter");

      zoneFilter.value = match.zone_name;

      const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === match.zone_name).map(t => t.region_name))].filter(Boolean).sort();
      regFilter.innerHTML = '<option value="">-- All Regions in Zone --</option>';
      regions.forEach(r => {{
        const opt = document.createElement("option");
        opt.value = r;
        opt.textContent = r;
        regFilter.appendChild(opt);
      }});
      regFilter.disabled = false;
      regFilter.value = match.region_name;

      const regTerrs = TERRITORIES.filter(t => t.zone_name === match.zone_name && t.region_name === match.region_name);
      populateReportMioTerrSelect(regTerrs, match.terr_code);

      renderMioReport(match.terr_code);
    }}

    // Initialize Hierarchy Reports Selectors and Tabs
    function initReportHierarchy() {{
      // 1. Populate MIO Filters (Zone, Region, Territory & Quick Search)
      const mioZoneFilter = document.getElementById("reportMioZoneFilter");
      const mioRegFilter = document.getElementById("reportMioRegionFilter");
      const mioSelect = document.getElementById("reportMioTerrSelect");
      const mioSearchInput = document.getElementById("reportMioQuickSearch");
      const mioSearchFeedback = document.getElementById("reportMioSearchFeedback");

      const uniqueZones = [...new Set(TERRITORIES.map(t => t.zone_name))].filter(Boolean).sort();
      mioZoneFilter.innerHTML = '<option value="">-- All Zones (Filter) --</option>';
      uniqueZones.forEach(z => {{
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        mioZoneFilter.appendChild(opt);
      }});

      populateReportMioTerrSelect(TERRITORIES);

      mioZoneFilter.addEventListener("change", (e) => {{
        const zone = e.target.value;
        if (mioSearchInput) {{
          mioSearchInput.value = "";
          mioSearchInput.classList.remove("is-invalid");
        }}
        if (mioSearchFeedback) mioSearchFeedback.style.display = "none";

        if (!zone) {{
          mioRegFilter.innerHTML = '<option value="">-- First Select Zone --</option>';
          mioRegFilter.disabled = true;
          populateReportMioTerrSelect(TERRITORIES);
          renderMioReport("");
          return;
        }}

        const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === zone).map(t => t.region_name))].filter(Boolean).sort();
        mioRegFilter.innerHTML = '<option value="">-- All Regions in Zone --</option>';
        regions.forEach(r => {{
          const opt = document.createElement("option");
          opt.value = r;
          opt.textContent = r;
          mioRegFilter.appendChild(opt);
        }});
        mioRegFilter.disabled = false;

        const zoneTerrs = TERRITORIES.filter(t => t.zone_name === zone);
        populateReportMioTerrSelect(zoneTerrs);
        renderMioReport("");
      }});

      mioRegFilter.addEventListener("change", (e) => {{
        const zone = mioZoneFilter.value;
        const reg = e.target.value;
        if (mioSearchInput) {{
          mioSearchInput.value = "";
          mioSearchInput.classList.remove("is-invalid");
        }}
        if (mioSearchFeedback) mioSearchFeedback.style.display = "none";

        if (!reg) {{
          const zoneTerrs = zone ? TERRITORIES.filter(t => t.zone_name === zone) : TERRITORIES;
          populateReportMioTerrSelect(zoneTerrs);
          renderMioReport("");
          return;
        }}

        const regTerrs = TERRITORIES.filter(t => (!zone || t.zone_name === zone) && t.region_name === reg);
        populateReportMioTerrSelect(regTerrs);
        renderMioReport("");
      }});

      mioSelect.addEventListener("change", (e) => {{
        const val = e.target.value;
        if (val) {{
          if (mioSearchInput) {{
            mioSearchInput.value = "";
            mioSearchInput.classList.remove("is-invalid");
          }}
          if (mioSearchFeedback) mioSearchFeedback.style.display = "none";
        }}
        renderMioReport(val);
      }});

      mioSearchInput.addEventListener("input", (e) => {{
        const term = e.target.value.trim().toLowerCase();

        if (!term) {{
          mioSearchInput.classList.remove("is-invalid");
          if (mioSearchFeedback) mioSearchFeedback.style.display = "none";
          if (currentMio) {{
            selectReportMioTerritory(currentMio.terr_code);
          }} else {{
            mioZoneFilter.value = "";
            mioRegFilter.innerHTML = '<option value="">-- First Select Zone --</option>';
            mioRegFilter.disabled = true;
            populateReportMioTerrSelect(TERRITORIES);
            renderMioReport("");
          }}
          return;
        }}

        let match = TERRITORIES.find(t => 
          (t.mio_code && t.mio_code.toLowerCase() === term) ||
          (t.terr_code && t.terr_code.toLowerCase() === term)
        );

        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().startsWith(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().startsWith(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().startsWith(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().startsWith(term))
          );
        }}

        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().includes(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().includes(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().includes(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().includes(term))
          );
        }}

        if (match) {{
          mioSearchInput.classList.remove("is-invalid");
          if (mioSearchFeedback) mioSearchFeedback.style.display = "none";
          selectReportMioTerritory(match.terr_code);
        }} else {{
          mioSearchInput.classList.add("is-invalid");
          if (mioSearchFeedback) mioSearchFeedback.style.display = "flex";
          renderMioReport("");
        }}
      }});

      // 2. Populate Zonal Head Zone Selector
      const zhZoneSelect = document.getElementById("reportZhZoneSelect");
      zhZoneSelect.innerHTML = '<option value="">-- Select Zone (35 Zones) --</option>';
      uniqueZones.forEach(z => {{
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        zhZoneSelect.appendChild(opt);
      }});

      // 3. Populate Regional Head Zone & Region Selectors
      const rhZoneSelect = document.getElementById("reportRhZoneSelect");
      rhZoneSelect.innerHTML = '<option value="">-- Select Zone --</option>';
      uniqueZones.forEach(z => {{
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        rhZoneSelect.appendChild(opt);
      }});

      const rhRegSelect = document.getElementById("reportRhRegionSelect");
      rhRegSelect.innerHTML = '<option value="">-- First Select Zone --</option>';
      rhRegSelect.disabled = true;

      // Event Listeners for report selectors
      zhZoneSelect.addEventListener("change", (e) => {{
        renderZhReport(e.target.value);
      }});

      rhZoneSelect.addEventListener("change", (e) => {{
        const zone = e.target.value;
        rhRegSelect.innerHTML = '<option value="">-- Select Region --</option>';
        if (!zone) {{
          rhRegSelect.disabled = true;
          renderRhReport("");
          return;
        }}
        const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === zone).map(t => t.region_name))].filter(Boolean).sort();
        regions.forEach(r => {{
          const opt = document.createElement("option");
          opt.value = r;
          opt.textContent = r;
          rhRegSelect.appendChild(opt);
        }});
        rhRegSelect.disabled = false;
        renderRhReport("");
      }});

      rhRegSelect.addEventListener("change", (e) => {{
        renderRhReport(e.target.value);
      }});

      // Tab Switching
      document.querySelectorAll(".report-tab-btn").forEach(btn => {{
        btn.addEventListener("click", () => {{
          document.querySelectorAll(".report-tab-btn").forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          const targetTab = btn.getAttribute("data-tab");
          document.querySelectorAll("#reportsModal .tab-content").forEach(tc => tc.style.display = "none");
          const activeContent = document.getElementById(targetTab);
          if (activeContent) activeContent.style.display = "block";
        }});
      }});
    }}

    function renderMioReport(terrCode) {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const filtered = terrCode ? surveys.filter(s => s.sap_territory_code === terrCode) : [];
      const terrObj = TERRITORIES.find(t => t.terr_code === terrCode);

      document.getElementById("mioStatTotalDocs").textContent = filtered.length;
      document.getElementById("mioStatTerrName").textContent = terrObj ? `${{terrObj.terr_name}} (${{terrObj.mio_name}})` : "-";

      const tbody = document.getElementById("tbodyMioDocs");
      tbody.innerHTML = "";

      if (filtered.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 18px;">No doctor surveys recorded yet in this territory</td></tr>';
        return;
      }}

      filtered.forEach((s, idx) => {{
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${{idx + 1}}</td>
          <td><strong>${{escapeHtml(s.doctor_name)}}</strong></td>
          <td><code>${{escapeHtml(s.doctor_rpl_id)}}</code></td>
          <td>${{escapeHtml(s.q1_answer_en || s.q1_code || "-")}}</td>
          <td>${{escapeHtml(s.q2_answer_en || s.q2_code || "-")}}</td>
          <td>${{escapeHtml(s.formatted_time || s.timestamp || "-")}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderRhReport(regName) {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const regTerrs = regName ? TERRITORIES.filter(t => t.region_name === regName) : [];
      const rhName = regTerrs[0]?.rh_name || "N/A";
      document.getElementById("dispReportRhName").textContent = regName ? `${{rhName}} (${{regName}})` : "-";

      const filteredSurveys = regName ? surveys.filter(s => s.region === regName) : [];
      const completedTerrs = regTerrs.filter(t => filteredSurveys.some(s => s.sap_territory_code === t.terr_code));
      const totalTerrs = regTerrs.length;
      const coveragePct = totalTerrs > 0 ? ((completedTerrs.length / totalTerrs) * 100).toFixed(1) + "%" : "0%";

      document.getElementById("rhStatTotalDocs").textContent = filteredSurveys.length;
      document.getElementById("rhStatCompletedTerrs").textContent = completedTerrs.length;
      document.getElementById("rhStatTotalTerrs").textContent = totalTerrs;
      document.getElementById("rhStatCoverage").textContent = coveragePct;

      // Render Territory Breakdown
      const tbodyTerrs = document.getElementById("tbodyRhTerritories");
      tbodyTerrs.innerHTML = "";
      if (regTerrs.length === 0) {{
        tbodyTerrs.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 14px;">Select a region to view territory progress</td></tr>';
      }} else {{
        regTerrs.forEach(t => {{
          const docCount = filteredSurveys.filter(s => s.sap_territory_code === t.terr_code).length;
          const statusBadge = docCount > 0 
            ? '<span class="badge-status badge-completed">Completed</span>' 
            : '<span class="badge-status badge-pending">Pending</span>';
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td><strong>${{escapeHtml(t.terr_name)}}</strong> (${{escapeHtml(t.terr_code)}})</td>
            <td>${{escapeHtml(t.mio_name)}}</td>
            <td>${{statusBadge}}</td>
            <td style="text-align: center; font-weight: 700;">${{docCount}}</td>
          `;
          tbodyTerrs.appendChild(tr);
        }});
      }}

      // Render Doctors List in Region
      const tbodyDocs = document.getElementById("tbodyRhDoctors");
      tbodyDocs.innerHTML = "";
      if (filteredSurveys.length === 0) {{
        tbodyDocs.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 14px;">No doctor surveys recorded in this region yet</td></tr>';
      }} else {{
        filteredSurveys.forEach((s, idx) => {{
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${{idx + 1}}</td>
            <td><strong>${{escapeHtml(s.doctor_name)}}</strong></td>
            <td><code>${{escapeHtml(s.doctor_rpl_id)}}</code></td>
            <td>${{escapeHtml(s.territory)}}</td>
            <td>${{escapeHtml(s.mio_name)}}</td>
            <td>${{escapeHtml(s.q1_answer_en || s.q1_code || "-")}}</td>
            <td>${{escapeHtml(s.q2_answer_en || s.q2_code || "-")}}</td>
            <td>${{escapeHtml(s.formatted_time || s.timestamp || "-")}}</td>
          `;
          tbodyDocs.appendChild(tr);
        }});
      }}
    }}

    function renderZhReport(zoneName) {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const zoneTerrs = zoneName ? TERRITORIES.filter(t => t.zone_name === zoneName) : [];
      const zhName = zoneTerrs[0]?.zh_name || "N/A";
      document.getElementById("dispReportZhName").textContent = zoneName ? `${{zhName}} (${{zoneName}})` : "-";

      const filteredSurveys = zoneName ? surveys.filter(s => s.zone === zoneName) : [];
      const completedTerrs = zoneTerrs.filter(t => filteredSurveys.some(s => s.sap_territory_code === t.terr_code));
      const totalTerrs = zoneTerrs.length;
      const coveragePct = totalTerrs > 0 ? ((completedTerrs.length / totalTerrs) * 100).toFixed(1) + "%" : "0%";

      document.getElementById("zhStatTotalDocs").textContent = filteredSurveys.length;
      document.getElementById("zhStatCompletedTerrs").textContent = completedTerrs.length;
      document.getElementById("zhStatTotalTerrs").textContent = totalTerrs;
      document.getElementById("zhStatCoverage").textContent = coveragePct;

      // Render Regional Breakdown
      const tbodyRegs = document.getElementById("tbodyZhRegions");
      tbodyRegs.innerHTML = "";
      if (zoneTerrs.length === 0) {{
        tbodyRegs.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 14px;">Select a zone to view regional performance</td></tr>';
      }} else {{
        const distinctRegs = [...new Set(zoneTerrs.map(t => t.region_name))].filter(Boolean).sort();
        distinctRegs.forEach(r => {{
          const rTerrs = zoneTerrs.filter(t => t.region_name === r);
          const rRhName = rTerrs[0]?.rh_name || "N/A";
          const rDocs = filteredSurveys.filter(s => s.region === r).length;
          const rComp = rTerrs.filter(t => filteredSurveys.some(s => s.sap_territory_code === t.terr_code)).length;
          const rCov = rTerrs.length > 0 ? ((rComp / rTerrs.length) * 100).toFixed(0) + "%" : "0%";

          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td><strong>${{escapeHtml(r)}}</strong></td>
            <td>${{escapeHtml(rRhName)}}</td>
            <td style="text-align: center;">${{rTerrs.length}}</td>
            <td style="text-align: center;">${{rComp}}</td>
            <td style="text-align: center; font-weight: 700;">${{rDocs}}</td>
            <td style="text-align: center;"><span class="badge-status ${{rComp === rTerrs.length ? 'badge-completed' : 'badge-pending'}}">${{rCov}}</span></td>
          `;
          tbodyRegs.appendChild(tr);
        }});
      }}

      // Render Doctor Records in Zone
      const tbodyDocs = document.getElementById("tbodyZhDoctors");
      tbodyDocs.innerHTML = "";
      if (filteredSurveys.length === 0) {{
        tbodyDocs.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 14px;">No doctor surveys recorded in this zone yet</td></tr>';
      }} else {{
        filteredSurveys.forEach((s, idx) => {{
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${{idx + 1}}</td>
            <td><strong>${{escapeHtml(s.doctor_name)}}</strong></td>
            <td><code>${{escapeHtml(s.doctor_rpl_id)}}</code></td>
            <td>${{escapeHtml(s.region)}}</td>
            <td>${{escapeHtml(s.territory)}}</td>
            <td>${{escapeHtml(s.mio_name)}}</td>
            <td>${{escapeHtml(s.q1_answer_en || s.q1_code || "-")}}</td>
            <td>${{escapeHtml(s.q2_answer_en || s.q2_code || "-")}}</td>
            <td>${{escapeHtml(s.formatted_time || s.timestamp || "-")}}</td>
          `;
          tbodyDocs.appendChild(tr);
        }});
      }}
    }}

    function exportMioExcel() {{
      const terrCode = document.getElementById("reportMioTerrSelect").value;
      if (!terrCode) {{
        showToast("⚠️ Please select a territory first.");
        return;
      }}
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const filtered = surveys.filter(s => s.sap_territory_code === terrCode);
      if (filtered.length === 0) {{
        showToast("⚠️ No doctor surveys recorded in this territory yet.");
        return;
      }}
      const rows = filtered.map((s, idx) => ({{
        "SL": idx + 1,
        "Timestamp": s.formatted_time || s.timestamp,
        "Territory Code": s.sap_territory_code,
        "Territory": s.territory,
        "MIO Code": s.sap_mio_code,
        "MIO Name": s.mio_name,
        "Doctor Name": s.doctor_name,
        "Doctor RPL ID": s.doctor_rpl_id,
        "Q1 Code": s.q1_code,
        "Q1 Answer": s.q1_answer_en,
        "Q2 Code": s.q2_code,
        "Q2 Answer": s.q2_answer_en
      }}));
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(rows);
      XLSX.utils.book_append_sheet(wb, ws, "MIO_Doctors");
      XLSX.writeFile(wb, `Exium_Doctor_Survey_Territory_${{terrCode}}.xlsx`);
      showToast("✅ Territory Excel report downloaded!");
    }}

    function exportRhExcel() {{
      const regName = document.getElementById("reportRhRegionSelect").value;
      if (!regName) {{
        showToast("⚠️ Please select a region first.");
        return;
      }}
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const filtered = surveys.filter(s => s.region === regName);
      if (filtered.length === 0) {{
        showToast("⚠️ No doctor surveys recorded in this region yet.");
        return;
      }}
      const rows = filtered.map((s, idx) => ({{
        "SL": idx + 1,
        "Timestamp": s.formatted_time || s.timestamp,
        "Region": s.region,
        "Regional Head": s.regional_head,
        "Territory Code": s.sap_territory_code,
        "Territory": s.territory,
        "MIO Code": s.sap_mio_code,
        "MIO Name": s.mio_name,
        "Doctor Name": s.doctor_name,
        "Doctor RPL ID": s.doctor_rpl_id,
        "Q1 Answer": s.q1_answer_en,
        "Q2 Answer": s.q2_answer_en
      }}));
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(rows);
      XLSX.utils.book_append_sheet(wb, ws, "Region_Doctors");
      XLSX.writeFile(wb, `Exium_Doctor_Survey_Region_${{regName.replace(/[^a-zA-Z0-9]/g, '_')}}.xlsx`);
      showToast("✅ Region Excel report downloaded!");
    }}

    function exportZhExcel() {{
      const zoneName = document.getElementById("reportZhZoneSelect").value;
      if (!zoneName) {{
        showToast("⚠️ Please select a zone first.");
        return;
      }}
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const filtered = surveys.filter(s => s.zone === zoneName);
      if (filtered.length === 0) {{
        showToast("⚠️ No doctor surveys recorded in this zone yet.");
        return;
      }}
      const rows = filtered.map((s, idx) => ({{
        "SL": idx + 1,
        "Timestamp": s.formatted_time || s.timestamp,
        "Zone": s.zone,
        "Zonal Head": s.zonal_head,
        "Region": s.region,
        "Territory": s.territory,
        "MIO Name": s.mio_name,
        "Doctor Name": s.doctor_name,
        "Doctor RPL ID": s.doctor_rpl_id,
        "Q1 Answer": s.q1_answer_en,
        "Q2 Answer": s.q2_answer_en
      }}));
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(rows);
      XLSX.utils.book_append_sheet(wb, ws, "Zone_Doctors");
      XLSX.writeFile(wb, `Exium_Doctor_Survey_Zone_${{zoneName.replace(/[^a-zA-Z0-9]/g, '_')}}.xlsx`);
      showToast("✅ Zone Excel report downloaded!");
    }}

    // Refresh Admin Statistics
    function refreshAdminStats() {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const total = surveys.length;
      const terrSet = new Set(surveys.map(s => s.sap_territory_code));

      document.getElementById("statTotalSurveys").textContent = total;
      document.getElementById("statUniqueTerritories").textContent = `${{terrSet.size}} / ${{TERRITORIES.length}}`;
      document.getElementById("statSyncCount").textContent = surveys.filter(s => s.synced).length;
      document.getElementById("statPendingCount").textContent = surveys.filter(s => !s.synced).length;

      // Question 1 Breakdown
      const q1Counts = {{}};
      const q1Config = activeQuestions.questions[0];
      q1Config.options.forEach(o => q1Counts[o.code] = 0);
      surveys.forEach(s => {{
        if (q1Counts[s.q1_code] !== undefined) q1Counts[s.q1_code]++;
      }});

      const q1Container = document.getElementById("q1AnalyticsContainer");
      q1Container.innerHTML = "";
      q1Config.options.forEach(opt => {{
        const count = q1Counts[opt.code] || 0;
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        q1Container.innerHTML += `
          <div class="chart-bar-item">
            <div class="chart-bar-header">
              <span>${{opt.code}}. ${{opt.text_en}}</span>
              <span>${{count}} (${{pct}}%)</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${{pct}}%;"></div>
            </div>
          </div>
        `;
      }});

      // Question 2 Breakdown
      const q2Counts = {{}};
      const q2Config = activeQuestions.questions[1];
      q2Config.options.forEach(o => q2Counts[o.code] = 0);
      surveys.forEach(s => {{
        if (q2Counts[s.q2_code] !== undefined) q2Counts[s.q2_code]++;
      }});

      const q2Container = document.getElementById("q2AnalyticsContainer");
      q2Container.innerHTML = "";
      q2Config.options.forEach(opt => {{
        const count = q2Counts[opt.code] || 0;
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        q2Container.innerHTML += `
          <div class="chart-bar-item">
            <div class="chart-bar-header">
              <span>${{opt.code}}. ${{opt.text_en}}</span>
              <span>${{count}} (${{pct}}%)</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${{pct}}%;"></div>
            </div>
          </div>
        `;
      }});

      const currentAdminTerr = document.getElementById("adminTerrSelect") ? document.getElementById("adminTerrSelect").value : "";
      if (currentAdminTerr) {{
        renderAdminTerrReport(currentAdminTerr);
      }}
    }}

    // Admin Territory Explorer Functions
    function populateAdminTerrSelect(terrs, selectedTerrCode = "") {{
      const terrSelect = document.getElementById("adminTerrSelect");
      if (!terrSelect) return;
      terrSelect.innerHTML = '<option value="">-- Choose Territory / MIO --</option>';
      const sorted = [...terrs].sort((a, b) => (a.terr_name || "").localeCompare(b.terr_name || ""));
      sorted.forEach(t => {{
        const opt = document.createElement("option");
        opt.value = t.terr_code;
        opt.textContent = `${{t.terr_name}} (${{t.terr_code}}) — ${{t.mio_name}}`;
        if (t.terr_code === selectedTerrCode) opt.selected = true;
        terrSelect.appendChild(opt);
      }});
      if (selectedTerrCode) terrSelect.value = selectedTerrCode;
    }}

    function selectAdminTerritory(terrCode) {{
      const match = TERRITORIES.find(t => t.terr_code === terrCode);
      if (!match) return;

      const zoneSelect = document.getElementById("adminZoneSelect");
      const regSelect = document.getElementById("adminRegionSelect");

      if (zoneSelect) zoneSelect.value = match.zone_name;

      if (regSelect) {{
        const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === match.zone_name).map(t => t.region_name))].filter(Boolean).sort();
        regSelect.innerHTML = '<option value="">-- All Regions in Zone --</option>';
        regions.forEach(r => {{
          const opt = document.createElement("option");
          opt.value = r;
          opt.textContent = r;
          regSelect.appendChild(opt);
        }});
        regSelect.disabled = false;
        regSelect.value = match.region_name;
      }}

      const regTerrs = TERRITORIES.filter(t => t.zone_name === match.zone_name && t.region_name === match.region_name);
      populateAdminTerrSelect(regTerrs, match.terr_code);

      renderAdminTerrReport(match.terr_code);
    }}

    function renderAdminTerrReport(terrCode) {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const filtered = terrCode ? surveys.filter(s => s.sap_territory_code === terrCode) : [];
      const terrObj = TERRITORIES.find(t => t.terr_code === terrCode);

      const summaryBox = document.getElementById("adminTerrSummaryBox");
      const statusBadge = document.getElementById("adminTerrStatusBadge");
      const dispStatus = document.getElementById("adminDispStatusBadge");
      const tbody = document.getElementById("tbodyAdminDocs");

      if (!terrCode || !terrObj) {{
        if (summaryBox) summaryBox.style.display = "none";
        if (statusBadge) {{
          statusBadge.textContent = "Select Territory";
          statusBadge.className = "badge badge-primary";
          statusBadge.style.background = "";
          statusBadge.style.color = "";
        }}
        if (tbody) {{
          tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 14px;">Select or search a territory to inspect submissions</td></tr>';
        }}
        return;
      }}

      const hasSubmitted = filtered.length > 0;
      if (summaryBox) summaryBox.style.display = "block";

      document.getElementById("adminDispTerrName").textContent = `${{terrObj.terr_name}} (${{terrObj.terr_code}})`;
      document.getElementById("adminDispMioName").textContent = terrObj.mio_name || "Vacant";
      document.getElementById("adminDispMioCode").textContent = terrObj.mio_code || "N/A";
      document.getElementById("adminDispRegName").textContent = `${{terrObj.region_name}} (${{terrObj.zone_name}})`;
      document.getElementById("adminDispDocCount").textContent = filtered.length;

      if (hasSubmitted) {{
        if (statusBadge) {{
          statusBadge.textContent = `Completed (${{filtered.length}} Doctors)`;
          statusBadge.className = "badge badge-accent";
          statusBadge.style.background = "";
          statusBadge.style.color = "";
        }}
        if (dispStatus) {{
          dispStatus.textContent = "Submitted / Completed";
          dispStatus.className = "badge-status badge-completed";
        }}
      }} else {{
        if (statusBadge) {{
          statusBadge.textContent = "Pending (0 Doctors)";
          statusBadge.className = "badge";
          statusBadge.style.background = "#fef3c7";
          statusBadge.style.color = "#92400e";
        }}
        if (dispStatus) {{
          dispStatus.textContent = "No Submission (Pending)";
          dispStatus.className = "badge-status badge-pending";
        }}
      }}

      if (tbody) {{
        tbody.innerHTML = "";
        if (filtered.length === 0) {{
          tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--danger); font-weight: 600; padding: 16px;">⚠️ No doctor surveys submitted yet by this territory</td></tr>';
        }} else {{
          filtered.forEach((s, idx) => {{
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>${{idx + 1}}</td>
              <td><strong>${{escapeHtml(s.doctor_name)}}</strong></td>
              <td><code>${{escapeHtml(s.doctor_rpl_id)}}</code></td>
              <td>${{escapeHtml(s.q1_answer_en || s.q1_code || "-")}}</td>
              <td>${{escapeHtml(s.q2_answer_en || s.q2_code || "-")}}</td>
              <td>${{escapeHtml(s.formatted_time || s.timestamp || "-")}}</td>
            `;
            tbody.appendChild(tr);
          }});
        }}
      }}
    }}

    function initAdminTerritoryExplorer() {{
      const zoneSelect = document.getElementById("adminZoneSelect");
      const regSelect = document.getElementById("adminRegionSelect");
      const terrSelect = document.getElementById("adminTerrSelect");
      const searchInput = document.getElementById("adminQuickSearch");
      const feedback = document.getElementById("adminSearchFeedback");

      if (!zoneSelect) return;

      const adminZones = [...new Set(TERRITORIES.map(t => t.zone_name))].filter(Boolean).sort();
      zoneSelect.innerHTML = '<option value="">-- All Zones (Filter) --</option>';
      adminZones.forEach(z => {{
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        zoneSelect.appendChild(opt);
      }});

      populateAdminTerrSelect(TERRITORIES);

      zoneSelect.addEventListener("change", (e) => {{
        const zone = e.target.value;
        if (searchInput) {{
          searchInput.value = "";
          searchInput.classList.remove("is-invalid");
        }}
        if (feedback) feedback.style.display = "none";

        if (!zone) {{
          regSelect.innerHTML = '<option value="">-- First Select Zone --</option>';
          regSelect.disabled = true;
          populateAdminTerrSelect(TERRITORIES);
          renderAdminTerrReport("");
          return;
        }}

        const regions = [...new Set(TERRITORIES.filter(t => t.zone_name === zone).map(t => t.region_name))].filter(Boolean).sort();
        regSelect.innerHTML = '<option value="">-- All Regions in Zone --</option>';
        regions.forEach(r => {{
          const opt = document.createElement("option");
          opt.value = r;
          opt.textContent = r;
          regSelect.appendChild(opt);
        }});
        regSelect.disabled = false;

        const zoneTerrs = TERRITORIES.filter(t => t.zone_name === zone);
        populateAdminTerrSelect(zoneTerrs);
        renderAdminTerrReport("");
      }});

      regSelect.addEventListener("change", (e) => {{
        const zone = zoneSelect.value;
        const reg = e.target.value;
        if (searchInput) {{
          searchInput.value = "";
          searchInput.classList.remove("is-invalid");
        }}
        if (feedback) feedback.style.display = "none";

        if (!reg) {{
          const zoneTerrs = zone ? TERRITORIES.filter(t => t.zone_name === zone) : TERRITORIES;
          populateAdminTerrSelect(zoneTerrs);
          renderAdminTerrReport("");
          return;
        }}

        const regTerrs = TERRITORIES.filter(t => (!zone || t.zone_name === zone) && t.region_name === reg);
        populateAdminTerrSelect(regTerrs);
        renderAdminTerrReport("");
      }});

      terrSelect.addEventListener("change", (e) => {{
        const val = e.target.value;
        if (val) {{
          if (searchInput) {{
            searchInput.value = "";
            searchInput.classList.remove("is-invalid");
          }}
          if (feedback) feedback.style.display = "none";
        }}
        renderAdminTerrReport(val);
      }});

      searchInput.addEventListener("input", (e) => {{
        const term = e.target.value.trim().toLowerCase();

        if (!term) {{
          searchInput.classList.remove("is-invalid");
          if (feedback) feedback.style.display = "none";
          zoneSelect.value = "";
          regSelect.innerHTML = '<option value="">-- First Select Zone --</option>';
          regSelect.disabled = true;
          populateAdminTerrSelect(TERRITORIES);
          renderAdminTerrReport("");
          return;
        }}

        let match = TERRITORIES.find(t => 
          (t.mio_code && t.mio_code.toLowerCase() === term) ||
          (t.terr_code && t.terr_code.toLowerCase() === term)
        );

        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().startsWith(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().startsWith(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().startsWith(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().startsWith(term))
          );
        }}

        if (!match) {{
          match = TERRITORIES.find(t => 
            (t.mio_code && t.mio_code.toLowerCase().includes(term)) ||
            (t.terr_code && t.terr_code.toLowerCase().includes(term)) ||
            (t.terr_name && t.terr_name.toLowerCase().includes(term)) ||
            (t.mio_name && t.mio_name.toLowerCase().includes(term))
          );
        }}

        if (match) {{
          searchInput.classList.remove("is-invalid");
          if (feedback) feedback.style.display = "none";
          selectAdminTerritory(match.terr_code);
        }} else {{
          searchInput.classList.add("is-invalid");
          if (feedback) feedback.style.display = "flex";
          renderAdminTerrReport("");
        }}
      }});
    }}

    // Export Master Excel File
    function exportExcelFile() {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      if (surveys.length === 0) {{
        showToast("⚠️ No survey responses recorded yet to export.");
        return;
      }}

      // Format Rows
      const rows = surveys.map((s, idx) => ({{
        "SL": idx + 1,
        "Timestamp": s.formatted_time,
        "Zone": s.zone,
        "Zonal Head": s.zonal_head,
        "Region": s.region,
        "Regional Head": s.regional_head,
        "SAP Territory Code": s.sap_territory_code,
        "Territory Name": s.territory,
        "SAP MIO Code": s.sap_mio_code,
        "MIO / Sr. MIO Name": s.mio_name,
        "Doctor Name": s.doctor_name,
        "Doctor RPL ID": s.doctor_rpl_id,
        "Q1 Code": s.q1_code,
        "Q1 Answer": s.q1_answer_en,
        "Q2 Code": s.q2_code,
        "Q2 Answer": s.q2_answer_en
      }}));

      const ws = XLSX.utils.json_to_sheet(rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Survey Responses");
      XLSX.writeFile(wb, "Exium_Gyne_Doctor_Survey_Responses_2026.xlsx");
      showToast("📥 Excel downloaded successfully!");
    }}

    // Export CSV
    function exportCSVFile() {{
      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      if (surveys.length === 0) {{
        showToast("⚠️ No survey responses recorded yet to export.");
        return;
      }}

      const headers = [
        "SL", "Timestamp", "Zone", "Region", "TerritoryCode", "TerritoryName",
        "SAPMIOCode", "MIOName", "DoctorName", "DoctorRPLID",
        "Q1Code", "Q1Answer", "Q2Code", "Q2Answer"
      ];

      const csvRows = [headers.join(",")];
      surveys.forEach((s, idx) => {{
        const row = [
          idx + 1,
          `"${{s.formatted_time}}"`,
          `"${{s.zone}}"`,
          `"${{s.region}}"`,
          `"${{s.sap_territory_code}}"`,
          `"${{s.territory}}"`,
          `"${{s.sap_mio_code}}"`,
          `"${{s.mio_name}}"`,
          `"${{s.doctor_name}}"`,
          `"${{s.doctor_rpl_id}}"`,
          `"${{s.q1_code}}"`,
          `"${{s.q1_answer_en}}"`,
          `"${{s.q2_code}}"`,
          `"${{s.q2_answer_en}}"`
        ];
        csvRows.push(row.join(","));
      }});

      const blob = new Blob([csvRows.join("\\n")], {{ type: "text/csv;charset=utf-8;" }});
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "Exium_Gyne_Doctor_Survey_Responses.csv";
      link.click();
      showToast("📥 CSV downloaded successfully!");
    }}

    // Toast Helper
    function showToast(msg) {{
      const toast = document.getElementById("appToast");
      toast.textContent = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 3200);
    }}

    // ==============================================
    // REAL-TIME GOOGLE SHEET CLOUD SYNC ENGINE
    // ==============================================

    function initCloudSync() {{
      populateAdminCloudSettings();

      // Fetch consolidated surveys once on startup
      const activeUrl = cloudApiUrl || DEFAULT_CLOUD_URL;
      if (activeUrl && activeUrl.startsWith("http")) {{
        setTimeout(() => {{
          pullCloudData(false);
        }}, 500);
      }}
    }}

    function populateAdminCloudSettings() {{
      const input = document.getElementById("adminCloudUrlInput");
      if (input) {{
        input.value = cloudApiUrl || DEFAULT_CLOUD_URL;
      }}
      updateAdminCloudPill();
    }}

    function updateAdminCloudPill() {{
      const pill = document.getElementById("adminCloudStatusPill");
      if (!pill) return;
      const url = cloudApiUrl || DEFAULT_CLOUD_URL;
      if (!url) {{
        pill.textContent = "Not Configured";
        pill.style.background = "#fef3c7";
        pill.style.color = "#92400e";
        pill.style.borderColor = "#fde68a";
      }} else {{
        pill.textContent = "Connected (Live)";
        pill.style.background = "#dcfce7";
        pill.style.color = "#15803d";
        pill.style.borderColor = "#86efac";
      }}
    }}

    function updateCloudStatusBadge() {{}}

    function saveAdminCloudUrl() {{
      const input = document.getElementById("adminCloudUrlInput");
      const url = input ? input.value.trim() : "";
      cloudApiUrl = url;
      localStorage.setItem(LS_CLOUD_URL, url);
      updateAdminCloudPill();
      updateCloudStatusBadge();

      const msg = document.getElementById("adminCloudMsg");
      if (msg) {{
        msg.style.display = "block";
        msg.style.background = "#ecfdf5";
        msg.style.color = "#065f46";
        msg.style.border = "1px solid #a7f3d0";
        msg.textContent = "✅ Google Apps Script URL saved successfully. Testing connection...";
      }}
      testCloudConnection();
    }}

    async function testCloudConnection() {{
      const msg = document.getElementById("adminCloudMsg");
      if (!cloudApiUrl || !cloudApiUrl.startsWith("http")) {{
        if (msg) {{
          msg.style.display = "block";
          msg.style.background = "#fffbeb";
          msg.style.color = "#92400e";
          msg.style.border = "1px solid #fde68a";
          msg.textContent = "⚠️ Please enter a valid Google Apps Script Web App URL (starts with https://).";
        }}
        showToast("⚠️ Please enter a valid Google Apps Script URL first.");
        return;
      }}

      if (msg) {{
        msg.style.display = "block";
        msg.style.background = "#f0f9ff";
        msg.style.color = "#0369a1";
        msg.style.border = "1px solid #bae6fd";
        msg.textContent = "⏳ Testing connection to Google Sheet...";
      }}

      try {{
        const sep = cloudApiUrl.includes("?") ? "&" : "?";
        const res = await fetch(`${{cloudApiUrl}}${{sep}}action=ping&_t=${{Date.now()}}`);
        const json = await res.json();
        if (json && (json.status === "ok" || json.total_records !== undefined)) {{
          if (msg) {{
            msg.style.background = "#ecfdf5";
            msg.style.color = "#065f46";
            msg.style.border = "1px solid #a7f3d0";
            msg.textContent = `✅ Connected to Google Sheet! Total records in sheet: ${{json.total_records || 0}}`;
          }}
          showToast("✅ Google Sheet Connected successfully!");
        }} else {{
          throw new Error("Unexpected response structure");
        }}
      }} catch (err) {{
        console.warn("[Cloud Test Error]:", err);
        if (msg) {{
          msg.style.background = "#fef2f2";
          msg.style.color = "#991b1b";
          msg.style.border = "1px solid #fecaca";
          msg.textContent = "⚠️ Connection test completed with CORS or notice. Note: Mobile background submissions will still push via no-cors.";
        }}
        showToast("⚠️ Note: Ensure Web App is deployed with Access: 'Anyone'.");
      }}
    }}

    // Push survey to Google Cloud Sheet once upon doctor submission
    async function pushSurveyToCloud(record) {{
      const targetUrl = cloudApiUrl || DEFAULT_CLOUD_URL;
      if (!targetUrl || !targetUrl.startsWith("http") || !navigator.onLine) {{
        console.log("[Cloud] Offline. Saved locally.");
        return;
      }}

      try {{
        await fetch(targetUrl, {{
          method: "POST",
          mode: "no-cors",
          keepalive: true,
          headers: {{ "Content-Type": "text/plain;charset=utf-8" }},
          body: JSON.stringify(record)
        }});

        console.log("[Cloud] Single survey dispatched to Google Sheet:", record.id);
      }} catch (err) {{
        console.warn("[Cloud Push Error]:", err);
      }}
    }}

    // Push all unsynced surveys to Google Sheet
    async function pushAllPendingToCloud(showFeedback = false) {{
      const targetUrl = cloudApiUrl || DEFAULT_CLOUD_URL;
      if (!targetUrl || !targetUrl.startsWith("http")) {{
        if (showFeedback) showToast("⚠️ Configure Google Apps Script URL in Admin first.");
        return;
      }}

      const surveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
      const unsynced = surveys.filter(s => !s.synced);

      if (unsynced.length === 0) {{
        if (showFeedback) showToast("ℹ️ All records are already synced with the cloud!");
        updateCloudStatusBadge();
        return;
      }}

      if (showFeedback) showToast(`⬆️ Pushing ${{unsynced.length}} local records to Google Sheet...`);


      try {{
        await fetch(cloudApiUrl, {{
          method: "POST",
          mode: "no-cors",
          headers: {{ "Content-Type": "text/plain;charset=utf-8" }},
          body: JSON.stringify({{ records: unsynced }})
        }});

        // Mark all as synced
        surveys.forEach(s => s.synced = true);
        localStorage.setItem(LS_SURVEYS, JSON.stringify(surveys));

        if (showFeedback) showToast(`✅ Successfully pushed ${{unsynced.length}} records to Google Sheet!`);
      }} catch (err) {{
        console.warn("[Cloud Batch Push Error]:", err);
        if (showFeedback) showToast("❌ Network error pushing to Google Sheet. Will retry when connection stabilizes.");
      }} finally {{
        updateCloudStatusBadge();
        if (isAdminLoggedIn) refreshAdminStats();
      }}
    }}

    // Pull all survey records from Google Sheet and merge
    async function pullCloudData(showFeedback = false) {{
      const targetUrl = cloudApiUrl || DEFAULT_CLOUD_URL;
      if (!targetUrl || !targetUrl.startsWith("http")) {{
        if (showFeedback) showToast("⚠️ Configure Google Apps Script URL in Admin first.");
        return;
      }}

      if (showFeedback) showToast("🔄 Fetching latest surveys from Google Sheet...");


      try {{
        const sep = cloudApiUrl.includes("?") ? "&" : "?";
        const res = await fetch(`${{cloudApiUrl}}${{sep}}action=get_all&_t=${{Date.now()}}`);
        if (!res.ok) throw new Error("HTTP " + res.status);
        const cloudRecords = await res.json();

        if (Array.isArray(cloudRecords)) {{
          const localSurveys = JSON.parse(localStorage.getItem(LS_SURVEYS) || "[]");
          const localMap = new Map();

          // Index local by id or RPL ID + territory
          localSurveys.forEach(s => {{
            const key = s.id || (s.doctor_rpl_id + "_" + s.sap_territory_code);
            localMap.set(key, s);
          }});

          let newAdded = 0;
          cloudRecords.forEach(c => {{
            const key = c.id || (c.doctor_rpl_id + "_" + c.sap_territory_code);
            if (!localMap.has(key)) {{
              localMap.set(key, {{ ...c, synced: true }});
              newAdded++;
            }}
          }});

          const merged = Array.from(localMap.values());
          // Sort newest first
          merged.sort((a, b) => new Date(b.timestamp || b.formatted_time || 0) - new Date(a.timestamp || a.formatted_time || 0));
          localStorage.setItem(LS_SURVEYS, JSON.stringify(merged));

          updateMySurveyCountBadge();
          if (isAdminLoggedIn) refreshAdminStats();

          // Refresh Survey Submission Report if active
          const reportsModal = document.getElementById("reportsModal");
          if (reportsModal && reportsModal.classList.contains("active")) {{
            const activeTabBtn = document.querySelector(".report-tab-btn.active");
            const activeTab = activeTabBtn ? activeTabBtn.dataset.tab : "tabMioReport";
            if (activeTab === "tabMioReport") {{
              const terrSelect = document.getElementById("reportMioTerrSelect");
              if (terrSelect && terrSelect.value) renderMioReport(terrSelect.value);
            }} else if (activeTab === "tabRhReport") {{
              const rhSelect = document.getElementById("reportRhRegionSelect");
              if (rhSelect && rhSelect.value) renderRhReport(rhSelect.value);
            }} else if (activeTab === "tabZhReport") {{
              const zhSelect = document.getElementById("reportZhZoneSelect");
              if (zhSelect && zhSelect.value) renderZhReport(zhSelect.value);
            }}
          }}

          if (showFeedback) {{
            showToast(`✅ Cloud Sync Complete! ${{newAdded}} new records merged (${{merged.length}} total).`);
          }} else if (newAdded > 0) {{
            showToast(`🔔 ${{newAdded}} new survey response(s) synced from field!`);
          }}
        }}
      }} catch (err) {{
        console.warn("[Cloud Pull Error]:", err);
        if (showFeedback) {{
          showToast("⚠️ Could not read from Google Sheet. Check permissions ('Anyone') or URL.");
        }}
      }} finally {{
        updateCloudStatusBadge();
      }}
    }}
  </script>
</body>
</html>
"""

    out_index = os.path.join(folder, "index.html")
    with open(out_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated:", out_index)

    out_portal = os.path.join(folder, "Survey_Gyne_Doctor_Portal.html")
    with open(out_portal, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated:", out_portal)

if __name__ == '__main__':
    build()
