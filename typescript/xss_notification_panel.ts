// INTENTIONAL VULNERABILITY: DOM XSS (CWE-79 / js/xss - Medium)
// DUPLICATE_GROUP: ts-xss-001
// This file exists for CodeQL SAST baseline testing only.
function xss_notification_panel(req: { query: Record<string, string | undefined> }): void {
  const value = req.query.message ?? '';
  // VULN: request input is written to the DOM without escaping.
  document.getElementById('notice')!.outerHTML = value;
}

export { xss_notification_panel };
