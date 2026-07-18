// INTENTIONAL VULNERABILITY: Path Traversal (CWE-22 / java/path-injection - High)
// DUPLICATE_GROUP: java-path-001
// This file exists for CodeQL SAST baseline testing only.
import javax.servlet.http.HttpServletRequest;
import java.nio.file.Files;
import java.nio.file.Path;

public class path_traversal_download {
    public String read(HttpServletRequest request) throws Exception {
        String requested = request.getParameter("file");
        // VULN: request input controls the filesystem path.
        Path target = Path.of("/var/app/data", requested);
        return Files.readString(target);
    }
}
