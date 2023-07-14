# PLANTFORM
#### Video Demo:  https://youtu.be/4qE27ifK4jQ
## Description
We, Josephine Dumas and Alina Vennes, collaborated on our final project Plantform, using Flask to build the website (incl. python, html, css, SQL).
Plantform is a website to manage data mapping from different stores with different data structure to one platform. Two stores are onboarded and for each store the user can set which data they want to retrieve for the different plantform fields, such as name, price, amount or picture.
Both customers have their own database with differents structure, to which we connect via an API. You can test the saved mapping by entering a plant-ID and requesting the data based on the entered mapping. If the mapping is incorrect, the data is not available and if the plant-id does not exist in the database, you get an error message. The output for the same plantID will be different per store (different stock, prices, etc.).
The site also includes an admin where registered users can manage the API address after signing up and logging in. If the API address is not available they user will also receive an error message.

## Design choices
- APIs instead of direct database connection
- Customer.html is dynamic
- Thought out all unhappy flows incl. data validation
- Hiding API configuration behind an admin (because this does not change as much and should not be easily changable, security)
- Not including adding customers as configuration as onboarding customers would include a longer process
- Dynamic error and success messages
We used Git and GitHub in combination with VSCode for collaboration and version control, working on different parts of the project on different branches, using PRs and merges to create a collaborative project.

## Requirements to run the application (as described also in `requirements.txt`)
- Flask should be downloaded and installed on computer
- SQLite3 should be downloaded and installed on computer

## Files  
Below the included files and what they do.

### Folder: static
- `Favicon.png`: the icon shown in the browser
- `Style.css`: The styling

### Folder: templates
- `Layout.html`: Layout base, include the header and menu structure. Here we also included bootstrap and imported fonts.
- `Index.html`: The homepage, giving a short introduction to the page and the link to both customer sites.
- `Customer.html`: The mapping can be filled in. To do so, this template contains a form to make a post-request to save the specified mapping fields. The chosen customer is filled in dynamically so we don't have to copy and paste the same code for each new customer, retrieving the friendly customer name, the set API address and set mapping from the database to fill in. When entering a plant id to save and test the mapping, a post request is done to retrieve the data, rendering the output via the mapper.html.
- `Mapper.html`: This template shows the output of the different data fields for a specific plant-id, depending on the mapping that is set on the customer.html, which customer you have selected before and which plantID was entered. The plantid, and the output of the different fields depending on the mapping specified in the customer.html are passed to this page as parameters.
- `Admin.html`: After log-in you can set the API URLs to be requested for each customer on this page. If saving correctly, a success message is shown when that message is passed to this template as a parameter. The page also shows for which user you are logged in, retrieving this from the current session. The configured URLs are retrieved from the database in the app.py and passed as parameters to this html. The template contains a form for a post-request to save API URLs.
- `Admin-login.html`: On this page you can log in for a previously created user. A success message is shown when that message is passed to this template as a parameter. The template contains a form for a post-request to log-in. 
- `Admin-register.html`: On this page you can create a new user. A success message is shown when that message is passed to this template as a parameter. The template contains a form to make a post request for registering as a user.
- `Apology.html`: This page handles error messages, using the error code and error message that is handed to the page as parameters to show a specific error meme.

### Database and source data files
- `database.db`: The database containing the registered users and the saved mapping for customers.
- `data_het_oosten.txt`: The source for the data behind the API for customer _"Het Oosten"_, such as stock and price for different plants.
- `data_intratuin`: The source for the data behind the API for customer _"Intratuin"_, such as stock and price for different plants.
- `schema.sql`: Describes the database structure and used to initially build the tables in the database.

### `app.py`
`app.py` contains the navigating routes of the user through the web application. It contains general application configuration and the routes for `/`, `api/<customer>`, `/<customer>`, `/admin`, `/admin-login`, `/register` and `/logout` and general application configuration.

#### Application configuration
- Functions from Flask are imported to enable a flask webapplication with templates, redirects and sessions
   - The Flask application is configured using `Flask(__name__)`
   - Sessions are configured using filesystem
- Functions from `helper.py` are imported
- `sqlite3` is imported to enable database mutations
- `json` is imported to enable API simulation
  
#### Route `/`
This route is designed to open the homepage
- The `index.html` template is rendered when this route is triggered using the `render_template` function from the Flask library.

#### Route `/<customer>`
This dynamic route is designed for loading the specific customer pages. `GET` requests are supported. This route is loaded for a `GET` request after an user clicks one of the buttons on the homepage (`index.html`) or by using the (burger) menu. 
- The `customer` parameter is defined by the `<customer>` in the URL
- All customer data from `database.db` is queried using the function `query_db` from `helper.py`
- A match between one of the customer suffices (`suffix` in `customers` table) in the customer data and the `customer` parameter is searched for.
  - If a match is found, `customer.html` is rendered. Customer name (`customerFriendly`), real customer API (`customerApi`), configured customer API (`urlConfig`), and all fields and tables for name, amount, picture and price (`[xxx]field` and `[xxx]table`) are retrieved from the customer data and passed as parameters together with the `customer` parameter.
  - If no match is found, `apology.html` from `helper.py` is rendered with error message _"Customer not available"_

#### Route `/api/<customerApi>`
This dynamic route is designed for simulating the specific customer's API. Only `POST` requests are supported. This route is loaded for a `POST` request after an user submits the mapping form on the customer page clicking the button _"Save and view mapping"_.
- The `customerApi` parameter is defined by the `<customerApi>` in the URL.
- If the route is loaded via a "GET" requests, `apology.html` is rendered.
- After the route is loaded via the "POST" request coming from `customer.html`, the plant ID filled in the form is stored in paramater `plantid` and tables and fields for name, amount, picture and price are stored in parameters `[xxx]Table` and `[xxx]Field`.
- All customer data from `database.db` is queried using the function `query_db`.
- A match between one of the customer configured API URLs (`urlconfig` in `customers` table) in the customer data and the `customerApi` parameter is searched for.
  - If a match is found,
     - The source parameter, which represents the name of the `.txt` file containing the source data of that customer,  and the customer parameter, being the customer suffix, are retrieved from the customer data (respectively `source` and `suffix` in `customers` table)
     - A connection with the database is made and the tables and fields for name, amount, price and picture (`[xxx]table` and `[xxx]field` in `custom ers` table) are updated using `UPDATE` SQL statements. These statements are executed using `conn.execute` from the `sqlite3` library.
     - The `source` file is opened using the `open` function from Python library. If the file can not be opened, `apology.html` is rendered.
     - From the `source` file, plant data is loaded using `f.read` from Python library and converted to json format using `json.loads` from the `json` library into the parameter 'records'.
     - Using a for-loop a match with the parameter `plant-id` is searched for in `records`.
       - If found, name, amount, price and picture information from the plant data is selected from the `record` using the fields and tables as saved in the mapping form (`[xxx]Table` and `[xxx]Field`) and stored in parameters `name`, `amount`, `price` and `picture`. If the specific data is not available in `record`, the specific parameter is defined as "Not available".
          - `mapper.html` is rendered with `plantid`, `name`, `price`, `picture`, `amount`, `customer` and `customerFriendly` as parsed paramaters to show the user the results of the configured mapping for the specified plant-id.
       - If the plant-id is not found, `apology.html` is rendered with error message _"Plant-id not found"_
  - If no API match is found, `apology.html` is rendered with error message _"This API cannot be found"_

#### Route `/admin`
This route is designed to allow admin users (for who authentication is required) to manage the API URLs of the two customers, _Intratuin_ and _Het Oosten_ in one page. Both `GET` as `POST` requests are supported. This route is loaded for a `GET` request after an user navigated to _Customer admin_ in the (burger) menu or as redirect after a succesfull log-in on `admin-login.html`. This route is loaded for a `POST` request after an user submits an API URL configuration form on `admin.html` succesfully.
- `login_required` from `helper.py` checks if an active session exists of an authenticated user. If not, a redirect to route `/admin-login` is triggered.
- If the route is loaded via a `GET` request
  - All customer data from `customer.db` is queried using the function `query_db`.
  - The configured API URLs for both the customer _Intratuin_ as _Het Oosten_ are retrieved from the `urlconfig` fields from `customers` table in the database. These configured API URLs are stored in parameters `urlConfigIntratuin` and `urlConfigHetOosten`.
  - Template `admin.html` is rendered. Parameters `urlConfigIntratuin` and `urlConfigHetOosten` are parsed so that they can be visualized as currenct configuration to the user. The `username` parameter is defined using the `session` and is parsed as well to show the user who is logged in at the moment.
- If the route is loaded via a `POST` request after the API URl configuration form is submitted within `admin.html`,
  - Parameters `urlConfigIntratuin` and `urlConfigHetOosten` are filled with form results for `url-config-intratuin` and `url-config-hetoosten` respectively.
  - A connection is made to the database and database fields `urlconfig` for both customers are updated.
  - All customer data from `customer.db` is queried using the function `query_db`.
  - The configured API URLs are checked by searching for a match between the configured API URL (`urlconfig`) and real API URL (`apiurl`) per customer in the `customers` table.
    - If a mismatch is found for one of the customers, `apology.html` is rendered with error message _This Api endpoint is not available. Make sure to change configuration_.
    - If both match, `admin.html` is rendered with parsed paramaters `urlConfigIntratuin`, `urlConfigHetOosten`, `username` and `message`, being _"API URL(s) succesfully saved!"_ (to show the user a confirmation message).

#### Route `/register`
This route is designed for user registration. The route supports both `GET` as `POST` requests.
- If the route is loaded via a `POST` request after a register form submission on `admin-register.html`
  - Form inputs username and both passwords are stored in parameters `username`, `password` and `password2`.
  - Password validation is carried out by comparing `password` and `password2`. If valid,
    - the username and password are inserted in database using `insertUser` from `helper.py`. Parameter `users` is defined by retrieving all user data from database using `retrieveUsers` from `helper.py`.
    - `admin-register.html` is rendered with parsed parameters `users` and `message`, being _"Registration was succesfull"_ to show as confirmation message
   - If both passwords don't match, `apology.html` is rendered with message _"Passwords didn't match"_

#### Route `/logout`
This route is designed to perform a log-out. Only `GET` requests are supported, loaded via clicking the button _Log-out_ on `admin.html`
- Session is cleared using the `session.clear()` function of Flask library and a redirect to `/admin-login` is triggered.

#### Teardown
If application is closed, the connection to the database is also closed using `getattr` from Python library and `db.close()` function from sqlite3 library.

### `helper.py`
`helper.py` contains helper functions used within `app.py`. The general variable `DATABASE` is defined as being `database.db`.

#### `get_db`
Function to connect to a database. No inputs required.

#### `query_db`
Function to execute queries on the database and store the results in an array. Inputs are a query (`query`), arguments to fill in the query (`args`). Output is an array of the results (`rv[0]`)

#### `init_db`
Function to perform database initialization. As we are only working with a local database, the database needs to be initialized during first use. `schema.sql` is used as query source.

#### `login_required`
Function to check if a session with an authenticated user is active.

#### `apology`
Function to create an error image and render `apology.html` with this error image. Inputs are an error message (`message`) and an error code (`code`). 

#### `insertUser`
Function to insert the `username` and `password` of an user in the `users` table of the database. Inputs are `username` and `password`. 

#### `retrieveUsers`
Function to retrieve all users from the `users` table of the database.
