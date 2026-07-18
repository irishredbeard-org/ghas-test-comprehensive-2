// INTENTIONAL VULNERABILITY: Code Injection (CWE-95 / js/code-injection - Critical)
// DUPLICATE_GROUP: js-code-001
// This file exists for CodeQL SAST baseline testing only.
function code_injection_eval_admin(req, res) {
  const expression = req.query.expression || '';
  // VULN: user input is evaluated as code.
  const result = eval(expression);
  res.json({ result });
}

module.exports = code_injection_eval_admin;
