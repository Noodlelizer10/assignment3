# Commonplace

Commonplace is a lightweight social sharing application designed for brief, thoughtful updates and community interaction. The project allows users to create posts, like content, share updates, add comments, and toggle between light and dark mode in a clean, responsive interface.

## Overview

This application provides a simple, polished user experience for posting short thoughts or updates in a community feed. It is built as a Python Flask app with a front-end template and CSS styling, making it easy to run locally and extend for future features.

## Features

- Create new posts up to 280 characters
- View a responsive community feed
- Like posts and preserve state across refreshes
- Comment on individual posts
- Sort the feed by newest or oldest entries
- Toggle between light and dark themes
- Persist data locally in a JSON file for straightforward local storage management

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JSON for local data persistence

## Getting Started

1. Ensure Python is installed on your system.
2. Install the required dependency:

   ```bash
   python -m pip install Flask
   ```

3. Start the application:

   ```bash
   python app.py
   ```

4. Open the following URL in your browser:

   ```text
   http://127.0.0.1:5000
   ```

## Project Structure

- `app.py` – application logic and Flask routes
- `templates/index.html` – user interface markup
- `static/styles.css` – application styling and theme support
- `posts.json` – persisted post and comment data

## Notes

This project is designed as a compact, local-first social app suitable for demos, coursework, or further extension into a larger community platform.
