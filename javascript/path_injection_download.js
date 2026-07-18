// INTENTIONAL VULNERABILITY: Path Injection (CWE-22 / js/path-injection - High)
// DUPLICATE_GROUP: js-path-001
// This file exists for CodeQL SAST baseline testing only.
const fs = require('fs');
const path = require('path');

function path_injection_download(req, res) {
  const requested = req.query.file || '';
  // VULN: request input controls the filesystem path.
  const target = path.join('/var/app/data', requested);
  res.send(fs.readFileSync(target, 'utf8'));
}

module.exports = path_injection_download;
