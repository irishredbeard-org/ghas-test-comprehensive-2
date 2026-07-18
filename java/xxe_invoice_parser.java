// INTENTIONAL VULNERABILITY: XXE (CWE-611 / java/xxe - Medium)
// DUPLICATE_GROUP: java-xxe-001
// This file exists for CodeQL SAST baseline testing only.
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.InputStream;

public class xxe_invoice_parser {
    public Document parse(InputStream input) throws Exception {
        // VULN: external entity resolution is not disabled.
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        return factory.newDocumentBuilder().parse(input);
    }
}
