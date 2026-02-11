from sqlalchemy.orm import Session
from models import Member
from schemas import MemberCreate, MemberUpdate
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append(r'D:/API ENV/crud.py') 
import schemas,models
from pymysql.err import IntegrityError



#crud operations for user 
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return db_user


def read_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def read_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return  {"message":"User Updated Successfully"}


#corrected
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return  {"message":"User deleted Successfully"}


#crud operations for members

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member



def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.Member_id == member_id).first()

##to be corrected
def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()


def update_member(db: Session, member_id: int, member_update: MemberUpdate):
    member = db.query(Member).filter(Member.Member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    update_data = member_update.dict(exclude_unset=True)
    db.query(Member).filter(Member.Member_id == member_id).update(update_data)
    db.commit()
    db.refresh(member)
    return  {"message":"Member updated Successfully"}



def delete_member(db: Session, member_id: int):
    member = db.query(models.Member).filter(models.Member.Member_id == member_id).first()
    if member:
        db.delete(member)
        db.commit()
        return  {"message":"Member deleted Successfully"}
    
#   File "/Users/awais/Documents/DBMS_Project/main.py", line 283, in read_all_country_info
#     return crud.get_all_country_info(db=db)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/awais/Documents/DBMS_Project/crud.py", line 115, in get_all_country_info
#     return db.query(models.Country_Info).all()
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 
#CRUD operations for Country_Info

def create_country_info(db: Session, country_info: schemas.add_country):
    db_country_info = models.Country_Info(**country_info.dict())
    db.add(db_country_info)
    db.commit()
    db.refresh(db_country_info)
    return db_country_info

def get_country_info(db: Session, country_id: int):
    return db.query(models.Country_Info).filter(models.Country_Info.Country_Id == country_id).first()


# def get_deposit_statuses(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Deposit_status).offset(skip).limit(limit).all()
def get_all_country_info(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Country_Info).offset(skip).limit(limit).all()

def update_country_info(db: Session, country_id: int, country_info: schemas.update_country):
    db_country_info = db.query(models.Country_Info).filter(models.Country_Info.Country_Id == country_id).first()
    if db_country_info:
        for attr, value in country_info.dict().items():
            setattr(db_country_info, attr, value)
        db.commit()
        db.refresh(db_country_info)
    return db_country_info

def delete_country_info(db: Session, country_id: int):
    db_country_info = db.query(models.Country_Info).filter(models.Country_Info.Country_Id == country_id).first()
    if db_country_info:
        db.delete(db_country_info)
        db.commit()
    return db_country_info


   #CRUD operation for currency supported

def add_currency(db: Session, currency_supported: schemas.add_currency):
    #import pdb ; pdb.set_trace()
    currency_in_db = models.Currency_supported(**currency_supported.dict())
    db.add(currency_in_db)
    db.commit()
    db.refresh(currency_in_db)
    return currency_in_db

def get_currency(db: Session, currency_id: int):
    return db.query(models.Currency_supported).filter(models.Currency_supported.currency_id ==currency_id ).first()



def get_currencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Currency_supported).offset(skip).limit(limit).all()


def update_currency(db: Session, currency_id: int, currency_update: schemas.update_currency):
    currency = db.query(models.Currency_supported).filter(models.Currency_supported.currency_id == currency_id).first()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    update_data = currency_update.dict(exclude_unset=True)
    db.query(models.Currency_supported).filter(models.Currency_supported.currency_id == currency_id).update(update_data)
    db.commit()
    db.refresh(currency)
    return  {"message":"Currency  Updated Successfully"}


def delete_currency(db: Session, currency_id : int):
    currency = db.query(models.Currency_supported).filter(models.Currency_supported.currency_id == currency_id).first()
    if currency:
        db.delete(currency)
        db.commit()
        return  {"message":"Currency deleted Successfully"}


 #CRUD operation for currency_info 

def add_currency_info(db: Session, currency_info: schemas.add_currency_info):
    #import pdb ; pdb.set_trace()
    currency_info_in_db = models.Currency_info(**currency_info.dict())
    db.add(currency_info_in_db)
    db.commit()
    db.refresh(currency_info_in_db)
    return currency_info_in_db 



def get_currency_info(db: Session, currency_info_id: int):
    return db.query(models.Currency_info).filter(models.Currency_info.currency_info_id ==currency_info_id ).first()



def get_currencies_info(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Currency_info).offset(skip).limit(limit).all()


def update_currency_info(db: Session, currency_info_id: int, currency_info_update: schemas.update_currency_info):
    currency_info = db.query(models.Currency_info).filter(models.Currency_info.currency_info_id == currency_info_id).first()
    if not currency_info:
        raise HTTPException(status_code=404, detail="Currency_info not found")
    update_data = currency_info_update.dict(exclude_unset=True)
    db.query(models.Currency_info).filter(models.Currency_info.currency_info_id == currency_info_id).update(update_data)
    db.commit()
    db.refresh(currency_info)
    return  {"message":"Currency_info  Updated Successfully"}


def delete_currency_info(db: Session, currency_info_id : int):
    currency = db.query(models.Currency_info).filter(models.Currency_info.currency_info_id == currency_info_id).first()
    if currency:
        db.delete(currency)
        db.commit()
        return  currency



# #CRUD operation for withdrawals
def get_withdrawal(db: Session, withdrawal_id: int):
    return db.query(models.Withdrawal).filter(models.Withdrawal.withdrawal_id == withdrawal_id).first()


def get_all_withdrawals(db: Session):
    return db.query(models.Withdrawal).all()


def create_withdrawal(db: Session, withdrawal: schemas.WithdrawalCreate):
    withdrawal_data = models.Withdrawal(**withdrawal.dict())
    db.add(withdrawal_data)
    db.commit()
    db.refresh(withdrawal_data)
    return withdrawal_data


def update_withdrawal(db: Session, withdrawal_id: int, withdrawal: schemas.WithdrawalUpdate):
    withdrawal_data = db.query(models.Withdrawal).filter(models.Withdrawal.withdrawal_id == withdrawal_id).first()
    if withdrawal_data:
        for key, value in withdrawal.dict(exclude_unset=True).items():
            setattr(withdrawal_data, key, value)
        db.commit()
        db.refresh(withdrawal_data)
    return  {"message":"Withdrawal updated Successfully"}


def delete_withdrawal(db: Session, withdrawal_id: int):
    withdrawal_data = db.query(models.Withdrawal).filter(models.Withdrawal.withdrawal_id == withdrawal_id).first()
    if withdrawal_data:
        db.delete(withdrawal_data)
        db.commit()
        return {"message":"Withdrawal deleted Successfully"}
    return { {"message":"Not existed"}}
#crud operations for Deposit


def create_deposit(db: Session, deposit:schemas.DepositCreate):
    db_deposit = models.Deposit(**deposit.dict())
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit


def get_deposit(db: Session, deposit_id: int):
    return db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()


def get_deposits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Deposit).offset(skip).limit(limit).all()


def update_deposit(db: Session, deposit_id: int, deposit_update: schemas.DepositUpdate):
    deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    update_data = deposit_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(deposit, key, value)
    db.commit()
    db.refresh(deposit)
    return {"message":"Deposit updated Successfully"}


def delete_deposit(db: Session, deposit_id: int):
    db_deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if db_deposit:
        db.delete(db_deposit)
        db.commit()
        return db_deposit


# cruds for deposit status
def create_deposit_status(db: Session, deposit:schemas.add_deposit_status):
    db_deposit = models.Deposit_status(**deposit.dict())
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit


def get_deposit_status(db: Session, deposit_id: int):
    return db.query(models.Deposit_status).filter(models.Deposit_status.status_id == deposit_id).first()


def get_deposit_status(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Deposit_status).offset(skip).limit(limit).all()


def update_deposit_status(db: Session, deposit_id: int, deposit_status_update: schemas.update_status):
    deposit_status = db.query(models.Deposit_status).filter(models.Deposit_status.status_id == deposit_id).first()
    if not deposit_status:
        raise HTTPException(status_code=404, detail="Deposit status not found")
    for key, value in deposit_status_update.dict(exclude_unset=True).items():
        setattr(deposit_status, key, value)
    db.commit()
    db.refresh(deposit_status)
    return deposit_status


def update_withdrawal(db: Session, withdrawal_id: int, withdrawal: schemas.WithdrawalUpdate):
    withdrawal_data = db.query(models.Withdrawal).filter(models.Withdrawal.withdrawal_id == withdrawal_id).first()
    if withdrawal_data:
        for key, value in withdrawal.dict(exclude_unset=True).items():
            setattr(withdrawal_data, key, value)
        db.commit()
        db.refresh(withdrawal_data)
    return  {"message":"Withdrawal updated Successfully"}


def delete_deposit_status(db: Session, status_id: int):
    db_deposit_status = db.query(models.Deposit_status).filter(models.Deposit_status.status_id == status_id).first()
    if db_deposit_status:
        db.delete(db_deposit_status)
        db.commit()
        return db_deposit_status



#CRUD operation for Gateway
def add_gateway(db: Session, gateway: schemas.add_gateway):
    #import pdb ; pdb.set_trace()
    gateway_in_db = models.gateway(**gateway.dict())
    db.add(gateway_in_db)
    db.commit()
    db.refresh(gateway_in_db)
    return gateway_in_db



def get_gateway(db: Session, gateway_id: int):
    return db.query(models.gateway).filter(models.gateway.gateway_id ==gateway_id ).first()



def get_gateways(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.gateway).offset(skip).limit(limit).all()

def update_gateway(db: Session, gateway_id: int, gateway_update: schemas.update_gateway):
    gateway = db.query(models.gateway).filter(models.gateway.gateway_id == gateway_id).first()
    if not gateway:
        raise HTTPException(status_code=404, detail="gateway not found")
    update_data = gateway_update.dict(exclude_unset=True)
    db.query(models.gateway).filter(models.gateway.gateway_id == gateway_id).update(update_data)
    db.commit()
    db.refresh(gateway)
    return {"message":"Gateway Updated Successfully"}




# def delete_gateway(db: Session, gateway_id : int):
#     gateway = db.query(models.gateway).filter(models.gateway.gateway_id == gateway_id ).first()
#     if gateway:
#         db.delete(gateway)
#         db.commit()
#         return {"message":"Gateway deleted Successfully"}

def delete_gateway(db: Session, gateway_id: int):
    gateway = db.query(models.gateway).filter(models.gateway.gateway_id == gateway_id).first()
    if gateway:
        db.delete(gateway)
        db.commit()
        return gateway
    else:
        raise HTTPException(status_code=404, detail="Gateway not found")

#Crud Operations for Transaction Logs 
    
def get_transaction_log(db: Session, transaction_log_id: int):
    return db.query(models.TransactionLog).filter(models.TransactionLog.transaction_log_id == transaction_log_id).first()


def get_all_transaction_logs(db: Session):
    return db.query(models.TransactionLog).all()


def create_transaction_log(db: Session, transaction_log: schemas.TransactionLogCreate):
    transaction_log_data = models.TransactionLog(**transaction_log.dict())
    db.add(transaction_log_data)
    db.commit()
    db.refresh(transaction_log_data)
    return transaction_log_data


def update_transaction_log(db: Session, transaction_log_id: int, transaction_log: schemas.TransactionLogUpdate):
    transaction_log_data = db.query(models.TransactionLog).filter(
        models.TransactionLog.transaction_log_id == transaction_log_id).first()
    if transaction_log_data:
        for key, value in transaction_log.dict(exclude_unset=True).items():
            setattr(transaction_log_data, key, value)
        db.commit()
        db.refresh(transaction_log_data)
    return transaction_log_data

def delete_transaction_log(db: Session, transaction_log_id: int):
    transaction_log_data = db.query(models.TransactionLog).filter(
        models.TransactionLog.transaction_log_id == transaction_log_id).first()
    if transaction_log_data:
        db.delete(transaction_log_data)
        db.commit()
        return {"message":"LOg deleted Successfully"}
    return {"message":"LOg not existed"}