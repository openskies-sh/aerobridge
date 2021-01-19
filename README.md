<img src="https://i.imgur.com/88pvVBP.png" height="200">

# Introduction

The [Directorate General of Civil Aviation (DGCA)](https://dgca.gov.in/digigov-portal/) in India has unveiled a policy of "No permission - No takeoff" for drone flights. This means that public and private companies intending to fly drones in India need to interface with DGCA's infrastructure for flight permissions and other authorizations. These APIs are called India's [Digital Sky](https://digitalsky.dgca.gov.in/) eco-system. Aerobridge is a server that helps you interface with the APIs in a standardized fashion and be in compliance with the regulatory requirements around operating drones.

## How can Aerobridge help you?

If you are a drone manufacturer, operator or just a researcher, you can benefit by adopting Aerobridge in your operational stack:

- Standard way to communicate with Digital Sky APIs
- Integration with PX4 / ArduControl
- Manage permissions and flight logs
- RFM integration
- Easily manage compliance with NPNT

## Webinar and pilot program ✨

We work with drone manufacturers to enable them to become compliant with NPNT by regular onboarding run through our canary program. You can find out more about this on our regular [webinar](http://webinar.aerobridge.in).

## Get Involved

Aerobridge is fully open source and you can get involved by participating in our weekly calls (details shortly) and our Slack channel: [Request access here](https://forms.gle/qdUgjJHiFQn2Yuhg6). Weather you are a drone enthusiast or a expert, join our community to shape the future of drone flights in India. There are many benefits of participation:

- You can shape the future of this software
- Join the community of fellow professionals interested in a open flexible drone eco-system in India
- Contribute to the development of open infrastructure to support your flight operations
- Reduce the time and cost of compliance

## Technical Details

This is a open source implementation of the "Manufacturer's Management Server" to help with key signing and managing interactions with India's [Digital Sky](https://digitalsky.dgca.gov.in/) API infrastructure. This server can be deployed to any public and private cloud and be used to manage communication with DGCA's Digital Sky Infrastructure and manage NPNT permissions. For more technical introduction, see this [presentation](https://docs.google.com/presentation/d/1cZrNwNrLtLIj5eKEGql2HN-G1gZFbbGhGbiTB1i16So/edit?usp=sharing).

## Aerobridge Stack

As of January 2021, Aerobridge provides the following toolset:

- **Management Server**
  - __Drone Registration__: Submit details of a drone and get a UIN number 
  - __Flight log management__: Upload Bundled Logs to the DGCA API and store logs on the server
  - __Permission Artefact management__: Submission of flight plans and fetching permission artefacts

- **GCS Module**
  - [Mavlink Aerobridge](https://github.com/openskies-sh/mavlink-aerobridge) Integration with RFM

- **RFM Module**
  - A customized Flight Controller coming soon

## References

- This repository uses the drone registry schema from [Aircraft Registry](https://aircraftregistry.herokuapp.com) project.
- Further details regarding NPNT can be found in the latest [RPAS Guidance Manual](https://public-prd-dgca.s3.ap-south-1.amazonaws.com/InventoryList/headerblock/drones/DGCA%20RPAS%20Guidance%20Manual.pdf).

## Test drive

- You can see the API using the API explorer: [Aerobridge OpenAPI renderer](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/openskies-sh/aerobridge/master/api/aerobridge-1.0.0.resolved.yaml)
- To load the database with dummy data for your test-drive you can run the following Python / Django command: `python manage.py loaddata registry/defaultregistrydata.json`, this will populate the database with sample drone operator data.

## LICENCE

Aerobrigde is licenced as a BSL licence popularized by other products such as [CockroachDB](https://www.cockroachlabs.com/docs/stable/licensing-faqs.html) and [Sentry](https://blog.sentry.io/2019/11/06/relicensing-sentry). Basically it means the following: 
- You cannot offer a commercial version of Aerobridge's service to third parties, if you want to do this, you will need an agreement with Openskies (the license grant restriction)
- After 36 months, the code becomes Apache-2.0 licensed (the conversion period)

If you want to host / run Aerobridge inside your company for your own assets and compliance, you are free to do so without any restrictions. This will ensure that we are protected from our work being used in an anti-competitive fashion. 


## Logo source / Credit

[Hatchful](https://hatchful.shopify.com/)
