# Lost Person Finder

A web-based system for reporting and finding missing persons using facial recognition technology. This system helps reunite families by allowing users to report missing persons, found persons, and search through a database of photos.

## 🚀 Features

- **Missing Person Reports**: Submit detailed reports with photos and personal information
- **Found Person Reports**: Report found individuals to help identify them
- **Photo Search**: Upload photos to search for matches in the database
- **Dashboard**: Real-time statistics and recent reports overview
- **REST API**: Complete API for integration with other systems
- **Facial Recognition**: AI-powered photo matching (coming soon)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ADITYASINGH03RAJPUT/lost-person-finder.git
   cd lost-person-finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python init_database.py
   ```

## 🚀 Quick Start

1. **Start the server**
   ```bash
   python server_simple.py
   ```

2. **Access the application**
   - Web Dashboard: http://localhost:5000
   - API Documentation: http://localhost:5000/api/health

3. **Test the system**
   ```bash
   python test_api.py
   ```

## 📁 Project Structure

```
lost-person-finder/
├── database/
│   ├── reports.json          # JSON database for reports
│   ├── matches.json          # Verified matches data
│   └── face_vectors.db       # SQLite database for face vectors
├── uploads/
│   ├── missing/              # Missing person photos
│   ├── found/                # Found person photos
│   ├── profiles/             # Profile photos
│   └── search/               # Search query photos
├── exports/
│   ├── daily_reports/        # Daily report exports
│   └── analytics/            # Analytics data
├── init_database.py          # Database initialization script
├── server.py                 # Full server with facial recognition
├── server_simple.py          # Simplified server (current)
├── test_api.py              # API testing script
├── index.html               # Web dashboard
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `GET /api/stats` - Dashboard statistics

### Reports
- `GET /api/reports/missing` - Get missing person reports
- `GET /api/reports/found` - Get found person reports
- `POST /api/reports/missing` - Submit missing person report
- `POST /api/reports/found` - Submit found person report

### Photos & Search
- `POST /api/upload/<type>/<id>` - Upload photos for a report
- `POST /api/search` - Search database with photo
- `GET /uploads/<filename>` - Serve uploaded files

### Matches
- `GET /api/matches` - Get verified matches

## 📊 Dashboard Features

The web dashboard provides:
- Real-time statistics (missing persons, found persons, matches)
- Recent reports overview
- Quick action buttons for reporting and searching
- API connection testing

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `UPLOAD_FOLDER`: Custom upload directory (default: `uploads`)
- `MAX_FILE_SIZE`: Maximum file size for uploads (default: 5MB)

### Supported File Types
- Images: PNG, JPG, JPEG, WEBP
- Maximum size: 5MB per file

## 🧪 Testing

Run the test suite:
```bash
python test_api.py
```

Test individual endpoints:
```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stats
```

## 🚧 Current Status

**Version**: 1.0.0 (Simplified Mode)
- ✅ Core API functionality
- ✅ Database operations
- ✅ Photo upload and storage
- ✅ Web dashboard
- ⏳ Facial recognition (in development)

## 🔮 Upcoming Features

- **Facial Recognition**: AI-powered photo matching using DeepFace
- **Advanced Search**: Filter by age, gender, location, date ranges
- **Notifications**: Email/SMS alerts for matches
- **Mobile App**: React Native mobile application
- **Admin Panel**: User management and system administration
- **Analytics**: Detailed reporting and statistics
- **Multi-language**: Support for multiple languages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/ADITYASINGH03RAJPUT/lost-person-finder/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [DeepFace](https://github.com/serengil/deepface) - Facial recognition library
- [OpenCV](https://opencv.org/) - Computer vision library
- [SQLite](https://www.sqlite.org/) - Database engine

## 📈 Statistics

- **Reports Processed**: Track through dashboard
- **Successful Matches**: View in matches section
- **Active Cases**: Monitor missing persons status

---

**Made with ❤️ for reuniting families**