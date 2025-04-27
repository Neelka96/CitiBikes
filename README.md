# CitiBike Tableau Analysis Repository  

**Module 18 Challenge**  
**EdX/UT Data Analytics and Visualization Bootcamp**  
**Cohort UTA-VIRT-DATA-PT-11-2024-U-LOLC**  
**Author:** Neel Agarwal  

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Repository Structure](#repository-structure)  
3. [Data Sources](#data-sources)  
4. [Setup & Installation](#setup--installation)  
5. [Rubric Alignment](#rubric-alignment)  
   - [Map (25 pts)](#map-25pts)  
   - [Visualizations (25 pts)](#visualizations-25pts)  
   - [Story (25 pts)](#story-25pts)  
   - [Analysis (25 pts)](#analysis-25pts)  
6. [Usage](#usage)  
7. [Limitations & File Sizes](#limitations--file-sizes)  
8. [Future Work](#future-work)  
9. [Credits & References](#credits--references)  

---

This project is also available for viewing on Tableau Public! Check it out here: [CitiBike Analysis.](https://public.tableau.com/app/profile/neel.agarwal3926/viz/CitiBikeAnalysis_17457797716150/MainStory)

## Project Overview  

This repository contains a complete Tableau‑based analysis of CitiBike ride data for Module 18 of the UT/edX Data Visualization Bootcamp.  
You’ll find:  

- **Tableau Workbooks** (`.twbx`) with interactive maps and dashboards.  
- **Jupyter Notebook** (`Bike_Wrangler.ipynb`) showing how raw ride/station CSVs are loaded, cleaned, and prepared for Tableau.  
- A detailed **Analysis Write‑Up** aligned with the assignment rubric.  

The goal was to explore station usage patterns, rider demographics, and temporal trends to support data‑driven decision‑making for city planners.  

---

## Repository Structure  

```plaintext
CitiBike-Tableau-Analysis/
├── Bike_Wrangler.ipynb         # Data prep & cleanup in Python
├── CitiBikeAnalysis.twbx       # Packaged Tableau workbook (interactive dashboards)
├── citibike_data.csv           # Not included in repo (too big)
├── README.md                   # This document
└── analysis.md                 # Analysis write‑up and story captions
```

> [!WARNING]  
> In a separate directory, files from [Citi Bike powered by Lyft](https://citibikenyc.com/system-data) were downloaded and parsed using the notebook.  
> The actual bin of files is accessible from the previous link but it included [here directly](https://s3.amazonaws.com/tripdata/index.html).  
> Therefore, without downloading the correct files, different results would be produced. The Jupyter Notebook is only included as a historical reference  
> for as to how it was brought in and compiled together. The focus of this project was the use of Tableau, therefore the Python aspect was not designed to  
> maintainable or accessible. Apologies!  

> **Note:** The full ride‑station extract (\~770 MB) and the `.twbx` file (90 MB) are too large for GitHub. See [Limitations & File Sizes](#limitations--file-sizes).

---

## Data Sources

- **CitiBike Open Data API**: Historical trip and station metadata (downloaded and exported to CSV).
- **Local Subset**: A small sample in `data/` for notebook testing.

Data preparation (deduplication, formatting, mapping station IDs) happens in `Bike_Wrangler.ipynb` before loading into Tableau.

---

## Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/CitiBike-Tableau-Analysis.git
   cd CitiBike-Tableau-Analysis
   ```
2. **Install Python dependencies** (for data prep notebook):
   ```bash
   pip install pandas numpy jupyterlab
   ```
3. **Open the Jupyter Notebook**:
   ```bash
   jupyter lab Bike_Wrangler.ipynb
   ```
4. **Publish or open the **``** in Tableau Desktop** (see limitations below for file size workarounds).

---

## Rubric Alignment

Below is how each rubric section is addressed in this project:

### Map (25 pts)

- **All Stations Plotted**: Every CitiBike station appears on `Station Usage Map`.
- **Styling by Popularity**: Markers sized by total rides, colored by subscriber ratio.
- **Month Selector**: A Parameter control lets viewers switch the map to any month/year.
- **Zip‑Code Layers**: Zip polygon layer drawn behind station markers for neighborhood context.
- **Map Write‑Up**: Included as the first story point in `analysis/analysis.md`.

### Visualizations (25 pts)

- **4+ Charts**: Dashboards include “Totals & Stats,” “Hourly Patterns,” “User & Bike Profiles,” and “Gender & Subscription Map.”
- **2 Dashboards**: Consolidated into Dashboard 1 (overview & temporal) and Dashboard 2 (demographics & map).
- **Descriptive Titles**: Each sheet and dashboard has a clear, rubric‑matching title.
- **Clean Data**: All nulls handled in the notebook; data types verified before import.
- **Interactivity**: Parameter and filter controls (month, age, station) enable drill‑down.

### Story (25 pts)

- **3 Story Points**: A Tableau Story (`Story 1`) ties together the dashboards and the map:
  1. **Main System Overview**
  2. **Rider & Bike Profiles**
  3. **Subscription & Demographic Patterns**
- **Narrative Flow**: Each point builds on the last, guiding a non‑technical audience through the key findings.
- **Captions & Navigation**: Custom headlines and “Next →” text objects ensure clarity.

### Analysis (25 pts)

- **Separate Write‑Up**: `analysis/analysis.md` covers each story point with 2–3 plain‑English sentences.
- **Dashboard References**: Each paragraph references its exact sheet title (e.g., “In *Trip Duration & Counts by Hour* …”).
- **Non‑Technical Language**: Jargon minimized; written for city planners and stakeholders.
- **Visual Call‑Outs**: Key chart features and parameter controls are highlighted.

---

## Usage

1. **Run data prep**: Open `Bike_Wrangler.ipynb`, execute all cells to generate cleaned CSVs.
2. **Open Tableau**: Load `CitiBikeAnalysis.twbx` in Tableau Desktop or Tableau Public.
3. **Interact**: Use the month/year parameter, filter cards, and the story navigator to explore the insights.

---

## Limitations & File Sizes

- **Data Extract (\~770 MB)** & **Workbook (.twbx, \~90 MB)** exceed GitHub size limits.
- **Workaround**:
  - **Subset**: A small sample is included in `data/` for notebook testing.
  - **External Download**: Provide a Dropbox/Google Drive link for full data and workbook.
  - **Published Viz**: Optionally share a Tableau Public URL for interactive access.

---

## Future Work

- Automate data extraction from the CitiBike API into scheduled CSV updates.
- Add more demographic layers (e.g., age, gender) to the map via hex‑bin or choropleth.
- Integrate Python‑driven chart generation (matplotlib) alongside Tableau for cross‑validation.

---

## Credits & References

1. **Data & Assignment**: UT/edX Data Visualization Bootcamp Module 18 rubric and dataset.  
2. **Tools**: Tableau Desktop, pandas, JupyterLab.  
3. **README Style**: Adapted from prior bootcamp READMEs and [OpenAI ChatGPT](https://chat.openai.com) assistance.  
4. **Help with Analysis**: ChatGPT was leveraged for help noticing themes and patterns within data visualization for more detailed analyses.  
5. **Python Docs**: For basic python usage documentation see [Python](https://docs.python.org/3/).  
6. **Pandas Docs**: For data prep and loading logic see [Pandas](https://pandas.pydata.org/docs/).  

---