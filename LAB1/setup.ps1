

if( !(Test-Path ".\main.py") ){
    New-Item -Path ".\main.py"
}
else{
    echo ".\main.py already exists"
}

if( !(Test-Path ".\model.py") ){
    New-Item -Path ".\model.py"
}
else{
    echo ".\model.py already exists"
}

if( !(Test-Path ".\config.py") ){
    New-Item -Path ".\config.py"
}
else{
    echo ".\config.py already exists"
}

if( !(Test-Path ".\requirements.txt") ){
    New-Item -Path  ".\requirements.txt"
    Set-Content -Path ".\requirements.txt" -Value "flask"
    Add-Content -Path ".\requirements.txt" -Value "`nflask-sqlalchemy"
}
else{
    echo ".\requirements.txt already exists"
}


if( !(Test-Path ".\venv\") ){
    python -m venv ./venv
}
else{
    echo "Virtual enviorement already exists."
}

./venv/Scripts/Activate.ps1
pip install -r ./requirements.txt 
cls