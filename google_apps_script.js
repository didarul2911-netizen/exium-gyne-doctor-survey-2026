/**
 * Google Apps Script for Exium MUPS - GERD and Pregnancy Survey 2026
 * 
 * Instructions:
 * 1. Create a Google Sheet named "Exium_Gyne_Doctor_Survey_2026" (or any name you prefer).
 * 2. Open Extensions > Apps Script.
 * 3. Replace all code in Code.gs with this entire script.
 * 4. Click Deploy > New Deployment.
 *    - Click the gear icon next to "Select type" and choose "Web app".
 *    - Description: Exium Survey Real-Time Sync v1
 *    - Execute as: "Me" (your email)
 *    - Who has access: "Anyone" (allows MIO field force phones to sync)
 * 5. Click "Deploy", authorize permissions when prompted, and copy the Web App URL.
 * 6. In your Survey Portal Admin Panel, paste this Web App URL.
 */

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Survey_Responses");
    if (!sheet) {
      sheet = ss.insertSheet("Survey_Responses");
      sheet.appendRow([
        "Timestamp", "Zone", "Zonal Head", "Region", "Regional Head", 
        "SAP Territory Code", "Territory Name", "SAP MIO Code", "MIO Name", 
        "Doctor Name", "Doctor RPL ID", "Speciality", "Chamber/Hospital", "Doctor Phone", 
        "Q1 Code", "Q1 Answer", "Q2 Code", "Q2 Answer", "Survey ID"
      ]);
      sheet.getRange(1, 1, 1, 19).setBackground("#0284c7").setFontColor("#ffffff").setFontWeight("bold");
      sheet.setFrozenRows(1);
    }

    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "No POST payload received."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var data = JSON.parse(e.postData.contents);
    var records = Array.isArray(data) ? data : (data.records ? data.records : [data]);
    var rowsToAdd = [];

    for (var i = 0; i < records.length; i++) {
      var r = records[i];
      if (!r || (!r.doctor_name && !r.doctor_rpl_id && !r.id)) continue;

      rowsToAdd.push([
        r.formatted_time || r.timestamp || new Date().toLocaleString(),
        r.zone || "",
        r.zonal_head || "",
        r.region || "",
        r.regional_head || "",
        r.sap_territory_code || "",
        r.territory || "",
        r.sap_mio_code || "",
        r.mio_name || "",
        r.doctor_name || "",
        r.doctor_rpl_id || "",
        r.doctor_speciality || "",
        r.doctor_chamber || "",
        r.doctor_phone || "",
        r.q1_code || "",
        r.q1_answer_en || "",
        r.q2_code || "",
        r.q2_answer_en || "",
        r.id || ("SURV_" + Date.now() + "_" + Math.floor(Math.random()*10000))
      ]);
    }

    if (rowsToAdd.length > 0) {
      sheet.getRange(sheet.getLastRow() + 1, 1, rowsToAdd.length, 19).setValues(rowsToAdd);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      count: rowsToAdd.length,
      total_rows: Math.max(0, sheet.getLastRow() - 1),
      message: "Data appended successfully to Google Sheet."
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Survey_Responses");
    
    if (e && e.parameter && e.parameter.action === "ping") {
      var count = sheet ? Math.max(0, sheet.getLastRow() - 1) : 0;
      return ContentService.createTextOutput(JSON.stringify({
        status: "ok",
        app: "Exium GERD and Pregnancy Survey Backend",
        timestamp: new Date().toISOString(),
        total_records: count
      })).setMimeType(ContentService.MimeType.JSON);
    }

    if (!sheet) {
      return ContentService.createTextOutput(JSON.stringify([])).setMimeType(ContentService.MimeType.JSON);
    }

    var values = sheet.getDataRange().getValues();
    if (values.length <= 1) {
      return ContentService.createTextOutput(JSON.stringify([])).setMimeType(ContentService.MimeType.JSON);
    }

    var result = [];
    for (var r = 1; r < values.length; r++) {
      var row = values[r];
      var obj = {
        formatted_time: String(row[0] || ""),
        timestamp: String(row[0] || ""),
        zone: String(row[1] || ""),
        zonal_head: String(row[2] || ""),
        region: String(row[3] || ""),
        regional_head: String(row[4] || ""),
        sap_territory_code: String(row[5] || ""),
        territory: String(row[6] || ""),
        sap_mio_code: String(row[7] || ""),
        mio_name: String(row[8] || ""),
        doctor_name: String(row[9] || ""),
        doctor_rpl_id: String(row[10] || ""),
        doctor_speciality: String(row[11] || ""),
        doctor_chamber: String(row[12] || ""),
        doctor_phone: String(row[13] || ""),
        q1_code: String(row[14] || ""),
        q1_answer_en: String(row[15] || ""),
        q2_code: String(row[16] || ""),
        q2_answer_en: String(row[17] || ""),
        id: String(row[18] || ("REC_" + r)),
        synced: true
      };
      result.push(obj);
    }

    return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}