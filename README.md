<img src="https://i.imgur.com/88pvVBP.png" height="200">

# Introduction

The [Directorate General of Civil Aviation (DGCA)](https://dgca.gov.in/digigov-portal/) in India has unveiled a policy of "No permission - No takeoff" for drone flights. This means that public and private companies intending to fly drones in India need to interface with DGCA's infrastructure for flight permissions and other authorizations. These APIs are called India's [Digital Sky](https://digitalsky.dgca.gov.in/) eco-system. Aerobridge is a server that helps you interface with the APIs in a standardized fashion and be in compliance with the regulatory requirements around operating drones.

## How can Aerobridge help you?

If you are a drone manufacturer, operator or just a researcher, you can benefit by adopting Aerobridge in your operational stack:

- Standard way to communicate with Digital Sky APIs
- Integration with PX4 / Ardupilot
- Manage permission artefacts and flight logs
- RFM integration
- Easily manage compliance with NPNT

## Webinar and pilot program ✨

We work with drone manufacturers to enable them to become compliant with NPNT by regular onboarding run through our canary program. You can find out more about this on our regular [webinar](https://webinar.aerobridge.in).

## Get Involved

Aerobridge is fully open source and you can get involved by participating in our weekly calls (details shortly) and our Slack channel: [Request access here](https://forms.gle/qdUgjJHiFQn2Yuhg6). Whether you are a drone enthusiast or an expert, join our community to shape the future of drone flights in India. There are many benefits of participation:

- You can shape the future of this software
- Join the community of fellow professionals interested in an open flexible drone eco-system in India
- Contribute to the development of open infrastructure to support your flight operations
- Reduce the time and cost of compliance

## Technical Details

This is an open source implementation of the "Manufacturer's Management Server" to help with key signing and managing interactions with India's [Digital Sky](https://digitalsky.dgca.gov.in/) API infrastructure. This server can be deployed to any public and private cloud and be used to manage communication with DGCA's Digital Sky Infrastructure and manage NPNT permissions. For a more technical introduction, see this [presentation](https://docs.google.com/presentation/d/1cZrNwNrLtLIj5eKEGql2HN-G1gZFbbGhGbiTB1i16So/edit?usp=sharing).

## Dependencies
> sudo apt install libpq-dev

## Aerobridge Stack

As of January 2021, Aerobridge provides the following toolset:

- **Management Server**
  - __Drone Registration__: Submit details of a drone and get a UIN number 
  - __Flight log management__: Upload Bundled Logs to the DGCA API and store logs on the server
  - __Permission Artefact management__: Submission of flight plans and fetching permission artefacts

- **GCS Module**
  - [Mavlink Aerobridge](https://github.com/openskies-sh/mavlink-aerobridge) Integration with RFM

- **RFM Module**
  - A customized Flight Controller Firmware and Bootloader (coming soon)

## References

- This repository uses the drone registry schema from [Aircraft Registry](https://aircraftregistry.herokuapp.com) project.
- Further details regarding NPNT can be found in the latest [RPAS Guidance Manual](https://public-prd-dgca.s3.ap-south-1.amazonaws.com/InventoryList/headerblock/drones/DGCA%20RPAS%20Guidance%20Manual.pdf).

## Test drive

- You can see the frontend using the [Testflight frontend](https://aerobridgetestflight.herokuapp.com/launchpad)
- Take a look at the backend API: [Aerobridge OpenAPI renderer](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/openskies-sh/aerobridge/master/api/aerobridge-1.0.0.resolved.yaml)

## LICENSE

Aerobridge is licensed under a BSL license popularized by other products such as [CockroachDB](https://www.cockroachlabs.com/docs/stable/licensing-faqs.html) and [Sentry](https://blog.sentry.io/2019/11/06/relicensing-sentry). Basically, it means the following:

- You cannot offer a version of Aerobridge as a service to third parties, if you want to do this, you will need an agreement with Openskies (the license grant restriction)
- After 24 months, the code becomes Apache-2.0 licensed (the conversion period)

In other words, if you want to host / run Aerobridge inside your company for your own operations, you are free to do so without any concerns or restrictions. If you want to offer services to third parties using a release of Aerobridge the opensource project that is less than two years old, you will need an agreement from Openskies.

## Logo source / Credit

[Hatchful](https://hatchful.shopify.com/)
