## Description
This homework will have you develop a web store application.  **This is an individual** assignment; you may discuss general Python/SQL techniques with other students, but all code that you write must be your own! You are expected to implement the following "from scratch", i.e., you may use the basic Flask libraries, templating abilities, etc, but you may not use 3rd party libraries to provide significant portions of functionality such as user logins.

**Deadline:** Monday 3/8/22, 11:59PM

> This is an **INDIVIDUAL** project. You may not share code with other students!


# WRITE YOUR NAME HERE

## Application Requirements
The website should be able to display products being sold in several categories. A user visiting your web store can search for products (i.e., search for a specific item name and display that item) or display all items in a certain category. The website should display the available quantity and price for each product.

Only a logged in user can add products to a shopping cart and then checkout to complete a purchase and buy the products. To "buy" a product means to reduce the quantity from that product with the quantity that was "bought" (i.e. your database should be updated to reflect the reduction in quantity of items after checkout, not when added to the cart). 

A logged in user's shopping cart can be viewed, edited, checked out or deleted. A logged in user can also see her order history which should include the list of items purchased and total cost of the order.

## Implementation
- Python Flask will be used for all the server side scripting.
- The cart should be implemented with Session variables. Hint: the session should be based on the user login.
  - This means the shopping cart should *not* be stored in your database.
- Check user input: do not allow me to buy -2 boxes of detergent or, 100 boxes if you only have 1 in stock.
- Keep minimum information about customers: username and password, first and last name. We are not interested in addresses at this point.
- Where details are not specified in the assignment, you should assume something "reasonable" that you think the client will expect. You should record any design decisions or assumptions you made in your `Readme.md`.


## Grading levels
You have to complete most of the requirements for a level before you qualify for the next one.

### Bare Minimum earns you 50%
- [ ] The user can see all the products the store sells; minimum of 10 products.
- [ ] The user can see all the products in a specific category; minimum of 3 categories.
- [ ] Database schema and scripts to create and populate the tables.
  - [ ] This must be kept in the `store_schema.sql` file.
- [ ] Minimal web interface: web page does not look professional, minimal styling, no form checks.


### Base level takes you to 85% 
- [ ] The user can search for a specific item by name.
- [ ] The user can login, but not create a new account.
  - [ ] Users who are not in the DB can't login.
  - [ ] Must include a sample user named `testuser` with password `testpass`
- [ ] The logged in user can view, add to, edit, check out or delete their cart.
  - [ ] The cart should be stored as a session variable.
- [ ] The database is updated when a user checks out.
- [ ] The store doesn't let a user buy negative amounts or more than is in the inventory.

### Medium level takes you to 95%
- [ ] A new user can sign up.
- [ ] A logged in user can see his/her previous order history.
- [ ] The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
- [ ] Website style: products have pictures.

### Prime level takes you to 100%
- [ ] Implement client-side validation for input forms (e.g. quantity added to cart can't be negative) using Javascript.
- [ ] The logged in user can sort its orders by date.
- [ ] The logged in user can search for a product in his/her past orders.
- [ ] Website inspires a professional look: has logo, product descriptions, etc.

## Submission
To submit your work you must carefully do the following:
  - Fill in your personal info at the top of `Readme.md`
  - Check off (i.e., fill in a `- [X]`) every task you fully completed in the Grading Levels listed above
  - Remember to hit submit on Replit!

