# EvaDB + Plaid

This project integrates Plaid with EvaDB, in order to allow you to gain insights about all of your financial data. Plaid's comprehensive API combined with EvaDB's data store + AI layer is a perfect combination to essentially make your bank accounts intelligent. 

I designed an API Framework in Flask that allows you to sign in and authenticate any financial account using Plaid's Link component. Once you login and authenticate an account, Plaid's Transactions API retrieves the last 6 months worth of transactions, and details about them. These are then stored within EvaDB, and the AI layer can be used to create text summarizations or ChatGPT queries about the data.

## Setup

In order to setup this project, make sure you download the necessary packages listed in requirements.txt (you can create a virtual environment for this if you want). Run 
```bash
pip install -r requirements.txt
```
Then make sure to install the necessary npm packages for the frontend:
```bash
cd frontend
npm install
```
You'll also need to add an OpenAI key in order to get the ChatGPT functionality to run properly. In this case, add your key into an env file, by doing the following:
```bash
touch .env
```
Inside of the env file, enter your key:
```env
OPEN_AI_KEY='sk-...'
```
## Getting it running
In order to run this locally, you first need to start the Flask server
```bash
cd server
bash start.sh
```
You should see a message that says `* Running on http://127.0.0.1:8000 `. Then load up the frontend
```bash
cd frontend
npm start
```

<img width="1506" alt="Screenshot 2023-10-17 at 5 33 00 PM" src="https://github.com/vhegde14/plaid_evadb/assets/12666686/4556c78d-97f5-4547-8197-5d3979b38a7a">

Once the frontend is loaded up, check the messages. If your server is running properly, you should see the message `Plaid link token authenticated`. click on the button that says `Connect a bank account`. You should then see the Plaid Link component. Authenticate your bank account using the flow.

<p align='center'>
  <img width="533" alt="Screenshot 2023-10-17 at 5 34 25 PM" src="https://github.com/vhegde14/plaid_evadb/assets/12666686/356bd2e2-b2a2-46d6-b066-a09d6cffa8e6">
</p>

If you reach the frontend page again and then see the message `Link Token exchanged for Public Token`, you have succesfully authenticated your account. You can then proceed to the Jupyter Notebook and follow along in order to create the EvaDB database and perform queries on your financial data.

## Future Goals

Ideally, I want to add some future features to this. This is a Proof-of-Concept to show how Plaid's Transactions API could be integrated with EvaDB, but I want to build out a frontend to essentially be able to converse with your bank account. To do this, I also have to convert my Juupyter Notebook into actual backend code.
