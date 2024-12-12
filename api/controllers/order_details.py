from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models import models, schemas

router = APIRouter(
    prefix="/order_details",
    tags=["order_details"],
)

def create_order_detail(db: Session, order_detail):
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        item_id=order_detail.item_id,
        quantity=order_detail.quantity,
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def read_all_order_details(db: Session = Depends(get_db)):
    return db.query(models.OrderDetail).all()

def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderDetail not found")
    return order_detail

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

def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OrderDetail not found")
    db.delete(db_order_detail)
    db.commit()
    return db_order_detail