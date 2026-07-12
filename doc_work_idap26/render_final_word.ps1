$ErrorActionPreference = 'Stop'

$jobs = @(
    @{
        Doc = 'E:\Downloads\saci_github_pages_site\deliverables\IDAP26_SACI_Graph_Attack_Surface_Final_TR.docx'
        Pdf = 'E:\Downloads\saci_github_pages_site\doc_work_idap26\qa\tr-v7\final.pdf'
    },
    @{
        Doc = 'E:\Downloads\saci_github_pages_site\deliverables\IDAP26_SACI_Graph_Attack_Surface_Final_EN.docx'
        Pdf = 'E:\Downloads\saci_github_pages_site\doc_work_idap26\qa\en-v7\final.pdf'
    }
)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.ScreenUpdating = $false
$word.DisplayAlerts = 0
$word.AutomationSecurity = 3
$word.Options.SaveNormalPrompt = $false

try {
    foreach ($job in $jobs) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $job.Pdf) | Out-Null
        Write-Output "Opening $($job.Doc)"
        $document = $word.Documents.Open($job.Doc, $false, $true, $false)
        try {
            Write-Output "Exporting $($job.Pdf)"
            $document.ExportAsFixedFormat($job.Pdf, 17)
        }
        finally {
            $document.Close($false)
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($document) | Out-Null
        }
    }
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

Write-Output 'Completed both Word PDF exports.'
