# AskOptum
![Project Status](https://img.shields.io/badge/Project%20Status-In%20Progress-green)

**Content:** [Overview](#overview), [Frontend](#start), [Frontend Docker](#docker), [Backend](#back), [References](#ref)

<a name="overview"></a>
### Overview

The goal of **AskOptum** is to be the location where initially UHG employees will be able to query and find UHG information that is specific to them. Further, this solution will be extended to members and providers.

**How it will work?**

Instead of looking through benefit plans, a member could simply ask for details with natural language. For example, a member might ask an open question like "How do I protect my family from COVID-19" and **AskOptum** will return several types of information to the member.

* We may show COVID clinics that are near the member and providers that are in their plan.
  * Complete with correct co-pay info / remaining deductible and other costs.
* If records are available we may also show other member information that is RELEVANT to the question asked.
  * If the member has COVID comorbidities we might highlight those and display general information related to those specific diseases and how they relate to COVID.
* And, finally, **AskOptum** will show highly rated related information about COVID but that may not be targeted to the member, things like news articles or other informational material

This application will be hosted in the public cloud due to its need to consume several NLP / ML Azure services.

### Deploy AskOptum to Azure For Development

Execute:

```commandline
bash ./deploy.sh
```

After this script completes you will have an askoptum instance specific to you in dev available at <your-ms-id>.ask.optum.com, for example mgrose.ask.optum.ai. 

> NOTE: The first-time deployment takes around ~30-40 minutes for azure to provision new certificates from digicert

See [deploy.sh](./deploy.sh) comments for behind the scenes details.

<a name="start"></a>
### Frontend 

**Pre-Requisites**

* Node.js - to install, request it on the AppStore [(here)](https://appstore.uhc.com/).

**Running the App**

Clone this repo:
```
git clone https://github.optum.com/ATC/AskOptum.git
```

Get to the *AskOptum* folder:
```
cd AskOptum/frontend
```

Install dependencies:
```
npm install
```

Start the app:
```
npm start
```

Open http://localhost:3000 to view it in the browser.

<a name="docker"></a>
#### Using Docker

Following steps to build and run the docker container.

Build the docker container:

`docker build -t askoptum .`

Run the docker container:

`docker run --name=askoptum --rm -p 5000:5000 askoptum`

Open in your browser:

`http://0.0.0.0:5000/`

To get access to the docker container:

`docker run --name=askoptum --rm -p 5000:5000 -it askoptum bash`

<a name="back"></a>
### Backend
- [Backend](backend/README.md)
 
<a name="Infra"></a>
### Infra
- [Infra](infra/README.md)
 

<a name="ref"></a>
### References

* [UIToolkit](https://uitoolkit.optum.com/)
* [DemoHarness Style Guide](https://github.optum.com/pages/ATC/DemoHarness/#/Introduction)

### Acknowledgment

Based on the [DemoHarness](https://github.optum.com/ATC/DemoHarness).

