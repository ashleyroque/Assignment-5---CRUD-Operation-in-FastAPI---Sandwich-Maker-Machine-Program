from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models import models, schemas

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)
def create_recipe(db: Session, recipe):
    db_recipe = models.Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    existing_recipe = db_recipe.first()
    if not existing_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    update_data = recipe.dict(exclude_unset=True)
    db_recipe.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_recipe)  # Refresh the existing recipe object
    return existing_recipe

def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return db_recipe