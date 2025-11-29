# Data Directory

## Dataset Overview

This directory contains the Facebook Ads performance dataset used for analysis.

### File: `synthetic_fb_ads_undergarments.csv`

**Description**: Synthetic eCommerce Facebook Ads campaign data for undergarments/apparel vertical.

**Rows**: ~1000-5000 records (varies by dataset)

**Date Range**: Typically 30-90 days of campaign data

## Schema

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| `campaign_name` | String | Unique campaign identifier | "Summer_Comfort_2024", "Retarget_Q1" |
| `adset_name` | String | Ad set within campaign | "Broad_Audience_1", "Lookalike_Women_25-34" |
| `date` | String (YYYY-MM-DD) | Date of performance metrics | "2024-01-15" |
| `spend` | Float | Daily ad spend in USD | 125.50 |
| `impressions` | Integer | Number of ad impressions | 15000 |
| `clicks` | Integer | Number of clicks | 450 |
| `ctr` | Float | Click-through rate (clicks/impressions) | 0.03 (3%) |
| `purchases` | Integer | Number of conversions/purchases | 12 |
| `revenue` | Float | Total revenue generated in USD | 350.00 |
| `roas` | Float | Return on ad spend (revenue/spend) | 2.8 |
| `creative_type` | String | Ad creative format | "image", "video", "carousel" |
| `creative_message` | String | Ad copy/headline text | "Experience Ultimate Comfort" |
| `audience_type` | String | Audience targeting type | "broad", "retargeting", "lookalike" |
| `platform` | String | Social media platform | "Facebook", "Instagram" |
| `country` | String | Target country/region | "US", "UK", "CA" |

## Data Quality Notes

- **No missing values**: All columns are populated
- **Spend > 0**: All records have positive spend
- **ROAS calculation**: Pre-calculated as `revenue / spend`
- **CTR calculation**: Pre-calculated as `clicks / impressions`
- **Date format**: ISO 8601 (YYYY-MM-DD)

## Usage in Code

### Loading Data

```python
from src.agents.data_agent import DataAgent

agent = DataAgent()
df, summary = agent.load_and_summarize("data/synthetic_fb_ads_undergarments.csv")
```

### Configuration

Set data path in `config/config.yaml`:

```yaml
data:
  csv_path: "data/synthetic_fb_ads_undergarments.csv"
```

Or override via environment variable:

```bash
export DATA_CSV_PATH="data/synthetic_fb_ads_undergarments.csv"
```

## Sample Data (First 3 Rows)

```csv
campaign_name,adset_name,date,spend,impressions,clicks,ctr,purchases,revenue,roas,creative_type,creative_message,audience_type,platform,country
Summer_Comfort,Broad_Women,2024-01-01,100.00,12000,360,0.03,10,280.00,2.80,image,Experience Ultimate Comfort,broad,Instagram,US
Fall_Collection,Retarget_Cart,2024-01-01,150.00,8000,200,0.025,15,450.00,3.00,video,Premium Quality You Deserve,retargeting,Facebook,US
Winter_Sale,Lookalike_High,2024-01-01,200.00,18000,270,0.015,8,320.00,1.60,carousel,Limited Time Offer - 30% Off,lookalike,Instagram,UK
```

## Metrics Thresholds (Benchmarks)

Based on industry standards for eCommerce:

- **Good CTR**: ≥ 2% (0.02)
- **Good ROAS**: ≥ 2.5
- **Low CTR**: < 2% (triggers creative recommendations)
- **ROAS Decline**: > 20% drop over 7 days (triggers investigation)

## Data Source

This is a **synthetic dataset** generated for the Kasparro assignment. It mimics realistic Facebook Ads performance patterns but does not represent real campaign data.

## File Size

Approximately 200-500 KB depending on number of records.

## Troubleshooting

### Issue: File not found

**Error**: `FileNotFoundError: data/synthetic_fb_ads_undergarments.csv`

**Solution**: 
1. Verify file exists in `data/` directory
2. Check `config/config.yaml` has correct path
3. Use absolute path if needed

### Issue: CSV parsing errors

**Error**: `pandas.errors.ParserError`

**Solution**:
1. Ensure CSV is properly formatted (comma-delimited)
2. Check for special characters in creative_message field
3. Verify file encoding is UTF-8

### Issue: Missing columns

**Error**: `KeyError: 'column_name'`

**Solution**:
1. Verify all 15 required columns are present
2. Check for typos in column names (case-sensitive)
3. Ensure no extra/missing commas in CSV header

## Adding New Data

To use your own dataset:

1. **Match the schema**: Ensure all 15 columns are present with exact names
2. **Validate data types**: Follow the types in schema table above
3. **Update config**: Point `data.csv_path` to your file
4. **Test**: Run `pytest tests/test_evaluator.py::TestDataAgent` to verify format

## Privacy & Security

⚠️ **Do not commit real campaign data** to version control.

If using real data:
1. Add CSV files to `.gitignore`
2. Store data outside the repo
3. Use environment variables for paths
4. Anonymize campaign names and creative messages
