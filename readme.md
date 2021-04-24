<p align="center">
  <img src="logo.png">
</p>

# MMPN srsLTE Remote Sensor Guide
> ## STEP 1: Reserve Resources
>
> * Reserve srsLTE experiment resources  **srsLTE_Over_The_Air** profile
> * Reserve a PC with **single-pc** profile
>

> ## STEP2: Connect to Nodes
>
> * In **Local_Scripts** run **node_start.sh** to open up shells for EPC, eNB, UE, KafkaServer
>    * This asks for your POWDER username, location of data center, PC number(s) for the EPC(s)/eNB(s), PC number for the Kafka server, and location of UE(s) (bookstore, meb, etc).
>
>
> * Clone this repo onto the node

> ## STEP 3: Spin up Kafka server
> _NOTE: By default, log retention is 1 minute. Edit **log.retention.ms** in **Kafka/config/server.properties** file to change this._
> * In **Node_Scripts** run in order:
>     * **Install_dependencies.sh**
>     * **Kafka_Scripts/kafka _up.sh** – This starts ZooKeeper/Kafka daemons. **kafka_down.sh** terminates the servers.
>     * **Kafka_Scripts/kafka_create_topics.sh** – This creates a list of topics from user-input
>     * ***Test

> ## STEP 4: Spin up srsLTE
> _NOTE: Set your **node identifier** to be of the form: **[node type][#]** (Ex. ue1)_
> * For each UE
>    * On the EPC node: add entries for distinct **keys** and **IMSIs** in **/etc/srslte/user_db.csv**
>    * On each UE: change the key and IMSI to ensure there are **no duplicates**
> * For each node (EPC/eNB/UE) in **Node_Scripts/srsLTE_Scripts** run **srsLTE_top.sh**
>    * Provide the Kafka server public IP (the value for advertised.listeners in the server.properties file)

> ## STEP 5: Consume/process data locally
> * In **Local_Scripts/Data_Processor** run **consumer_top.sh** and specify the Kafka server IP
>    * This script creates a consumer for each topic and reads in the log files

> ## STEP 6: _classified_
