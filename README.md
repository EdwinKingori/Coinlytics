# Crypto / Coin Price Scraper-API & WebApp

## Problem Statement 

In the current world of evolving crypto currencies, coin prices fluctuate rapidly across different exchanges. Traders and investors  often struggle to:
   - Monitor multiple coins in real time,
   - Compare coin performance over time, 
   - Get real time alerts when prices spike &
   - Analyze coin behavior with historical trends.  

To many, these tasks are trivial, but they often require users to visit multiple sites using third-party platforms with limited free access or with written scripts, which is time consuming, technical or costly.  

## Solution 

1. Project Overview
Developing a scalable webApp Crypto/ Coin Price Scraper API tool designed to scrape:
   - Real-time price data of determined cryptocurrecies from multiple sources,   
   - market cap 
   - trading volumes &
   - Provide currency exchange rates and comparisons in visualized data.

The tool will allow users to compare different coins based on performance. It will also notify users by (email/sms) by sending alerts and analytics insights based on user-defined preferences and when a user's preferred coin hits a specified threshold. 

In Summary: The CoinScraper tool wil simplify the crypto market monitorig and insights extraction for individual users, saving their time, reducing on paid tools and enabling smarter decisions.  


⚖️  NOTE:  All rules will be applied to abide with the legal terms provided by various target websites. 

 
2. TechStack 

 🧷 Backend Config:
   
   ✔️ Python3 & Django - The core framework used for its mature ecosystem, and a built-in and adjustable admin panel.  
   
   ✔️ DjangoRest Framework (DRF) - Allws for building robust, secure and scalable APIs
   
   ✔️ Djoser: implemented to simplify authentication flows like login, logout, password reset, and JWT support. Once the MVP is developed, the authentication setup will be transitioned to using keycloak to handle advanced role-based access control. 
   
   ✔️ PostgreSQL - Used as the main relational database for storing user data, coins and historical prices. 

   ✔️ Redis - Used to support data caching (e.g., for coin data) and handling expirations (e.g., alerts)

   ✔️ Celery - Help schedule background scraping tasks such as rendering templates and sending emails asynchronously - replacing the synchronous execution in the signals.


 🧷 Frontend Config:
   
   ✔️ Html & CSS - Used to develop a simple UI for the MVP and testing objectives.

   ✔️ React (Optional) - To be used as the final stack for developing a SPA dashboard for coin tracking and analytics charts. 


📈 Analytics & Visualization

   ✔️ Matplotlib / Seaborn / Plotly: For generating line charts, bar charts, and comparative graphs.

   ✔️ Pandas: Used for cleaning and analyzing historical price data.


🧪 Testing & Dev Tools

   ✔️ Postman: For testing API endpoints.

   ✔️ pytest + DRF TestClient: Backend unit and integration tests.


   


4. Features 

    
