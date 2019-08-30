param (
    [string]$app = "com.mtsbyme",
    [int]$sleepTime = 5
)

function Join-String
{
    [CmdletBinding()]
    param
    (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)][string]$String,
        [Parameter(Position = 1)][string]$Delimiter = ""
    )
    BEGIN {$items = @() }
    PROCESS { $items += $String }
    END { return ($items -join $Delimiter) }
}

Clear-Host
$file = "dump_mem.csv"
$separator = ","
Remove-Item $file

$pattern1 = "Private Other:"
$pattern2 = "Native Heap:"

New-Item -Path . -Name $file

"ITERATION,HEAP,PRIVATE" | Add-Content $file

$iter = 1

While($TRUE) {
    $iter | Add-Content $file -NoNewline
    $separator | Add-Content $file -NoNewline
    adb shell dumpsys meminfo $app | Select-String -Pattern $pattern1, $pattern2 | % {$_.ToString().replace($pattern1,"").replace($pattern2, "").trim()} | Join-String $separator | Add-Content $file
    Start-Sleep -Seconds $sleepTime
    $iter = $iter + 1
}