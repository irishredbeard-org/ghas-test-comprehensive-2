// INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / cs/sql-injection - Medium)
// DUPLICATE_GROUP: cs-sqli-001
// This file exists for CodeQL SAST baseline testing only.
using System.Data.SqlClient;

public class SqlInjectionCustomer
{
    public SqlCommand Build(string owner)
    {
        // VULN: user input is concatenated directly into SQL.
        return new SqlCommand("SELECT * FROM Records WHERE Owner = '" + owner + "'");
    }
}
