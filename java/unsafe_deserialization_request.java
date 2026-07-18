// INTENTIONAL VULNERABILITY: Unsafe Deserialization (CWE-502 / java/unsafe-deserialization - High)
// DUPLICATE_GROUP: java-deser-001
// This file exists for CodeQL SAST baseline testing only.
import java.io.ObjectInputStream;
import javax.servlet.http.HttpServletRequest;

public class unsafe_deserialization_request {
    public Object deserialize(HttpServletRequest request) throws Exception {
        // VULN: request body bytes are deserialized without validation.
        ObjectInputStream stream = new ObjectInputStream(request.getInputStream());
        return stream.readObject();
    }
}
