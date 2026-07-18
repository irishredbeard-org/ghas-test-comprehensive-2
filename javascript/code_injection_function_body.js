// INTENTIONAL VULNERABILITY: Code Injection (CWE-95 / js/code-injection - Critical)
// DUPLICATE_GROUP: js-code-001
// This file exists for CodeQL SAST baseline testing only.
function code_injection_function_body(req, res) {
  const expression = req.query.expression || '';
  // VULN: user input becomes executable JavaScript.
  const runner = new Function('context', expression);
  res.json({ result: runner({ user: req.user }) });
}

module.exports = code_injection_function_body;
