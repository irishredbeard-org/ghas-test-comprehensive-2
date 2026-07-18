// INTENTIONAL VULNERABILITY: Command Injection (CWE-78 / java/exec-tainted-command - Critical)
// DUPLICATE_GROUP: java-exec-001
// This file exists for CodeQL SAST baseline testing only.
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

public class exec_tainted_archive {
    public void handle(HttpServletRequest request) throws IOException {
        String command = request.getParameter("cmd");
        // VULN: request input flows directly into exec().
        Runtime.getRuntime().exec(command);
    }
}
