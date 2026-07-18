// INTENTIONAL VULNERABILITY: Unsafe Deserialization (CWE-502 / java/unsafe-deserialization - High)
// DUPLICATE_GROUP: java-deser-001
// This file exists for CodeQL SAST baseline testing only.
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import javax.servlet.http.HttpServletRequest;

public class unsafe_deserialization_cache {
    public Object deserialize(HttpServletRequest request) throws Exception {
        String payload = request.getParameter("cache");
        byte[] data = payload.getBytes();
        // VULN: request-controlled cache bytes are deserialized without validation.
        ObjectInputStream stream = new ObjectInputStream(new ByteArrayInputStream(data));
        return stream.readObject();
    }
}
