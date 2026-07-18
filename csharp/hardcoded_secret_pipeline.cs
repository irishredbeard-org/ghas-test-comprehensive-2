// INTENTIONAL VULNERABILITY: Hardcoded Credentials (CWE-798 / cs/hardcoded-credentials - High)
// DUPLICATE_GROUP: cs-secret-002
// This file exists for CodeQL SAST baseline testing only.
public class HardcodedSecretPipeline
{
    public string GetToken()
    {
        // VULN: credential is hardcoded in source.
        return "ghp_example_static_pipeline_token_123456";
    }
}
