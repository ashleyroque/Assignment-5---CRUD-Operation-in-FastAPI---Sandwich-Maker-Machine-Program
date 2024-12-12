from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models import models, schemas

router = APIRouter(
    prefix="/resources",
    tags=["resources"],
)

def create_resource(db: Session, resource):
    db_resource = models.Resource(
        name=resource.name,
        description=resource.description,
        type=resource.type,
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).all()

def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource

def update_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    existing_resource = db_resource.first()
    if not existing_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    update_data = resource.dict(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(existing_resource)  # Refresh the existing resource object
    return existing_resource

def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    db.delete(db_resource)
    db.commit()
    return db_resource