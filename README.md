# Crypto / Coin Price Scraper-API & WebApp

A scalable, asynchronous, and analytics-driven cryptocurrency data platform for monitoring, comparing, and analyzing real-time coin market movements across multiple exchanges.

## Problem Statement 

Cryptocurrency markets operate 24/7 — prices fluctuate within seconds across exchanges.
For traders and analysts, tracking multiple coins in real-time, comparing historical trends, and reacting to market shifts is often:

   - Fragmented across multiple APIs

   - Limited by paywalls or slow scripts

   - Time-consuming and technically complex

The Coinlytics project eliminates these pain points through a unified API and analytics dashboard that aggregates, stores, and visualizes live crypto data efficiently.  

## Solution 

### Project Overview

Developing a scalable webApp Crypto/ Coin Price Scraper API tool designed to provide a high-performance data pipeline for:
   - Real-time price data of determined cryptocurrecies & market cap scraping from multiple sources   
   - Real-time exchange rates conversions (e.g., BTC→USD, ETH→EUR)
   - Provide comparative analytics between coins as well as historic trend visualization.
   - Provide real-time alerts (email/SMS) when a coin crosses a user-defined threshold. 

## Core Architecture 

The system is built on modular, event-driven architecture designed for performance and scalability. 

 
### TechStack 

 🧷 Backend Config:
   
   ✔️ Python3 & Django - The core framework used for its mature ecosystem, and a built-in and adjustable admin panel.  
   
   ✔️ DjangoRest Framework (DRF) - Allws for building robust, secure and scalable APIs
   
   ✔️ Djoser: implemented to simplify authentication flows like login, logout, password reset, and JWT support. Once the MVP is developed, the authentication setup will be transitioned to using keycloak to handle advanced role-based access control. 
   
   ✔️ PostgreSQL - Used as the main relational database for storing user data, coins and historical prices. 

   ✔️ Redis - Used to support data caching (e.g., for coin data) and handling expirations (e.g., alerts)

   ✔️ Celery - Help schedule background scraping tasks 


 🧷 Frontend Config:
   
   ✔️ Html & CSS - Used to develop a simple UI for the MVP and testing objectives.

   ✔️ React (Planned) - To be used as the final stack for developing a SPA dashboard for providing live coin tracking, analytics and visualizations. 


📈 Analytics & Visualization

   ✔️ Matplotlib / Seaborn / Plotly: For generating line charts, bar charts, and comparative graphs.

   ✔️ Pandas: Used for cleaning and analyzing historical price data.




### Advanced Integrations 

##### Automated Logging System

A unified logging system captures lifecycle events across:

   - HTTP requests

   - Database connections

   - Celery task execution

Implementation Highlights:

 - File-based logger (coinlytics_system.log)

 - Timestamped entries using Django’s timezone.now()

 - Lifecycle hooks via Django and Celery signals:

    - request_started, request_finished

    - connection_created

    - task_prerun, task_postrun, task_failure

Example Log:

         [2025-10-20 14:22:10] [INFO] Request started: GET /api/coins/
         [2025-10-20 14:22:11] [INFO] 🚀 Celery Task Started: scrape_coin_prices
         [2025-10-20 14:22:11] [INFO] ✅ Celery Task Completed: scrape_coin_prices

    

### Security & Data Integrity

- HTTPS enforced for all API communications

- Redis HMAC signing for protected cached data

- Strict CORS and CSRF configurations

- JWT authentication (via Djoser)

- Future plan: Keycloak integration for enterprise-grade RBAC



### 🧪 Testing, Monitoring & Dev Tools


| Tool                        | Purpose                              |
| --------------------------- | ------------------------------------ |
| **pytest / DRF TestClient** | Unit and integration testing         |
| **Postman**                 | Manual endpoint testing              |
| **Celery Flower**           | Task monitoring dashboard            |
| **Custom log reports**      | System and task performance tracking |



### Future Ongoing Enhancements

📊 Interactive React dashboard

🧠 AI-driven anomaly detection for coin volatility

📨 Push notifications (WebSocket-based alerts)

🔄 Exchange integration with Binance, Kraken, and CoinGecko APIs