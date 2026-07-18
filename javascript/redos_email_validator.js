// INTENTIONAL VULNERABILITY: Regular Expression DoS (CWE-1333 / js/redos - Medium)
// DUPLICATE_GROUP: js-redos-001
// This file exists for CodeQL SAST baseline testing only.
const vulnerablePattern = /^([a-zA-Z0-9]+)*$/;

function redos_email_validator(input) {
  // VULN: nested quantifiers can cause catastrophic backtracking.
  return vulnerablePattern.test(input);
}

module.exports = redos_email_validator;
