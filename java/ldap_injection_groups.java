// INTENTIONAL VULNERABILITY: LDAP Injection (CWE-90 / java/ldap-injection - High)
// DUPLICATE_GROUP: java-ldap-001
// This file exists for CodeQL SAST baseline testing only.
import javax.servlet.http.HttpServletRequest;
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;

public class ldap_injection_groups {
    public Object search(DirContext context, HttpServletRequest request) throws Exception {
        String value = request.getParameter("value");
        // VULN: request input is concatenated into an LDAP filter.
        String filter = "(uid=" + value + ")";
        return context.search("ou=people,dc=example,dc=com", filter, new SearchControls());
    }
}
