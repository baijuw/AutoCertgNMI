import toml
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from pathlib import Path
import ipaddress

# Load the configuration file.
config_file = "config.toml"
T = toml.load(config_file)
servers = T.get("servers", None)
sr_switches = T.get("sr_switches", None)
cert_subject = T.get("cert_subject")
if not any((servers, sr_switches)):
    print(f'''

    Please update the config file {config_file} it is missing the [sr_switches] or [servers] section.
    At least one server or switch is required. 

    ''')


# Class to initialize the CA certificate and also the associated methods.
class CertSigner:
    def __init__(self, cert_subject):
        self.subject = self.issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, cert_subject["COUNTRY_NAME"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, cert_subject["STATE_OR_PROVINCE_NAME"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, cert_subject["LOCALITY_NAME"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert_subject["ORGANIZATION_NAME"]),
            x509.NameAttribute(NameOID.COMMON_NAME, cert_subject["COMMON_NAME"]),
        ])
        self.ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=backends.default_backend())
        Path("ca").mkdir(parents=True, exist_ok=True)
        with open("ca/ca_key.pem", "wb") as f:
            f.write(self.ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"password"),
            ))
        self.ca_cert = x509.CertificateBuilder().subject_name(self.subject) \
            .issuer_name(self.issuer) \
            .public_key(self.ca_key.public_key()) \
            .serial_number(x509.random_serial_number()) \
            .not_valid_before(datetime.datetime.utcnow()) \
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True) \
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650)) \
            .sign(self.ca_key, hashes.SHA256(), backends.default_backend())
        with open("ca/ca_cert.pem", "wb") as f:
            f.write(self.ca_cert.public_bytes(serialization.Encoding.PEM))

    def client_cert_gen(self, host, ip):
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=backends.default_backend())
        # Write our key to disk for safe keeping
        Path("client").mkdir(parents=True, exist_ok=True)
        with open("client/" + host + "_key.pem", "wb") as f:
            f.write(self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        self.client_subject_name = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, cert_subject["COUNTRY_NAME"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, cert_subject["STATE_OR_PROVINCE_NAME"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, cert_subject["LOCALITY_NAME"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert_subject["ORGANIZATION_NAME"]),
            x509.NameAttribute(NameOID.COMMON_NAME, host),
        ])
        self.subject_alt_name = [x509.IPAddress(ipaddress.IPv4Address(ip)), x509.DNSName(host)]
        self.csr = x509.CertificateSigningRequestBuilder().subject_name(self.client_subject_name) \
            .add_extension(x509.SubjectAlternativeName(self.subject_alt_name),
                           critical=False, ).sign(self.key, hashes.SHA256(), backends.default_backend())
        # Uncomment the next two lines if you want a copy of the CSR written to disk.
        # with open("client/"+host+"_csr.pem", "wb") as f:
        #     f.write(self.csr.public_bytes(serialization.Encoding.PEM))

        self.cert = x509.CertificateBuilder().subject_name(self.client_subject_name) \
            .issuer_name(self.ca_cert.issuer) \
            .public_key(self.key.public_key()) \
            .serial_number(x509.random_serial_number()) \
            .not_valid_before(datetime.datetime.utcnow()) \
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=cert_subject["VALIDITY_IN_DAYS"])) \
            .add_extension(x509.SubjectAlternativeName(self.subject_alt_name), critical=False, ) \
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True) \
            .sign(self.ca_key, hashes.SHA256(), backends.default_backend())

        with open("client/" + host + "_cert.pem", "wb") as f:
            f.write(self.cert.public_bytes(serialization.Encoding.PEM))


if __name__ == "__main__":
    mycert = CertSigner(cert_subject)
    for host, ip in sr_switches.items():
        mycert.client_cert_gen(host, ip)
    for host, ip in servers.items():
        mycert.client_cert_gen(host, ip)
