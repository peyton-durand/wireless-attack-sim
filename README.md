# wireless-attack-sim

A simulation of wireless availability attacks (jamming, RACH flooding, carrier sense exploits) with countermeasures. Built for CPTS 427 at WSU.

## Setup

### Backend
* cd backend
* python -m venv venv
* venv\Scripts\activate
* pip install -r requirements.txt
* uvicorn api.main:app --reload

### Frontend
* cd frontend
* npm install
* npm run dev
