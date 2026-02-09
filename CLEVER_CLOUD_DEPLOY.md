# Deploying Diogen to Clever Cloud

This guide describes how to deploy the Diogen FastAPI application to Clever Cloud.

## Prerequisites

- A [Clever Cloud account](https://www.clever-cloud.com/).
- Check that your project has a `requirements.txt` file (already present).
- Ensure your `run` command is properly configured (we use `uvicorn`).

## 1. Create a Python Application

1. Log in to the Clever Cloud Console.
2. Click **Create** -> **Application**.
3. Select **Python** as the runtime.
4. Link your GitHub repository or push your local code to the provided Clever Cloud remote.

## 2. Configure Environment Variables

Go to the **Environment variables** tab of your application and add the following:

| Variable | Value | Description |
|---|---|---|
| `CC_PYTHON_VERSION` | `3.11` | Specifies the Python version. |
| `CC_POETRY_VERSION` | `1.4.2` | (Optional) If you switch to Poetry later. |
| `PORT` | `8080` | Clever Cloud expects the app to listen on port 8080. |
| `POSTGRES_ADDON_URI` | *Auto-generated* | Link a PostgreSQL add-on to your app. |
| `POSTGRES_USER` | *Auto-generated* | Database user. |
| `POSTGRES_PASSWORD` | *Auto-generated* | Database password. |
| `POSTGRES_DB` | *Auto-generated* | Database name. |
| `MODULE` | `api.main:app` | (Optional) If using a custom start script. |

> **Note:** For the database connection to work, create a **PostgreSQL Add-on** in Clever Cloud and link it to your application. The `POSTGRES_Uri` variables will be injected automatically.

## 3. Start Script

Clever Cloud looks for a `uwsgi.ini` or attempts to run a default command. For FastAPI with Uvicorn, it's best to create a `clevercloud/python.json` or explicitly set the **Post Deploy** or **Run** hook.

**Recommended:** Create a `clevercloud/python.json` file in your repository root (optional but good for explicit configuration):

```json
{
  "build": {
    "type": "python"
  },
  "deploy": {
    "rakia": {
      "rules": [
        {
          "is_root": true,
          "cmd": "uvicorn api.main:app --host 0.0.0.0 --port 8080"
        }
      ]
    }
  }
}
```

Alternatively, you can just set a custom **Run command** in the dashboard:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8080
```

## 4. Database Migrations

To run migrations automatically upon deployment, add a hook in `clevercloud/hooks.json` (if supported) or add it to your run command chain, e.g.:

```bash
alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 8080
```
*(Ensure `alembic` is configured and `alembic.ini` is present).*

## 5. Deploy

Push your changes to the master/main branch:

```bash
git add .
git commit -m "Prepare for Clever Cloud deployment"
git push clever master
```

Monitor the deployment logs in the Console.
