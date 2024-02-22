#Defining all functions necessary for the application

#importing List to leave type hints for FastAPI
import os
from typing import List
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#defining global variables
menu = []

#function to take ingredients input from the user, input string and output an array of 7 ingredients
def take_ingredients(ingredients: List[str]) -> List[str]: 
    list_of_ingredients = ingredients
    return list_of_ingredients

#function to generate recipe, taking input list of ingredients above and outputting generated recipe as text
def generate_recipe(list_of_ingredients: List[str]) -> str: 
    user_prompt = "Ingredients: " + ", ".join(list_of_ingredients)
    system_prompt = "As a fitness nutritionist, my main objective is to create a single, healthy, balanced, and nutritious main meal recipe for either lunch or dinner at one time, with a strong emphasis on using the provided list of ingredients. The recipe should predominantly use the submitted ingredients, only adding extra items if absolutely necessary to enhance nutritional value, add flavour and excitement, or fulfill basic cooking requirements. The recipe should maintain a balance of nutrients, using the ingredients in suitable quantities. Please include a list of ingredients with specified quantities and offer detailed step-by-step preparation instructions. The focus should be on a recipe that supports an active lifestyle, highlighting lean proteins, whole grains, and fresh vegetables, while minimizing processed foods and excessive fats. The recipe should be presented in an easy-to-follow format, suitable for home cooking. Please generate one complete recipe at a time to ensure specificity and detailed guidance."
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.6,
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
            ]
        )
        recipe = completion.choices[0].message.content
        return recipe
    except Exception as e: 
        print("Error in generating recipe:", e)
        return "Error in recipe generation."

def save_recipes(recipe): 
    global menu
    if len(menu) < 7: 
        menu.append(recipe)
    elif len(menu) >=7: 
        print("7 recipes have been saved.")
    return menu

def generate_menu_pdf(menu, filename="menu.pdf"): 
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Starting Y position for the first line

    c.drawString(30, y_position, "Weekly Menu Recipes")
    y_position -= 20  # Space between title and first recipe

    for recipe in menu:
        lines = recipe.split('\n')
        for line in lines:
            line = line.replace('\n', ' ')
            y_position -= 20  # Space between recipes
            if y_position < 40:  # Check for new page
                c.showPage()
                y_position = height - 40
            # Draw each line and adjust the y_position
            c.drawString(30, y_position, line)
            y_position -= 20

    c.save()
    return filename


#defining the fast api endpoints for each function
@app.get("/")
async def read_root(request: Request):
    # You can pass variables to the template from here
    return templates.TemplateResponse("index.html", {"request": request})
#starting with the generate recipe endpoint

@app.post("/generate_recipe/")
async def generate_recipe_endpoint(ingredient1: str = Form(...), ingredient2: str = Form(...), ingredient3: str = Form(...), ingredient4: str = Form(...), ingredient5: str = Form(...)):
    ingredients = [ingredient1, ingredient2, ingredient3, ingredient4, ingredient5]
    # Filter out empty strings if ingredients are not provided
    ingredients = [ingredient for ingredient in ingredients if ingredient]
    recipe = generate_recipe(ingredients)
    if recipe.startswith("Error"):
        raise HTTPException(status_code=500, detail=recipe)
    return {"recipe": recipe, "message": "Recipe generated successfully."}

@app.post("/save_recipe/")
async def save_recipe_endpoint(recipe: str = Form(...)):
    if len(menu) >= 7:
        raise HTTPException(status_code=400, detail="You have already saved 7 recipes.")
    menu.append(recipe)
    return {"message": "Recipe saved successfully."}

@app.get("/download_menu/")
async def download_menu_endpoint():
    if not menu:
        raise HTTPException(status_code=404, detail="No recipes to generate a menu.")
    filename = generate_menu_pdf(menu)
    return FileResponse(path=filename, filename=filename, media_type='application/pdf')