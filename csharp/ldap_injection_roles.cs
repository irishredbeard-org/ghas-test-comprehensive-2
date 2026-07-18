// INTENTIONAL VULNERABILITY: LDAP Injection (CWE-90 / cs/ldap-injection - High)
// DUPLICATE_GROUP: cs-ldap-001
// This file exists for CodeQL SAST baseline testing only.
using System.DirectoryServices;

public class LdapInjectionRoles
{
    public DirectorySearcher Build(string value)
    {
        // VULN: user input is concatenated into an LDAP filter.
        return new DirectorySearcher("(uid=" + value + ")");
    }
}
