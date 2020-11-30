<img src="https://i.imgur.com/88pvVBP.png" height="200">

# About

This is a open source implementation of the "Manufacturer's Management Server" to help with key signing and managing interactions with India's [Digital Sky](https://digitalsky.dgca.gov.in/) API infrastructure. This server can be deployed to any public and private cloud and be used to manage communication with DGCA's Digital Sky Infrastructure and manage NPNT permissions.

## Why Aerobridge?

- India's DGCA have released a set of APIs as part of the DigitalSky Initiative, these APIs manage permissions and interactions as a part of "No permission No take-off" policy. However, there is no standard way to interact with these APIs, Aerobridge server aims to standardize interactions by developing a open source layer to interact with DigitalSky.
- We hope to enable broad compliance with NPNT and easy on-boarding into the DigitalSky eco-system by open sourcing this important bridge.
- Finally we hope to develop a community within the Indian UTM stakeholders and standardize different unique aspects of the Indian UTM eco-system.

## Features

As of November 2020, once you connect / point your GCS software to an instance and can do the following using Aerobridge API:

- __Flight log management__: Upload Bundled Logs to the DGCA API and store logs on the server
- __Permission Artefact management__: Submission of flight plans and fetching permission artefacts

## References

This repository uses the drone registry schema from [Aircraft Registry](https://aircraftregistry.herokuapp.com) project.

## Test drive

- You can see the API using the API explorer: Link TBC
- To load the database with dummy data for your test-drive you can run the following Python / Django command: `python manage.py loaddata registry/defaultregistrydata.json`, this will populate the database with sample drone operator data. 

## Logo source / Credit

[Hatchful](https://hatchful.shopify.com/)