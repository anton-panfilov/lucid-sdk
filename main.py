import lucid
import redis

login_key = "getLoginKeyFromEnv"
rds = redis.Redis(host='localhost', port=6379, db=3, decode_responses=True)
token_name = 'LucidToken'

lucid_sdk = lucid.Sdk(
    login_key=login_key,
    token=rds.get(token_name),
    save_token_trigger=lambda value, ex=60: rds.set(token_name, str(value), ex=ex)
)

res = lucid_sdk.payday_score({
    "clientIP": "18.221.221.179",
    "userAgent": "mozilla/5.0 (macintosh; intel mac os x 10_12_6) applewebkit/537.36 (khtml like gecko) chrome/89.0.4",
    "loanAmount": "500",
    "loanPurpose": "debt_consolidation",
    "creditScore": "good",
    "email": "buzz.aldrin@nasa.com",
    "dob": "1999-11-28",
    "zip": "90405",
    "state": "CA",
    "monthsAtAddress": 24,
    "homeOwnership": "rent",
    "driversLicenseState": "CA",
    "cellPhone": "8182345432",
    "ssn": "522662633",
    "employmentType": "employed",
    "employerName": "Space Exploration Technologies Corp.",
    "military": 0,
    "monthsEmployed": 3,
    "monthlyIncome": "1200",
    "payFrequency": "biweekly",
    "nextPayDate": "2021-11-12",
    "payType": "direct_deposit",
    "bankRoutingNumber": "121122676",
    "bankName": "Bank of America",
    "bankAccountType": "checking",
    "monthsAtBank": 50
})

print('value: ' + str(res['value']))
print('prob: ' + str(res['prob']))
