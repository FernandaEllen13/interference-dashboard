
# 📡 Interference Dashboard

A clean and interactive dashboard built with Python to monitor **telecom site interference** based on uploaded CSV data. Sites exceeding a **-110 dBm interference threshold** are highlighted with visual indicators and statistics.

## 🧩 Features

- 📁 **CSV Upload** for interference data (`site_name`, `interference_value`)
- 📊 **Dashboard** with key visualizations:
  - Highlighted sites with interference > -110 dBm
  - Summary: average, min, max, and percentage of affected sites
  - Breakdown of sites per state (based on site code)
- 📦 **CI/CD Pipeline** via GitHub Actions:
  - Automated testing with `pytest`
  - Packaging of the project
  - 📬 Email notification after pipeline execution

## 🖼️ Example

![image](https://github.com/user-attachments/assets/4782be3d-8cb0-4ff6-bcad-a1461141b9bc)

## 📂 CSV Format

Your input CSV should look like this:

```csv
nome_do_site,valor_interferencia
SPABC01,-108
MGBHZ02,-112
RJRIO03,-109
```

- `nome_do_site`: follows pattern **[UF][CIDADE][ID]** (e.g., `MGABC01`)
- `valor_interferencia`: measured in dBm (e.g., `-110`)

## 🚀 Getting Started

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the dashboard

```bash
python app.py
```

Then access: [http://localhost:8050](http://localhost:8050)

## ✅ Running Tests

```bash
pytest
```

Unit tests are located in the `/tests` folder, using simulated DataFrames.

## 🔁 CI/CD Pipeline

This project includes a GitHub Actions pipeline with:

- 🧪 **Test Job**: runs `pytest` and stores test reports
- 📦 **Build Job**: packages the code as a `.zip`
- 📬 **Notify Job**: sends a notification email


## 📁 Project Structure

```
INTERFERENCE-DASHBOARD/
│
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de CI/CD
│
├── app/
│   └── dashboard.py           # Código principal do dashboard
│
├── scripts/
│   └── send_email.py          # Script para envio de e-mail
│
├── tests/
│   └── test_dashboard.py      # Testes unitários com pytest
│
```


