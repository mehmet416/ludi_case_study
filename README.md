# Ludi Case Study
## Project Title: Ludi Case Study Presentation

### Overview:

This project is a web application aimed at presenting the Ludi Case Study. It provides an interactive interface for users to explore different sections of the case study, including Users, Simulations, Companies, and a Main Page. Each section offers various functionalities for users to interact with the data effectively.

### How to Use:

To use this project, follow these steps:

1. **Clone the Repository:**
   - Clone the repository from GitHub to your local machine.
   
2. **Navigate to the Project Directory:**
   - Navigate to the directory of the cloned repository:
     ```bash
     cd ludi_case_study
     ```
   
3. **Run the Development Server:**
   - Run the Django development server:
     ```bash
     python manage.py runserver
     ```
   - The website will be accessible at `http://127.0.0.1:8000/`.

4. **Explore the Website:**
   - Open your web browser and visit `http://127.0.0.1:8000/` to access the main page and explore the different sections of the case study.

### Project Structure:

- **Source:** The project source code is organized into different directories, including:
  - `myapp`: Contains the Django application code.
  - `templates`: Contains HTML templates for different sections of the website.
  - `static`: Contains static files (e.g., CSS, JavaScript) used in the project.
- **Templates:**
  - `base.html`: The main template that each section inherits. It defines the overall structure of the website.
  - `index.html`: The main page template displaying a graph of daily user growth.
  - `users.html`, `simulations.html`, `companies.html`: Templates for presenting data about users, simulations, and companies, respectively.
- **Functionality:**
  - Each section of the website provides functionalities for users to interact with the data, such as sorting columns, visual representations (e.g., progress bars), and exploring details about users, simulations, and companies.
  - The main page features a graph depicting the daily growth of users, providing insights into user engagement over time.

### Sources:

- This project is built using Django, a high-level Python web framework.
- Bootstrap is used for styling the website and ensuring a responsive design.
- Python libraries such as matplotlib and pandas are utilized for data visualization and manipulation.
- The project's source code is available on [GitHub](https://github.com/mehmet416/ludi_case_study), allowing users to contribute, report issues, or suggest improvements.

### Conclusion:

The Ludi Case Study Presentation website offers a comprehensive platform for users to explore and analyze the data effectively. By following the steps mentioned above, users can easily download and run the project on their local machine, gaining valuable insights into the case study's various aspects.
