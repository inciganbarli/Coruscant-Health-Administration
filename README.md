# Welcome to Coruscant Health Administration

## Task
The problem was to rebuild the Medical Management System for the Coruscant Health Administration (CHA). The challenge involved creating a multi-stakeholder platform (Patients, Doctors, Administrators, Emergency Services, and Departments) that handles sensitive medical data, daily health readings from devices, and medical service orders, all while maintaining high security standards and a premium user experience in the Galactic Republic context.

## Description
I solved this problem by developing a robust web application using **Python** and **Django**. 
- **Stakeholder Management**: Implemented role-based access control for all 5 stakeholder groups.
- **Security**: Developed a custom authenticated encryption layer (PBKDF2-HMAC-SHA256) to ensure that all uploaded medical documents are encrypted on disk and only accessible to authorized users.
- **UI/UX**: Created a high-end, responsive dark-themed interface using Vanilla CSS and modern design principles.
- **Functionality**: Built features for real-time device data uploads, medical reporting, service order tracking (CT Scans, MRI, etc.), and efficient emergency patient admission.
- **Quality Assurance**: Integrated comprehensive unit tests and a CI/CD pipeline via GitHub Actions.

## Installation
To install and run this project locally:

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py run_server
   ```

## Usage
The application works through a web browser. Once the server is running:

1. Navigate to `http://127.0.0.1:8000/`.
2. Register as a **Doctor** or **Patient** (or use an Admin account to manage users).
3. **Patients** can upload data from their medical devices.
4. **Doctors** can view patient records, prescribe reports, and order scans.
5. **Departments** can fulfill orders and upload encrypted results.
6. **Emergency Services** can use the "Emergency" dashboard for rapid patient intake.

Run tests with:
```bash
python manage.py test
```

## The Core Team
Inci Ganbarli & Ilgar Farhadov

Made at Qwasar SV -- Software Engineering School <img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' />
