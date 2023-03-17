# Varys Web Crawler and Backend
Refer to [Project Varys Documentations](https://youzu.feishu.cn/docx/Mf3cd0xkLoFhwdxhvaDcUJronn9) for more details. \
Refer to [API Documentation](https://youzu.feishu.cn/docx/DqopdXA7novAzCxbhwHckR7tnie) for what each API does.

## Installation
Clone this repository into your directory.

```
bash
git init
git clone https://ygitlab.southeastasia.cloudapp.azure.com/youzu_ai/new-varys/backend-service.git
cd backend-service
```

## Setup
You will need to make an `.env` file in the root directory of the repository.
```
touch .env
vim .env
```

and download the `.env` file [here](https://youzu.feishu.cn/docx/Mf3cd0xkLoFhwdxhvaDcUJronn9).
After saving the `.env` file, just run `docker compose up -d --build` in the same root directory to get it set up instantly.
```
docker-compose up -d --build
```

You will also need a postgres folder with postgres files. Run this if you do not have one automatically from docker compose up.
```
make migrate
```

## Alembic Commands
Notes on useful commands. You can find more in backend-service/Makefile


You can populate your postgres database with test data. This is 
```
make populate
```

You can run tests with this. Ensure that you have a database named test before running. This database is auto-generated via bash from file backend-service/01-init.sh \
If it complains you don't have test database just manually create one through pgadmin. \
tests are found in the backend-service/backend/app/tests/api folder.
```
make tests
```

You can check over your code with this. Note that you have to pass this or pipeline won't pass.
```
make check
```

If you made a new table to add, use this. It autogenerates an alembic revision file that you can then name.(please keep revision id in front) \
These alembic files can be found in backend-service/backend/migrations/versions \
Example Generate: 6d7891c90db8 \
Rename to: 6d7891c90db8_follower_count_update
```
make migrations
```

You can get alembic to create your postgres database with this command. \
postgres must be in backend-service folder.
```
make migrate
```

## Usage
You can access the Swagger UI through `http://localhost/api/v1/docs`. \
You can access pgadmin UI through `http://localhost:4000/`.

You can create an account and authenticate through `api/v1/create` and `/api/v1/auth/login` respectively using Postman or on the Swagger UI Docs. \
Depending on the domain that you're using for the backend (https://varysdev.southeastasia.cloudapp.azure.com, in this case), to access the backend API endpoint:

```
https://varysdev.southeastasia.cloudapp.azure.com/api/v1/data?platform=twitter&page=1&size=2
```

Example output for Data Endpoint:
```
{
  "items": [
    {
      "post_id": 1244388,
      "game": "Echocalypse",
      "platform": "Twitter",
      "country": "Global",
      "author_name": "QuerySurge",
      "content": "42\nPromoted",
      "post_date": "2023-03-09",
      "platform_data": {
        "likes": 42,
        "replies": 0,
        "retweets": 3,
        "hyperlink": "https://twitter.com/QuerySurge/status/1610653190696869889/analytics",
        "author_tag": "@QuerySurge",
        "follower_count": null,
        "author_location": "New York, NY"
      },
      "tags": [],
      "processed": true,
      "parsed_content": "42\nPromoted",
      "detected_language": "en",
      "ai_data": {
        "label": "positive",
        "probability": 0.849022388458252
      }
    },
    {
      "post_id": 1319663,
      "game": "Echocalypse",
      "platform": "Discord",
      "country": "Japan (2013005)",
      "author_name": "orurisu#3896",
      "content": "ユーザー名：オルリス\nサーバー名：JP-ホアレス\nUID：19590\n今日の一言：宿舎の3階\n当日ゲームスクショ：",
      "post_date": "2023-01-19",
      "platform_data": {
        "replies": {},
        "author_id": 371276432632184800,
        "hyperlink": "https://discord.com/channels/928110438217048194/1063449318595514450/1065469564260974653"
      },
      "tags": [],
      "processed": true,
      "parsed_content": "User name: Olly server: J-Horeres, UID: 19590, today's one word: Game scoop on the third floor of the inn.",
      "detected_language": "ja",
      "ai_data": {
        "label": "negative",
        "probability": 0.5504811406135559
      }
    }
  ],
  "total": 153610,
  "page": 1,
  "size": 2
}
```
