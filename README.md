
# 🎮 GameVault - Consolidated Game Library

**GameVault** is a personal game library manager and price tracker that brings your entire game collection together in one place. No more switching between Steam, Epic Games, Xbox, PlayStation, and other launchers just to see what you own. GameVault helps you browse and organize games from multiple platforms with minimal effort, features automatic syncing (where possible), a FastAPI-powered web interface, and a planned store section to help you find the best deals on new titles.

## ✨ Why GameVault?

Launching multiple game clients just to check your library is tedious. GameVault solves this by:
- Syncing your owned games from various platforms
- Displaying your entire collection on a single, clean web interface
- Helping you track, browse, and manage your games in one place
- Planning a Store & Buy feature to show the cheapest platforms to purchase new games

## 📦 Features

✅ **Game Library Consolidation**  
- Displays your complete game library in one place  
- Clear separation for unmatched items and non-game media  

✅ **Epic Games Sync (Browser Extension Assisted)**  
- Due to the lack of an official API or proper library tab on the Epic Games website, GameVault uses a **custom browser extension**  
- After logging in to Epic Games, users click the extension button to fetch their transaction history  
- Purchased games are then synced to the GameVault database  

✅ **Frontend & Backend with FastAPI**  
- Clean web interface built with **HTML**, **CSS**, and **JavaScript**  
- Served via a **FastAPI** backend  
- Game icons retrieved from **IGDB**  

✅ **Planned Features**  
- Support for syncing:  
  - Steam  
  - Xbox  
  - PlayStation  
- **Store & Buy section**  
  - Browse games available for purchase  
  - Automatically find the **cheapest platform** to buy a game  
- Advanced search and filtering  
- Manual unmatched game handling  
- Wishlist and tracking features  

## 🛠️ Technologies Used

**Frontend:**  
- HTML  
- CSS  
- JavaScript  

**Backend:**  
- Python  
- FastAPI  
- Uvicorn (development server)  
- PostgreSQL  

**Browser Extension:**  
- JavaScript-based extension for fetching Epic Games transactions  

**APIs:**  
- IGDB (for game icons, via Twitch API)  
- *(Planned)*: Price comparison APIs  

## ⚙️ Database Structure

- **`games`** - Confirmed games with metadata  
- **`non_games`** - Non-game media  
- **`unmatched`** - Items needing manual review  

## 🚀 Getting Started

### Prerequisites

- Python 3.9+  
- PostgreSQL  
- IGDB/Twitch API credentials  
- Epic Games account  
- Installed browser extension for Epic Games sync
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

1. Clone the repository:  
   ```bash  
   git clone https://github.com/ParthS33/GameVault.git  
   cd GameVault  
   ```  

2. Install backend dependencies:  
   ```bash  
   poetry install    
   ```  

3. Configure environment variables:  
   ```ini  
   POSTGRES_HOST=localhost  
   POSTGRES_NAME=gamevault  
   POSTGRES_USER=your_db_user  
   POSTGRES_PASSWORD=your_db_password  
   POSTGRES_PORT=5432  
   TWITCH_CLIENT_ID=your_igdb_client_id  
   TWITCH_CLIENT_SECRET=your_igdb_client_secret  
   ```  

4. Initialize the database:  
   ```bash  
   python db/setup.py  
   ```  

5. Run the FastAPI backend:  
   ```bash  
   uvicorn src.gamevault.main:app --reload --port 8005  
   ```  

6. Sync your Epic Games library:  
   - Login to the Epic Games website  
   - Click the GameVault browser extension button  
   - The extension will fetch your transaction history and populate your GameVault library  

7. Access the web interface:  
   - Open your browser and go to [http://127.0.0.1:8005](http://127.0.0.1:8005)  

## 📂 Project Structure

```
GameVault/
├── frontend/           # HTML, CSS, JavaScript for the web interface
├── extension/          # Browser extension source code
├── db/                 # Database setup files
├── src/gamevault/      # FastAPI backend source code
├── scripts/            # Backend sync and utility scripts
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # Project documentation
```

## 🗺️ Roadmap

- [x] Epic Games sync via browser extension  
- [x] FastAPI backend  
- [x] Frontend served through FastAPI  
- [ ] Steam, Xbox, PlayStation support  
- [ ] Store & Buy section with price comparison  
- [ ] Search and filter functionality  
- [ ] Manual unmatched item handling  
- [ ] Wishlist and tracking  

## 🤝 Contributing

Contributions are welcome! Feature suggestions, bug reports, and pull requests are appreciated.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🎉 Acknowledgments

- [IGDB](https://www.igdb.com/) for game icons  
- Open-source tools and libraries  
- Future price comparison APIs  

**GameVault** helps you track your game collection, discover new games, and find the best deals - all in one place.
