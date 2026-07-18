// INTENTIONAL VULNERABILITY: Weak Cryptography (CWE-327 / cs/weak-crypto - Medium)
// DUPLICATE_GROUP: cs-crypto-001
// This file exists for CodeQL SAST baseline testing only.
using System.Security.Cryptography;
using System.Text;

public class WeakCryptoSha1
{
    public byte[] Digest(string value)
    {
        // VULN: weak cryptography is used for sensitive data.
        using var hash = SHA1.Create();
        return hash.ComputeHash(Encoding.UTF8.GetBytes(value));
    }
}
