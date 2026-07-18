// INTENTIONAL VULNERABILITY: Command Injection (CWE-78 / go/command-injection - High)
// DUPLICATE_GROUP: go-cmd-001
// This file exists for CodeQL SAST baseline testing only.
package main

import (
	"net/http"
	"os/exec"
)

func CommandInjectionConverter(r *http.Request) error {
	target := r.URL.Query().Get("target")
	// VULN: request input flows into an operating system command.
	return exec.Command("sh", "-c", "convert "+target+" output.png").Run()
}
