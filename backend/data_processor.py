"""
Deciora - Adaptive Bulletproof Data Processor
Works with ANY data, ANY column names, ANY format
Never fails — always extracts maximum possible insight
"""
import io
import re
import uuid
import warnings
import pandas as pd
import numpy as np
from backend.config import supabase_admin, STORAGE_BUCKET

warnings.filterwarnings("ignore")

# ── Column Intent Keywords ─────────────────────────────────
# System inhe use karke columns ka purpose samjhega

INTENT_MAP = {
    "date": [
        "date", "time", "month", "year", "day", "period", "week",
        "quarter", "tarikh", "din", "mahina", "sal", "timestamp",
        "created", "updated", "recorded", "when", "dt", "fecha"
    ],
    "revenue": [
        "revenue", "sales", "income", "turnover", "gross", "earning",
        "receipt", "collection", "billing", "invoice", "amount",
        "value", "price", "rate", "fee", "charge", "total",
        "bikri", "aay", "paisa", "rassi", "raqam", "rupee", "inr",
        "usd", "eur", "gbp", "售额", "收入"
    ],
    "expense": [
        "expense", "cost", "spend", "expenditure", "opex", "capex",
        "payment", "paid", "purchase", "buy", "debit", "outflow",
        "kharcha", "lagat", "vyay", "خرچ"
    ],
    "profit": [
        "profit", "margin", "net", "ebitda", "pbt", "pat",
        "earning", "gain", "return", "munafa", "laabh"
    ],
    "quantity": [
        "quantity", "qty", "units", "count", "volume", "number",
        "pieces", "pcs", "stock", "inventory", "matra", "sankhya"
    ],
    "category": [
        "category", "type", "class", "segment", "group", "division",
        "product", "item", "service", "brand", "sku", "department",
        "region", "area", "zone", "city", "state", "country",
        "channel", "source", "medium", "platform", "vibhag"
    ],
    "customer": [
        "customer", "client", "buyer", "user", "member", "account",
        "name", "naam", "grahak", "顾客"
    ],
    "employee": [
        "employee", "staff", "worker", "karmchari", "person",
        "hr", "payroll", "salary", "wage", "designation", "role"
    ],
    "id": [
        "id", "uuid", "code", "number", "no", "num", "serial",
        "ref", "reference", "order", "invoice_no", "bill"
    ],
}


# ── File Upload ────────────────────────────────────────────

def upload_file_to_storage(file_bytes: bytes, file_name: str, user_id: str) -> dict:
    """Upload file to Supabase Storage."""
    try:
        ext = file_name.split(".")[-1].lower()
        storage_path = f"{user_id}/{uuid.uuid4()}.{ext}"

        supabase_admin.storage.from_(STORAGE_BUCKET).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": _get_mime(ext)},
        )

        url_res = supabase_admin.storage.from_(STORAGE_BUCKET).create_signed_url(
            storage_path, 3600
        )
        file_url = url_res.get("signedURL", storage_path)

        return {
            "success": True,
            "storage_path": storage_path,
            "file_url": file_url,
            "file_size": len(file_bytes),
            "file_type": ext,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Smart File Loader ──────────────────────────────────────

def load_dataframe(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    """
    Load ANY file into DataFrame.
    Tries multiple strategies before giving up.
    """
    ext = file_name.split(".")[-1].lower()
    buf = io.BytesIO(file_bytes)

    if ext == "csv":
        return _load_csv(buf)
    elif ext in ("xlsx", "xls"):
        return _load_excel(buf, ext)
    else:
        # Try CSV anyway as last resort
        try:
            return _load_csv(buf)
        except Exception:
            raise ValueError(f"Cannot read file format: {ext}. Please upload CSV or Excel.")


def _load_csv(buf) -> pd.DataFrame:
    """Try multiple CSV loading strategies."""
    strategies = [
        # encoding, separator, header
        ("utf-8", ",", 0),
        ("utf-8", ";", 0),
        ("utf-8", "\t", 0),
        ("latin-1", ",", 0),
        ("latin-1", ";", 0),
        ("cp1252", ",", 0),
        ("utf-8", ",", 1),   # header on row 2
        ("latin-1", ",", 1),
    ]
    last_error = None
    for enc, sep, header in strategies:
        try:
            buf.seek(0)
            df = pd.read_csv(buf, encoding=enc, sep=sep, header=header,
                             on_bad_lines="skip", low_memory=False)
            if len(df) > 0 and len(df.columns) > 0:
                return df
        except Exception as e:
            last_error = e
            continue
    raise ValueError(f"Could not read CSV: {last_error}")


def _load_excel(buf, ext: str) -> pd.DataFrame:
    """Try multiple Excel loading strategies."""
    engines = ["openpyxl"] if ext == "xlsx" else ["xlrd", "openpyxl"]
    last_error = None
    for engine in engines:
        for header_row in [0, 1, 2]:
            try:
                buf.seek(0)
                df = pd.read_excel(buf, engine=engine, header=header_row)
                if len(df) > 0 and len(df.columns) > 0:
                    return df
            except Exception as e:
                last_error = e
                continue
    raise ValueError(f"Could not read Excel: {last_error}")


# ── Bulletproof Cleaner ────────────────────────────────────

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean ANY DataFrame no matter how messy.
    Never fails — always returns something useful.
    """
    if df is None or len(df) == 0:
        return pd.DataFrame()

    df = df.copy()

    # Step 1: Fix column names
    df = _fix_column_names(df)

    # Step 2: Drop completely empty rows/cols
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Step 3: Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Step 4: Fix string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({
            "nan": np.nan, "None": np.nan, "none": np.nan,
            "NULL": np.nan, "null": np.nan, "NA": np.nan,
            "N/A": np.nan, "n/a": np.nan, "-": np.nan,
            "": np.nan, " ": np.nan, "#N/A": np.nan,
        })

    # Step 5: Parse dates
    df = _parse_dates(df)

    # Step 6: Parse numeric columns
    df = _parse_numerics(df)

    # Step 7: Drop cols that are still all null after cleaning
    df.dropna(axis=1, how="all", inplace=True)

    # Step 8: Reset index
    df.reset_index(drop=True, inplace=True)

    return df


def _fix_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names — handle Unnamed, duplicates, special chars."""
    new_cols = []
    seen = {}

    for i, col in enumerate(df.columns):
        col_str = str(col).strip()

        # Handle unnamed columns (from Excel/CSV artifacts)
        if col_str.startswith("Unnamed") or col_str == "" or col_str == "nan":
            col_str = f"column_{i+1}"

        # Normalize: lowercase, replace spaces/special chars
        col_clean = re.sub(r"[^\w]", "_", col_str.lower())
        col_clean = re.sub(r"_+", "_", col_clean).strip("_")

        # Handle duplicates
        if col_clean in seen:
            seen[col_clean] += 1
            col_clean = f"{col_clean}_{seen[col_clean]}"
        else:
            seen[col_clean] = 0

        new_cols.append(col_clean)

    df.columns = new_cols
    return df


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Smart date parsing — works with any date format."""
    date_formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
        "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d",
        "%d %b %Y", "%b %d %Y", "%B %d %Y",
        "%d-%b-%Y", "%b-%Y", "%B %Y",
        "%Y-%m", "%m-%Y",
    ]

    for col in df.columns:
        # Check by column name intent
        col_lower = col.lower()
        is_date_col = any(kw in col_lower for kw in INTENT_MAP["date"])

        if is_date_col:
            # Try pandas auto-parse first
            try:
                parsed = pd.to_datetime(df[col], infer_datetime_format=True,
                                       errors="coerce", dayfirst=True)
                if parsed.notna().sum() / max(len(df), 1) > 0.5:
                    df[col] = parsed
                    continue
            except Exception:
                pass

            # Try each format explicitly
            for fmt in date_formats:
                try:
                    parsed = pd.to_datetime(df[col], format=fmt, errors="coerce")
                    if parsed.notna().sum() / max(len(df), 1) > 0.5:
                        df[col] = parsed
                        break
                except Exception:
                    continue

        else:
            # Even non-date-named columns might have dates — check values
            if df[col].dtype == object:
                sample = df[col].dropna().head(10)
                try:
                    parsed = pd.to_datetime(sample, infer_datetime_format=True,
                                           errors="coerce", dayfirst=True)
                    if parsed.notna().sum() / max(len(sample), 1) > 0.8:
                        df[col] = pd.to_datetime(df[col], infer_datetime_format=True,
                                                errors="coerce", dayfirst=True)
                except Exception:
                    pass

    return df


def _parse_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Parse numeric values from any format — currency, comma-separated, etc."""
    currency_pattern = re.compile(r"[₹$€£¥₩\s,]")

    for col in df.select_dtypes(include=["object"]).columns:
        # Skip if already parsed as date
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue

        # Skip ID-like columns
        col_lower = col.lower()
        if any(kw in col_lower for kw in INTENT_MAP["id"]):
            continue

        try:
            # Clean currency symbols and commas
            cleaned = df[col].astype(str).apply(
                lambda x: currency_pattern.sub("", x).strip()
            )
            # Handle negative in brackets: (1200) → -1200
            cleaned = cleaned.apply(
                lambda x: "-" + x[1:-1] if x.startswith("(") and x.endswith(")") else x
            )
            # Handle percentage
            cleaned = cleaned.str.rstrip("%")

            numeric = pd.to_numeric(cleaned, errors="coerce")

            # Only convert if majority are numeric
            valid_ratio = numeric.notna().sum() / max(len(df), 1)
            if valid_ratio > 0.6:
                df[col] = numeric
        except Exception:
            pass

    return df


# ── Adaptive Column Classifier ─────────────────────────────

def classify_data(df: pd.DataFrame) -> dict:
    """
    Adaptively classify ANY DataFrame.
    Works even if columns are named col1, col2, xyz, etc.
    """
    if df is None or df.empty:
        return _empty_classification()

    cols = list(df.columns)

    # Build column intent map
    column_intents = _detect_column_intents(df)

    # Detect overall data type
    data_type = _detect_data_type(column_intents, cols)

    # Get column type lists
    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    date_cols = list(df.select_dtypes(include=["datetime64"]).columns)
    categorical_cols = [
        col for col in df.select_dtypes(include=["object"]).columns
        if df[col].nunique() < min(50, len(df) * 0.5)
    ]
    high_cardinality_cols = [
        col for col in df.select_dtypes(include=["object"]).columns
        if col not in categorical_cols
    ]

    return {
        "data_type": data_type,
        "total_rows": len(df),
        "total_columns": len(cols),
        "numeric_columns": numeric_cols,
        "date_columns": date_cols,
        "categorical_columns": categorical_cols,
        "high_cardinality_columns": high_cardinality_cols,
        "column_intents": column_intents,
        "missing_pct": round(df.isnull().mean().mean() * 100, 2),
        "columns": cols,
        "has_time_series": len(date_cols) > 0,
        "has_financials": bool(
            column_intents.get("revenue") or
            column_intents.get("expense") or
            column_intents.get("profit")
        ),
    }


def _detect_column_intents(df: pd.DataFrame) -> dict:
    """
    For each intent (date, revenue, expense, etc.)
    find which column best matches — even if named randomly.
    """
    intents = {}
    used_cols = set()

    for intent, keywords in INTENT_MAP.items():
        best_col = None
        best_score = 0

        for col in df.columns:
            if col in used_cols:
                continue

            score = 0
            col_lower = col.lower()

            # Score by column name match
            for kw in keywords:
                if kw in col_lower:
                    score += 10
                    break

            # Score by data type match
            if intent == "date" and pd.api.types.is_datetime64_any_dtype(df[col]):
                score += 15
            elif intent in ("revenue", "expense", "profit", "quantity") and \
                    pd.api.types.is_numeric_dtype(df[col]):
                score += 5
            elif intent in ("category", "customer", "employee") and \
                    df[col].dtype == object:
                score += 3

            # Score by value patterns
            if intent == "revenue" and pd.api.types.is_numeric_dtype(df[col]):
                # Revenue columns tend to have larger values
                try:
                    mean_val = df[col].mean()
                    if mean_val > 100:
                        score += 3
                except Exception:
                    pass

            if score > best_score:
                best_score = score
                best_col = col

        if best_col and best_score > 0:
            intents[intent] = best_col
            if intent not in ("category",):  # category can overlap
                used_cols.add(best_col)

    return intents


def _detect_data_type(column_intents: dict, cols: list) -> str:
    """Detect overall dataset type from column intents."""
    col_str = " ".join(cols).lower()

    if column_intents.get("employee") or \
            any(k in col_str for k in ["salary", "payroll", "wage", "designation"]):
        return "Payroll / HR Data"
    elif column_intents.get("revenue") and column_intents.get("expense"):
        return "P&L / Financial Data"
    elif column_intents.get("revenue"):
        return "Revenue / Sales Data"
    elif column_intents.get("expense"):
        return "Expense Data"
    elif column_intents.get("quantity") and \
            any(k in col_str for k in ["stock", "inventory", "sku", "warehouse"]):
        return "Inventory Data"
    elif column_intents.get("customer"):
        return "Customer Data"
    elif column_intents.get("profit"):
        return "Profitability Data"
    else:
        return "General Business Data"


def _empty_classification() -> dict:
    return {
        "data_type": "Unknown",
        "total_rows": 0,
        "total_columns": 0,
        "numeric_columns": [],
        "date_columns": [],
        "categorical_columns": [],
        "high_cardinality_columns": [],
        "column_intents": {},
        "missing_pct": 100.0,
        "columns": [],
        "has_time_series": False,
        "has_financials": False,
    }


# ── Data Summary for AI Context ────────────────────────────

def generate_data_summary(df: pd.DataFrame, classification: dict) -> dict:
    """
    Generate rich summary for AI context.
    Uses column_intents so AI gets meaningful column names.
    """
    summary = {}
    intents = classification.get("column_intents", {})

    # Numeric stats — only meaningful columns
    num_df = df.select_dtypes(include=["number"])
    if not num_df.empty:
        desc = num_df.describe().to_dict()
        summary["numeric_stats"] = {
            col: {k: round(v, 2) for k, v in stats.items()}
            for col, stats in desc.items()
        }

    # Date range
    date_cols = df.select_dtypes(include=["datetime64"]).columns
    if len(date_cols) > 0:
        dc = date_cols[0]
        try:
            summary["date_range"] = {
                "column": dc,
                "min": str(df[dc].min().date()),
                "max": str(df[dc].max().date()),
                "periods": df[dc].nunique(),
            }
        except Exception:
            pass

    # Category breakdown
    summary["categorical_counts"] = {}
    for col in classification.get("categorical_columns", [])[:5]:
        try:
            summary["categorical_counts"][col] = \
                df[col].value_counts().head(5).to_dict()
        except Exception:
            pass

    # Intent-mapped columns for AI
    summary["intent_columns"] = {
        intent: col for intent, col in intents.items()
        if intent != "id"
    }

    # Data quality flags
    summary["quality_flags"] = []
    missing = classification.get("missing_pct", 0)
    if missing > 30:
        summary["quality_flags"].append(f"High missing data: {missing}%")
    if classification.get("total_rows", 0) < 10:
        summary["quality_flags"].append("Very few rows — insights may be limited")
    if not classification.get("has_financials"):
        summary["quality_flags"].append("No clear financial columns detected")

    return summary


# ── Helpers ────────────────────────────────────────────────

def _get_mime(ext: str) -> str:
    mimes = {
        "csv": "text/csv",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "xls": "application/vnd.ms-excel",
    }
    return mimes.get(ext, "application/octet-stream")