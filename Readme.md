Invoke-WebRequest -Uri "http://127.0.0.1:8000/oauth2/token/" `
                  -Method POST `
                  -Body "grant_type=password&username=javier&password=elpepe34&client_id=loloid&client_secret=lolosecreto" `
                  -ContentType "application/x-www-form-urlencoded"