![Work in Progress](https://www.psychologiepraktijkheijnen.nl/wp-content/uploads/2017/04/work-in-progress.png)


# NajdiStan.mk - rework to Django v.3

This is a rework of the original Najdistan.mk application that was built initially with Flask.
The application can be found at: [http://najdistan-mk.herokuapp.com](http://najdistan-mk.herokuapp.com]). It is hosted on Heroku's free tier and the initial loading (landing) of the website can be slow until their dyno's start up. Subsequent requests will function normally.

The codename of this project is "NajdistanDjango3.0". When it is ready for production it can be branded to anything. This is WIP (Work in Progress). Currently the backend is mostly being developed. There is still no style, just some basic bootstrapping.

## Core functionalities:
* User profiles (Register, Login, Reset Password, Profile page)
* Listing management (Create/Retrieve/Update/Delete)
* Search page (Display data based on your filters)
* Search Profiles (Create so-called "SP" to get informed about new listings matching your criteria every X TIME)
* Get notified (email/sms) when someone starts a private thread / sends a public comment.
* Compare listings
* Admin dashboard (with statistics, charts etc)
* ...

### Things done so far:
* Database set-up and management (Postgres for production, SQlite for development)
* Production-ready environment with secrets hidden
* Production ready storage for storing listings images and user profile images (AWS S3 storage)
* A-to-Z registration and user management system
  * User 2-step registration (e-mail confirm)
  * User login, logout and reset forgotten password
  * User Profile and Editing profile
* Listing-related forms and logic
  * Create/Retrieve/Update/Delete listing (permission based)
  * Listing display: Title, Description, Price, (listing info such us floor, basemenet, heating etc.), Type of listing, Images, Location, Contact, Public comments and much more info
* Admin dashboard
* Data fixtures
* ...

### Things in progress:
* API development
* Listing upload handling images
* Search filter criteria based
* Search profile(s) - (Get informed about listings matching your criteria every X TIME [selectable]
* Listing reports. Comments reports
* Favorite a listing. (If logged-in put it on your profile. If not put it in the user browser localStorage)
* User comments / threads
* ...

### Things to be done:
* STYLING !
* Social authentication
* Premium user membership (lots of ideas already for Premium membership)
* Listing message thread (1-to-1 private message system)
* Listing Compare views
* Unit tests
* ...


## Local development and playground

  1. Clone the repo locally (`git clone git@github.com:DonExo/NajdistanDjango3.0.git`)
  2. Create virtual environment with (at least) python3.7 as interpreter (`mkvirtualenv --python=`which python3.7\` najdistanvenv) - for this you need to have virtualenvwrapper activated and python3.7 on your machine. Activate the venv if it is not (`workon najdistanvenv`)
  3. CD into newly cloned project. (`cd Najdistandjango3.0`)
  4. Install the requirements (`pip install -r requirements.txt`)
  5. Rename the .env.example file to just .env (`mv .env.example .env`)
  6. Run migrations (`./manage.py migrate`)
  7. Optional: Load fixtures (`./manage.py loaddata fixtures.py`) (Currently outdated!)
  8. Optional: Create super uesr for easy admin access (`./manage.py createsuperuser`)
  9. Run local server (`./manage.py runserver`)
  10. Play around!
  
*NOTE:*

The default settings.py have been changed with a more robust solution: local.py and production.py settings. This project now loads `settings/local.py` by default. 

If for whatever reason you'd like to run it with production settings - start your server with `./manage.py runserver --settings=najdistandjango30.settings.production`. Any `./manage.py ...` command should have the new settings added.

Also, do not forget to add the proper settings values in your local `.env` file (i.e. SMTP settings, DB settings, AWS...)
