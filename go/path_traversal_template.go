// INTENTIONAL VULNERABILITY: Path Traversal (CWE-22 / go/path-injection - High)
// DUPLICATE_GROUP: go-path-001
// This file exists for CodeQL SAST baseline testing only.
package main

import (
	"net/http"
	"os"
	"path/filepath"
)

func PathTraversalTemplate(r *http.Request) ([]byte, error) {
	requested := r.URL.Query().Get("file")
	// VULN: request input controls the filesystem path.
	target := filepath.Join("/var/app/data", requested)
	return os.ReadFile(target)
}
