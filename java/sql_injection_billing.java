// INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / java/sql-injection - Medium)
// DUPLICATE_GROUP: java-sqli-002
// This file exists for CodeQL SAST baseline testing only.
import javax.servlet.http.HttpServletRequest;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class sql_injection_billing {
    public ResultSet find(Connection connection, HttpServletRequest request) throws Exception {
        String account = request.getParameter("account");
        Statement statement = connection.createStatement();
        // VULN: request input is concatenated directly into SQL.
        return statement.executeQuery("SELECT * FROM invoices WHERE account = '" + account + "'");
    }
}
