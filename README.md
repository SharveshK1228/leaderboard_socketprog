# Distributed Leaderboard System

| Category        | Details                                   |
|----------------|-------------------------------------------|
| Project Type   | Distributed System                        |
| Communication  | TCP with SSL/TLS                          |
| Clients        | Multiple (Python GUI)                     |
| Server         | Python with Monitoring Dashboard          |

## Overview
A real-time distributed leaderboard system where multiple clients update scores concurrently over a secure TCP connection using SSL.

## Features
- Multi-client support  
- Real-time leaderboard updates  
- SSL-secured communication  
- Conflict resolution (Last Write Wins)  
- Server monitoring dashboard  
- Premium GUI for clients  

## Architecture
Clients → Server → Leaderboard

## Security
- SSL/TLS encryption  
- Server-side certificate authentication  

## How to Run

### 1. Start Server
cd server  
python server_gui.py  

### 2. Run Clients
cd client  
python client_premium.py  

## Requirements
- Same WiFi network  
- Python 3.x  

## Concepts Used
- Distributed Systems  
- TCP Sockets  
- SSL Encryption  
- Multithreading  
- Synchronization (Locks)  
- Conflict Resolution  
