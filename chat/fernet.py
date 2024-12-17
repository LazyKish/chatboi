from cryptography.fernet import Fernet

# Generate a valid Fernet key
key = Fernet.generate_key()

# Save the key for future use
print(key)  # This w