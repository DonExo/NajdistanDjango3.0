![Work in Progress](https://www.psychologiepraktijkheijnen.nl/wp-content/uploads/2017/04/work-in-progress.png)


# Najdistan v3.0 - rework to Django

This is a rework of the original Najdistan.mk application that was built initially with Flask.

It is intended to be used as a Listing service where people can register to sell/buy/rent a home. Something similar to Funda and Pararius.

The project can be found at: https://crelayo.shop (the domain name has no meaning at all) 

The codename of this project is "Najdistan v3.0". When it is ready for production it can be branded to anything. This is Work in Progress (WIP).

## Core functionalities:
* User profiles (Register, Login, Reset Password, Profile page)
* Listing management (Create/Retrieve/Update/Delete)
* Listings compare, bookmark, highlight
* Search functionality (display data based on your filters)
* Search Profiles (create so-called "SP" to get you informed about new listings matching your criteria every X TIME)
* Get notified (by email/sms) when someone starts a private thread / sends a public comment.
* Share listing via social media
* 'Premium' user that has extra features available (i.e. highlighted Listings, extra Search Profiles, more options in SP and more...)
* Admin dashboard (with statistics, charts etc)
* ...

### Things done so far:
* Created production-ready environment by following best practices
* Database architecture and set-up (Postgres for production, SQlite for development)
* Production ready storage for storing listing images and user profile images (AWS S3 for production, local for development)
* A-to-Z registration and user management system
  * User 2-step registration (e-mail confirmation)
  * User login, logout and reset forgotten password
  * User profile and editing profile
* Listing-management, and related logic
  * Create/Retrieve/Update/Delete listing (permission based)
  * Listing display: Title, Description, Price, (listing info such us floor, basemenet, heating etc.), Type of listing, Images, Location, Contact, Public comments and much more info
* Safe listing image uploads
* Search filter to narrow down your results
* Search profiles - (Get informed about listings matching your criteria every X TIME [selectable]
* Cron jobs for the Search Profiles

* Admin dashboard
* Data fixtures
* ...

### Things in progress:
* STYLING ! (Sorry if you see inconsistencies or wrongly-placed object)
* Premium user membership (lots of ideas already for Premium membership)
* Listing Compare views
* Listing reports. Comments reports
* Save a listing.
* User comments / threads
* ...

### Things to be done:
* API development
* Social authentication
* Listing message thread (1-to-1 private message system)
* SMS verification
* Show listings on map
* Translations
* Unit tests
* ...


## Local development and playground (This guide will work on Unix-alike systems [Linux, MacOS])

  1. Clone the repo locally (`git clone https://github.com/DonExo/NajdistanDjango3.0.git` or use SSH)
  2. Create virtual environment with (at least) python3.7 as interpreter (`mkvirtualenv --python=`which python3.7\` najdistanvenv) - for this you need to have virtualenvwrapper activated and python3.7 on your machine. Activate the venv if it is not (`workon najdistanvenv`)
  3. CD into newly cloned project. (`cd Najdistandjango3.0`). For latest development check other branches (frontend, development..)
  4. Install the requirements (`pip install -r requirements.txt`)
  5. Run migrations (`./manage.py migrate`)
  6. Optional: Load dummy fixtures (`./manage.py loaddata fixtures.py`)
  7. Optional: Create super user for easy admin access (`./manage.py createsuperuser`)
  8. Run local server (`./manage.py runserver`)
  9. Optioanl: If you want to use the production-ready server:
      * rename the `.env.example` file to `.env`
      * add your personal keys in the `.env` file (i.e your Postgre DB credentials, e-mail server credentials, AWS bucket etc)
      * run the server with `./manage.py runserver --settings=najdistandjango30.settings.production`
  10. Open 'http://127.0.0.1:8000' in your browser and have fun!
  
*NOTE:*

The default settings.py have been changed with a more robust solution: `local.py` and `production.py` settings. This project now loads `settings/local.py` by default. 

If for whatever reason you'd like to run it with production settings - start your server with `./manage.py runserver --settings=najdistandjango30.settings.production`. Any `./manage.py ...` command should have the new settings added.

