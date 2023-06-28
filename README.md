# Django-Issue-Tracker

As of today I start this project. I decided to write an SRS and follow it in sprints until project completion. 

Please see below my SRS for this Project:

# Software Requirements Specification (SRS)

## 1. Introduction:
    
### Overview:

This web app will allow a team to work collaboratively by providing a platform where they can track each task they are performing as a ticket (or "issue"). Team members will be able to collaborate on each ticket they are assigned to by sending messages and attachments until the task is finished and the ticket is closed.

## Intended users:

- **admin**: oversees the work being done on the platform.
- **team_member**: works on the tasks linked to the tickets, and the tickets themselves.
- **guest:** has access to the platform, but only for read purposes.
	    
### Underlying assumptions or dependencies:

- **Dependencies:** Django, Bootstrap, PostgreSQL.
- **Security and Authentication:** HTTPS; Django authentication system.
- **External services:** SendGrid API.

## 2. Functional Requirements:

- Access to the web app will be through username/password login.
- Operations available to each user type:
	- **admin**: full access to all CRUD operations for tickets and users.
	- **team_member**: can create, read and update tickets.
	- **guest:** can read tickets.
- Tickets status:
	- OPEN: the task is not finished.
	- CLOSED: the task is finished.
	- ON HOLD: the task can't be completed right now.
- Ticket submission process:
	- A team_member creates a ticket (status OPEN), and assigns it to one or more team members.
	- The assigned team members (ticket creator included) start to work in the ticket, sending messages and attachments in it.
	- Once the task is finished, one of the assigned team members closes the ticket (status CLOSED).
- Additional features or modules required:
	* Notifications: to be sent when to user when a ticket liked to them is created or updated. 
	* File Attachments: files can be uploaded upon ticket creation, or comments in tickets.
	* Ticket categories: to be managed by admin. By default tickets will be classified as "general".

## 4. Project Timeline and Resources:
    
- The project is expected to be finished in one month.
- I will advance in sprints of 3 to 7 days.
- Key milestones:
	1. Project Setup and User Authentication.
	2. Ticket Management.
	4. Guest Ticket Viewing.
	5. Ticket Responses and Updates.
	6. Frontend Enhancements.
	7. Testing and Quality Assurance.
	8. Deployment and Launch.
	9. Post-Launch Enhancements and Maintenance.

<!--
Things I might add to the SRS (below is a template):

## 3. Non-functional Requirements

- Performance expectations:
	- Response time: response times under two seconds for most operations to ensure a smooth user experience.
	- Concurrent users: the amount of users the ticket app should be able to handle without significant degradation in performance will be 20.
	- Scalability: if this was for formal project and not a portfolio one, I would use AWS for horizontal scaling (adding more servers) when needed.
	- Database Performance: I will optimize database queries, use appropriate indexing, and consider caching strategies to improve database performance.
	- File Attachments: the expected size per file will be 2 Megabytes, and number of attachments per message will be 5. The file uploads and downloads will be optimized to minimize the impact on system performance.
	- Caching and Optimizations: I will implement caching mechanisms to reduce the load on the server and improve response times.
	- Error Handling and Logging: I will implement error handling mechanisms to capture and handle errors gracefully.
	- Monitoring and Alerting: I will set up monitoring tools to track system performance, resource utilization, and application metrics.
	- Testing and Optimization: I will conduct performance testing at various stages of development to identify and address bottlenecks early on.

- Security measures: 
	- Secure Authentication:
		- Enforce strong password policies.
		- Secure password storage.
	- Role- Based Access Control: users can only access the features and data relevant to them.
	- Secure communication: 
		- HTTPS/TLS to encrypt data transmitted between the client and the server.
		- Implement mechanisms to prevent common web vulnerabilities (as Cross Site Scripting  and Cross-Site Request Forgery attacks).
	- Input Validation and Sanitization:
		- Strict input validation to prevent common security vulnerabilities.
	- Protection against Brute-Force Attacks:
		- Implement mechanisms to detect and prevent brute-force attacks on user accounts, such as account lockouts or CAPTCHA challenges after a certain number of failed login attempts.


## 4. System Architecture:

- Describe the overall system architecture, including the Django framework and any other components or technologies being used.
	
- Document any integration points with external systems or APIs.
	
- Specify any performance or scalability considerations related to the system architecture.


## 3. User Interface (UI) Design:

- Provide a description or mock-ups of the user interface, highlighting key elements and navigation.
	
- Specify any design guidelines or branding requirements.
	
- Include any usability considerations or accessibility requirements.

## Testing and Quality Assurance:
    
- Specify the testing approach, including unit testing, integration testing, and user acceptance testing.
	
- Document any quality assurance processes or standards to be followed.
	
- Outline any performance or security testing requirements.
        
## Deployment and Maintenance:

- Describe the deployment strategy, including the target hosting environment (e.g., cloud hosting, on-premises).
	
- Specify any maintenance or support activities required, such as regular updates or bug fixes.
	
- Document any disaster recovery or backup procedures.    
-->
