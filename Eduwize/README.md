# Eduwize - AI-Powered Learning Platform

Eduwize is a comprehensive educational platform designed specifically for college students, leveraging AI to enhance the learning experience through personalized recommendations, interactive study tools, and performance tracking.

![Eduwize Platform](eduwize_app/static/eduwize_app/images/default-profile.png)

## 🚀 Features

### For Students
- **Personalized Dashboard**: Get a quick overview of your courses, upcoming quizzes, and performance metrics
- **AI Learning Assistant**: Chat with our AI assistant to get help with course concepts, study planning, and more
- **Smart Recommendations**: Receive personalized course and resource recommendations based on your learning patterns
- **Interactive Quizzes**: Test your knowledge with adaptive quizzes that adjust to your skill level
- **Performance Analytics**: Track your progress with detailed analytics and insights
- **Study Material Management**: Access and organize all your course materials in one place

### For Educators
- **Course Management**: Create and manage courses with ease
- **Quiz Creation**: Design quizzes with various question types and automatic grading
- **Student Progress Tracking**: Monitor student performance and identify areas where they need help
- **Resource Sharing**: Share study materials, videos, and documents with students
- **Feedback Collection**: Gather and analyze student feedback to improve courses

## 🛠️ Technology Stack

- **Backend**: Django (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Services**: Custom AI models for chatbot and recommendations
- **Authentication**: Django's built-in authentication system
- **Responsive Design**: Mobile-friendly interface that works on all devices

## 🔧 Installation

### Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/eduwize.git
   cd eduwize
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

### Production Deployment

#### Using Docker (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/eduwize.git
   cd eduwize
   ```

2. Create an environment file:
   ```
   cp .env.example .env
   # Edit .env with your production settings
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up -d
   ```

4. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

5. Access the application at your domain (configured in Nginx)

#### Manual Deployment

1. Set up a server with Ubuntu 22.04 LTS

2. Install required packages:
   ```
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql nginx redis-server
   ```

3. Create a PostgreSQL database and user:
   ```
   sudo -u postgres psql
   CREATE DATABASE eduwize;
   CREATE USER eduwize_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE eduwize TO eduwize_user;
   \q
   ```

4. Create a system user:
   ```
   sudo adduser eduwize
   sudo usermod -aG www-data eduwize
   ```

5. Clone the repository:
   ```
   sudo -u eduwize git clone https://github.com/yourusername/eduwize.git /home/eduwize/app
   ```

6. Set up a virtual environment:
   ```
   sudo -u eduwize python3 -m venv /home/eduwize/venv
   sudo -u eduwize /home/eduwize/venv/bin/pip install -r /home/eduwize/app/requirements-prod.txt
   ```

7. Create and configure the .env file:
   ```
   sudo -u eduwize cp /home/eduwize/app/.env.example /home/eduwize/app/.env
   sudo -u eduwize nano /home/eduwize/app/.env
   # Edit with your production settings
   ```

8. Set up Gunicorn service:
   ```
   sudo cp /home/eduwize/app/scripts/gunicorn.service /etc/systemd/system/
   sudo systemctl enable gunicorn
   sudo systemctl start gunicorn
   ```

9. Configure Nginx:
   ```
   sudo cp /home/eduwize/app/nginx/conf.d/eduwize.conf /etc/nginx/sites-available/eduwize
   sudo ln -s /etc/nginx/sites-available/eduwize /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

10. Set up SSL with Let's Encrypt:
    ```
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d eduwize.com -d www.eduwize.com
    ```

11. Access the application at your domain

## 📱 User Interface

Eduwize features a modern, intuitive user interface designed for optimal user experience:

- **Clean Dashboard**: Get a quick overview of your academic progress
- **Intuitive Navigation**: Easily find what you need with our well-organized menu
- **Dark/Light Mode**: Choose the theme that works best for you
- **Responsive Design**: Access Eduwize from any device - desktop, tablet, or mobile
- **Accessibility Features**: Designed to be accessible to all users

## 🤖 AI Capabilities

Our platform leverages artificial intelligence to enhance the learning experience:

- **Intelligent Chatbot**: Get instant answers to your questions about courses, concepts, and study strategies
- **Personalized Recommendations**: Receive custom-tailored course and resource suggestions based on your learning patterns
- **Adaptive Learning**: Experience a learning path that adapts to your strengths and weaknesses
- **Performance Prediction**: Get insights into your expected performance based on your study habits
- **Content Summarization**: AI-generated summaries of study materials to help you review efficiently

## 🔒 Security & Privacy

We take security and privacy seriously:

- **Secure Authentication**: Robust user authentication system
- **Data Encryption**: All sensitive data is encrypted
- **Privacy Controls**: Users have control over their data
- **Regular Backups**: Automatic backup system to prevent data loss
- **GDPR Compliance**: Designed with privacy regulations in mind

### Production Security Measures

For production deployments, we've implemented additional security measures:

- **HTTPS Enforcement**: All traffic is encrypted using SSL/TLS
- **Content Security Policy (CSP)**: Prevents XSS attacks
- **HTTP Strict Transport Security (HSTS)**: Ensures secure connections
- **Rate Limiting**: Prevents brute force and DDoS attacks
- **Database Connection Pooling**: Optimizes database connections
- **Secure Cookie Settings**: Prevents cookie theft and session hijacking
- **Environment Variable Management**: Sensitive data is stored in environment variables
- **Regular Security Updates**: Dependencies are regularly updated to patch vulnerabilities

### Maintenance Procedures

To keep your Eduwize installation secure and performant:

1. **Regular Backups**: Daily automated database backups
2. **Monitoring**: Prometheus and Grafana for system monitoring
3. **Health Checks**: Endpoint for monitoring system health
4. **Log Rotation**: Prevents logs from consuming disk space
5. **Database Maintenance**: Regular vacuum and index optimization
6. **Security Audits**: Periodic security assessments
7. **Dependency Updates**: Regular updates of all dependencies

## 🔄 Future Enhancements

We're constantly working to improve Eduwize. Upcoming features include:

- **Peer Collaboration Tools**: Work together with classmates on projects and study groups
- **Advanced Analytics**: More detailed insights into learning patterns
- **Mobile App**: Native mobile applications for iOS and Android
- **Integration with LMS**: Seamless integration with popular Learning Management Systems
- **Gamification Elements**: Earn points, badges, and rewards for learning achievements

## 👥 Contributing

We welcome contributions to Eduwize! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to get involved.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any questions or support, please contact us at support@eduwize.com or open an issue on GitHub.
