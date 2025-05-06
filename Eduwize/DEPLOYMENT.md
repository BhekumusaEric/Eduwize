# Deploying Eduwize to PythonAnywhere

This guide will walk you through deploying the Eduwize application on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (Free tier is sufficient for initial deployment)
2. Your Eduwize codebase

## Deployment Steps

### 1. Create a PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for an account
2. Choose the "Beginner" (free) account for initial deployment

### 2. Upload Your Code

#### Option 1: Using Git

1. Open a Bash console in PythonAnywhere
2. Clone your repository:
   ```bash
   git clone https://github.com/YourUsername/Eduwize.git
   ```

#### Option 2: Upload a ZIP file

1. Create a ZIP file of your Eduwize project
2. In PythonAnywhere, go to the Files tab
3. Upload the ZIP file
4. Open a Bash console and unzip the file:
   ```bash
   unzip Eduwize.zip
   ```

### 3. Set Up a Virtual Environment

1. In the Bash console, create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 eduwize-env
   ```

2. Activate the virtual environment:
   ```bash
   workon eduwize-env
   ```

3. Install the required packages:
   ```bash
   cd Eduwize
   pip install -r requirements.txt
   ```

### 4. Configure the Database

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### 5. Collect Static Files

1. Run the collectstatic command:
   ```bash
   python manage.py collectstatic --noinput
   ```

### 6. Configure the Web App

1. Go to the Web tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Enter the path to your project (e.g., `/home/yourusername/Eduwize`)

### 7. Configure WSGI File

1. Click on the WSGI configuration file link
2. Replace the contents with the contents of `pythonanywhere_wsgi.py`
3. Update the path to match your PythonAnywhere username:
   ```python
   path = '/home/yourusername/Eduwize'
   ```
4. Save the file

### 8. Configure Static Files

1. In the Web tab, scroll down to "Static files"
2. Add the following mappings:
   - URL: `/static/` -> Directory: `/home/yourusername/Eduwize/staticfiles`
   - URL: `/media/` -> Directory: `/home/yourusername/Eduwize/media`

### 9. Configure Virtual Environment

1. In the Web tab, scroll to "Virtualenv"
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/eduwize-env
   ```

### 10. Reload the Web App

1. Click the "Reload" button at the top of the Web tab

### 11. Visit Your Site

Your site should now be available at:
```
yourusername.pythonanywhere.com
```

## Troubleshooting

### Error Logs

If you encounter issues, check the error logs in the Web tab:
- Error log
- Server log
- Access log

### Common Issues

1. **Static files not loading**:
   - Make sure you've run `collectstatic`
   - Check the static files mappings in the Web tab

2. **Database errors**:
   - Make sure you've run migrations
   - Check database settings in `settings.py`

3. **WSGI errors**:
   - Check the path in the WSGI file
   - Make sure the virtual environment is correctly configured

## Updating Your Site

To update your site after making changes:

1. Upload the new code (via Git or ZIP)
2. Run migrations if needed
3. Collect static files if needed
4. Reload the web app in the Web tab
