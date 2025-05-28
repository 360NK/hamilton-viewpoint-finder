# Hamilton Viewspot Finder 🏞️

**Goal:** An interactive web platform to discover optimal recreational viewpoints along Hamilton's Niagara Escarpment using advanced viewshed analysis and multi-criteria scoring.

**Project Status:** 🚧 **In Progress (Week 1 of 8 - Started May 2025)** 🚧 - Currently building foundational data processing and core viewshed algorithms.

---

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Validation](#validation)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

---

## About The Project

Finding the perfect viewpoint involves more than just elevation. It's about the quality of the view, how private it is, how easy it is to get to, and even the current weather. This project aims to create a tool specifically for the beautiful Hamilton Niagara Escarpment area (Hamilton, Ontario, Canada) that helps hikers, photographers, and nature lovers find _their_ ideal spot.

It uses geospatial data (like Digital Elevation Models - DEMs) and advanced viewshed analysis to calculate what can be seen from any given point. But it goes further by layering on a multi-criteria scoring system to rank viewpoints based on:

- Scenic Quality
- Privacy/Seclusion (using reverse viewshed)
- Accessibility (slope, trail distance)
- Weather Protection (planned)
- Real-time Conditions (weather, air quality - planned)

---

## Key Features

- **Advanced Viewshed Analysis:** Calculates visible areas from any point on the escarpment.
- **Multi-Criteria Scoring:** Ranks viewpoints based on user-defined preferences.
- **Interactive Map Interface:** Click on the map to analyze potential viewpoints (React & Leaflet).
- **Real-time Data Integration:** Incorporates current weather (Environment Canada) and other conditions.
- **Spatial Database Backend:** Uses PostGIS for efficient spatial data storage and querying.
- **API Access:** Provides data via a high-performance FastAPI backend.
- **Ground-Truth Validation:** All key viewpoints and algorithm results are validated through field visits.

---

## Technology Stack

This project leverages a modern stack for geospatial analysis and web development:

- **Backend:** Python, FastAPI
- **Geospatial Processing:** GDAL, Rasterio, GeoPandas, NumPy
- **Database:** PostgreSQL + PostGIS
- **Frontend:** React + TypeScript
- **Mapping:** Leaflet
- **Environment:** Conda
- **Version Control:** Git & GitHub
- **Testing:** Pytest

---

## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Git
- Conda (Miniconda or Anaconda)
- PostgreSQL + PostGIS extension installed and running

### Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/360NK/hamilton-viewpoint-finder.git](https://github.com/360NK/hamilton-viewpoint-finder.git)
    cd hamilton-viewpoint-finder
    ```
2.  **Create & Activate Conda Environment:**
    _(You might want to create an `environment.yml` file later for easier setup)_
    ```bash
    conda create -n hamilton-viewspot-finder python=3.9 # Or your preferred version
    conda activate hamilton-viewspot-finder
    ```
3.  **Install Python Libraries:**
    ```bash
    conda install -c conda-forge rasterio gdal numpy geopandas fastapi uvicorn psycopg2-binary pytest
    # Add any other libraries as you need them
    ```
4.  **Set up Environment Variables:**
    - Create a `.env` file (copy from `.env.example` when you create one).
    - Add your database connection details and any API keys.
      _(You will need to create the `.env.example` file first)_
5.  **Set up Database:**
    - Create your PostGIS database and user.
    - Run database migrations (when you create them).
6.  **Download Data:**
    - Obtain the Hamilton CDEM elevation data (instructions TBD).
    - Place it in the designated `data/` directory (ensure `data/` is in `.gitignore` if large).

---

## Usage

_(This section will be filled out as the project progresses)_

- **Running the Backend:**
  ```bash
  uvicorn main:app --reload # Or similar command
  ```
- **Running the Frontend:**
  ```bash
  cd frontend
  npm install
  npm start # Or similar commands
  ```
- **API Documentation:** Access auto-generated docs at `http://127.0.0.1:8000/docs` when the backend is running.

---

## Validation

The accuracy of this tool is paramount. We employ a systematic ground-truth validation process:

- Field Visits: Visiting known and algorithm-predicted viewpoints.
- Photographic Documentation: Capturing panoramic views and specific landmarks.
- Known Sites: Calibrating using established viewpoints like Dundurn Castle, Devil's Punchbowl, and Dundas Peak.
- Data Collection: Recording GPS, elevation, and observable conditions during visits.

See the full [Validation Plan](validation_plan.md) for details.

---

## Roadmap

This is an 8-week project (May 2025 - July 2025). Key milestones include:

- Week 2: Core Analysis Engine
- Week 4: Complete Backend & API
- Week 6: Functional Web Application
- Week 8: Deployed & Validated System

See the detailed [Project Roadmap](project_roadmap.md) for the week-by-week plan.

---

## License

This project is distributed under the MIT License. See `LICENSE` for more information. _(You'll need to add a LICENSE file later)_

---

## Contact

Kashy - [GitHub Profile](https://github.com/360NK) - [LinkedIn]{https://www.linkedin.com/in/kashinath-namboothiri-46657b1a8/}

Project Link: [https://github.com/360NK/hamilton-viewpoint-finder](https://github.com/360NK/hamilton-viewpoint-finder)
