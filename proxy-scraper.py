import requests

def get_proxy_country(proxy_ip):
    url = f"http://ip-api.com/json/{proxy_ip}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['country']
        else:
            return None
    else:
        return None

def filter_proxies_by_country(input_file, output_file, target_country='Portugal'):
    with open(input_file, 'r') as file:
        proxies = file.readlines()
    
    portuguese_proxies = []

    for proxy in proxies:
        proxy_ip = proxy.strip().split(':')[0]  # Get the part before the ":"
        if proxy_ip:
            country = get_proxy_country(proxy_ip)
            if country == target_country:
                portuguese_proxies.append(proxy.strip())  # Keep the original proxy format
                print(f"{proxy_ip} is from {country}. Keeping it.")
            else:
                print(f"{proxy_ip} is from {country}. Discarding it.")
    
    with open(output_file, 'w') as file:
        for proxy in portuguese_proxies:
            file.write(proxy + '\n')
    
    print(f"Filtered proxies have been saved to {output_file}")

if __name__ == "__main__":
    storage_file = "C:\\Users\\lette\\Desktop\\online-work\\Projects\\web-booking-automation\\Storage-file\\"
    input_file = storage_file+"http.txt"
    output_file = storage_file+"portugal_proxies.txt"
    filter_proxies_by_country(input_file, output_file)
