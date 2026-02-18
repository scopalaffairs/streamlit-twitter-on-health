# streamlit-twitter-on-health

## Dissecting the public health discourse in the post-pandemic era
### Analysing hashtags across the globe

#### Explore insightful trends on Twitter by visiting the interactive visualization of the sentiment analysis
https://scopalaffairs-streamlit-twitter-on-hea-twitter-on-health-2jfica.streamlit.app/


![Emotions of tweets across the globe tagged with #WHO](plots/emotions_who.png)

![Emotions by Country tagged #WHO](plots/emotions_country_who.png)

![Emotions of tweets across the globe tagged with #monkeypox](plots/emotions_monkeypox.png)

![Emotions by Country tagged #monkeypox](plots/emotions_country_monkeypox.png)

![Emotions of tweets across the globe tagged #covid](plots/emotions_covid.png)

![Emotions by Country tagged #covid](plots/emotions_country_covid.png)

## Setup (first time only)

Download static reference data (not in git):
```bash
curl -o data-final/countries.geojson \
  "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
curl -o data-final/plotly_countries.csv \
  "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
```

## Deployment (Production Server)

The app runs as user `deploy` on port 8501.

**Pull latest changes and restart:**
```bash
cd /home/deploy/streamlit-twitter-on-health
git pull
pkill -f "streamlit run"
nohup streamlit run twitter_on_health.py --server.port=8501 --server.headless=true &
```

**Check if running:**
```bash
ps aux | grep streamlit
```
