# Run wis2box using test-data

Download the archive and unzip it:

```
wget http://10.0.2.222/wis2-training-materials/wis2box-training.zip
unzip wis2box-training.zip
```

Go into the new directory:

```
cd wis2box-training
```

## review the test-data-setup

Copy test.env to dev.env:

```
cp test.env dev.env
```

Review the contents of test.env. 

```
more test.env
```


- What is the directory defining the wis2box-data-directory on the host?

Review the contents of this directory: 
- Inspect the content of data-mappings.yml, what topics are configured in this file ?
- Inspect the content of metadata/station/station_list.csv. How many stations are defined in this file?
- Inspect the content in the 'observations'-directory. What is the data-format used? What type of observations are reported in this file?

## start the wis2box

To start the wis2box type:

```
python3 wis2box-ctl.py start
```

Wait until the command has completed.
After that, inspect the status as follows:

```
python3 wis2box-ctl.py status
```





