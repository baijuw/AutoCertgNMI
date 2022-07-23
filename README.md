# AutoCertgNMI
Helps create a common CA and sign a bunch of certificates for nodes needing mTLS.  eg gNMI </p>

# step 1
Once the project is downloaded run the following command to install all the dependencies for the script to run correctly. 

**pip install -r requirements.txt -v**


# Step 2
Edit the config.toml file to </p>

    1. Update the hostname and IP address to the file for which you want to generate a signed certificate.
    2. Update the cert_subject section to add details of the certificate

**PS:** Followup addition of nodes will not re-create the root key or certificate as long as the artifacts are present in the **ca** directory. The is the case for client certificate and keys too as long as the files still exist in the **client** directory. 

# Step 3
Run the main.py script. 

# Step 4
Find the newly created certificates and private keys under the **client** directory
