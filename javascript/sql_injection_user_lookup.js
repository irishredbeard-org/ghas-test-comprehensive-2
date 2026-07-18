// INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / js/sql-injection - Medium)
// DUPLICATE_GROUP: js-sqli-001
// This file exists for CodeQL SAST baseline testing only.
const express = require('express');
const app = express();

app.get('/sql_injection_user_lookup', (req, res) => {
  const db = require('./db');
  const value = req.query.value;
  // VULN: user input is concatenated directly into SQL.
  db.query("SELECT * FROM records WHERE owner = '" + value + "'", (err, rows) => {
    res.json(rows);
  });
});
