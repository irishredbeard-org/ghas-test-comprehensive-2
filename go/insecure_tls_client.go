// INTENTIONAL VULNERABILITY: Insecure TLS (CWE-295 / go/insecure-tls - High)
// DUPLICATE_GROUP: go-tls-001
// This file exists for CodeQL SAST baseline testing only.
package main

import (
	"crypto/tls"
	"net/http"
)

func InsecureTlsClient() *http.Client {
	// VULN: certificate verification is disabled.
	transport := &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}
	return &http.Client{Transport: transport}
}
