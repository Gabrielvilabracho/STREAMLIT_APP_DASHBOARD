# Streamlit dashboard for Snowflake

Run the same dashboard locally, as Streamlit in Snowflake, or as an installable
Snowflake Native App. All three charts still use synthetic data. This adaptation
does not implement OCR, Cortex calls, or queries against Snowflake tables.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501. Stop the server with Ctrl+C.
`requirements.txt` remains the local dependency list. Snowflake's warehouse
runtime uses `environment.yml` instead; do not install it with pip.

If the project folder was renamed, an existing virtual environment's activation
scripts can still reference its old location. Recreate the environment at the
new path before relying on activation. For the existing tested environment in
this checkout, you can run directly without activation:

```bash
.venv/bin/python -m streamlit run app.py
```

## Deploy a Native App in your development account

The following commands create or update objects in Snowflake. They are not part
of local validation. Use a development account and an existing warehouse.

Prerequisites:
- Snowflake CLI 3.14 or later, with an authenticated named connection configured
  outside this project. Never add credentials to these files.
- A role with `CREATE APPLICATION PACKAGE` and `CREATE APPLICATION` on the account,
  plus `USAGE` on an existing warehouse. Creating and updating an existing package
  or application also requires the relevant ownership privileges.
- Access to the Snowflake Anaconda packages and acknowledgement of the External
  Offerings Terms by an authorized administrator, if required.

From the project directory, first inspect the local package (no Snowflake login
or remote changes required):

```bash
snow app bundle
```

Replace `YOUR_CONNECTION` and `YOUR_EXISTING_WAREHOUSE` below with your configured
connection name and warehouse identifier. Review the object names in
`snowflake.yml` before running:

```bash
snow app run --connection YOUR_CONNECTION --env warehouse=YOUR_EXISTING_WAREHOUSE
snow app open --connection YOUR_CONNECTION --env warehouse=YOUR_EXISTING_WAREHOUSE
```

`snow app run` uploads the explicit artifact list, validates the setup script on
Snowflake, and installs or upgrades a development application. It creates the
`STREAMLIT_DASHBOARD_PKG` package, its `APP_SRC.STAGE` stage, and the
`STREAMLIT_DASHBOARD_APP` application. It does not create a warehouse.

To share the installed app, an authorized administrator can grant its role:

```sql
GRANT APPLICATION ROLE STREAMLIT_DASHBOARD_APP.viewer TO ROLE YOUR_VIEWER_ROLE;
GRANT USAGE ON WAREHOUSE YOUR_EXISTING_WAREHOUSE TO ROLE YOUR_VIEWER_ROLE;
```

Viewers may need to select their warehouse when opening the app. Warehouse use
incurs credits even though the chart data is generated in Python.

This is an **internal development package**, not a Marketplace publication.
Distribution to other accounts requires a separate release/listing workflow and
the applicable Snowflake validation. No listing or release is created here.

## Deploy only as Streamlit in Snowflake

If you do not need an installable application, use the same source directly:

```bash
snow streamlit deploy dashboard --connection YOUR_CONNECTION --database YOUR_DATABASE --schema YOUR_SCHEMA --env warehouse=YOUR_EXISTING_WAREHOUSE --open
```

The deployment role needs `USAGE` on the database and warehouse, and `USAGE`,
`CREATE STREAMLIT`, and `CREATE STAGE` on the schema. Review existing object names
before deploying. To intentionally update this standalone app, repeat with
`--replace`. This command does not install the Native App.

## Compatibility and validation

| Area | Behavior |
|---|---|
| Runtime | Warehouse, Python 3.11, Streamlit 1.52.2. No compute pool needed. |
| Dependencies | Snowflake channel; NumPy 2.x, pandas 2.2.x, Plotly 6.x. Account policies and package resolution still require validation. |
| Accessibility | Newer Streamlit gets chart `alt` text; 1.52.2 gets a visible caption instead. Captions are not equivalent to native chart ARIA labels. |
| Page settings | Only `layout` is set; unsupported page-title/icon/menu settings are omitted. |
| Source | `app.py` and `chart_display.py` are shared, not duplicated for deployment. |
| Package safety | Explicit artifact list excludes `.venv`, secrets, tests and `preview.html`. |
| Permissions | The app grants only access to its own UI. No consumer-table references or external integrations. |

Run the regression tests locally:

```bash
python -m unittest discover -s tests -v
```

For a closer local check, use a **separate** Python 3.11 environment with
`streamlit==1.52.2`, `numpy==2.2.6`, `pandas==2.2.3`, and `plotly==6.3.0`.
Passing local tests does not certify Snowflake installation or Conda resolution.
After deployment, verify all three charts, hover values, widths, viewer-role
access, and the warehouse selection in Snowsight. `preview.html` is a separate
approximation and is not used by the deployed app.

### Local checks performed

- Snowflake CLI 3.34.0 successfully built the six-file Native App bundle.
- All three regression tests passed on the existing Python 3.13 / Streamlit
  1.67.0 environment and an isolated Python 3.11 / Streamlit 1.52.2 environment.
- The generated bundle's entrypoint loaded three charts and five captions on
  Streamlit 1.52.2 without exceptions.
- A temporary localhost server on Streamlit 1.67.0 returned three charts with
  `ready` status on first load and rerun through the agent API. It was stopped
  after verification; the agent API is not enabled in deployment configuration.
- Ruff lint and ty type checks passed. No account connection, remote SQL
  validation, warehouse use, or Native App installation was performed.

## Files

- `snowflake.yml`: CLI definitions and source-to-package artifact mapping.
- `native_app/manifest.yml`: installation metadata and default Streamlit UI.
- `native_app/setup.sql`: versioned UI schema and application-role grants.
- `environment.yml`: warehouse-runtime dependencies, beside `app.py` in the bundle.
- `chart_display.py`: compatibility for chart descriptions across Streamlit versions.

To undo the local adaptation, remove the deployment files and tests, restore the
original direct chart calls and page settings in `app.py`, and remove
`chart_display.py`. This does not uninstall remote objects. Remote cleanup must
be reviewed separately; no automatic teardown is performed.

## Official references

- [Native Apps with Streamlit](https://docs.snowflake.com/en/developer-guide/native-apps/adding-streamlit)
- [Supported versions and dependency management](https://docs.snowflake.com/en/developer-guide/streamlit/app-development/dependency-management)
- [Native App CLI project definitions](https://docs.snowflake.com/en/developer-guide/snowflake-cli/native-apps/project-definitions)
