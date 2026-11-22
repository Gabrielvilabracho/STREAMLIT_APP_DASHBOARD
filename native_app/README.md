# Streamlit radial dashboard

This demonstration displays three Plotly charts with synthetic data: two radial
bands, category bubbles, and cumulative areas. It does not read consumer tables,
perform OCR, or call Cortex or any external service.

## Open the dashboard

Open the installed application in Snowsight and choose an existing warehouse
when prompted. Running the app consumes warehouse credits. Your account role
must have access to that warehouse and to the application's `viewer` role.

The app uses the warehouse runtime with Python 3.11 and Streamlit 1.52.2.
Dependencies are resolved from the Snowflake Anaconda Channel. An administrator
may need to acknowledge the External Offerings Terms and allow the packages.

The package includes no data ingestion, tables, compute pools, or background jobs.
