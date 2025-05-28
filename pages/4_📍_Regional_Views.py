AttributeError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/project0514/pages/4_📍_Regional_Views.py", line 27, in <module>
    m.add_ee_layer(landcover, {}, f"{region_name} 土地覆蓋 (2020)")
File "/home/adminuser/venv/lib/python3.11/site-packages/leafmap/leafmap.py", line 478, in add_ee_layer
    asset_id = asset_id.strip()
               ^^^^^^^^^^^^^^
