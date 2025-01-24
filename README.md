# Encrypted at Rest

Motivation: just wanted some experience in storing encrypted data in the database.

Method: user should specify an encryption key when submitting or retrieving messages. The data is stored encrypted, with no knowledge of the encryption key that was used. So long as the same key is used when retrieving the message, it will be decrypted.
