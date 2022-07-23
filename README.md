# AutoCertgNMI
Often large projects have several TLS integrations. This script will help generate self-signed certificates for the
entire project in one go. This will ensure that you have a common CA for all nodes needing mTLS.  eg gNMI </p>
Once the certificates are signed you will find them in the newly created directory **client** in the root of the project.
The CA certificate will be in the **ca** directory with the filename **ca_cert.pem**. </p>

**ca/ca_key.pem** file is the secret key for the entire project. This needs to be protected and never shared with anyone.

# step 1
Once the project is downloaded run the following command to install all the dependencies for the script to run correctly. 

**pip install -r requirements.txt -v**


# Step 2
Edit the config.toml file to </p>

    1. Update the hostname and IP address under the [switches] and [servers] section for which you want certificates generated.
    2. Update the [cert_subject] section to add details of the certificate.
    3. Edit the [root_key_password] section with a strong password to encrypt the root key at rest. Never share this password with anyone.

**PS:** Followup addition of nodes will not re-create the root key or certificate as long as the artifacts are present in the **ca** directory. The is the case for client certificate and keys too as long as the files still exist in the **client** directory. 

# Step 3
Run the main.py script. 

# Step 4
Find the newly created certificates and private keys under the **client** directory. You will also find the CA certificate 
at **ca/ca_cert.pem**. This is used at the trust anchor with all the clients. 
