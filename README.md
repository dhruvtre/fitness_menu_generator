# Fitness Menu Generator

## Overview
The Fitness Menu Generator is an API that creates a customized weekly menu of recipes designed to support an active and healthy lifestyle. The application receives user input for preferred ingredients and leverages OpenAI's language model to generate unique, balanced, and nutritious recipes. An easy-to-use HTML front end allows users to interact with the API through a web browser.

## Features

### Ingredient Input
- **Collects User Input**: Users can submit up to five ingredients they wish to include in their recipes via a simple HTML form.

### Recipe Generation
- **AI-Powered Recipes**: The application uses OpenAI's language model to generate recipes that focus on lean proteins, whole grains, and fresh vegetables, while minimizing processed foods and excessive fats.

### Menu Compilation
- **Weekly Menu**: Users can save up to seven recipes to create a weekly menu.

### PDF Generation
- **Downloadable Menu**: The menu can be compiled into a downloadable PDF, providing a convenient format for meal preparation.

### Front End
- **Interactive Web Page**: The `index.html` provides a user-friendly interface for entering ingredients and generating recipes. It includes form inputs for ingredient submission and buttons for recipe generation, saving recipes, and downloading the menu.

## Technical Details

### Backend
- The API is written in Python and uses FastAPI as the web framework.
- CORS middleware is configured to allow cross-origin requests, facilitating frontend integration.

### AI Integration
- The recipe generation is powered by OpenAI's GPT-3.5-turbo model, ensuring creative and diverse recipe suggestions.

### PDF Creation
- The application uses `reportlab` to generate a PDF file containing the user's weekly menu.

### Front End
- Built with HTML and minimal styling, the front end allows users to input ingredients, generate recipes, save them to a menu, and download the menu as a PDF.
- JavaScript is used to handle button clicks, form submissions, and to interact with the FastAPI backend.
