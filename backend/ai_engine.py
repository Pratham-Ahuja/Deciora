"""
Deciora - Agentic RAG AI Engine
GPT-4o with Function Calling — Multi-step reasoning on real data
"""
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
from backend.config import OPENAI_API_KEY
from backend.data_processor import generate_data_summary

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o"

# ── Agent Tools Definition ─────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_data",
            "description": "Filter, group, and aggregate the uploaded business DataFrame to answer specific questions. Use this to get actual numbers from the data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["sum", "mean", "count", "max", "min", "groupby", "filter", "trend"],
                        "description": "The operation to perform on the data"
                    },
                    "column": {
                        "type": "string",
                        "description": "The column name to operate on"
                    },
                    "group_by": {
                        "type": "string",
                        "description": "Column to group by (optional)"
                    },
                    "filter_column": {
                        "type": "string",
                        "description": "Column to filter on (optional)"
                    },
                    "filter_value": {
                        "type": "string",
                        "description": "Value to filter for (optional)"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Return top N results (optional, default 10)"
                    }
                },
                "required": ["operation", "column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_metric",
            "description": "Calculate specific business metrics like growth rate, percentage change, moving average, or ratio between columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "enum": ["growth_rate", "pct_change", "moving_average", "ratio", "cumulative", "yoy_change", "mom_change"],
                        "description": "The metric to calculate"
                    },
                    "column": {
                        "type": "string",
                        "description": "Primary column for calculation"
                    },
                    "column2": {
                        "type": "string",
                        "description": "Secondary column (for ratio calculation)"
                    },
                    "window": {
                        "type": "integer",
                        "description": "Window size for moving average (default 3)"
                    }
                },
                "required": ["metric", "column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_anomalies",
            "description": "Detect outliers and anomalies in any column of the data using statistical methods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Column to detect anomalies in"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["zscore", "iqr"],
                        "description": "Detection method — zscore or IQR"
                    }
                },
                "required": ["column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forecast",
            "description": "Project future trend for a numeric column based on historical data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Column to forecast"
                    },
                    "periods": {
                        "type": "integer",
                        "description": "Number of future periods to forecast (default 3)"
                    }
                },
                "required": ["column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_insights",
            "description": "Retrieve previously generated AI insights for this session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "enum": ["all", "descriptive", "diagnostic", "predictive", "prescriptive", "executive_summary"],
                        "description": "Which section of insights to retrieve"
                    }
                },
                "required": ["section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_segments",
            "description": "Compare performance across different segments, categories, or time periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value_column": {
                        "type": "string",
                        "description": "Numeric column to compare"
                    },
                    "segment_column": {
                        "type": "string",
                        "description": "Categorical column to segment by"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Top N segments to show (default 5)"
                    }
                },
                "required": ["value_column", "segment_column"]
            }
        }
    }
]


# ── Tool Executor ──────────────────────────────────────────

def execute_tool(
    tool_name: str,
    tool_args: dict,
    df: pd.DataFrame,
    classification: dict,
    insights: dict,
) -> str:
    """Execute a tool call and return result as string."""
    try:
        if tool_name == "query_data":
            return _tool_query_data(df, tool_args)
        elif tool_name == "calculate_metric":
            return _tool_calculate_metric(df, tool_args)
        elif tool_name == "detect_anomalies":
            return _tool_detect_anomalies(df, tool_args)
        elif tool_name == "forecast":
            return _tool_forecast(df, tool_args)
        elif tool_name == "get_insights":
            return _tool_get_insights(insights, tool_args)
        elif tool_name == "compare_segments":
            return _tool_compare_segments(df, tool_args)
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Tool execution note: {str(e)}. Available columns: {list(df.columns) if df is not None else []}"


def _tool_query_data(df: pd.DataFrame, args: dict) -> str:
    operation = args.get("operation")
    column = args.get("column")
    group_by = args.get("group_by")
    filter_col = args.get("filter_column")
    filter_val = args.get("filter_value")
    top_n = args.get("top_n", 10)

    # Fuzzy column match — find closest column even if name slightly off
    column = _fuzzy_match_column(column, df.columns)
    if group_by:
        group_by = _fuzzy_match_column(group_by, df.columns)
    if filter_col:
        filter_col = _fuzzy_match_column(filter_col, df.columns)

    if column not in df.columns:
        return f"Column '{column}' not found. Available: {list(df.columns)}"

    work_df = df.copy()

    # Apply filter if specified
    if filter_col and filter_val and filter_col in work_df.columns:
        try:
            work_df = work_df[
                work_df[filter_col].astype(str).str.lower().str.contains(
                    str(filter_val).lower(), na=False
                )
            ]
        except Exception:
            pass

    if len(work_df) == 0:
        return "No data found after applying filter."

    # Execute operation
    if operation == "sum":
        if group_by and group_by in work_df.columns:
            result = work_df.groupby(group_by)[column].sum().sort_values(ascending=False).head(top_n)
            return f"Sum of {column} by {group_by}:\n{result.to_string()}"
        else:
            total = work_df[column].sum()
            return f"Total {column}: {total:,.2f}"

    elif operation == "mean":
        if group_by and group_by in work_df.columns:
            result = work_df.groupby(group_by)[column].mean().sort_values(ascending=False).head(top_n)
            return f"Average {column} by {group_by}:\n{result.to_string()}"
        else:
            avg = work_df[column].mean()
            return f"Average {column}: {avg:,.2f}"

    elif operation == "count":
        if group_by and group_by in work_df.columns:
            result = work_df.groupby(group_by)[column].count().sort_values(ascending=False).head(top_n)
            return f"Count of {column} by {group_by}:\n{result.to_string()}"
        else:
            return f"Count of {column}: {work_df[column].count()}"

    elif operation == "max":
        max_val = work_df[column].max()
        max_row = work_df[work_df[column] == max_val].head(1)
        return f"Maximum {column}: {max_val:,.2f}\nRow: {max_row.to_dict('records')}"

    elif operation == "min":
        min_val = work_df[column].min()
        return f"Minimum {column}: {min_val:,.2f}"

    elif operation == "groupby":
        if not group_by or group_by not in work_df.columns:
            return f"group_by column required. Available: {list(work_df.columns)}"
        result = work_df.groupby(group_by)[column].agg(["sum", "mean", "count"]).head(top_n)
        return f"Analysis of {column} by {group_by}:\n{result.to_string()}"

    elif operation == "filter":
        return f"Filtered data ({len(work_df)} rows):\n{work_df[[column]].head(10).to_string()}"

    elif operation == "trend":
        date_cols = work_df.select_dtypes(include=["datetime64"]).columns
        if len(date_cols) > 0:
            dc = date_cols[0]
            trend = work_df.groupby(dc)[column].sum().reset_index()
            return f"Trend of {column} over time:\n{trend.to_string()}"
        else:
            trend = work_df[column].rolling(3).mean()
            return f"Rolling average trend of {column}:\n{trend.dropna().to_string()}"

    return f"Operation {operation} not recognized."


def _tool_calculate_metric(df: pd.DataFrame, args: dict) -> str:
    metric = args.get("metric")
    column = _fuzzy_match_column(args.get("column"), df.columns)
    column2 = args.get("column2")
    window = args.get("window", 3)

    if column not in df.columns:
        return f"Column '{column}' not found. Available: {list(df.columns)}"

    series = df[column].dropna()

    if metric == "growth_rate":
        if len(series) < 2:
            return "Not enough data for growth rate."
        first = series.iloc[0]
        last = series.iloc[-1]
        if first == 0:
            return "Cannot calculate growth rate — starting value is 0."
        rate = ((last - first) / abs(first)) * 100
        return f"Overall growth rate of {column}: {rate:+.2f}%\nFrom {first:,.2f} to {last:,.2f}"

    elif metric == "pct_change":
        changes = series.pct_change().dropna() * 100
        return f"Period-over-period % change for {column}:\n{changes.round(2).to_string()}\nAvg change: {changes.mean():+.2f}%"

    elif metric == "moving_average":
        ma = series.rolling(window=window).mean().dropna()
        return f"{window}-period moving average of {column}:\nLatest: {ma.iloc[-1]:,.2f}\nTrend: {'↑ Increasing' if ma.iloc[-1] > ma.iloc[0] else '↓ Decreasing'}"

    elif metric == "ratio":
        if not column2:
            return "column2 required for ratio calculation."
        column2 = _fuzzy_match_column(column2, df.columns)
        if column2 not in df.columns:
            return f"Column2 '{column2}' not found."
        ratio = df[column].sum() / df[column2].sum()
        return f"Ratio of {column} to {column2}: {ratio:.4f} ({ratio*100:.2f}%)"

    elif metric == "cumulative":
        cumsum = series.cumsum()
        return f"Cumulative {column}:\nTotal: {cumsum.iloc[-1]:,.2f}\nMidpoint: {cumsum.iloc[len(cumsum)//2]:,.2f}"

    elif metric in ("mom_change", "yoy_change"):
        date_cols = df.select_dtypes(include=["datetime64"]).columns
        if len(date_cols) == 0:
            return "No date column found for period comparison."
        dc = date_cols[0]
        period = "M" if metric == "mom_change" else "Y"
        label = "Month" if metric == "mom_change" else "Year"
        grouped = df.groupby(df[dc].dt.to_period(period))[column].sum()
        changes = grouped.pct_change() * 100
        result = pd.DataFrame({"value": grouped, "change_%": changes}).tail(12)
        return f"{label}-over-{label} change for {column}:\n{result.to_string()}"

    return f"Metric {metric} not recognized."


def _tool_detect_anomalies(df: pd.DataFrame, args: dict) -> str:
    column = _fuzzy_match_column(args.get("column"), df.columns)
    method = args.get("method", "iqr")

    if column not in df.columns:
        return f"Column '{column}' not found."

    series = df[column].dropna()

    if method == "zscore":
        mean = series.mean()
        std = series.std()
        if std == 0:
            return f"No variation in {column} — cannot detect anomalies."
        z_scores = np.abs((series - mean) / std)
        anomalies = series[z_scores > 2.5]
    else:  # IQR
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        anomalies = series[(series < lower) | (series > upper)]

    if len(anomalies) == 0:
        return f"No anomalies detected in {column}. Data looks consistent."

    return (
        f"Anomalies detected in {column} ({len(anomalies)} outliers):\n"
        f"Values: {anomalies.values.tolist()[:10]}\n"
        f"Normal range: {series.quantile(0.05):,.2f} to {series.quantile(0.95):,.2f}\n"
        f"These values are statistically unusual and may need investigation."
    )


def _tool_forecast(df: pd.DataFrame, args: dict) -> str:
    column = _fuzzy_match_column(args.get("column"), df.columns)
    periods = args.get("periods", 3)

    if column not in df.columns:
        return f"Column '{column}' not found."

    series = df[column].dropna()

    if len(series) < 3:
        return "Not enough data points for forecasting (need at least 3)."

    try:
        # Simple linear trend forecast
        x = np.arange(len(series))
        coeffs = np.polyfit(x, series.values, 1)
        slope, intercept = coeffs

        future_x = np.arange(len(series), len(series) + periods)
        forecast_vals = slope * future_x + intercept

        direction = "↑ Upward" if slope > 0 else "↓ Downward"
        confidence = min(95, max(50, int(70 + abs(np.corrcoef(x, series.values)[0, 1]) * 25)))

        result = f"Forecast for {column} (next {periods} periods):\n"
        for i, val in enumerate(forecast_vals, 1):
            result += f"  Period +{i}: {val:,.2f}\n"
        result += f"Trend direction: {direction}\n"
        result += f"Confidence: ~{confidence}%\n"
        result += f"Based on trend: {slope:+.2f} per period"

        return result
    except Exception as e:
        return f"Forecast error: {str(e)}"


def _tool_get_insights(insights: dict, args: dict) -> str:
    section = args.get("section", "all")

    if not insights:
        return "No insights generated yet. Please run analysis first."

    if section == "all":
        return json.dumps(insights, indent=2)
    elif section == "executive_summary":
        return insights.get("executive_summary", "No executive summary available.")
    else:
        analyses = insights.get("analyses", {})
        if section in analyses:
            return json.dumps(analyses[section], indent=2)
        return f"No {section} analysis available."


def _tool_compare_segments(df: pd.DataFrame, args: dict) -> str:
    value_col = _fuzzy_match_column(args.get("value_column"), df.columns)
    segment_col = _fuzzy_match_column(args.get("segment_column"), df.columns)
    top_n = args.get("top_n", 5)

    if value_col not in df.columns:
        return f"Value column '{value_col}' not found."
    if segment_col not in df.columns:
        return f"Segment column '{segment_col}' not found."

    result = df.groupby(segment_col)[value_col].agg([
        "sum", "mean", "count"
    ]).sort_values("sum", ascending=False).head(top_n)

    result["share_%"] = (result["sum"] / result["sum"].sum() * 100).round(2)

    return (
        f"Comparison of {value_col} by {segment_col} "
        f"(Top {top_n}):\n{result.to_string()}"
    )


# ── Fuzzy Column Matcher ───────────────────────────────────

def _fuzzy_match_column(col_name: str, columns) -> str:
    """Find closest matching column name even if slightly different."""
    if col_name is None:
        return ""
    if col_name in columns:
        return col_name

    col_lower = col_name.lower().strip()

    # Exact lowercase match
    for col in columns:
        if col.lower() == col_lower:
            return col

    # Partial match
    for col in columns:
        if col_lower in col.lower() or col.lower() in col_lower:
            return col

    # Return original if no match — error handled upstream
    return col_name


# ── Context Builder ────────────────────────────────────────

def build_data_context(df: pd.DataFrame, classification: dict) -> str:
    """Build rich text context from DataFrame for LLM system prompt."""
    from backend.data_processor import generate_data_summary
    summary = generate_data_summary(df, classification)

    lines = []
    lines.append(f"DATA TYPE: {classification['data_type']}")
    lines.append(f"ROWS: {classification['total_rows']:,} | COLUMNS: {classification['total_columns']}")
    lines.append(f"MISSING DATA: {classification['missing_pct']}%")
    lines.append(f"ALL COLUMNS: {', '.join(classification['columns'])}")

    # Intent-mapped columns — key for AI
    intents = classification.get("column_intents", {})
    if intents:
        lines.append("\nCOLUMN MAPPING (what each column represents):")
        for intent, col in intents.items():
            if intent != "id":
                lines.append(f"  {intent.upper()} → '{col}'")

    # Date range
    if "date_range" in summary:
        dr = summary["date_range"]
        lines.append(f"\nTIME PERIOD: {dr['min']} to {dr['max']} ({dr.get('periods', '?')} periods)")

    # Numeric summary
    if "numeric_stats" in summary:
        lines.append("\nNUMERIC SUMMARY:")
        for col, stats in list(summary["numeric_stats"].items())[:8]:
            lines.append(
                f"  {col}: total={stats.get('count', 0)*stats.get('mean', 0):,.0f}, "
                f"mean={stats.get('mean', 0):,.2f}, "
                f"min={stats.get('min', 0):,.2f}, "
                f"max={stats.get('max', 0):,.2f}"
            )

    # Category breakdown
    if "categorical_counts" in summary:
        lines.append("\nCATEGORY BREAKDOWN:")
        for col, counts in list(summary["categorical_counts"].items())[:3]:
            top = list(counts.items())[:4]
            lines.append(f"  {col}: " + ", ".join([f"{k}({v})" for k, v in top]))

    # Quality flags
    if summary.get("quality_flags"):
        lines.append("\nDATA QUALITY NOTES:")
        for flag in summary["quality_flags"]:
            lines.append(f"  ⚠ {flag}")

    # Sample data
    sample = df.head(3).to_string(index=False, max_cols=10)
    lines.append(f"\nSAMPLE ROWS:\n{sample}")

    return "\n".join(lines)


# ── Main Analysis Engine ───────────────────────────────────

def generate_insights(
    df: pd.DataFrame,
    classification: dict,
    analysis_types: list,
) -> dict:
    """Run AI analysis and return structured insights."""
    data_context = build_data_context(df, classification)
    analysis_str = ", ".join([a.title() for a in analysis_types])

    prompt = f"""You are Deciora, an elite business intelligence AI for MSMEs.
Analyze the following business data and provide {analysis_str} analysis.

{data_context}

Return a JSON object with EXACTLY this structure:
{{
  "session_title": "Brief descriptive title (max 6 words)",
  "data_health": {{
    "score": <0-100 integer>,
    "issues": ["issue1", "issue2"],
    "strengths": ["strength1", "strength2"]
  }},
  "analyses": {{
    "descriptive": {{
      "summary": "2-3 sentence summary of what the data shows",
      "key_metrics": [
        {{"label": "Metric Name", "value": "formatted value", "trend": "up/down/stable"}}
      ],
      "patterns": ["pattern1", "pattern2", "pattern3"]
    }},
    "diagnostic": {{
      "root_causes": ["cause1", "cause2"],
      "anomalies": ["anomaly1"],
      "correlations": ["correlation insight"]
    }},
    "predictive": {{
      "forecast_summary": "What is likely to happen",
      "predictions": [
        {{"metric": "name", "direction": "up/down", "confidence": "72%", "reasoning": "..."}}
      ],
      "risks": ["risk1", "risk2"]
    }},
    "prescriptive": {{
      "top_actions": [
        {{"priority": "HIGH/MEDIUM/LOW", "action": "Specific action", "expected_impact": "Impact"}}
      ],
      "quick_wins": ["quick win 1", "quick win 2"]
    }}
  }},
  "executive_summary": "3-4 sentence overall summary for MSME owner"
}}

Only include analyses requested: {analysis_str}.
Use ACTUAL column names from the data when referencing metrics.
Return ONLY valid JSON, no markdown fences."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2500,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def generate_charts(df: pd.DataFrame, classification: dict) -> list:
    """Generate Plotly chart specs from data."""
    charts = []
    intents = classification.get("column_intents", {})
    num_cols = classification["numeric_columns"]
    date_cols = classification["date_columns"]
    cat_cols = classification["categorical_columns"]

    # Smart column selection using intents
    revenue_col = intents.get("revenue") or (num_cols[0] if num_cols else None)
    date_col = intents.get("date") or (date_cols[0] if date_cols else None)
    category_col = intents.get("category") or (cat_cols[0] if cat_cols else None)

    DARK_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,21,53,0.8)",
        font=dict(color="#e0e8ff", size=11),
        margin=dict(l=40, r=20, t=40, b=40),
    )

    # Chart 1: Time series
    if date_col and revenue_col:
        try:
            ts = df[[date_col, revenue_col]].dropna().sort_values(date_col)
            fig = px.line(
                ts, x=date_col, y=revenue_col,
                title=f"{revenue_col.replace('_',' ').title()} Over Time",
                template="plotly_dark",
                color_discrete_sequence=["#4A9EF5"],
            )
            fig.update_layout(**DARK_LAYOUT)
            fig.update_traces(line=dict(width=2.5))
            charts.append({"type": "time_series", "figure": fig.to_json(),
                          "title": fig.layout.title.text})
        except Exception:
            pass

    # Chart 2: Bar by category
    if category_col and revenue_col:
        try:
            grp = df.groupby(category_col)[revenue_col].sum()\
                    .sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(
                grp, x=category_col, y=revenue_col,
                title=f"{revenue_col.replace('_',' ').title()} by {category_col.replace('_',' ').title()}",
                template="plotly_dark",
                color=revenue_col,
                color_continuous_scale=["#1a237e", "#4A9EF5", "#a78bfa"],
            )
            fig.update_layout(**DARK_LAYOUT)
            charts.append({"type": "bar", "figure": fig.to_json(),
                          "title": fig.layout.title.text})
        except Exception:
            pass

    # Chart 3: Distribution
    if revenue_col:
        try:
            fig = px.histogram(
                df, x=revenue_col,
                title=f"Distribution of {revenue_col.replace('_',' ').title()}",
                template="plotly_dark",
                color_discrete_sequence=["#a78bfa"],
                nbins=25,
            )
            fig.update_layout(**DARK_LAYOUT)
            charts.append({"type": "histogram", "figure": fig.to_json(),
                          "title": fig.layout.title.text})
        except Exception:
            pass

    # Chart 4: Correlation heatmap
    if len(num_cols) >= 3:
        try:
            corr = df[num_cols[:8]].corr()
            fig = px.imshow(
                corr,
                title="Column Correlations",
                template="plotly_dark",
                color_continuous_scale=["#1a237e", "#4A9EF5", "#a78bfa"],
                text_auto=".2f",
                aspect="auto",
            )
            fig.update_layout(**DARK_LAYOUT)
            charts.append({"type": "heatmap", "figure": fig.to_json(),
                          "title": fig.layout.title.text})
        except Exception:
            pass

    return charts


# ── Agentic RAG Chat ───────────────────────────────────────

def chat_with_data(
    user_message: str,
    df: pd.DataFrame,
    classification: dict,
    insights: dict,
    chat_history: list,
) -> str:
    """
    Agentic RAG Chat — GPT-4o with function calling.
    Agent decides which tools to use, executes them,
    and reasons over real data before answering.
    """
    data_context = build_data_context(df, classification)

    system_prompt = f"""You are Deciora, an elite AI business intelligence advisor for MSMEs.
You have access to the user's actual business data and powerful analysis tools.

IMPORTANT RULES:
1. ALWAYS use tools to get actual numbers before answering — never guess
2. If unsure which column to use, check the COLUMN MAPPING below
3. Be specific — give exact numbers from the data
4. Be concise but insightful — MSME owners are busy
5. If data is insufficient, say so honestly
6. Format responses clearly with numbers highlighted

{data_context}

You have these tools available:
- query_data: Get actual values from the data
- calculate_metric: Compute growth rates, changes, ratios
- detect_anomalies: Find outliers
- forecast: Project future trends
- get_insights: Retrieve generated analysis
- compare_segments: Compare categories

Always use at least one tool before answering factual questions about the data."""

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]

    # Add chat history (last 8 messages)
    for msg in chat_history[-8:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"],
        })

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    # ── Agentic Loop ───────────────────────────────────────
    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=1000,
        )

        response_message = response.choices[0].message

        # If no tool calls — we have final answer
        if not response_message.tool_calls:
            return response_message.content.strip()

        # Add assistant message with tool calls
        messages.append(response_message)

        # Execute each tool call
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except Exception:
                tool_args = {}

            # Execute tool
            tool_result = execute_tool(
                tool_name, tool_args, df, classification, insights
            )

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            })

    # Fallback if max iterations hit
    return "I analyzed your data but the query was too complex. Please try a more specific question."


def generate_session_title(df: pd.DataFrame, classification: dict, analysis_types: list) -> str:
    """Generate smart session title."""
    data_type = classification.get("data_type", "Business")
    analysis_str = " + ".join([a.title() for a in analysis_types[:2]])
    return f"{data_type} — {analysis_str}"