# prisma-cnns
Prisma Cloud CNNS initiatives, deployment scripts and materials.

## I. Microsegmentation firewall rules generator

### Demo

[![IMAGE ALT TEXT](http://img.youtube.com/vi/_ODR050KmeM/0.jpg)](https://www.youtube.com/watch?v=_ODR050KmeM "Prisma Cloud Firewall Policy Generator - Demo")

### Procedure

The version 1.0 of the script is for a greenfield scenario. It is possible to append new firewall rules to the existing entries. It is a subject for the next release.

The procedure to generate CNNF/CNNS microsegmentation rules based on Prisma Cloud observations.

#### Step 0. Do the backup of existing firewall rules. 

Do the backup at _Compute > Defend > CNNF/CNNS > Export icon_
    
The configuration can be reverted back at any time. The imported policy overwrites the existing one.

**DO NOT SHARE publicly your exported csv file as it contains the token!**

<img width="326" alt="image" src="https://user-images.githubusercontent.com/36215334/201353947-693dff01-7d1a-447a-aa47-310d79fe9cd8.png">

##### Step 1. Add any to any observation rule. 

Upload the file: [cnns-initial-policy.json](/fw-rules-gen/cnns-initial-policy.json) at _Compute > Defend > CNNF/CNNS > Import icon_
**OR** configure the monitoring rule manually.

<img width="1428" alt="image" src="https://user-images.githubusercontent.com/36215334/201267312-2c455f6a-5a6d-4baa-9cfa-89a81dd5b220.png">

##### Step 2. Wait for observation results. 

Check over time if the counters are going up at _Compute > Monitor > Events > CNNF/CNNS for containers_

<img width="1410" alt="image" src="https://user-images.githubusercontent.com/36215334/201266569-8b833d03-25f0-413b-945e-9b49e5f8340b.png">

##### Step 3. Export audit logs to a CSV file. 

Get the CSV file from _Compute > Monitor > Events > CNNF/CNNS for containers > CSV icon_

##### Step 4. Use the generator/script to transform audit logs to firewall rules.

You can run a rule generator as a Jupyter notebook or a Python script. Both require the Pandas Python library which is included for the future data science and ML purposes.

##### 4.1 Use a Jupyter notebook [cnns-events2rules-v1.0.ipynb](/fw-rules-gen/cnns-events2rules-v1.0.ipynb) to generate rules.

By default produced rules are in Alert mode, it can be changed to Allow.

Set your file names

    file_in = "INSERT_FILE_NAME.csv"
    file_result = "INSERT_FILE_NAME.json"

Choose the rule effect

    Available rule effects: "allow" OR "alert" OR "prevent"
    Default rule_effect = "alert"

Run the notebook.

##### 4.2 Use a Python script [cnns-gen.py](/fw-rules-gen/cnns-gen.py) derived from the Jupyter notebook with parametrization.

Default script arguments are:
RULE_EFFECT = "alert", INPUT = "in.csv",  OUTPUT = "out.json"

Run the script with default settings or use your own argument values.

    python cnns-gen.py -h
    usage: cnns-gen.py [-h] [-e RULE_EFFECT] [-i INPUT] [-o OUTPUT]

    CNNF/CNNS firewall rules generator v1.0

    optional arguments:
      -h, --help            show this help message and exit
      -e RULE_EFFECT, --rule_effect RULE_EFFECT
                            rule effect (default: alert)
      -i INPUT, --input INPUT
                            image input (default: in.csv)
      -o OUTPUT, --output OUTPUT
                            image output (default: out.json)

Example script usage:

    python cnns-gen.py -e allow -i twistlock_firewall_network_container_audit_11_11_22_11_26_05.csv -o fw-rules-to-be-imported.json

##### Step 5. Import a JSON output file to CNNF/CNNS. 

Import the output file at _Compute > Defend > CNNF/CNNS > Import icon_

It can take roughly 10 seconds per each 150 rules for the Console to finish and confirm the task.

The screenshot attached below depicts importing rules in CNNF in the self-hosted Console. The same applies to CNNS in the SaaS Console.
<img width="1398" alt="image" src="https://user-images.githubusercontent.com/36215334/201305181-4ba38316-7052-4972-abce-35a8214183e7.png">

Collections are configured by the same import.
<img width="717" alt="image" src="https://user-images.githubusercontent.com/36215334/201310951-ef459453-7a97-46b1-b475-167c2cd66969.png">

