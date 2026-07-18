// INTENTIONAL VULNERABILITY: Path Traversal (CWE-22 / cs/path-injection - High)
// DUPLICATE_GROUP: cs-path-001
// This file exists for CodeQL SAST baseline testing only.
using System.IO;

public class PathTraversalTemplate
{
    public string Read(string file)
    {
        // VULN: user input controls the filesystem path.
        string target = Path.Combine("/var/app/data", file);
        return File.ReadAllText(target);
    }
}
