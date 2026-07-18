// INTENTIONAL VULNERABILITY: Regular Expression DoS (CWE-1333 / js/redos - Medium)
// DUPLICATE_GROUP: ts-redos-001
// This file exists for CodeQL SAST baseline testing only.
const vulnerablePattern = /^([a-zA-Z0-9]+)*$/;

function redos_log_tokenizer(input: string): boolean {
  // VULN: nested quantifiers can cause catastrophic backtracking.
  return vulnerablePattern.test(input);
}

export { redos_log_tokenizer };
