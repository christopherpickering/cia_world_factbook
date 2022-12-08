import json
import os

import requests

BASE_URL = "https://www.cia.gov/the-world-factbook/page-data"

COUNTRY_URLS = []
OUT = {}

# get country urls
p = requests.get(f"{BASE_URL}/countries/page-data.json")

page_json = p.json()

results = page_json["result"]["data"]["countries"]["edges"]

# iterate countries and get the summary

for country in results:
    node = country["node"]
    # print(country["node"])

    # country summary
    # uri + /summaries/page-data.json
    slug = node["uri"].replace("/countries/", "").strip("/")
    p = requests.get(f"{BASE_URL}{node['uri']}/summaries/page-data.json")
    try:
        # not all items in the country list are really countries.
        page_json = p.json()
        country_results = json.loads(page_json["result"]["data"]["country"]["json"])
    except:
        print("error in ", country["node"])
        continue

    # print(json.dumps(country_results, indent=4))
    # print(country_results)

    data = {
        "title": node["title"],
        "code": node["code"],
        "uri": BASE_URL + node["uri"],
        "region": country_results["region"],
    }
    OUT[slug] = data

    # break


META_URLS = [
    "/field/religions",
    "/field/location",
    "/field/languages",
    "/field/geographic-coordinates",
    "/field/area-comparative",
    "/field/land-boundaries",
    "/field/coastline",
    "/field/maritime-claims",
    "/field/climate",
    "/field/terrain",
    "/field/elevation",
    "/field/natural-resources",
    "/field/land-use",
    "/field/irrigated-land",
    "/field/major-lakes-area-sq-km",
    "/field/major-rivers-by-length-in-km",
    "/field/major-watersheds-area-sq-km",
    "/field/population-distribution",
    "/field/natural-hazards",
    "/field/geography-note",
    "/field/population",
    "/field/nationality",
    "/field/ethnic-groups",
    "/field/background",
    "/field/map-references",
    "/field/area",
    "/field/age-structure",
    "/field/dependency-ratios",
    "/field/median-age",
    "/field/population-growth-rate",
    "/field/birth-rate",
    "/field/death-rate",
    "/field/net-migration-rate",
    "/field/urbanization",
    "/field/major-urban-areas-population",
    "/field/sex-ratio",
    "/field/mothers-mean-age-at-first-birth",
    "/field/maternal-mortality-ratio",
    "/field/infant-mortality-rate",
    "/field/life-expectancy-at-birth",
    "/field/total-fertility-rate",
    "/field/contraceptive-prevalence-rate",
    "/field/drinking-water-source",
    "/field/current-health-expenditure",
    "/field/physicians-density",
    "/field/hospital-bed-density",
    "/field/sanitation-facility-access",
    "/field/hiv-aids-adult-prevalence-rate",
    "/field/major-infectious-diseases",
    "/field/obesity-adult-prevalence-rate",
    "/field/alcohol-consumption-per-capita",
    "/field/tobacco-use",
    "/field/children-under-the-age-of-5-years-underweight",
    "/field/child-marriage",
    "/field/education-expenditures",
    "/field/literacy",
    "/field/school-life-expectancy-primary-to-tertiary-education",
    "/field/unemployment-youth-ages-15-24",
    "/field/environment-current-issues",
    "/field/environment-international-agreements",
    "/field/air-pollutants",
    "/field/revenue-from-forest-resources",
    "/field/revenue-from-coal",
    "/field/food-insecurity",
    "/field/waste-and-recycling",
    "/field/total-water-withdrawal",
    "/field/total-renewable-water-resources",
    "/field/country-name",
    "/field/government-type",
    "/field/capital",
    "/field/administrative-divisions",
    "/field/independence",
    "/field/national-holiday",
    "/field/constitution",
    "/field/legal-system",
    "/field/international-law-organization-participation",
    "/field/citizenship",
    "/field/suffrage",
    "/field/executive-branch",
    "/field/legislative-branch",
    "/field/judicial-branch",
    "/field/political-parties-and-leaders",
    "/field/international-organization-participation",
    "/field/diplomatic-representation-in-the-us",
    "/field/diplomatic-representation-from-the-us",
    "/field/flag-description",
    "/field/national-symbols",
    "/field/national-anthem",
    "/field/national-heritage",
    "/field/economic-overview",
    "/field/real-gdp-purchasing-power-parity",
    "/field/real-gdp-growth-rate",
    "/field/real-gdp-per-capita",
    "/field/gdp-official-exchange-rate",
    "/field/inflation-rate-consumer-prices",
    "/field/gdp-composition-by-sector-of-origin",
    "/field/gdp-composition-by-end-use",
    "/field/agricultural-products",
    "/field/industries",
    "/field/industrial-production-growth-rate",
    "/field/labor-force",
    "/field/labor-force-by-occupation",
    "/field/unemployment-rate",
    "/field/population-below-poverty-line",
    "/field/gini-index-coefficient-distribution-of-family-income",
    "/field/household-income-or-consumption-by-percentage-share",
    "/field/budget",
    "/field/budget-surplus-or-deficit",
    "/field/public-debt",
    "/field/taxes-and-other-revenues",
    "/field/fiscal-year",
    "/field/current-account-balance",
    "/field/exports",
    "/field/exports-partners",
    "/field/exports-commodities",
    "/field/imports",
    "/field/imports-partners",
    "/field/imports-commodities",
    "/field/reserves-of-foreign-exchange-and-gold",
    "/field/debt-external",
    "/field/exchange-rates",
    "/field/electricity-access",
    "/field/electricity",
    "/field/electricity-generation-sources",
    "/field/coal",
    "/field/petroleum",
    "/field/refined-petroleum-products-production",
    "/field/refined-petroleum-products-exports",
    "/field/refined-petroleum-products-imports",
    "/field/natural-gas",
    "/field/carbon-dioxide-emissions",
    "/field/energy-consumption-per-capita",
    "/field/telephones-fixed-lines",
    "/field/telephones-mobile-cellular",
    "/field/telecommunication-systems",
    "/field/broadcast-media",
    "/field/internet-country-code",
    "/field/internet-users",
    "/field/broadband-fixed-subscriptions",
    "/field/national-air-transport-system",
    "/field/civil-aircraft-registration-country-code-prefix",
    "/field/airports",
    "/field/airports-with-paved-runways",
    "/field/airports-with-unpaved-runways",
    "/field/heliports",
    "/field/pipelines",
    "/field/roadways",
    "/field/waterways",
    "/field/ports-and-terminals",
    "/field/military-and-security-forces",
    "/field/military-expenditures",
    "/field/military-and-security-service-personnel-strengths",
    "/field/military-equipment-inventories-and-acquisitions",
    "/field/military-service-age-and-obligation",
    "/field/military-note",
    "/field/terrorist-groups",
    "/field/disputes-international",
    "/field/refugees-and-internally-displaced-persons",
    "/field/trafficking-in-persons",
    "/field/illicit-drugs",
]

for url in META_URLS:
    slug = url.replace("/field/", "").strip("/")
    p = requests.get(f"{BASE_URL}{url}/page-data.json")
    page_json = json.loads(p.json()["result"]["data"]["page"]["json"])["countries"]

    for country in page_json:
        if country["slug"] in OUT:
            OUT[country["slug"]][slug] = country["data"]
        else:
            print(country["slug"], "is missing from build.")

RANK_URLS = [
    "/field/median-age/country-comparison",
    "/field/median-age/country-comparison",
    "/field/population-growth-rate/country-comparison",
    "/field/birth-rate/country-comparison",
    "/field/death-rate/country-comparison",
    "/field/net-migration-rate/country-comparison",
    "/field/maternal-mortality-ratio/country-comparison",
    "/field/infant-mortality-rate/country-comparison",
    "/field/life-expectancy-at-birth/country-comparison",
    "/field/total-fertility-rate/country-comparison",
    "/field/obesity-adult-prevalence-rate/country-comparison",
    "/field/alcohol-consumption-per-capita/country-comparison",
    "/field/tobacco-use/country-comparison",
    "/field/children-under-the-age-of-5-years-underweight/country-comparison",
    "/field/education-expenditures/country-comparison",
    "/field/revenue-from-forest-resources/country-comparison",
    "/field/revenue-from-coal/country-comparison",
    "/field/real-gdp-purchasing-power-parity/country-comparison",
    "/field/real-gdp-growth-rate/country-comparison",
    "/field/real-gdp-per-capita/country-comparison",
    "/field/inflation-rate-consumer-prices/country-comparison",
    "/field/industrial-production-growth-rate/country-comparison",
    "/field/labor-force/country-comparison",
    "/field/unemployment-rate/country-comparison",
    "/field/unemployment-youth-ages-15-24/country-comparison",
    "/field/gini-index-coefficient-distribution-of-family-income/country-comparison",
    "/field/budget-surplus-or-deficit/country-comparison",
    "/field/public-debt/country-comparison",
    "/field/taxes-and-other-revenues/country-comparison",
    "/field/current-account-balance/country-comparison",
    "/field/exports/country-comparison",
    "/field/imports/country-comparison",
    "/field/reserves-of-foreign-exchange-and-gold/country-comparison",
    "/field/debt-external/country-comparison",
    "/field/refined-petroleum-products-production/country-comparison",
    "/field/refined-petroleum-products-exports/country-comparison",
    "/field/refined-petroleum-products-imports/country-comparison",
    "/field/carbon-dioxide-emissions/country-comparison",
    "/field/energy-consumption-per-capita/country-comparison",
    "/field/telephones-fixed-lines/country-comparison",
    "/field/telephones-mobile-cellular/country-comparison",
    "/field/internet-users/country-comparison",
    "/field/broadband-fixed-subscriptions/country-comparison",
    "/field/airports/country-comparison",
    "/field/roadways/country-comparison",
    "/field/waterways/country-comparison",
    "/field/military-expenditures/country-comparison",
    "/field/population/country-comparison",
    "/field/area/country-comparison",
]

for url in RANK_URLS:
    slug = (
        url.replace("/field/", "").replace("/country-comparison", "").strip("/")
        + "-rank"
    )
    p = requests.get(f"{BASE_URL}{url}/page-data.json")
    page_json = json.loads(p.json()["result"]["data"]["page"]["rankingJson"])[
        "rankings"
    ]

    for country in page_json:
        if country["slug"] in OUT:
            OUT[country["slug"]][slug] = country["ranking"]
        else:
            print(country["slug"], "is missing from build.")

if not os.path.isdir("data"):
    os.makedirs("data")

json_object = json.dumps(OUT, indent=4)
with open("data/cia_world_factbook.json", "w") as outfile:
    outfile.write(json_object)

"""
other interesting urls

/references/terrorist-organizations

"""
