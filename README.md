# Yu-Gi-Crud
http://35.246.125.174:8001/


[Presentation](https://github.com/devops-cohort/piers/tree/Feature/Images/Card_GamePresentation.pptx)


![ERD diagram](https://github.com/devops-cohort/piers/tree/Feature/Images/Card_GameERD.PNG)

My ERD Diagram stayed the same throughout the project the many to many table relationship was fairly difficuly to code

![KANBAN board](https://github.com/devops-cohort/piers/tree/Feature/Images/Card_GameTrello.PNG)

Most of my KANBAN Board has been fully realised in the web app, noreable exceptions are; a seperate cloud environment for the flask app and; Admin ability to delete cards. Noteable successes are; Admin panel requiring the inclusion of a user class system in the database and; Users accessing many deck lists.

![Testing Coverage](https://github.com/devops-cohort/piers/tree/Feature/Images/Card_GameCoverage.PNG)

Testing could be drastically improved with Integration testing. This project will become a test base for me to practice tests on.

[CI Pipeline install file](https://github.com/devops-cohort/piers/tree/Feature/.install)

My CI Pipeline includes an install file that makes jenkins set up much more streamlined.


[Full Database](https://github.com/devops-cohort/piers/tree/Feature/Images/Cards.csv)




*Risk Assessment*

Password security:

The risk of password being compromised would be very high impact on the service, but steps were taken early on to ensure no passwords are ever stored in clear text.


GCP MySQL compromised:

The database being compromised would be catastrophic to the operation of the app, to ensure all measures were taken to protect this resource, environmental variables were used from the begining of development until the end.


Users accessing pages without permission:

Users accessing pages without permission could potentially lead to a server crash, extensive use of the login_required tag and redirect if statements have secured these pages.
