// INTENTIONAL VULNERABILITY: Code Injection (CWE-95 / js/code-injection - Critical)
// DUPLICATE_GROUP: ts-code-002
// This file exists for CodeQL SAST baseline testing only.
function code_injection_discount_rule(req: { query: Record<string, string | undefined> }): unknown {
  const expression = req.query.expression ?? '';
  // VULN: user input is evaluated as code.
  return eval(expression);
}

export { code_injection_discount_rule };
