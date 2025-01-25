# Encrypted at Rest

## Motivation

I just wanted some experience in storing encrypted data in the database.

## Method

The user should specify an encryption key when submitting or retrieving messages. The data is stored encrypted, with no knowledge of the encryption key that was used. So long as the same key is used when retrieving the message, it will be decrypted.

## Not suitable for production

It's a fun little proof-of-concept. Gives me a starting point if I ever need to encrypt data at rest in future.

# How to use

## Set up environment

Same as any django project - clone the repo, and `cd` into the project directory and then:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver 8000
```

## Example Requests

```python
import requests

# create users just because it's required for messages
response = requests.post('http://localhost:8000/api/app-users/', json={'name': 'Alfie'})
user_id1 = response.json()['id']
response = requests.post('http://localhost:8000/api/app-users/', json={'name': 'Brenda'})
user_id2 = response.json()['id']

# send some messages
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id1, 'user_to': user_id2, 'key': 'SuperSecretKey123', 'content': 'I have something really important to tell you but it must remain private'})
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id2, 'user_to': user_id1, 'key': 'SuperSecretKey123', 'content': 'omg seriously?!'})
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id1, 'user_to': user_id2, 'key': 'SuperSecretKey123', 'content': 'Yes, but we cant communicate via normal channels - let\'s use the encrypted service'})
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id2, 'user_to': user_id1, 'key': 'SuperSecretKey123', 'content': 'Yeah makes sense!'})

# View API endpoint without specifying the key
response = requests.get('http://localhost:8000/api/view-messages/')
response.json()
# Note how result are encrypted - totally meaningless because we did not provide the encryption key
```

```json
[
    {
        "id": "a0be081b-528d-421a-bc37-7b3587f34a10",
        "created_at": "2025-01-25T00:40:20.491353Z",
        "content": "Z0FBQUFBQm5sREwwLVpJSlNLRW9aQklDaUJtN0FrMFhWR0pUeDI0dF9heGR4cU4zSG1QVnBrMTE5UFp3ajhpQkh0UEMyb1dTX2Z3NkpXWDRIYW5GejhDMllKWGNSOUVla2M2MGY3ZFRFc1Nnb2NTX21UWU9IUEE9",
        "user_from": "395e2009-4f78-4fd8-b1ef-b535fc5704b8",
        "user_to": "d8d069ee-eb63-404d-9a34-952a6a0af48c"
    },
    {
        "id": "6f987b53-13a9-4c44-8748-d6c1acef0833",
        "created_at": "2025-01-25T00:40:20.463756Z",
        "content": "Z0FBQUFBQm5sREwwRGtPOUs1ak0xSnVNUGg5RVdVNE9KYWUzSXo4U1dNclZrS3hwRnNablZTXzBYTDl1RjBrbmNLR0lZTzBUYlpnaF9TUEp5d1Q4cXBaMXBSRm5BcEVzamR4VF8tS2I2cmM5d0doZlZURWxXMFpFMFViRFQ1Y0lzQzN3blAxSUxucC1CN0Mxc09Wa3VtU2phWk9LZ0dEQlVOUkZqdzduTWV6YnRsRDhRRHlqOEJNUVdfa3ktVmFrVjdUaDFmUjlXZkNa",
        "user_from": "d8d069ee-eb63-404d-9a34-952a6a0af48c",
        "user_to": "395e2009-4f78-4fd8-b1ef-b535fc5704b8"
    },
    {
        "id": "30bb36e4-8d47-4193-b866-d12a7da0926f",
        "created_at": "2025-01-25T00:40:20.436107Z",
        "content": "Z0FBQUFBQm5sREwwZjN2U1ZtazlDSVp0QjlmMXQ3cEt0cURaX1kwT0doYjU0WGpqRFllcU5yQWtKb2U0ci1LRWNVN292WlpKR3ZTV1VaaXQ0bmdIUlZ3ZDVRdzhZcmxSN2c9PQ==",
        "user_from": "395e2009-4f78-4fd8-b1ef-b535fc5704b8",
        "user_to": "d8d069ee-eb63-404d-9a34-952a6a0af48c"
    },
    {
        "id": "d375829a-d404-49ed-b70b-484a8a13e69b",
        "created_at": "2025-01-25T00:40:20.394545Z",
        "content": "Z0FBQUFBQm5sREwwZzdyczl4bVdfdjhaM3JpQXNfVnpwS1NHN1FRamtWN0gwZWZIZkxWenpNSERTMWJJQ3NBdGk3NXFiM3ZKZlppU3NXX0x5ZkhBeVJPVkt4aDJFRzhNNWpFX1QzVlZQREk4c2FoSVJVbEJ5d01scXhMTzdBbUNXUFFNZ3d6alhRQTUtODJPYXlpV25rY0FKc0dTYVd6N0pYUDlVYjMwUm84bF9peW04eWh5MllrPQ==",
        "user_from": "d8d069ee-eb63-404d-9a34-952a6a0af48c",
        "user_to": "395e2009-4f78-4fd8-b1ef-b535fc5704b8"
    }
]
```

```python
# View API endpoint - this time, specifying the key
response = requests.get('http://localhost:8000/api/view-messages/?key=SuperSecretKey123')
response.json()
```

```json
[
  {
    "id": "c66c93bc-7ccf-4587-bc65-fb891965624e",
    "created_at": "2025-01-25T00:46:06.132711Z",
    "content": "Yeah makes sense!",
    "user_from": "13490489-330a-4620-9376-a98e6c037add",
    "user_to": "a6188145-a304-4ab0-8ab8-1527b1f74581"
  },
  {
    "id": "bf730481-cfbe-4253-89d0-9c62bab061a8",
    "created_at": "2025-01-25T00:46:06.104957Z",
    "content": "Yes, but we cant communicate via normal channels - let's use the encrypted service",
    "user_from": "a6188145-a304-4ab0-8ab8-1527b1f74581",
    "user_to": "13490489-330a-4620-9376-a98e6c037add"
  },
  {
    "id": "a1316d20-0209-4f5b-95df-653d615ed222",
    "created_at": "2025-01-25T00:46:06.077017Z",
    "content": "omg seriously?!",
    "user_from": "13490489-330a-4620-9376-a98e6c037add",
    "user_to": "a6188145-a304-4ab0-8ab8-1527b1f74581"
  },
  {
    "id": "e4f137fa-830e-460f-8663-259578166b29",
    "created_at": "2025-01-25T00:46:06.046608Z",
    "content": "I have something really important to tell you but it must remain private",
    "user_from": "a6188145-a304-4ab0-8ab8-1527b1f74581",
    "user_to": "13490489-330a-4620-9376-a98e6c037add"
  }
]
```

# Further work

I guess all fields, not just the content, should probably be encrypted - otherwise, the user_from/to ids could leak. This might also make it easier to implement the functionality on the model itself, rather than in the views.
