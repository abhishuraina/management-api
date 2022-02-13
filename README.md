# management-api
Start the Project 
1. Clone the repo.
2. Make a virtual Env, Activate it and run pip install -r requirements.txt.
3. Run python manage.py runserver to start the server.
After the app starts to test the different urls go to http://localhost:8000/docs/ Docs will have all the end points.

Steps to perform all operations ( all operations tested in postman )
1. Make a POST Request to http://127.0.0.1:8000/api/user/register/ 
 Type can be - APP_ADMIN, COMPANY_ADMIN, EMPLOYEE
Payload {
    "email": "testuser@gmail.com",
    "password": "12345678",
    "user_name": "test user",
    "type": "EMPLOYEE"
}
2. Add the login credentials in post man under Basic auth username = email user registered with and password
3. Make a POST Request to http://localhost:8000/api/company/ ( To add a company )
Payload - {
    "name": "bmw",
    "admin": 8
}
Here name is Name of the company and admin is the company admin we want with the respective company 
4. Make a POST request to http://localhost:8000/api/employees/ ( Add a employee to company )
payload - {
    "name": 6,
    "company": 1
}
Here name is the userId and company is the company id (added)
5. Make a POST request to http://localhost:8000/api/project/ (add a project to a company)
payload - {
    "name": "improve production",
    "description": "improves sales",
    "creator": "7",
    "company" : "2",
    "admin" :"8"
}
Here name - name of the project, description - Project description, Creator - userId, Company - company id, admin - company Admin
6. To edit a project Make a PUT Request to http://localhost:8000/api/project/{id}/  id = project id
payload - payload - {
    "name": "improve production",
    "description": "improves sales",
    "creator": "7",
    "company" : "2",
    "admin" :"8"
}
7. To delete a project Make a Delete Request to http://localhost:8000/api/project/{id}/  id = project id
8. To Remove Employees from company Make a PUT Request to http://localhost:8000/api/company/{id}/ id = company id 
{
    "name": 9,
    "company": ""
}
Here name is registered User Id, company is registered company = ""
9. Remove a company Make a DELETE Request to http://localhost:8000/api/company/{id}/
10. To edit user Profile make a PUT Request to http://localhost:8000/api/user/profile/{id}/  registered user id
payload - {
    "email": "abhishuraina@gmail.com",
    "user_name": "abhishu",
    "type": "COMPANY_ADMIN",
    "id": 1,
    "company": null,
    "first_name":"rainaa",
    "last_name": "abhishu"
}
11. Helping APIs Get http://localhost:8000/api/users/ gives all registerd users
12. http://localhost:8000/api/project/ gives all projects 
13. http://localhost:8000/api/company/ gives list of all companies 
14. http://localhost:8000/api/employees/ gives list of all employees 
