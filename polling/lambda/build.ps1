#!/usr/bin/env pwsh

$BUILD_DIR = ".target"

if (Test-Path -Path $BUILD_DIR) {
    Remove-Item -Recurse -Force -Path $BUILD_DIR
}

New-Item -ItemType Directory -Path $BUILD_DIR
& $PYTHON310 -m pip install -r requirements.txt -t $BUILD_DIR

Copy-Item -Path *.py -Destination $BUILD_DIR

$OUT_FILE = [System.IO.Path]::GetFullPath("$pwd/../terraform/code/lambda.zip")
Compress-Archive -Force -Path $BUILD_DIR\* -DestinationPath $OUT_FILE

Write-Host "Created - $OUT_FILE"
