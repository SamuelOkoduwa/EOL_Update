import requests

# Set your API key and Port organization details
API_KEY = 'api_key_here'
ORG_ID = 'org_id_here'
PORT_API_BASE_URL = 'https://api.getport.io'

# Function to get all service entities
def get_services():
    url = f"{PORT_API_BASE_URL}/v1/orgs/{ORG_ID}/services"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to get all framework entities
def get_frameworks():
    url = f"{PORT_API_BASE_URL}/v1/orgs/{ORG_ID}/frameworks"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to update the number of EOL packages for a service
def update_service_eol_count(service_id, eol_count):
    url = f"{PORT_API_BASE_URL}/v1/orgs/{ORG_ID}/services/{service_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"numberOfEOLPackages": eol_count}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Main function to calculate and update EOL packages
def main():
    services = get_services()
    frameworks = get_frameworks()

    # Create a dictionary of frameworks with their states
    framework_state = {fw['id']: fw['state'] for fw in frameworks}

    for service in services:
        eol_count = 0
        for framework_id in service['frameworks']:
            if framework_state.get(framework_id) == 'EOL':
                eol_count += 1
        # Update the service with the calculated EOL count
        update_service_eol_count(service['id'], eol_count)
        print(f"Updated service {service['name']} with {eol_count} EOL packages")

if __name__ == "__main__":
    main()

