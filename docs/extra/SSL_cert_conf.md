# Configuring Polarion certificate

1. Find Git (or even Polarion) path and add to the environment variables. The path ``C:\Program Files\Git\usr\bin`` should have the ``openssl.exe``` to create a [*Self-signed SSL certificate*](https://docs.sw.siemens.com/en-US/doc/230235217/PL20221020258116340.xid1465510/xid1568235) file using:
```properties
openssl req -x509 -nodes -days 3650 -newkey rsa:1024 -keyout privateKey.key -out serverCert.pem
```

2. Copy your certificate and keyfile to ``C:\Polarion\bundled\apache\conf\``

3. Activate and configure SSL. Use a text editor application to open file ``C:\Polarion\bundled\apache\conf\httpd.conf``.

4. Search for the line containing: ``LoadModule ssl_module modules/mod_ssl.so`` and remove the leading comment marker (#). Uncommenting this line activates the SSL module.

5. Search for the line containing ``Include conf/extra/httpd-ssl.conf`` and remove the leading comment marker (#).

6. (Optionally) Deactivate unencrypted http traffic. Edit the file ``C:\Polarion\bundled\apache\conf\httpd.conf``. Find the line ``Listen 80`` and add a comment marker # at the beginning, leaving the line as: ``#Listen 80``.

7. Set up the certificate file in SSL. Edit file ``C:\Polarion\bundled\apache\conf\extra\httpd-ssl.conf``, and search for ``SSLCertificateFile``. Change the path to point to the certificate file.

```properties
SSLCertificateFile "C:\Polarion\bundled\apache\conf\certificate.pem"
```

8. Set up the key file in SSL. Edit file ``C:\Polarion\bundled\apache\conf\extra\httpd-ssl.conf`` and search for ``SSLCertificateKeyFile``. Change line path to point to the certificate key file.

```properties
SSLCertificateKeyFile "C:\Polarion\bundled\apache\conf\privateKey.key"
```

9. If you are using a certificate that is not from an authority trusted by Java — a self-signed certificate, for example — import the certificate to the Java keystore, as described in Import a Certificate to the Java Keystore.
    
10. Copy the default keystore $JDK_HOME/lib/security/cacerts as $JDK_HOME/lib/security/jssecacerts. And import the certificate to the ``jssecacerts`` keystore using the following command, replacing variables as noted below:

```properties
"C:\Program Files\Java\jdk-17\bin\keytool" -importcert -file "C:\Polarion\bundled\apache\conf\serverCert.pem" -alias polarion_server_ssl_01 -keystore "C:\Program Files\Java\jdk-17\lib\security\jssecacerts" -storepass changeit -noprompt
```
11. (Optional) To check that the certificate is not corrupted
```
openssl x509 -in serverCert.pem -text
```

12. When prompted, check the certificate and confirm that it should be trusted. The prompt to verify and confirm the certificate can be suppressed by adding option -noprompt.

13. Add the certificate's path to the ``polarion.ini`` file under ``C:\Polarion\polarion\polarion.ini``.

```properties
-Djavax.net.ssl.trustStore=$JAVA_HOME/lib/security/jssecacerts
```

14. Change ``repo`` option on ``C:\Polarion\polarion\configuration\polarion.properties`` file from ``http`` to ``https``.