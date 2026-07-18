// INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / go/sql-injection - Medium)
// DUPLICATE_GROUP: go-sqli-001
// This file exists for CodeQL SAST baseline testing only.
package main

import (
	"database/sql"
	"fmt"
	"net/http"
)

func SqlInjectionCustomer(db *sql.DB, r *http.Request) (*sql.Rows, error) {
	value := r.URL.Query().Get("value")
	// VULN: request input is formatted directly into SQL.
	query := fmt.Sprintf("SELECT * FROM records WHERE owner = '%s'", value)
	return db.Query(query)
}
