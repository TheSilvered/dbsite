if (!(Test-Path -Path venv\))
{
    python -m venv venv
}

venv\Scripts\Activate.ps1

$packages = python -m pip list

if (!($packages -like "*django*"))
{
    python -m pip install django
}

if (!($packages -like "*matplotlib*"))
{
    python -m pip install matplotlib
}

if (!($packages -like "*numpy*"))
{
    python -m pip install numpy
}

Set-Alias -Name mng -Value .\mng
