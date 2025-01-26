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
    "id": "b208a0bb-297f-45c7-84ce-ea82b739689e",
    "encrypted": {
      "id": "c407ad1c-ad2d-4829-b889-f027ab0d1e84",
      "created_at": "Z0FBQUFBQm5sZmRzWnI4MEJQVTFTaGhKZF9pNGdsc0gyRGpxeGdsTk1LakRVVXMwWk9WOVJEb3JkejVObUlZSkRiN2pyd241b2dMb1duVC1KT3A4Z1FadFFNU083WXJaTURZeWJFM2pheDA4ZjNYeUQ2eFdCd289",
      "user_from": "Z0FBQUFBQm5sZmRzOGNnQ0xTZWJUMXdCUWc2N0tKczFHd21uZlFUVDdnRXBqSVBuTEF2dVc4YjdPYkZJdjd3UEMxM1JlUHBHUkhUX3REdkJJa0FHaXNoaUpObHphRVNfb1c4WU9uS0lITmRybmRhQ2F5OHdudXBxWDg4aFR4TUVlUHJyRzdwNXZUT3c=",
      "user_to": "Z0FBQUFBQm5sZmRzQ3JlUnVjVGQya0ZfQjBZRDVwUlNfVXVvQjRVTHJfMVBXOWNtMWQwdFBFVm8xdWxnRkExdEVfX01ueTExSVpsR2NXUUlvQXlYcHB4MmtRZmF0OVdwaldQQzZxX21Ma0ROMnFUc0dXSl9ZRHhUVEMzU0w4Zk44eEJ4WWZMaXJma20=",
      "content": "Z0FBQUFBQm5sZmRzNXlucGxBOE1lV2dwejhaYWNFcWR0Sk8zcTlrbDl1M0o4ekpSQllUbXdGcmNGWjV0dm1zd0FleE52VjhqdXc4YUVVamQ2X1RySHpWejVVanNBTV9CdFI1RDEzdmw2WWhqU01GSHE1VkQwLW5kcDdYTWNxcmt1OU1YeldvWGhadHo0X0s4RUxJTV9xS0czT0NFbm1RTlRLMkZ2VTR2bVpVT2doVlVROFUwbU5WREtaTk5tdVZIZW14dEpyd0ctY2lh"
    }
  },
  {
    "id": "1e1a2958-823f-41ca-8605-a447eb08afc9",
    "encrypted": {
      "id": "cd25aa72-d2f8-4594-841b-47647cc42b6d",
      "created_at": "Z0FBQUFBQm5sZmRvZ1BDYzZXM3Jwel9ram9MUXR4eElVRHkzajJtcjEwRDRlYzd3YjhVbFk0MEZtNEJ2bFc4NG03cDN1MlVmTDcxZEc0ODJNOHc4R0Z1UFlUOXdycUVyWGk1SHdIdnpVejBnclZpNkpJQ2FLeFU9",
      "user_from": "Z0FBQUFBQm5sZmRvOVhkZW9kcGxqOGdac0x5TTNveFpoZVY5WWhEV3pBWWV0OWZMUmJsTUVuSzB1ZndoNE1KZVEzWW9jaFdzUlNCMmJmeVpKNFFfRW01WENPZ3o4R2xXM2p1cUktM2g3ZHhWc1hQTGdTZUtDOEhOUWMxeUtKVVNFUjRjR3gtYkY2VFU=",
      "user_to": "Z0FBQUFBQm5sZmRvT2wzT254RThGVWw0Y1F1WEg4QzVsaGxBTTlwSThxZkxwQjBDVEZlUGk0MkVqc1ZOLWVUUFA5UG02ZEIyWEY2dXlVYVhxazdtaU5IZThwTjhZcXFRUncwaXVjd3NWa2lLZkdXYTRUVDdfWlhicFMzTVBTTXE3T0tpcVlvajFpWE4=",
      "content": "Z0FBQUFBQm5sZmRvNThZbWpjZTFvRHZ4dkV0ZXptaUViNGx0aVFyLUdVbGJhN1I0Q0ZRTTZJODNLRlhFQnp0ZlRqaXh1Uk42bjlZZzhkQ3hVYVNOVUFyQ19oNUx5N3lpNGc9PQ=="
    }
  },
  {
    "id": "16006619-c330-4a13-b325-8b82e0ff9327",
    "encrypted": {
      "id": "70713899-f623-4576-9345-c950f97b1a14",
      "created_at": "Z0FBQUFBQm5sZmRqSFBMTzA2c3pnWlYyZDdaa01SejNEdFlsalFubjlEUDZKUG9mLW5MNVA3NktTcVJEV1dBVElTUXdRWGFtblpxRFA3SFVnS2tseTE4UWZvV290ay1iTWR5UVRuR280RDhHMWlLYjJkWEdWN1U9",
      "user_from": "Z0FBQUFBQm5sZmRqemhyZWdMTTljekxVY0hNZGNNMFJyVXJtX01DZV90aEZGQWtrSTZLLTdSc3hzdTltTVlXZS1aNEVYdjVQTTA2b2xzaWEwVnJRc2dhZVlXSmdzQTNBZU5POVRKZUJ4V3gxQ3k3Y2F3QzZzTm1xVmpqdVZjYXNkNU9QQy1zUmp3b1o=",
      "user_to": "Z0FBQUFBQm5sZmRqSnBsZ0prZWY1UFE5TjBBQi1GTHdsazUxTVY3S2tzMElrOUVfcjdKLXBqMnBzQV95bFZ3a0w4N2lvU1kteEdFREthWlRsbWxDLU45OHZScHU0OFJQZzNFYW5vSWhYUGJYY2V5d0NhZ1B0Unh4ZmNvOVc2NzBZeDdLcHFsWE9xZ0I=",
      "content": "Z0FBQUFBQm5sZmRqRnZkSnExNm80YVlMM1lZYzlDbUl6dklwUUdpbUhtWU1DRjZONDgzOGZIN0RXWTZhRkwybllkdHU5V3BaTGlXOTRXTGNOcFVONkoyQ3NFQ3FkVERJR1pJdnZ5eFVqZUlDc0Ewak9qVW9jeE9DZWRxaTc4ay0weUt0VThaYlJDX0NNN0NsSnVkY1k2VHd6N1BwRVRGalpaa0c0MkxvQUtfYUVOUFJ5LU91dXVFPQ=="
    }
  },
  {
    "id": "85d2125f-9f89-4a13-b9ac-adb8731895a9",
    "encrypted": {
      "id": "6de6a9e2-1099-4c61-8b9b-96addafb485f",
      "created_at": "Z0FBQUFBQm5sZmQ3NkFOLXJSc1RRVUVQRnFEV0tRQmdzenMwbzhWNmZZNl9zdmpSMnZOODZCUU5IckFiT0xLdWMwQkw1aDZwUVFMY2w5YWllTXgxa0h5Q0pqWmtSbjBhV3B4dzB1UWtEcktPWmtPV0ljTVpIT009",
      "user_from": "Z0FBQUFBQm5sZmQ3bDRSUmdzV2VtektaaUF3Zmo2bUliYWktbGF6Nk9LZDRmcXRNdEp0cjNTMWo3c2J3VEtNVzY2Umc4QWhuWGRkMGdWTGR0dkxjckRnZVdoWVRHcWI5cUhSMEVMX2ZwdVNxRjBEdEFtZ0xMQUV0Q1d6Nmh3RjR4eFZEYVo2MEFrTEE=",
      "user_to": "Z0FBQUFBQm5sZmQ3VUdLQk1wLWpKU1ZHX1VoQjJZOENOYWl1X3B5UVNiOFI1RFZFR290REdoSHNncHRJWVV3a24ycE1TbmhxX1NBZmgybzJnMlEtX3RCU1NEWEhvYjRtb0R0cGdOaVV4LVBoS1B0dzNPSDF0MjYyODFUOGdlWHRGSjIxb3JKZ3NHYXM=",
      "content": "Z0FBQUFBQm5sZmQ3SG5OMWhRYVQwSWRoM1RSeEpGd2FocjJuUGo1Y3pORU1qYk5wa3gtaWxWVUR1ZUhkeml1V2l4SWVQX0xoOXQ3dHI1SnJwTFN5dTFHTGN6Tmc1Y3daSFJIZmt2NmxKZk50aTZDYlBSMjhQQjg9"
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
        "id": "85d2125f-9f89-4a13-b9ac-adb8731895a9",
        "encrypted": {
            "id": "6de6a9e2-1099-4c61-8b9b-96addafb485f",
            "created_at": "2025-01-26T08:51:07.458010",
            "user_from": "b1ca7b79-c75e-4353-8e9c-29a960150621",
            "user_to": "f616641a-e31e-4abe-90e1-3201b073594b",
            "content": "Yeah makes sense!"
        }
    },
    {
        "id": "b208a0bb-297f-45c7-84ce-ea82b739689e",
        "encrypted": {
            "id": "c407ad1c-ad2d-4829-b889-f027ab0d1e84",
            "created_at": "2025-01-26T08:50:52.816386",
            "user_from": "f616641a-e31e-4abe-90e1-3201b073594b",
            "user_to": "b1ca7b79-c75e-4353-8e9c-29a960150621",
            "content": "Yes, but we cant communicate via normal channels - let's use the encrypted service"
        }
    },
    {
        "id": "1e1a2958-823f-41ca-8605-a447eb08afc9",
        "encrypted": {
            "id": "cd25aa72-d2f8-4594-841b-47647cc42b6d",
            "created_at": "2025-01-26T08:50:48.566052",
            "user_from": "b1ca7b79-c75e-4353-8e9c-29a960150621",
            "user_to": "f616641a-e31e-4abe-90e1-3201b073594b",
            "content": "omg seriously?!"
        }
    },
    {
        "id": "16006619-c330-4a13-b325-8b82e0ff9327",
        "encrypted": {
            "id": "70713899-f623-4576-9345-c950f97b1a14",
            "created_at": "2025-01-26T08:50:43.014737",
            "user_from": "f616641a-e31e-4abe-90e1-3201b073594b",
            "user_to": "b1ca7b79-c75e-4353-8e9c-29a960150621",
            "content": "I have something really important to tell you but it must remain private"
        }
    }
]
```
