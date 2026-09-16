/**
 * Google Apps Script for Exium MUPS - GERD and Pregnancy Survey 2026
 * 
 * Updates in this version (5 Questions Support):
 * 1. Target Tab: Writes directly into "Survey Responses" sheet tab.
 * 2. 5 Survey Questions (22 Columns):
 *    - Q1: Trimester of GERD occurrence
 *    - Q2: Most common GERD symptom
 *    - Q3: Lifestyle modification resolution rate
 *    - Q4: First-choice medication
 *    - Q5: Preferred PPI molecule
 * 3. Server-Side Strict Deduplication: Checks Doctor RPL ID & Territory Code.
 * 4. Single-Submit Integrity: Appends once upon doctor submission.
 * 5. Clear All Data (Admin): Allows Admin to wipe all response rows.
 * 
 * How to update in Google Drive:
 * 1. Open your Google Sheet: "Exium_Gyne_Doctor_Survey_Master_2026".
 * 2. Open Extensions > Apps Script.
 * 3. Replace all code in Code.gs with this code.
 * 4. Click Deploy > Manage deployments > Click the Pencil (Edit) icon.
 * 5. Change Version to: "New version", and click Deploy.
 */

var HEADERS_22 = [
  "Timestamp", "Zone", "Zonal Head", "Region", "Regional Head", 
  "SAP Territory Code", "Territory Name", "SAP MIO Code", "MIO / Sr. MIO Name", 
  "Doctor Full Name", "Doctor RPL ID", 
  "Q1 Code", "Q1 Answer (Trimester)", 
  "Q2 Code", "Q2 Answer (GERD Symptom)", 
  "Q3 Code", "Q3 Answer (Lifestyle Resolution)", 
  "Q4 Code", "Q4 Answer (First Choice Medicine)", 
  "Q5 Code", "Q5 Answer (Preferred PPI Molecule)", 
  "Survey Record ID"
];

function getTargetSheet(ss) {
  var sheet = ss.getSheetByName("Survey Responses") || ss.getSheetByName("Survey_Responses");
  if (!sheet) {
    sheet = ss.insertSheet("Survey Responses");
    sheet.appendRow(HEADERS_22);
    sheet.getRange(1, 1, 1, HEADERS_22.length).setBackground("#0284c7").setFontColor("#ffffff").setFontWeight("bold");
    sheet.setFrozenRows(1);
  } else if (sheet.getLastColumn() < HEADERS_22.length) {
    sheet.getRange(1, 1, 1, HEADERS_22.length).setValues([HEADERS_22]).setBackground("#0284c7").setFontColor("#ffffff").setFontWeight("bold");
  }
  return sheet;
}

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = getTargetSheet(ss);

    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "No POST payload received."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var data = JSON.parse(e.postData.contents);

    // ADMIN ACTION: Clear All Data from Google Sheet
    if (data && (data.action === "clear_all" || data.action === "reset_all")) {
      var lastRow = sheet.getLastRow();
      var lastCol = Math.max(sheet.getLastColumn(), HEADERS_22.length);
      if (lastRow > 1) {
        sheet.getRange(2, 1, lastRow - 1, lastCol).clearContent();
      }
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        message: "All survey responses cleared successfully from Google Sheet."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var records = Array.isArray(data) ? data : (data.records ? data.records : [data]);

    // Build map of existing IDs in the sheet to PREVENT ANY DUPLICATE
    var existingIds = {};
    var lastRow = sheet.getLastRow();
    var lastCol = Math.max(sheet.getLastColumn(), HEADERS_22.length);
    if (lastRow > 1) {
      var existingData = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();
      for (var k = 0; k < existingData.length; k++) {
        var rowTerr = String(existingData[k][5] || "").trim();  // col 6: SAP Territory Code
        var rowDocRpl = String(existingData[k][10] || "").trim(); // col 11: Doctor RPL ID
        var rowSurveyId = String(existingData[k][existingData[k].length - 1] || "").trim(); // last col: Survey Record ID
        
        if (rowSurveyId) existingIds[rowSurveyId] = true;
        if (rowDocRpl && rowTerr) existingIds[rowDocRpl + "_" + rowTerr] = true;
      }
    }

    var rowsToAdd = [];
    for (var i = 0; i < records.length; i++) {
      var r = records[i];
      if (!r || (!r.doctor_name && !r.doctor_rpl_id && !r.id)) continue;

      var surveyId = String(r.id || "").trim();
      var docRpl = String(r.doctor_rpl_id || "").trim();
      var terrCode = String(r.sap_territory_code || "").trim();
      var dedupKey = (docRpl && terrCode) ? (docRpl + "_" + terrCode) : "";

      // DEDUPLICATION: If this doctor survey already exists, SKIP IT
      if (surveyId && existingIds[surveyId]) {
        continue;
      }
      if (dedupKey && existingIds[dedupKey]) {
        continue;
      }

      // Mark as seen
      if (surveyId) existingIds[surveyId] = true;
      if (dedupKey) existingIds[dedupKey] = true;

      // 22 Columns (5 Questions)
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
        r.q1_code || "",
        r.q1_answer_en || "",
        r.q2_code || "",
        r.q2_answer_en || "",
        r.q3_code || "",
        r.q3_answer_en || "",
        r.q4_code || "",
        r.q4_answer_en || "",
        r.q5_code || "",
        r.q5_answer_en || "",
        surveyId || ("SURV_" + Date.now() + "_" + Math.floor(Math.random()*10000))
      ]);
    }

    if (rowsToAdd.length > 0) {
      sheet.getRange(sheet.getLastRow() + 1, 1, rowsToAdd.length, HEADERS_22.length).setValues(rowsToAdd);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      appended: rowsToAdd.length,
      total_rows: Math.max(0, sheet.getLastRow() - 1),
      message: "Data processed with strict deduplication."
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
    var sheet = getTargetSheet(ss);

    // ADMIN ACTION: Clear All Data via GET
    if (e && e.parameter && (e.parameter.action === "clear_all" || e.parameter.action === "reset_all")) {
      var lastRow = sheet.getLastRow();
      var lastCol = Math.max(sheet.getLastColumn(), HEADERS_22.length);
      if (lastRow > 1) {
        sheet.getRange(2, 1, lastRow - 1, lastCol).clearContent();
      }
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        message: "All survey responses cleared successfully from Google Sheet."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    if (e && e.parameter && e.parameter.action === "ping") {
      var count = sheet ? Math.max(0, sheet.getLastRow() - 1) : 0;
      return ContentService.createTextOutput(JSON.stringify({
        status: "ok",
        app: "Exium GERD and Pregnancy Survey Backend (5 Questions)",
        sheet_name: sheet.getName(),
        total_records: count
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var values = sheet.getDataRange().getValues();
    if (values.length <= 1) {
      return ContentService.createTextOutput(JSON.stringify([])).setMimeType(ContentService.MimeType.JSON);
    }

    var result = [];
    for (var r = 1; r < values.length; r++) {
      var row = values[r];
      var is22Col = row.length >= 22;
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
        q1_code: String(row[11] || ""),
        q1_answer_en: String(row[12] || ""),
        q2_code: String(row[13] || ""),
        q2_answer_en: String(row[14] || ""),
        q3_code: is22Col ? String(row[15] || "") : "",
        q3_answer_en: is22Col ? String(row[16] || "") : "",
        q4_code: is22Col ? String(row[17] || "") : "",
        q4_answer_en: is22Col ? String(row[18] || "") : "",
        q5_code: is22Col ? String(row[19] || "") : "",
        q5_answer_en: is22Col ? String(row[20] || "") : "",
        id: String(row[row.length - 1] || ("REC_" + r)),
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
