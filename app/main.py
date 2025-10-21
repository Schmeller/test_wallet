from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from . import schemas, services, database
from .database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wallet API", version="1.0.0")

@app.post("/api/v1/wallets/{wallet_id}/operation")
def create_operation(
    wallet_id: uuid.UUID,
    operation: schemas.OperationCreate,
    db: Session = Depends(database.get_db)
):
    try:
        wallet = services.WalletService.process_operation(db, wallet_id, operation)
        return {"message": "Operation completed successfully", "balance": float(wallet.balance)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@app.get("/api/v1/wallets/{wallet_id}")
def get_wallet(
    wallet_id: uuid.UUID,
    db: Session = Depends(database.get_db)
):
    wallet = services.WalletService.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return schemas.WalletResponce(
        id=wallet.id,
        balance=float(wallet.balance),
        created_at=wallet.created_at.isoformat()
    )

@app.post("/api/v1/wallets")
def create_wallet(db: Session = Depends(database.get_db)):
    wallet = services.WalletService.create_wallet(db)
    return schemas.WalletResponce(
        id=wallet.id,
        balance=float(wallet.balance),
        created_at=wallet.created_at.isoformat()
    )

@app.get("/")
def read_root():
    return {"message": "Wallet API", "docs": "/docs", "version": "1.0.0"}