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
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id1, 'user_to': user_id2, 'key': 'SuperSecretKey123', 'content': 'Yes, but we cant communicate via normal channels - lets use the encrypted service'})
requests.post('http://localhost:8000/api/send-message/', json={'user_from': user_id2, 'user_to': user_id1, 'key': 'SuperSecretKey123', 'content': 'Yeah makes sense!'})

# View API endpoint without specifying the key
response = requests.get('http://localhost:8000/api/view-messages/')
response.json()
```

Note how result are encrypted - totally meaningless because we did not provide the encryption key

```json
[
  {
    "id": "964fb2d6-af0a-4bb2-aef2-ea8c306c2efd",
    "encrypted": {
      "created_at": "Z0FBQUFBQm5sZ3EzZ1dMcWpfRURIbzRsZ0N6TFhIY0FjU3RHN3daanhHbTNuUlR5alk1T2dFRXRMcE43WWhlQWdFX1pFV0FxT0xKdmdUV2o0bkFJdkl1SU9XTjJXeDQwMjlLeGJPTDVBbkJQLThBVHdVWDU4cEU9",
      "user_from": "Z0FBQUFBQm5sZ3EzR0NvdjBxUE5Ca09pOVllc0lEWlRmSkRqcUtPT2t4cEJHYVdEWC1UZU5qS2puOFdUdjltaGo3cXBFS3NSUFp1c2ZvZzNyMEdWdE9pWHFOcHRmalprSEFPX2VJV1pKOXJDSHNSNnduM0xBdDBRYmZJQ1hkbjRwelFzT3lzcXpDbms=",
      "user_to": "Z0FBQUFBQm5sZ3EzanFuM3pPN2RWTGVHd0tlZnJYcTE2S2JlMkxyWDVCYWZsamV2RjZlX2RteFMzZVRHeXVEWWk1QXZPX1dXY0xWajVBWl9OUTZlSDN1ZThFQzUxbjY1Rk5DNFRoc01zZVp5ODJTcEdDRnZQaXZ6YnlXSGNUUEdfR05TMWY3bkVveXo=",
      "content": "Z0FBQUFBQm5sZ3EzdVg4UHN1WnZGQ00teUhOQV9JeDVSeXhjUGF1eHNZQzUydHVNQXo2WWpTSW5sUHM3UklxaUg1dTVzUHBpTnVDRFBzTERUZENVSnZfQ1NDQm03Ti1FUEY2SXJ1aHpKR2xDUzl0UnZpM2xwMVNfNmRUVUY0Tlg0OUNhbTRLZmpucVJ6ZnR5VUlaaXhWbU45MXJxMHplaWlDVTJGYnp2a0lzeVlzclEwNS12RmlhNEZscUI0UzkwMHRXMW0weU1MaTJ3"
    }
  },
  {
    "id": "5144b952-355a-45e4-8ef7-5dde8622e1be",
    "encrypted": {
      "created_at": "Z0FBQUFBQm5sZ3EzR3JjMmpwTW5zZnNCdHFkUHlxQzhjN0pfVExUSnpxV0dIeWxUSlZsVGdrbHdQeGNYV0Fibk1lYVFfNV9GNF84MkNIS0JqU0xPRVdBLUdibVJpaU1KQkNuem5OV09aMUhYWEhEZUZncEZ2aW89",
      "user_from": "Z0FBQUFBQm5sZ3EzUWM0ckJqZmMwR2VTRGRxVldYQVNXMl9vckZyWng2VFhSTlMwMDRvMUJnbHNFWmVsa280dHpLdS1QbFQzQTA2dEZsOUd1SG56RElHYV9rdkNXeXJQcE93T3lUYTV6VTdzZ250SnFZejVMb3dPRjNIdHVkRHYzOGlSQnI5a1FKZUM=",
      "user_to": "Z0FBQUFBQm5sZ3EzcDEzck9NWE5tOEVnbXVxMEswMlFNbnBjdml3RDRVNlpybjNGXzN1cmZTcVBUSXViNjFOQklfWWduaWxESlhtNE9TR0lEdFFKY0JmSjE4YjNEdkh2MDV4Zl9GUUNLLW1jV082Z2l2MGpNRlJaQU1hSTlDSE52RDdHSlhRald2dHM=",
      "content": "Z0FBQUFBQm5sZ3EzQUt1ZlpESnV0Y0l2UTZkRUFMZHBTdGZMZm80TjJEWkVZLUNONlBtV1BRVUFxQXJaMlVzNWd0S1VLZDFkYU9NYnFvTU9wMWpEUnVBNi11c0MtSkFWZ0djYzhNQ1VHMXhqTVdxSk1HbllBSWc9"
    }
  },
  {
    "id": "bd1e0b07-4030-4c90-897a-6393f0e25e16",
    "encrypted": {
      "created_at": "Z0FBQUFBQm5sZ3EycmszWVlZek1TYVN6Y09NaUdGMlVmWjNmU2QzRjQwOEstNFN3YzZlZmJmS2NBRVJVQjBEU2M0b0lRWlpONUdCY3BDMTdnUWVJM29FWkgyVW5MY0w1N1hsQTJqOGRpeTRDSmIzaDlFY2ttR009",
      "user_from": "Z0FBQUFBQm5sZ3EyMHdLOFZ6MjhQS3d2UjE0bUF6bmJDNUw3ZnhlRFhTQjlFa0ozYXBENzIwbHlBenVRZFA0MExIS2wtbzM5U2ZnUjB4cWxzdzNWOEo3Z25XZmhHTG9kSDZFNXZDX01kNkY1QlRjTllCVjlEdll6TzY2VW9tdGxnekIyai02UTVGSWg=",
      "user_to": "Z0FBQUFBQm5sZ3EyMkNQU2llWGNrTzB1ZDhWTmZtQTVTY2RzaDRQT00wXzJXY0VjX2dnbjAtQkNIM0hhYnhLSEdLdHVwZnpYTExrRm05Y2didmhRQW9Ka21wMEZua2tNRVJHYXpGVTg3TWRDZ25IWWJFdjM1VWtvNWVDdWYwYTVjZUhSNUhuRzRFaGM=",
      "content": "Z0FBQUFBQm5sZ3EyMEluMlNHZVpKeVpwTGF4OWo3ekx1Q2htX0hBbzk0dUNPMnpDaEYyZ2hXclN1dENYZjZsMVM3OEN1ZFFhaUk4c09hdk4xcmJrNGpjQVdVTjBCRXVwU0xUbDZZeXFiTGIzUFBfUGxXejFEMFBJTjk3R0d2UElqVmQyUS1vRjJoOHNsakdWNVVELUZzaHFFN1ZUQlZhSHdTZzh5bmM5NFIyQjJmdEltcWc0ZXdnPQ=="
    }
  },
  {
    "id": "cfdecd98-cbe0-4add-a414-cc604b3529e3",
    "encrypted": {
      "created_at": "Z0FBQUFBQm5sZ3EySzJabnhzV0wxajBEb3ZyWGxIU1RfUVNMTW9JZVhnQjZZemhtbzVvXzEyekh4WmRVU0hfYnVtamZkRUdjSFdydHg2OUJPQWtIYWd1S0VXSG5xSHZFRno4U1ZScXhXUG1HT0czTE0tWE9RS1E9",
      "user_from": "Z0FBQUFBQm5sZ3EyaXZDM1BCXzNTVm5PSklyR1ptOHdRVFRkTjR6SHVBMlZBd1BmUFZCUTZJQ0R3S3F6VldLTUFMNnRwNHIzc1pvYW84R0ZDcXpxdHIzZmtjT1JUNHhHcDUyaTNTc1FlQUpjdjg1dU5qRVYzRkpfMWdTUEdIUTdtU1d0SnFYdEhKRDA=",
      "user_to": "Z0FBQUFBQm5sZ3EyNFZjS0dGQXR3dUF0ekpzTkNRcE84MzNvLXJOdi1rN1B6bkdxbXhjaWwzY0lmMFhqN3RZUXN5T2RveVFKa3lCXzV1NHNRSExUd3IteTFrdjZGMWkzWmMyZXhTZ1BVWm9MM1lHV1hBVGl5OFo4ZGdIUFR4dTBpUXRRUER3ekZna0w=",
      "content": "Z0FBQUFBQm5sZ3EzR25zb0Z3UUxINkpTSC03ck5hRlVBTGpSc2J6MUtWcTduSGRkZndWSkdEYmlIYTBWUThTcXhzcjFVY2ZzX2JzU0lwaFEzTG04cFNTa0x2TW84VUNoRkE9PQ=="
    }
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
    "id": "5144b952-355a-45e4-8ef7-5dde8622e1be",
    "encrypted": {
      "created_at": "2025-01-26T10:13:11.098331",
      "user_from": "a2f08389-3959-4436-8b20-2666133f7e32",
      "user_to": "53d5ebc5-9dd5-489b-b7bd-74b37f5bfd06",
      "content": "Yeah makes sense!"
    }
  },
  {
    "id": "964fb2d6-af0a-4bb2-aef2-ea8c306c2efd",
    "encrypted": {
      "created_at": "2025-01-26T10:13:11.022902",
      "user_from": "53d5ebc5-9dd5-489b-b7bd-74b37f5bfd06",
      "user_to": "a2f08389-3959-4436-8b20-2666133f7e32",
      "content": "Yes, but we cant communicate via normal channels - lets use the encrypted service"
    }
  },
  {
    "id": "cfdecd98-cbe0-4add-a414-cc604b3529e3",
    "encrypted": {
      "created_at": "2025-01-26T10:13:10.949202",
      "user_from": "a2f08389-3959-4436-8b20-2666133f7e32",
      "user_to": "53d5ebc5-9dd5-489b-b7bd-74b37f5bfd06",
      "content": "omg seriously?!"
    }
  },
  {
    "id": "bd1e0b07-4030-4c90-897a-6393f0e25e16",
    "encrypted": {
      "created_at": "2025-01-26T10:13:10.858042",
      "user_from": "53d5ebc5-9dd5-489b-b7bd-74b37f5bfd06",
      "user_to": "a2f08389-3959-4436-8b20-2666133f7e32",
      "content": "I have something really important to tell you but it must remain private"
    }
  }
]
```
