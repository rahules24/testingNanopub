from Crypto.PublicKey import RSA

def strip_key_lines(key_str):
    return '\n'.join(key_str.splitlines()[1:-1])

key = RSA.generate(2048)
private_key_str = strip_key_lines(key.export_key('PEM', pkcs=8).decode('utf-8'))
public_key_str = strip_key_lines(key.publickey().export_key().decode('utf-8'))

# Save the private key
with open(r'C:\Users\scarl\.nanopub\id_rsa', 'w') as private_file:
    private_file.write(private_key_str)

# Save the public key
with open(r'C:\Users\scarl\.nanopub\id_rsa.pub', 'w') as public_file:
    public_file.write(public_key_str)
