from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.core.security import get_current_user
from app.core.database import get_db
from app.core.config import settings
from app.models.user import StoredFile
from app.services.storage import storage

router=APIRouter(prefix="/api/files",tags=["Files"])
ALLOWED={"image/jpeg","image/png","application/pdf","image/webp"}

@router.post("/upload")
async def upload(file:UploadFile=File(...),user=Depends(get_current_user),db=Depends(get_db)):
    if file.content_type not in ALLOWED:
        raise HTTPException(400,"Only JPG, PNG, WEBP and PDF files are allowed")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:
        raise HTTPException(413,f"Maximum file size is {settings.max_upload_mb} MB")
    path,url=storage.save(data,file.filename or "upload",file.content_type)
    row=StoredFile(user_id=user.id,file_name=file.filename or "upload",storage_path=path,content_type=file.content_type,file_size=len(data))
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"file_name":row.file_name,"url":url,"size":row.file_size}
