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
        "id": "18a58e3d-9dde-402e-8d18-6de72900f29a",
        "encrypted": {
            "created_at": "Z0FBQUFBQm5sZ2lsRWY2RGk2NV9CYkFGR3UteW9GV2xqZEhZZFU1eTFLQ1g3ZVlaaXFOMDdPZWxPbnpvYjlkUXpnbTFxdG5mSFV1Ni14XzREX1FvVkI5VTIyc1dqMnhqLUFfNTZKN3MtcHJQMk4xekRpdHh4SXM9",
            "user_from": "Z0FBQUFBQm5sZ2lsdlRWektHSEdSOFpGMVFKMXp1cDQxb3J1YTFOQzF0U1k3aVhINFZrRXp6emV1SDRpVU1RYVpwT2N1Z2huX3RDYVhmXzZEdWdGQWZhT2E4RXdSTjAwNEdQYjZmY0pHVUtPNDYwVUw5bE1JNjJfd0ZaYWR5cGRRXzZjVG1xWXlqR18=",
            "user_to": "Z0FBQUFBQm5sZ2lseG51LS1UYnVQN2NXbnMwTkE4UGJ0TnlCMnlnQjc0UzZfZ1AxQnJ3NWVxcFpFcUJsNEdMVjZTc2lpSkcxZ3VZaHY2TF9BejdRQ1RnT0JLd3kxazN1TXllRlBvOTR3R1ZSanViM1ZqR3AyTWloVVI1MjBnS3JoVjhSVzFxRnR1elk=",
            "content": "Z0FBQUFBQm5sZ2lsc3EwLTIwV0JHYUVORk9ITEkwdXNsNXVmRDRJRE5SOGgxRDBtcVJDZnRoZWpMODh2QTg0ck9sUnZocjhFWlEyZ05UWUZ0c3VhX0RxMGREQWUyLXBTc0E9PQ=="
        }
    },
    {
        "id": "19178939-d1f9-4504-9a1c-bf73bf5d2e31",
        "encrypted": {
            "created_at": "Z0FBQUFBQm5sZ2lsRFJ6cWdHakZxX1RpS1FUdzQzZ3ZTRHRhSjJOTk5odHRrbmNmQlNpZ0swdi1CVnRrR0VVazU1REVTZWNRQldrSFZJWUdYREhxX1A5Z1JHX3p3YTljSTdkdmRSMmNxWnJsMzUwU3J6YjJIRkE9",
            "user_from": "Z0FBQUFBQm5sZ2lscElQemxBRVNvbEI3a1U0V1ZGbFRva1NBcDEzM0hCSTQ1S3NCbHN2UktOMjR0ZU50QlYtLUdKOGNUM1E3SEJ5REZsUUJLNmF3bGVpWXIzNVZDOWVhSE1fMW5nZnREM0NodzhiWWRRWjVnUmRNY1p3bWpjYU90LWNRMXh2NlZLcGo=",
            "user_to": "Z0FBQUFBQm5sZ2lscmpISDBJUEU2Sms0Yzh6MzhYSDRTd2pIbG1wUnFzc090YTNTSDJNWmJLaXFqMzFHczFSWXRtaXlvcFZxV3VwLUhDblc0WFJ0dks1VXl6Vk93OFB2QnBzd2JHcURfNzI3djViZ3Q1SmJwWXVUQjRQWVhyT3V1NF9zbUtGNVJLVVk=",
            "content": "Z0FBQUFBQm5sZ2lsY2tTSVBKSkktUGhRYkp5RFNVcmN5U1JveGJNbUp3Z0FkM3phZ0RFLVJkdnVLWHU3QlJJZURnSU9TYV9iV0h4MWRyQjF4NWN3SVdUeTZxQzkxbFBXc3pxUTBXSS1GWEtZTmtpbGNYWk1USllqVlZPR2lSclEtV3JOamdJVld4ZEl4V3RRNHphV0ExMmczbHhRRWFhaGZjaXZsMm81V3ZWSnl6blpxa1dkYnNpMzdUT0pWNDctd21tMGtza1M2TGRp"
        }
    },
    {
        "id": "2969e1c8-d855-4d02-bfaa-81d7c6871596",
        "encrypted": {
            "created_at": "Z0FBQUFBQm5sZ2lsMjNUdHF1em5tMm9qWDRTdGQ4LUotV0dEN2lFZHcyXzkydDc1TzZWWUFRbDVOUVhZeUt5VmxvbmM1bFJpaExyQlVHNXZYZktyVUJtVXpYTVJKM1JYbVFpV1NfenlDOHcxTXZSUnpsQlBXYzg9",
            "user_from": "Z0FBQUFBQm5sZ2lsU0VkeG50VWs4TmlERUhMaVc4UWFIdXZxcG04UUZIWkNWMHM1alNFYkhNaHhvY3VKMWJTTk44ZmhrRFNXd3hhZ0sxaEpfWDAwMFNVclowXzFZa3ZpdFRBTzhtVjM5QlpqQzc4QmhyVTdSQUI0UV94SGZidDc5TzdHQ0lCSXlUSTA=",
            "user_to": "Z0FBQUFBQm5sZ2lsczN6MTRYRW9tY0xrWEVMSVVjQ0JhWkRoRWk3VUtocENndXdBYmpnX0Y1QVpmTS01YlFFU3NkWGN6M0tkVC1lR3ZLN0lqWjhrOUU1Yl90MlZhM0xMQTZnbDhjLVdrR1BQM1lmZzJfbS10U1ZoWDNib3BPR0VRVlBkbjMtaEk0R2c=",
            "content": "Z0FBQUFBQm5sZ2lsQ2g5Z29NWXpzRXVneDFDSjVkaHF5UkxPVjh3NGtvZE5kZVU0a1lmOTVUQUVjX3JrSTFBb0JaRElhQ1Z5c1ctQnBWZ0NQWm9CQkxkRXFOY0lad1BDT0JGdDE1TnhHWFVBYnlsc1pfMGY3Z289"
        }
    },
    {
        "id": "9192eeaa-e39f-4c4b-acf5-17b1bd4402e9",
        "encrypted": {
            "created_at": "Z0FBQUFBQm5sZ2lrNTJfa2xtWkl4djBpa1cycWJHMTNsc1I0YjhsY09GQk5kYVZaUTI5STZJWGF2NmRSb0YtX003T3NIa1FIZVFaZ3RGa2ptWGRsaTBZcXRTQW5jVHZZM0pFeTZIdFZtT3U5TTY0OGVkdUdSWXc9",
            "user_from": "Z0FBQUFBQm5sZ2lrTXRxMTVDc0hDYnpjTUVmdTNDN2ZlTDVPeWk0amlabndMZDdrUXh6NXdteW1Lc0VyZ1JwZ0JPVkhIY3ZuTC1pcEdVMUhZa2xURWEtc3NkSXF4U3hKczU3SDlIMTUyYS1nM29rR2JZc2Q1LVJXZHdrMFpXZ1BnbHZuNXFxWHpTUi0=",
            "user_to": "Z0FBQUFBQm5sZ2lrc3hvdmF3LXBsRV9WTTdZZklCZEVta041TFU5bHh0NVotMVpneGF4c1dxdkVreUJQOUtGTU1EZXhJdVc4M29NRDE2ZVVLZVloVl9iWjlTOWx6ZzFRU2NlQmt4YkYwcmZEeUdQUmVjZ1VqdkhUQUxhNlp1ZktfNFpkS0RYOE5rUl8=",
            "content": "Z0FBQUFBQm5sZ2lrZ1Y2SnhfN0xKdXZuUm5DdUJIelRzMmRtQzVfTENPNFh5eUJ4T09QMklkTFpMMWY2cGNtUlV2dmlMYm9RQlBTNDFZQUFHOGZMLXdMUlhDVFZsal9SOHRQbzhuT3c2Y3V5MmpiaFRpS3lmUTR5am94c21haExhTXpoVXJCam1sVmxreVFva1JLLUdfNHk1MTNUTDYtYUZlLTdoMWVlTUtDMjdUVG5tZ1IzVzhRPQ=="
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
        "id": "2969e1c8-d855-4d02-bfaa-81d7c6871596",
        "encrypted": {
            "created_at": "2025-01-26T10:04:21.194432",
            "user_from": "0b1cff3d-05b7-438a-b33e-62a7e3c78714",
            "user_to": "38299f07-a533-4ceb-ba4d-bc51fa664d92",
            "content": "Yeah makes sense!"
        }
    },
    {
        "id": "19178939-d1f9-4504-9a1c-bf73bf5d2e31",
        "encrypted": {
            "created_at": "2025-01-26T10:04:21.105685",
            "user_from": "38299f07-a533-4ceb-ba4d-bc51fa664d92",
            "user_to": "0b1cff3d-05b7-438a-b33e-62a7e3c78714",
            "content": "Yes, but we cant communicate via normal channels - lets use the encrypted service"
        }
    },
    {
        "id": "18a58e3d-9dde-402e-8d18-6de72900f29a",
        "encrypted": {
            "created_at": "2025-01-26T10:04:21.023191",
            "user_from": "0b1cff3d-05b7-438a-b33e-62a7e3c78714",
            "user_to": "38299f07-a533-4ceb-ba4d-bc51fa664d92",
            "content": "omg seriously?!"
        }
    },
    {
        "id": "9192eeaa-e39f-4c4b-acf5-17b1bd4402e9",
        "encrypted": {
            "created_at": "2025-01-26T10:04:20.925932",
            "user_from": "38299f07-a533-4ceb-ba4d-bc51fa664d92",
            "user_to": "0b1cff3d-05b7-438a-b33e-62a7e3c78714",
            "content": "I have something really important to tell you but it must remain private"
        }
    }
]
```
