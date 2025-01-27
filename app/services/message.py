from flask import flash

def success(message: str):
    flash(message, "success")
    
def error(message: str):
    flash(message, "error")
    
def created_success(entity: str):
    success(entity + " created successfully.")

def updated_success(entity: str):
    success(entity + " updated successfully.")
    
def deleted_success(entity: str):
    success(entity + " deleted successfully.")
    
def created_error(entity: str):
    error(entity + " creation failed.")

def updated_error(entity: str):
    error(entity + " updating failed.")
    
def deleted_error(entity: str):
    error(entity + " deletion failed.")