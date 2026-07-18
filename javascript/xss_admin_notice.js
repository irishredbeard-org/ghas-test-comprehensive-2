// INTENTIONAL VULNERABILITY: Cross-Site Scripting (CWE-79 / js/xss - Medium)
// DUPLICATE_GROUP: js-xss-002
// This file exists for CodeQL SAST baseline testing only.
function xss_admin_notice(req) {
  const value = req.query.notice || '';
  // VULN: request input is written to the DOM without escaping.
  document.getElementById('admin-notice').innerHTML = value;
}

module.exports = xss_admin_notice;
