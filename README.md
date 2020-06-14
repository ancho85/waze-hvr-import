# waze-hvr-import
## waze high volume report importer
1. download HVR csv files to "import" directory
2. rename "config.cfg.example" to "config.cfg" and edit your mysql connection settings
3. run "python waze-hvr-import.py"
4. move csv files to another directory or delete them to prevent index errors due to data already been imported
