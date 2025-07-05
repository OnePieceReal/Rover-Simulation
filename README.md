# 🛰️ 2D Rover Simulator

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.1-green)
![React](https://img.shields.io/badge/React-19%2B-blue)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Messaging-orange)
![gRPC](https://img.shields.io/badge/gRPC-Protocol-lightgrey)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4%2B-teal)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow)

---

## 📑 Table of Contents


- [📜 Project Description](#-project-description)
- [🧭 Commands](#-commands)
- [💣 Mine Disarmament](#-mine-disarmament)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Backend Setup (FastAPI Server)](#-backend-setup-fastapi-server)
  - [🌐 Frontend Setup (React)](#-frontend-setup-react)
- [📸 Preview/Result](#-preview-result)

---

## 📜 Project Description

This project simulates a 2D rover navigating a terrain filled with hidden mines. The rover interprets movement commands, avoids obstacles, and disarms mines using a proof-of-work-based hashing mechanism.

---

## 🧭 Commands

- `L` — Turn the rover left
- `R` — Turn the rover right
- `M` — Move forward one step in the current direction
- `D` — Dig and attempt to disarm a mine at the current location

---

## 💣 Mine Disarmament

Each mine is associated with a **unique serial number**. To disarm it, the rover:

1. Generates a random **PIN** and prepends it to the serial number.
2. Hashes the result using **SHA-256**.
3. Checks if the hash starts with **six leading zeros (`000000`)**.
4. Repeats the process until successful.

This mimics a basic **proof-of-work** algorithm similar to blockchain mining.

---

## 🚀 Getting Started

### 🔧 Backend Setup (FastAPI Server)

```bash
# Install FastAPI and Uvicorn
pip install fastapi==0.115.1 uvicorn==0.34.0

# Run the FastAPI server
uvicorn Fastapi_Rover_Server:app --reload

# API Root: http://127.0.0.1:8000
# Swagger UI: http://127.0.0.1:8000/docs
```
### 🌐 Frontend Setup (React)

```bash
# Navigate to the frontend directory
cd frontend

# Install all dependencies
npm install

# Start the development server
npm run dev
```
### 📸 Preview/Result


<p align="center">
  <img src="Preview/map-mine.PNG" width="800"/>
</p>

<p align="center">
  <img src="Preview/rover.PNG" width="800"/>
</p>
<p align="center">
  <img src="Preview/rover-8.PNG" width="800"/>
</p>
<p align="center">
  <img src="Preview/rover-10.PNG" width="800"/>
</p>
