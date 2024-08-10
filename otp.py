import requests

url = "https://virtual-number.p.rapidapi.com/api/v1/e-sim/view-messages"

querystring = {"countryId":"{+44","number":"757683022"}

headers = {
	"x-rapidapi-key": "8afe3aa9camsh20e9e929b783190p1bbd3bjsnacec6643ff06",
	"x-rapidapi-host": "virtual-number.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
