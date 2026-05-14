# README.md

````markdown id="w6s0ls"
# 📊 Excel Reconciliation System

An enterprise-style Excel reconciliation application built using Python and Streamlit.

This application allows users to:

- Upload a Primary Excel file
- Upload multiple Secondary Excel files
- Dynamically map columns between files
- Reconcile records using selected mappings
- Identify unmatched rows
- Generate downloadable Excel reconciliation reports

---

# 🚀 Features

## ✅ Dynamic Column Mapping
Map columns between files even if column names are different.

Example:

| Primary File | Secondary File |
|---|---|
| Invoice_No | Invoice_Number |
| GSTIN | GST_Number |
| Amount | Taxable_Amount |

---

## ✅ Multiple Excel File Support

Supports:
- One Primary Excel file
- Multiple Secondary Excel files

---

## ✅ Multi-Sheet Support

Users can select:
- Worksheet from Primary file
- Worksheet from Secondary files

---

## ✅ Composite Reconciliation Logic

Reconcile using multiple columns together.

Example:
- Invoice Number
- Amount
- GSTIN
- Date

---

## ✅ Full Unmatched Row Export

The generated report contains:
- Complete unmatched rows
- All original columns
- Reconciliation status
- Composite reconciliation key

---

## ✅ Summary Dashboard

Application generates:
- Total rows
- Matched rows
- Unmatched rows

---

# 🏗️ Project Structure

```text
excel_reconciliation_app/
│
├── app.py
├── requirements.txt
│
├── utils/
│   ├── reconciler.py
│   └── report_generator.py
│
├── outputs/
└── uploads/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <your-repository-url>
cd excel_reconciliation_app
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📦 Requirements

Create a `requirements.txt` file:

```txt
streamlit
pandas
openpyxl
xlsxwriter
```

---

# 🧠 How Reconciliation Works

The application creates a composite key using mapped columns.

Example:

Primary File:

| Invoice_No | Amount |
|---|---|
| INV001 | 1000 |

Secondary File:

| Invoice_Number | Taxable_Amount |
|---|---|
| INV001 | 1000 |

Generated Composite Key:

```text
inv001||1000
```

Records are matched using these generated keys.

---

# 📊 Generated Report

The application generates an Excel report containing:

| Sheet Name | Description |
|---|---|
| Summary | Match statistics |
| Secondary File Name | Unmatched rows |

---

# 📁 Example Use Cases

## Finance Reconciliation
- Bank statements
- Vendor payments
- Expense matching

---

## GST Reconciliation
- Invoice matching
- GSTIN validation
- Tax amount comparison

---

## HR Reconciliation
- Payroll vs attendance
- Employee master validation

---

## Inventory Reconciliation
- Warehouse stock comparison
- ERP stock validation

---

# 🔒 Current Matching Logic

Current logic supports:

✅ Exact matching  
✅ Case-insensitive matching  
✅ Trim-space matching  

---

# 🚀 Future Enhancements

Planned features:

- Fuzzy matching
- AI-based smart column mapping
- Duplicate detection
- Dashboard charts
- Login authentication
- Database integration
- Audit logs
- Scheduled reconciliation
- Email report delivery
- ERP integrations

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend processing |
| Streamlit | UI framework |
| Pandas | Data processing |
| OpenPyXL | Excel handling |
| XlsxWriter | Excel report generation |

---

# 📸 Recommended Test Files

Use the provided sample files:

- Enhanced_Primary_Test_File.xlsx
- Enhanced_Secondary_Test_File.xlsx

Suggested mappings:

| Primary Column | Secondary Column |
|---|---|
| Invoice_No | Invoice_Number |
| Customer_Name | Client_Name |
| GSTIN | GST_Number |
| Invoice_Date | Bill_Date |
| Amount | Taxable_Amount |
| Tax_Amount | GST_Tax |

---

# 👨‍💻 Author

Developed using:
- Python
- Streamlit
- Pandas

---

# 📄 License

This project is licensed under the MIT License.

````
