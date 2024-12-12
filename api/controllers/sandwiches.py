from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models import models, schemas

router = APIRouter(
    prefix="/sandwiches",
    tags=["sandwiches"],
)

def create_sandwich(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        description=sandwich.description,
        price=sandwich.price,
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all_sandwiches(db: Session = Depends(get_db)):
    return db.query(models.Sandwich).all()

def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich

def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    existing_sandwich = db_sandwich.first()
    if not existing_sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")

    update_data = sandwich.dict(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_sandwich)  # Refresh the existing sandwich object
    return existing_sandwich

def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    db.delete(db_sandwich)
    db.commit()
    return db_sandwich