from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .models import models, schemas
from .controllers import orders, sandwiches, resources, recipes, order_details
from .dependencies.database import engine, get_db

app.include_router(orders.router)
app.include_router(sandwiches.router)
app.include_router(resources.router)
app.include_router(recipes.router)
app.include_router(order_details.router)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sandwiches.router)
app.include_router(orders.router)

@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)

@app.post("/", response_model=schemas.Sandwich)
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return create_sandwich(db=db, sandwich=sandwich)

@app.get("/", response_model=List[schemas.Sandwich])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return read_all(db=db)

@app.get("/{sandwich_id}", response_model=schemas.Sandwich)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = read_one(db=db, sandwich_id=sandwich_id)
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich

@app.put("/{sandwich_id}", response_model=schemas.Sandwich)
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    return update(db=db, sandwich_id=sandwich_id, sandwich=sandwich)

@app.delete("/{sandwich_id}", response_model=schemas.Sandwich)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return delete(db=db, sandwich_id=sandwich_id)

@app.post("/", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return create_resource(db=db, resource=resource)

@app.get("/", response_model=List[schemas.Resource])
def read_all_resources(db: Session = Depends(get_db)):
    return read_all_resources(db=db)

@app.get("/{resource_id}", response_model=schemas.Resource)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    return read_one_resource(db=db, resource_id=resource_id)

@app.put("/{resource_id}", response_model=schemas.Resource)
def update_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    return update_resource(db=db, resource_id=resource_id, resource=resource)

@app.delete("/{resource_id}", response_model=schemas.Resource)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    return delete_resource(db=db, resource_id=resource_id)

@app.post("/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return create_recipe(db=db, recipe=recipe)

@app.get("/", response_model=List[schemas.Recipe])
def read_all_recipes(db: Session = Depends(get_db)):
    return read_all_recipes(db=db)

@app.get("/{recipe_id}", response_model=schemas.Recipe)
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return read_one_recipe(db=db, recipe_id=recipe_id)

@app.put("/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    return update_recipe(db=db, recipe_id=recipe_id, recipe=recipe)

@app.delete("/{recipe_id}", response_model=schemas.Recipe)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return delete_recipe(db=db, recipe_id=recipe_id)

@app.post("/", response_model=schemas.OrderDetail)
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        item_id=order_detail.item_id,
        quantity=order_detail.quantity,
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

@app.get("/", response_model=List[schemas.OrderDetail])
def read_all_order_details(db: Session = Depends(get_db)):
    return db.query(models.OrderDetail).all()

@app.get("/{order_detail_id}", response_model=schemas.OrderDetail)
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderDetail not found")
    return order_detail

@app.put("/{order_detail_id}", response_model=schemas.OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    existing_order_detail = db_order_detail.first()
    if not existing_order_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderDetail not found")

    update_data = order_detail.dict(exclude_unset=True)
    db_order_detail.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_order_detail)  # Refresh the existing order detail object
    return existing_order_detail

@app.delete("/{order_detail_id}", response_model=schemas.OrderDetail)
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderDetail not found")
    db.delete(db_order_detail)
    db.commit()
    return db_order_detail