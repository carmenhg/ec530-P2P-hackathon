# ec530-P2P-hackathon

Author: Carmen Hurtado 

## Project Description
Create a peer to peer chat architecture. Each peer (client) will have its own local database that is implemented using SQLite. 
There is a rendezvous server that is used to set up a hadshake between the clients and can be turned off afterwards leaving us with a P2P module. 

## Database
I implemented a simple SQLite database. Each clinet would create their own database locally and save messages with the following fields.
- source
- destination
- message
- identifier number that served as the primary key for the db
## Results
I was able to open a connection between to clients standing on their own without the rendevous server on. My clients were:
- One client in my local machine
- One client on an Azure VM
Although they were able to send messages only my local client received the messages. Any messages sent from the local client to the VM was not received by the VM. I believe the BU wifi could have some rules in the Firewall blocking my messaged going out. 

Below are some images of the results

Image 1-2: Connection between clients. We can see that only on is receiving the messages

![Connection Client 1](/images/client1.png)
![Connection Client 2](/images/client2.png)

Image 3: SQLite extension for vscode to help me visualize the dbs created. Super easy to use tool. 

![SQLite extension](/images/extension.png)

Image 4: Example of client db with some inputs

![Visual DB table](/images/visual-db.png)