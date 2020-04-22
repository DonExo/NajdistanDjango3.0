![Work in Progress](https://www.psychologiepraktijkheijnen.nl/wp-content/uploads/2017/04/work-in-progress.png)


# Najdistan v3.0 - rework to Django

This is a rework of the original Najdistan.mk application that was built initially with Flask.

It is intended to be used as a Listing service where people can register to sell/buy/rent a home. Something similar to Funda and Pararius.

The codename of this project is "Najdistan v3.0". When it is ready for production it can be branded to anything. This is WIP (Work in Progress). Currently the backend is mostly being developed. There is some very, very basic styling!

## Core functionalities:
* User profiles (Register, Login, Reset Password, Profile page)
* Listing management (reate/Retrieve/Update/Delete)
* Search functionality (display data based on your filters)
* Search Profiles (create so-called "SP" to get informed about new listings matching your criteria every X TIME)
* Get notified (by email/sms) when someone starts a private thread / sends a public comment.
* Compare listings
* Save listing for viewing later
* Share listing via social media
* 'Premium' user that has extra features available
* Admin dashboard (with statistics, charts etc)
* ...

### Things done so far:
* Created production-ready environment by following best practices
* Database architecture and set-up (Postgres for production, SQlite for development)
* Production ready storage for storing listing images and user profile images (AWS S3 for production, local for development)
* A-to-Z registration and user management system
  * User 2-step registration (e-mail confirm)
  * User login, logout and reset forgotten password
  * User profile and editing profile
* Listing-management, and related logic
  * Create/Retrieve/Update/Delete listing (permission based)
  * Listing display: Title, Description, Price, (listing info such us floor, basemenet, heating etc.), Type of listing, Images, Location, Contact, Public comments and much more info
* Safe listing image uploads
* Search filter
* Search profile(s) - (Get informed about listings matching your criteria every X TIME [selectable]
* Admin dashboard
* Data fixtures
* ...

### Things in progress:
* API development
* Listing reports. Comments reports
* Save a listing.
* User comments / threads
* ...

### Things to be done:
* STYLING !
* Social authentication
* Premium user membership (lots of ideas already for Premium membership)
* Listing message thread (1-to-1 private message system)
* Listing Compare views
* SMS verification
* Show listings on map
* Cron jobs for the Search Profiles
* Translations
* Unit tests
* ...


## Local development and playground

  1. Clone the repo locally (`git clone git@github.com:DonExo/NajdistanDjango3.0.git`)
  2. Create virtual environment with (at least) python3.7 as interpreter (`mkvirtualenv --python=`which python3.7\` najdistanvenv) - for this you need to have virtualenvwrapper activated and python3.7 on your machine. Activate the venv if it is not (`workon najdistanvenv`)
  3. CD into newly cloned project. (`cd Najdistandjango3.0`)
  4. Install the requirements (`pip install -r requirements.txt`)
  5. Rename the .env.example file to just .env (`mv .env.example .env`)
  6. Run migrations (`./manage.py migrate`)
  7. Optional: Load fixtures (`./manage.py loaddata fixtures.py`)
  8. Optional: Create super user for easy admin access (`./manage.py createsuperuser`)
  9. Run local server (`./manage.py runserver`)
  10. Play around!
  
*NOTE:*

The default settings.py have been changed with a more robust solution: local.py and production.py settings. This project now loads `settings/local.py` by default. 

If for whatever reason you'd like to run it with production settings - start your server with `./manage.py runserver --settings=najdistandjango30.settings.production`. Any `./manage.py ...` command should have the new settings added.

Also, do not forget to add the proper settings values in your local `.env` file (i.e. SMTP settings, DB settings, AWS...)
