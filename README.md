# AutoCertgNMI
Often large projects have several TLS integrations. This script will help generate self-signed certificates for the
entire project in one go. This will ensure that you have a common CA for all nodes needing mTLS.  eg gNMI </p>
Once the certificates are signed you will find them in the newly created directory **client** in the root of the project.
The CA certificate will be in the **ca** directory with the filename **ca_cert.pem**. </p>

**ca/ca_key.pem** file is the secret key for the entire project. This needs to be protected and never shared with anyone.

It is safe to rerun the script by adding new nodes to the config file. The root key, root certificate and old the node's key and certificates will not be overwritten as long as the old files are present in the **ca**  and **client** directory. 
To re-key an existing node, one must delete the files corresponding to that node from the **client** directory. 

# step 1
Once the project is downloaded run the following command to install all the dependencies for the script to run correctly. 

**pip install -r requirements.txt -v**


# Step 2
Edit the config.toml file to:- </p>

   > 1. Update the hostname and IP address under the [switches] and [servers] section for which you want certificates generated. Multiple IP addresses can be added by grouping IP's inside square brackets. Examples can be found in the config.toml file. These IPs will be bundled into the client certificate as AltNames. 
   > 2. Update the [cert_subject] section to add details of the certificate.
   > 3. Edit the [root_key_password] section with a strong password to encrypt the root key at rest. Never share this password with anyone.

**PS:** It is safe to rerun the script by adding new nodes to the config file. The root key, root certificate and old the node's key and certificates will not be overwritten as long as the old files are present in the **ca**  and ** client** directory.
# Step 3
Run the main.py script. 

# Step 4
Find the newly created certificates and private keys under the **client** directory. You will also find the CA certificate 
at **ca/ca_cert.pem**. This is used at the trust anchor with all the clients. 
