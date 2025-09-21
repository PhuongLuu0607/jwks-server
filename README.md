JWKS Server – CSCE 3550 Project

This project implements a basic JSON Web Key Set (JWKS) server using FastAPI.
It supports RSA key generation, key expiry, and JWT issuance with unique kid values.
The server is for educational purposes only.

✨ Features

🔑 Key Generation
Generates RSA key pairs (private + public).
Each key is assigned a unique Key ID (kid).
Keys expire after a configurable time window.

🌐 JWKS Endpoint (/.well-known/jwks.json)
Serves all unexpired public keys in JWKS format.

🔒 Auth Endpoint (/auth)
Issues a JWT signed with an active key.
Supports ?expired=true to issue a JWT signed with an expired key.

🧪 Testing
Includes pytest unit tests with >80% coverage.
Verified against the provided blackbox test client.

Project Structure:
jwks-server/
main.py            # FastAPI server with JWKS + Auth endpoints
keys.py            # RSA key generation and JWK conversion
tests/test_app.py  # Pytest test suite
requirements.txt   # Dependencies
README.md          # Project documentation
screenshots/       #Screenshots of test client and test coverage

Install dependencies: pip install -r requirements.txt
Run the Server: uvicorn main:app --reload --port 8080
Endpoints to Test: 
# JWKS (active keys only)
curl http://localhost:8080/.well-known/jwks.json

# Request a valid JWT
curl -X POST http://localhost:8080/auth

# Request an expired JWT
curl -X POST "http://localhost:8080/auth?expired=true"

Run unit tests with coverage: pytest --cov=.

Blackbox test: 
cd ~/Downloads/CSCE3550_Darwin_arm64
chmod +x gradebot
./gradebot project1
