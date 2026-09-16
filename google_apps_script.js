/**
 * Google Apps Script for Exium MUPS - GERD and Pregnancy Survey 2026
 * 
 * Updates in this version:
 * 1. Target Tab: Writes directly into the existing "Survey Responses" sheet tab (with space).
 * 2. Clean Columns: Removed Speciality, Chamber/Hospital, Doctor Phone (strictly 16 columns).
 * 3. Server-Side Strict Deduplication: Checks existing Doctor RPL ID & Survey ID to prevent duplicate rows.
 * 4. Single-Submit Integrity: Appends once and only once upon doctor submission.
 * 5. Clear All Data (Admin): Allows Admin to permanently wipe all response rows (keeping header intact).
 * 
 * How to update in Google Drive:
 * 1. Open your Google Sheet: "Exium_Gyne_Doctor_Survey_Master_2026".
 * 2. Open Extensions > Apps Script.
 * 3. Replace all code in Code.gs with this code.
 * 4. Click Deploy > Manage deployments > Click the Pencil (Edit) icon.
 * 5. Change Version to: "New version", and click Deploy.
 */

function getTargetSheet(ss) {
  var sheet = ss.getSheetByName("Survey Responses") || ss.getSheetByName("Survey_Responses");
  if (!sheet) {
    sheet = ss.insertSheet("Survey Responses");
    sheet.appendRow([
      "Timestamp", "Zone", "Zonal Head", "Region", "Regional Head", 
      "SAP Territory Code", "Territory Name", "SAP MIO Code", "MIO / Sr. MIO Name", 
      "Doctor Full Name", "Doctor RPL ID", 
      "Q1 Code", "Q1 Answer (Trimester)", "Q2 Code", "Q2 Answer (GERD Symptom)", "Survey Record ID"
    ]);
    sheet.getRange(1, 1, 1, 16).setBackground("#0284c7").setFontColor("#ffffff").setFontWeight("bold");
    sheet.setFrozenRows(1);
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
      if (lastRow > 1) {
        sheet.getRange(2, 1, lastRow - 1, 16).clearContent();
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
    if (lastRow > 1) {
      var existingData = sheet.getRange(2, 1, lastRow - 1, 16).getValues();
      for (var k = 0; k < existingData.length; k++) {
        var rowTerr = String(existingData[k][5] || "").trim();  // col 6: SAP Territory Code
        var rowDocRpl = String(existingData[k][10] || "").trim(); // col 11: Doctor RPL ID
        var rowSurveyId = String(existingData[k][15] || "").trim(); // col 16: Survey Record ID
        
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

      // Clean 16 Columns (NO Speciality, NO Chamber/Hospital, NO Doctor Phone)
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
        surveyId || ("SURV_" + Date.now() + "_" + Math.floor(Math.random()*10000))
      ]);
    }

    if (rowsToAdd.length > 0) {
      sheet.getRange(sheet.getLastRow() + 1, 1, rowsToAdd.length, 16).setValues(rowsToAdd);
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
      if (lastRow > 1) {
        sheet.getRange(2, 1, lastRow - 1, 16).clearContent();
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
        app: "Exium GERD and Pregnancy Survey Backend",
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
        id: String(row[15] || ("REC_" + r)),
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