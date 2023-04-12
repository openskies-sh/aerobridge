<img src="https://i.imgur.com/88pvVBP.png" height="200">

# Introduction

Aerobridge is management server to help you with your drone flights and operations. With Aerobridge your GCS, Drones and Pilots interface with your company's digital infrastructure in a standardized fashion and be in compliance with the regulatory requirements around operating drones.

## How can Aerobridge help you?

If you are a drone manufacturer, operator or just a researcher, you can benefit by adopting Aerobridge in your operational stack:

- Store and approve missions
- Prevent unauthorized use of fleet and equipment
- Integration with Ardupilot (PX4 coming soon)
- Approve flights via one-time-password like permissions
- Integrate with UTM system of choice
## Live Demo 🚀

- You can see the frontend using the [Testflight frontend](https://aerobridge.io)
- Take a look at the backend API: [Aerobridge OpenAPI renderer](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/openskies-sh/aerobridge/master/api/aerobridge-1.0.0.resolved.yaml)

## Webinar and pilot program ✨

We work with drone manufacturers and operators to enable them to become compliant by regular onboarding run through our canary program. You can find out more about this on our regular [webinar](https://webinar.aerobridge.in).

## Get Involved

Aerobridge is fully open source and you can get involved by participating in our weekly calls and our Slack channel: [Request access here](https://forms.gle/qdUgjJHiFQn2Yuhg6). Whether you are a drone enthusiast or an expert, join our community to shape the future of drone flights. There are many benefits of participation:

- You can shape the future of this software
- Join the community of fellow professionals interested in an open flexible drone eco-system in India
- Contribute to the development of open infrastructure to support your flight operations
- Reduce the time and cost of compliance

## Technical Details

This is an open source implementation of the "Manufacturer's Management Server" to help with key signing and managing interactions with external APIs. This server can be deployed to any public and private cloud and be used to manage communication.

## Get Started / Self hosting / Debugging

Aerobridge is a Django server and is python based. To setup a local instance with a SQLLite database follow the following steps:

1. Clone the repository
2. Install dependencies, we recommend creating a virtual environment via a tool like [Anaconda](https://docs.conda.io/en/latest/)
3. Install Aerobridge specific dependencies via `pip install -r requirements.txt`
4. Copy the `.env.sample` file and create a `.env` file, you need to put in a strong password for the Django secret

Now you can use the Docker or non-Docker methods to run the installation, if you just want to test it we recommend you use Docker, use non-Docker setup for debugging / contributing.

### Docker

1. Create a Docker Container via the following command `./build_aerobridge_docker.sh`
2. Then run the containers using `docker-compose up` 
3. Finally login to the container and run the `aerobridge_entrypoint.sh` to populate with initial data.

#### Non-Docker

1. Migrate the database `python manage.py migrate` , this will create a SQLlite database called `aerobridge.sqlite3`
2. Load sample data `python manage.py loaddata fixtures/initial_data.json`
3. Launch server via `python manage.py runserver`

## Additional Dependencies

``` 
sudo apt install sqlite3          # SQLite3 Database
sudo apt install python3-pygraphviz # Graphviz for automatically generating database ER diagram
```

## Usage commands

1. Run the server locally
   ```
   DJANGO_SECRET=<YOUR_DJANGO_SECRET_KEY> python manage.py runserver
   ```
2. Create database ER diagram
   ```
   DJANGO_SECRET=<YOUR_DJANGO_SECRET_KEY> python manage.py graph_models -a -g -o test.png
   ```
3. Run automated tests
    ```
    DJANGO_SECRET=<YOUR_DJANGO_SECRET_KEY> python manage.py test
    ```

## Aerobridge Stack

Aerobridge provides the following toolset:

- **Management Server**  
  - _Assembly and supply chain management_: Develop a digital supply chain for your assembly and manufacturing operations
  - _Flight log management_: Store Bundled Logs on the server
  - _Public Key Rotation and storage_: Submission of flight plans and JWT based flight permissions
  - _Approve Missions_: Digitally sign mission approvals and verify on GCS and RFM side
  - _Maintain equipment and personnel_: Manage drone parts and people operating them in the company

- **GCS Module**
  - [QGCS Aerobridge Trusted Flight](https://github.com/openskies-sh/qgroundcontrol) A ground control station to interact with the server and the vehicle

- **Mavlink Integration**
  - [Mavlink Aerobridge](https://github.com/openskies-sh/mavlink-aerobridge) By-pass a GCS and communicate directly with the vehicle via MavLINK

- **RFM Module**
  - A customized Flight Controller Firmware and Bootloader: ([Trusted Flight RFM](https://github.com/openskies-sh/ardupilot))

## References

- This repository uses the drone registry schema from [Aircraft Registry](https://aircraftregistry.herokuapp.com) project.
- This project extensively uses logic and methods from the amazing [InvenTree](https://github.com/inventree/InvenTree) project. All code from InvenTree is Copyright (c) 2017-2022 InvenTree. For more information about their license see [their file](https://github.com/inventree/InvenTree/blob/master/LICENSE).

## LICENSE

Aerobridge is licensed under a BSL license popularized by other products such as [CockroachDB](https://www.cockroachlabs.com/docs/stable/licensing-faqs.html) and [Sentry](https://blog.sentry.io/2019/11/06/relicensing-sentry). Basically, it means the following:

- You cannot offer a version of Aerobridge as a service to third parties, if you want to do this, you will need an agreement with Openskies (the license grant restriction)
- After 24 months, the code becomes Apache-2.0 licensed (the conversion period)

In other words, if you want to host / run Aerobridge inside your company for your own operations, you are free to do so without any concerns or restrictions. If you want to offer services to third parties using a release of Aerobridge the opensource project that is less than two years old, you will need an agreement from Openskies.

## Logo source / Credit

[Hatchful](https://hatchful.shopify.com/)
