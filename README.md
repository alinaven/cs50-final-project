# PLANTFORM
#### Video Demo:  https://youtu.be/4qE27ifK4jQ
#### Description: 

We, Josephine Dumas and Alina Vennes, collaborated on our final project Plantform, using Flask to build the website (incl. python, html, css, SQL).

Plantform is a website to manage data mapping from different stores with different data structure to one platform. Two stores are onboarded and for each store the user can set which data they want to retrieve for the different plantform fields, such as name, price, amount or picture. 

Both customers have their own database with differents structure, to which we connect via an API. You can test the saved mapping by entering a plant-ID and requesting the data based on the entered mapping. If the mapping is incorrect, the data is not available and if the plant-id does not exist in the database, you get an error message. The output for the same plantID will be different per store (different stock, prices, etc.). 

The site also includes an admin where registered users can manage the API address after signing up and logging in. If the API address is not available they user will also receive an error message.

Below the included files and what they do:
Folder: static
    Favicon.png: the icon shown in the browser
    Style.css: The styling
Folder: templates
    Layout.html: Layout base, include the header and menu structure. Here we also included bootstrap and imported fonts.
    Index.html: The homepage, giving a short introduction to the page and the link to both customer sites.
    Customer.html: The mapping can be filled in. The chosen customer is filled in dynamically so we don't have to copy and paste the same code for each new customer. When entering a plant id to save and test the mapping, a post request is done to retrieve the data, rendering the output via the mapper.html.
    Mapper.html:
    Admin.html
    Admin-login.html
    Admin-register.html
    Admin.html
.gitattributes
.gitgnore
database.db
database.sqlite
data_het_oosten.txt
data_intratuin
requirements.txt
schema.sql


Design choices (include above)
- APIs instead of direct database connection
- Customer.html is dynamic
- Thought out all unhappy flows incl. data validation
- Hiding API configuration behind an admin (because this does not change as much and should not be easily changable, security)
- Not including adding customers as configuration as onboarding customers would include a longer process
- Dynamic error and success messages

We collaborated using GitHub.

Requirements invullen

