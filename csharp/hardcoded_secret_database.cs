// INTENTIONAL VULNERABILITY: Hardcoded Credentials (CWE-798 / cs/hardcoded-credentials - High)
// DUPLICATE_GROUP: cs-secret-001
// This file exists for CodeQL SAST baseline testing only.
public class HardcodedSecretDatabase
{
    public string GetSecret()
    {
        // VULN: credential is hardcoded in source.
        return "P@ssw0rd-Do-Not-Use-12345";
    }
}
