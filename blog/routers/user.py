from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

get_db = database.get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get('/{id}', response_model = schemas.ShowUser)
def show(id, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.Blog.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with id: {id} is not available."}
    return user