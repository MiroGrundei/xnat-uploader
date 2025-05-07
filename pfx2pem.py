import OpenSSL.crypto
import os


def pfx_to_pem(pfx_path, pfx_password, pem_path):
    ''' Converts a .pfx file to a .pem file and saves it. '''
    with open(pfx_path, 'rb') as pfx_file:
        pfx_data = pfx_file.read()

    p12 = OpenSSL.crypto.load_pkcs12(pfx_data, pfx_password)

    with open(pem_path, 'wb') as pem_file:
        # Write the private key
        pem_file.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
        # Write the certificate
        pem_file.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))

        # Write any CA certificates if they exist
        ca_certs = p12.get_ca_certificates()
        if ca_certs:
            for cert in ca_certs:
                pem_file.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))

    print(f"PEM file saved at: {pem_path}")


# Example usage
pfx_path = 'C:/Users/nnu04/Documents/MeMoSLAP/XNAT/GRUNDEI.p12'  # Your .pfx certificate path
pfx_password = ''  # Your password
pem_path = 'C:/Users/nnu04/Documents/MeMoSLAP/XNAT/GRUNDEI.pem'  # Desired .pem output path

pfx_to_pem(pfx_path, pfx_password, pem_path)
