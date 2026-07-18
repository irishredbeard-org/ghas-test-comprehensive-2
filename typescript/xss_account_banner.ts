// INTENTIONAL VULNERABILITY: DOM XSS (CWE-79 / js/xss - Medium)
// DUPLICATE_GROUP: ts-xss-001
// This file exists for CodeQL SAST baseline testing only.
function xss_account_banner(req: { query: Record<string, string | undefined> }): void {
  const value = req.query.message ?? '';
  // VULN: request input is written to the DOM without escaping.
  document.getElementById('output')!.innerHTML = value;
}

export { xss_account_banner };
