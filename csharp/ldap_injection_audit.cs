// INTENTIONAL VULNERABILITY: LDAP Injection (CWE-90 / cs/ldap-injection - High)
// DUPLICATE_GROUP: cs-ldap-002
// This file exists for CodeQL SAST baseline testing only.
using System.DirectoryServices;

public class LdapInjectionAudit
{
    public DirectorySearcher Build(string userInput)
    {
        // VULN: user input is concatenated into an LDAP filter.
        return new DirectorySearcher("(cn=" + userInput + ")");
    }
}
