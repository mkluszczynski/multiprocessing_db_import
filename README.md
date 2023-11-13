# Multiprocessing db import 🗃️💻

## Set up

First copy .env.example file as .env file and fill all configuration details:

```bash
cp .env.example .env
```

Then use script to create docker instance of database: 

```bash
cli/start_db
```

Remember to download all dependencies:

```bash
pip3 install -r requirements.txt
```

Now you should be good to go.

If you're working on Windows, to set up a docker paste this into the terminal:
```bash
docker compose -f docker/docker-compose.yaml up
```