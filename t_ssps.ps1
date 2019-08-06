[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") > $null
[System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") > $null


$jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.FormatDescription -eq "JPEG" }; Start-Sleep -Milliseconds 250
[System.Windows.Forms.Sendkeys]::SendWait("{PrtSc}"); Start-Sleep -Milliseconds 250   
$bitmap = [System.Windows.Forms.Clipboard]::GetImage()    
$ep = New-Object Drawing.Imaging.EncoderParameters
$ep.Param[0] = New-Object Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, [long]100)


$admin = (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))


if($admin)
{
    $path = "C:\Windows\Temp\" + [System.IO.Path]::GetRandomFileName() + ".jpg"
    $bitmap.Save($path, $jpegCodec, $ep); Start-Sleep -Milliseconds 250
    Write-Host $path
}
elseif (Test-Path -Path $env:TEMP)
{
    $path = $env:TEMP + "\" + [System.IO.Path]::GetRandomFileName() + ".jpg"
    $bitmap.Save($path, $jpegCodec, $ep); Start-Sleep -Milliseconds 250
    Write-Host $path
}
else
{
    Write-Host "Could not save image."
}