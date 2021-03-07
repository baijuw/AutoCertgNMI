# AutoCertgNMI
Helps create a common CA and sign a bunch of certificates for nodes needing mTLS.  eg gNMI </p>

# Step 1
Edit the config.toml file. Add the hostname and IP address to the file for which you want to generate a signed certificate.

# Step 2
Run the main.py script. 

# Step 3
Find the newly created certificates and private keys under the **client** directory
