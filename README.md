# `app.py`
`app.py` contains the navigating routes of the user through the web application. It contains general application configuration and the routes for `/`, `api/<customer>`, `/<customer>`, `/admin`, `/admin-login`, `/register` and `/logout` and general application configuration.

## Application configuration
- Functions from Flask are imported to enable a flask webapplication with templates, redirects and sessions
   - The Flask application is configured using `Flask(__name__)`
   - Sessions are configured using filesystem
- Functions from `helper.py` are imported
- `sqlite3` is imported to enable database mutations
- `json` is imported to enable API simulation

## Route `/`
This route is designed to open the homepage
- The `index.html` template is rendered when this route is triggered using the `render_template` function from the Flask library.

## Route `/<customer>`
This dynamic route is designed for loading the specific customer pages. `GET` requests are supported. This route is loaded for a `GET` request after an user clicks one of the buttons on the homepage (`index.html`) or by using the (burger) menu. 
- The `customer` parameter is defined by the `<customer>` in the URL
- All customer data from `database.db` is queried using the function `query_db` from `helper.py`
- A match between one of the customer suffices (`suffix` in `customers` table) in the customer data and the `customer` parameter is searched for.
  - If a match is found, `customer.html` is rendered. Customer name (`customerFriendly`), real customer API (`customerApi`), configured customer API (`urlConfig`), and all fields and tables for name, amount, picture and price (`[xxx]field` and `[xxx]table`) are retrieved from the customer data and passed as parameters together with the `customer` parameter.
  - If no match is found, `apology.html` from `helper.py` is rendered with error message _"Customer not available"_

## Route `/api/<customerApi>`
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

## Route `/admin`
This route is designed for allowing admin users (for who authentication is required) to change the API URLs of the different customers.
- Using `login_required` from `helper.py` checks if an active session exists of an authenticated user. If not, a redirect to route `/admin-login` is triggered.
- 
