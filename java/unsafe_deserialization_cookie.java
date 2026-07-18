// INTENTIONAL VULNERABILITY: Unsafe Deserialization (CWE-502 / java/unsafe-deserialization - High)
// DUPLICATE_GROUP: java-deser-001
// This file exists for CodeQL SAST baseline testing only.
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import java.util.Base64;
import javax.servlet.http.HttpServletRequest;

public class unsafe_deserialization_cookie {
    public Object deserialize(HttpServletRequest request) throws Exception {
        String payload = request.getParameter("session");
        byte[] data = Base64.getDecoder().decode(payload);
        // VULN: cookie-controlled bytes are deserialized without validation.
        ObjectInputStream stream = new ObjectInputStream(new ByteArrayInputStream(data));
        return stream.readObject();
    }
}
