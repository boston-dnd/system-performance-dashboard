### Boston CoC System Exploration App

[Open app](https://system-performance-app.herokuapp.com/)

## Purpose / Audience

This repo houses a web application that displays core metrics about the Boston Homelessness Continuum of Care that can be filtered across a variety of demographics and subpopulations.

The goal of this web app is to allow and empower the Supportive Housing Divison to explore and ask questions of the HMIS data. The app provides answers to broad system performance questions like "is the average length of stay decreasing?" but also allows users to dig deeper and uncover insights from the data, like "White veterans are older and have shorter lengths of stay than veterans of color" (no clue if that's true - just an example). The baseline measures displayed in the app are an adaption/expansion of HUD's [System Performance Measures](https://www.hudexchange.info/programs/coc/system-performance-measures/#guidance). The Supportive Housing Division collaborated to workshop and tailor these measures to be more relevant to the goals of our CoC.

## Data

The data used to power this app was pulled from the City of Boston's HMIS. R scripts cleaned, reshaped, and deidentified HMIS data into key reporting tables, which were then written to a Postgres backend.

The app operates off the following key reporting tables:

**Census**

Number of individuals in Emergency Shelter / Street Outreach on a given night, by Gender, Race, Ethnicity, Household Status, and Veteran Status

**Inflow**

Number of individuals experiencing their first-ever stay in an Emergency Shelter / Street Outreach in a given year, by Gender, Race, Ethnicity, Household Status, and Veteran Status

**Length of Stay**

Avereage length of stay in Emergency Shelter / Street Outreach in a given year, by Gender, Race, Ethnicity, Household Status, and Veteran Status

**Exits to Permanent Housing**

Number of individuals exiting to a permanent housing destination in a given year, by Gender, Race, Ethnicity, Household Status, and Veteran Status

**Returns to Shelter**

Number of individuals returning to Emergency Shelter or Street Outreach from a prior exit to a permanent housing destination in a given year, by Gender, Race, Ethnicity, Household Status, and Veteran Status

## File Structure

Write a bit about the file structure and where developers can find documentation/methodology for any calculations.

## Built With

- [Python Flask](http://flask.pocoo.org/)
- [Plotly Dash](https://dash.plot.ly/)
- Hosted on Heroku

## Usage

Outline how a developer could access and run this piece of software with their own HMIS data.

## License

This software is licensed under the MIT license ([LICENSE file](https://github.com/boston-dnd/system-performance-dashboard/blob/master/LICENSE)).