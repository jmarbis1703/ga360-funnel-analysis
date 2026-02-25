"""GA360 Funnel Analysis project.

Reads the two raw CSV exports from BigQuery, cleans them, engineers
session-level features, and writes analysis-ready parquet files to the
data/ directory."""

import os
import pandas as pd
import numpy as np

# Configuration
RAW_FUNNEL_FILE = "data/session_funnel.csv"
RAW_PRODUCT_FILE = "data/product_performance.csv"
OUTPUT_DIR = "data"

FUNNEL_STAGES = [
    "reached_home",
    "reached_category_view",
    "reached_product_view",
    "reached_add_to_cart",
    "reached_checkout",
    "reached_transaction",
]

STAGE_LABELS = [
    "Home",
    "Category View",
    "Product View",
    "Add to Cart",
    "Checkout",
    "Transaction",
]

# Outlier Thresholds
REVENUE_CAP_PERCENTILE = 99.5  # Winsorize converter revenue at this percentile
MAX_PAGEVIEWS = 200  # Sessions beyond this are most certainly bots or crawlers
MAX_TIME_ON_SITE = 10800  # 3 hours, sessions beyond this are likely abandoned tabs
MAX_PAGES_PER_SECOND = 2.0   # anything faster is non-human navigation
MIN_PAGEVIEWS_FOR_SPEED_CHECK = 5   # Only apply speed check to sessions with enough pages to judge

# Loading
def load_session_funnel(filepath):
    df = pd.read_csv(filepath, dtype={"fullVisitorId": str})
    print(f"Loaded session funnel: {len(df):,} rows, {df.shape[1]} columns")
    return df

def load_product_performance(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded product performance: {len(df):,} rows, {df.shape[1]} columns")
    return df



# Cleaning
def clean_session_funnel(df):
    """Convert null pageview and time-on-site values (single-hit bounces) to zero. 
    This ensures aggregation functions process every row."""
    rows_before = len(df)

    # Nulls to 0
    df["total_pageviews"] = df["total_pageviews"].fillna(0).astype(int)
    df["time_on_site"] = df["time_on_site"].fillna(0).astype(int)
    df["transaction_revenue_usd"] = df["transaction_revenue_usd"].fillna(0.0)

    # date-time
    df["session_date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d")

    # lowercases
    df["device_category"] = df["device_category"].str.lower().str.strip()

    # whitespaces
    df["country"] = df["country"].str.strip()

    rows_after = len(df)
    print(f"Cleaning complete. Rows: {rows_before:,} -> {rows_after:,} (no rows dropped)")
    return df


def remove_outliers(df):
    """Remove sessions that would distort business metrics due to bot traffic,
    test transactions, or measurement artifacts."""

    #Bot /Crawlers
    rows_before = len(df)
    mask_extreme_pv = df["total_pageviews"] > MAX_PAGEVIEWS
    bot_pv_count = mask_extreme_pv.sum()

    #speed
    has_time = df["time_on_site"] > 0
    enough_pages = df["total_pageviews"] >= MIN_PAGEVIEWS_FOR_SPEED_CHECK
    pages_per_sec = df["total_pageviews"] / df["time_on_site"].replace(0, np.nan)
    mask_speed_bot = has_time & enough_pages & (pages_per_sec > MAX_PAGES_PER_SECOND)
    bot_speed_count = mask_speed_bot.sum()

    # Multi signal
    mask_bot = mask_extreme_pv | mask_speed_bot
    total_bot_count = mask_bot.sum()

    df = df[~mask_bot].copy()

    print(f"Bot removal: {total_bot_count:,} sessions dropped "
          f"({bot_pv_count:,} extreme pageviews, "
          f"{bot_speed_count:,} impossible browsing speed)")

   
   # time on site camping
    capped_time_count = (df["time_on_site"] > MAX_TIME_ON_SITE).sum()
    df["time_on_site"] = df["time_on_site"].clip(upper=MAX_TIME_ON_SITE)

    print(f"Time-on-site capping: {capped_time_count:,} sessions "
          f"capped at {MAX_TIME_ON_SITE:,}s ({MAX_TIME_ON_SITE // 3600}h)")

    # Revenue Winsorization
    converters = df.loc[df["transaction_revenue_usd"] > 0, "transaction_revenue_usd"]
    revenue_cap = converters.quantile(REVENUE_CAP_PERCENTILE / 100)
    capped_rev_count = (df["transaction_revenue_usd"] > revenue_cap).sum()

    df["transaction_revenue_usd"] = df["transaction_revenue_usd"].clip(upper=revenue_cap)

    print(f"Revenue Winsorization: {capped_rev_count:,} transactions "
          f"capped at ${revenue_cap:,.2f} "
          f"(p{REVENUE_CAP_PERCENTILE} of converter revenue)")


    # Summary
    rows_after = len(df)
    rows_dropped = rows_before - rows_after
    print(f"Outlier handling complete. "
          f"Rows: {rows_before:,} -> {rows_after:,} "
          f"({rows_dropped:,} dropped, "
          f"{capped_time_count + capped_rev_count:,} values capped)")
    return df

#cleaning
def clean_product_performance(df):
    """Normalizing values to Uncategorized to ensure category level aggregation remain accurate."""

    placeholder_patterns = ["(not set)", "${escCatTitle}", "(not provided)"]
    df["product_category_clean"] = df["product_category"].apply(
        lambda x: "Uncategorized" if x in placeholder_patterns else x
    )

    # Strip 'Home/' prefix
    df["product_category_clean"] = (
        df["product_category_clean"]
        .str.replace("Home/", "", regex=False)
        .str.strip("/")
    )

    print(f"Product cleaning complete. {len(df):,} products across "
          f"{df['product_category_clean'].nunique()} clean categories")
    return df



# Feature Engineering
def engineer_session_features(df):
    """While raw flags only show if a stage was hit, derived features show total progression.
    - deepest_funnel_stage: Groups users by highest level of intent.
    - is_converter: Success metric for statistical tests."""

    # (0 = Home only, 5 = Transaction)
    stage_columns = FUNNEL_STAGES
    df["deepest_funnel_stage"] = df[stage_columns].sum(axis=1) - 1
    df["deepest_funnel_stage"] = df["deepest_funnel_stage"].clip(lower=0)

    df["is_converter"] = (df["reached_transaction"] == 1).astype(int)

    df["engagement_tier"] = pd.cut(
        df["total_pageviews"],
        bins=[-1, 1, 3, 7, 1000],
        labels=["Bounce", "Low", "Medium", "High"],
    )

    df["duration_bucket"] = pd.cut(
        df["time_on_site"],
        bins=[-1, 0, 60, 300, 100000],
        labels=["Zero", "Under 1 min", "1-5 min", "Over 5 min"],
    )

    # Grouping
    medium_map = {
        "(none)": "Direct",
        "organic": "Organic Search",
        "referral": "Referral",
        "cpc": "Paid Search",
        "affiliate": "Affiliate",
        "cpm": "Display",
        "(not set)": "Other",
    }
    df["channel_group"] = df["traffic_medium"].map(medium_map).fillna("Other")

    df["is_us"] = (df["country"] == "United States").astype(int)

    feature_count = 6  
    print(f"Feature engineering complete. Added {feature_count} new columns")
    return df


def engineer_product_features(df):
    """Adding conversion rate and revenue-per-session to product data.
    These metrics normalize for traffic differences, revealing which products convert efficiently regardless of session volume."""
    df["conversion_rate"] = df["purchases"] / df["sessions"]
    df["revenue_per_session"] = df["total_revenue_usd"] / df["sessions"]

    print(f"Product features complete."
          f"Median conversion rate: {df['conversion_rate'].median():.1%}, "
          f"Median rev/session: ${df['revenue_per_session'].median():.2f}")
    return df



# Saving
def save_outputs(funnel_df, product_df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    funnel_path = os.path.join(output_dir, "session_funnel_clean.csv")
    product_path = os.path.join(output_dir, "product_performance_clean.csv")
    funnel_df.to_csv(funnel_path, index=False)
    product_df.to_csv(product_path, index=False)
    print(f"Saved: {funnel_path} ({len(funnel_df):,} rows)")
    print(f"Saved: {product_path} ({len(product_df):,} rows)")


# Pipeline
def run_pipeline():
    """Execute the full ETL pipeline end to end."""
    print("=" * 60)
    print("GA360 FUNNEL ANALYSIS -- DATA PIPELINE")

    # load
    print("\nLoading raw data")
    funnel = load_session_funnel(RAW_FUNNEL_FILE)
    products = load_product_performance(RAW_PRODUCT_FILE)

    # clean
    print("\nCleaning session funnel")
    funnel = clean_session_funnel(funnel)

    # clean perf
    print("\nCleaning product performance")
    products = clean_product_performance(products)

    # feature engineering
    print("\nEngineering session features")
    funnel = engineer_session_features(funnel)
    products = engineer_product_features(products)

    # save
    print("\nSaving outputs")
    save_outputs(funnel, products, OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    return funnel, products

if __name__ == "__main__":
    run_pipeline()
