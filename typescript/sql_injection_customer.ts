// INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / js/sql-injection - Medium)
// DUPLICATE_GROUP: ts-sqli-001
// This file exists for CodeQL SAST baseline testing only.
type Database = { query(sql: string): Promise<unknown> };

function sql_injection_customer(db: Database, req: { query: Record<string, string | undefined> }): Promise<unknown> {
  const value = req.query.value ?? '';
  // VULN: request input is concatenated directly into SQL.
  return db.query("SELECT * FROM records WHERE owner = '" + value + "'");
}

export { sql_injection_customer };
