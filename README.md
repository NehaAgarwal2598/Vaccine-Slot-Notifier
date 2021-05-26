### This project Notifies(sends you email) you of the number slots available to book a vaccine

## 1. Clone the repository - 
```bash
git clone https://github.com/NehaAgarwal2598/Vaccine-Slot-Notifier.git
```
## 2. Create a `config.py` and store the username and password in it 
```python
username="notifier@email.com" 
password="yourPasswordForTheEmail"
```
## 3. Build the docker file to create a docker image
```bash
docker build . -t {{name of image of you choice}}
```
**for example -**
```bash 
docker build .  -t vaccine-slot-notifier
```
## 4. Run the docker image
```bash
docker run -d -e DISTRICT={{District-Id}} -e EMAIL={{emailId}} --name notifier-{{District-Id}} vaccine-slot-notifier 
```
where district Id is the id assigned to district for example - for `kolkata` it is `721`
```bash 
docker run -d -e DISTRICT='721' -e EMAIL='email@address.com' --name notifier-725 vaccine-slot-notifier 
```
