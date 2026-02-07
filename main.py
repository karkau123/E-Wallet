from fastapi import FastAPI,HTTPException,Query,Depends,status,Response
from typing import Optional,List
import mysql.connector
import time
from database import Base,engine,SessionLocal
from models import User
#from . import models,schemas
from sqlalchemy.orm import Session
from pydantic import ValidationError
from sqlalchemy import text

import sys
sys.path.append(r'D:/API ENV/main.py')
import models , schemas , crud
from crud import create_user, read_users, read_user, update_user, delete_user
models.Base.metadata.create_all(bind=engine)
from sqlalchemy import func

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="naJL9!2d",
            database="Digital_Wallet"
        )
        print("Connected")
        break


    except Exception as error:
        print("Connection Failed")
        print("Error", error)
        time.sleep(2)


mycursor = mydb.cursor()


@app.post("/users/", response_model=schemas.UserBase)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
     db_user = create_user(db=db, user=user)
     return schemas.UserBase.from_orm(db_user)

# get all users
@app.get("/users/", response_model=List[schemas.User])
def read_users_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = "SELECT * FROM Users"
    mycursor.execute(query, {"limit": limit, "skip": skip})
    users = mycursor.fetchall()
    return [
        schemas.User(
            id=user[0],
            username=user[1],
            password=user[2],
            complete_name=user[3],
            email_address=user[4]
        )
        for user in users
    ]


# get a specific user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_api(user_id: int, db: Session = Depends(get_db)):
    query = "SELECT * FROM Users WHERE id = %s"
    mycursor.execute(query, (user_id,))
    user = mycursor.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User(
        id=user[0],
        username=user[1],
        password=user[2],
        complete_name=user[3],
        email_address=user[4]
    )

#update a user by id

@app.put("/users/{user_id}")
def update_user_api(user_id: int, user:schemas.UserUpdate , db: Session = Depends(get_db)):
    query = text("UPDATE users SET username = :username, password = :password, complete_name = :complete_name, email_address = :email_address WHERE id = :id")
    values = {
        "id": user_id,
        "username": user.username,
        "password": user.password,
        "complete_name": user.complete_name,
        "email_address": user.email_address,
    }
    db.execute(query, values)
    db.commit()
    return {"message": "User updated successfully"}



# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete(id: str):

#     query = f"delete from post where id = {id}"
#     mycursor.execute(query)
#     myresult = mycursor.fetchone()
#     mydb.commit()
#     if myresult==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT, detail="Post was deleted")

# delete a user by id
# @app.delete("/users/{user_id}")
# def delete_user_api(user_id: int, db: Session = Depends(get_db)):
#     query = "DELETE FROM Users WHERE id = %s"
#     values = (user_id,)
#     mycursor.execute(query, values)
    
#     if mycursor.rowcount == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

#     db.commit()
#     db.close()

#     return {"messsge":"User deleted successfully"}

#corrected
@app.delete("/users/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

#CRUD operations for Member entity
#create a new member

@app.post("/members/", response_model=schemas.Member)
def create_member_api(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    try:
        processed_by_id = member.processed_by_id
        print(processed_by_id)
        return crud.create_member(db=db, member=member)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
#getting All members

@app.get("/members/", response_model=List[schemas.Member])
def read_members_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = "SELECT * FROM Members"
    mycursor.execute(query, {"limit": limit, "skip": skip})
    members = mycursor.fetchall()
    return [
        schemas.Member(
            Member_id=row[0],
            First_name=row[1],
            Middle_name=row[2],
            Last_name=row[3],
            Email=row[4],
            Country_Id=row[5],
            Contact_Number=row[6],
            username=row[7],
            password=row[8],
            account_status=row[9],
            processed_by_id =row[10]
        )
        for row in members
    ]
  # get a specific member by id
@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member_api(member_id: int, db: Session = Depends(get_db)):
    query = "SELECT * FROM Members WHERE Member_id = %s"
    mycursor.execute(query, (member_id,))
    member = mycursor.fetchone()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return schemas.Member(
           Member_id=member[0],
            First_name=member[1],
            Middle_name=member[2],
            Last_name=member[3],
            Email=member[4],
            Country_Id=member[5],
            Contact_Number=member[6],
            username=member[7],
            password=member[8],
            account_status=member[9],
            processed_by_id =member[10]
        )
    



#Corrected
@app.put("/members/{member_id}", response_model=schemas.Member)
def update_member_api(member_id: int, member_update: schemas.MemberUpdate, db: Session = Depends(get_db)):
    query = text("""
        UPDATE members 
        SET First_name = :first_name, 
            Last_name = :last_name,
            Email = :email,
            Country_ID = :country_id,
            Contact_Number = :contact_number,
            username = :username,
            password = :password,
            account_status = :account_status,
            processed_by_id = :processed_by_id
        WHERE Member_id = :member_id
    """)

    values = {
        "member_id": member_id,
        "first_name": member_update.First_name,
        "last_name": member_update.Last_name,
        "email": member_update.Email,
        "country_id": member_update.Country_Id,
        "contact_number": member_update.Contact_Number,
        "username": member_update.username,
        "password": member_update.password,
        "account_status": member_update.account_status,
        "processed_by_id": member_update.processed_by_id
    }

    db.execute(query, values)
    db.commit()

    updated_member = crud.get_member(db, member_id=member_id)
    if updated_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return updated_member
# delete a member by id`

#Corrected
@app.delete("/members/{member_id}")
def delete_member_api(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_member(db=db, member_id=member_id)
    return {"message": "Member deleted successfully"}

#creating a new currrency
@app.post("/country_info/", response_model=schemas.Country_Info)
def create_country_info(country_info: schemas.add_country, db: Session = Depends(get_db)):
    try:
        return crud.create_country_info(db=db, country_info=country_info)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/country_info/{country_id}", response_model=schemas.Country_Info)
def read_country_info(country_id: int, db: Session = Depends(get_db)):
    db_country_info = crud.get_country_info(db=db, country_id=country_id)
    if db_country_info is None:
        raise HTTPException(status_code=404, detail="Country info not found")
    return db_country_info