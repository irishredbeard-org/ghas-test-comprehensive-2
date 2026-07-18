// INTENTIONAL VULNERABILITY: Open Redirect (CWE-601 / go/unvalidated-url-redirection - High)
// DUPLICATE_GROUP: go-redirect-002
// This file exists for CodeQL SAST baseline testing only.
package main

import "net/http"

func OpenRedirectSupport(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("target")
	// VULN: request input controls the redirect destination.
	http.Redirect(w, r, target, http.StatusFound)
}
