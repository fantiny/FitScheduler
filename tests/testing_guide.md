### http://localhost:8000/api/v1/auth/register

```powershell
$body = @{ email = 'user@example.com'; username = 'testuser'; phone = '1234567890'; is_active = $true; membership_rank = 'STANDARD'; password = 'testpassword123' } | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/register' -Method Post -Body $body -ContentType 'application/json' -ErrorVariable err -ErrorAction SilentlyContinue; if ($err) { Write-Host "Error: $($err.Exception.Message)"; if ($err.Exception.Response) { $reader = [System.IO.StreamReader]::new($err.Exception.Response.GetResponseStream()); $reader.BaseStream.Position = 0; $reader.DiscardBufferedData(); $responseBody = $reader.ReadToEnd(); Write-Host "Response body: $responseBody"; $reader.Close() } } else { Write-Host "Response: $($response.Content)" }
```

### http://localhost:8000/api/v1/auth/login
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/users/me
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/users/me' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/users/me (Update Phone Number)
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $updateBody = @{ phone = '9876543210' } | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/users/me' -Method Patch -Body $updateBody -ContentType 'application/json' -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/venues/
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/venues/' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/venues/1
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/venues/1' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/venues/1/coaches
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/venues/1/coaches' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/coaches/
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/coaches/' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/coaches/1
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/coaches/1' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/reviews/
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/reviews/' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/reviews/1
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/reviews/1' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/bookings/
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/bookings/' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```

### http://localhost:8000/api/v1/bookings/1
```powershell
$form = @{ username = 'user@example.com'; password = 'testpassword123' }; $loginResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/auth/login' -Method Post -Form $form -Headers @{ 'accept' = 'application/json' }; $token = ($loginResponse.Content | ConvertFrom-Json).access_token; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/bookings/1' -Method Get -Headers @{ 'accept' = 'application/json'; 'Authorization' = "Bearer $token" }; Write-Host "Status Code: $($response.StatusCode)"; Write-Host "Response: $($response.Content)"
```
