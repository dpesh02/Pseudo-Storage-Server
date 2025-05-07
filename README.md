# Pseudo-Storage-Server

**Pseudo-Storage-Server** is a web application that centralizes images from multiple Google Drive accounts into a single, easy-to-use image gallery. It leverages the Google Drive API to fetch images from user-specified folders and organizes them into albums. The gallery allows users to browse images, search for albums, and display them in an organized and visually appealing way.

---

## Features

- **Centralized Gallery**: Collect images from multiple Google Drive accounts using an API key.
- **Album Groups**: Organize albums into custom groups for better navigation.
- **Customizable**: Users can provide their own folder IDs and create custom album groups.
- **Dynamic Search**: Quickly search through albums and images.
- **Responsive Design**: Fully responsive interface for a great user experience on any device.

---

## How it Works

1. **Google Drive Integration**: 
   - The app uses the **Google Drive API** to fetch images from specified Google Drive folders.
   - Folder IDs are provided by the user, and the images are fetched via a secure backend that hides the API key.

2. **Customizable Folder IDs and Album Groups**:
   - Users can modify the `folderIds` and `albumGroups` configurations to specify their own Google Drive folder IDs and the organization of albums.
   - The app allows flexible album grouping (e.g., by device, theme, event, etc.).

3. **Image Display**:
   - The gallery displays images in a glass-like UI with hover effects and smooth transitions.
   - Clicking on an image opens it in a full-screen modal view.

---

## Installation

### Prerequisites
- A **Google Cloud project** with the **Google Drive API** enabled.
- An **API key** for accessing the Google Drive API.

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Pseudo-Storage-Server.git
   cd Pseudo-Storage-Server
