# ==============================================
# SMAC-Members-Inventory-Dashboard 
# ==============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ----------------------------------------------
# Setup: Define constants & helper functions
# ----------------------------------------------

DATA_FOLDER = "data"
country_name_map = {
    "ARG": "Argentina", "BRA": "Brazil", "CAN": "Canada", "DEU": "Germany",
    "ESP": "Spain", "IND": "India", "KOR": "South Korea", "MEX": "Mexico",
    "NGA": "Nigeria", "USA": "United States", "ZAF": "South Africa"
}
SMAC_COUNTRIES_FULL = [v for v in country_name_map.values()]
SMAC_COUNTRIES = list(country_name_map.keys())  # ← 新加的

AVAILABLE_YEARS = [2021, 2022, 2023, 2024]

def load_country_year_data(country_code, year):
    file_name = f"{country_code}_{year}.csv"
    file_path = os.path.join(DATA_FOLDER, file_name)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.warning(f"Data file not found for {country_code} {year}. Please check your folder.")
        return pd.DataFrame()

country_centroids = {
    "ARG": {"Country": "Argentina", "Lat": -38.4, "Lon": -63.6},
    "BRA": {"Country": "Brazil", "Lat": -14.2, "Lon": -51.9},
    "CAN": {"Country": "Canada", "Lat": 56.1, "Lon": -106.3},
    "DEU": {"Country": "Germany", "Lat": 51.2, "Lon": 10.5},
    "ESP": {"Country": "Spain", "Lat": 40.5, "Lon": -3.7},
    "IND": {"Country": "India", "Lat": 21.1, "Lon": 78.0},
    "KOR": {"Country": "South Korea", "Lat": 36.5, "Lon": 127.9},
    "MEX": {"Country": "Mexico", "Lat": 23.6, "Lon": -102.5},
    "NGA": {"Country": "Nigeria", "Lat": 9.1, "Lon": 8.7},
    "USA": {"Country": "United States", "Lat": 37.1, "Lon": -95.7},
    "ZAF": {"Country": "South Africa", "Lat": -30.6, "Lon": 22.9},
}

# Sector mapping
sector_map = {
    "electricity-generation": "power", "solid-fuel-transformation": "power",
    "heat-plants": "power", "cement": "manufacturing", "chemicals": "manufacturing",
    "aluminum": "manufacturing", "iron-and-steel": "manufacturing", "glass": "manufacturing",
    "lime": "manufacturing", "food-beverage-tobacco": "manufacturing", "wood-and-wood-products": "manufacturing",
    "pulp-and-paper": "manufacturing", "textiles-leather-apparel": "manufacturing", "other-manufacturing": "manufacturing",
    "petrochemical-steam-cracking": "manufacturing", "other-chemicals": "manufacturing", "other-metals": "manufacturing",
    "road-transportation": "transportation", "domestic-aviation": "transportation", "international-aviation": "transportation",
    "railways": "transportation", "other-transport": "transportation", "domestic-shipping": "transportation",
    "international-shipping": "transportation", "crop-residues": "agriculture", "cropland-fires": "agriculture",
    "rice-cultivation": "agriculture", "synthetic-fertilizer-application": "agriculture", "other-agricultural-soil-emissions": "agriculture",
    "enteric-fermentation-cattle-pasture": "agriculture", "enteric-fermentation-cattle-operation": "agriculture",
    "enteric-fermentation-other": "agriculture", "manure-left-on-pasture-cattle": "agriculture",
    "manure-management-cattle-operation": "agriculture", "manure-management-other": "agriculture",
    "manure-applied-to-soils": "agriculture", "coal-mining": "fossil-fuel-operations", "oil-and-gas-production": "fossil-fuel-operations",
    "oil-and-gas-transport": "fossil-fuel-operations", "oil-and-gas-refining": "fossil-fuel-operations",
    "other-fossil-fuel-operations": "fossil-fuel-operations", "solid-waste-disposal": "waste",
    "biological-treatment-of-solid-waste-and-biogenic": "waste", "incineration-and-open-burning-of-waste": "waste",
    "domestic-wastewater-treatment-and-discharge": "waste", "industrial-wastewater-treatment-and-discharge": "waste",
    "forest-land-clearing": "land-use-change", "forest-land-degradation": "land-use-change", "forest-land-fires": "land-use-change",
    "net-forest-land": "land-use-change", "net-shrubgrass": "land-use-change", "net-wetland": "land-use-change",
    "wetland-fires": "land-use-change", "shrubgrass-fires": "land-use-change", "removals": "land-use-change",
    "water-reservoirs": "land-use-change", "bauxite-mining": "mineral-extraction", "copper-mining": "mineral-extraction",
    "iron-mining": "mineral-extraction", "sand-quarrying": "mineral-extraction", "rock-quarrying": "mineral-extraction",
    "other-mining-quarrying": "mineral-extraction", "fluorinated-gases": "fluorinated-gases",
    "residential-onsite-fuel-usage": "other-energy-use", "non-residential-onsite-fuel-usage": "other-energy-use",
    "other-onsite-fuel-usage": "other-energy-use", "other-energy-use": "other-energy-use"
}

st.set_page_config(layout="wide")
st.title("SMAC Members Methane Inventory")

st.markdown("""
This dashboard displays methane (CH₄) emissions trends and comparisons across the SMAC group countries.

The data presented may be updated, revised, restructured, or removed at any time without prior notice.
While every effort is made to ensure accuracy, the data is provided as-is and may contain errors or omissions.

👉 You can also explore the SMAC Methane Emissions Sunburst Tool here:
[https://observablehq.com/@max-no-sekai/smac-methane-emissions-sunburst-tool](https://observablehq.com/@max-no-sekai/smac-methane-emissions-sunburst-tool)
""")


# ----------------------------------------------
# Tabs: Global View (Tab 1) | SMAC Group (Tab 2) | Comparison (Tab 3)
# ----------------------------------------------

st.markdown("---")
tab_selection = st.radio(
        "",  
        options=["🌎 SMAC Group Overview", "SMAC Member Methane Emissions", "Comparison Tool"],
        horizontal=True,
    )
st.markdown("---")


# ========== TAB 1: SMAC Group Overview – CH₄ Emissions ==========

if tab_selection == "🌎 SMAC Group Overview":
 
    st.header("🌍 SMAC Group Overview – CH₄ Emissions")
  
    selected_year_tab1 = st.selectbox("Select Year", AVAILABLE_YEARS, key='tab1_year')

    # Combine all country data for the selected year
    combined_df = pd.DataFrame()
    for country in SMAC_COUNTRIES:
        temp_df = load_country_year_data(country, selected_year_tab1)
        if not temp_df.empty:
            temp_df['country'] = country
            combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

    if not combined_df.empty:
        df_ch4_group = combined_df[combined_df['gas'] == 'ch4']

        # Aggregate by country
        country_emissions = (
            df_ch4_group.groupby('country')['total_emission']
            .sum()
            .reset_index()
            .sort_values(by='total_emission', ascending=False)
        )
        country_emissions['Country Full Name'] = country_emissions['country'].map(country_name_map)

        # Add centroid coordinates for real map style
        country_emissions["Lat"] = country_emissions["country"].apply(lambda x: country_centroids[x]["Lat"])
        country_emissions["Lon"] = country_emissions["country"].apply(lambda x: country_centroids[x]["Lon"])

        # Real Map Style (Mapbox) + Ranking Table (side by side)
        col_map, col_rank = st.columns([3, 1])

        with col_map:
            st.subheader(f"SMAC GROUP CH₄ Emissions Map  – {selected_year_tab1}")

            fig_mapbox = px.scatter_mapbox(
                country_emissions,
                lat="Lat",
                lon="Lon",
                size="total_emission",
                color="total_emission",
                hover_name="Country Full Name",
                size_max=50,
                zoom=1,
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={'total_emission': 'CH₄ Emissions'},
                title=f"CH₄ Emissions by Country ({selected_year_tab1})"
            )
            fig_mapbox.update_traces(
                hovertemplate=
            "<b>%{hovertext}</b><br>" +
            "CH₄ Emissions: %{marker.size:.2f}<br>" +
            "Lat: %{lat}<br>" +
            "Lon: %{lon}<extra></extra>")

            fig_mapbox.update_layout(
                mapbox_style="carto-positron",
                margin={"r":0, "t":30, "l":0, "b":0}
            )

            st.plotly_chart(fig_mapbox, use_container_width=True)

        with col_rank:
            st.subheader("CH₄ Emissions Ranking")
            country_emissions_rank = country_emissions.copy()
            country_emissions_rank['Rank'] = range(1, len(country_emissions_rank) + 1)
            country_emissions_rank = country_emissions_rank[['Rank', 'Country Full Name', 'total_emission']]
            country_emissions_rank.columns = ['Rank', 'Country', 'CH₄ Emissions']
            st.dataframe(country_emissions_rank, hide_index=True, use_container_width=True)

        # 2️⃣ Full-width: Sector Emissions Over Time (2021–2024)
        st.subheader("SMAC Group CH₄ Emissions by Sector (2021–2024)")

        combined_all_years = pd.DataFrame()
        for year in AVAILABLE_YEARS:
            for country in SMAC_COUNTRIES:
                temp_df = load_country_year_data(country, year)
                if not temp_df.empty:
                    temp_df['year'] = year
                    temp_df['country'] = country
                    combined_all_years = pd.concat([combined_all_years, temp_df], ignore_index=True)

        if not combined_all_years.empty:
            df_ch4_all = combined_all_years[combined_all_years['gas'] == 'ch4'].copy()
            df_ch4_all['sector'] = df_ch4_all['original_inventory_sector'].map(sector_map).fillna('other')

            sector_time_df = (
                df_ch4_all.groupby(['year', 'sector'])['total_emission']
                .sum()
                .reset_index()
            )

            fig_sector_over_time = px.bar(
                sector_time_df,
                x='year',
                y='total_emission',
                color='sector',
                labels={'total_emission': 'CH₄ Emissions', 'year': 'Year'},
                title="CH₄ Emissions by Sector Over Time"
            )
            st.plotly_chart(fig_sector_over_time, use_container_width=True)

        # 3️⃣ Full-width: Country Share Pie Chart
        st.subheader(f"Country Share of Total CH₄ Emissions ({selected_year_tab1})")

        fig_country_pie = px.pie(
            country_emissions,
            names='Country Full Name',
            values='total_emission',
            title=f"Country Share of Total CH₄ Emissions ({selected_year_tab1})"
        )
        st.plotly_chart(fig_country_pie, use_container_width=True)

        # 4️⃣ Full-width: Top 10 Emitting Locations Across SMAC Group
        st.subheader(f"Top 10 Emitting Locations Across SMAC Group ({selected_year_tab1})")

        top_locations_group = (
            df_ch4_group.groupby(['location', 'country'])['total_emission']
            .sum()
            .reset_index()
            .sort_values(by='total_emission', ascending=False)
            .head(10)
        )
        top_locations_group['Country Full Name'] = top_locations_group['country'].map(country_name_map)

        fig_top_locations = px.bar(
            top_locations_group,
            x='location',
            y='total_emission',
            color='Country Full Name',
            title=f"Top 10 Emitting Locations ({selected_year_tab1})",
            labels={'total_emission': 'CH₄ Emissions', 'location': 'Location'}
        )
        st.plotly_chart(fig_top_locations, use_container_width=True)


# ========== TAB 2: SMAC Group Methane Emissions ==========
elif tab_selection == "SMAC Member Methane Emissions":
    country_full = st.selectbox("Select a Country", SMAC_COUNTRIES_FULL, key='tab2_country')
    year = st.selectbox("Select a Year", AVAILABLE_YEARS, key='tab2_year')

    country_code = [k for k, v in country_name_map.items() if v == country_full][0]

    st.header(f"{country_full} ({year}) Methane Emissions")

    df = load_country_year_data(country_code, year)

    if not df.empty:
        df_ch4 = df[df['gas'] == 'ch4']

        # Sector Breakdown 
        st.subheader(f"{country_full} ({year}) – CH₄ Emissions by Sector")
        sector_df = df_ch4.groupby('original_inventory_sector')['total_emission'].sum().reset_index()
        sector_df['sector'] = sector_df['original_inventory_sector'].map(sector_map).fillna('other')
        sector_grouped = sector_df.groupby('sector')['total_emission'].sum().reset_index()

        fig_sector = px.bar(
            sector_grouped.sort_values(by='total_emission', ascending=False),
            x='sector',
            y='total_emission',
            labels={'total_emission': 'Emissions (CH₄)'},
            title="Sector Breakdown"
        )
        st.plotly_chart(fig_sector, use_container_width=True)

        # Pie Chart
        st.subheader(f"{country_full} ({year}) – Subsector Breakdown (CH₄)")
        fig_subsector = px.pie(sector_df, names='original_inventory_sector', values='total_emission',
                               title="Subsector Breakdown Pie Chart")
        fig_subsector.update_traces(
            textinfo='none',
            pull=[0.05]*len(sector_df),
            insidetextorientation='radial'
        )
        fig_subsector.update_layout(
            uniformtext_minsize=10,
            uniformtext_mode='hide',
            legend=dict(font=dict(size=10)),
            showlegend=True
        )
        st.plotly_chart(fig_subsector, use_container_width=True)

        # Top 10 Locations Table
        st.subheader(f"Top 10 Locations for CH₄ Emissions – {country_full} ({year})")
        top_locations = (
            df_ch4.groupby('location')['total_emission']
            .sum()
            .reset_index()
            .sort_values(by='total_emission', ascending=False)
            .head(10)
        )
        top_locations = top_locations.reset_index(drop=True)
        top_locations['Rank'] = top_locations.index + 1
        top_locations['CH₄ Emissions'] = top_locations['total_emission'].apply(lambda x: f"{x:.3f}")
        top_locations = top_locations[['Rank', 'location', 'CH₄ Emissions']]
        st.dataframe(top_locations, hide_index=True)

        # NEW: Add 2021–2024 Trend Chart for This Country
        st.subheader(f"{country_full} – CH₄ Emissions Trend (2021–2024)")
        
        combined_country_years = pd.DataFrame()
        for year_iter in AVAILABLE_YEARS:
            df_temp = load_country_year_data(country_code, year_iter)
            if not df_temp.empty:
                df_temp['year'] = year_iter
                combined_country_years = pd.concat([combined_country_years, df_temp], ignore_index=True)
                
        if not combined_country_years.empty:
            df_ch4_all = combined_country_years[combined_country_years['gas'] == 'ch4'].copy()
            df_ch4_all['sector'] = df_ch4_all['original_inventory_sector'].map(sector_map).fillna('other')
            
            sector_time_df = (
                df_ch4_all.groupby(['year', 'sector'])['total_emission']
                .sum()
                .reset_index())
            
            fig_trend = px.bar(
                sector_time_df,
                x='year', 
                y='total_emission',
                color='sector',
                labels={'total_emission': 'CH₄ Emissions', 'year': 'Year'},
                title=f"{country_full} CH₄ Emissions by Sector (2021–2024)")
            st.plotly_chart(fig_trend, use_container_width=True)


# ========== TAB 3: Comparison Tool ==========
elif tab_selection == "Comparison Tool":
   
    st.header("Compare CH₄ Emissions")

    # Side-by-side selectors for A and B
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Location A")
        country_a_full = st.selectbox("Country A", SMAC_COUNTRIES_FULL, key='a')
        year_a = st.selectbox("Year A", AVAILABLE_YEARS, key='year_a')
        country_a = [k for k, v in country_name_map.items() if v == country_a_full][0]
        df_a = load_country_year_data(country_a, year_a)

    with col2:
        st.subheader("Location B")
        country_b_full = st.selectbox("Country B", SMAC_COUNTRIES_FULL, key='b')
        year_b = st.selectbox("Year B", AVAILABLE_YEARS, key='year_b')
        country_b = [k for k, v in country_name_map.items() if v == country_b_full][0]
        df_b = load_country_year_data(country_b, year_b)

    # Side-by-side plots and tables for A and B
    col3, col4 = st.columns(2)
    with col3:
        if not df_a.empty:
            st.subheader(f"{country_a_full} ({year_a}) – Sector Breakdown")
            df_ch4_a = df_a[df_a['gas'] == 'ch4']
            sector_df_a = df_ch4_a.groupby('original_inventory_sector')['total_emission'].sum().reset_index()
            sector_df_a['sector'] = sector_df_a['original_inventory_sector'].map(sector_map).fillna('other')

            # Bar Chart
            fig_a = px.bar(sector_df_a.sort_values(by='total_emission', ascending=False),
                           x='sector', y='total_emission',
                           title=f"{country_a_full} – CH₄ Emissions by Sector")
            st.plotly_chart(fig_a, use_container_width=True, key='fig_a_bar')

            # Pie Chart
            fig_pie_a = px.pie(sector_df_a, names='original_inventory_sector', values='total_emission',
                               title=f"{country_a_full} – CH₄ Emissions by Subsector")
            fig_pie_a.update_traces(
                textinfo='none',
                pull=[0.05]*len(sector_df_a),
                insidetextorientation='radial'
            )
            fig_pie_a.update_layout(
                uniformtext_minsize=10,
                uniformtext_mode='hide',
                legend=dict(font=dict(size=10)),
                showlegend=True
            )
            st.plotly_chart(fig_pie_a, use_container_width=True, key='fig_a_pie')

            # Data Table
            st.subheader("Data Table – Location A")
            st.dataframe(sector_df_a)

            #  NEW: Add 2021–2024 Trend Chart for Location A
            st.subheader(f"{country_a_full} – CH₄ Emissions Trend (2021–2024)")
            
            combined_a_years = pd.DataFrame()
            for year_iter in AVAILABLE_YEARS:
                df_temp_a = load_country_year_data(country_a, year_iter)
                if not df_temp_a.empty:
                    df_temp_a['year'] = year_iter
                    combined_a_years = pd.concat([combined_a_years, df_temp_a], ignore_index=True)
                    
            if not combined_a_years.empty:
                df_ch4_all_a = combined_a_years[combined_a_years['gas'] == 'ch4'].copy()
                df_ch4_all_a['sector'] = df_ch4_all_a['original_inventory_sector'].map(sector_map).fillna('other')
                
                sector_time_df_a = (
                    df_ch4_all_a.groupby(['year', 'sector'])['total_emission']
                    .sum()
                    .reset_index())
                
                fig_trend_a = px.bar(
                    sector_time_df_a,
                    x='year',
                    y='total_emission',
                    color='sector',
                    labels={'total_emission': 'CH₄ Emissions', 'year': 'Year'},
                    title=f"{country_a_full} CH₄ Emissions by Sector (2021–2024)")
                st.plotly_chart(fig_trend_a, use_container_width=True, key='fig_trend_a')


    with col4:
        if not df_b.empty:
            st.subheader(f"{country_b_full} ({year_b}) – Sector Breakdown")
            df_ch4_b = df_b[df_b['gas'] == 'ch4']
            sector_df_b = df_ch4_b.groupby('original_inventory_sector')['total_emission'].sum().reset_index()
            sector_df_b['sector'] = sector_df_b['original_inventory_sector'].map(sector_map).fillna('other')

            # Bar Chart
            fig_b = px.bar(sector_df_b.sort_values(by='total_emission', ascending=False),
                           x='sector', y='total_emission',
                           title=f"{country_b_full} – CH₄ Emissions by Sector")
            st.plotly_chart(fig_b, use_container_width=True, key='fig_b_bar')

            # Pie Chart
            fig_pie_b = px.pie(sector_df_b, names='original_inventory_sector', values='total_emission',
                               title=f"{country_b_full} – CH₄ Emissions by Subsector")
            fig_pie_b.update_traces(
                textinfo='none',
                pull=[0.05]*len(sector_df_b),
                insidetextorientation='radial'
            )
            fig_pie_b.update_layout(
                uniformtext_minsize=10,
                uniformtext_mode='hide',
                legend=dict(font=dict(size=10)),
                showlegend=True
            )
            st.plotly_chart(fig_pie_b, use_container_width=True, key='fig_b_pie')

            # Data Table
            st.subheader("Data Table – Location B")
            st.dataframe(sector_df_b)

            # NEW: Add 2021–2024 Trend Chart for Location B
            st.subheader(f"{country_b_full} – CH₄ Emissions Trend (2021–2024)")
            
            combined_b_years = pd.DataFrame()
            for year_iter in AVAILABLE_YEARS:
                df_temp_b = load_country_year_data(country_b, year_iter)
                if not df_temp_b.empty:
                    df_temp_b['year'] = year_iter
                    combined_b_years = pd.concat([combined_b_years, df_temp_b], ignore_index=True)
                
            if not combined_b_years.empty:
                df_ch4_all_b = combined_b_years[combined_b_years['gas'] == 'ch4'].copy()
                df_ch4_all_b['sector'] = df_ch4_all_b['original_inventory_sector'].map(sector_map).fillna('other')
                
                sector_time_df_b = (
                    df_ch4_all_b.groupby(['year', 'sector'])['total_emission']
                    .sum()
                    .reset_index())
                
                fig_trend_b = px.bar(
                    sector_time_df_b,
                    x='year',
                    y='total_emission',
                    color='sector',
                    labels={'total_emission': 'CH₄ Emissions', 'year': 'Year'},
                    title=f"{country_b_full} CH₄ Emissions by Sector (2021–2024)")
                st.plotly_chart(fig_trend_b, use_container_width=True, key='fig_trend_b')

