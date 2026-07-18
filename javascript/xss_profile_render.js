// INTENTIONAL VULNERABILITY: Cross-Site Scripting (CWE-79 / js/xss - Medium)
// DUPLICATE_GROUP: js-xss-001
// This file exists for CodeQL SAST baseline testing only.
function xss_profile_render(req) {
  const value = req.query.message || '';
  // VULN: request input is written to the DOM without escaping.
  document.getElementById('output').innerHTML = value;
}

module.exports = xss_profile_render;
