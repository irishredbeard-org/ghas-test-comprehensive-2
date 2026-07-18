// INTENTIONAL VULNERABILITY: Path Injection (CWE-22 / js/path-injection - High)
// DUPLICATE_GROUP: ts-path-002
// This file exists for CodeQL SAST baseline testing only.
import * as fs from 'fs';
import * as path from 'path';

function path_injection_snapshot(req: { query: Record<string, string | undefined> }): string {
  const requested = req.query.file ?? '';
  // VULN: request input controls the filesystem path.
  const target = path.join('/var/app/snapshots', requested);
  return fs.readFileSync(target, 'utf8');
}

export { path_injection_snapshot };
