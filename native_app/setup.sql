-- No account-level privileges, consumer data access or external access required.
CREATE APPLICATION ROLE IF NOT EXISTS viewer;
CREATE OR ALTER VERSIONED SCHEMA ui;

CREATE OR REPLACE STREAMLIT ui.dashboard
  FROM '/streamlit'
  MAIN_FILE = 'app.py';

GRANT USAGE ON SCHEMA ui TO APPLICATION ROLE viewer;
GRANT USAGE ON STREAMLIT ui.dashboard TO APPLICATION ROLE viewer;
