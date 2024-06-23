import requests


# Start inference job (POST /v0/batch/jobs)
def createJob():
    response = requests.post(
    "https://api.hume.ai/v0/batch/jobs",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT",
        "Content-Type": "application/json"
    },
    json={
        "notify": False,
        "text": [
        "today apple released final cut pro for ipad 2 transforming ipad into an even more powerful production studio, and final cut pro for mac 10.8"
        ],
        "models": {
        "language": {
            "granularity": "sentence",
            "sentiment": {},
            "toxicity": {}
        }
        }
    },
    )
    data = response.json()
    print(data["job_id"])
    return data["job_id"]


def jobStatusCheck(job_id):
    response = requests.get(
    f"https://api.hume.ai/v0/batch/jobs/{job_id}",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT"
    },
    )
    data = response.json()
    #print(data)
    return data["state"]["status"]

def getHighests(job_id):
    # Get job predictions (GET /v0/batch/jobs/:id/predictions)
    response = requests.get(
    f"https://api.hume.ai/v0/batch/jobs/{job_id}/predictions",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT"
    },
    )
    emotions = response.json()[0]['results']['predictions'][0]['models']['language']['grouped_predictions'][0]['predictions'][0]['emotions']
    
    sentiments = response.json()[0]['results']['predictions'][0]['models']['language']['grouped_predictions'][0]['predictions'][0]['sentiment']

    print(overallPosOrNeg(emotions))

    print(_getHighest(sentiments))


def _getHighest(para):
    highest_emotion = max(para, key=lambda para: para['score'])
    return highest_emotion

def overallPosOrNeg(emotions):
    weight = [1,1,0,0,-2,-1,-1,1.5,-1,0,0,1,-1.5,0,-1.5,1,1,0,1.5,-1.5,-1,-1.5,-1.5,-2,1.5,-1.5,-1,1.5,0,0,2,-1,1,0,0,1.5,1.5,1,0,-1,1,0,0,0,-1,0,1,-1,-1,1,0,0,2]
    score = 0
    for ind in range(len(emotions)):
        score += weight[ind] * emotions[ind]["score"]
    return score

    
job_id = createJob()
while jobStatusCheck(job_id) == "IN_PROGRESS":
    pass
print(jobStatusCheck(job_id))
print(getHighests(job_id))



"""
emotions --> > 0 = positive
sentiments --> 
"""
