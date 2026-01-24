# Personal Finance Tracking System
This project is a personal finance tracking system built with a deterministic-first architecture.
All financial calculations are handled by a **finance engine**, while a local LLM (LLaMA via Ollama) is used only for explanations, behavioural insights, and suggestions - NEVER FOR CALCULATIONS.

This app is designed to demonstrate:
- Backend system design.
- Clean data modeling.
- Basic deterministic financial computation
- AI integration

## Table of Contents
1. [Prerequisite](#prerequisite)
2. [Build and Run the App](#build-and-run-the-app)
3. [Explore the app](#explore-the-app)
4. [What's next](#whats-next)

## Prerequisite
Before you begin, ensure you have the following installed:
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) (for a fully reproducible local environment with zero manual setup)
- [Postman](https://www.postman.com/downloads/) (for testing the APIs)

With these tools installed on your machine, you can run the app easily
## Build and Run the App
### Step 1: Clone the Repository
```bash
git clone https://github.com/MinhPhamLapTrinh/Personal-Finance-Tracking-System.git
cd Personal-Finance-Tracking-System
```

### Step 2: Set up Env File
```bash
touch .env.development
```
You can setup the file as same as the following one:
```bash
POSTGRES_URL=postgresql://postgres:postgres@postgres:5432/expense_tracker
SECRET_KEY="your-secret-key"
MODEL="llama3"
OLLAMA_HOST="http://ollama:11434"
```

"MODEL" attribute here can be replaced by your desired LLM model.

### Step 3: Build and Run the app using Docker

```bash
docker compose build
docker compose up
```

Check out this [LINK](https://docs.docker.com/compose/gettingstarted) for more information of using **docker compose**

**NOTE**: If you want to stick with the "llama3" model, please open another terminal and run the command for ollama to pull the llama3 model

```bash
docker exec -it ollama ollama pull llama3
```

### Step 4: What's next
Now you are all set, so you can explore the features of the app. The following information will give you an overview of how to use the feature of the app using POSTMAN.

## Explore the app
A full APIs documentation is written [HERE](https://www.postman.com/aviation-explorer-6353115/workspace/personal-finance-tracking-system)

### API Endpoints
#### Authentication
```bash
POST   /api/v1/auth/register
```
![Auth Register](images/image.png)

This route will register users. It requires username, user email, and password


```bash
POST   /api/v1/auth/login
```
![Auth Login](images/image-1.png)

For login route, it requires user email and password, it will return a backend token for other routes authorization. The other routes depend on the valid backend token. 

#### Transaction
These features are the core principle of the app:
```bash
POST /api/v1/transaction
```
![Transaction Creation](images/image-2.png)

This route is used for adding your income/expense. It requires you to specify the category name (RENT, FOOD, and so on), category type (INCOME/EXPENSE), amount, occurred time (YYYY-MM-DD HH-MM), and optional description.

```bash
GET /api/v1/transactions
```

![Transaction Retrieve](images/image-3.png)

This route will return us a list of transactions

```bash
GET /api/v1/transaction/{{transaction_id}}
```

![Retrieve a transaction](images/image-4.png)

This route will return us a specific transaction based on the ``transaction_id``

```bash
DELETE /api/v1/transaction/{{transaction_id}}
```
![Remove transaction](images/image-5.png)

This route allows us to remove a specific transaction based on the ``transaction_id``

```bash
PATCH /api/v1/transaction/{{transaction_id}}
```
![Update Transaction](images/image-6.png)

This route allows users to update a transaction. It could be an amount, a description, a category name, a category type, or the time they made it.

#### AI Insight

```bash
GET /api/v1/finance/report/{{year}}/{{month}}
```
![Get a report](images/image-7.png)

We can retrieve a report of transactions by giving the year and the month. This information is later sent to the LLM model for insight. 

```bash
GET /api/v1/finance/insights/summary/{{year}}/{{month}}
```
![AI insight](images/image-8.png)

This route allows users to receive an insight into their monthly spending through the LLM model. 

## What's next
User Interface is currently being worked on, and the app will allow users to have a conversation with AI to understand even more about their spending habits.