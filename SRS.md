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